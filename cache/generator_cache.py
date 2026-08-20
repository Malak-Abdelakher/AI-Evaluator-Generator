from cache.cache_keys import (
    generator_cache_key,
)
from cache.cache_service import CacheService


class GeneratorCache:
    """
    Redis cache for Generator LLM responses.
    """

    def __init__(
        self,
        cache: CacheService | None = None,
    ):
        self.cache = (
            cache or CacheService()
        )

    def get(
        self,
        question: str,
        context: str,
        history: str,
        feedback: str,
        model: str,
    ) -> str | None:

        key = generator_cache_key(
            question=question,
            context=context,
            history=history,
            feedback=feedback,
            model=model,
        )

        return self.cache.get(key)

    def set(
        self,
        question: str,
        context: str,
        history: str,
        feedback: str,
        model: str,
        answer: str,
    ) -> None:

        key = generator_cache_key(
            question=question,
            context=context,
            history=history,
            feedback=feedback,
            model=model,
        )

        self.cache.set(
            key,
            answer,
        )

    def clear(self) -> int:
        return self.cache.delete_pattern(
            "generator:*"
        )