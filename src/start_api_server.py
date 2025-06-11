import os

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
    api_server = infrastructure.api_server.FastAPIServer(
        reviews_use_cases=reviews_use_cases
    )
    api_server.start()


if __name__ == "__main__":
    main()
