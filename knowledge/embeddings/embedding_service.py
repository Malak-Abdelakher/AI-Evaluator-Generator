from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

from config.constants import EMBEDDING_MODEL_NAME


class EmbeddingService:
    """
    Provides the embedding model used by
    the external knowledge system.
    """

    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL_NAME,
    ):
        self._embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            encode_kwargs={
                "normalize_embeddings": True,
            },
        )

    @property
    def embeddings(self) -> Embeddings:
        return self._embeddings

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        return self._embeddings.embed_query(query)

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return self._embeddings.embed_documents(texts)