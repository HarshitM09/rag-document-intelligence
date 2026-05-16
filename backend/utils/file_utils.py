import os
from pathlib import Path
from typing import List


def list_text_files(root_path: str) -> List[str]:
    """Traverse repository folders and collect supported text document paths."""
    path = Path(root_path)
    if not path.exists():
        return []

    sources = []
    for candidate in path.rglob("*.md"):
        sources.append(str(candidate.resolve()))
    for candidate in path.rglob("*.txt"):
        sources.append(str(candidate.resolve()))
    return sources


def read_document(path: str) -> str:
    """Read document content with fallback encoding for enterprise source files."""
    with open(path, "r", encoding="utf-8", errors="ignore") as file_handle:
        return file_handle.read()


def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """Split content into overlapping chunks suitable for embedding.

    This helps maintain semantic continuity for vector search and inference.
    """
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be larger than overlap")

    tokens = text.split()
    segments = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        segment = " ".join(tokens[start:end])
        segments.append(segment)
        if end == len(tokens):
            break
        start += chunk_size - overlap
    return segments
