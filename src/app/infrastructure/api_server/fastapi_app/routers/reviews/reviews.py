from fastapi import APIRouter, status
from celery import Celery
from celery.result import AsyncResult

from app import usecases
from . import models

router = APIRouter(prefix="/api/v1/reviews")

reviews_use_cases: usecases.ReviewUseCases = None
celery_app = Celery(
    "worker",
    broker="redis://:password@localhost:6379/0",
    backend="redis://:password@localhost:6379/0",
)


@router.post("/add")
async def add_review(body: models.TextBody):  # todo: return view
    error_code, error_message = None, None
    try:
        await reviews_use_cases.add_review(body.text)
    except usecases.errors.ReviewsStorageError as exc:
        error_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_message = str(exc)

    if error_code is not None and error_message is not None:
        return {"error_code": error_code, "message": error_message}


@router.post("/find_similar")
async def find_similar(body: models.TextBody, top_k: int):
    task = celery_app.send_task("process_review", args=[body.text, top_k])
    return {"task_id": task.id}


@router.get("/status/{task_id}")  # todo: better endpoint
async def get_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.ready():
        return {"status": "done", "result": task_result.result}
    return {"status": "pending"}
