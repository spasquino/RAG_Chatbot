import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
WEAVIATE_EMBEDDED = os.getenv("WEAVIATE_EMBEDDED", "1") == "1"
