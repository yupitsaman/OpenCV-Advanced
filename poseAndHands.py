# Hand and Pose Detection
import cv2
import mediapipe as mp
import time
from poseEstModule import poseDetector
from handTrackModule import handDetector


cTime = 0
pTime = 0

detector = poseDetector()
detectorHand = handDetector()
cap = cv2.VideoCapture(0)

while True :
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (640,620))

    img = detector.findPose(img)
    img = detectorHand.findHands(img)
    lmList = detector.findPosition(img)
    lmListHand = detectorHand.findPosition(img)

    # if len(lmList) != 0 :
    #     cv2.circle(img, (lmList[14][1], lmList[14][2]), 5, (0, 255, 0), cv2.FILLED)
    #     print(lmList[14])

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, "fps : "+str(int(fps)), (10,30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("Video",img)

    if cv2.waitKey(1) & 0xFF == ord('q') :
        break