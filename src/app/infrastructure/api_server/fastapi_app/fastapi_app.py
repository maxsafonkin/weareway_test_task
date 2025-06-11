from fastapi import FastAPI
from celery import Celery

from app import usecases
from . import routers


def get_app(reviews_use_cases: usecases.ReviewUseCases, celery_app: Celery) -> FastAPI:
    app = FastAPI()

    routers.reviews.reviews_use_cases = reviews_use_cases
    routers.reviews.celery_app = celery_app

    app.include_router(routers.reviews.router)

    return app
