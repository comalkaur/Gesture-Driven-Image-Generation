"""
Entry point for the Air Canvas application.

Responsibility: own the video capture loop, wire together the hand
tracker, gesture recognizer, and canvas, and render output.
No detection, gesture-classification, or drawing logic lives here.
"""

import time

import cv2

from air_canvas import AirCanvas
from gestures import Gesture, GestureRecognizer
from hand_tracker import HandTracker
from utils import normalized_to_pixel


class AirCanvasApp:
    """Owns the top-level application loop and wires modules together."""

    # Minimum seconds between repeated triggers of a discrete action
    # (clear/save), so a held gesture doesn't fire hundreds of times.
    ACTION_COOLDOWN_SECONDS = 1.5

    def __init__(self, camera_index: int = 0) -> None:
        self.camera_index = camera_index
        self.capture = None

        self.hand_tracker = HandTracker(max_num_hands=1)
        self.gesture_recognizer = GestureRecognizer()
        self.canvas = None  # created once we know frame size

        self._last_action_time = 0.0

    def start(self) -> None:
        """Initialize the camera and run the main loop."""
        self.capture = cv2.VideoCapture(self.camera_index)

        if not self.capture.isOpened():
            raise RuntimeError(f"Could not open camera index {self.camera_index}")

        self._run_loop()

    def _run_loop(self) -> None:
        while True:
            success, frame = self.capture.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)  # mirror for natural interaction

            if self.canvas is None:
                height, width = frame.shape[:2]
                self.canvas = AirCanvas(width=width, height=height)

            landmarks = self.hand_tracker.process(frame)
            gesture = Gesture.NONE

            if landmarks is not None:
                gesture = self.gesture_recognizer.recognize(landmarks)
                self._handle_gesture(gesture, landmarks, frame)
            else:
                self.canvas.lift_pen()

            display = self.canvas.overlay_on(frame)
            self._draw_hud(display, gesture)

            cv2.imshow("Air Canvas", display)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self._cleanup()

    def _handle_gesture(self, gesture: Gesture, landmarks, frame) -> None:
        """Route the classified gesture to the appropriate canvas action."""
        now = time.time()

        if gesture == Gesture.DRAW:
            fingertip_norm = self.gesture_recognizer.get_index_fingertip(landmarks)
            height, width = frame.shape[:2]
            point = normalized_to_pixel(fingertip_norm, width, height)
            self.canvas.draw_point(point)

        elif gesture == Gesture.STOP:
            self.canvas.lift_pen()

        elif gesture == Gesture.CLEAR:
            if now - self._last_action_time > self.ACTION_COOLDOWN_SECONDS:
                self.canvas.clear()
                self._last_action_time = now

        elif gesture == Gesture.SAVE:
            if now - self._last_action_time > self.ACTION_COOLDOWN_SECONDS:
                path = self.canvas.save("sketch.png")
                print(f"Sketch saved to: {path}")
                self._last_action_time = now

        else:
            self.canvas.lift_pen()

    def _draw_hud(self, frame, gesture: Gesture) -> None:
        """Overlay the current gesture/mode as text for user feedback."""
        cv2.putText(
            frame,
            f"Mode: {gesture.name}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )
        cv2.putText(
            frame,
            "Index=Draw | Index+Middle=Stop | OpenPalm=Clear | Thumb=Save | q=Quit",
            (10, frame.shape[0] - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (200, 200, 200),
            1,
        )

    def _cleanup(self) -> None:
        """Release all resources on shutdown."""
        if self.capture is not None:
            self.capture.release()
        self.hand_tracker.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = AirCanvasApp()
    app.start()
