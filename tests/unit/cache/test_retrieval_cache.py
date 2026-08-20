import fakeredis

from langchain_core.documents import Document

from cache.cache_service import CacheService
from cache.retrieval_cache import RetrievalCache


def create_retrieval_cache() -> RetrievalCache:
    fake_client = fakeredis.FakeRedis()

    cache_service = CacheService(
        client=fake_client,
        default_ttl=3600,
    )

    return RetrievalCache(
        cache=cache_service,
    )


def test_retrieval_cache_set_and_get_documents():
    cache = create_retrieval_cache()

    documents = [
        Document(
            page_content="Redis can be used as a caching layer.",
            metadata={
                "source": "redis.txt",
                "source_type": "txt",
                "chunk_index": 0,
            },
        ),
        Document(
            page_content="Chroma is used as the vector database.",
            metadata={
                "source": "architecture.txt",
                "source_type": "txt",
                "chunk_index": 1,
            },
        ),
    ]

    cache.set(
        query="What technologies are used?",
        k=4,
        documents=documents,
    )

    result = cache.get(
        query="What technologies are used?",
        k=4,
    )

    assert result is not None
    assert len(result) == 2

    assert isinstance(result[0], Document)
    assert isinstance(result[1], Document)

    assert result[0].page_content == (
        "Redis can be used as a caching layer."
    )

    assert result[0].metadata == {
        "source": "redis.txt",
        "source_type": "txt",
        "chunk_index": 0,
    }

    assert result[1].page_content == (
        "Chroma is used as the vector database."
    )

    assert result[1].metadata == {
        "source": "architecture.txt",
        "source_type": "txt",
        "chunk_index": 1,
    }


def test_retrieval_cache_missing_query_returns_none():
    cache = create_retrieval_cache()

    result = cache.get(
        query="Unknown question",
        k=4,
    )

    assert result is None


def test_retrieval_cache_distinguishes_different_k_values():
    cache = create_retrieval_cache()

    documents = [
        Document(
            page_content="Cached result",
            metadata={
                "source": "test.txt",
                "source_type": "txt",
            },
        )
    ]

    cache.set(
        query="What is cached?",
        k=4,
        documents=documents,
    )

    assert (
        cache.get(
            query="What is cached?",
            k=4,
        )
        is not None
    )

    assert (
        cache.get(
            query="What is cached?",
            k=5,
        )
        is None
    )


def test_retrieval_cache_clear_removes_retrieval_entries():
    cache = create_retrieval_cache()

    documents = [
        Document(
            page_content="Old retrieval result",
            metadata={
                "source": "old.txt",
                "source_type": "txt",
            },
        )
    ]

    cache.set(
        query="What is the answer?",
        k=4,
        documents=documents,
    )

    assert (
        cache.get(
            query="What is the answer?",
            k=4,
        )
        is not None
    )

    deleted_count = cache.clear()

    assert deleted_count == 1

    assert (
        cache.get(
            query="What is the answer?",
            k=4,
        )
        is None
    )