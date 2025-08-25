import cv2
import mediapipe as mp
import pygame
import os

# Initialize Pygame mixer
pygame.mixer.init()

# Load piano sounds (rename files key1.wav ... key13.wav)
sounds = {}
for i in range(1, 14):  
    sounds[i] = pygame.mixer.Sound(os.path.join("sounds", f"key{i}.wav"))

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

# Webcam
cap = cv2.VideoCapture(0)

# track last keys pressed to avoid repeats
last_keys = set()

# Fingertip indices
fingertips = [4, 8, 12, 16, 20]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    h, w, _ = frame.shape
    current_keys = set()

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            for tip in fingertips:
                x = int(handLms.landmark[tip].x * w)
                y = int(handLms.landmark[tip].y * h)
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

                # divide into 13 keys
                zone_width = w // 13
                key_index = x // zone_width + 1

                if 1 <= key_index <= 13:
                    current_keys.add(key_index)
                    cv2.putText(frame, f"Key {key_index}", (x, y - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # play new keys that were not pressed before
    new_keys = current_keys - last_keys
    for k in new_keys:
        sounds[k].play()

    last_keys = current_keys

    cv2.imshow("Virtual Piano", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
