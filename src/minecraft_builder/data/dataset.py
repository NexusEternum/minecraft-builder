"""PyTorch dataset for voxel diffusion training."""

from __future__ import annotations

import json
import random
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import Dataset

from .ingest import SUPPORTED_EXTENSIONS, load_voxels
from .palette import AIR_INDEX, BlockPalette, voxels_to_palette_indices


class VoxelDataset(Dataset):
  """
  Loads preprocessed .npz files or raw schematic files.
  Each sample: {voxels: (R,R,R) int64, caption: str}
  """

  def __init__(
    self,
    data_dir: Path,
    palette: BlockPalette,
    captions: dict[str, str] | None = None,
    resolution: int = 32,
  ):
    self.data_dir = Path(data_dir)
    self.palette = palette
    self.captions = captions or {}
    self.resolution = resolution
    self.samples = self._discover_samples()

  def _discover_samples(self) -> list[Path]:
    paths: list[Path] = []
    for ext in ("*.npz",):
      paths.extend(sorted(self.data_dir.glob(ext)))
    if not paths:
      raise FileNotFoundError(f"No training files found in {self.data_dir}")
    return paths

  def __len__(self) -> int:
    return len(self.samples)

  def __getitem__(self, idx: int) -> dict:
    path = self.samples[idx]
    caption = self._caption_for(path)

    if path.suffix == ".npz":
      data = np.load(path)
      indices = data["voxels"].astype(np.int64)
    elif path.suffix == ".npy":
      voxels = np.load(path, allow_pickle=True)
      indices = voxels_to_palette_indices(voxels, self.palette)
    else:
      voxels = load_voxels(path, self.resolution)
      indices = voxels_to_palette_indices(voxels, self.palette)

    return {
      "voxels": torch.from_numpy(indices).long(),
      "caption": caption,
      "path": str(path),
    }

  def _caption_for(self, path: Path) -> str:
    for key in (path.name, path.stem):
      if key in self.captions:
        return self.captions[key]
    # Derive a weak caption from filename
    return path.stem.replace("_", " ").replace("-", " ")


def collate_batch(batch: list[dict]) -> dict:
  return {
    "voxels": torch.stack([b["voxels"] for b in batch]),
    "captions": [b["caption"] for b in batch],
    "paths": [b["path"] for b in batch],
  }


def load_captions(path: Path | None) -> dict[str, str]:
  if path is None or not path.exists():
    return {}
  return json.loads(path.read_text(encoding="utf-8"))


def train_val_split(
  dataset: VoxelDataset, val_ratio: float, seed: int = 42
) -> tuple[VoxelDataset, VoxelDataset]:
  indices = list(range(len(dataset)))
  rng = random.Random(seed)
  rng.shuffle(indices)
  split = int(len(indices) * (1 - val_ratio))
  train_idx, val_idx = indices[:split], indices[split:]

  train_ds = _Subset(dataset, train_idx)
  val_ds = _Subset(dataset, val_idx)
  return train_ds, val_ds


class _Subset(Dataset):
  def __init__(self, dataset: VoxelDataset, indices: list[int]):
    self.dataset = dataset
    self.indices = indices

  def __len__(self) -> int:
    return len(self.indices)

  def __getitem__(self, idx: int) -> dict:
    return self.dataset[self.indices[idx]]
