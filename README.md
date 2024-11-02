# GestureX

GestureX is an Indian Sign Language (ISL) recognition system aimed at improving communication accessibility for the deaf and mute community by translating hand gestures into text in real-time. Leveraging advanced machine learning models, GestureX provides reliable gesture detection, auto-correction, and text-to-speech functionality, accessible through an intuitive web interface.

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license) 

---

## Overview

GestureX enables users to detect and translate Indian Sign Language gestures into text, with on-demand options for multilingual support, auto-correction, and text-to-speech conversion. The platform combines TensorFlow's Object Detection API with Flask, making it easy to integrate with other applications.

## Key Features

- *Real-Time Gesture Detection*: Accurate and responsive ISL gesture-to-text translation.
- *On-Demand Auto-Correction*: Agent-based auto-correction for enhanced detection accuracy.
- *Text-to-Speech*: Convert translated text to speech for a smoother user experience.
- *Multilingual Support*: Option to translate gestures into multiple languages.
- *User -Friendly Interface*: Simple, responsive web interface for all users.

---

## Technology Stack

- *Frontend*: HTML, CSS, JavaScript
- *Backend*: Flask
- *Machine Learning*: TensorFlow (Object Detection Code)

---

## Installation

### Prerequisites
- Python 3.8+

### Steps

1. *Clone the repository*
   bash
   git clone https://github.com/nawabkh2040/GestureX.git
   cd GestureX

2. **Set up a virtual environment (recommended)**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. *Install required Python libraries*

    ```bash
    pip install -r requirements.txt
    ```
4. **Start the Application**
    ```bash
    python app.py
    ```
5. *Access:* Open http://localhost:5000 in your browser.

### Usage 
1. Launch the application via flask run. 
2. Navigate to http://localhost:5000 and use the interface to detect, correct, and translate ISL gestures.
3. Use the API endpoints below for custom integrations and real-time detection requests.
#### API Endpoints

| Endpoint              | Method | Description                               |
|-----------------------|--------|-------------------------------------------|
| /detect             | POST   | Detects gestures and returns text         |
| /auto_correct       | POST   | Provides auto-corrected detection         |
| /text_to_speech     | POST   | Converts translated text to speech        |
| /multilingual       | POST   | Translates detected text into languages   |
| /upload_model       | POST   | Uploads a custom model for detection      |
| /history            | GET    | Retrieves gesture detection history       |

### Project Structure

GestureX/
│
├── models/                # Contains pre-trained models and custom ISL models
├── flask_app/             # Backend code
|── app.py                 # Main Flask application file
├── templates/             # HTML templates
├── Tensorflow/            # Tensorflow Object Detection Model
├── static/                # CSS, JavaScript, and images                     
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
### Contributing
We welcome contributions to improve GestureX! Here’s how you can contribute:

1. Fork the repository.
2. Create a branch (e.g., git checkout -b feature/YourFeature).
3. Commit your changes (e.g., git commit -m 'Add new feature').
4. Push to the branch (e.g., git push origin feature/YourFeature).
5. Create a pull request, and we’ll review your changes.
### License
This project is licensed under the MIT License. See the LICENSE file for more information.

Thank you for using GestureX! We’re committed to enhancing communication accessibility for everyone.
