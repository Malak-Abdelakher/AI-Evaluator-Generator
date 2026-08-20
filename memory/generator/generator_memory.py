from memory.generator.generator_history import (
    GeneratorAttempt,
    GeneratorHistory,
)


class GeneratorMemory:
    """
    Dedicated memory store for the Generator.

    This memory is intentionally independent from
    any Evaluator memory.
    """

    def __init__(self):
        self._histories: dict[
            str,
            GeneratorHistory,
        ] = {}

    def get_history(
        self,
        conversation_id: str,
    ) -> GeneratorHistory:

        if not conversation_id.strip():
            raise ValueError(
                "conversation_id cannot be empty."
            )

        if conversation_id not in self._histories:
            self._histories[
                conversation_id
            ] = GeneratorHistory(
                conversation_id=conversation_id
            )

        return self._histories[conversation_id]

    def add_attempt(
        self,
        conversation_id: str,
        question: str,
        context: str,
        answer: str,
        feedback: str = "",
    ) -> GeneratorAttempt:

        history = self.get_history(
            conversation_id
        )

        return history.add_attempt(
            question=question,
            context=context,
            answer=answer,
            feedback=feedback,
        )

    def get_latest_attempt(
        self,
        conversation_id: str,
    ) -> GeneratorAttempt | None:

        history = self.get_history(
            conversation_id
        )

        return history.latest_attempt()

    def get_prompt_history(
        self,
        conversation_id: str,
        limit: int = 3,
    ) -> str:

        history = self.get_history(
            conversation_id
        )

        return history.format_for_prompt(
            limit=limit
        )

    def clear(
        self,
        conversation_id: str,
    ) -> None:

        self._histories.pop(
            conversation_id,
            None,
        )

    def clear_all(self) -> None:
        self._histories.clear()