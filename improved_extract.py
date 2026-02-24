import cv2
import os
import numpy as np
import string
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

# Path to your dataset
DATASET_DIR = r"c:\Users\tejas\Downloads\SLR Project with premade dataset\SLR Project with premade dataset\Dataset ISL"

# Labels (A-Z)
LABELS = list(string.ascii_uppercase)

def get_mp_hands():
    """Helper to initialize MediaPipe in each worker process"""
    try:
        import mediapipe.solutions.hands as mp_hands
    except (ImportError, ModuleNotFoundError, AttributeError):
        from mediapipe.python.solutions import hands as mp_hands
    return mp_hands.Hands(
        static_image_mode=True, 
        max_num_hands=2, 
        min_detection_confidence=0.5
    )

def normalize_hand(hand_landmarks):
    """Normalize a single hand's landmarks relative to the wrist (landmark 0)"""
    landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
    
    # Translation invariance: subtract wrist coordinates
    wrist = landmarks[0]
    landmarks -= wrist
    
    # Scale invariance: divide by the max distance from wrist
    max_dist = np.max(np.linalg.norm(landmarks, axis=1))
    if max_dist > 0:
        landmarks /= max_dist
        
    return landmarks.flatten() # 63 features

def process_folder(label):
    """Process all images in a specific label folder"""
    folder = os.path.join(DATASET_DIR, label.lower())
    if not os.path.exists(folder):
        return [], []

    hands_tool = get_mp_hands()
    local_X, local_y = [], []
    
    print(f"Starting Folder: {label}")
    image_files = os.listdir(folder)
    
    for img_file in image_files:
        img_path = os.path.join(folder, img_file)
        img = cv2.imread(img_path)
        if img is None:
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands_tool.process(img_rgb)

        if results.multi_hand_landmarks:
            all_features = []
            # Sort hands by x to ensure consistency
            sorted_hands = sorted(results.multi_hand_landmarks, key=lambda h: h.landmark[0].x)
            
            for hand_landmarks in sorted_hands:
                all_features.extend(normalize_hand(hand_landmarks))
            
            if len(sorted_hands) == 1:
                all_features.extend([0.0] * 63)
            
            all_features = all_features[:126]
            local_X.append(all_features)
            local_y.append(label)
            
    hands_tool.close()
    print(f"Finished Folder: {label} ({len(local_X)} samples)")
    return local_X, local_y

if __name__ == "__main__":
    start_total = time.time()
    X, y = [], []

    # Use multiprocessing to process folders in parallel
    # We use max_workers=None to use all available cores (8 detected earlier)
    with ProcessPoolExecutor(max_workers=None) as executor:
        futures = {executor.submit(process_folder, label): label for label in LABELS}
        
        for future in as_completed(futures):
            label = futures[future]
            try:
                folder_X, folder_y = future.result()
                X.extend(folder_X)
                y.extend(folder_y)
            except Exception as e:
                print(f"Error processing folder {label}: {e}")

    # Convert to NumPy arrays
    X = np.array(X)
    y = np.array(y)

    # Save arrays
    np.save("X_optimized.npy", X)
    np.save("y_optimized.npy", y)

    print(f"\n✅ Parallel extraction complete in {time.time() - start_total:.2f}s!")
    print("X_optimized shape:", X.shape)
    print("y_optimized shape:", y.shape)
