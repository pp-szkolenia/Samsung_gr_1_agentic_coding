import os
from typing import Annotated
from fastmcp.prompts import prompt, Message
from langfuse import Langfuse
from pydantic import Field


langfuse = Langfuse(
    public_key=os.getenv("SIMPLE_LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("SIMPLE_LANGFUSE_SECRET_KEY"),
    base_url=os.getenv("LANGFUSE_BASE_URL"),
)


@prompt(
    name="operation-a-on-nth-numbers-pair",
    description="Explains how to perform operation A on the n-th pair of numbers"
)
def operation_a_on_nth_numbers_pair(
    index: Annotated[int, Field(description="Index of the numbers pair in the numerical data")]
):
    langfuse_prompt = langfuse.get_prompt("operation-a-prompt")
    # return [Message("test")]
    return [Message(langfuse_prompt.compile(index=index))]


@prompt(
    name="concatenate-nth-texts-pair",
    description="Explains how to concatenate the n-th pair of texts from the text data",
)
def concatenate_nth_texts_pair(
    index: Annotated[int, Field(description="Index of the texts pair in the text data")],
) -> list[Message]:
    langfuse_prompt = langfuse.get_prompt("concatenate-nth-texts-pair", label="production")
    return [Message(langfuse_prompt.compile(index=index))]
