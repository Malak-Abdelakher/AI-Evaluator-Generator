from pathlib import Path

from ingestion.base.base_loader import BaseKnowledgeLoader
from ingestion.loaders.code_loader import (
    CodeKnowledgeLoader,
    SUPPORTED_CODE_EXTENSIONS,
)
from ingestion.loaders.docx_loader import DOCXKnowledgeLoader
from ingestion.loaders.pdf_loader import PDFKnowledgeLoader
from ingestion.loaders.txt_loader import TXTKnowledgeLoader


FILE_LOADERS = {
    ".txt": TXTKnowledgeLoader,
    ".pdf": PDFKnowledgeLoader,
    ".docx": DOCXKnowledgeLoader,
}

for extension in SUPPORTED_CODE_EXTENSIONS:
    FILE_LOADERS[extension] = CodeKnowledgeLoader


def get_file_loader(
    source: str | Path,
) -> BaseKnowledgeLoader:
    """
    Resolve the appropriate loader for a local file.
    """
    path = Path(source)

    extension = path.suffix.lower()

    loader_class = FILE_LOADERS.get(extension)

    if loader_class is None:
        raise ValueError(
            f"Unsupported file type: {extension or '[no extension]'}"
        )

    return loader_class()