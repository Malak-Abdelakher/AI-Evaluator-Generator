from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

from chains.generator_chain import build_generator_chain


def test_generator_chain_returns_string():
    """
    Test the Generator LCEL chain without calling Ollama.
    """

    fake_llm = RunnableLambda(
        lambda prompt: AIMessage(
            content="Redis can be used for caching."
        )
    )

    chain = build_generator_chain(
        llm=fake_llm
    )

    result = chain.invoke(
        {
            "question": "What can Redis be used for?",
            "context": (
                "Redis can be used as a caching layer."
            ),
            "history": (
                "No previous Generator attempts."
            ),
            "feedback": "",
        }
    )

    assert isinstance(result, str)
    assert "caching" in result