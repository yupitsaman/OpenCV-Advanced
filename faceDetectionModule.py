# Face Detection Module

import cv2
import mediapipe as mp
import time

class faceDetector() :
    # Initialization
    def __init__(self, minDetectionCon = 0.5) :
        self.minDetectionCon = minDetectionCon

        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)


    # Finding faces and landmarks
    def findFaces(self, img, draw = True) :
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.faceDetection.process(imgRGB)

        bboxes = []                                   # [id, bbox, detection.score]

        if self.results.detections :
            for id, detection in enumerate(self.results.detections) :
                bboxC = detection.location_data.relative_bounding_box

                ih, iw, ic = img.shape

                bbox = int(bboxC.xmin*iw), int(bboxC.ymin*ih), int(bboxC.width*iw), int(bboxC.height*ih)
                bboxes.append([id, bbox, detection.score])

                if draw :
                    img = self.fancyDraw(img, bbox)
                    cv2.putText(img, f'{int(detection.score[0]*100)}%', (bbox[0], bbox[1]-20), 1, cv2.FONT_HERSHEY_PLAIN, (0, 255, 0), 2)

        return img, bboxes


    # To draw rectangle around faces
    def fancyDraw(self, img, bbox) :
        x, y, w, h = bbox
        x1, y1 = x+w, y+h                                             # Diagonal corner point
        l = 20
        t = 3                                                        # thickness for corner lines

        cv2.rectangle(img, bbox, (0, 255, 0), 1)

        # Upper left corner  x, y
        cv2.line(img, (x,y), (x+l,y), (0, 255, 0), t)
        cv2.line(img, (x,y), (x,y+l), (0, 255, 0), t)

        # Upper right corner  x1, y
        cv2.line(img, (x1,y), (x1-l,y), (0, 255, 0), t)
        cv2.line(img, (x1,y), (x1,y+l), (0, 255, 0), t)

        # Lower left corner  x, y1
        cv2.line(img, (x,y1), (x+l,y1), (0, 255, 0), t)
        cv2.line(img, (x,y1), (x,y1-l), (0, 255, 0), t)

        # Lower right corner  x1, y1
        cv2.line(img, (x1,y1), (x1-l,y1), (0, 255, 0), t)
        cv2.line(img, (x1,y1), (x1,y1-l), (0, 255, 0), t)

        return img



def main() :
    pTime = 0
    cap = cv2.VideoCapture("OpenCV/Advanced/Media/faceDetection2.mp4")

    detector = faceDetector()

    while True :
        success, img = cap.read()
        img = cv2.resize(img, (680, 400))
        # img = cv2.flip(img, 1)

        img, bboxes = detector.findFaces(img)
        if bboxes :
            print(bboxes)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f'fps : {int(fps)}', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

        cv2.imshow("Video", img)

        if cv2.waitKey(1) & 0xFF == ord('q') :
            break

if __name__ == "__main__" : 
    main()