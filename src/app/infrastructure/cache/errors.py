from app.usecases.interfaces.cache_storage.errors import (
    CacheError,
    CacheConnectionError as InterfaceCacheConnectionError,
    CacheSerializationError as InterfaceCacheSerializationError,
)


class RedisCacheError(CacheError):
    """Base class for Redis-specific cache errors."""

    pass


class RedisCacheConnectionError(InterfaceCacheConnectionError):
    """Raised when there are Redis-specific connection issues."""

    pass


class RedisCacheSerializationError(InterfaceCacheSerializationError):
    """Raised when there are Redis-specific serialization issues."""

    pass
