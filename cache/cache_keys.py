import hashlib
import json
from typing import Any


def stable_hash(value: Any) -> str:
    """
    Create a deterministic SHA-256 hash from
    JSON-serializable input.
    """

    serialized = json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        default=str,
    )

    return hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()


def retrieval_cache_key(
    query: str,
    k: int,
) -> str:

    digest = stable_hash(
        {
            "query": query,
            "k": k,
        }
    )

    return f"retrieval:{digest}"


def generator_cache_key(
    question: str,
    context: str,
    history: str,
    feedback: str,
    model: str,
) -> str:

    digest = stable_hash(
        {
            "question": question,
            "context": context,
            "history": history,
            "feedback": feedback,
            "model": model,
        }
    )

    return f"generator:{digest}"