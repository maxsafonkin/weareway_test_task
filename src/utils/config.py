import json

from typing import Self
from .strict_model import StrictModel


class EmbedderConfig(StrictModel):
    model_path: str
    device: str


class PostgreSQLConfig(StrictModel):
    host: str
    port: int
    user: str
    password: str
    db_name: str


class ServiceConfig(StrictModel):
    embedder_config: EmbedderConfig
    postgres_config: PostgreSQLConfig

    @classmethod
    def load(cls, path: str) -> Self:
        with open(path, "r") as f:
            raw_config = json.load(f)

        return cls(**raw_config)
