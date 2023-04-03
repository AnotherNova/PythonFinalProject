import cv2
import numpy as np
import pyautogui

# displays webcam using DirectShow API
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# pre-trained face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
# failsafe
pyautogui.FAILSAFE = False


while True:
    ret, frame = cap.read()
    # converts img to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detects faces
    faces = face_cascade.detectMultiScale(gray, 1.07, 7)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)
        # mouse control
        cx,cy = (x//2)*5, (y//2)*5
        pyautogui.moveTo(cx,cy)
        #######################
        roi_gray = gray[y:y+w, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.07, 4)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)

    cv2.imshow('camera', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

#write and read to serial port between programs.
#udp broadcast?
