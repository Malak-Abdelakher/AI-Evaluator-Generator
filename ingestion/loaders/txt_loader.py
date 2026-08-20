from pathlib import Path

from langchain_core.documents import Document

from ingestion.base.base_loader import BaseKnowledgeLoader


class TXTKnowledgeLoader(BaseKnowledgeLoader):
    """
    Loader for plain-text (.txt) knowledge sources.
    """

    def load(self, source: str | Path) -> list[Document]:
        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(f"TXT file not found: {path}")

        if not path.is_file():
            raise ValueError(f"TXT source is not a file: {path}")

        if path.suffix.lower() != ".txt":
            raise ValueError(
                f"TXTKnowledgeLoader only accepts .txt files: {path}"
            )

        content = path.read_text(encoding="utf-8")

        document = Document(
            page_content=content,
            metadata={
                "source": str(path),
                "source_type": "txt",
                "filename": path.name,
            },
        )

        return [document]