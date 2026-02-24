# SLR Project (Sign Language Recognition)

This project is a Sign Language Recognition system that uses computer vision to detect hand gestures and translate them into text and speech. It features a modern Next.js frontend and a Python Flask backend.

## Features
-   **Real-time Hand Tracking**: Uses MediaPipe to detect hand landmarks.
-   **Gesture Classification**: Uses a K-Nearest Neighbors (KNN) algorithm to classify gestures.
-   **Modern UI**: A responsive and professional frontend built with Next.js and Tailwind CSS.
-   **Text-to-Speech**: Converts the recognized text into speech.

## Prerequisites
-   **Python 3.8+**
-   **Node.js 18+** & **npm**
-   **Webcam**

## Installation & Setup

### 1. Backend Setup (Flask)
The backend handles the video processing and machine learning model.

1.  Navigate to the project root.
2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    # source venv/bin/activate # macOS/Linux
    ```
3.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### 2. Frontend Setup (Next.js)
The frontend provides the user interface.

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  **Install Node.js dependencies**:
    ```bash
    npm install
    ```

## How to Run (Recommended)

We have created a simple **One-Click Start Script** for Windows.

1.  Double-click **`start_project.bat`** in the main folder.
2.  It will automatically:
    -   Check if Python and npm are installed.
    -   Start the Backend Server.
    -   Start the Frontend Server.
    -   Open the Dashboard in your default browser.

---

## Technical Details

-   **Backend**: Flask running on `http://127.0.0.1:5000`
-   **Frontend**: Next.js running on `http://localhost:3000`
-   **Communication**: The frontend uses Next.js rewrites to proxy API requests to the backend, avoiding CORS issues.

## Troubleshooting
-   **Webcam not found**: Ensure no other app is using the camera.
-   **Backend connection failed**: Make sure the Flask app is running on port 5000.
