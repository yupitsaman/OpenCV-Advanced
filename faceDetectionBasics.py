# Face Detection Basics

import cv2
import mediapipe as mp
import time


pTime = 0

mpFaceDetection = mp.solutions.face_detection
faceDetection = mpFaceDetection.FaceDetection(0.75)                                             # (minimum detection confidence), 0.5 by default
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture("OpenCV/Advanced/Media/faceDetection1.mp4")

while True :
    success, img = cap.read()
    img = cv2.resize(img, (680, 400))
    # img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = faceDetection.process(imgRGB)

    if results.detections :
        for id, detection in enumerate(results.detections) :
            # Drawing rectangle using inbuilt function
            # mpDraw.draw_detection(img, detection)

            # print(id, detection)
            # print(detection.score)  
            # print(detection.location_data.relative_bounding_box)                                                 # xmin, ymin, width, height

            bboxC = detection.location_data.relative_bounding_box

            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin*iw), int(bboxC.ymin*ih), int(bboxC.width*iw), int(bboxC.height*ih)

            cv2.rectangle(img, bbox, (0, 255, 0), 2)
            # Showing the detection confidence score
            cv2.putText(img, f'{int(detection.score[0]*100)}%', (bbox[0], bbox[1]-10), 1, cv2.FONT_HERSHEY_PLAIN, (0, 255, 0), 2)

    # Getting the frame rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'fps : {int(fps)}', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord('q') :
        break