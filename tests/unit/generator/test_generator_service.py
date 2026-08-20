from langchain_core.runnables import RunnableLambda

from agents.generator.generator_service import GeneratorService
from memory.generator.generator_memory import GeneratorMemory


def test_generator_service_stores_answer_in_memory():
    fake_chain = RunnableLambda(
        lambda inputs: "Generated grounded answer."
    )

    memory = GeneratorMemory()

    generator = GeneratorService(
        chain=fake_chain,
        memory=memory,
    )

    generator.generate(
        question="What is Redis?",
        context="Redis can be used for caching.",
        conversation_id="test-conversation",
    )

    latest = memory.get_latest_attempt(
        "test-conversation"
    )

    assert latest is not None
    assert latest.answer == "Generated grounded answer."
    assert latest.attempt_number == 1


def test_generator_stores_improvement_attempt():
    responses = iter(
        [
            "Initial answer.",
            "Improved answer.",
        ]
    )

    fake_chain = RunnableLambda(
        lambda inputs: next(responses)
    )

    memory = GeneratorMemory()

    generator = GeneratorService(
        chain=fake_chain,
        memory=memory,
    )

    conversation_id = "improvement-test"

    generator.generate(
        question="Explain Redis.",
        context="Redis can be used for caching.",
        conversation_id=conversation_id,
    )

    generator.generate(
        question="Explain Redis.",
        context="Redis can be used for caching.",
        feedback="Mention its use as a caching layer.",
        conversation_id=conversation_id,
    )

    history = memory.get_history(
        conversation_id
    )

    assert len(history.attempts) == 2

    assert history.attempts[0].answer == "Initial answer."

    assert history.attempts[1].answer == "Improved answer."

    assert (
        history.attempts[1].feedback
        == "Mention its use as a caching layer."
    )
