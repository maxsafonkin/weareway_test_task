import logging
from app import entities
from . import interfaces
from .error_handler import handle_interfaces_error
import hashlib


logger = logging.getLogger(__name__)


class ReviewUseCases:
    def __init__(
        self,
        embedder: interfaces.embedder.Embedder,
        reviews_storage: interfaces.reviews_storage.ReviewsStorage,
        cache: interfaces.cache_storage.CacheInterface,
    ):
        self._embedder = embedder
        self._reviews_storage = reviews_storage
        self._cache = cache

    @handle_interfaces_error
    async def add_review(self, text: str) -> entities.review.Review:
        logger.info("Adding new review")
        embedding = self._embedder.get_embedding(text=text)
        logger.debug("Generated embedding for review")
        id = await self._reviews_storage.add_review(text=text, embedding=embedding)
        logger.info(f"Review added successfully with id: {id}")
        return entities.review.Review(id=id, text=text)

    def _generate_cache_key(self, text: str, top_k: int) -> str:
        """Generate a cache key for similar reviews search."""
        key_data = f"{text}:{top_k}"
        return f"similar_reviews:{hashlib.md5(key_data.encode()).hexdigest()}"

    @handle_interfaces_error
    async def find_similar_reviews(
        self, text: str, top_k: int
    ) -> list[entities.review.Review]:
        logger.info(f"Finding similar reviews with top_k={top_k}")
        cache_key = self._generate_cache_key(text, top_k)
        logger.debug(f"Generated cache key: {cache_key}")

        cached_result = await self._cache.get(cache_key)
        if cached_result is not None:
            logger.info("Found results in cache")
            return [entities.review.Review(**review) for review in cached_result]

        logger.info("Cache miss, computing similar reviews")
        embedding = self._embedder.get_embedding(text=text)
        logger.debug("Generated embedding for search")

        reviews = await self._reviews_storage.find_similar_reviews(
            embedding=embedding, top_k=top_k
        )
        logger.info(f"Found {len(reviews)} similar reviews")

        logger.debug("Caching results")
        await self._cache.set(
            cache_key,
            [review.model_dump() for review in reviews],
            expire=3600,
        )

        return reviews
