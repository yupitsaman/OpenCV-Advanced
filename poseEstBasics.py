# Pose estimation minimum

from enum import EnumMeta
import cv2
import mediapipe as mp
import time

cTime = 0
pTime = 0

mpPose = mp.solutions.pose
# (static image i.e. only detection, model_complexity, upper_body_only, smooth_landmarks, detection confidence, tracking confidence)
pose = mpPose.Pose(False, 1, False, True, 0.5, 0.5)
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture("OpenCV/Advanced/Media/poseVideo2.mp4")

while True :
    success, img = cap.read()
    img = cv2.resize(img, (800,520))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Storing information of all 33 landmarks in results
    results = pose.process(imgRGB)

    if results.pose_landmarks :
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        for id, lm in enumerate(results.pose_landmarks.landmark) :
            # print(id, lm)

            h, w, c = img.shape

            cx, cy = int(lm.x*w), int(lm.y*h)

            # cv2.circle(img, (cx, cy), 5, (255, 0, 0), -1)



    # Getting frame rate
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, "fps : "+str(int(fps)), (10,30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q') :
        break