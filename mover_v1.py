import cv2
import mediapipe as mp
import pyautogui
import pytweening
from pytweening import easeInOutQuad

cap = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands()
draw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            y = handLms.landmark[8].y  # y coord Index fingertip
            x = handLms.landmark[8].x  # x coord Index fingertip
            width, height = pyautogui.size()
            adjy = (height * y)
            adjx = (width * (1-x))
            pyautogui.moveTo(adjx, adjy, duration=0.5, tween=pytweening.easeOutQuad)
            pyautogui.MINIMUM_DURATION = 0

            draw.draw_landmarks(img, handLms, mp.solutions.hands.HAND_CONNECTIONS) #draws hand map thingie
            h, w, _ = img.shape
            cx, cy = int(handLms.landmark[8].x * w), int(handLms.landmark[8].y * h)
            cv2.circle(img, (cx, cy), 20, (255, 255, 255), 2)  # radius 20, white, 2px border]

    cv2.imshow("Hand Scroller", img)
    if cv2.waitKey(1) & 0xFF == ord('`'):
        break
