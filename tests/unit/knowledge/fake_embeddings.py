from langchain_core.embeddings import Embeddings


class FakeKeywordEmbeddings(Embeddings):
    """
    Tiny deterministic embedding model for tests.
    """

    @staticmethod
    def _embed(text: str) -> list[float]:
        text = text.lower()

        return [
            1.0,
            float(text.count("redis")),
            float(text.count("cache")),
            float(text.count("lcel")),
            float(text.count("langchain")),
            float(text.count("document")),
        ]

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        return [
            self._embed(text)
            for text in texts
        ]

    def embed_query(
        self,
        text: str,
    ) -> list[float]:

        return self._embed(text)