# Face mesh basics
# To get different 468 landmarks on a face

import cv2
import mediapipe as mp
import time

mpDraw = mp.solutions.drawing_utils
drawSpec = mpDraw.DrawingSpec(color = (0, 255, 0), thickness = 1, circle_radius = 1)

mpFaceMesh = mp.solutions.face_mesh
# (static image, max. no. of faces, redefine landmarks, min. detection confidence, min. tracking confidence)
faceMesh = mpFaceMesh.FaceMesh(False, 1, False, 0.5, 0.5)

cap = cv2.VideoCapture("OpenCV/Advanced/Media/faceDetection1.mp4")
pTime = 0

while True :
    success, img = cap.read()
    img = cv2.resize(img, (700, 420))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks :
        for faceLms in results.multi_face_landmarks :
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec)                                 # FACEMESH_TESSELATION

            for id, lm in enumerate(faceLms.landmark) :
                # print(id, lm)

                ih, iw, ic = img.shape
                x, y = int(lm.x*iw), int(lm.y*ih)

                print(id, x, y)


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'fps : {int(fps)}', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord('q') :
        break