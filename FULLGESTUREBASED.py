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
# Load dataset + KNN
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
# Buffers + sentence
# =========================
pred_history = deque(maxlen=7)
stable_letter = ""
stable_start_time = None
final_string = ""

# Gesture buffers
last_space_time = 0
last_next_time = 0
space_cooldown = 0.5
next_cooldown = 0.5
open_palm_count = 0
palm_last_seen = 0

# =========================
# TTS Function
# =========================
def speak_text(text):
    def run_speech():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    threading.Thread(target=run_speech, daemon=True).start()

# =========================
# Gesture heuristics
# =========================
def is_fist(hand_landmarks):
    tips = [8, 12, 16, 20]  # fingertips
    pips = [6, 10, 14, 18]  # middle joints
    folded = 0
    for tip, pip in zip(tips, pips):
        if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y:
            folded += 1
    return folded == 4

def is_open_palm(hand_landmarks):
    x_coords = [lm.x for lm in hand_landmarks.landmark]
    y_coords = [lm.y for lm in hand_landmarks.landmark]
    spread = (max(x_coords)-min(x_coords)) + (max(y_coords)-min(y_coords))
    return spread > 1.5  # adjust threshold as needed

# =========================
# Webcam loop
# =========================
cap = cv2.VideoCapture(0)
cv2.namedWindow("Gesture Typing")

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

    gesture_space = False
    gesture_next = False

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check gestures first
            if is_open_palm(hand_landmarks):
                gesture_space = True
            if is_fist(hand_landmarks):
                gesture_next = True

            # Extract landmarks
            for lm in hand_landmarks.landmark:
                landmarks_all_hands.extend([lm.x, lm.y, lm.z])

        # Pad to 126 features
        if len(result.multi_hand_landmarks) == 1:
            landmarks_all_hands.extend([0.0] * (21*3))
        if len(landmarks_all_hands) < 126:
            landmarks_all_hands.extend([0.0] * (126 - len(landmarks_all_hands)))

        # Predict letter
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
    # Stable letter timer
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
    # Gesture-based actions with buffers
    # =========================
    current_time = time.time()

    if gesture_space:
        if current_time - palm_last_seen > 0.7:  # reset if gap > 0.7s
            open_palm_count = 0
        open_palm_count += 1
        palm_last_seen = current_time

        if open_palm_count == 2 and current_time - last_space_time > space_cooldown:
            if len(final_string) == 0 or final_string[-1] != " ":
                final_string += " "
            last_space_time = current_time
            open_palm_count = 0

    elif gesture_next and current_time - last_next_time > next_cooldown:
        if stable_letter != "":
            final_string += stable_letter
            stable_letter = ""
            stable_start_time = None
        last_next_time = current_time
        open_palm_count = 0

    else:
        if current_time - palm_last_seen > 0.7:
            open_palm_count = 0

    # =========================
    # Keypresses
    # =========================
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        if final_string.strip() != "":
            speak_text(final_string)
    elif key == 8:  # Backspace
        final_string = final_string[:-1]

    # =========================
    # Display
    # =========================
    cv2.putText(frame, prediction_text, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
    cv2.putText(frame, f"Stable Letter: {stable_letter}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.putText(frame, f"Sentence: {final_string}", (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Gesture Typing", frame)

cap.release()
cv2.destroyAllWindows()
