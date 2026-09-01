"""Block palette management for voxel encoding."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

AIR = "minecraft:air"
AIR_INDEX = 0


class BlockPalette:
    """Maps Minecraft block IDs to integer class indices. Index 0 is always air."""

    def __init__(self, max_size: int = 256):
        self.max_size = max_size
        self.block_to_idx: dict[str, int] = {AIR: AIR_INDEX}
        self.idx_to_block: dict[int, str] = {AIR_INDEX: AIR}

    @property
    def size(self) -> int:
        return len(self.block_to_idx)

    def encode(self, block_id: str) -> int:
        if block_id not in self.block_to_idx:
            if len(self.block_to_idx) >= self.max_size:
                return self._fallback_index(block_id)
            idx = len(self.block_to_idx)
            self.block_to_idx[block_id] = idx
            self.idx_to_block[idx] = block_id
        return self.block_to_idx[block_id]

    def decode(self, idx: int) -> str:
        return self.idx_to_block.get(int(idx), AIR)

    def _fallback_index(self, block_id: str) -> int:
        """Hash overflow blocks into remaining slots."""
        slot = (hash(block_id) % (self.max_size - 1)) + 1
        return slot

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "max_size": self.max_size,
            "block_to_idx": self.block_to_idx,
            "idx_to_block": {str(k): v for k, v in self.idx_to_block.items()},
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> BlockPalette:
        payload = json.loads(path.read_text(encoding="utf-8"))
        palette = cls(max_size=payload["max_size"])
        palette.block_to_idx = payload["block_to_idx"]
        palette.idx_to_block = {int(k): v for k, v in payload["idx_to_block"].items()}
        return palette


def block_state_to_id(block) -> str:
    """Convert a litemapy BlockState to a minecraft:block_id string."""
    if hasattr(block, "to_block_state_identifier"):
        bid = block.to_block_state_identifier()
        return AIR if bid == "minecraft:air" else bid

    bid = block.id if hasattr(block, "id") else str(block)
    if bid == "minecraft:air":
        return AIR

    props = getattr(block, "properties", None)
    if callable(props):
        items = list(props())
    elif props:
        items = sorted(props.items())
    else:
        return bid

    if not items:
        return bid

    prop_str = ",".join(f"{k}={v}" for k, v in sorted(items))
    return f"{bid}[{prop_str}]"


def voxels_to_palette_indices(voxels: np.ndarray, palette: BlockPalette) -> np.ndarray:
    """Encode a (D,H,W) array of block ID strings into integer indices."""
    encoded = np.zeros(voxels.shape, dtype=np.int64)
    unique = np.unique(voxels)
    mapping = {b: palette.encode(str(b)) for b in unique}
    for block_id, idx in mapping.items():
        encoded[voxels == block_id] = idx
    return encoded
