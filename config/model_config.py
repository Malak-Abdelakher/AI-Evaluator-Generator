import os


OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)


GENERATOR_MODEL = os.getenv(
    "GENERATOR_MODEL",
    "llama3.1:latest",
)

GENERATOR_TEMPERATURE = float(
    os.getenv(
        "GENERATOR_TEMPERATURE",
        "0.2",
    )
)


EVALUATOR_MODEL = os.getenv(
    "EVALUATOR_MODEL",
    "llama3.1:latest",
)

EVALUATOR_TEMPERATURE = float(
    os.getenv(
        "EVALUATOR_TEMPERATURE",
        "0.0",
    )
)