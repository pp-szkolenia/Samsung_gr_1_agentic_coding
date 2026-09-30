from fastmcp.tools import tool
from pydantic import Field
from typing import Annotated


@tool(description="Perform operation A on two numbers and return the results")
def operation_a(
    a: Annotated[float, Field(description="The first number")],
    b: Annotated[float, Field(description="The second number")]
):
    return 2*a + 3*b
