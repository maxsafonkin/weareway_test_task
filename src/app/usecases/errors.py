class ReviewUseCasesError(Exception):
    """Base review use case error"""

    pass


class EmbeddingError(ReviewUseCasesError):
    """Raised whenever embedding process failed"""


class ReviewsStorageError(ReviewUseCasesError):
    """Raised whenever storage process failed"""


class InsertionError(ReviewsStorageError):
    """Raised whenever review insertion failed"""
