from pathlib import Path

from langchain_core.documents import Document


def normalize_metadata(document: Document) -> Document:
    """
    Normalize common metadata fields while preserving
    source-specific metadata.
    """

    metadata = dict(document.metadata)

    source = metadata.get("source")

    if source is not None:
        metadata["source"] = str(source)

    if "filename" not in metadata and source:
        source_path = Path(str(source))

        if source_path.name:
            metadata["filename"] = source_path.name

    document.metadata = metadata

    return document