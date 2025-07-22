import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands()
draw = mp.solutions.drawing_utils

prev_y = None

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            y = handLms.landmark[8].y  # Index fingertip

            if prev_y:
                diff = y - prev_y
                if diff > 0.1:
                    pyautogui.scroll(-50)  # Scroll down
                elif diff < -0.1:
                    pyautogui.scroll(50)   # Scroll up

            prev_y = y
            draw.draw_landmarks(img, handLms, mp.solutions.hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Scroller", img)
    if cv2.waitKey(1) & 0xFF == ord('`'):
        break
