import asyncio
import os

from app import infrastructure, usecases
from app.infrastructure.celery.celery_app import CeleryApp
from utils import ServiceConfig


config_path = os.environ["SERVICE_CONFIG_PATH"]
service_config = ServiceConfig.load(config_path)

db_config = infrastructure.storage.ReviewsStorageConfig(
    **service_config.postgres_config.model_dump()
)
reviews_storage = infrastructure.storage.ReviewsStorage(db_config=db_config)
embedder = infrastructure.embedder.Embedder(
    **service_config.embedder_config.model_dump()
)
reviews_use_cases = usecases.ReviewUseCases(
    embedder=embedder, reviews_storage=reviews_storage
)

# Initialize Celery app
CeleryApp.initialize(
    broker_url=service_config.redis_config.url,
    backend_url=service_config.redis_config.url,
)
celery_app = CeleryApp.get_instance()
celery_app.conf.task_serializer = "json"


async def _process_review_async(text: str, top_k: int):
    return await reviews_use_cases.find_similar_reviews(text, top_k)


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


@celery_app.task(name="process_review")
def process_review(text: str, top_k: int):
    loop = get_or_create_eventloop()
    try:
        result = loop.run_until_complete(_process_review_async(text, top_k))
        return [review.to_dict() for review in result]
    except RuntimeError as e:
        if "loop is closed" not in str(e):
            raise
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(_process_review_async(text, top_k))
        return [review.to_dict() for review in result]
