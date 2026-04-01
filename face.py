import cv2

def detect_face():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    cap.release()
    return 1 if ret else 0