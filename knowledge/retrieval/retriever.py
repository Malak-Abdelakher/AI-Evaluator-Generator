from langchain_core.documents import Document

from cache.retrieval_cache import RetrievalCache
from config.constants import DEFAULT_RETRIEVAL_K
from knowledge.vectorstore.vector_store import (
    VectorStoreService,
)


class KnowledgeRetriever:
    """
    Retrieves relevant knowledge chunks,
    using Redis when possible.
    """

    def __init__(
        self,
        vector_store: VectorStoreService,
        cache: RetrievalCache | None = None,
    ):
        self.vector_store = vector_store
        self.cache = cache

    def retrieve(
        self,
        query: str,
        k: int = DEFAULT_RETRIEVAL_K,
    ) -> list[Document]:

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        if k <= 0:
            raise ValueError(
                "k must be greater than zero."
            )

        if self.cache is not None:
            cached = self.cache.get(
                query,
                k,
            )

            if cached is not None:
                return cached

        documents = (
            self.vector_store
            .similarity_search(
                query=query,
                k=k,
            )
        )

        if self.cache is not None:
            self.cache.set(
                query,
                k,
                documents,
            )

        return documents