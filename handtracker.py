import cv2  # bring in OpenCV to use the camera and show pictures
import mediapipe as mp  # bring in Mediapipe to find hands in pictures

cap = cv2.VideoCapture(0)  # open the webcam to start grabbing video frames

hands = mp.solutions.hands.Hands()  # make a hand detector to find hands in the frames
draw = mp.solutions.drawing_utils  # get the tool that draws hand lines and dots

while True:  # keep doing this forever until we tell it to stop
    success, frame = cap.read()  # take one picture from the webcam
    if not success:  # if no picture was grabbed, skip and try again
        continue

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # change the picture colors so Mediapipe can understand it
    results = hands.process(rgb)  # ask Mediapipe to find hand parts in the picture

    if results.multi_hand_landmarks:  # if any hands were found
        for hand_landmarks in results.multi_hand_landmarks:  # for each hand found
            draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
            # draw the hand dots and lines on the picture

    cv2.imshow("Hand Tracker", frame)  # show the picture with hands drawn on it in a window
    if cv2.waitKey(1) & 0xFF == ord('`'):  # if you press the '`' key, stop running the program
        break

cap.release()  # turn off the webcam when done
cv2.destroyAllWindows()  # close the window showing the video
