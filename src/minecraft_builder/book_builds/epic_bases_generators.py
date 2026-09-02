"""Procedural generators for Minecraft Epic Bases modular builds."""

from __future__ import annotations

import numpy as np

from ..data.palette import AIR
from .epic_bases_registry import EPIC_BASES


def generate_epic_base(build_id: str) -> np.ndarray:
  if build_id not in EPIC_BASES:
    raise KeyError(f"Unknown epic base: {build_id}")
  fn = _GENERATORS.get(build_id)
  if fn is None:
    raise NotImplementedError(f"No generator for {build_id}")
  return fn()


def _b(name: str) -> str:
  return name if name.startswith("minecraft:") else f"minecraft:{name}"


def _set(v: np.ndarray, x: int, y: int, z: int, block: str) -> None:
  if 0 <= x < v.shape[0] and 0 <= y < v.shape[1] and 0 <= z < v.shape[2]:
    v[x, y, z] = block


def _generate_epic_bases_wolf_figurehead() -> np.ndarray:
  STONE = _b("stone_bricks")
  AND = _b("andesite")
  POL = _b("polished_andesite")
  GRAY = _b("gray_concrete")
  SPRUCE = _b("spruce_planks")
  DARK = _b("dark_oak_planks")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 14, 1
  for y in range(oy, oy + 7):
    for x in range(ox, ox + 4):
      for z in range(oz, oz + 4):
        _set(v, x, y, z, STONE if y < oy + 4 else AND)
  for x in range(ox + 1, ox + 3):
    _set(v, x, oy + 4, oz + 1, POL)
    _set(v, x, oy + 5, oz, GRAY)
    _set(v, x, oy + 6, oz + 2, GRAY)
  _set(v, ox + 3, oy + 2, oz + 1, SPRUCE)
  _set(v, ox, oy + 1, oz + 2, DARK)
  return v


def _generate_epic_bases_deck_brazier() -> np.ndarray:
  SPRUCE = _b("spruce_planks")
  FENCE = _b("dark_oak_fence")
  FIRE = _b("campfire")
  LANTERN = _b("lantern")
  TRAP = _b("oak_trapdoor")
  CHAIN = _b("chain")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 14, 14, 2
  for x in range(ox, ox + 4):
    for z in range(oz, oz + 4):
      _set(v, x, oy, z, SPRUCE)
  _set(v, ox + 1, oy + 1, oz + 1, FIRE)
  _set(v, ox + 2, oy + 2, oz + 1, LANTERN)
  for x in range(ox, ox + 4):
    _set(v, x, oy + 1, oz, FENCE)
    _set(v, x, oy + 1, oz + 3, FENCE)
  _set(v, ox + 1, oy + 3, oz + 2, CHAIN)
  _set(v, ox + 2, oy + 4, oz + 2, TRAP)
  return v


def _generate_epic_bases_emerald_wolf() -> np.ndarray:
  EMERALD = _b("emerald_block")
  LANTERN = _b("sea_lantern")
  SPRUCE = _b("spruce_planks")
  DARK = _b("dark_oak_planks")
  STONE = _b("stone_bricks")
  GOLD = _b("gold_block")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 14, 14, 1
  for x in range(ox, ox + 4):
    for z in range(oz, oz + 4):
      _set(v, x, oy, z, SPRUCE)
  for y in range(oy + 1, oy + 4):
    _set(v, ox + 1, y, oz + 1, EMERALD)
    _set(v, ox + 2, y, oz + 2, EMERALD if y < oy + 3 else LANTERN)
  _set(v, ox, oy + 1, oz, STONE)
  _set(v, ox + 3, oy + 2, oz + 3, GOLD)
  _set(v, ox + 2, oy, oz + 1, DARK)
  return v


def _generate_epic_bases_crows_nest() -> np.ndarray:
  FENCE = _b("oak_fence")
  SPRUCE = _b("spruce_planks")
  DARK = _b("dark_oak_planks")
  LADDER = _b("ladder")
  TRAP = _b("oak_trapdoor")
  LANTERN = _b("lantern")
  LOG = _b("oak_log")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 10):
    _set(v, cx, y, cz, LOG)
    _set(v, cx, y, cz + 1, LADDER)
  for x in range(cx - 1, cx + 2):
    for z in range(cz - 1, cz + 2):
      _set(v, x, oy + 8, z, SPRUCE)
      _set(v, x, oy + 9, z, FENCE if x in (cx - 1, cx + 1) or z in (cz - 1, cz + 1) else DARK)
  _set(v, cx, oy + 9, cz, TRAP)
  _set(v, cx + 1, oy + 9, cz + 1, LANTERN)
  return v


def _generate_epic_bases_ship_flag() -> np.ndarray:
  RED = _b("red_wool")
  WHITE = _b("white_wool")
  FENCE = _b("oak_fence")
  SFENCE = _b("spruce_fence")
  LOG = _b("oak_log")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 8):
    _set(v, cx, y, cz, LOG)
  for y in range(oy + 3, oy + 7):
    for x in range(cx + 1, cx + 4):
      _set(v, x, y, cz, RED if (x + y) % 2 else WHITE)
  _set(v, cx + 1, oy + 2, cz, FENCE)
  _set(v, cx + 2, oy + 7, cz, SFENCE)
  return v


def _generate_epic_bases_ship_oars() -> np.ndarray:
  SPRUCE = _b("spruce_planks")
  DARK = _b("dark_oak_planks")
  FENCE = _b("oak_fence")
  STAIR = _b("spruce_stairs")
  WATER = _b("water")
  LOG = _b("dark_oak_log")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 13, 2
  for x in range(ox, ox + 10):
    _set(v, x, oy, oz, SPRUCE)
    _set(v, x, oy, oz + 5, DARK)
    _set(v, x, oy - 1, oz + 2, WATER)
  for x in range(ox + 1, ox + 9, 2):
    _set(v, x, oy + 1, oz - 1, FENCE)
    _set(v, x, oy + 1, oz + 6, FENCE)
    _set(v, x, oy, oz + 1, STAIR)
  _set(v, ox + 4, oy + 1, oz + 3, LOG)
  return v


def _generate_epic_bases_artillery_cannon() -> np.ndarray:
  DARK = _b("dark_oak_planks")
  STONE = _b("stone_bricks")
  IRON = _b("iron_block")
  TNT = _b("tnt")
  DISP = _b("dispenser")
  STAIR = _b("oak_stairs")
  WATER = _b("water")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 13, 2
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 6):
      _set(v, x, oy, z, DARK)
  _set(v, ox + 2, oy + 1, oz + 1, STONE)
  _set(v, ox + 3, oy + 2, oz + 2, IRON)
  _set(v, ox + 4, oy + 2, oz + 3, TNT)
  _set(v, ox + 2, oy + 3, oz + 4, DISP)
  _set(v, ox + 1, oy + 1, oz + 5, STAIR)
  _set(v, ox + 5, oy - 1, oz + 2, WATER)
  return v


_GENERATORS: dict[str, object] = {
  "epic_bases_wolf_figurehead": _generate_epic_bases_wolf_figurehead,
  "epic_bases_deck_brazier": _generate_epic_bases_deck_brazier,
  "epic_bases_emerald_wolf": _generate_epic_bases_emerald_wolf,
  "epic_bases_crows_nest": _generate_epic_bases_crows_nest,
  "epic_bases_ship_flag": _generate_epic_bases_ship_flag,
  "epic_bases_ship_oars": _generate_epic_bases_ship_oars,
  "epic_bases_artillery_cannon": _generate_epic_bases_artillery_cannon,
}
