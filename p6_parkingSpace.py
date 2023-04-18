import cv2
import cvzone
import pickle
import numpy as np

cap = cv2.VideoCapture("OpenCV\\Project\\Media\\carPark.mp4")

width, height = 90, 40

with open('CarParkPos','rb') as f :
        posList = pickle.load(f)


def checkParkingSpace(imgPro) :

    spaceCounter = 0

    for pos in posList :
        x, y = pos
        imgCrop = imgPro[y:y+height, x:x+width]
        # cv2.imshow(str(x*y),imgCrop)

        # Counting no zero pixels
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x, y+height-7), scale = 1, thickness=1, offset= 0)

        if count < 750 :
            color = (0, 255, 0)
            thickness = 3
            spaceCounter += 1
        else : 
            color = (0, 0, 255)
            thickness = 2
        
        cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), color, thickness)
    
    cvzone.putTextRect(img, f'Free : {spaceCounter}/{len(posList)}', (5, 30), scale = 2, thickness=2, offset= 0, colorR= (0, 0, 0))


while True :
    # Continuing the video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT) :
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img  = cap.read()
    img = cv2.resize(img, (940,580))

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)

    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)

    cv2.imshow("Video",img)
    # cv2.imshow("Threshold", imgThreshold)
    # cv2.imshow("Median Blur", imgMedian)
    # cv2.imshow("Dilated image", imgDilate)
    if cv2.waitKey(1) & 0xFF == ord('q') :
        break