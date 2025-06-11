import asyncio
import os
import logging

from app import infrastructure, usecases
from app.infrastructure.celery.celery_app import CeleryApp
from utils import ServiceConfig
from utils.logging_config import setup_logging


# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

logger.info("Starting worker...")

config_path = os.environ["SERVICE_CONFIG_PATH"]
service_config = ServiceConfig.load(config_path)
logger.info("Service configuration loaded")

db_config = infrastructure.storage.ReviewsStorageConfig(
    **service_config.postgres_config.model_dump()
)
reviews_storage = infrastructure.storage.ReviewsStorage(db_config=db_config)
logger.info("Database storage initialized")

embedder = infrastructure.embedder.Embedder(
    **service_config.embedder_config.model_dump()
)
logger.info("Embedder initialized")

cache = infrastructure.cache.redis_cache.RedisCache(config=service_config.redis_config)
logger.info("Cache initialized")

reviews_use_cases = usecases.ReviewUseCases(
    embedder=embedder, reviews_storage=reviews_storage, cache=cache
)
logger.info("Review use cases initialized")

CeleryApp.initialize(
    broker_url=service_config.redis_config.url,
    backend_url=service_config.redis_config.url,
)
celery_app = CeleryApp.get_instance()
logger.info("Celery app configured")


async def _process_review_async(text: str, top_k: int):
    logger.info(f"Processing review with top_k={top_k}")
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
    logger.info(f"Received task to process review with top_k={top_k}")
    loop = get_or_create_eventloop()
    try:
        result = loop.run_until_complete(_process_review_async(text, top_k))
        logger.info(
            f"Successfully processed review, found {len(result)} similar reviews"
        )
        return [review.to_dict() for review in result]
    except RuntimeError as e:
        if "loop is closed" not in str(e):
            logger.error(f"Error processing review: {str(e)}")
            raise
        logger.warning("Event loop was closed, creating new one")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(_process_review_async(text, top_k))
        logger.info(
            f"Successfully processed review with new loop, found {len(result)} similar reviews"
        )
        return [review.to_dict() for review in result]
