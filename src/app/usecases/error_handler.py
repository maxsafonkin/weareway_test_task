from typing import Callable
from functools import wraps

from . import errors
from . import interfaces

ERRORS_CONVERTER = {
    interfaces.embedder.errors.EmbedderError: errors.EmbeddingError,
    interfaces.reviews_storage.errors.InsertionError: errors.InsertionError,
    interfaces.reviews_storage.errors.ReviewsStorageError: errors.ReviewsStorageError,
    Exception: errors.ReviewsStorageError,
}


def handle_interfaces_error(function: Callable) -> Callable:
    @wraps(function)
    async def wrapper(*args, **kwargs):
        try:
            return await function(*args, **kwargs)
        except Exception as exc:
            for ERROR, ERROR_TO_RAISE in ERRORS_CONVERTER.items():
                if isinstance(exc, ERROR):
                    raise ERROR_TO_RAISE(str(exc)) from exc

    return wrapper
