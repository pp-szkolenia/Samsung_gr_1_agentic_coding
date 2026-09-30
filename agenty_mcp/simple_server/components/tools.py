from fastmcp.tools import tool
from pydantic import Field
from typing import Annotated


@tool(description="Perform operation A on two numbers and return the results")
def operation_a(
    a: Annotated[float, Field(description="The first number")],
    b: Annotated[float, Field(description="The second number")]
):
    return 2*a + 3*b


@tool(description="Concatenate two texts (a first, then b) and return the result")
def concatenate(
    a: Annotated[str, Field(description="The first text")],
    b: Annotated[str, Field(description="The second text")],
) -> str:
    return f"{a}:{b}"
