SUPPORTED_SOURCE_TYPES = {
    "pdf",
    "docx",
    "txt",
    "code",
    "pptx",
    "web",
    "wikipedia",
    "wav",
}

EMBEDDING_MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

CHROMA_COLLECTION_NAME = "external_knowledge"

CHROMA_PERSIST_DIRECTORY = (
    "storage/vector_db/chroma"
)

DEFAULT_RETRIEVAL_K = 4

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0",
)

CACHE_DEFAULT_TTL = int(
    os.getenv(
        "CACHE_DEFAULT_TTL",
        "3600",
    )
)