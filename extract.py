import cv2
import os
import numpy as np
import mediapipe as mp

# Path to your dataset
DATASET_DIR = r"C:\Users\91773\OneDrive\Desktop\SLR Project with premade dataset\Dataset ISL"

# MediaPipe Hands setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)

X_raw = []  # Landmark data
y_raw = []  # Labels
labels_dict = {letter: idx for idx, letter in enumerate(sorted(os.listdir(DATASET_DIR)))}

# Loop through each folder (a-z)
for label in sorted(os.listdir(DATASET_DIR)):
    folder_path = os.path.join(DATASET_DIR, label)
    if not os.path.isdir(folder_path):
        continue

    print(f"Processing: {label}")

    # Loop through images in the folder
    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)

        # Read image
        image = cv2.imread(img_path)
        if image is None:
            continue

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        # Prepare a container for both hands (126 values: 2 hands × 21 landmarks × 3 coords)
        landmarks_all_hands = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.extend([lm.x, lm.y, lm.z])
                landmarks_all_hands.extend(landmarks)

            # If only one hand detected, pad with zeros for the other hand
            if len(results.multi_hand_landmarks) == 1:
                landmarks_all_hands.extend([0.0] * (21 * 3))
        else:
            # No hands detected → pad both hands with zeros
            landmarks_all_hands.extend([0.0] * (2 * 21 * 3))

        X_raw.append(landmarks_all_hands)
        y_raw.append(labels_dict[label])

hands.close()

# Convert to NumPy arrays
X_raw = np.array(X_raw)
y_raw= np.array(y_raw)

# Save arrays
np.save("X_raw.npy", X_raw)
np.save("y_raw.npy", y_raw)

print(f"Saved landmark data: {X_raw.shape} features, {y_raw.shape} labels")
