from agents.generator.generator_service import (
    GeneratorService,
)
from knowledge.knowledge_pipeline import (
    KnowledgePipeline,
)


class QAService:
    """
    Coordinates knowledge retrieval and generation.
    The Evaluator will be added in the next stage.
    """

    def __init__(
        self,
        knowledge: KnowledgePipeline,
        generator: GeneratorService,
    ):
        self.knowledge = knowledge
        self.generator = generator

    def answer(
        self,
        question: str,
        k: int = 4,
        conversation_id: str = "default",
    ) -> str:

        context = self.knowledge.retrieve_context(
            query=question,
            k=k,
        )

        return self.generator.generate(
            question=question,
            context=context,
            conversation_id=conversation_id,
        )