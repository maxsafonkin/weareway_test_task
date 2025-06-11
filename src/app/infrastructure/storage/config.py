from utils import StrictModel


class ReviewsStorageConfig(StrictModel):
    host: str
    port: int
    user: str
    password: str
    db_name: str
