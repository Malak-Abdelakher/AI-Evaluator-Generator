from typing import Any


REQUIRED_METADATA_FIELDS = {
    "source",
    "source_type",
}


def validate_document_metadata(metadata: dict[str, Any]) -> bool:
    """
    Validate the minimum metadata required
    for every document in the knowledge pipeline.
    """
    return REQUIRED_METADATA_FIELDS.issubset(metadata.keys())