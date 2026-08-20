# Project 3 — Evaluator/Generator RAG System

A retrieval-augmented generation system with a generator/evaluator feedback loop,
document ingestion pipeline, caching layer, and a workflow orchestration layer.

## Structure
See the project directory tree for module layout: ingestion, knowledge (chunking/embeddings/vectorstore/retrieval),
llms, agents (generator/evaluator), memory, cache, workflow, chains, services, ui, api.

## Setup
1. Copy `.env.example` to `.env` and fill in API keys.
2. `pip install -r requirements.txt`
3. `python scripts/start_redis.py`
4. `python app.py`

## Testing
`pytest tests/`
