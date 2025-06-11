from app import entities

import abc


class ReviewsStorage(abc.ABC):
    @abc.abstractmethod
    async def add_review(self, text: str, embedding: list[float]) -> int:
        pass

    @abc.abstractmethod
    async def find_similar_reviews(
        self, embedding: list[float], top_k: int
    ) -> list[entities.review.Review]:
        pass
