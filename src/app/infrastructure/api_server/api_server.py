import uvicorn

from app import usecases
from .fastapi_app import get_app


class FastAPIServer:
    __SERVER_PORT = 7890

    def __init__(self, reviews_use_cases: usecases.ReviewUseCases) -> None:
        self._reviews_use_cases = reviews_use_cases

    def start(self) -> None:
        config = uvicorn.Config(
            app=get_app(self._reviews_use_cases),
            host="0.0.0.0",
            port=self.__SERVER_PORT,
        )
        server = uvicorn.Server(config)
        server.run()
