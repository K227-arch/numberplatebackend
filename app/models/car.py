from sqlalchemy import Column, DateTime, Integer, String, LargeBinary

from app.database.database import Base

class CarParking(Base):
    __tablename__ = "car_parking"
    id = Column(Integer, primary_key=True, autoincrement=True)
    number_plate = Column(String(20), nullable=True)
    entrance_time = Column(DateTime, nullable=True, default=None)
    exit_time = Column(DateTime, nullable=True, default=None)
    image_data = Column(LargeBinary, nullable=True)

