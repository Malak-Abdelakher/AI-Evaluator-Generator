import pytest
from langchain_core.documents import Document

from ingestion.processing.document_validator import (
    DocumentValidationError,
    validate_document,
)
from ingestion.processing.processor import DocumentProcessor
from ingestion.processing.text_cleaner import clean_text


def test_clean_text():
    text = "Hello   \r\n\r\n\r\nWorld\x00"

    cleaned = clean_text(text)

    assert cleaned == "Hello\n\nWorld"


def test_processor_preserves_metadata():
    document = Document(
        page_content="Some content.",
        metadata={
            "source": "example.pdf",
            "source_type": "pdf",
            "page": 3,
        },
    )

    processor = DocumentProcessor()

    processed = processor.process([document])

    assert len(processed) == 1
    assert processed[0].metadata["source"] == "example.pdf"
    assert processed[0].metadata["source_type"] == "pdf"
    assert processed[0].metadata["page"] == 3
    assert processed[0].metadata["filename"] == "example.pdf"


def test_validator_rejects_empty_document():
    document = Document(
        page_content="   ",
        metadata={
            "source": "example.txt",
            "source_type": "txt",
        },
    )

    with pytest.raises(DocumentValidationError):
        validate_document(document)


def test_validator_rejects_missing_metadata():
    document = Document(
        page_content="Valid text",
        metadata={
            "source": "example.txt",
        },
    )

    with pytest.raises(DocumentValidationError):
        validate_document(document)