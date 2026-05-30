import cv2
import matplotlib.pyplot as mpl
import sys
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, image = cap.read()
    cv2.imshow("Cam",image)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release
cv2.destroyAllWindows()




