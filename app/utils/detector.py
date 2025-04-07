import cv2
import base64
import logging


def capture_video():
    try:
        # Try to access the webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Could not open webcam")

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # Perform car detection (you can add your detection logic here)

            # Convert frame to RGB (if needed for further processing)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

            # Encode frame as JPEG and then base64
            _, jpeg = cv2.imencode('.jpg', frame_rgb)
            b64_frame = base64.b64encode(jpeg.tobytes()).decode('utf-8')

            # Yield base64-encoded frame
            yield b64_frame

    except RuntimeError as e:
        # Log the error if webcam cannot be accessed
        logging.error(f"Error occurred while accessing the webcam: {str(e)}")
        return {"error": str(e), "message": "Unable to access the webcam. Please check the connection or try again."}

    except Exception as e:
        # Catch other unexpected errors
        logging.error(f"Unexpected error occurred: {str(e)}")
        return {"error": "An unexpected error occurred", "message": "Please try again later."}

    finally:
        # Ensure the webcam resource is released if it's opened
        if 'cap' in locals() and cap.isOpened():
            cap.release()
