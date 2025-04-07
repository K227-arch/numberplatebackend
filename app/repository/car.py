from app.models.car import CarParking

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


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