"""Load the Minecraft Guide to Creative from PDF or text files."""

from __future__ import annotations

from pathlib import Path

from .chunking import Chunk, chunk_text


def load_document(path: Path, chunk_size: int = 500, overlap: int = 80) -> list[Chunk]:
  """Load a single file and return chunks."""
  suffix = path.suffix.lower()
  if suffix == ".pdf":
    return _load_pdf(path, chunk_size, overlap)
  if suffix in {".txt", ".md", ".markdown"}:
    return _load_text(path, chunk_size, overlap)
  raise ValueError(f"Unsupported file type: {suffix}. Use .pdf, .txt, or .md")


def load_directory(
  directory: Path,
  chunk_size: int = 500,
  overlap: int = 80,
) -> list[Chunk]:
  """Load all supported documents from a directory."""
  chunks: list[Chunk] = []
  patterns = ("*.pdf", "*.txt", "*.md", "*.markdown")
  files: list[Path] = []
  for pattern in patterns:
    files.extend(sorted(directory.glob(pattern)))

  if not files:
    raise FileNotFoundError(f"No .pdf/.txt/.md files found in {directory}")

  for path in files:
    chunks.extend(load_document(path, chunk_size, overlap))
  return chunks


def _load_text(path: Path, chunk_size: int, overlap: int) -> list[Chunk]:
  text = path.read_text(encoding="utf-8", errors="replace")
  return chunk_text(text, source=path.name, chunk_size=chunk_size, overlap=overlap)


def _load_pdf(path: Path, chunk_size: int, overlap: int) -> list[Chunk]:
  try:
    from pypdf import PdfReader
  except ImportError as exc:
    raise ImportError("Install pypdf to ingest PDF books: pip install pypdf") from exc

  reader = PdfReader(str(path))
  all_chunks: list[Chunk] = []
  for page_num, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ""
    page_chunks = chunk_text(
      text,
      source=path.name,
      chunk_size=chunk_size,
      overlap=overlap,
      page=page_num,
    )
    all_chunks.extend(page_chunks)
  return all_chunks
