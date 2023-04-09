import cv2
import numpy as np
import pyautogui
#failsafe bypass
pyautogui.FAILSAFE = False
class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # directshow api
        cv2.namedWindow("CameraWindow",cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("CameraWindow",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    def get_frame(self):
        s, img = self.cap.read()
        if s:
            pass
        return img
    def release_camera(self):
        self.cap.release()
        cv2.destroyAllWindows()
def main():
    cam = Camera()
    # centers mouse
    pyautogui.moveTo((1920/2),(1080/2))
    while True:
        frame = cam.get_frame()
        # converts img to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detects faces
        faces = cam.face_cascade.detectMultiScale(gray, 1.07, 7)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)
            #centers to camera
            cx, cy = (x+w//2)*3, (y+h//2)*1.75
            pyautogui.moveTo(cx,cy)
            roi_gray = gray[y:y+w, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = cam.eye_cascade.detectMultiScale(roi_gray, 1.07, 4)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)

        cv2.imshow('CameraWindow', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cam.release_camera()
if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()
#write and read to serial port between programs.
#udp broadcast?
