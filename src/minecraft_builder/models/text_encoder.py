"""Character-level text encoder trained from scratch (no pretrained CLIP)."""

from __future__ import annotations

import torch
import torch.nn as nn


PAD_IDX = 0
UNK_IDX = 1


def tokenize(text: str, max_len: int, vocab_size: int = 128) -> torch.Tensor:
  """Encode ASCII text to token indices. Chars 32-126 map to 2..96."""
  tokens = [PAD_IDX] * max_len
  for i, ch in enumerate(text[: max_len - 1]):
    code = ord(ch)
    if 32 <= code <= 126:
      tokens[i] = min(code - 30, vocab_size - 1)
    else:
      tokens[i] = UNK_IDX
  return torch.tensor(tokens, dtype=torch.long)


class TextEncoder(nn.Module):
  """
  Small transformer encoder for text prompts.
  Trained jointly with the diffusion model via classifier-free guidance.
  """

  def __init__(
    self,
    vocab_size: int = 128,
    max_len: int = 128,
    embed_dim: int = 128,
    out_dim: int = 256,
    num_heads: int = 4,
    num_layers: int = 3,
  ):
    super().__init__()
    self.max_len = max_len
    self.token_embed = nn.Embedding(vocab_size, embed_dim, padding_idx=PAD_IDX)
    self.pos_embed = nn.Parameter(torch.randn(1, max_len, embed_dim) * 0.02)

    encoder_layer = nn.TransformerEncoderLayer(
      d_model=embed_dim,
      nhead=num_heads,
      dim_feedforward=embed_dim * 4,
      batch_first=True,
      activation="gelu",
    )
    self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
    self.proj = nn.Sequential(
      nn.LayerNorm(embed_dim),
      nn.Linear(embed_dim, out_dim),
      nn.GELU(),
      nn.Linear(out_dim, out_dim),
    )

  def forward(self, tokens: torch.Tensor) -> torch.Tensor:
    """
    Args:
      tokens: (B, L) int64 token indices
    Returns:
      (B, out_dim) text embedding
    """
    mask = tokens == PAD_IDX
    x = self.token_embed(tokens) + self.pos_embed
    x = self.transformer(x, src_key_padding_mask=mask)
    # Mean pool over non-pad tokens
    valid = (~mask).unsqueeze(-1).float()
    pooled = (x * valid).sum(dim=1) / valid.sum(dim=1).clamp(min=1)
    return self.proj(pooled)

  def encode_batch(self, captions: list[str], device: torch.device) -> torch.Tensor:
    tokens = torch.stack([tokenize(c, self.max_len) for c in captions]).to(device)
    return self.forward(tokens)
