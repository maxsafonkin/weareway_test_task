from app import entities
from app.usecases import interfaces

from . import config
from .models import Review, Base
from . import errors

from sqlalchemy import select, text, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class ReviewsStorage(interfaces.reviews_storage.ReviewsStorage):
    def __init__(self, db_config: config.ReviewsStorageConfig):
        conn_uri = f"postgresql+asyncpg://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.db_name}"
        engine = create_async_engine(conn_uri, echo=True)
        self._sessionmaker = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

        self._init_db_sync(db_config)

    def _init_db_sync(self, db_config: config.ReviewsStorageConfig):
        """Initialize database extensions and tables synchronously."""
        sync_uri = f"postgresql://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.db_name}"
        sync_engine = create_engine(sync_uri, echo=True)

        with sync_engine.begin() as conn:
            try:
                conn.execute(
                    text("CREATE EXTENSION IF NOT EXISTS vector SCHEMA public")
                )
            except SQLAlchemyError:
                result = conn.execute(
                    text("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
                )
                if not result.scalar():
                    raise

            Base.metadata.create_all(bind=conn, checkfirst=True)

    async def add_review(self, text: str, embedding: list[float]) -> int:
        review = Review(text=text, embedding=embedding)
        async with self._sessionmaker() as session:
            try:
                async with session.begin():
                    session.add(review)
                    await session.flush()
                    await session.refresh(review)
            except SQLAlchemyError as exc:
                await session.rollback()
                raise errors.ReviewsStorageError(str(exc)) from exc
            finally:
                await session.close()

        return int(review.id)

    async def find_similar_reviews(
        self, embedding: list[float], top_k: int
    ) -> list[entities.review.Review]:
        query = (
            select(Review)
            .order_by(Review.embedding.cosine_distance(embedding))
            .limit(top_k)
        )

        async with self._sessionmaker() as session:
            try:
                async with session.begin():
                    result = await session.execute(query)
                    similar_reviews = result.scalars().all()
            except SQLAlchemyError as exc:
                raise errors.ReviewsStorageError(str(exc)) from exc
            finally:
                await session.close()

        return [
            entities.review.Review(id=review.id, text=review.text)
            for review in similar_reviews
        ]
