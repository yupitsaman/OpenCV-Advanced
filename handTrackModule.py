# Hand Detection Module

import cv2
import mediapipe as mp
import time
import math

# Creating class for hand detection
class handDetector () :
    # Initialization
    def __init__(self, mode = False, maxHands = 2, modelCom = 1, detectCon = 0.5, trackCon = 0.5) :
        self.mode = mode
        self.maxHands = maxHands
        self.modelCom = modelCom
        self.detectCon = detectCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelCom, self.detectCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4, 8, 12, 16, 20]

    # Function to detect and track hands
    def findHands(self, img, draw = True) :
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks :
            for handLms in self.results.multi_hand_landmarks :
                if draw :
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    # Function to find landmarks for a particular hand
    def findPosition (self, img, handNo = 0, draw = False) :
        # Landmark list 
        self.lmList = []                                    # To store [id, x, y]

        if self.results.multi_hand_landmarks :
            myHand = self.results.multi_hand_landmarks[handNo]                                   # Getting landmarks for only handNo. 0
            for id, lm in enumerate(myHand.landmark) :

                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.lmList.append([id, cx, cy])

                if draw :
                    cv2.circle(img, (cx, cy), 7, (0, 255, 0), -1)
        
        return self.lmList

    # To find if fingers are up or down, 1 : open , 0 : closed
    def fingersUp (self) :
        fingers = []

        # For right hand thumb
        if self.lmList[17][1]  > self.lmList[1][1] :
            if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0]-1][1] :
                fingers.append(1)
            else :
                fingers.append(0)

        # For left hand thumb
        if self.lmList[17][1]  < self.lmList[1][1] :
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1] :
                fingers.append(1)
            else :
                fingers.append(0)

        # For fingers 
        for id in range (1, 5) :
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2] :
                fingers.append(1)
            else :
                fingers.append(0)

        return fingers
    
    # To find the distance between two landmarks
    def findDistance(self, p1, p2, img, draw = True, r = 10, t = 4) :
        x1, y1 = self.lmList[p1][1:3]
        x2, y2 = self.lmList[p2][1:3]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2

        length = math.hypot(x2 - x1, y2 - y1)

        if draw :
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            if length < 25 :
                cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        return length, img, [x1, y1, x2, y2, cx, cy]


def main () :
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    # Calling the class with object 'detector'
    detector = handDetector()

    while True :
        success, img = cap.read()
        image = cv2.flip(img, 1)

        # Fucntion to detect hands
        image = detector.findHands(image)

        # Function to find the position of landmarks as a list
        lmList = detector.findPosition(image)
        if len(lmList) != 0 :
            # print(lmList[8])

            # fingers = detector.fingersUp()
            # print(fingers)

            length, img, lineList = detector.findDistance(4, 8, image)
            print(length)

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(image, "fps : "+str(int(fps)), (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

        cv2.imshow("Camera",image)

        if cv2.waitKey(1) & 0xFF == ord('q') :
            break

if __name__ == "__main__" :
    main ()