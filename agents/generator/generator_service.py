from langchain_core.runnables import Runnable

from cache.generator_cache import GeneratorCache
from chains.generator_chain import build_generator_chain
from config.model_config import GENERATOR_MODEL
from memory.generator.generator_memory import (
    GeneratorMemory,
)


class GeneratorService:
    """
    Grounded answer generation with dedicated
    memory and optional Redis caching.
    """

    def __init__(
        self,
        chain: Runnable | None = None,
        memory: GeneratorMemory | None = None,
        cache: GeneratorCache | None = None,
    ):
        self.chain = (
            chain or build_generator_chain()
        )

        self.memory = (
            memory or GeneratorMemory()
        )

        self.cache = cache

    def generate(
        self,
        question: str,
        context: str,
        feedback: str = "",
        conversation_id: str = "default",
    ) -> str:

        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        history = (
            self.memory.get_prompt_history(
                conversation_id,
                limit=3,
            )
        )

        answer = None

        if self.cache is not None:
            answer = self.cache.get(
                question=question,
                context=context,
                history=history,
                feedback=feedback,
                model=GENERATOR_MODEL,
            )

        if answer is None:
            result = self.chain.invoke(
                {
                    "question": question,
                    "context": context,
                    "history": history,
                    "feedback": feedback,
                }
            )

            answer = str(result).strip()

            if self.cache is not None:
                self.cache.set(
                    question=question,
                    context=context,
                    history=history,
                    feedback=feedback,
                    model=GENERATOR_MODEL,
                    answer=answer,
                )

        self.memory.add_attempt(
            conversation_id=conversation_id,
            question=question,
            context=context,
            answer=answer,
            feedback=feedback,
        )

        return answer