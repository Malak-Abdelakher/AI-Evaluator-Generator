from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

from llms.generator_llm import create_generator_llm
from prompts.generator_prompt import GENERATOR_PROMPT


def build_generator_chain(
    llm: Runnable | None = None,
) -> Runnable:
    """
    Build the Generator using LCEL.
    """

    model = llm or create_generator_llm()

    return (
        GENERATOR_PROMPT
        | model
        | StrOutputParser()
    )