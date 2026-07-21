<<<<<<< HEAD
# Sketch2Image — Phase 1: Air Canvas

Gesture-based air drawing using a webcam and MediaPipe hand tracking.
This is Phase 1 only: no AI, no Stable Diffusion, no backend, no frontend.

## Project Structure

```
Sketch2Image/
├── main.py           # App loop, wiring, display only
├── hand_tracker.py    # MediaPipe detection only
├── gestures.py         # Gesture classification only
├── air_canvas.py        # Drawing, clearing, saving only
├── utils.py              # Pure helper functions
├── sketches/               # Saved PNG output lands here
└── requirements.txt
```

## Setup in VS Code

1. Open the `Sketch2Image` folder in VS Code (`File > Open Folder`).
2. Open a terminal in VS Code (`` Ctrl+` ``).
3. Create and activate a virtual environment:

   **Windows**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS / Linux**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. In VS Code, select the `venv` interpreter: `Ctrl+Shift+P` →
   `Python: Select Interpreter` → choose the one inside `venv`.

6. Run it:
   ```
   python main.py
   ```

## Controls (Gestures)

| Gesture                     | Action              |
|------------------------------|---------------------|
| Index finger only up        | Draw                |
| Index + middle finger up    | Stop drawing (lift pen) |
| Open palm (4 fingers up)    | Clear canvas        |
| Thumb only up                | Save sketch as `sketches/sketch.png` |
| `q` key                      | Quit                |

Clear and Save have a short cooldown so holding the gesture doesn't
trigger the action repeatedly.

## Notes

- If `python main.py` fails to open the camera, try changing
  `AirCanvasApp(camera_index=0)` in `main.py` to `1` — some laptops
  have a virtual camera registered at index 0.
- The saved file only contains your drawing (transparent background
  logic isn't needed since it's saved from the raw canvas, not the
  camera overlay).
- This code is intentionally modular per the architecture rules:
  `hand_tracker.py` never draws, `gestures.py` never touches OpenCV
  drawing calls, and `air_canvas.py` never touches MediaPipe. This
  keeps it ready to extend in Phase 2 without refactoring.
=======
# air-gesture-image-generator
Draw in the air using hand gestures and transform rough sketches into realistic AI-generated images using MediaPipe, OpenCV, ControlNet, and Stable Diffusion.
>>>>>>> 7bc04e7e78015e14fc0b754b8d9faacd50dfd52e
