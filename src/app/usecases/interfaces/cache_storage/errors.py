class CacheError(Exception):
    """Base class for cache-related errors."""

    pass


class CacheConnectionError(CacheError):
    """Raised when there are connection issues with the cache."""

    pass


class CacheSerializationError(CacheError):
    """Raised when there are issues serializing/deserializing cache data."""

    pass
