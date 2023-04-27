import cv2
import cvzone
import pickle
import numpy as np

cap = cv2.VideoCapture("OpenCV\\Project\\Media\\carPark.mp4")

width, height = 90, 40
freeInLanesOld = np.zeros(6)

# freeLane1 = np.ones(12)

with open('CarParkPos','rb') as f :
        posList = pickle.load(f)

# posList.sort()
# # print(posList)
# lane1 = posList[:12]
# lane2 = posList[12:24]
# lane3 = posList[24:35]
# lane4 = posList[35:46]
# lane5 = posList[46:58]
# lane6 = posList[58:]
# lane1 = sorted(lane1 , key=lambda k: [k[1], k[0]])
# lane2 = sorted(lane2 , key=lambda k: [k[1], k[0]])
# lane3 = sorted(lane3 , key=lambda k: [k[1], k[0]])
# lane4 = sorted(lane4 , key=lambda k: [k[1], k[0]])
# lane5 = sorted(lane5 , key=lambda k: [k[1], k[0]])
# lane6 = sorted(lane6 , key=lambda k: [k[1], k[0]])
# # print(len(lane6))
# # print(lane6)

def checkParkingSpace(imgPro) :

    spaceCounter = 0

    for pos in posList :
        x, y = pos
        imgCrop = imgPro[y:y+height, x:x+width]
        # cv2.imshow(str(x*y),imgCrop)

        # Counting non zero pixels
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

def laneNumber(img) :
    color = (0, 0, 255)
    cv2.putText(img, f'1', (70,570), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
    cv2.putText(img, f'2', (160,570), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
    cv2.putText(img, f'3', (380,570), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
    cv2.putText(img, f'4', (470,570), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
    cv2.putText(img, f'5', (680,570), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
    cv2.putText(img, f'6', (810,570), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
    # cvzone.putTextRect(img, f'1', (70, 570), scale = 2, thickness=2, offset= 0, colorR= (0, 0, 0))
    # cvzone.putTextRect(img, f'2', (160, 570), scale = 2, thickness=2, offset= 0, colorR= (0, 0, 0))
    # cvzone.putTextRect(img, f'3', (380, 570), scale = 2, thickness=2, offset= 0, colorR= (0, 0, 0))
    # cvzone.putTextRect(img, f'4', (470, 570), scale = 2, thickness=2, offset= 0, colorR= (0, 0, 0))
    # cvzone.putTextRect(img, f'5', (680, 570), scale = 2, thickness=2, offset= 0, colorR= (0, 0, 0))
    # cvzone.putTextRect(img, f'6', (800, 570), scale = 2, thickness=2, offset= 0, colorR= (0, 0, 0))

def definingLanes() :
    allLanes = []
    posList.sort()
    # print(posList)
    lane1 = posList[:12]
    lane2 = posList[12:24]
    lane3 = posList[24:35]
    lane4 = posList[35:46]
    lane5 = posList[46:58]
    lane6 = posList[58:]
    lane1 = sorted(lane1 , key=lambda k: [k[1], k[0]])
    lane2 = sorted(lane2 , key=lambda k: [k[1], k[0]])
    lane3 = sorted(lane3 , key=lambda k: [k[1], k[0]])
    lane4 = sorted(lane4 , key=lambda k: [k[1], k[0]])
    lane5 = sorted(lane5 , key=lambda k: [k[1], k[0]])
    lane6 = sorted(lane6 , key=lambda k: [k[1], k[0]])
    allLanes.append(lane1)
    allLanes.append(lane2)
    allLanes.append(lane3)
    allLanes.append(lane4)
    allLanes.append(lane5)
    allLanes.append(lane6)
    # print(len(lane6))
    # print(lane6)

    return allLanes

def freeSpotPos (img, lane, laneNumber, freeInLanesOld) :
    # global freeInLanesOld
    freeSpaces = []
    freeInLanes = 0
    for i, pos in enumerate(lane) :
        x, y = pos
        spot = img[y:y+height, x:x+width]
        # cv2.imshow(f'Image {i}', spot)
        checkFree = cv2.countNonZero(spot)
        if checkFree < 750 :
            freeInLanes += 1
            freeSpaces.append(i+1)

    if freeInLanes != freeInLanesOld[laneNumber] :
        print(f'Free in lane {laneNumber+1}  : {freeSpaces}')
        freeInLanesOld[laneNumber] = freeInLanes
        # print(f'freeInLanes : {freeInLanes}')
        # print(f'freeInLanesOld : {freeInLanesOld}')
        

while True :

    # Continuing the video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT) :
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        freeInLanesOld = [0, 0, 0, 0, 0, 0]
        print(f'#########################################################')

    success, img  = cap.read()
    img = cv2.resize(img, (940,580))


    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)

    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # cv2.rectangle(img, lane2[0], (lane2[10][0]+width, lane2[10][1]+height), (255, 0, 0), 5)

    allLanes = definingLanes()

    checkParkingSpace(imgDilate)

    # Putting lane number
    laneNumber(img)

    # Print free spots
    for i in range(6) :
        freeSpotPos(imgDilate, allLanes[i], i, freeInLanesOld)
    # freeSpotPos(imgDilate, allLanes[1], 1)
    # freeInLanesOld = 0

    cv2.imshow("Video",img)
    # cv2.imshow("Threshold", imgThreshold)
    # cv2.imshow("Median Blur", imgMedian)
    # cv2.imshow("Dilated image", imgDilate)
    if cv2.waitKey(1) & 0xFF == ord('q') :
        break