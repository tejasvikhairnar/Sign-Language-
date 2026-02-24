from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
try:
    import mediapipe.solutions.hands as mp_hands
    import mediapipe.solutions.drawing_utils as mp_draw
except (ImportError, ModuleNotFoundError, AttributeError):
    from mediapipe.python.solutions import hands as mp_hands
    from mediapipe.python.solutions import drawing_utils as mp_draw
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import time
import threading
import pyttsx3
from collections import deque, Counter
import string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# -----------------------------
# Load Dataset and Model
# -----------------------------
try:
    X = np.load("X_raw.npy")
    y = np.load("y_raw.npy")
    idx_to_label = {i: letter for i, letter in enumerate(string.ascii_lowercase)}

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)
    print("Model loaded and trained successfully.")
except Exception as e:
    print(f"Error loading model/data: {e}")
    # Initialize dummy model to prevent crash if files missing
    X = np.zeros((10, 63))
    y = np.zeros(10)
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)

# -----------------------------
# Mediapipe setup
# -----------------------------
# mp_hands = mp.solutions.hands # Already imported
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2)
# mp_draw = mp.solutions.drawing_utils # Already imported

# -----------------------------
# Globals
# -----------------------------
pred_history = deque(maxlen=7)
stable_letter = ""
stable_start_time = None
final_string = ""
prediction_text = "No Hand"
timer_left = 0
last_confirmed_letter = ""

# -----------------------------
# TTS function
# -----------------------------
import pythoncom

def speak_text(text):
    def run_speech():
        try:
            pythoncom.CoInitialize() # Required for COM in threads on Windows
            logging.info(f"TTS: Starting speech for '{text}'")
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            engine.stop()
            logging.info("TTS: Speech completed")
        except Exception as e:
            logging.error(f"TTS Error: {e}")
            print(f"TTS Error: {e}")
    threading.Thread(target=run_speech, daemon=True).start()

# -----------------------------
# Webcam
# -----------------------------
# cap = cv2.VideoCapture(0) # Moved to generate_frames to handle re-connection potentially

# -----------------------------
# Frame Generator
# -----------------------------
import logging

# Configure logging to file
logging.basicConfig(filename='backend_debug.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def generate_frames():
    global stable_letter, stable_start_time, final_string, prediction_text, timer_left, last_confirmed_letter
    
    logging.info("Attempting to open camera index 0...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Try DirectShow for Windows
    
    logging.info(f"Camera open call finished. isOpened: {cap.isOpened()}")
    if not cap.isOpened():
        logging.error("Could not open webcam.")
    
    frame_count = 0

    while True:
        success, frame = cap.read()
        if not success:
            logging.warning("Failed to read frame from webcam.")
            break
        
        frame_count += 1
        if frame_count <= 5:
             logging.info(f"Successfully read frame {frame_count}")
        
        if frame_count % 30 == 0:
             logging.info(f"Processing frame {frame_count}")

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        prediction_text = "No Hand"
        # color = (0, 0, 255) # Unused in frontend stream usually, but good for debug
        landmarks_all_hands = []

        if result.multi_hand_landmarks:
            if frame_count % 10 == 0:
                logging.info("Hand detected by MediaPipe")

            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmarks_all_hands.extend([lm.x, lm.y, lm.z])
        else:
            if frame_count % 30 == 0:
                logging.debug("No hand detected by MediaPipe")

        if not landmarks_all_hands:
            # No hands detected
            if frame_count % 30 == 0:
                logging.debug("No hand detected - skipping prediction")
            stable_letter = ""
            stable_start_time = None
            timer_left = 0
            prediction_text = "No Hand"
            # Optional: Allow re-detection of same letter if hand leaves and comes back?
            # For now, let's keep last_confirmed_letter until a different letter is seen
            # or we can clear it here if we want "A" -> "No Hand" -> "A" to work immediately.
            # User said "continuously", implying holding the sign. 
            # If they remove hand, they likely want to be able to do "A" again.
            last_confirmed_letter = "" 
        else:
            # Pad to 126 features (expected by model, likely 2 hands)
            expected_features = 126
            if len(landmarks_all_hands) < expected_features:
                landmarks_all_hands.extend([0.0] * (expected_features - len(landmarks_all_hands)))
            
            # Truncate if somehow we have more
            landmarks_all_hands = landmarks_all_hands[:expected_features]

            data = np.array(landmarks_all_hands).reshape(1, -1)
            try:
                pred_idx = knn.predict(data)[0]
                prob = knn.predict_proba(data).max()
                pred_letter = idx_to_label.get(pred_idx, "?")
                
                if frame_count % 10 == 0:
                    logging.debug(f"Prediction: {pred_letter} (Prob: {prob:.2f})")

                if prob > 0.7:
                    pred_history.append(pred_letter)
                    most_common = Counter(pred_history).most_common(1)[0][0]

                    if stable_letter != most_common:
                        stable_letter = most_common
                        stable_start_time = time.time()
                        logging.info(f"New stable letter candidate: {stable_letter}")
                    
                    # Check if we already confirmed this letter recently (Repeat Lock)
                    if stable_letter == last_confirmed_letter:
                         prediction_text = f"Confirmed: {stable_letter}"
                         # Do not show timer or countdown
                         stable_start_time = None 
                         timer_left = 0
                    else:
                         prediction_text = f"Stable: {stable_letter} ({prob:.2f})"

                elif prob > 0.3:
                    prediction_text = f"Uncertain ({pred_letter})"
                    stable_letter = ""
                    stable_start_time = None
                    timer_left = 0
                else:
                    stable_letter = ""
                    stable_start_time = None
                    timer_left = 0
            except Exception as e:
                logging.error(f"Prediction Error: {e}")
                print(f"Prediction Error: {e}")

        # Handle stable timer
        if stable_letter and stable_start_time and stable_letter != last_confirmed_letter:
            elapsed = time.time() - stable_start_time
            timer_left = max(0, 3 - int(elapsed))
            if elapsed > 3:
                final_string += stable_letter
                logging.info(f"Letter Confirmed: {stable_letter}")
                last_confirmed_letter = stable_letter # Lock this letter
                stable_letter = ""
                stable_start_time = None
                timer_left = 0
            
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    cap.release()

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    logging.info("Video feed requested")
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/status')
def status():
    global stable_letter, final_string, timer_left
    return jsonify({
        "char": stable_letter if stable_letter else "-",
        "sentence": final_string if final_string else "-",
        "timer": timer_left
    })


@app.route('/clear')
def clear():
    global final_string, stable_letter, stable_start_time
    final_string = ""
    stable_letter = ""
    stable_start_time = None
    return jsonify({"status": "cleared"})


@app.route('/speak')
def speak():
    logging.info(f"Speak request received. Current text: '{final_string}'")
    if final_string.strip():
        speak_text(final_string)
        return jsonify({"status": "spoken", "text": final_string})
    else:
        logging.warning("Speak request ignored: text is empty")
        return jsonify({"status": "ignored", "reason": "empty text"})


@app.route('/add_space')
def add_space():
    global final_string, last_confirmed_letter
    final_string += " "
    last_confirmed_letter = "" # Reset lock so they can type the same letter again if needed
    return jsonify({"status": "space added"})


@app.route('/backspace')
def backspace():
    global final_string, last_confirmed_letter
    if len(final_string) > 0:
        final_string = final_string[:-1]
    last_confirmed_letter = "" # Reset lock to be safe
    return jsonify({"status": "backspaced", "current_string": final_string})


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
