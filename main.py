from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO
import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime
import threading
import time
from dotenv import load_dotenv

from flask import send_from_directory
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Email configuration
sender_email = "charukeshwarans@gmail.com"
receiver_email = "charukeshwarans11@gmail.com"
subject = "Security Alert: Unknown Person Detected"
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "charukeshwarans@gmail.com"
smtp_password = "uuac indf nkov rdpf"  # Use your app password here
image_folder = r"C:\Users\mrcha\OneDrive\Desktop\screenshots"
# Load environment variables
load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app)


def send_email_with_images():
    # Get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    location = "Chennai"  # Hardcoded location

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Email body with HTML content (dynamic time and location)
    html_content = f"""
    <html>
  <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333; background-color: #f5f5f5; margin: 0; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 8px; padding: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
      
      <!-- Header -->
      <div style="border-bottom: 1px solid #eaeaea; padding-bottom: 15px; margin-bottom: 20px;">
        <span style="background: #d32f2f; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold; display: inline-block; margin-bottom: 10px;">SECURITY ALERT</span>
        <h2 style="margin: 0; color: #d32f2f;">Unauthorized Access Detected</h2>
      </div>
      
      <!-- Main Content -->
      <p>Dear Security Team,</p>
      <p>Our surveillance system has detected an unknown individual in the monitored area. <strong>Immediate action is required.</strong></p>
      
      <!-- Incident Details Box -->
      <div style="background: #f9f9f9; border-left: 4px solid #d32f2f; padding: 12px 15px; margin: 15px 0; border-radius: 0 4px 4px 0;">
        <p style="margin: 0 0 8px 0; font-weight: bold;">Incident Details:</p>
        <ul style="margin: 5px 0; padding-left: 20px;">
          <li><strong>Time:</strong> {current_time}</li>
          <li><strong>Location:</strong> {location}</li>
        </ul>
      </div>
      
      <p>Please review the attached images for verification and take necessary action.</p>
      <p style="font-weight: bold; color: #d32f2f;">⚠️ This is a high-priority alert.</p>
      
      <!-- Footer -->
      <div style="margin-top: 25px; padding-top: 15px; border-top: 1px solid #eaeaea; font-size: 0.9em; color: #777;">
        <p>Best regards,</p>
        <p><strong>Security Operations Team</strong></p>
        <p style="font-size: 0.8em; margin-top: 5px;">This is an automated alert. Please do not reply.</p>
      </div>
    </div>
  </body>
</html>
    """
    msg.attach(MIMEText(html_content, 'html'))

    # Attach all images from the folder
    image_count = 0
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):  # Check for image files
            image_path = os.path.join(image_folder, filename)
            with open(image_path, 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', f'<image{image_count + 1}>')  # Embed the image in the email
                img.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                msg.attach(img)
                image_count += 1

    print(f"{image_count} images attached.")

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Configuration
IMAGE_FOLDER = "static/unknown_faces"
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# Load known faces
try:
    charukesh_image = face_recognition.load_image_file(r"C:\Users\mrcha\OneDrive\Documents\Face-recognition-attendence-main[1]\Face-recognition-attendence-main\photos\1.jpg")
    charukesh_encoding = face_recognition.face_encodings(charukesh_image)[0]
    
    karthi_image = face_recognition.load_image_file(r"C:\Users\mrcha\OneDrive\Documents\Face-recognition-attendence-main[1]\Face-recognition-attendence-main\photos\2.jpg")
    karthi_encoding = face_recognition.face_encodings(karthi_image)[0]

    sriraam_image = face_recognition.load_image_file(r"C:\Users\mrcha\OneDrive\Documents\Face-recognition-attendence-main[1]\Face-recognition-attendence-main\photos\3.jpg")
    sriraam_encoding = face_recognition.face_encodings(sriraam_image)[0]

    kishore_image = face_recognition.load_image_file(r"C:\Users\mrcha\OneDrive\Documents\Face-recognition-attendence-main[1]\Face-recognition-attendence-main\photos\4.jpg")
    kishore_encoding = face_recognition.face_encodings(kishore_image)[0]

    known_face_encodings = [charukesh_encoding, karthi_encoding, sriraam_encoding, kishore_encoding]
    known_face_names = ["charukesh", "karthi", "sriraam", "kishore"]
except Exception as e:
    print(f"Error loading images: {e}")
    exit()

# Global variables
detected_faces = []
unknown_faces = []
last_email_sent = 0
email_cooldown = 300  # 5 minutes in seconds

def detect_faces():
    global last_email_sent
    
    video_capture = cv2.VideoCapture(0)
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
            
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Recognize faces
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        current_detections = []
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distance)
            
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                current_detections.append(name)
                
                # Draw green box for known faces
                top, right, bottom, left = [v * 4 for v in face_location]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
            else:
                # Unknown face handling
                top, right, bottom, left = [v * 4 for v in face_location]
                
                # Save screenshot
                image_folder = r"C:\Users\mrcha\OneDrive\Desktop\screenshots"
                if not os.path.exists(image_folder):  # Create the directory if it doesn't exist
                    os.makedirs(image_folder)
                screenshot_path = os.path.join(image_folder, f"unknown_face_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                cv2.imwrite(screenshot_path, frame)
                print(f"Screenshot saved: {screenshot_path}")
    
                
                
                # Draw red box for unknown faces
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, "Unknown", (left + 6, bottom - 6), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                # Check if the folder has 10 or more images
                image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
                if len(image_files) >= 10:
                    print("10 images detected. Sending email...")
                    send_email_with_images()
                    # Clear the folder after sending the email
                    for file in image_files:
                        os.remove(os.path.join(image_folder, file))
                    print("Folder cleared.")
                
        # Update detected faces
        detected_faces.clear()
        detected_faces.extend(current_detections)
        
        # Convert frame to JPEG for streaming
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(detect_faces(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_detections')
@app.route('/detections')
def get_detections():
    return jsonify({
        "known_faces": detected_faces,
        "unknown_faces": unknown_faces[-10:]  # Return last 10 unknown faces
    })
@app.route('/favicon.ico')
def favicon():
    return '', 404

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')