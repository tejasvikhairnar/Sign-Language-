import cv2
import numpy as np
import mediapipe as mp
from sklearn.neighbors import KNeighborsClassifier
from collections import deque, Counter
import string

# =========================
# Load dataset
# =========================
X = np.load("X_raw.npy")
y = np.load("y_raw.npy")

# Map indices to letters (0->a, 1->b, ..., 25->z)
idx_to_label = {i: letter for i, letter in enumerate(string.ascii_lowercase)}

# Train classifier
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

# =========================
# Mediapipe setup
# =========================
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=2
)

# =========================
# Rolling window buffer
# =========================
pred_history = deque(maxlen=7)  # smooth predictions over last 7 frames

# =========================
# Webcam
# =========================
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    prediction_text = "No Hand"
    color = (0, 0, 255)
    landmarks_all_hands = []

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            for lm in hand_landmarks.landmark:
                landmarks_all_hands.extend([lm.x, lm.y, lm.z])

        # Pad if only one hand detected
        if len(result.multi_hand_landmarks) == 1:
            landmarks_all_hands.extend([0.0] * (21 * 3))

        # Make sure vector length is always 126
        if len(landmarks_all_hands) < 126:
            landmarks_all_hands.extend([0.0] * (126 - len(landmarks_all_hands)))

        if len(landmarks_all_hands) == 126:
            landmarks_all_hands = np.array(landmarks_all_hands).reshape(1, -1)
            pred_idx = knn.predict(landmarks_all_hands)[0]
            prob = knn.predict_proba(landmarks_all_hands).max()

            pred_letter = idx_to_label.get(pred_idx, "?")

            # Only accept high-confidence predictions
            if prob > 0.7:
                pred_history.append(pred_letter)

                # Majority vote from history
                most_common = Counter(pred_history).most_common(1)[0][0]

                prediction_text = f"Prediction: {most_common} ({prob:.2f})"
                color = (0, 255, 0)
            elif prob > 0.3:
                prediction_text = f"Uncertain ({pred_letter})"
                color = (0, 255, 255)

    cv2.putText(frame, prediction_text, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    cv2.imshow("Live Prediction", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
