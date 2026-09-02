"""Pretrained sentence-transformer text encoder (frozen)."""

from __future__ import annotations

import torch
import torch.nn as nn


class PretrainedTextEncoder(nn.Module):
  """
  Wraps a frozen sentence-transformers model to produce fixed-dim text embeddings.
  Only the projection head is trainable.
  """

  def __init__(self, out_dim: int = 256, model_name: str = "all-MiniLM-L6-v2"):
    super().__init__()
    from sentence_transformers import SentenceTransformer

    self.st_model = SentenceTransformer(model_name)
    for p in self.st_model.parameters():
      p.requires_grad = False

    st_dim = self.st_model.get_sentence_embedding_dimension()
    self.proj = nn.Sequential(
      nn.Linear(st_dim, out_dim),
      nn.GELU(),
      nn.Linear(out_dim, out_dim),
    )
    self.max_len = 128  # kept for config compat

  def forward(self, captions: list[str]) -> torch.Tensor:
    device = next(self.proj.parameters()).device
    with torch.no_grad():
      raw = self.st_model.encode(
        captions, convert_to_tensor=True, show_progress_bar=False,
        device=device,
      )
    return self.proj(raw.to(device).float())

  def encode_batch(self, captions: list[str], device: torch.device) -> torch.Tensor:
    emb = self.forward(captions)
    return emb.to(device)
