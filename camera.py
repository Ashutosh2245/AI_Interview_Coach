import cv2
import streamlit as st
import time
import numpy as np


def detect_face_live(duration=30):
    """
    Advanced Proctoring: Analyzes focus, center alignment, and eye contact.
    Returns a weighted focus score (0.0 - 1.0).
    """
    # Load Cascades
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("❌ Hardware Error: Camera not found. Please check your connection.")
        return 0.0

    placeholder = st.empty()
    start_time = time.time()

    # Metrics
    frames_with_face = 0
    total_frames = 0
    eye_contact_frames = 0
    centered_frames = 0

    try:
        while time.time() - start_time < duration:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)  # Mirror effect for user comfort
            h, w, _ = frame.shape
            center_x, center_y = w // 2, h // 2

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Histogram equalization for better detection in low light
            gray = cv2.equalizeHist(gray)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            total_frames += 1

            # Default State: RED (Warning)
            status_color = (0, 0, 255)
            info_text = "⚠️ ALERT: FACE NOT CENTERED / NOT FOUND"

            if len(faces) == 1:
                frames_with_face += 1

                for (x, y, fw, fh) in faces:
                    # Calculate Face Center
                    fx, fy = x + fw // 2, y + fh // 2

                    # Check if face is within the 'Center Zone' (20% margin)
                    is_centered = abs(fx - center_x) < (w * 0.2) and abs(fy - center_y) < (h * 0.2)

                    if is_centered:
                        centered_frames += 1
                        status_color = (0, 255, 0)  # GREEN (Safe)
                        info_text = "✅ POSURE: PERFECT"
                    else:
                        status_color = (0, 165, 255)  # ORANGE (Warning)
                        info_text = "⚠️ PLEASE CENTER YOUR FACE"

                    # Draw Face Box
                    cv2.rectangle(frame, (x, y), (x + fw, y + fh), status_color, 2)

                    # Eye Contact Detection
                    roi_gray = gray[y:y + fh, x:x + fw]
                    eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)

                    if len(eyes) >= 2:
                        eye_contact_frames += 1
                        cv2.putText(frame, "👁️ EYE CONTACT: OK", (x, y - 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            elif len(faces) > 1:
                status_color = (0, 0, 255)
                info_text = "🚫 MULTIPLE FACES DETECTED (PROHIBITED)"
                for (x, y, fw, fh) in faces:
                    cv2.rectangle(frame, (x, y), (x + fw, y + fh), (0, 0, 255), 3)

            # UI OVERLAY (Top Bar)
            time_left = int(duration - (time.time() - start_time))
            # camera.py ke loop ke andar:
            cv2.putText(frame, f"TIME: {time_left}s | 🔴 RECORDING LIVE", (20, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255) if status_color == (0, 0, 255) else (0, 255, 0), 2)
            cv2.rectangle(frame, (0, 0), (w, 50), (0, 0, 0), -1)
            cv2.putText(frame, f"TIME: {time_left}s | {info_text}", (20, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Live Focus Percentage
            curr_focus = (frames_with_face / total_frames) * 100
            cv2.putText(frame, f"FOCUS: {int(curr_focus)}%", (w - 150, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            placeholder.image(frame, channels="BGR", use_container_width=True)

    except Exception as e:
        st.error(f"Logic Error: {str(e)}")
    finally:
        cap.release()
        placeholder.empty()

    if total_frames == 0: return 0.0

    # WEIGHTED CALCULATION
    # 50% Face Presence, 30% Eye Contact, 20% Center Alignment
    score = (
            (frames_with_face / total_frames) * 0.5 +
            (eye_contact_frames / total_frames) * 0.3 +
            (centered_frames / total_frames) * 0.2
    )

    return min(score, 1.0)