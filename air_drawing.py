import cv2
import numpy as np
import mediapipe as mp
import math

# ---------------- Instructions ----------------
print("\n🖐️  AIR DRAWING TOOLKIT CONTROLS 🖌️")
print("------------------------------------")
print("🖊  Draw          : Index finger up only")
print("🎨  Change Color  :")
print("       -  Middle → Blue")
print("       -  Ring   → Green")
print("       -  Pinky  → Yellow")
print("🧹  Clear Screen  : All fingers up (open palm)")
print("⬛  Shape Drawing : Pinch Index + Thumb → Rectangle")
print("↩️  Undo          : Thumb + Pinky only")
print("❌  Exit          : Press 'ESC'\n")
print("------------------------------------\n")

# Initialize
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)
canvas = None
prev_x, prev_y = None, None
current_color = (0, 0, 255)  # Default Red
brush_thickness = 5

# For undo feature
history = []

# Helper: Fingers up
def fingers_up(lm_list):
    fingers = []
    # Thumb
    fingers.append(1 if lm_list[4][1] < lm_list[3][1] else 0)
    # Other fingers
    for tip in [8, 12, 16, 20]:
        fingers.append(1 if lm_list[tip][2] < lm_list[tip - 2][2] else 0)
    return fingers

# Distance function
def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

shape_start = None
drawing_shape = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    if canvas is None:
        canvas = np.zeros_like(frame)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        lm_list = []
        h, w, _ = frame.shape
        for id, lm in enumerate(hand_landmarks.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append([id, cx, cy])

        finger_state = fingers_up(lm_list)

        # --- Gesture Controls ---
        # Clear screen
        if sum(finger_state) == 5:
            canvas = np.zeros_like(frame)
            history.clear()

        # Color switching (only middle, ring, pinky can change color)
        if finger_state[2] == 1 and sum(finger_state) == 1:   # Middle only
            current_color = (255, 0, 0)   # Blue
        elif finger_state[3] == 1 and sum(finger_state) == 1: # Ring only
            current_color = (0, 255, 0)   # Green
        elif finger_state[4] == 1 and sum(finger_state) == 1: # Pinky only
            current_color = (0, 255, 255) # Yellow
        # index (finger_state[1]) does NOT set any color now




        # Undo
        if finger_state[0] == 1 and finger_state[4] == 1 and sum(finger_state) == 2:
            if history:
                canvas = history.pop()

        # Drawing
        if finger_state[1] == 1 and finger_state[2] == 0:
            x, y = lm_list[8][1], lm_list[8][2]
            cv2.circle(frame, (x, y), 10, current_color, cv2.FILLED)

            if prev_x is not None and prev_y is not None:
                history.append(canvas.copy())
                cv2.line(canvas, (prev_x, prev_y), (x, y), current_color, brush_thickness)

            prev_x, prev_y = x, y
        else:
            prev_x, prev_y = None, None

        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
    cv2.imshow("Air Drawing Toolkit", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
