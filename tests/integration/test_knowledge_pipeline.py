import uuid

from ingestion.pipeline import (
    IngestionPipeline,
)
from knowledge.knowledge_pipeline import (
    KnowledgePipeline,
)
from knowledge.retrieval.retriever import (
    KnowledgeRetriever,
)
from knowledge.vectorstore.vector_store import (
    VectorStoreService,
)
from tests.unit.knowledge.fake_embeddings import (
    FakeKeywordEmbeddings,
)


def test_txt_to_semantic_retrieval(
    tmp_path,
):
    file_path = tmp_path / "knowledge.txt"

    file_path.write_text(
        (
            "Redis is a fast in-memory database "
            "that can be used for caching.\n\n"
            "LCEL is LangChain Expression Language "
            "and connects runnable components."
        ),
        encoding="utf-8",
    )

    vector_store = VectorStoreService(
        embedding_function=(
            FakeKeywordEmbeddings()
        ),
        collection_name=(
            f"test_{uuid.uuid4().hex}"
        ),
        persist_directory=None,
    )

    retriever = KnowledgeRetriever(
        vector_store
    )

    pipeline = KnowledgePipeline(
        ingestion_pipeline=(
            IngestionPipeline()
        ),
        vector_store=vector_store,
        retriever=retriever,
    )

    result = pipeline.ingest_file(
        file_path
    )

    assert result["chunks_stored"] > 0

    documents = pipeline.retrieve(
        "What is used for caching?",
        k=1,
    )

    assert len(documents) == 1
    assert "Redis" in documents[0].page_content