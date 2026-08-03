import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://bot:botpass@localhost:5432/jobdb"
)

DATA_DIR = Path(os.getenv("DATA_DIR", str(PROJECT_ROOT / "data")))
INPUT_DIR = Path(os.getenv("INPUT_DIR", str(DATA_DIR / "input")))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", str(DATA_DIR / "output")))

INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
