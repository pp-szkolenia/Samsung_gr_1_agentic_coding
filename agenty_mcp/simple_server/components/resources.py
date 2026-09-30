from pathlib import Path
from fastmcp.resources import resource


DATA_DIR = Path(__file__).parent.parent / "data"


@resource(
    "data://numbers",
    name="Numerical data",
    description="Pairs of numbers (a, b) used as input data",
    mime_type="application/json"
)
def numbers_data():
    return (DATA_DIR / "numbers.json").read_text(encoding="utf-8")


@resource(
    "data://strings",
    name="Text data",
    description="Pairs of texts (a, b) used as input data",
    mime_type="application/json",
)
def strings_data() -> str:
    return (DATA_DIR / "strings.json").read_text(encoding="utf-8")
