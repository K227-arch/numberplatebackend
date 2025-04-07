from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class CarParkingBase(BaseModel):
    number_plate: Optional[str] = None
    entrance_time: Optional[datetime] = None
    exit_time: Optional[datetime] = None


class CarParkingCreate(CarParkingBase):
    pass


class CarParkingUpdate(CarParkingBase):
    pass


class CarParkingInDB(CarParkingBase):
    id: int


class CarParkingResponse(CarParkingInDB):
    pass
