from pathlib import Path

from langchain_core.documents import Document

from ingestion.base.loader_registry import (
    get_file_loader,
)
from ingestion.processing.processor import (
    DocumentProcessor,
)
from knowledge.chunking.chunker import (
    DocumentChunker,
)


class IngestionPipeline:
    """
    Local-file ingestion pipeline:

    Source
        -> Loader
        -> Processor
        -> Chunker
    """

    def __init__(
        self,
        processor: DocumentProcessor | None = None,
        chunker: DocumentChunker | None = None,
    ):
        self.processor = (
            processor or DocumentProcessor()
        )

        self.chunker = (
            chunker or DocumentChunker()
        )

    def ingest_file(
        self,
        source: str | Path,
    ) -> list[Document]:

        loader = get_file_loader(source)

        documents = loader.load(source)

        processed_documents = (
            self.processor.process(documents)
        )

        chunks = self.chunker.split(
            processed_documents
        )

        return chunks