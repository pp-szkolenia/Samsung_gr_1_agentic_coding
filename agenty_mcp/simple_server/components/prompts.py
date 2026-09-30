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


def operation_a_on_nth_numbers_pair(
    index: Annotated[int, Field(description="Index of the numbers pair in the numerical data")]
):
    langfuse_prompt = langfuse.get_prompt("operation-a-prompt")
    return [Message(langfuse_prompt.compile(index=index))]
