from pathlib import Path
from fastmcp import FastMCP
from fastmcp.server.providers import FileSystemProvider
from dotenv import load_dotenv


load_dotenv()


mcp = FastMCP(
    "simple-server",
    providers=[FileSystemProvider(Path(__file__).parent / "components")]
)


if __name__ == "__main__":
    mcp.run(
        transport="http", host="0.0.0.0", port=8030, stateless_http=True, json_response=True
    )
