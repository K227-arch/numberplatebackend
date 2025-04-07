import cv2
import base64

def capture_video():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Perform car detection

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

        _, jpeg = cv2.imencode('.jpg', frame_rgb)
        b64_frame = base64.b64encode(jpeg.tobytes()).decode('uft-8')

        yield b64_frame

    cap.release()
