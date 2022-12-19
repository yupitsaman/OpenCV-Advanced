# Project 5
# Virtual Keyboard

import cv2
import cvzone
from  handTrackModule import handDetector
import time
from pynput.keyboard import Controller
import numpy as np

# Drawing all the buttons
# def drawAll(img, buttonList) :
#     for button in buttonList :
#         x, y = button.pos
#         w, h = button.size
#         cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)
#         cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), -1)
#         cv2.putText(img, button.text, (x + 15, y + 70), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 4)
#     return img

def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)
        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 40, y + 60), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    # print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out


class Button () :
    def __init__(self, pos, text, size = [85,85]) :
        self.pos = pos
        self.text = text
        self.size = size


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
pTime = 0

detector = handDetector(detectCon = 0.8)

buttonList = []
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""

# keyboard = Controller()

for i in range(len(keys)) :
        for j, key in enumerate(keys[i]) :
            buttonList.append(Button([100*j + 50, 100*i + 50], key))

while True :
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)

    img = drawAll(img, buttonList)

    if lmList :
        for button in buttonList :
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][1] < x+w and y < lmList[8][2] < y+h:

                # Making the button dark purple if hovered
                cv2.rectangle(img, (x-8, y-8), (x + w+8, y + h+8), (175, 0, 175), -1)
                cv2.putText(img, button.text, (x + 15, y + 70), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 4)

                # Finding the distance
                l, _, _ = detector.findDistance(8, 12, img, draw = False)
                print(l)
                if l < 35 :
                    # keyboard.press(button.text)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), -1)
                    cv2.putText(img, button.text, (x + 15, y + 70), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 4)
                    finalText += button.text
                    time.sleep(0.35)

    # Showing the final text
    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), -1)
    cv2.putText(img, finalText, (60, 425), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 4)

    # Calculating fps
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'fps : {int(fps)}', (1090, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
    
    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == ord('q') :
        break