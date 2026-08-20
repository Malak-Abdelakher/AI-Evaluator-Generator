from redis import Redis

import config.settings  # noqa: F401

from config.constants import REDIS_URL


def create_redis_client() -> Redis:
    """
    Create the Redis client used by the application.
    """

    return Redis.from_url(
        REDIS_URL,
        decode_responses=True,
    )