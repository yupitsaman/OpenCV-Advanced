# Project 2
# Finger counter

import cv2
import time 
import os
from handTrackModule import handDetector


wCam, hCam = 740, 580
pTime = 0


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)


folderPath = "OpenCV/Advanced/Media/FingerImages"
myList = os.listdir(folderPath)                                            # List of all the images
# print(myList)

# List of the paths of all the images
overlay = []   

for imPath in myList :
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    overlay.append(image)
# print(len(overlay))


detector = handDetector()
# Tip point of all the fingers
tipIds = [4, 8, 12, 16, 20]      


while True :
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.resize(img, [wCam, hCam])

    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0 :
        # To check if the fingers are closed or open
        # 1 : for open
        # 0 : for closed
        fingers = []                                                                

        # For front right hand and back left hand thumb
        if lmList[17][1] > lmList[1][1] :    
            if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1] :
                fingers.append(1)
            else :
                fingers.append(0)

        # For front left hand and back right hand thumb 
        if lmList[17][1] < lmList[1][1] :             
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1] :
                fingers.append(1)
            else :
                fingers.append(0)

        # For fingers
        for id in range (1, 5) :
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2] :
                fingers.append(1)       
            else :
                fingers.append(0)            
        # print(fingers)

        # To count the number of fingers open
        totalFingers = fingers.count(1)                                                  # Count the number of 1's in fingers
        print(totalFingers)

        # Overlaying the images on original image
        h, w, c = overlay[totalFingers-1].shape
        img[0:h, 0:w] = overlay[totalFingers-1]                                           # overlay[-1] means the last image

        # Showing the count
        cv2.rectangle(img, (20,230),(180,430), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{totalFingers}', (30,420), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 20)

    # Frame rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'fps :{int(fps)}', (580,30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord('q') :
        break