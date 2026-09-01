"""Procedural synthetic builds for bootstrapping training without external datasets."""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np

from .palette import AIR

# Common building blocks used in synthetic data
STONE = "minecraft:stone"
COBBLE = "minecraft:cobblestone"
PLANKS = "minecraft:oak_planks"
LOG = "minecraft:oak_log"
GLASS = "minecraft:glass"
BRICKS = "minecraft:stone_bricks"
DIRT = "minecraft:dirt"


def generate_synthetic_dataset(
    output_dir: Path,
    count: int = 200,
    resolution: int = 32,
    seed: int = 42,
) -> dict[str, str]:
    """
    Generate synthetic .npy voxel arrays + captions for training bootstrap.
    Returns caption mapping {filename: caption}.
    """
    rng = random.Random(seed)
    output_dir.mkdir(parents=True, exist_ok=True)
    captions: dict[str, str] = {}

    generators = [
        _gen_tower,
        _gen_cottage,
        _gen_wall,
        _gen_platform,
        _gen_pyramid,
    ]

    for i in range(count):
        gen = rng.choice(generators)
        voxels, caption = gen(rng, resolution)
        name = f"synthetic_{i:04d}.npy"
        np.save(output_dir / name, voxels, allow_pickle=True)
        captions[name] = caption

    return captions


def _gen_tower(rng: random.Random, res: int) -> tuple[np.ndarray, str]:
    v = _empty(res)
    mat = rng.choice([STONE, COBBLE, BRICKS])
    w = rng.randint(4, 8)
    h = rng.randint(8, 22)
    cx, cz = res // 2, res // 2
    x0, z0 = cx - w // 2, cz - w // 2

    for y in range(h):
        for x in range(x0, x0 + w):
            for z in range(z0, z0 + w):
                edge = x in (x0, x0 + w - 1) or z in (z0, z0 + w - 1)
                if edge or y == 0:
                    _set(v, x, y, z, mat)

    # Battlements
    if h > 10:
        for x in range(x0, x0 + w, 2):
            for z in range(z0, z0 + w, 2):
                _set(v, x, h, z, mat)

    style = rng.choice(["stone", "cobblestone", "brick"])
    return v, f"a {style} tower {w} blocks wide and {h} blocks tall"


def _gen_cottage(rng: random.Random, res: int) -> tuple[np.ndarray, str]:
    v = _empty(res)
    w = rng.randint(6, 10)
    d = rng.randint(6, 10)
    h = rng.randint(4, 7)
    cx, cz = res // 2, res // 2
    x0, z0 = cx - w // 2, cz - d // 2
    wall = PLANKS
    foundation = COBBLE

    # Foundation
    for x in range(x0 - 1, x0 + w + 1):
        for z in range(z0 - 1, z0 + d + 1):
            _set(v, x, 0, z, foundation)

    # Walls
    for y in range(1, h + 1):
        for x in range(x0, x0 + w):
            for z in range(z0, z0 + d):
                edge = x in (x0, x0 + w - 1) or z in (z0, z0 + d - 1)
                if edge:
                    _set(v, x, y, z, wall)

    # Door opening
    door_x = x0 + w // 2
    _set(v, door_x, 1, z0, AIR)
    _set(v, door_x, 2, z0, AIR)

    # Windows
    for wx in (x0 + 1, x0 + w - 2):
        _set(v, wx, 2, z0, GLASS)
        _set(v, wx, 2, z0 + d - 1, GLASS)

    # Flat roof
    for x in range(x0 - 1, x0 + w + 1):
        for z in range(z0 - 1, z0 + d + 1):
            _set(v, x, h + 1, z, PLANKS)

    return v, f"a small oak cottage {w}x{d} with stone foundation"


def _gen_wall(rng: random.Random, res: int) -> tuple[np.ndarray, str]:
    v = _empty(res)
    mat = rng.choice([STONE, COBBLE, BRICKS])
    length = rng.randint(10, 24)
    height = rng.randint(3, 6)
    cx, cz = res // 2, res // 2
    axis = rng.choice(["x", "z"])

    for i in range(length):
        for y in range(height):
            if axis == "x":
                _set(v, cx - length // 2 + i, y, cz, mat)
            else:
                _set(v, cx, y, cz - length // 2 + i, mat)

    return v, f"a {mat.split(':')[1].replace('_', ' ')} wall {length} blocks long"


def _gen_platform(rng: random.Random, res: int) -> tuple[np.ndarray, str]:
    v = _empty(res)
    mat = rng.choice([PLANKS, STONE, COBBLE])
    w = rng.randint(8, 16)
    cx, cz = res // 2, res // 2
    x0, z0 = cx - w // 2, cz - w // 2

    for x in range(x0, x0 + w):
        for z in range(z0, z0 + w):
            _set(v, x, 0, z, mat)

    # Pillars at corners
    for px, pz in [(x0, z0), (x0 + w - 1, z0), (x0, z0 + w - 1), (x0 + w - 1, z0 + w - 1)]:
        for y in range(1, 4):
            _set(v, px, y, pz, LOG)

    return v, f"a {w}x{w} wooden platform with corner pillars"


def _gen_pyramid(rng: random.Random, res: int) -> tuple[np.ndarray, str]:
    v = _empty(res)
    mat = rng.choice([SAND := "minecraft:sand", SANDSTONE := "minecraft:sandstone", STONE])
    base = rng.randint(6, 14)
    cx, cz = res // 2, res // 2
    x0, z0 = cx - base // 2, cz - base // 2

    for layer in range(base // 2 + 1):
        size = base - layer * 2
        for x in range(size):
            for z in range(size):
                _set(v, x0 + layer + x, layer, z0 + layer + z, mat)

    return v, f"a {mat.split(':')[1]} pyramid with base {base}"


def _empty(res: int) -> np.ndarray:
    return np.full((res, res, res), AIR, dtype=object)


def _set(v: np.ndarray, x: int, y: int, z: int, block: str) -> None:
    if 0 <= x < v.shape[0] and 0 <= y < v.shape[1] and 0 <= z < v.shape[2]:
        v[x, y, z] = block
