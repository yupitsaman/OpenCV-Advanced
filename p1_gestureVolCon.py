# Project 1
# Volume control using hand gestures

import cv2
import numpy as np
import time
import math
from handTrackModule import handDetector
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wCam = 640
hCam = 480
vol = 0
volBar = 400
volPer = 0


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = handDetector()


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()                                                      # To get the volume range

minVol = volRange[0]
maxVol = volRange[1]


while True :
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0 :
        # print(lmList[4], lmList[8])                                                                 # 4 : thumb tip, 8 : index finger tip

        x1, y1 = lmList[4][1], lmList[4][2]        
        x2, y2 = lmList[8][1], lmList[8][2]       
        # To find the centre of the line 
        cx, cy = (x1 + x2)//2, (y1 + y2)//2       

        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 4)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        # To find the length between thumb and finger
        length = math.hypot((x2-x1),(y2-y1))
        # print(length)

        # Hand range 25 to 230
        # Volume range -65 to 0
        # We need to convert hand range to volume
        vol = np.interp(length,[25,230],[minVol, maxVol])
        # print(vol)

        # Changing the hand range to change in volume bar
        volBar = np.interp(length, [25,230],[400,150])

        # Changing the hand range to volume percentage
        volPer = np.interp(length, [25,230],[0,100])

        # To change the master volume
        volume.SetMasterVolumeLevel(vol, None)

        if length < 25 :
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
    
    # Drawing the volume bar
    cv2.rectangle(img, (40,150),(75,400),(255, 0, 0), 3)

    # Showing the change in volume
    cv2.rectangle(img, (40,int(volBar)),(75,400),(255, 0, 0), cv2.FILLED)

    # Volume percentage below volume bar
    cv2.putText(img, f'{int(volPer)}%', (40,430), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)

    cTime = time.time()    
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS : {int(fps)}', (5,20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)

    cv2.imshow("Camera", img)
    if cv2.waitKey(1) & 0xFF == ord('q') :
        break