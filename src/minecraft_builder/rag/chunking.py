"""Split book text into overlapping chunks for retrieval."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Chunk:
  text: str
  source: str
  page: int | None = None
  index: int = 0


def chunk_text(
  text: str,
  source: str,
  chunk_size: int = 500,
  overlap: int = 80,
  page: int | None = None,
) -> list[Chunk]:
  """Split text into overlapping word-based chunks."""
  text = _normalize(text)
  if not text:
    return []

  words = text.split()
  if len(words) <= chunk_size:
    return [Chunk(text=text, source=source, page=page, index=0)]

  chunks: list[Chunk] = []
  start = 0
  idx = 0
  while start < len(words):
    end = min(start + chunk_size, len(words))
    chunk_words = words[start:end]
    chunks.append(
      Chunk(
        text=" ".join(chunk_words),
        source=source,
        page=page,
        index=idx,
      )
    )
    if end >= len(words):
      break
    start += chunk_size - overlap
    idx += 1
  return chunks


def _normalize(text: str) -> str:
  text = text.replace("\r\n", "\n")
  text = re.sub(r"[ \t]+", " ", text)
  text = re.sub(r"\n{3,}", "\n\n", text)
  return text.strip()
