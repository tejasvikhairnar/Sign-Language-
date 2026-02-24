import cv2
import numpy as np
import mediapipe as mp
from sklearn.neighbors import KNeighborsClassifier
from collections import deque, Counter
import string
import time
import pyttsx3
import threading

# =========================
# Load dataset
# =========================
X = np.load("X_raw.npy")
y = np.load("y_raw.npy")

idx_to_label = {i: letter for i, letter in enumerate(string.ascii_lowercase)}

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
# Buffers for prediction + word building
# =========================
pred_history = deque(maxlen=7)
stable_letter = ""           
stable_start_time = None     
final_string = ""

# =========================
# TTS Setup (Google Translate style)
# =========================
engine = pyttsx3.init()
tts_lock = threading.Lock()

def speak_text(text):
    def run_speech():
        with tts_lock:
            engine.stop()       # stop any ongoing speech instantly
            engine.say(text)
            engine.runAndWait()
    threading.Thread(target=run_speech, daemon=True).start()

# =========================
# Mouse callback for speaker button
# =========================
def mouse_callback(event, x, y, flags, param):
    global final_string
    if event == cv2.EVENT_LBUTTONDOWN:
        h, w, _ = param.shape
        bx1, by1 = w - 120, h - 60
        bx2, by2 = w - 20, h - 20
        if bx1 <= x <= bx2 and by1 <= y <= by2:
            if final_string.strip() != "":
                speak_text(final_string)  # instant speak

# =========================
# Webcam
# =========================
cap = cv2.VideoCapture(0)
cv2.namedWindow("Live Prediction Typing")

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

        if len(result.multi_hand_landmarks) == 1:
            landmarks_all_hands.extend([0.0] * (21 * 3))

        if len(landmarks_all_hands) < 126:
            landmarks_all_hands.extend([0.0] * (126 - len(landmarks_all_hands)))

        if len(landmarks_all_hands) == 126:
            landmarks_all_hands = np.array(landmarks_all_hands).reshape(1, -1)
            pred_idx = knn.predict(landmarks_all_hands)[0]
            prob = knn.predict_proba(landmarks_all_hands).max()

            pred_letter = idx_to_label.get(pred_idx, "?")

            if prob > 0.8:
                pred_history.append(pred_letter)
                most_common = Counter(pred_history).most_common(1)[0][0]

                if stable_letter != most_common:
                    stable_letter = most_common
                    stable_start_time = time.time()

                prediction_text = f"Stable: {stable_letter} ({prob:.2f})"
                color = (0, 255, 0)
            elif prob > 0.3:
                prediction_text = f"Uncertain ({pred_letter})"
                color = (0, 255, 255)
            else:
                stable_letter = ""
                stable_start_time = None

    # =========================
    # Handle stable timer
    # =========================
    if stable_letter != "" and stable_start_time is not None:
        elapsed = time.time() - stable_start_time
        if elapsed > 3:
            stable_letter = ""
            stable_start_time = None
        else:
            cv2.putText(frame, f"Timer: {3 - int(elapsed)}s",
                        (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 255), 2)

    # =========================
    # Handle keypresses
    # =========================
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == 13:  # Enter key
        if stable_letter != "":
            final_string += stable_letter
            stable_letter = ""
            stable_start_time = None
    elif key == 32:  # Space key
        final_string += " "
    elif key == 8:   # Backspace
        final_string = final_string[:-1]

    # =========================
    # Display predictions
    # =========================
    cv2.putText(frame, prediction_text, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    cv2.putText(frame, f"Stable Letter: {stable_letter}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.putText(frame, f"Word: {final_string}", (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # =========================
    # Draw speaker button (bottom-right)
    # =========================
    h, w, _ = frame.shape
    bx1, by1 = w - 120, h - 60
    bx2, by2 = w - 20, h - 20
    cv2.rectangle(frame, (bx1, by1), (bx2, by2), (0, 255, 0), -1)
    cv2.putText(frame, "Speak", (bx1 + 10, by2 - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    cv2.setMouseCallback("Live Prediction Typing", mouse_callback, frame)

    cv2.imshow("Live Prediction Typing", frame)

cap.release()
cv2.destroyAllWindows()
