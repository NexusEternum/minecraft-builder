"""Load Minecraft schematic files into dense voxel grids."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .palette import AIR, block_state_to_id

SUPPORTED_EXTENSIONS = {".litematic", ".schem", ".schematic", ".nbt"}


def load_voxels(path: Path, resolution: int = 32) -> np.ndarray:
    """
    Load a schematic file and return a (resolution, resolution, resolution) array
    of block ID strings. Structures are centered and padded with air.
    """
    suffix = path.suffix.lower()
    if suffix == ".litematic":
        raw = _load_litematic(path)
    elif suffix in (".schem", ".schematic"):
        raw = _load_schematic(path)
    else:
        raise ValueError(f"Unsupported format: {suffix}")

    return _normalize_volume(raw, resolution)


def _load_litematic(path: Path) -> np.ndarray:
    from litemapy import Schematic

    schem = Schematic.load(str(path))
    if not schem.regions:
        raise ValueError(f"No regions in {path}")

    # Merge all regions into one volume
    regions = list(schem.regions.values())
    min_x = min(r.x for r in regions)
    min_y = min(r.y for r in regions)
    min_z = min(r.z for r in regions)
    max_x = max(r.x + r.width - 1 for r in regions)
    max_y = max(r.y + r.height - 1 for r in regions)
    max_z = max(r.z + r.length - 1 for r in regions)

    w = max_x - min_x + 1
    h = max_y - min_y + 1
    d = max_z - min_z + 1
    volume = np.full((w, h, d), AIR, dtype=object)

    for region in regions:
        for x, y, z in region.block_positions():
            gx = x - min_x
            gy = y - min_y
            gz = z - min_z
            block = region[x, y, z]
            volume[gx, gy, gz] = block_state_to_id(block)

    return volume


def _load_schematic(path: Path) -> np.ndarray:
    import nbtlib

    nbt = nbtlib.load(path)
    root = nbt

    # Sponge v2 / WorldEdit .schem
    if "Palette" in root and "BlockData" in root:
        return _decode_sponge_palette(root)

    # Classic MCEdit .schematic
    if "Blocks" in root and "Materials" in root:
        return _decode_classic_schematic(root)

    raise ValueError(f"Unrecognized schematic format: {path}")


def _decode_sponge_palette(root) -> np.ndarray:
    palette = root["Palette"]
    idx_to_block = {int(v): str(k) for k, v in palette.items()}
    width = int(root["Width"])
    height = int(root["Height"])
    length = int(root["Length"])
    block_data = root["BlockData"]

    volume = np.full((width, height, length), AIR, dtype=object)
    i = 0
    for y in range(height):
        for z in range(length):
            for x in range(width):
                idx = int(block_data[i])
                volume[x, y, z] = idx_to_block.get(idx, AIR)
                i += 1
    return volume


def _decode_classic_schematic(root) -> np.ndarray:
    materials = str(root["Materials"])
    if materials != "Alpha":
        raise ValueError(f"Unsupported schematic materials: {materials}")

    width = int(root["Width"])
    height = int(root["Height"])
    length = int(root["Length"])
    blocks = root["Blocks"]
    data = root["Data"]

    # Legacy numeric IDs — map common ones; unknown → stone
    legacy_map = {
        0: AIR,
        1: "minecraft:stone",
        2: "minecraft:grass_block",
        3: "minecraft:dirt",
        4: "minecraft:cobblestone",
        5: "minecraft:oak_planks",
        17: "minecraft:oak_log",
        20: "minecraft:glass",
        98: "minecraft:stone_bricks",
    }

    volume = np.full((width, height, length), AIR, dtype=object)
    i = 0
    for y in range(height):
        for z in range(length):
            for x in range(width):
                bid = int(blocks[i])
                volume[x, y, z] = legacy_map.get(bid, "minecraft:stone")
                i += 1
    return volume


def _normalize_volume(volume: np.ndarray, resolution: int) -> np.ndarray:
    """Center-crop or pad a volume to (resolution, resolution, resolution)."""
    w, h, d = volume.shape
    out = np.full((resolution, resolution, resolution), AIR, dtype=object)

    # Crop if too large (center crop)
    src = volume
    if w > resolution:
        start = (w - resolution) // 2
        src = src[start : start + resolution, :, :]
        w = resolution
    if h > resolution:
        start = (h - resolution) // 2
        src = src[:, start : start + resolution, :]
        h = resolution
    if d > resolution:
        start = (d - resolution) // 2
        src = src[:, :, start : start + resolution]
        d = resolution

    # Pad into center of output
    ox = (resolution - w) // 2
    oy = (resolution - h) // 2
    oz = (resolution - d) // 2
    out[ox : ox + w, oy : oy + h, oz : oz + d] = src
    return out
