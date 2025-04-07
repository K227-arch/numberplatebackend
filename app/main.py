from fastapi import FastAPI

from app.routes.car import car_app


def create_application():
    application = FastAPI()
    # Users
    application.include_router(car_app)

    return application

app = create_application()


@app.get("/")
def index():
    return {"message": "set up is up and running"}