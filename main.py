import cv2
import numpy as np

# frame for the screen
frameHeight = 600
frameWidth = 900
# capturing Video from Webcam
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

cap.set(10,150)
