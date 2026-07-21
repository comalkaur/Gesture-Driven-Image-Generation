"""
Hand detection module.

Responsibility:
- Initialize MediaPipe Hands
- Detect a hand in a frame
- Return raw landmark data

This module must NOT draw anything, recognize gestures, or save images.
"""

from typing import List, Optional, Tuple

import cv2
import mediapipe as mp


class HandTracker:
    """Wraps MediaPipe Hands to provide landmark detection only."""

    def __init__(
        self,
        max_num_hands: int = 1,
        detection_confidence: float = 0.7,
        tracking_confidence: float = 0.7,
    ) -> None:
        self._mp_hands = mp.solutions.hands
        self._hands = self._mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )

    def process(self, frame_bgr) -> Optional[List[Tuple[float, float]]]:
        """
        Detect a hand in the given BGR frame and return normalized landmarks.

        Args:
            frame_bgr: The camera frame in OpenCV's default BGR format.

        Returns:
            A list of 21 (x, y) tuples in normalized [0, 1] coordinates,
            or None if no hand is detected.
        """
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self._hands.process(frame_rgb)

        if not results.multi_hand_landmarks:
            return None

        hand_landmarks = results.multi_hand_landmarks[0]
        landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]
        return landmarks

    def close(self) -> None:
        """Release MediaPipe resources. Call this on app shutdown."""
        self._hands.close()
