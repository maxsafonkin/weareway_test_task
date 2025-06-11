import os
import logging
from celery import Celery

from app import infrastructure, usecases
from utils import ServiceConfig
from utils.logging_config import setup_logging


def main():
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting API server...")

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

    cache = infrastructure.cache.RedisCache(config=service_config.redis_config)
    logger.info("Cache initialized")

    reviews_use_cases = usecases.ReviewUseCases(
        embedder=embedder, reviews_storage=reviews_storage, cache=cache
    )
    logger.info("Review use cases initialized")

    celery_app = Celery(
        "worker",
        broker=service_config.redis_config.url,
        backend=service_config.redis_config.url,
    )
    logger.info("Celery app configured")

    api_server = infrastructure.api_server.FastAPIServer(
        reviews_use_cases=reviews_use_cases, celery_app=celery_app
    )
    logger.info("API server initialized, starting...")
    api_server.start()


if __name__ == "__main__":
    main()
