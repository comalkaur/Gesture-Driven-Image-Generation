"""
Air canvas module.

Responsibility:
- Store drawing points
- Draw lines onto a persistent canvas
- Clear the canvas
- Save the canvas as an image file

This module must NOT detect hands, use MediaPipe, or recognize gestures.
"""

import os
from typing import Optional, Tuple

import cv2
import numpy as np


class AirCanvas:
    """A persistent drawing surface that accumulates strokes over time."""

    def __init__(
        self,
        width: int,
        height: int,
        color: Tuple[int, int, int] = (255, 0, 255),
        thickness: int = 6,
        save_dir: str = "sketches",
    ) -> None:
        self.width = width
        self.height = height
        self.color = color
        self.thickness = thickness
        self.save_dir = save_dir

        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self._prev_point: Optional[Tuple[int, int]] = None

        os.makedirs(self.save_dir, exist_ok=True)

    def draw_point(self, point: Tuple[int, int]) -> None:
        """
        Extend the current stroke to a new point.

        Args:
            point: (x, y) pixel coordinates in canvas space.
        """
        if self._prev_point is not None:
            cv2.line(self.canvas, self._prev_point, point, self.color, self.thickness)
        self._prev_point = point

    def lift_pen(self) -> None:
        """Break the current stroke so the next draw_point starts a fresh line."""
        self._prev_point = None

    def clear(self) -> None:
        """Erase the entire canvas."""
        self.canvas[:] = 0
        self._prev_point = None

    def overlay_on(self, frame: np.ndarray) -> np.ndarray:
        """
        Merge the canvas on top of a camera frame for live display.

        Uses a mask so only drawn (non-black) pixels replace the frame,
        keeping the rest of the live camera feed visible underneath.
        """
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        background = cv2.bitwise_and(frame, frame, mask=mask_inv)
        foreground = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)

        return cv2.add(background, foreground)

    def save(self, filename: str = "sketch.png") -> str:
        """
        Save the current canvas (drawing only, no camera feed) to disk.

        Returns:
            The full path the file was saved to.
        """
        path = os.path.join(self.save_dir, filename)
        cv2.imwrite(path, self.canvas)
        return path
