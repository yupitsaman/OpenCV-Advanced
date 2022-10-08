# Pose estimation module

import cv2
import mediapipe as mp
import time
import math

class poseDetector () :
    # Initialization
    def __init__(self, mode = False, mCom = 1, uppBody = False, smoothLms = True, detectCon = 0.5, trackCon = 0.5) :
        self.mode = mode
        self.mCom = mCom
        self.uppBody = uppBody
        self.smoothLms = smoothLms
        self.detectCon = detectCon
        self.trackCon = trackCon

        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.mCom, self.uppBody, self.smoothLms, self.detectCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findPose(self, img, draw = True) :
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks :
            if draw :
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img

    def findPosition (self, img, draw = False) :
        self.lmList = []

        if self.results.pose_landmarks :
            for id, lm in enumerate(self.results.pose_landmarks.landmark) :
                h, w, c = img.shape

                cx, cy = int(lm.x*w), int(lm.y*h)

                self.lmList.append([id, cx, cy])

                if draw :
                    cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)
        
        return self.lmList

    # To find the angle between three landmarks
    def findAngle(self, img, p1, p2, p3, draw = True) :
        x1, y1 = self.lmList[p1][1:3]
        x2, y2 = self.lmList[p2][1:3]
        x3, y3 = self.lmList[p3][1:3]

        # Angle
        angle = math.degrees(math.atan2(y3-y2, x3-x2) - math.atan2(y1-y2, x1-x2))
        if angle < 0 :
            angle += 360

        if draw :
            # Lines
            cv2.line(img, (x1, y1), (x2, y2), (255,255,255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255,255,255), 3)

            # Circles
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), 2)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 0), 2)
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (255, 0, 0), 2)

            # Angle
            cv2.putText(img, f'{int(angle)}', (x2, y2-20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)

        return angle



def main () :
    cTime = 0
    pTime = 0

    detector = poseDetector()
    cap = cv2.VideoCapture(1)

    while True :
        success, img = cap.read()
        img = cv2.resize(img, (800,520))

        img = detector.findPose(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0 :
            # cv2.circle(img, (lmList[14][1], lmList[14][2]), 5, (0, 255, 0), cv2.FILLED)
            print(lmList[14])

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img, "fps : "+str(int(fps)), (10,30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

        cv2.imshow("Video",img)

        if cv2.waitKey(1) & 0xFF == ord('q') :
            break

if __name__ == "__main__" :
    main()