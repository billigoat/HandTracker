import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
draw_utils = mp.solutions.drawing_utils

points = []

def onCook(dat):
    videoIn = op('video_device_in1')  # Make sure this is the name of your video TOP
    outTop = op('out1')               # This is your output TOP

    frame = videoIn.numpyArray(delayed=False)
    if frame is None:
        return

    frame_bgr = cv2.cvtColor(frame[:, :, :3], cv2.COLOR_RGB2BGR)
    img_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    h, w, _ = frame.shape
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            index_tip = handLms.landmark[8]
            pip = handLms.landmark[6]

            cx, cy = int(index_tip.x * w), int(index_tip.y * h)
            if index_tip.y < pip.y:
                points.append((cx, cy))

    for i in range(1, len(points)):
        cv2.line(frame_bgr, points[i - 1], points[i], (0, 255, 0), 3)

    # Convert back to RGBA for TouchDesigner
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    rgba = np.concatenate([frame_rgb, np.full((h, w, 1), 255, dtype=np.uint8)], axis=2)

    outTop.copyNumpyArray(rgba)
    return
