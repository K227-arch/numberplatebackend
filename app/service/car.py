from app.repository.car import CarParkingRepository
from app.schemas.car import *
from app.models.car import CarParking

from fastapi.responses import JSONResponse
from fastapi import HTTPException, status


class CarParkingService:
    def __init__(self, car_parking_repository: CarParkingRepository):
        self.car_parking_repository = car_parking_repository

    async def create_car_parking(self, data: CarParkingCreate):

        car_parking_to_create = CarParking(
            number_plate=data.number_plate,
            entrance_time=data.entrance_time,
            exit_time=data.exit_time
        )
        self.car_parking_repository.create_car_parking(car_parking_to_create)

        return JSONResponse("Car parking created")

    async def get_all_car_parking(self):
        cars = self.car_parking_repository.get_all_car_parking()
        if not cars:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No car parking found.")
        return [CarParkingResponse(
            id=car.id,
            number_plate=car.number_plate,
            entrance_time=car.entrance_time,
            exit_time=car.exit_time
        ) for car in cars]

    async def get_logs_after(self, last_seen_time: Optional[datetime]):
        if last_seen_time is None:
            # Initial fetch - get recent N logs
            return self.car_parking_repository.get_recent_logs(limit=10)
        return self.car_parking_repository.get_logs_after_time(last_seen_time)
