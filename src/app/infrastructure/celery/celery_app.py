from celery import Celery
from typing import Optional


class CeleryApp:
    _instance: Optional[Celery] = None

    @classmethod
    def initialize(cls, broker_url: str, backend_url: str) -> None:
        cls._instance = Celery(
            "worker",
            broker=broker_url,
            backend=backend_url,
        )
        cls._instance.conf.task_serializer = "json"
        cls._instance.conf.broker_connection_retry_on_startup = True

    @classmethod
    def get_instance(cls) -> Celery:
        if cls._instance is None:
            raise RuntimeError("Celery app not initialized")
        return cls._instance
