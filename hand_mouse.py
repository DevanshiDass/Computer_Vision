import cv2
import mediapipe as mp
import pyautogui
import math

screen_width, screen_height = pyautogui.size()

class HandDetector:
    def __init__(self, mode=False, max_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_number=0, draw=True):
        lm_list = []
        if self.results.multi_hand_landmarks:
            selected_hand = self.results.multi_hand_landmarks[hand_number]
            for id, landmark in enumerate(selected_hand.landmark):
                h, w, _ = img.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return lm_list

def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    cam_width, cam_height = 640, 480
    cap.set(3, cam_width)
    cap.set(4, cam_height)

    left_pressed = False
    right_pressed = False

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.find_hands(img)
        lm_list = detector.find_position(img)

        if lm_list:
            # Cursor: index finger tip (8)
            x, y = lm_list[8][1], lm_list[8][2]
            screen_x = int(x * screen_width / cam_width)
            screen_y = int(y * screen_height / cam_height)
            pyautogui.moveTo(screen_x, screen_y)

            # Finger tips
            thumb_x, thumb_y = lm_list[4][1], lm_list[4][2]
            middle_x, middle_y = lm_list[12][1], lm_list[12][2]

            # Distances
            dist_left = math.hypot(thumb_x - x, thumb_y - y)        # Index + Thumb
            dist_right = math.hypot(middle_x - x, middle_y - y)     # Index + Middle

            # Left click (press-and-hold)
            if dist_left < 40:
                if not left_pressed:
                    pyautogui.mouseDown()
                    left_pressed = True
                cv2.circle(img, ((x + thumb_x)//2, (y + thumb_y)//2), 15, (0,255,0), cv2.FILLED)
            else:
                if left_pressed:
                    pyautogui.mouseUp()
                    left_pressed = False

            # Right click
            if dist_right < 40:
                if not right_pressed:
                    pyautogui.click(button='right')
                    right_pressed = True
                cv2.circle(img, ((x + middle_x)//2, (y + middle_y)//2), 15, (0,0,255), cv2.FILLED)
            else:
                right_pressed = False

        cv2.imshow("Hand Mouse", img)
        if cv2.waitKey(1) & 0xFF == 27:  # Press Esc to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
