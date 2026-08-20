from pathlib import Path
from typing import Type

from ingestion.base.base_loader import BaseKnowledgeLoader
from ingestion.loaders.code_loader import (
    CodeKnowledgeLoader,
    SUPPORTED_CODE_EXTENSIONS,
)
from ingestion.loaders.docx_loader import DOCXKnowledgeLoader
from ingestion.loaders.pdf_loader import PDFKnowledgeLoader
from ingestion.loaders.txt_loader import TXTKnowledgeLoader


FILE_LOADERS: dict[str, Type[BaseKnowledgeLoader]] = {}


def register_file_loader(
    extension: str,
    loader_class: Type[BaseKnowledgeLoader],
) -> None:
    """
    Register a loader class for a file extension.
    """

    if not extension.startswith("."):
        extension = f".{extension}"

    extension = extension.lower()

    if not issubclass(loader_class, BaseKnowledgeLoader):
        raise TypeError(
            "loader_class must inherit from BaseKnowledgeLoader."
        )

    FILE_LOADERS[extension] = loader_class


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
            f"Unsupported file type: "
            f"{extension or '[no extension]'}"
        )

    return loader_class()


# Built-in loaders
register_file_loader(".txt", TXTKnowledgeLoader)
register_file_loader(".pdf", PDFKnowledgeLoader)
register_file_loader(".docx", DOCXKnowledgeLoader)

for extension in SUPPORTED_CODE_EXTENSIONS:
    register_file_loader(
        extension,
        CodeKnowledgeLoader,
    )