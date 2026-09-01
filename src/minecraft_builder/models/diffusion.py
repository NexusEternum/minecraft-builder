"""DDPM diffusion process and combined voxel diffusion model."""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F

from .text_encoder import TextEncoder
from .unet3d import UNet3D


@dataclass
class DiffusionConfig:
  timesteps: int = 200
  beta_schedule: str = "cosine"
  embed_dim: int = 32
  num_classes: int = 256
  base_channels: int = 64
  channel_mults: list[int] | None = None
  num_res_blocks: int = 2
  text_dim: int = 256
  text_vocab_size: int = 128
  text_max_len: int = 128


class GaussianDiffusion(nn.Module):
  """
  DDPM on continuous voxel embeddings.
  Each discrete block class is embedded, noised, denoised, then decoded back to classes.
  """

  def __init__(self, config: DiffusionConfig):
    super().__init__()
    self.config = config
    self.embed_dim = config.embed_dim
    self.num_classes = config.num_classes

    self.block_embed = nn.Embedding(config.num_classes, config.embed_dim)
    self.text_encoder = TextEncoder(
      vocab_size=config.text_vocab_size,
      max_len=config.text_max_len,
      out_dim=config.text_dim,
    )
    self.unet = UNet3D(
      in_channels=config.embed_dim,
      base_channels=config.base_channels,
      channel_mults=config.channel_mults,
      num_res_blocks=config.num_res_blocks,
      text_dim=config.text_dim,
    )

    betas = self._make_betas(config.timesteps, config.beta_schedule)
    self.register_buffer("betas", betas)
    alphas = 1.0 - betas
    self.register_buffer("alphas", alphas)
    self.register_buffer("alphas_cumprod", torch.cumprod(alphas, dim=0))
    self.register_buffer(
      "sqrt_alphas_cumprod", torch.sqrt(self.alphas_cumprod)
    )
    self.register_buffer(
      "sqrt_one_minus_alphas_cumprod", torch.sqrt(1.0 - self.alphas_cumprod)
    )

  @staticmethod
  def _make_betas(timesteps: int, schedule: str) -> torch.Tensor:
    if schedule == "linear":
      return torch.linspace(1e-4, 0.02, timesteps)
    # Cosine schedule (Nichol & Dhariwal)
    steps = timesteps + 1
    t = torch.linspace(0, timesteps, steps)
    s = 0.008
    f = torch.cos(((t / timesteps) + s) / (1 + s) * math.pi / 2) ** 2
    alphas_cumprod = f / f[0]
    betas = 1 - (alphas_cumprod[1:] / alphas_cumprod[:-1])
    return betas.clamp(0.0001, 0.9999)

  def embed_voxels(self, voxel_indices: torch.Tensor) -> torch.Tensor:
    """(B, D, H, W) int -> (B, C, D, H, W) float"""
    emb = self.block_embed(voxel_indices)  # (B, D, H, W, C)
    return emb.permute(0, 4, 1, 2, 3).contiguous()

  def encode_text(self, captions: list[str], device: torch.device) -> torch.Tensor:
    return self.text_encoder.encode_batch(captions, device)

  def q_sample(
    self, x0: torch.Tensor, t: torch.Tensor, noise: torch.Tensor | None = None
  ) -> tuple[torch.Tensor, torch.Tensor]:
    if noise is None:
      noise = torch.randn_like(x0)
    sqrt_alpha = self.sqrt_alphas_cumprod[t][:, None, None, None, None]
    sqrt_one_minus = self.sqrt_one_minus_alphas_cumprod[t][:, None, None, None, None]
    xt = sqrt_alpha * x0 + sqrt_one_minus * noise
    return xt, noise

  def training_loss(
    self,
    voxel_indices: torch.Tensor,
    captions: list[str],
    non_air_weight: float = 5.0,
    uncond_prob: float = 0.1,
  ) -> torch.Tensor:
    device = voxel_indices.device
    b = voxel_indices.shape[0]
    voxel_indices = voxel_indices.clamp(0, self.num_classes - 1)
    x0 = self.embed_voxels(voxel_indices)
    t = torch.randint(0, self.config.timesteps, (b,), device=device)
    xt, noise = self.q_sample(x0, t)

    # Classifier-free guidance: randomly drop text conditioning during training
    text_emb = self.encode_text(captions, device)
    if uncond_prob > 0:
      mask = torch.rand(b, device=device) < uncond_prob
      null_emb = self.encode_text([""] * b, device)
      text_emb = torch.where(mask.unsqueeze(1), null_emb, text_emb)

    pred_noise = self.unet(xt, t, text_emb)
    weight = torch.where(
      voxel_indices.unsqueeze(1) != 0,
      torch.full((), non_air_weight, device=device, dtype=x0.dtype),
      torch.ones((), device=device, dtype=x0.dtype),
    )
    loss = (weight * (pred_noise - noise).pow(2)).mean()
    return loss

  @torch.no_grad()
  def sample(
    self,
    captions: list[str],
    resolution: int,
    guidance_scale: float = 3.0,
    device: torch.device | None = None,
  ) -> torch.Tensor:
    """
    Generate voxel class indices via reverse diffusion.
    Returns (B, D, H, W) int64 tensor.
    """
    device = device or next(self.parameters()).device
    b = len(captions)
    shape = (b, self.embed_dim, resolution, resolution, resolution)

    text_emb = self.encode_text(captions, device)
    null_emb = self.encode_text([""] * b, device)

    x = torch.randn(shape, device=device)
    for step in reversed(range(self.config.timesteps)):
      t = torch.full((b,), step, device=device, dtype=torch.long)
      pred = self.unet(x, t, text_emb)
      if guidance_scale != 1.0:
        pred_uncond = self.unet(x, t, null_emb)
        pred = pred_uncond + guidance_scale * (pred - pred_uncond)
      x = self._p_sample(x, pred, t)
    return self._decode_to_indices(x)

  def _p_sample(self, x: torch.Tensor, pred_noise: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
    beta = self.betas[t][:, None, None, None, None]
    alpha = self.alphas[t][:, None, None, None, None]
    alpha_cumprod = self.alphas_cumprod[t][:, None, None, None, None]
    sqrt_recip_alpha = torch.sqrt(1.0 / alpha)
    mean = sqrt_recip_alpha * (x - beta / torch.sqrt(1 - alpha_cumprod) * pred_noise)
    if (t == 0).all():
      return mean
    noise = torch.randn_like(x)
    return mean + torch.sqrt(beta) * noise

  def _decode_to_indices(self, x: torch.Tensor) -> torch.Tensor:
    """Nearest-neighbor decode from embedding space back to block classes."""
    # x: (B, C, D, H, W) -> compare against all class embeddings
    weights = self.block_embed.weight  # (num_classes, C)
    x_perm = x.permute(0, 2, 3, 4, 1)  # (B, D, H, W, C)
    # Cosine similarity
    x_norm = F.normalize(x_perm, dim=-1)
    w_norm = F.normalize(weights, dim=-1)
    logits = torch.matmul(x_norm, w_norm.T)  # (B, D, H, W, num_classes)
    return logits.argmax(dim=-1)
