from langchain_core.documents import Document

from cache.cache_keys import (
    retrieval_cache_key,
)
from cache.cache_service import CacheService


class RetrievalCache:
    """
    Redis cache for retrieved knowledge chunks.
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
        query: str,
        k: int,
    ) -> list[Document] | None:

        key = retrieval_cache_key(
            query,
            k,
        )

        data = self.cache.get(key)

        if data is None:
            return None

        return [
            Document(
                page_content=item[
                    "page_content"
                ],
                metadata=item[
                    "metadata"
                ],
            )
            for item in data
        ]

    def set(
        self,
        query: str,
        k: int,
        documents: list[Document],
    ) -> None:

        key = retrieval_cache_key(
            query,
            k,
        )

        data = [
            {
                "page_content": (
                    document.page_content
                ),
                "metadata": (
                    document.metadata
                ),
            }
            for document in documents
        ]

        self.cache.set(
            key,
            data,
        )

    def clear(self) -> int:
        return self.cache.delete_pattern(
            "retrieval:*"
        )