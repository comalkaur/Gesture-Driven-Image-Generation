"""
Utility helpers shared across modules.

Only pure helper functions belong here — no OpenCV window logic,
no MediaPipe calls, no gesture logic.
"""

from typing import Tuple


def normalized_to_pixel(
    point: Tuple[float, float], frame_width: int, frame_height: int
) -> Tuple[int, int]:
    """Convert a normalized (x, y) in [0, 1] to pixel coordinates."""
    x, y = point
    return int(x * frame_width), int(y * frame_height)
