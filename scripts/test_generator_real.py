from agents.generator.generator_service import GeneratorService
from knowledge.knowledge_pipeline import KnowledgePipeline
from services.qa_service import QAService
from cache.generator_cache import GeneratorCache

def main():
    print("Initializing knowledge system...")

    knowledge = KnowledgePipeline.create_default()

    print("Ingesting knowledge...")

    knowledge.ingest_file(
        "tests/fixtures/sample.txt"
    )

    generator = GeneratorService(
        cache=GeneratorCache()
    )

    qa = QAService(
        knowledge=knowledge,
        generator=generator,
    )

    question = "Who is the president of France?"

    print("\nQUESTION:")
    print(question)

    answer = qa.answer(
        question,
        k=2,
    )

    print("\nANSWER:")
    print(answer)


if __name__ == "__main__":
    main()