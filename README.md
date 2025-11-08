# 🔒 VisionGuard AI – Real-Time Face Recognition Security Alert System

A **real-time facial recognition security system** built using **Flask**, **OpenCV**, and **face_recognition**.  
The system continuously monitors a live video feed from a webcam, identifies known individuals, and automatically sends an **email alert with screenshots** when **unknown faces are detected 10 times**.

---

## 🚀 Features

✅ **Live Face Recognition** — Detects and identifies known faces in real-time using your webcam.  
✅ **Unknown Face Detection** — Captures and stores screenshots of unknown individuals.  
✅ **Automated Email Alerts** — Sends a detailed alert email with attached images of unknown persons after 10 detections.  
✅ **Flask Web Interface** — Streams live video feed and shows detection status in a web browser.  
✅ **Secure & Configurable** — Uses environment variables for sensitive data and structured email formatting.  

---

## 🧠 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend** | Python (Flask, Flask-SocketIO) |
| **Face Recognition** | [face_recognition](https://github.com/ageitgey/face_recognition), OpenCV |
| **Email Service** | smtplib (Gmail SMTP) |
| **Frontend** | HTML (Jinja2 Templates) |
| **Utilities** | dotenv, datetime, threading |

---

## 📂 Project Structure

│
├── main.py # Main Flask application
├── templates/
│ └── index.html # Web interface for live video feed
├── static/
│ └── unknown_faces/ # Temporarily stores unknown face images
├── photos/ # Known persons' images for recognition
├── .env # Environment variables (optional)
└── README.md # Project documentation

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/CHARUKESHWARAN-S/VisionGuard-AI.git
cd VisionGuard-AI

### 2️⃣ Create a virtual environment (recommended)

python -m venv venv
venv\Scripts\activate   # For Windows
# or
source venv/bin/activate  # For Mac/Linux
