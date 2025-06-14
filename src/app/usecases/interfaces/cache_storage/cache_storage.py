from abc import ABC, abstractmethod
from typing import Any, Optional


class CacheInterface(ABC):
    """Interface for cache operations."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache by key."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: int = 3600) -> None:
        """Set value in cache with optional expiration time in seconds."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete value from cache by key."""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        pass
