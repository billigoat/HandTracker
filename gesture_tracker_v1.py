import cv2
import mediapipe as mp
import pyautogui
import pytweening
from pytweening import easeInOutQuad

cap = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands()
draw = mp.solutions.drawing_utils

#hand detection
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # flip horizontally
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # index fingertip coords
            y = handLms.landmark[8].y
            x = handLms.landmark[8].x
            width, height = pyautogui.size()
            adjy = (height * y)
            adjx = (width * (1 - x))
            pyautogui.MINIMUM_DURATION = 0

            h, w, _ = img.shape
            draw.draw_landmarks(img, handLms, mp.solutions.hands.HAND_CONNECTIONS)

            # get all fingertips
            fingers = [handLms.landmark[i] for i in [0, 4, 8, 12, 16, 20]]

            # small circles on all fingertips
            for lm in fingers:
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 25, (255, 255, 255), 1)

            # big circles on index fingertips
            cv2.circle(img, (int(handLms.landmark[8].x * w), int(handLms.landmark[8].y * h)), 60, (225, 225, 225), 2)
            cv2.circle(img, (int(handLms.landmark[8].x * w), int(handLms.landmark[8].y * h)), 25, (255, 255, 255), 4)


    # Boolean for finger states
    def is_finger_up(lms, tip_id, pip_id):
        return lms.landmark[tip_id].y < lms.landmark[pip_id].y


    # Checks hands
    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, handLms in enumerate(results.multi_hand_landmarks):
            hand_label = results.multi_handedness[idx].classification[0].label

            # Define finger states here
            # Thumb (horizontal check)
            thumb_up = (handLms.landmark[4].x > handLms.landmark[3].x) if hand_label == "Right" else (
                        handLms.landmark[4].x < handLms.landmark[3].x)
            thumb_neutral = abs(handLms.landmark[4].x - handLms.landmark[3].x) <= 0.02
            thumb_down = not thumb_up and not thumb_neutral

            # Index finger (vertical check)
            index_up = handLms.landmark[8].y < handLms.landmark[6].y - 0.02
            index_neutral = abs(handLms.landmark[8].y - handLms.landmark[6].y) <= 0.02
            index_down = handLms.landmark[8].y > handLms.landmark[6].y + 0.02

            # Middle finger
            middle_up = handLms.landmark[12].y < handLms.landmark[10].y - 0.02
            middle_neutral = abs(handLms.landmark[12].y - handLms.landmark[10].y) <= 0.02
            middle_down = handLms.landmark[12].y > handLms.landmark[10].y + 0.02

            # Ring finger
            ring_up = handLms.landmark[16].y < handLms.landmark[14].y - 0.02
            ring_neutral = abs(handLms.landmark[16].y - handLms.landmark[14].y) <= 0.02
            ring_down = handLms.landmark[16].y > handLms.landmark[14].y + 0.02

            # Pinky finger
            pinky_up = handLms.landmark[20].y < handLms.landmark[18].y - 0.02
            pinky_neutral = abs(handLms.landmark[20].y - handLms.landmark[18].y) <= 0.02
            pinky_down = handLms.landmark[20].y > handLms.landmark[18].y + 0.02


            if hand_label == "Right":
                if index_up and not middle_up and not ring_up and not pinky_up:
                    cv2.putText(img, "RPOINTING", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                elif all([thumb_up, index_up, middle_up, ring_up, pinky_up]):
                    cv2.putText(img, "ROPEN HAND", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                elif not any([index_up, middle_up, ring_up, pinky_up]):
                    cv2.putText(img, "RFIST", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                elif thumb_up and not index_up and not middle_up:
                    cv2.putText(img, "RTHUMBS UP", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                elif any([index_down, index_neutral, middle_down, middle_neutral, ring_down, ring_neutral, pinky_down, pinky_neutral, thumb_down, thumb_neutral]):
                    cv2.putText(img, "???", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

            elif hand_label == "Left":
                if index_up and not middle_up and not ring_up and not pinky_up:
                    cv2.putText(img, "LPOINTING", (1600, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                elif all([thumb_up, index_up, middle_up, ring_up, pinky_up]):
                    cv2.putText(img, "LOPEN HAND", (1600, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                elif not any([index_up, middle_up, ring_up, pinky_up]):
                    cv2.putText(img, "LFIST", (1600, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                elif thumb_up and not index_up and not middle_up:
                    cv2.putText(img, "LTHUMBS UP", (1600, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                elif any([index_down, index_neutral, middle_down, middle_neutral, ring_down, ring_neutral, pinky_down, pinky_neutral, thumb_down, thumb_neutral]):
                    cv2.putText(img, "???", (1600, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

    # Example gestures
   # if index_up and not middle_up and not ring_up and not pinky_up:
      #  cv2.putText(img, "POINTING", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
   # elif all([thumb_up, index_up, middle_up, ring_up, pinky_up]):
     #   cv2.putText(img, "OPEN HAND", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
   # elif not any([index_up, middle_up, ring_up, pinky_up]):
    #    cv2.putText(img, "FIST", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
   # elif thumb_up and not index_up and not middle_up:
   #     cv2.putText(img, "THUMBS UP", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

    cv2.imshow("Hand Tracker v2", img)
    if cv2.waitKey(1) & 0xFF == ord('`'):
        break
