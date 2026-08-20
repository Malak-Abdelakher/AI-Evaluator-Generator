import json
from typing import Any

from redis import Redis

from cache.redis_client import create_redis_client
from config.constants import CACHE_DEFAULT_TTL


class CacheService:
    """
    Generic JSON-based Redis cache service.
    """

    def __init__(
        self,
        client: Redis | None = None,
        default_ttl: int = CACHE_DEFAULT_TTL,
    ):
        self.client = client or create_redis_client()
        self.default_ttl = default_ttl

    def ping(self) -> bool:
        return bool(self.client.ping())

    def get(self, key: str) -> Any | None:
        value = self.client.get(key)

        if value is None:
            return None

        return json.loads(value)

    def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> None:

        serialized = json.dumps(
            value,
            ensure_ascii=False,
        )

        effective_ttl = (
            self.default_ttl
            if ttl is None
            else ttl
        )

        if effective_ttl > 0:
            self.client.setex(
                key,
                effective_ttl,
                serialized,
            )
        else:
            self.client.set(
                key,
                serialized,
            )

    def delete(self, key: str) -> None:
        self.client.delete(key)

    def exists(self, key: str) -> bool:
        return bool(
            self.client.exists(key)
        )

    def delete_pattern(
        self,
        pattern: str,
    ) -> int:
        keys = list(
            self.client.scan_iter(
                match=pattern
            )
        )

        if not keys:
            return 0

        return int(
            self.client.delete(*keys)
        )