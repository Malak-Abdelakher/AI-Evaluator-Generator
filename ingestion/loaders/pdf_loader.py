from pathlib import Path

import pymupdf
from langchain_core.documents import Document

from ingestion.base.base_loader import BaseKnowledgeLoader


class PDFKnowledgeLoader(BaseKnowledgeLoader):
    """Loader for PDF knowledge sources."""

    def load(self, source: str | Path) -> list[Document]:
        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {path}")

        if not path.is_file():
            raise ValueError(f"PDF source is not a file: {path}")

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                f"PDFKnowledgeLoader only accepts .pdf files: {path}"
            )

        documents = []

        pdf = pymupdf.open(path)

        try:
            for page_index, page in enumerate(pdf):
                text = page.get_text("text").strip()

                if not text:
                    continue

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": str(path),
                            "source_type": "pdf",
                            "filename": path.name,
                            "page": page_index + 1,
                        },
                    )
                )
        finally:
            pdf.close()

        return documents