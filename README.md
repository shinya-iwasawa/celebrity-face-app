# Celebrity Face Recognition App

This is a web application that allows users to upload images of celebrities and have them identified using facial recognition.

## Features

*   Upload images of celebrities
*   Facial recognition to identify the celebrity
*   View a gallery of identified celebrities

## Technologies Used
*   **Backend:**
    *   Python (Flask)
*   **AI Library:**
    *   deepface (SFace model)
*   **Core Libraries:**
    *   OpenCV
    *   NumPy
    *   SciPy
*   **Note:** This is a simple, server-rendered application. It does NOT use a separate frontend framework like React or a database like SQLAlchemy.

## Setup and Installation

### Prerequisites
*   Python 3.x

### Installation
1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd celebrity-face-recognition-app
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application
1.  Activate your virtual environment (if not already active):
    ```bash
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
2.  Run the Flask application:
    ```bash
    python app.py
    ```
3.  Open your web browser and navigate to `http://127.0.0.1:5000` (or the address shown in your console).

## Development Process & Technical Challenges

This project presented several interesting challenges during its development, particularly concerning deployment and packaging, which ultimately shaped its final form.

### Challenge 1: Memory Limits on Cloud Deployment (Render Free Tier)

Our initial goal was to deploy the application on Render's free tier to make it easily accessible. However, we quickly encountered significant hurdles, primarily in the form of `HTTP 502` errors and frequent `out-of-memory` crashes. Investigation revealed that the combination of `deepface` and its underlying `tensorflow` AI libraries demanded more than the 512MB RAM limit imposed by the free plan.

To mitigate this, we implemented two key solutions:
1.  **AI Model Optimization:** We switched from the resource-intensive `VGG-Face` model to the more lightweight `SFace` model within the `deepface` library. This significantly reduced the memory footprint.
2.  **Gunicorn Tuning:** We configured the `gunicorn` web server to use only a single worker (`--workers 1`) and increased the startup timeout to accommodate the AI model's loading time.

Despite these optimizations, the fundamental memory constraints of the free tier proved insurmountable for the application's AI components.

### Challenge 2: Application Packaging with PyInstaller

Concurrently, we explored packaging the application into a single, easy-to-use executable file using PyInstaller. This endeavor, performed within a Colab environment, introduced its own set of complex build errors, largely due to the massive size and intricate dependencies of TensorFlow.

We successfully debugged and resolved several specific issues, including:
*   `RecursionError`: This was addressed by modifying the PyInstaller `.spec` file to increase the recursion limit.
*   Various `SyntaxError` issues: These were typically resolved by ensuring correct Python versions and dependency compatibility.

However, we ultimately hit a fundamental `AttributeError` within PyInstaller's internal hooks, indicating a deep incompatibility with the build environment that was beyond a straightforward fix.

### Final Conclusion & Pivot

These experiences led to a crucial realization: deploying and packaging a Python application with heavy AI dependencies like TensorFlow are non-trivial challenges, especially when constrained by free-tier cloud resources or complex build environments.

Consequently, we decided to pivot the final deliverable. Instead of focusing on cloud deployment or a standalone executable, the project now emphasizes a robust, well-documented local demonstration. This approach perfectly showcases the application's core celebrity face recognition functionality without being hindered by external infrastructure limitations, providing a clear and effective proof of concept.
