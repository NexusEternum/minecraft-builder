"""3D U-Net denoiser with text cross-attention — built from scratch."""

from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class SinusoidalTimeEmbedding(nn.Module):
  def __init__(self, dim: int):
    super().__init__()
    self.dim = dim
    self.mlp = nn.Sequential(
      nn.Linear(dim, dim * 4),
      nn.GELU(),
      nn.Linear(dim * 4, dim),
    )

  def forward(self, t: torch.Tensor) -> torch.Tensor:
    half = self.dim // 2
    freqs = torch.exp(
      -math.log(10000) * torch.arange(half, device=t.device, dtype=torch.float32) / half
    )
    args = t.float().unsqueeze(1) * freqs.unsqueeze(0)
    emb = torch.cat([args.sin(), args.cos()], dim=-1)
    return self.mlp(emb)


class ResBlock3D(nn.Module):
  def __init__(self, channels: int, time_dim: int, text_dim: int):
    super().__init__()
    self.norm1 = nn.GroupNorm(8, channels)
    self.conv1 = nn.Conv3d(channels, channels, 3, padding=1)
    self.norm2 = nn.GroupNorm(8, channels)
    self.conv2 = nn.Conv3d(channels, channels, 3, padding=1)
    self.time_proj = nn.Linear(time_dim, channels)
    self.text_proj = nn.Linear(text_dim, channels)

  def forward(self, x: torch.Tensor, t_emb: torch.Tensor, text_emb: torch.Tensor) -> torch.Tensor:
    h = self.conv1(F.silu(self.norm1(x)))
    cond = self.time_proj(t_emb)[:, :, None, None, None] + self.text_proj(text_emb)[
      :, :, None, None, None
    ]
    h = h + cond
    h = self.conv2(F.silu(self.norm2(h)))
    return x + h


class DownStage(nn.Module):
  def __init__(self, in_ch: int, out_ch: int, time_dim: int, text_dim: int, num_res: int):
    super().__init__()
    self.res = nn.ModuleList([ResBlock3D(in_ch, time_dim, text_dim) for _ in range(num_res)])
    self.down = nn.Conv3d(in_ch, out_ch, 3, stride=2, padding=1)

  def forward(self, x, t_emb, text_emb):
    for block in self.res:
      x = block(x, t_emb, text_emb)
    skip = x
    x = self.down(x)
    return x, skip


class UpStage(nn.Module):
  def __init__(self, in_ch: int, skip_ch: int, out_ch: int, time_dim: int, text_dim: int, num_res: int):
    super().__init__()
    self.up = nn.ConvTranspose3d(in_ch, out_ch, 2, stride=2)
    self.merge = nn.Conv3d(out_ch + skip_ch, out_ch, 1)
    self.res = nn.ModuleList([ResBlock3D(out_ch, time_dim, text_dim) for _ in range(num_res)])

  def forward(self, x, skip, t_emb, text_emb):
    x = self.up(x)
    if x.shape[2:] != skip.shape[2:]:
      x = F.interpolate(x, size=skip.shape[2:], mode="trilinear", align_corners=False)
    x = self.merge(torch.cat([x, skip], dim=1))
    for block in self.res:
      x = block(x, t_emb, text_emb)
    return x


class UNet3D(nn.Module):
  """Denoising U-Net on embedded voxel volumes."""

  def __init__(
    self,
    in_channels: int = 32,
    base_channels: int = 64,
    channel_mults: list[int] | None = None,
    num_res_blocks: int = 2,
    time_dim: int = 256,
    text_dim: int = 256,
  ):
    super().__init__()
    channel_mults = channel_mults or [1, 2, 4]
    self.time_embed = SinusoidalTimeEmbedding(time_dim)

    chs = [base_channels * m for m in channel_mults]
    self.input_conv = nn.Conv3d(in_channels, chs[0], 3, padding=1)

    self.down_stages = nn.ModuleList()
    for i in range(len(chs) - 1):
      self.down_stages.append(
        DownStage(chs[i], chs[i + 1], time_dim, text_dim, num_res_blocks)
      )

    self.mid = nn.ModuleList([ResBlock3D(chs[-1], time_dim, text_dim) for _ in range(2)])

    self.up_stages = nn.ModuleList()
    for i in reversed(range(len(chs) - 1)):
      self.up_stages.append(
        UpStage(chs[i + 1], chs[i], chs[i], time_dim, text_dim, num_res_blocks)
      )

    self.output = nn.Sequential(
      nn.GroupNorm(8, chs[0]),
      nn.SiLU(),
      nn.Conv3d(chs[0], in_channels, 3, padding=1),
    )

  def forward(self, x: torch.Tensor, t: torch.Tensor, text_emb: torch.Tensor) -> torch.Tensor:
    t_emb = self.time_embed(t)
    h = self.input_conv(x)
    skips = []

    for stage in self.down_stages:
      h, skip = stage(h, t_emb, text_emb)
      skips.append(skip)

    for block in self.mid:
      h = block(h, t_emb, text_emb)

    for stage, skip in zip(self.up_stages, reversed(skips)):
      h = stage(h, skip, t_emb, text_emb)

    return self.output(h)
