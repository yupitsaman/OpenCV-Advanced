# Hand Tracking Minimum

import cv2
import mediapipe as mp
import time

# To get the frame rate
cTime = 0
pTime = 0


### Hand tracking module  ###
mpHands = mp.solutions.hands

# (static image i.e. only detection, max number of hands, model complexity, min detection confidence, min tracking confidence)
hands = mpHands.Hands(False, 2, 1, 0.5, 0.5)                                     # False, as we need detection as well as tracking

# To get the points on hands to draw landmarks
mpDraw = mp.solutions.drawing_utils



cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
# cap.set(10,100)

while True :
    success, img = cap.read()
    image = cv2.flip(img, 1)

    # Changing to rgb as handTrackingModule only works with rgb images
    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks :
        # As there can be multiple hands
        for handLms in results.multi_hand_landmarks :

            # Getting the ids and landmarks of each hand (there are 21 landmarks in a hand)
            for id, lm in enumerate(handLms.landmark) :
                # print(id, lm)                                                                          # it will give the x and y values in decimal

                # Converting decimal to pixels
                h, w, c = image.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)

                if id == 8 :
                    cv2.circle(image, (cx, cy), 15, (255, 0, 0), -1)

            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)                              # mp.HAND_CONNECTIONS to connect the dots

    # Getting the frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(image, "fps : "+str(int(fps)),(10,30),cv2.FONT_HERSHEY_COMPLEX,1,(255, 0, 255), 2)

    cv2.imshow("Camera",image)

    if cv2.waitKey(1) & 0xFF == ord('q') :
        break