from langchain_ollama import ChatOllama

import config.settings  # noqa: F401

from config.model_config import (
    GENERATOR_MODEL,
    GENERATOR_TEMPERATURE,
    OLLAMA_BASE_URL,
)


def create_generator_llm() -> ChatOllama:
    """
    Create the local Ollama model used by
    the Generator agent.
    """

    return ChatOllama(
        model=GENERATOR_MODEL,
        temperature=GENERATOR_TEMPERATURE,
        base_url=OLLAMA_BASE_URL,
    )