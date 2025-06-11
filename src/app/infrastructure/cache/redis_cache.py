import json
from typing import Any, Optional

import redis.asyncio as redis
from app.usecases.interfaces.cache_storage import CacheInterface
from .config import RedisConfig
from .errors import RedisCacheConnectionError, RedisCacheSerializationError


class RedisCache(CacheInterface):
    """Redis implementation of cache interface."""

    def __init__(self, config: RedisConfig):
        try:
            self._redis = redis.Redis(
                host=config.host,
                port=config.port,
                password=config.password,
                db=config.db,
                decode_responses=True,
            )
        except redis.ConnectionError as e:
            raise RedisCacheConnectionError(f"Failed to connect to Redis: {str(e)}")

    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache by key."""
        try:
            value = await self._redis.get(key)
            if value is None:
                return None
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except redis.RedisError as e:
            raise RedisCacheConnectionError(f"Failed to get value from Redis: {str(e)}")

    async def set(self, key: str, value: Any, expire: int = 3600) -> None:
        """Set value in Redis cache with optional expiration time in seconds."""
        try:
            if isinstance(value, (dict, list)):
                try:
                    value = json.dumps(value)
                except (TypeError, ValueError) as e:
                    raise RedisCacheSerializationError(
                        f"Failed to serialize value: {str(e)}"
                    )
            elif not isinstance(value, (str, bytes)):
                value = str(value)

            await self._redis.set(key, value, ex=expire)
        except redis.RedisError as e:
            raise RedisCacheConnectionError(f"Failed to set value in Redis: {str(e)}")

    async def delete(self, key: str) -> None:
        """Delete value from Redis cache by key."""
        try:
            await self._redis.delete(key)
        except redis.RedisError as e:
            raise RedisCacheConnectionError(
                f"Failed to delete value from Redis: {str(e)}"
            )

    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis cache."""
        try:
            return bool(await self._redis.exists(key))
        except redis.RedisError as e:
            raise RedisCacheConnectionError(
                f"Failed to check key existence in Redis: {str(e)}"
            )
