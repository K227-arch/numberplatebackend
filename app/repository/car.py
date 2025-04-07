from app.models.car import CarParking

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from datetime import datetime


class CarParkingRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_car_parking(self, car_parking: CarParking):
        try:
            self.session.add(car_parking)
            self.session.commit()
            self.session.refresh(car_parking)
        except IntegrityError:
            self.session.rollback()
            raise

    def get_all_car_parking(self):
        return self.session.query(CarParking).all()

    def get_recent_logs(self, limit: int = 10):
        return (
            self.session.query(CarParking)
            .order_by(CarParking.timestamp.desc())
            .limit(limit)
            .all()
        )

    def get_logs_after_time(self, last_seen_time: datetime):
        return (
            self.session.query(CarParking)
            .filter(CarParking.timestamp > last_seen_time)
            .order_by(CarParking.timestamp.asc())
            .all()
        )
