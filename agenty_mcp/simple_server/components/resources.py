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
