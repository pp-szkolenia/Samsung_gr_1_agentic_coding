import asyncio
import os
import json
from typing import Any
from dotenv import load_dotenv
from langfuse import Langfuse
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai import Agent, ModelRetry
from pydantic_ai.messages import ModelRequest, ModelResponse, TextPart, ToolCallPart, ToolReturnPart, UserPromptPart
from pydantic_ai.mcp import MCPError, MCPToolset

load_dotenv()

langfuse = Langfuse(
    public_key=os.environ["SIMPLE_LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["SIMPLE_LANGFUSE_SECRET_KEY"],
    base_url=os.environ["LANGFUSE_BASE_URL"],
)
# Agent.instrument_all()


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
    try:
        return await mcp_server.read_resource(uri)
    except MCPError as error:
        raise ModelRetry(str(error))


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


def as_text(value: Any) -> str:
    """MCP passes prompt arguments as strings; objects and lists go as JSON."""
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, default=str)

@agent.tool_plain
async def get_prompt(name: str, arguments: dict[str, Any]) -> str:
    """Get the instructions of an MCP prompt by its name, filled with the given arguments.

    Pass exactly the argument names that list_prompts reports for this prompt, all of the required ones.
    """
    try:
        result = await mcp_server.get_prompt(name, {key: as_text(value) for key, value in
                                                    arguments.items()})
    except MCPError as error:
        raise ModelRetry(str(error))
    return "\n\n".join(message.content.content for message in result.messages)


def print_agent_trace(result, max_length: int = 200) -> None:
    print("-" * 60)
    for message in result.new_messages():
        for part in message.parts:
            if isinstance(message, ModelRequest) and isinstance(part, UserPromptPart):
                print(f"[user] {part.content}")
            elif isinstance(part, ToolCallPart):
                print(f"[tool call] {part.tool_name}({part.args})")
            elif isinstance(part, ToolReturnPart):
                content = " ".join(str(part.content).split())
                print(f"[tool return] {part.tool_name} -> {content[:max_length]}")
            elif isinstance(message, ModelResponse) and isinstance(part, TextPart):
                print(f"[model] {part.content[:max_length]}")
    print(f"[usage] {result.usage}")
    print("-" * 60)


async def main() -> None:
    async with agent:
        result = await agent.run(
            "Wykonaj operację konkatencacji naa parze stringów o indeksie 2. Nie korzystaj z promptów dostepnych przez MCP"
        )
    print(result.output)

async def chat() -> None:
    history = []
    async with agent:
        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if user_input.lower() in ("exit", "quit", "q"):
                break
            if not user_input:
                continue

            result = await agent.run(user_input, message_history=history)
            history = result.all_messages()
            print_agent_trace(result)
            print(f"Agent: {result.output}\n")

    langfuse.flush()

if __name__ == "__main__":
    asyncio.run(chat())
