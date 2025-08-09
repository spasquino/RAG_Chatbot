"""
Text preprocessing utils.
- `normalize_text(text)` operates purely on a string (no file I/O).
- `normalize_file(file_path)` reads a file then applies `normalize_text`.
"""
import re
import unicodedata
from pathlib import Path

# Compile expensive patterns once
_TS_RANGE = re.compile(r"\b\d{2}:\d{2}:\d{2}:\d{2}\s*-\s*\d{2}:\d{2}:\d{2}:\d{2}\b")
_MULTI_WS = re.compile(r"\s+")

def normalize_text(text: str) -> str:
    """Clean a raw text string.
    Steps:
      - Replace Unicode replacement char
      - Remove specific tokens (e.g., 'Unbekannt')
      - Strip time-range stamps like HH:MM:SS:FF - HH:MM:SS:FF
      - Unicode normalize (NFKC)
      - Collapse whitespace
    """
    if text is None:
        return ""

    # Replace replacement character and known noise tokens
    text = text.replace("\ufffd", " ")
    text = text.replace("Unbekannt", " ")

    # Remove time-range patterns
    text = _TS_RANGE.sub(" ", text)

    # Unicode normalize
    text = unicodedata.normalize("NFKC", text)

    # Collapse whitespace
    text = _MULTI_WS.sub(" ", text).strip()
    return text

def normalize_file(file_path: str) -> str:
    """Read a file and return its normalized content."""
    p = Path(file_path)
    raw = p.read_text(encoding="utf-8", errors="replace")
    return normalize_text(raw)
