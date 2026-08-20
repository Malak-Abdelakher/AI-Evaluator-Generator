import pytest

from langchain_core.documents import Document

from knowledge.knowledge_pipeline import KnowledgePipeline


class FakeIngestionPipeline:
    def ingest_file(self, source):
        return [
            Document(
                page_content="New knowledge",
                metadata={
                    "source": str(source),
                    "source_type": "txt",
                    "chunk_index": 0,
                },
            )
        ]


class FakeVectorStore:
    def __init__(self, should_fail=False):
        self.should_fail = should_fail
        self.received_documents = None

    def add_documents(self, documents):
        if self.should_fail:
            raise RuntimeError(
                "Simulated vector store failure."
            )

        self.received_documents = documents

        return ["chunk-id-1"]


class FakeRetrievalCache:
    def __init__(self):
        self.clear_calls = 0

    def clear(self):
        self.clear_calls += 1
        return 1


class FakeRetriever:
    def __init__(self, cache):
        self.cache = cache


def test_successful_ingestion_clears_retrieval_cache():
    retrieval_cache = FakeRetrievalCache()

    pipeline = KnowledgePipeline(
        ingestion_pipeline=FakeIngestionPipeline(),
        vector_store=FakeVectorStore(),
        retriever=FakeRetriever(
            cache=retrieval_cache,
        ),
    )

    result = pipeline.ingest_file(
        "new_knowledge.txt"
    )

    assert result["chunks_created"] == 1
    assert result["chunks_stored"] == 1

    assert retrieval_cache.clear_calls == 1


def test_failed_vector_store_write_does_not_clear_cache():
    retrieval_cache = FakeRetrievalCache()

    pipeline = KnowledgePipeline(
        ingestion_pipeline=FakeIngestionPipeline(),
        vector_store=FakeVectorStore(
            should_fail=True,
        ),
        retriever=FakeRetriever(
            cache=retrieval_cache,
        ),
    )

    with pytest.raises(
        RuntimeError,
        match="Simulated vector store failure",
    ):
        pipeline.ingest_file(
            "new_knowledge.txt"
        )

    assert retrieval_cache.clear_calls == 0