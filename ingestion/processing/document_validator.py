from langchain_core.documents import Document

from schemas.document import validate_document_metadata


class DocumentValidationError(ValueError):
    """Raised when an ingested document is invalid."""


def validate_document(document: Document) -> None:
    """
    Validate a document before it enters the
    knowledge/chunking pipeline.
    """

    if not isinstance(document, Document):
        raise DocumentValidationError(
            "Expected a LangChain Document."
        )

    if not document.page_content:
        raise DocumentValidationError(
            "Document contains no content."
        )

    if not document.page_content.strip():
        raise DocumentValidationError(
            "Document contains only whitespace."
        )

    if not validate_document_metadata(document.metadata):
        raise DocumentValidationError(
            "Document is missing required metadata."
        )