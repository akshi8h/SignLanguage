import cv2
import mediapipe as mp
from utils import preprocess_hand_landmarks

class CameraHandler:
    def __init__(self, predictor, camera_index=0):
        self.predictor = predictor

        # ✅ Ensure camera_index is integer
        self.cap = cv2.VideoCapture(int(camera_index))
        if not self.cap.isOpened():
            raise RuntimeError("❌ Cannot open webcam")

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None, None

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)
        landmarks = None

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            landmarks = [(lm.x, lm.y) for lm in hand.landmark]
            self.mp_draw.draw_landmarks(frame, hand, self.mp_hands.HAND_CONNECTIONS)

        features = preprocess_hand_landmarks(landmarks)
        label, conf = self.predictor.predict(features)

        return frame, label, conf

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
