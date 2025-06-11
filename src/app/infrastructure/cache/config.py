from utils import StrictModel


class RedisConfig(StrictModel):
    host: str
    port: int
    password: str
    db: int

    @property
    def url(self) -> str:
        """Get Redis connection URL."""
        return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
