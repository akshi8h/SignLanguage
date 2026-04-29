import numpy as np
import cv2


def preprocess_hand_landmarks(landmarks):
    """
    Convert 21 hand landmarks to a flat NumPy array for ML models.
    landmarks: list of 21 (x, y) tuples
    Returns: np.array of shape (42,)
    """
    if landmarks is None:
        return None

    return np.array(landmarks).flatten().astype(np.float32)


def extract_keypoints(landmarks):
    """
    Used by camera.py
    Converts landmarks into a flat Python list:
    [x1, y1, x2, y2, ..., x21, y21]
    """
    if landmarks is None:
        return None

    keypoints = []
    for x, y in landmarks:
        keypoints.extend([x, y])

    return keypoints


def overlay_text_on_frame(
    frame,
    text,
    position=(10, 30),
    color=(0, 165, 255),
    scale=1.0,
    thickness=2
):
    """
    Draw text on a BGR frame using OpenCV.
    Default color is orange (BGR).
    """
    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        color,
        thickness,
        cv2.LINE_AA,
    )
