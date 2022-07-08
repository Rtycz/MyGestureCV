import cv2
import mediapipe as mp
import time


class handDetector:
    def __init__(self, mode=False, maxHands=2, complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        self.BigTipID = 4
        self.TipIDS = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print (results.multi_hand_landmarks)

        if draw:
            if self.results.multi_hand_landmarks:
                for handLms in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print (id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)

        return self.lmList

    def fingersUp(self):
        """
        Количество поднятых пальцев
        :return: список из пяти элементов 0\1 каждый из которых обозначает поднят палец или нет
        """
        fingers = []
        # Большой палец правой руки
        if self.lmList[self.BigTipID][1] < self.lmList[self.BigTipID - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Остальные палцьцы
        for id in range(1, 5):
            if self.lmList[self.TipIDS[id]][2] < self.lmList[self.TipIDS[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers


def main():
    pTime = 0  # previous time
    cTime = 0  # current time

    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()

        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()