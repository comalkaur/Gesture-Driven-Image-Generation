"""
Gesture recognition module.

Responsibility:
- Analyze hand landmarks
- Classify the current gesture: draw, stop, clear, save

This module must NOT draw anything, open the webcam, use MediaPipe
directly, or call OpenCV drawing functions.
"""

from enum import Enum, auto
from typing import List, Tuple


class Gesture(Enum):
    """All recognizable gestures for Phase 1."""

    NONE = auto()
    DRAW = auto()   # index finger only -> draw
    STOP = auto()   # index + middle -> pause drawing (lift pen)
    CLEAR = auto()  # open palm (all 4 fingers) -> clear canvas
    SAVE = auto()   # thumb only -> save sketch


# MediaPipe hand landmark indices (tip and pip joint per finger)
_THUMB_TIP, _THUMB_IP = 4, 3
_INDEX_TIP, _INDEX_PIP = 8, 6
_MIDDLE_TIP, _MIDDLE_PIP = 12, 10
_RING_TIP, _RING_PIP = 16, 14
_PINKY_TIP, _PINKY_PIP = 20, 18
_WRIST = 0


class GestureRecognizer:
    """Classifies gestures from normalized hand landmarks."""

    def recognize(self, landmarks: List[Tuple[float, float]]) -> Gesture:
        """
        Determine the current gesture from 21 normalized landmarks.

        Args:
            landmarks: list of 21 (x, y) tuples, MediaPipe index order.

        Returns:
            The classified Gesture.
        """
        index, middle, ring, pinky, thumb = self._get_fingers_up(landmarks)

        if index and middle and ring and pinky:
            return Gesture.CLEAR

        if index and middle and not ring and not pinky:
            return Gesture.STOP

        if index and not middle and not ring and not pinky:
            return Gesture.DRAW

        if thumb and not index and not middle and not ring and not pinky:
            return Gesture.SAVE

        return Gesture.NONE

    def get_index_fingertip(
        self, landmarks: List[Tuple[float, float]]
    ) -> Tuple[float, float]:
        """Return the normalized (x, y) position of the index fingertip."""
        return landmarks[_INDEX_TIP]

    def _get_fingers_up(
        self, landmarks: List[Tuple[float, float]]
    ) -> Tuple[bool, bool, bool, bool, bool]:
        """
        Determine which fingers are extended.

        A finger is "up" if its tip sits above its PIP joint (smaller y,
        since image coordinates increase downward). The thumb is judged
        on the x-axis instead, since it extends sideways rather than up.

        Returns:
            (index, middle, ring, pinky, thumb) booleans.
        """
        index_up = landmarks[_INDEX_TIP][1] < landmarks[_INDEX_PIP][1]
        middle_up = landmarks[_MIDDLE_TIP][1] < landmarks[_MIDDLE_PIP][1]
        ring_up = landmarks[_RING_TIP][1] < landmarks[_RING_PIP][1]
        pinky_up = landmarks[_PINKY_TIP][1] < landmarks[_PINKY_PIP][1]

        thumb_up = abs(landmarks[_THUMB_TIP][0] - landmarks[_WRIST][0]) > abs(
            landmarks[_THUMB_IP][0] - landmarks[_WRIST][0]
        )

        return index_up, middle_up, ring_up, pinky_up, thumb_up
