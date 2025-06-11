from app.usecases.interfaces.reviews_storage import errors


class ReviewsStorageError(errors.ReviewsStorageError):
    pass


class InsertionError(errors.InsertionError):
    pass
