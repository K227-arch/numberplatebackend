import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.utils.connectionManager import ConnectionManager
from app.utils.detector import capture_video
from typing import List
from app.service.car import CarParkingService
from app.repository.car import CarParkingRepository
from app.schemas.car import *
from app.database.database import get_session
from sqlalchemy.orm import Session
from datetime import datetime

def get_car_parking_service(session: Session = Depends(get_session)) -> CarParkingService:
    car_parking_repository = CarParkingRepository(session)
    return CarParkingService(car_parking_repository)

manager = ConnectionManager()

car_app = APIRouter()

# Flag to manage video stream status
video_streaming: bool = False
video_clients: List[WebSocket] = []

@car_app.websocket("/ws/video")
async def video_stream(
    websocket: WebSocket,
    car_parking_service: CarParkingService = Depends(get_car_parking_service)
):
    global video_streaming
    await manager.connect(websocket)
    video_clients.append(websocket)

    # Set the flag to True when video streaming starts
    video_streaming = True
    video_gen = capture_video()

    try:
        # Send video frames to client while streaming is active
        for frame in video_gen:
            if not video_streaming:
                break
            await manager.broadcast(frame)
            await asyncio.sleep(0.05)

    except WebSocketDisconnect:
        print("WebSocket disconnected")

    finally:
        # Clean up when the connection closes
        video_clients.remove(websocket)
        await manager.disconnect(websocket)

        # Stop the video stream if no clients are connected
        if not video_clients:
            video_streaming = False

@car_app.post("/stop-video")
async def stop_video():
    global video_streaming
    video_streaming = False

    # Close all video WebSocket clients
    for client in video_clients[:]:
        await client.close()
        await manager.disconnect(client)

    return {"message": "Video stream stopped and all video connections closed"}

# Log streaming function (example)
log_clients: List[WebSocket] = []

@car_app.websocket("/ws/logs")
async def log_stream(websocket: WebSocket, car_parking_service: CarParkingService = Depends(get_car_parking_service)):
    await manager.connect(websocket)
    log_clients.append(websocket)

    last_seen_time = datetime.utcnow()

    try:
        while True:
            # Query new logs after the last seen time
            new_logs = await car_parking_service.get_logs_after(last_seen_time)

            if new_logs:
                # Convert logs to response format
                logs_data = [
                    {
                        "id": log.id,
                        "number_plate": log.number_plate,
                        "entrance_time": log.entrance_time.isoformat(),
                        "exit_time": log.exit_time.isoformat() if log.exit_time else None
                    }
                    for log in new_logs
                ]
                # Update last seen time
                last_seen_time = new_logs[-1].entrance_time

                await websocket.send_text(json.dumps(logs_data))

            await asyncio.sleep(2)  # wait before next check

    except WebSocketDisconnect:
        log_clients.remove(websocket)
        await manager.disconnect(websocket)

@car_app.post("/disconnect-log")
async def disconnect_log():
    # Close all log WebSocket connections
    for client in log_clients[:]:
        await client.close()
        log_clients.remove(client)
        await manager.disconnect(client)

    return {"message": "All log connections closed"}



