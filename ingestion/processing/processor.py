from langchain_core.documents import Document

from ingestion.processing.document_validator import validate_document
from ingestion.processing.metadata_normalizer import normalize_metadata
from ingestion.processing.text_cleaner import clean_document


class DocumentProcessor:
    """
    Shared processing stage used by every knowledge source.
    """

    def process(
        self,
        documents: list[Document],
    ) -> list[Document]:

        processed_documents = []

        for document in documents:
            document = normalize_metadata(document)
            document = clean_document(document)

            validate_document(document)

            processed_documents.append(document)

        return processed_documents