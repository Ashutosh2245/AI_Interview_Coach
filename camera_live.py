import cv2
import numpy as np
from streamlit_webrtc import VideoTransformerBase
import streamlit as st


class FaceDetector(VideoTransformerBase):
    def __init__(self):
        # Load the cascade once
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.detected_count = 0
        self.total_frames = 0

    def transform(self, frame):
        # Convert frame to ndarray
        img = frame.to_ndarray(format="bgr24")

        # Performance: Grayscale for detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        if len(faces) > 0:
            self.detected_count += 1

        self.total_frames += 1

        # Calculate confidence
        confidence = self.detected_count / self.total_frames

        # CRITICAL: We use a simple attribute instead of session_state here
        # The main app will pull this value from the 'ctx' object
        self.last_confidence = confidence

        # Draw rectangles on the feed
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, f"Conf: {int(confidence * 100)}%", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return img