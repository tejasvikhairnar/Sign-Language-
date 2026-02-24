import cv2
import numpy as np
import mediapipe as mp
from sklearn.neighbors import KNeighborsClassifier
import string

# Load dataset
X = np.load("X.npy")
y = np.load("y.npy")

# Create index-to-letter mapping (0 -> 'a', 1 -> 'b', ..., 25 -> 'z')
idx_to_label = {i: letter for i, letter in enumerate(string.ascii_lowercase)}

# Train classifier
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=2
)

# Webcam
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

        if len(landmarks_all_hands) == 126:
            landmarks_all_hands = np.array(landmarks_all_hands).reshape(1, -1)
            pred_idx = knn.predict(landmarks_all_hands)[0]
            prob = knn.predict_proba(landmarks_all_hands).max()

            # Map index to letter
            pred_letter = idx_to_label.get(pred_idx, "?")

            prediction_text = f"Prediction: {pred_letter}"
            if prob > 0.8:
                color = (0, 255, 0)
            elif prob > 0.5:
                color = (0, 255, 255)

    cv2.putText(frame, prediction_text, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    cv2.imshow("Live Prediction", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
