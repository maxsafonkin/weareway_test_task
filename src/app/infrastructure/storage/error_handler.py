from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from . import errors


def handle_sql_errors(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with self._sessionmaker() as session:
            try:
                # Provide session to the method
                result = await func(self, session, *args, **kwargs)
                return result
            except SQLAlchemyError as exc:
                await session.rollback()
                raise errors.ReviewsStorageError(str(exc)) from exc
            finally:
                await session.close()

    return wrapper
