from langchain_core.documents import Document

from schemas.document import validate_document_metadata


def test_valid_document_metadata():
    document = Document(
        page_content="This is some knowledge.",
        metadata={
            "source": "example.txt",
            "source_type": "txt",
        },
    )

    assert validate_document_metadata(document.metadata)


def test_invalid_document_metadata():
    document = Document(
        page_content="This document has incomplete metadata.",
        metadata={
            "source": "example.txt",
        },
    )

    assert not validate_document_metadata(document.metadata)