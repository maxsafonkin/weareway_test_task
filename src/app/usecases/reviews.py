from app import entities
from . import interfaces
from .error_handler import handle_interfaces_error


class ReviewUseCases:
    def __init__(
        self,
        embedder: interfaces.embedder.Embedder,
        reviews_storage: interfaces.reviews_storage.ReviewsStorage,
    ):
        self._embedder = embedder
        self._reviews_storage = reviews_storage

    @handle_interfaces_error
    async def add_review(self, text: str) -> entities.review.Review:
        embedding = self._embedder.get_embedding(text=text)
        id = await self._reviews_storage.add_review(text=text, embedding=embedding)
        return entities.review.Review(id=id, text=text)

    @handle_interfaces_error
    async def find_similar_reviews(
        self, text: str, top_k: int
    ) -> list[entities.review.Review]:
        embedding = self._embedder.get_embedding(text=text)
        reviews = await self._reviews_storage.find_similar_reviews(
            embedding=embedding, top_k=top_k
        )

        return reviews
