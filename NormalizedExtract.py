import cv2
import os
import numpy as np
import mediapipe as mp
import string

# Path to your dataset
DATASET_DIR = r"C:\Users\91773\OneDrive\Desktop\SLR Project with premade dataset\Dataset ISL"

# Initialize Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Mediapipe Hands setup
hands = mp_hands.Hands(
    static_image_mode=True, 
    max_num_hands=2, 
    min_detection_confidence=0.5
)

X, y = [], []

# Labels (A-Z)
labels = list(string.ascii_uppercase)

def normalize_landmarks(landmarks):
    """Normalize landmarks for scale and translation invariance"""
    landmarks = np.array(landmarks)
    # Subtract mean (centering)
    landmarks -= np.mean(landmarks, axis=0)
    # Scale to unit norm
    max_val = np.max(np.linalg.norm(landmarks, axis=1))
    if max_val > 0:
        landmarks /= max_val
    return landmarks.flatten()

# Loop through dataset folders
for label in labels:
    folder = os.path.join(DATASET_DIR, label)
    if not os.path.exists(folder):
        print(f"Skipping missing folder: {folder}")
        continue

    print(f"Processing {label}...")

    for img_file in os.listdir(folder):
        img_path = os.path.join(folder, img_file)
        img = cv2.imread(img_path)

        if img is None:
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            all_landmarks = []

            for hand_landmarks in results.multi_hand_landmarks:
                single_hand = []
                for lm in hand_landmarks.landmark:
                    single_hand.append([lm.x, lm.y, lm.z])
                all_landmarks.extend(single_hand)

            # If only one hand detected → pad with zeros (21 landmarks * 3 = 63 features)
            if len(results.multi_hand_landmarks) == 1:
                all_landmarks.extend([[0, 0, 0]] * 21)

            # Normalize & store
            norm_landmarks = normalize_landmarks(all_landmarks)
            X.append(norm_landmarks)
            y.append(label)

# Save arrays
X = np.array(X)
y = np.array(y)

np.save("X.npy", X)
np.save("y.npy", y)

print("✅ Dataset extraction complete!")
print("X shape:", X.shape)
print("y shape:", y.shape)
