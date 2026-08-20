from langchain_core.documents import Document

from config.constants import DEFAULT_RETRIEVAL_K
from knowledge.vectorstore.vector_store import (
    VectorStoreService,
)


class KnowledgeRetriever:
    """
    Retrieves relevant knowledge chunks
    from the vector store.
    """

    def __init__(
        self,
        vector_store: VectorStoreService,
    ):
        self.vector_store = vector_store

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

        return self.vector_store.similarity_search(
            query=query,
            k=k,
        )