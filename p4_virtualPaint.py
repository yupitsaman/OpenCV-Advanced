# Project 4
# Virtual Paint
# Selection using index and middle fingers
# Drawing using index finger

import cv2
import numpy as np
import os
import time
from handTrackModule import handDetector

w, h = 860, 600
brushThickness = 10
eraserThickness = 40
pTime = 0


folderPath = "OpenCV/Advanced/Media/Header"
myList = os.listdir(folderPath)
# print(myList)
# Images have same width as of camera             860*84
overLay = []
for imPath in myList :
    image = cv2.imread(f'{folderPath}/{imPath}')
    overLay.append(image)
# print(len(overLay))
header = overLay[0]

# Initially the drawColor is first color
drawColor = (120, 9, 239)
xp, yp = 0, 0

# We'll draw on a different image
imgCanvas = np.zeros((h, w, 3), np.uint8)


detector = handDetector(detectCon = 0.85)


cap = cv2.VideoCapture(0)

while True :
    success, img = cap.read()
    img = cv2.resize(img, (w, h))
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0 :
        # print(lmList)

        # Getting the landmarks for index and middle finger
        x1, y1 = lmList[8][1:3]
        x2, y2 = lmList[12][1:3]

        # Finding which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)

        # Selection mode
        if fingers[1] and fingers[2] :
            xp, yp = 0, 0
            # print("Selection mode")

            if y1 < 84 :
                if 124 < x1 < 261 :
                    header = overLay[0]
                    drawColor = (120, 9, 239)
                elif 292 < x1 < 434 :
                    header = overLay[1]
                    drawColor = (255, 113, 82)
                elif 471 < x1 < 613 :
                    header = overLay[2]
                    drawColor = (57, 123, 2)
                elif 666 < x1 < 813 :
                    header = overLay[3]
                    drawColor = (0, 0, 0)

            cv2.rectangle(img, (x1, y1-25), (x2, y2+25), drawColor, cv2.FILLED)

        # Drawing mode
        if fingers[1] and fingers[2] == False :
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            # print("Drawing mode")

            if xp == 0 and yp == 0 :
                xp , yp = x1, y1

            if drawColor == (0, 0, 0) :
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)

            cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

    # Changing the drawing to black and canvas to white
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    
    # Changing the canvas back to bgr to merge
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    # Merging
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Overlaying the header images
    img[0:84, 0:w] = header

    # Getting the frame rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'fps : {int(fps)}', (0, h-20), cv2.FONT_HERSHEY_COMPLEX, 1, drawColor, 2)

    cv2.imshow("Camera", img)
    # cv2.imshow("Canvas", imgCanvas)
    if cv2.waitKey(1) & 0xFF == ord('q') :
        break