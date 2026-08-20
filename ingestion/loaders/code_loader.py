from pathlib import Path

from langchain_core.documents import Document

from ingestion.base.base_loader import BaseKnowledgeLoader


SUPPORTED_CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".cs",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".html",
    ".css",
    ".json",
    ".xml",
    ".sql",
    ".sh",
    ".ps1",
    ".yaml",
    ".yml",
}


class CodeKnowledgeLoader(BaseKnowledgeLoader):
    """Loader for text-based source-code files."""

    def load(self, source: str | Path) -> list[Document]:
        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(f"Code file not found: {path}")

        if not path.is_file():
            raise ValueError(f"Code source is not a file: {path}")

        extension = path.suffix.lower()

        if extension not in SUPPORTED_CODE_EXTENSIONS:
            raise ValueError(
                f"Unsupported source-code extension: {extension}"
            )

        content = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        return [
            Document(
                page_content=content,
                metadata={
                    "source": str(path),
                    "source_type": "code",
                    "filename": path.name,
                    "extension": extension,
                },
            )
        ]