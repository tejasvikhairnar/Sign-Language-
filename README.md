# SLR Project (Sign Language Recognition)

This project is a high-accuracy Sign Language Recognition system that uses independent hand normalization and an Extra Trees Classifier to translate hand gestures into text and speech in real-time.

## Features
-   **99.5% Accuracy**: Optimized model with wrist-relative normalization.
-   **Real-time Hand Tracking**: Powered by MediaPipe.
-   **Ensemble ML Model**: High-performance Extra Trees Classifier.
-   **Full-Stack UI**: Modern Next.js interface with speech synthesis.

## Prerequisites
-   **Python 3.8**: Required specifically for MediaPipe compatibility in this environment.
-   **Node.js 18+** & **npm**
-   **Webcam**

## Installation & Setup

### 1. Backend Setup
1.  Navigate to the project root.
2.  Install dependencies: `pip install -r requirements.txt` (Ensure you use Python 3.8).

### 2. Frontend Setup
1.  Navigate to `/frontend`.
2.  Install dependencies: `npm install`.

## How to Run

### Local Execution (Recommended)
Double-click **`start_project.bat`**. This script will:
-   Launch the Flask backend (`final_backend.py`) on port 5000.
-   Launch the Next.js frontend on port 3000.
-   Open the Dashboard automatically.

### Running with Netlify/Vercel (Public Deployment)
Since the backend requires a physical webcam and high-performance execution, we use a hybrid deployment:
1.  **Frontend**: Deploy the `frontend/` folder to Vercel or Netlify.
2.  **Backend Tunnel**: Run your backend locally and bridge it using:
    -   Double-click **`start_tunnel.bat`**.
    -   Copy the public URL provided.
3.  **Config**: Set `NEXT_PUBLIC_API_URL` in Vercel/Netlify settings to that URL.

---

## Technical Details
-   **Recognition Engine**: Extra Trees Classifier trained on 25k+ optimized frames.
-   **Normalization**: Independent hand scaling for translation/scale invariance.
-   **Backend**: Flask / Port 5000.
-   **Frontend**: Next.js / Port 3000.
