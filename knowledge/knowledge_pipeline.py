from pathlib import Path

from langchain_core.documents import Document
from cache.retrieval_cache import RetrievalCache
from ingestion.pipeline import IngestionPipeline
from knowledge.embeddings.embedding_service import (
    EmbeddingService,
)
from knowledge.retrieval.context_builder import (
    build_context,
)
from knowledge.retrieval.retriever import (
    KnowledgeRetriever,
)
from knowledge.vectorstore.vector_store import (
    VectorStoreService,
)


class KnowledgePipeline:
    """
    Complete external knowledge pipeline.

    File
      -> Load
      -> Process
      -> Chunk
      -> Embed
      -> Store
      -> Retrieve
    """

    def __init__(
        self,
        ingestion_pipeline: IngestionPipeline,
        vector_store: VectorStoreService,
        retriever: KnowledgeRetriever,
    ):
        self.ingestion_pipeline = (
            ingestion_pipeline
        )
        self.vector_store = vector_store
        self.retriever = retriever

    @classmethod
    def create_default(cls):
        embedding_service = EmbeddingService()
        
        vector_store = VectorStoreService(
            embedding_function=(
                embedding_service.embeddings
            )
        )
        retrieval_cache = RetrievalCache()

        retriever = KnowledgeRetriever(
            vector_store=vector_store,
            cache=retrieval_cache,
        )

        return cls(
            ingestion_pipeline=(
                IngestionPipeline()
            ),
            vector_store=vector_store,
            retriever=retriever,
        )

    def ingest_file(
        self,
        source: str | Path,
    ) -> dict:

        chunks = (
            self.ingestion_pipeline
            .ingest_file(source)
        )

        ids = self.vector_store.add_documents(
            chunks
        )
        if self.retriever.cache is not None:
            self.retriever.cache.clear()

        return {
            "source": str(source),
            "chunks_created": len(chunks),
            "chunks_stored": len(ids),
        }

    def retrieve(
        self,
        query: str,
        k: int = 4,
    ) -> list[Document]:

        return self.retriever.retrieve(
            query=query,
            k=k,
        )

    def retrieve_context(
        self,
        query: str,
        k: int = 4,
    ) -> str:

        documents = self.retrieve(
            query=query,
            k=k,
        )

        return build_context(documents)