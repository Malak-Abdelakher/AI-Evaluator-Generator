import hashlib
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from config.constants import (
    CHROMA_COLLECTION_NAME,
    CHROMA_PERSIST_DIRECTORY,
)


class VectorStoreService:
    """
    Wrapper around the Chroma vector store.
    """

    def __init__(
        self,
        embedding_function: Embeddings,
        collection_name: str = CHROMA_COLLECTION_NAME,
        persist_directory: str | Path | None = (
            CHROMA_PERSIST_DIRECTORY
        ),
    ):
        if persist_directory is not None:
            Path(persist_directory).mkdir(
                parents=True,
                exist_ok=True,
            )

        self._store = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_function,
            persist_directory=(
                str(persist_directory)
                if persist_directory is not None
                else None
            ),
        )

    @staticmethod
    def _create_document_id(
        document: Document,
    ) -> str:
        """
        Create a stable ID based on document source,
        location, chunk and content.
        """

        metadata = document.metadata

        identity = "|".join(
            [
                str(metadata.get("source", "")),
                str(metadata.get("page", "")),
                str(metadata.get("slide", "")),
                str(metadata.get("chunk_index", "")),
                document.page_content,
            ]
        )

        return hashlib.sha256(
            identity.encode("utf-8")
        ).hexdigest()

    def add_documents(
        self,
        documents: list[Document],
    ) -> list[str]:

        if not documents:
            return []

        ids = [
            self._create_document_id(document)
            for document in documents
        ]

        self._store.add_documents(
            documents=documents,
            ids=ids,
        )

        return ids

    def similarity_search(
        self,
        query: str,
        k: int = 4,
    ) -> list[Document]:

        if not query.strip():
            raise ValueError(
                "Search query cannot be empty."
            )

        return self._store.similarity_search(
            query=query,
            k=k,
        )

    def as_retriever(
        self,
        k: int = 4,
    ):
        return self._store.as_retriever(
            search_kwargs={
                "k": k,
            }
        )