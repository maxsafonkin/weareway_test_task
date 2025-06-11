import os
from celery import Celery

from app import infrastructure, usecases
from utils import ServiceConfig


def main():
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

    celery_app = Celery(
        "worker",
        broker=service_config.redis_config.url,
        backend=service_config.redis_config.url,
    )
    celery_app.conf.task_serializer = "json"

    api_server = infrastructure.api_server.FastAPIServer(
        reviews_use_cases=reviews_use_cases,
        celery_app=celery_app
    )
    api_server.start()


if __name__ == "__main__":
    main()
