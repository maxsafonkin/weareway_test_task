from fastapi import FastAPI

from app import usecases
from . import routers


def get_app(reviews_use_cases: usecases.ReviewUseCases) -> FastAPI:
    app = FastAPI()

    routers.reviews.reviews_use_cases = reviews_use_cases

    app.include_router(routers.reviews.router)

    return app
