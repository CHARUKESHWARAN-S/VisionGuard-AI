# 🔒 VisionGuard AI — Real-Time Face Recognition Security Alert System

**VisionGuard AI** is a real-time security system built using **Flask**, **OpenCV**, and **face_recognition**.  
It identifies known individuals from a webcam feed, captures unknown faces automatically, and sends an **email alert** when 10 unknown detections occur.

---

## ⚙️ Features

- Real-time face recognition via webcam  
- Detects **known** and **unknown** faces instantly  
- Captures screenshots of **unknown** individuals  
- Automatically sends an **email alert** with all unknown images when 10 are detected  
- Supports JSON response for latest detections  

---

## 🧰 Requirements

- Python **3.9 – 3.11**  
- A working **webcam**  
- **CMake** and **C++ build tools** for installing `face_recognition`  

### 🪟 Windows
Install:
- [CMake](https://cmake.org/download/)  
- [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) → select “Desktop development with C++”

### 🍎 macOS
```bash
xcode-select --install
brew install cmake
```

### 🐧 Linux
```bash
sudo apt-get update
sudo apt-get install build-essential cmake libopenblas-dev liblapack-dev
```

---

## 📦 Installation Steps

```bash
# 1️⃣ Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

# 2️⃣ Upgrade pip
python -m pip install --upgrade pip

# 3️⃣ Install dependencies
pip install flask flask-socketio python-dotenv opencv-python numpy face_recognition
```

---

## 🧾 Environment Setup (.env File)

Create a `.env` file in the project root:

```env
# Email credentials (use Gmail App Password)
SENDER_EMAIL=youraddress@gmail.com
RECEIVER_EMAIL=security-team@example.com
SMTP_USERNAME=youraddress@gmail.com
SMTP_PASSWORD=your_16_char_gmail_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Screenshot storage folder
IMAGE_FOLDER=static/unknown_faces

# Location name for alert email
ALERT_LOCATION=Chennai
```

> ⚠️ **Do not commit your `.env` file** to GitHub.  
> Use an App Password for Gmail — not your normal account password.

---

## 📸 Preparing Known Faces

Place known person images in the `photos/` folder:

```
photos/
├─ 1.jpg   → "charukesh"
├─ 2.jpg   → "karthi"
├─ 3.jpg   → "sriraam"
└─ 4.jpg   → "kishore"
```

Ensure the names in your script match these individuals.  
Use clear, front-facing, well-lit images for accurate recognition.

---

## ▶️ Running the Application

```bash
# Activate your virtual environment
.venv\Scripts\activate  # Windows
# or
# source .venv/bin/activate  # macOS/Linux

# Run the Flask application
python app.py
```

Then open in your browser:
```
http://localhost:5000/
```

The webcam feed will start, and detections will appear in real time.

---

## 📧 Email Alert Functionality

- The app monitors all unknown face screenshots stored in `IMAGE_FOLDER`.  
- When 10 or more images are detected, the system sends an **email alert** containing:  
  - Timestamp  
  - Location (from `.env`)  
  - Attached images of the intruder(s)  
- After sending, the folder is automatically **cleared** to prepare for new detections.

---

## 🧱 Recommended Project Structure

```
visionguard-ai/
├─ main.py
├─ webpage.py
├─ templates/
│  └─ index.html
│  └─ home.html
│  └─ success.html
├─ screenshots/
├─ static/
│  └─ unknown_faces/
│  └─ styles.css
├─ photos/
│  ├─ 1.jpg
│  ├─ 2.jpg
│  ├─ 3.jpg
│  └─ 4.jpg
├─ .env
├─ requirements.txt
└─ README.md
```

---

## 🛡️ Production Recommendations

- Remove `debug=True` before deploying  
- Use **HTTPS** and authentication for secure access  
- Log detection and email events for auditing  
- Rotate Gmail App Passwords regularly  

---

## 📄 License

Licensed under the **MIT License** — free for personal and commercial use.

---

## 📥 Clone This Repository (Placed Last, as Requested)

```bash
git clone https://github.com/your-username/visionguard-ai.git
cd visionguard-ai
```

> After cloning, follow these steps in order:  
> **Requirements → Installation → Environment Setup → Prepare Known Faces → Run the Application**

