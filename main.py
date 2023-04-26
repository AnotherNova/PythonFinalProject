import cv2
import numpy as np
import pyautogui
from PIL import ImageEnhance 
import dlib

accuracy = 1.04
max_distance = 200

#failsafe bypass
pyautogui.FAILSAFE = False
#does all the frame setup
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
    def enhanceDat(self):
        self.enhancer = enhancer
        enhancer = ImageEnhance.Sharpness(main.frame)
        for i in range(8):
            factor = i / 4.0
            enhancer.enhance(factor).show(f"Sharpness {factor:f}")
def main(q):
    global scaling
    scaling = 15
    cam = Camera()
    # centers mouse
    pyautogui.moveTo((1920/2),(1080/2))
    while True:
        frame = cam.get_frame()
        frame = cv2.flip(frame,1)
        # converts img to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detects faces
        faces = cam.face_cascade.detectMultiScale(gray, accuracy, 7)
        mouse_pos = pyautogui.position()
        mouse_vel = [0, 0]
        if len(faces) > 0:
            largest_face = max(faces, key=lambda f: f[2] * f[3])
            x, y, w, h = largest_face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)
            #centers to camera
            # calculate target mouse position
            target_pos = (x+w//2)*3, (y+h//2)*1.75
            # calculate distance between current and target mouse position
            dist = np.sqrt((target_pos[0]-mouse_pos[0])**2 + (target_pos[1]-mouse_pos[1])**2)
            key = cv2.waitKey(1)
            if key == ord('w'):
                scaling += 5
            elif key == ord('s'):
                scaling -= 5
            if dist > max_distance:
                # calculate mouse velocity proportional to distance
                mouse_vel[0] = (target_pos[0]-mouse_pos[0])/dist * scaling
                mouse_vel[1] = (target_pos[1]-mouse_pos[1])/dist * scaling
                # update mouse position
                mouse_pos = (mouse_pos[0]+mouse_vel[0], mouse_pos[1]+mouse_vel[1])
                # move mouse
                pyautogui.moveTo(mouse_pos, duration = 0.1)
            roi_gray = gray[y:y+w, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            #eyes = cam.eye_cascade.detectMultiScale(roi_gray, accuracy, 4)
            #for (ex, ey, ew, eh) in eyes:
            #   cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)

        # identify thread data
        q.put((mouse_pos))

        cv2.imshow('CameraWindow', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cam.release_camera()
if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()
