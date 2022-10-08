# Project 3
# Personal AI Trainer

import cv2
import numpy as np
import time
from poseEstModule import poseDetector

pTime = 0
w, h = 860, 500


cap = cv2.VideoCapture("OpenCV/Advanced/Media/AI Trainer/bicepCurl2.mp4")

detector = poseDetector()
count = 0                                                                                           # To count the number  of curls
# dir == 0 : up
# dir == 1 : down
dir = 0

while True :
    success, img = cap.read()
    # img = cv2.imread("OpenCV/Advanced/Media/AI Trainer/bicepCurl.jpg")
    img = cv2.resize(img, (w, h))

    img = detector.findPose(img, draw = False)
    lmList = detector.findPosition(img)
    if len(lmList) != 0 :
        # Right arm
        # angle = detector.findAngle(img, 12, 14, 16)

        # Left arm
        angle = detector.findAngle(img, 11, 13, 15)

        # Percentage
        per = np.interp(angle, (210, 320), (0, 100))
        # print(angle, per)

        # Bar
        bar = np.interp(per, (0, 100), (450, 100))

        color = (255, 0, 255)
        if per == 100 :
            color = (0, 0, 255)
            if dir == 0 :
                count += 0.5
                dir = 1

        if per == 0 :
            color = (0, 255, 0)
            if dir == 1 :
                count += 0.5
                dir = 0

        print(count)

        # Bar
        cv2.rectangle(img, (770, 100), (825, 450), color, 3)
        cv2.rectangle(img, (770, int(bar)), (825, 450), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (760, 90), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)

        # Showing the number of curls
        cv2.rectangle(img, (0, 350), (150, 500), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(count)}', (30,480), cv2.FONT_HERSHEY_COMPLEX, 5, (255, 0, 0), 8)

    
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'fps : {int(fps)}', (10,30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord('q') :
        break