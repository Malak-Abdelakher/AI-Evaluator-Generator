from abc import ABC, abstractmethod
from pathlib import Path

from langchain_core.documents import Document


class BaseKnowledgeLoader(ABC):
    """
    Base contract for every external-knowledge loader.

    Every loader must convert its source into a list
    of LangChain Document objects.
    """

    @abstractmethod
    def load(self, source: str | Path) -> list[Document]:
        """
        Load a knowledge source.

        Args:
            source:
                File path, URL, or other source identifier.

        Returns:
            A list of LangChain Document objects.
        """
        raise NotImplementedError