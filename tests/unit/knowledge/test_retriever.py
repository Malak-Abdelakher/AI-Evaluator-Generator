import uuid

from langchain_core.documents import Document

from knowledge.retrieval.context_builder import (
    build_context,
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


def create_test_store():
    return VectorStoreService(
        embedding_function=FakeKeywordEmbeddings(),
        collection_name=(
            f"test_{uuid.uuid4().hex}"
        ),
        persist_directory=None,
    )


def test_vector_store_adds_documents():
    store = create_test_store()

    documents = [
        Document(
            page_content=(
                "Redis provides caching."
            ),
            metadata={
                "source": "notes.txt",
                "source_type": "txt",
                "chunk_index": 0,
            },
        )
    ]

    ids = store.add_documents(documents)

    assert len(ids) == 1


def test_similarity_search():
    store = create_test_store()

    store.add_documents(
        [
            Document(
                page_content=(
                    "Redis is used for caching."
                ),
                metadata={
                    "source": "redis.txt",
                    "source_type": "txt",
                    "chunk_index": 0,
                },
            ),
            Document(
                page_content=(
                    "LCEL connects LangChain "
                    "runnables."
                ),
                metadata={
                    "source": "lcel.txt",
                    "source_type": "txt",
                    "chunk_index": 0,
                },
            ),
        ]
    )

    results = store.similarity_search(
        "Redis cache",
        k=1,
    )

    assert len(results) == 1
    assert "Redis" in results[0].page_content


def test_retriever_returns_documents():
    store = create_test_store()

    store.add_documents(
        [
            Document(
                page_content=(
                    "LCEL connects LangChain "
                    "components."
                ),
                metadata={
                    "source": "notes.txt",
                    "source_type": "txt",
                    "chunk_index": 0,
                },
            )
        ]
    )

    retriever = KnowledgeRetriever(store)

    results = retriever.retrieve(
        "LCEL LangChain",
        k=1,
    )

    assert len(results) == 1


def test_context_builder_preserves_source():
    documents = [
        Document(
            page_content="Some useful knowledge.",
            metadata={
                "source": "report.pdf",
                "source_type": "pdf",
                "page": 7,
            },
        )
    ]

    context = build_context(documents)

    assert "report.pdf" in context
    assert "page=7" in context
    assert "Some useful knowledge" in context