from memory.generator.generator_memory import (
    GeneratorMemory,
)


def test_generator_memory_stores_attempt():
    memory = GeneratorMemory()

    attempt = memory.add_attempt(
        conversation_id="conversation-1",
        question="What is Redis?",
        context="Redis can be used for caching.",
        answer="Redis can be used for caching.",
    )

    assert attempt.attempt_number == 1
    assert attempt.question == "What is Redis?"
    assert (
        attempt.answer
        == "Redis can be used for caching."
    )


def test_attempt_numbers_increment():
    memory = GeneratorMemory()

    memory.add_attempt(
        conversation_id="conversation-1",
        question="Question",
        context="Context",
        answer="Answer 1",
    )

    second = memory.add_attempt(
        conversation_id="conversation-1",
        question="Question",
        context="Context",
        answer="Answer 2",
        feedback="Improve completeness.",
    )

    assert second.attempt_number == 2


def test_conversations_are_isolated():
    memory = GeneratorMemory()

    memory.add_attempt(
        conversation_id="conversation-A",
        question="Question A",
        context="Context A",
        answer="Answer A",
    )

    memory.add_attempt(
        conversation_id="conversation-B",
        question="Question B",
        context="Context B",
        answer="Answer B",
    )

    history_a = memory.get_history(
        "conversation-A"
    )

    history_b = memory.get_history(
        "conversation-B"
    )

    assert len(history_a.attempts) == 1
    assert len(history_b.attempts) == 1

    assert (
        history_a.attempts[0].answer
        == "Answer A"
    )

    assert (
        history_b.attempts[0].answer
        == "Answer B"
    )


def test_memory_preserves_feedback():
    memory = GeneratorMemory()

    attempt = memory.add_attempt(
        conversation_id="conversation-1",
        question="What is LCEL?",
        context="LCEL connects runnables.",
        answer="LCEL connects things.",
        feedback=(
            "Be more precise about runnables."
        ),
    )

    assert (
        attempt.feedback
        == "Be more precise about runnables."
    )


def test_prompt_history_contains_previous_answer():
    memory = GeneratorMemory()

    memory.add_attempt(
        conversation_id="conversation-1",
        question="What is Redis?",
        context="Redis is used for caching.",
        answer="Redis is used for caching.",
    )

    history = memory.get_prompt_history(
        "conversation-1"
    )

    assert "Attempt 1" in history
    assert "Redis is used for caching." in history


def test_clear_conversation():
    memory = GeneratorMemory()

    memory.add_attempt(
        conversation_id="conversation-1",
        question="Question",
        context="Context",
        answer="Answer",
    )

    memory.clear("conversation-1")

    history = memory.get_history(
        "conversation-1"
    )

    assert len(history.attempts) == 0