from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class GeneratorAttempt:
    """
    Represents one answer-generation attempt.
    """

    attempt_number: int
    question: str
    context: str
    answer: str
    feedback: str = ""
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class GeneratorHistory:
    """
    Stores Generator attempts for one conversation.
    """

    conversation_id: str
    attempts: list[GeneratorAttempt] = field(
        default_factory=list
    )

    def add_attempt(
        self,
        question: str,
        context: str,
        answer: str,
        feedback: str = "",
    ) -> GeneratorAttempt:

        attempt = GeneratorAttempt(
            attempt_number=len(self.attempts) + 1,
            question=question,
            context=context,
            answer=answer,
            feedback=feedback,
        )

        self.attempts.append(attempt)

        return attempt

    def latest_attempt(
        self,
    ) -> GeneratorAttempt | None:

        if not self.attempts:
            return None

        return self.attempts[-1]

    def get_recent_attempts(
        self,
        limit: int = 3,
    ) -> list[GeneratorAttempt]:

        if limit <= 0:
            return []

        return self.attempts[-limit:]

    def format_for_prompt(
        self,
        limit: int = 3,
    ) -> str:
        """
        Build a concise representation of recent Generator
        history that can be supplied to the LLM.
        """

        recent = self.get_recent_attempts(limit)

        if not recent:
            return "No previous Generator attempts."

        parts = []

        for attempt in recent:
            item = [
                f"Attempt {attempt.attempt_number}",
                f"Question: {attempt.question}",
                f"Previous answer: {attempt.answer}",
            ]

            if attempt.feedback:
                item.append(
                    f"Evaluator feedback used: {attempt.feedback}"
                )

            parts.append("\n".join(item))

        return "\n\n".join(parts)