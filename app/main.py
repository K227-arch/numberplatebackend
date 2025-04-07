from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import cv2
import base64
import asyncio



app = FastAPI()

@app.websocket("/ws/video")
async def video_stream(websocket: WebSocket):
    await websocket.accept()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        await websocket.close(code=1011)
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            _, jpeg = cv2.imencode('.jpg', frame)
            b64_jpeg = base64.b64encode(jpeg.tobytes()).decode('utf-8')

            await websocket.send_text(b64_jpeg)
            await asyncio.sleep(0.03)  # 30 fps

    except WebSocketDisconnect:
        print("Client disconnected")

    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        cap.release()
        try:
            await websocket.close()
        except RuntimeError:
            # Already closed
            pass


@app.get("/")
def index():
    return {"message": "set up is up and running"}