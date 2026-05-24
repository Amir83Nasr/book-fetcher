"""Cache helpers - Redis and In-Memory."""

import json
from typing import Any

import redis

from app.config import settings

# ========== Redis Cache ==========
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
)


def get_cache_redis(key: str) -> dict | None:
    data = redis_client.get(key)
    return json.loads(data) if data else None


def set_cache_redis(key: str, value: Any, ttl: int = None) -> None:
    if ttl is None:
        ttl = settings.REDIS_CACHE_TTL
    redis_client.setex(key, ttl, json.dumps(value, default=str))


# ========== In-Memory Cache ==========
_memory_cache: dict = {}


def get_cache_memory(key: str) -> dict | None:
    return _memory_cache.get(key)


def set_cache_memory(key: str, value: Any) -> None:
    _memory_cache[key] = value


# ========== Default (Redis) ==========
def get_cache(key: str) -> dict | None:
    return get_cache_redis(key)


def set_cache(key: str, value: Any, ttl: int = None) -> None:
    set_cache_redis(key, value, ttl)


# ========== Utilities ==========
def delete_cache(pattern: str = "*") -> None:
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)
    _memory_cache.clear()


def cache_key(*parts: str) -> str:
    return ":".join(parts)
