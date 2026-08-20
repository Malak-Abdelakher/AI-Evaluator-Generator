import re

from langchain_core.documents import Document


def clean_text(text: str) -> str:
    """
    Apply safe normalization without destroying
    meaningful document structure.
    """

    text = text.replace("\x00", "")

    # Normalize Windows/macOS newlines.
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove trailing whitespace from lines.
    lines = [
        line.rstrip()
        for line in text.splitlines()
    ]

    text = "\n".join(lines)

    # Collapse excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_document(document: Document) -> Document:
    document.page_content = clean_text(
        document.page_content
    )

    return document