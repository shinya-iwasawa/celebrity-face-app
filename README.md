# Celebrity Face Recognition App

This is a web application that allows users to upload images of celebrities and have them identified using facial recognition.

## Features

*   Upload images of celebrities
*   Facial recognition to identify the celebrity
*   View a gallery of identified celebrities

## Tech Stack

*   **Frontend:** React, TypeScript
*   **Backend:** FastAPI, Python
*   **Database:** SQLite

## Getting Started

1.  Clone the repository:

    ```bash
    git clone https://github.com/your-username/celebrity-face-recognition-app.git
    ```

2.  Install the dependencies for the frontend:

    ```bash
    cd web
    npm install
    ```

3.  Install the dependencies for the backend:

    ```bash
    cd ../app
    pip install -r requirements.txt
    ```

4.  Run the application:

    ```bash
    # Start the backend server
    uvicorn main:app --reload

    # Start the frontend server
    cd ../web
    npm start
    ```
