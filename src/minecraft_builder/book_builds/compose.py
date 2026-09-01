"""Stamp and merge voxel arrays for combination book builds."""

from __future__ import annotations

import numpy as np

from ..data.palette import AIR


def stamp_voxels(
  base: np.ndarray,
  patch: np.ndarray,
  ox: int,
  oy: int,
  oz: int,
) -> np.ndarray:
  """Place patch into base; non-air patch blocks overwrite base."""
  out = base.copy()
  for x in range(patch.shape[0]):
    for y in range(patch.shape[1]):
      for z in range(patch.shape[2]):
        block = patch[x, y, z]
        if block != AIR:
          tx, ty, tz = ox + x, oy + y, oz + z
          if 0 <= tx < out.shape[0] and 0 <= ty < out.shape[1] and 0 <= tz < out.shape[2]:
            out[tx, ty, tz] = block
  return out


def overlay_voxels(base: np.ndarray, top: np.ndarray) -> np.ndarray:
  """Overlay top onto base where both share the same shape and origin."""
  return stamp_voxels(base, top, 0, 0, 0)
