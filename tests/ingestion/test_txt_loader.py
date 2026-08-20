from pathlib import Path

import pytest

from ingestion.loaders.txt_loader import TXTKnowledgeLoader
from schemas.document import validate_document_metadata


FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
SAMPLE_TXT = FIXTURES_DIR / "sample.txt"


def test_txt_loader_returns_documents():
    loader = TXTKnowledgeLoader()

    documents = loader.load(SAMPLE_TXT)

    assert len(documents) > 0


def test_txt_loader_extracts_content():
    loader = TXTKnowledgeLoader()

    documents = loader.load(SAMPLE_TXT)

    content = documents[0].page_content

    assert "LangChain" in content
    assert "LCEL" in content
    assert "Redis" in content


def test_txt_loader_adds_required_metadata():
    loader = TXTKnowledgeLoader()

    documents = loader.load(SAMPLE_TXT)

    metadata = documents[0].metadata

    assert validate_document_metadata(metadata)
    assert metadata["source_type"] == "txt"
    assert metadata["filename"] == "sample.txt"


def test_txt_loader_rejects_missing_file():
    loader = TXTKnowledgeLoader()

    missing_file = FIXTURES_DIR / "does_not_exist.txt"

    with pytest.raises(FileNotFoundError):
        loader.load(missing_file)