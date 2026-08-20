import pytest
from langchain_core.documents import Document

from knowledge.chunking.chunker import DocumentChunker


def test_chunker_splits_long_document():
    document = Document(
        page_content="LangChain " * 300,
        metadata={
            "source": "example.txt",
            "source_type": "txt",
        },
    )

    chunker = DocumentChunker(
        chunk_size=200,
        chunk_overlap=20,
    )

    chunks = chunker.split([document])

    assert len(chunks) > 1


def test_chunker_preserves_metadata():
    document = Document(
        page_content="Artificial intelligence " * 100,
        metadata={
            "source": "report.pdf",
            "source_type": "pdf",
            "page": 7,
        },
    )

    chunker = DocumentChunker(
        chunk_size=200,
        chunk_overlap=20,
    )

    chunks = chunker.split([document])

    for chunk in chunks:
        assert chunk.metadata["source"] == "report.pdf"
        assert chunk.metadata["source_type"] == "pdf"
        assert chunk.metadata["page"] == 7
        assert "chunk_index" in chunk.metadata


def test_chunk_indices_start_at_zero():
    document = Document(
        page_content="AI systems " * 100,
        metadata={
            "source": "example.txt",
            "source_type": "txt",
        },
    )

    chunker = DocumentChunker(
        chunk_size=100,
        chunk_overlap=10,
    )

    chunks = chunker.split([document])

    assert chunks[0].metadata["chunk_index"] == 0


def test_invalid_chunk_configuration():
    with pytest.raises(ValueError):
        DocumentChunker(
            chunk_size=100,
            chunk_overlap=100,
        )