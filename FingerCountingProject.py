'''Скрипт с подсчетом пальцев'''

import cv2
import time
import os
import HandTrackinModule as htm

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "FingerImages"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))

pTime = 0

detector = htm.handDetector(maxHands=1, detectionCon=0.75)

BigTipID = 4
TipIDS = [8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)

    if len(lmList) != 0:
        fingers = []

        # Большой палец правой руки
        if lmList[BigTipID][1] > lmList[BigTipID - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Остальные палцьцы
        for id in TipIDS:
            if lmList[id][2] < lmList[id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)

        h, w, c = overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1]

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
