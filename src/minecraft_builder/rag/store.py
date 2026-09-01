"""Local TF-IDF vector store for private book RAG."""

from __future__ import annotations

import json
import pickle
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .chunking import Chunk


@dataclass
class SearchResult:
  chunk: Chunk
  score: float


class GuideIndex:
  """Simple offline retrieval index — no API calls, no cloud."""

  def __init__(self):
    self.chunks: list[Chunk] = []
    self._vectorizer = None
    self._matrix = None

  def build(self, chunks: list[Chunk]) -> None:
    from sklearn.feature_extraction.text import TfidfVectorizer

    if not chunks:
      raise ValueError("No chunks to index")

    self.chunks = chunks
    texts = [c.text for c in chunks]
    self._vectorizer = TfidfVectorizer(
      stop_words="english",
      ngram_range=(1, 2),
      max_features=20000,
    )
    self._matrix = self._vectorizer.fit_transform(texts)

  def search(self, query: str, top_k: int = 4) -> list[SearchResult]:
    if self._vectorizer is None or self._matrix is None:
      raise RuntimeError("Index not built. Run ingest_guide first.")

    query_vec = self._vectorizer.transform([query])
    scores = (self._matrix @ query_vec.T).toarray().ravel()
    top_indices = np.argsort(scores)[::-1][:top_k]

    results: list[SearchResult] = []
    for idx in top_indices:
      score = float(scores[idx])
      if score <= 0:
        continue
      results.append(SearchResult(chunk=self.chunks[int(idx)], score=score))
    return results

  def save(self, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    payload = {
      "chunks": [
        {
          "text": c.text,
          "source": c.source,
          "page": c.page,
          "index": c.index,
        }
        for c in self.chunks
      ],
    }
    (directory / "chunks.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    with open(directory / "index.pkl", "wb") as f:
      pickle.dump({"vectorizer": self._vectorizer, "matrix": self._matrix}, f)

  @classmethod
  def load(cls, directory: Path) -> GuideIndex:
    chunks_path = directory / "chunks.json"
    index_path = directory / "index.pkl"
    if not chunks_path.exists() or not index_path.exists():
      raise FileNotFoundError(
        f"RAG index not found in {directory}. Run: python -m minecraft_builder.scripts.ingest_guide"
      )

    payload = json.loads(chunks_path.read_text(encoding="utf-8"))
    chunks = [
      Chunk(text=c["text"], source=c["source"], page=c.get("page"), index=c.get("index", 0))
      for c in payload["chunks"]
    ]

    with open(index_path, "rb") as f:
      data = pickle.load(f)

    store = cls()
    store.chunks = chunks
    store._vectorizer = data["vectorizer"]
    store._matrix = data["matrix"]
    return store
