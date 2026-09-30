import asyncio
import os

from dotenv import load_dotenv
from langfuse import Langfuse
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv()

langfuse = Langfuse(
    public_key=os.environ["SIMPLE_LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["SIMPLE_LANGFUSE_SECRET_KEY"],
    base_url=os.environ["LANGFUSE_BASE_URL"],
)

model = OpenAIChatModel(
    os.environ["LLM_MODEL"],
    provider=OpenAIProvider(base_url=os.environ["LLM_BASE_URL"], api_key=os.environ["LLM_API_KEY"]),
)

"""
Jesteś pomocnym asystentem z dostępem do narzędzi, zasobów i promptów MCP.
Korzystaj z nich, aby dokładnie odpowiadać na pytania. Przed wykonaniem jakiejkolwiek operacji sprawdź, czy istnieje
prompt MCP opisujący, jak ją wykonać, i postępuj zgodnie z jego instrukcjami.
Pobierając prompt MCP, podawaj dokładnie te nazwy argumentów, które zwraca lista promptów — nie zmyślaj ich i nie zmieniaj.
Bardzo ważne: w odpowiedzi podaj WYŁĄCZNIE wynik, bez żadnych wyjaśnień ani dodatkowego tekstu.
"""

mcp_server = MCPToolset(os.environ["SIMPLE_MCP_URL"])

agent = Agent(
    model,
    instructions=langfuse.get_prompt("simple-agent-system", label="production").compile(),
    toolsets=[mcp_server],
)


@agent.tool_plain
async def list_resources() -> list[dict]:
    """List MCP resources: data sets available on the server."""
    resources = await mcp_server.list_resources()
    return [{"uri": r.uri, "name": r.name, "description": r.description}
            for r in resources]


@agent.tool_plain
async def read_resource(uri: str) -> str:
    """Read the content of an MCP resource by its URI."""
    return await mcp_server.read_resource(uri)


@agent.tool_plain
async def list_prompts() -> list[dict]:
    """List MCP prompts: instructions describing how to perform operations, with the arguments each of them takes.

    Check them before performing any operation.
    """
    prompts = await mcp_server.list_prompts()
    return [
        {
            "name": p.name,
            "description": p.description,
            "arguments": [
                {"name": a.name, "description": a.description, "required": a.required} for a in p.arguments or []
            ],
        }
        for p in prompts
    ]


@agent.tool_plain
async def get_prompt(name: str, arguments: dict[str, str]) -> str:
    """Get the instructions of an MCP prompt by its name, filled with the given arguments.

    Pass exactly the argument names that list_prompts reports for this prompt, all of the required ones.
    """
    result = await mcp_server.get_prompt(name, arguments)
    return "\n\n".join(message.content.content for message in result.messages)



async def main() -> None:
    async with agent:
        result = await agent.run("Wykonaj operację A na parze liczb o indeksie 1 (z danych liczbowych)")
    print(result.output)


if __name__ == "__main__":
    asyncio.run(main())
