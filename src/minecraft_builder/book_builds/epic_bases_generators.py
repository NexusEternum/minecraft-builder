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


def _fenrir_v():
  return _tomb_v()


def _generate_epic_bases_fenrir_billowing_sails() -> np.ndarray:
  RED, WHITE, STAIR, SLAB, FENCE, LOG = _b("red_wool"), _b("white_wool"), _b("spruce_stairs"), _b("spruce_slab"), _b("oak_fence"), _b("oak_log")
  v = _fenrir_v(); cx, cz, oy = 16, 16, 2
  for y in range(oy, oy + 8):
    _set(v, cx, y, cz, LOG)
  for y in range(oy + 2, oy + 7):
    for x in range(cx + 1, cx + 5):
      _set(v, x, y, cz + 1, RED if (x + y) % 2 else WHITE)
      _set(v, x, y, cz + 2, STAIR if y % 2 else SLAB)
  _set(v, cx + 5, oy + 4, cz, FENCE)
  return v


def _generate_epic_bases_fenrir_boat_ribs() -> np.ndarray:
  SPRUCE, DARK, STAIR, LOG = _b("spruce_planks"), _b("dark_oak_planks"), _b("spruce_stairs"), _b("oak_log")
  v = _fenrir_v(); ox, oz, oy = 11, 13, 2
  for i in range(5):
    x = ox + i * 2
    for z in range(oz, oz + 6):
      depth = abs(z - (oz + 3))
      _set(v, x, oy + depth, z, STAIR if depth else SPRUCE)
      _set(v, x, oy + depth + 1, z, DARK)
  _set(v, ox + 4, oy + 3, oz + 3, LOG)
  return v


def _generate_epic_bases_fenrir_storage_cabin() -> np.ndarray:
  SPRUCE, DARK, CHEST, DOOR, LANTERN = _b("spruce_planks"), _b("dark_oak_planks"), _b("chest"), _b("oak_door"), _b("lantern")
  v = _fenrir_v(); ox, oz, oy = 14, 14, 3
  for y in range(oy, oy + 3):
    for x in range(ox, ox + 4):
      for z in range(oz, oz + 3):
        edge = x in (ox, ox + 3) or z in (oz, oz + 2)
        if edge:
          _set(v, x, y, z, SPRUCE if y < oy + 2 else DARK)
  _set(v, ox + 1, oy + 1, oz, DOOR)
  _set(v, ox + 2, oy + 1, oz + 1, CHEST)
  _set(v, ox + 2, oy + 3, oz + 1, LANTERN)
  return v


def _generate_epic_bases_fenrir_thatched_roof() -> np.ndarray:
  HAY, S_STAIR, D_STAIR, PLANK = _b("hay_block"), _b("spruce_stairs"), _b("dark_oak_stairs"), _b("spruce_planks")
  v = _fenrir_v(); ox, oz, oy = 13, 13, 5
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 5):
      _set(v, x, oy, z, PLANK)
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 5):
      _set(v, x, oy + 1, z, HAY if (x + z) % 2 else S_STAIR)
      if (x + z) % 3 == 0:
        _set(v, x, oy + 2, z, D_STAIR)
  return v


def _generate_epic_bases_fenrir_bunk_beds() -> np.ndarray:
  BED, PLANK, LADDER, TORCH, CHEST = _b("green_bed"), _b("spruce_planks"), _b("ladder"), _b("torch"), _b("chest")
  v = _fenrir_v(); ox, oz, oy = 14, 14, 2
  for x in range(ox, ox + 4):
    for z in range(oz, oz + 3):
      _set(v, x, oy, z, PLANK)
  _set(v, ox + 1, oy + 1, oz + 1, BED)
  _set(v, ox + 1, oy + 2, oz + 1, BED)
  _set(v, ox + 2, oy + 1, oz + 2, LADDER)
  _set(v, ox + 3, oy + 2, oz + 1, TORCH)
  _set(v, ox + 1, oy + 1, oz + 2, CHEST)
  return v


def _generate_epic_bases_fenrir_map_table() -> np.ndarray:
  CART, PLANK, DARK, FRAME, LANTERN = _b("cartography_table"), _b("spruce_planks"), _b("dark_oak_planks"), _b("item_frame"), _b("lantern")
  v = _fenrir_v(); ox, oz, oy = 13, 13, 2
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 5):
      _set(v, x, oy, z, PLANK)
  _set(v, ox + 2, oy + 1, oz + 2, CART)
  _set(v, ox + 3, oy + 1, oz + 2, CART)
  _set(v, ox + 4, oy + 2, oz + 1, FRAME)
  _set(v, ox + 1, oy + 2, oz + 3, LANTERN)
  for x in range(ox, ox + 6):
    _set(v, x, oy + 2, oz, DARK)
  return v


def _generate_epic_bases_fenrir_crossbeams() -> np.ndarray:
  LOG, DLOG, FENCE, HAY = _b("spruce_log"), _b("dark_oak_log"), _b("spruce_fence"), _b("hay_block")
  v = _fenrir_v(); cx, cz, oy = 16, 16, 4
  for i in range(-2, 3):
    _set(v, cx + i, oy, cz + i, LOG)
    _set(v, cx + i, oy, cz - i, DLOG)
  for y in range(oy + 1, oy + 4):
    _set(v, cx, y, cz, FENCE)
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      _set(v, x, oy + 3, z, HAY)
  return v


def _generate_epic_bases_fenrir_throne_room() -> np.ndarray:
  EMERALD, PLANK, LOG, CANDLE, GOLD, CARPET, LANTERN = (
    _b("emerald_block"), _b("dark_oak_planks"), _b("spruce_log"),
    _b("candle"), _b("gold_block"), _b("red_carpet"), _b("lantern"),
  )
  v = _fenrir_v(); ox, oz, oy = 13, 12, 1
  for x in range(ox, ox + 7):
    for z in range(oz, oz + 6):
      _set(v, x, oy, z, EMERALD)
  for y in range(oy + 1, oy + 4):
    for x in range(ox, ox + 7):
      for z in range(oz, oz + 6):
        if x in (ox, ox + 6) or z in (oz, oz + 5):
          _set(v, x, y, z, LOG if x % 2 == 0 else PLANK)
  _set(v, ox + 3, oy + 1, oz + 2, GOLD)
  _set(v, ox + 3, oy, oz + 3, CARPET)
  _set(v, ox + 1, oy + 2, oz + 1, CANDLE)
  _set(v, ox + 5, oy + 2, oz + 4, LANTERN)
  return v


def _generate_epic_bases_fenrir_tnt_cannon_redstone() -> np.ndarray:
  DARK, DISP, TNT, REP, DUST, TORCH, CAULDRON, GRIND, BUTTON, WATER = (
    _b("dark_oak_planks"), _b("dispenser"), _b("tnt"), _b("redstone_repeater"),
    _b("redstone_dust"), _b("redstone_torch"), _b("cauldron"), _b("grindstone"),
    _b("stone_button"), _b("water"),
  )
  v = _fenrir_v(); ox, oz, oy = 13, 14, 2
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 4):
      _set(v, x, oy, z, DARK)
  for x in range(ox + 1, ox + 5):
    _set(v, x, oy + 1, oz + 1, DISP)
    _set(v, x, oy + 2, oz + 1, TNT)
  _set(v, ox + 2, oy + 1, oz + 2, CAULDRON)
  _set(v, ox + 3, oy + 1, oz + 2, GRIND)
  for i, x in enumerate(range(ox, ox + 5)):
    _set(v, x, oy - 1, oz, REP)
    _set(v, x, oy - 1, oz + 1, DUST)
  _set(v, ox + 5, oy - 1, oz, TORCH)
  _set(v, ox + 1, oy - 1, oz + 3, BUTTON)
  _set(v, ox + 4, oy - 1, oz + 2, WATER)
  return v


def _tomb_v(res=32):
  return np.full((res, res, res), AIR, dtype=object)


def _generate_epic_bases_tomb_desert_oasis() -> np.ndarray:
  SAND, SANDSTONE, WATER = _b("sand"), _b("sandstone"), _b("water")
  GRASS, LOG, LEAVES = _b("grass_block"), _b("acacia_log"), _b("acacia_leaves")
  v = _tomb_v()
  ox, oz, oy = 12, 12, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 8):
      _set(v, x, oy - 1, z, SAND)
  for x in range(ox + 2, ox + 6):
    for z in range(oz + 2, oz + 6):
      _set(v, x, oy, z, WATER if (x + z) % 3 == 0 else GRASS)
  for tx, tz in ((ox + 1, oz + 1), (ox + 6, oz + 5)):
    for y in range(oy + 1, oy + 5):
      _set(v, tx, y, tz, LOG)
    _set(v, tx, oy + 5, tz, LEAVES)
    _set(v, tx + 1, oy + 4, tz, LEAVES)
  return v


def _generate_epic_bases_tomb_water_bearer_statue() -> np.ndarray:
  RED, ORANGE, WATER, GLASS = _b("red_sandstone"), _b("orange_terracotta"), _b("water"), _b("blue_stained_glass")
  v = _tomb_v()
  cx, cz, oy = 16, 14, 1
  for y in range(oy, oy + 9):
    _set(v, cx, y, cz, RED)
    _set(v, cx - 1, y, cz, ORANGE)
    _set(v, cx + 1, y, cz, ORANGE)
  for y in range(oy + 6, oy + 9):
    _set(v, cx - 1, y, cz + 1, WATER)
    _set(v, cx + 1, y, cz + 1, WATER)
  for y in range(oy, oy + 8):
    _set(v, cx, y, cz + 2, GLASS if y % 2 else WATER)
  return v


def _generate_epic_bases_tomb_fire_bearer_statue() -> np.ndarray:
  RED, ORANGE, FIRE = _b("red_sandstone"), _b("orange_terracotta"), _b("campfire")
  v = _tomb_v()
  cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 7):
    _set(v, cx, y, cz, RED)
    _set(v, cx - 1, y, cz, ORANGE)
    _set(v, cx + 1, y, cz, ORANGE)
  _set(v, cx, oy + 7, cz, FIRE)
  _set(v, cx - 1, oy + 6, cz, FIRE)
  return v


def _generate_epic_bases_tomb_grand_entrance() -> np.ndarray:
  RED, SAND, CHISELED, BANNER = _b("red_sandstone"), _b("sandstone"), _b("chiseled_sandstone"), _b("blue_banner")
  v = _tomb_v()
  ox, oz, oy = 12, 14, 1
  for y in range(oy, oy + 9):
    for x in range(ox, ox + 8):
      _set(v, x, y, oz, RED)
      _set(v, x, y, oz + 1, SAND if y < oy + 7 else CHISELED)
  for y in range(oy + 2, oy + 6):
    _set(v, ox + 3, y, oz + 2, AIR)
    _set(v, ox + 4, y, oz + 2, AIR)
  _set(v, ox + 2, oy + 7, oz, BANNER)
  _set(v, ox + 5, oy + 7, oz, BANNER)
  return v


def _generate_epic_bases_tomb_pillared_river() -> np.ndarray:
  PILLAR, QUARTZ, BANNER, WATER, SAND = _b("quartz_pillar"), _b("quartz_block"), _b("blue_banner"), _b("water"), _b("sandstone")
  v = _tomb_v()
  ox, oz, oy = 10, 12, 1
  for i in range(6):
    px = ox + i * 2
    for y in range(oy, oy + 7):
      _set(v, px, y, oz, PILLAR)
      _set(v, px, y, oz + 6, PILLAR)
    _set(v, px, oy + 7, oz, BANNER)
    _set(v, px, oy, oz + 3, WATER)
    _set(v, px, oy + 1, oz + 2, SAND)
    _set(v, px, oy + 1, oz + 4, SAND)
  return v


def _generate_epic_bases_tomb_fire_beacons() -> np.ndarray:
  SAND, SANDSTONE, FIRE = _b("sand"), _b("sandstone"), _b("campfire")
  v = _tomb_v()
  cx, cz, oy = 16, 16, 1
  for x in range(cx - 4, cx + 5):
    for z in range(cz - 4, cz + 5):
      _set(v, x, oy - 1, z, SAND)
  for x, z in ((cx - 4, cz), (cx + 4, cz), (cx, cz - 4), (cx, cz + 4)):
    _set(v, x, oy, z, SANDSTONE)
    _set(v, x, oy + 1, z, FIRE)
  return v


def _generate_epic_bases_tomb_library() -> np.ndarray:
  SHELF, SAND, CARPET, TORCH = _b("bookshelf"), _b("sandstone"), _b("red_carpet"), _b("torch")
  v = _tomb_v()
  ox, oz, oy = 12, 11, 1
  for y in range(oy, oy + 4):
    for x in range(ox, ox + 8):
      for z in range(oz, oz + 6):
        edge = x in (ox, ox + 7) or z in (oz, oz + 5)
        if edge:
          _set(v, x, y, z, SHELF if y < oy + 3 else SAND)
        elif y == oy:
          _set(v, x, oy, z, CARPET)
  _set(v, ox + 4, oy + 2, oz + 3, TORCH)
  return v


def _generate_epic_bases_tomb_tree_farm() -> np.ndarray:
  GRASS, DIRT, OLOG, OLEAVES, ALOG, ALEAVES, SAND, TORCH = (
    _b("grass_block"), _b("dirt"), _b("oak_log"), _b("oak_leaves"),
    _b("acacia_log"), _b("acacia_leaves"), _b("sandstone"), _b("torch"),
  )
  v = _tomb_v()
  ox, oz, oy = 12, 12, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 6):
      _set(v, x, oy - 1, z, DIRT)
      _set(v, x, oy, z, GRASS)
  for tx, tz, log, leaf in ((ox + 1, oz + 1, OLOG, OLEAVES), (ox + 5, oz + 4, ALOG, ALEAVES)):
    for y in range(oy + 1, oy + 5):
      _set(v, tx, y, tz, log)
    _set(v, tx, oy + 5, tz, leaf)
  for x in range(ox, ox + 8):
    _set(v, x, oy + 5, oz, SAND)
    _set(v, x, oy + 5, oz + 5, SAND)
  _set(v, ox + 4, oy + 3, oz + 3, TORCH)
  return v


def _generate_epic_bases_tomb_royal_bedchamber() -> np.ndarray:
  YELLOW, BLUE, CHISELED, BED, SAND, TORCH = (
    _b("yellow_terracotta"), _b("blue_terracotta"), _b("chiseled_sandstone"),
    _b("red_bed"), _b("sandstone"), _b("torch"),
  )
  v = _tomb_v()
  ox, oz, oy = 13, 13, 1
  for x in range(ox, ox + 7):
    for z in range(oz, oz + 7):
      _set(v, x, oy, z, YELLOW if (x + z) % 2 else BLUE)
  for y in range(oy + 1, oy + 4):
    for x in range(ox, ox + 7):
      for z in range(oz, oz + 7):
        if x in (ox, ox + 6) or z in (oz, oz + 6):
          _set(v, x, y, z, SAND)
  _set(v, ox + 3, oy + 1, oz + 3, CHISELED)
  _set(v, ox + 3, oy + 1, oz + 4, BED)
  _set(v, ox + 1, oy + 2, oz + 1, TORCH)
  return v


def _generate_epic_bases_tomb_lava_parkour() -> np.ndarray:
  LAVA, STONE, BRICK, COBBLE = _b("lava"), _b("stone"), _b("stone_bricks"), _b("cobblestone")
  v = _tomb_v()
  ox, oz, oy = 11, 12, 1
  for x in range(ox, ox + 10):
    for z in range(oz, oz + 8):
      _set(v, x, oy - 1, z, LAVA)
  for i, (px, pz) in enumerate(((ox + 1, oz + 1), (ox + 4, oz + 3), (ox + 7, oz + 5), (ox + 3, oz + 6))):
    for y in range(oy, oy + 2 + i):
      _set(v, px, y, pz, STONE if i % 2 else BRICK)
  _set(v, ox + 8, oy + 1, oz + 2, COBBLE)
  return v


def _generate_epic_bases_tomb_defensive_maze() -> np.ndarray:
  BRICK, MOSSY, COBBLE, TORCH = _b("stone_bricks"), _b("mossy_stone_bricks"), _b("cobblestone"), _b("torch")
  v = _tomb_v()
  ox, oz, oy = 11, 11, 1
  walls = [
    (ox, oz, ox + 8, oz), (ox, oz + 8, ox + 8, oz + 8), (ox, oz, ox, oz + 8), (ox + 8, oz, ox + 8, oz + 8),
    (ox + 3, oz, ox + 3, oz + 5), (ox + 5, oz + 3, ox + 8, oz + 3), (ox, oz + 5, ox + 6, oz + 5),
  ]
  for x0, z0, x1, z1 in walls:
    for x in range(min(x0, x1), max(x0, x1) + 1):
      for z in range(min(z0, z1), max(z0, z1) + 1):
        for y in range(oy, oy + 3):
          _set(v, x, y, z, BRICK if (x + z) % 2 else MOSSY)
  _set(v, ox + 2, oy + 2, oz + 2, TORCH)
  _set(v, ox + 6, oy + 2, oz + 6, COBBLE)
  return v


def _generate_epic_bases_tomb_waterfall_exit() -> np.ndarray:
  WATER, SAND, GLASS, TORCH = _b("water"), _b("sandstone"), _b("blue_stained_glass"), _b("torch")
  v = _tomb_v()
  cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 7):
    _set(v, cx, y, cz, WATER)
    _set(v, cx - 1, y, cz, GLASS)
    _set(v, cx + 1, y, cz, GLASS)
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      _set(v, x, oy - 1, z, SAND)
      _set(v, x, oy, z, WATER if abs(x - cx) <= 1 and abs(z - cz) <= 1 else SAND)
  _set(v, cx + 2, oy + 3, cz, TORCH)
  return v


def _generate_epic_bases_tomb_entrance_atrium() -> np.ndarray:
  SAND, RED, WATER, BANNER, LANTERN = _b("sandstone"), _b("red_sandstone"), _b("water"), _b("blue_banner"), _b("lantern")
  v = _tomb_v()
  ox, oz, oy = 11, 12, 1
  for y in range(oy, oy + 6):
    for x in range(ox, ox + 10):
      _set(v, x, y, oz, RED if y > oy + 3 else SAND)
      _set(v, x, y, oz + 7, SAND)
  for x in range(ox + 2, ox + 8):
    for z in range(oz + 2, oz + 6):
      _set(v, x, oy, z, WATER)
  _set(v, ox + 2, oy + 5, oz + 1, BANNER)
  _set(v, ox + 7, oy + 5, oz + 1, BANNER)
  _set(v, ox + 5, oy + 4, oz + 6, LANTERN)
  return v


def _generate_epic_bases_tomb_daylight_doorway() -> np.ndarray:
  SAND, RED, PISTON, REPEATER, DUST, DAYLIGHT = (
    _b("sandstone"), _b("red_sandstone"), _b("sticky_piston"),
    _b("redstone_repeater"), _b("redstone_dust"), _b("daylight_detector"),
  )
  v = _tomb_v()
  ox, oz, oy = 13, 14, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 3):
      _set(v, x, oy, z, SAND)
  for x in range(ox + 1, ox + 5):
    _set(v, x, oy + 1, oz, PISTON)
    _set(v, x, oy + 2, oz, RED)
  for y in range(oy + 1, oy + 6):
    _set(v, ox + 5, y, oz + 1, REPEATER if y % 2 else DUST)
  _set(v, ox + 2, oy + 6, oz + 1, DAYLIGHT)
  return v


def _generate_epic_bases_tomb_ladder_parkour() -> np.ndarray:
  BRICK, LADDER, GLOW = _b("stone_bricks"), _b("ladder"), _b("glowstone")
  v = _tomb_v()
  cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 10):
    for x in range(cx - 1, cx + 2):
      for z in range(cz - 1, cz + 2):
        if x in (cx - 1, cx + 1) or z in (cz - 1, cz + 1):
          _set(v, x, y, z, BRICK)
  for y in range(oy + 1, oy + 9, 2):
    _set(v, cx + 1, y, cz, LADDER)
    _set(v, cx, y + 1, cz + 1, LADDER)
  _set(v, cx, oy + 5, cz, GLOW)
  return v


def _generate_epic_bases_tomb_indoor_farm() -> np.ndarray:
  WHEAT, FARM, WATER, SAND, ORANGE, TORCH = (
    _b("wheat"), _b("farmland"), _b("water"), _b("sandstone"), _b("orange_terracotta"), _b("torch"),
  )
  v = _tomb_v()
  ox, oz, oy = 13, 14, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 4):
      _set(v, x, oy - 1, z, SAND)
      _set(v, x, oy, z, FARM)
      _set(v, x, oy + 1, z, WHEAT)
  for z in range(oz, oz + 4):
    _set(v, ox + 2, oy, z, WATER)
  for x in range(ox, ox + 6):
    _set(v, x, oy + 2, oz - 1, ORANGE)
    _set(v, x, oy + 2, oz + 4, ORANGE)
  _set(v, ox + 5, oy + 2, oz + 2, TORCH)
  return v


def _lab_v():
  return _tomb_v()


def _generate_epic_bases_lab_floating_nether_portal() -> np.ndarray:
  OBS, NETH, PORTAL, PLANK, FENCE, LANTERN = _b("obsidian"), _b("netherrack"), _b("nether_portal"), _b("oak_planks"), _b("dark_oak_fence"), _b("lantern")
  v = _lab_v(); cx, cz, oy = 16, 16, 4
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      _set(v, x, oy - 1, z, PLANK)
  for y in range(oy, oy + 4):
    for x, z in ((cx - 1, cz - 1), (cx + 1, cz - 1), (cx - 1, cz + 1), (cx + 1, cz + 1)):
      _set(v, x, y, z, OBS)
  for y in range(oy + 1, oy + 3):
    _set(v, cx, y, cz, PORTAL)
  _set(v, cx - 2, oy, cz, NETH)
  _set(v, cx + 2, oy + 2, cz, LANTERN)
  for x in range(cx - 2, cx + 3):
    _set(v, x, oy, cz - 2, FENCE)
  return v


def _generate_epic_bases_lab_ballonet() -> np.ndarray:
  WHITE, BROWN, FENCE, CHAIN = _b("white_wool"), _b("brown_wool"), _b("oak_fence"), _b("chain")
  v = _lab_v(); cx, cz, oy = 16, 16, 6
  for y in range(oy, oy + 6):
    r = 3 - abs(y - oy - 3) // 2
    for x in range(cx - r, cx + r + 1):
      for z in range(cz - r, cz + r + 1):
        if abs(x - cx) + abs(z - cz) <= r + 1:
          _set(v, x, y, z, WHITE if (x + z + y) % 2 else BROWN)
  _set(v, cx, oy - 1, cz, CHAIN)
  _set(v, cx, oy - 2, cz, FENCE)
  return v


def _generate_epic_bases_lab_propeller() -> np.ndarray:
  TRAP, SLAB, IRON, FENCE, PLANK = _b("oak_trapdoor"), _b("oak_slab"), _b("iron_block"), _b("dark_oak_fence"), _b("oak_planks")
  v = _lab_v(); cx, cz, oy = 16, 16, 3
  _set(v, cx, oy, cz, IRON)
  for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    _set(v, cx + dx * 2, oy, cz + dz * 2, TRAP)
    _set(v, cx + dx, oy, cz + dz, SLAB)
  _set(v, cx, oy - 1, cz, PLANK)
  _set(v, cx + 2, oy + 1, cz, FENCE)
  return v


def _generate_epic_bases_lab_potions_tower() -> np.ndarray:
  WHITE, GREEN, LOG, GLASS, BREW, CAULDRON = _b("white_concrete"), _b("green_concrete"), _b("dark_oak_log"), _b("glass_pane"), _b("brewing_stand"), _b("cauldron")
  v = _lab_v(); ox, oz, oy = 14, 14, 1
  for y in range(oy, oy + 10):
    for x in range(ox, ox + 5):
      for z in range(oz, oz + 5):
        edge = x in (ox, ox + 4) or z in (oz, oz + 4)
        if edge:
          _set(v, x, y, z, LOG if y % 3 == 0 else WHITE)
        elif y == oy + 4:
          _set(v, x, y, z, GREEN)
  _set(v, ox + 2, oy + 5, oz, GLASS)
  _set(v, ox + 2, oy + 1, oz + 2, BREW)
  _set(v, ox + 3, oy + 1, oz + 2, CAULDRON)
  return v


def _generate_epic_bases_lab_windmill() -> np.ndarray:
  TRAP, FENCE, WHITE = _b("oak_trapdoor"), _b("oak_fence"), _b("white_concrete")
  v = _lab_v(); ox, oz, oy = 14, 15, 2
  for y in range(oy, oy + 5):
    _set(v, ox, y, oz, WHITE)
  for dx, dz in ((0, -2), (0, 2), (-2, 0), (2, 0)):
    _set(v, ox + dx, oy + 3, oz + dz, TRAP)
  _set(v, ox, oy + 3, oz, FENCE)
  return v


def _generate_epic_bases_lab_libratory() -> np.ndarray:
  SHELF, WHITE, STAIR, PLANK, TABLE, ANVIL, LANTERN = _b("bookshelf"), _b("white_concrete"), _b("dark_oak_stairs"), _b("dark_oak_planks"), _b("enchanting_table"), _b("anvil"), _b("lantern")
  v = _lab_v(); ox, oz, oy = 12, 12, 1
  for y in range(oy, oy + 5):
    for x in range(ox, ox + 8):
      for z in range(oz, oz + 6):
        edge = x in (ox, ox + 7) or z in (oz, oz + 5)
        if edge and y < oy + 4:
          _set(v, x, y, z, SHELF if y < oy + 3 else WHITE)
        elif y == oy + 4:
          _set(v, x, y, z, STAIR)
  _set(v, ox + 4, oy + 1, oz + 3, TABLE)
  _set(v, ox + 2, oy + 1, oz + 2, ANVIL)
  _set(v, ox + 6, oy + 3, oz + 3, LANTERN)
  return v


def _generate_epic_bases_lab_fumigation_chimney() -> np.ndarray:
  BRICK, WALL, FIRE, STAIR = _b("stone_bricks"), _b("cobblestone_wall"), _b("campfire"), _b("dark_oak_stairs")
  v = _lab_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 8):
    _set(v, cx, y, cz, BRICK)
    _set(v, cx + 1, y, cz, WALL)
  _set(v, cx, oy, cz, FIRE)
  _set(v, cx + 2, oy + 2, cz, STAIR)
  return v


def _generate_epic_bases_lab_giant_mushroom() -> np.ndarray:
  RED, WHITE, CONCRETE, PLANK = _b("red_mushroom_block"), _b("white_wool"), _b("white_concrete"), _b("dark_oak_planks")
  v = _lab_v(); cx, cz, oy = 16, 16, 1
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      _set(v, x, oy, z, PLANK)
  for y in range(oy + 1, oy + 4):
    r = 4 - (y - oy)
    for x in range(cx - r, cx + r + 1):
      for z in range(cz - r, cz + r + 1):
        if (x - cx) ** 2 + (z - cz) ** 2 <= r * r + 2:
          _set(v, x, y, z, RED if (x + z) % 3 else WHITE)
  _set(v, cx, oy + 4, cz, CONCRETE)
  return v


def _generate_epic_bases_lab_victorian_tower() -> np.ndarray:
  WHITE, LOG, STAIR, GLASS, GREEN, LANTERN, LADDER = _b("white_concrete"), _b("dark_oak_log"), _b("dark_oak_stairs"), _b("light_blue_stained_glass"), _b("green_concrete"), _b("lantern"), _b("ladder")
  v = _lab_v(); ox, oz, oy = 13, 13, 1
  for y in range(oy, oy + 12):
    for x in range(ox, ox + 6):
      for z in range(oz, oz + 6):
        edge = x in (ox, ox + 5) or z in (oz, oz + 5)
        if edge:
          _set(v, x, y, z, LOG if y % 2 == 0 else WHITE)
    if y in (oy + 3, oy + 7, oy + 11):
      for x in range(ox, ox + 6):
        for z in range(oz, oz + 6):
          _set(v, x, y, z, STAIR)
  _set(v, ox + 3, oy + 5, oz, GLASS)
  _set(v, ox + 2, oy + 1, oz + 3, LADDER)
  _set(v, ox + 4, oy + 8, oz + 4, LANTERN)
  _set(v, ox + 1, oy, oz + 1, GREEN)
  return v


def _generate_epic_bases_airship_express() -> np.ndarray:
  GREEN, PLANK, FENCE, STAIR, BARREL = _b("green_concrete"), _b("dark_oak_planks"), _b("oak_fence"), _b("spruce_stairs"), _b("barrel")
  v = _lab_v(); ox, oz, oy = 12, 14, 3
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 4):
      _set(v, x, oy, z, PLANK)
      _set(v, x, oy - 1, z, GREEN)
  for x in range(ox, ox + 8, 2):
    _set(v, x, oy + 1, oz - 1, FENCE)
    _set(v, x, oy + 1, oz + 4, FENCE)
  _set(v, ox + 1, oy + 1, oz + 2, STAIR)
  _set(v, ox + 6, oy + 1, oz + 1, BARREL)
  return v


def _generate_epic_bases_airship_engine_furnace() -> np.ndarray:
  STONE, FIRE, TRAP, LEVER, IRON = _b("stone_bricks"), _b("campfire"), _b("oak_trapdoor"), _b("lever"), _b("iron_block")
  v = _lab_v(); cx, cz, oy = 16, 16, 2
  for x in range(cx - 1, cx + 2):
    for z in range(cz - 1, cz + 2):
      _set(v, x, oy - 1, z, STONE)
  _set(v, cx, oy, cz, FIRE)
  _set(v, cx, oy + 1, cz, TRAP)
  _set(v, cx + 1, oy + 1, cz, LEVER)
  _set(v, cx - 1, oy, cz, IRON)
  return v


def _generate_epic_bases_airship_quarterdeck() -> np.ndarray:
  PLANK, LECTERN, FENCE, LANTERN = _b("dark_oak_planks"), _b("lectern"), _b("oak_fence"), _b("lantern")
  v = _lab_v(); ox, oz, oy = 14, 14, 3
  for x in range(ox, ox + 4):
    for z in range(oz, oz + 3):
      _set(v, x, oy, z, PLANK)
  _set(v, ox + 2, oy + 1, oz + 1, LECTERN)
  for x in range(ox, ox + 4):
    _set(v, x, oy + 1, oz, FENCE)
  _set(v, ox + 3, oy + 2, oz + 2, LANTERN)
  return v


def _generate_epic_bases_airship_balloon() -> np.ndarray:
  WHITE, GOLD, TRAP, SLAB, FENCE, CHAIN = _b("white_wool"), _b("yellow_wool"), _b("oak_trapdoor"), _b("oak_slab"), _b("oak_fence"), _b("chain")
  v = _lab_v(); cx, cz, oy = 16, 16, 8
  for y in range(oy, oy + 6):
    r = 3 - abs(y - oy - 3) // 2
    for x in range(cx - r, cx + r + 1):
      for z in range(cz - r, cz + r + 1):
        if abs(x - cx) + abs(z - cz) <= r + 1:
          _set(v, x, y, z, WHITE if (x + y) % 2 else GOLD)
  _set(v, cx, oy - 1, cz, CHAIN)
  _set(v, cx + 2, oy + 2, cz, TRAP)
  _set(v, cx - 2, oy + 3, cz, SLAB)
  _set(v, cx, oy - 2, cz, FENCE)
  return v


def _generate_epic_bases_airship_storage_hold() -> np.ndarray:
  PLANK, CHEST, LANTERN, GREEN, TRAP = _b("dark_oak_planks"), _b("chest"), _b("lantern"), _b("green_concrete"), _b("oak_trapdoor")
  v = _lab_v(); ox, oz, oy = 13, 13, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 4):
      _set(v, x, oy, z, PLANK)
      _set(v, x, oy - 1, z, GREEN)
  _set(v, ox + 2, oy, oz + 2, CHEST)
  _set(v, ox + 3, oy, oz + 2, CHEST)
  _set(v, ox + 4, oy + 1, oz + 1, LANTERN)
  _set(v, ox + 1, oy + 1, oz, TRAP)
  return v


def _generate_epic_bases_airship_propeller() -> np.ndarray:
  WOOL, ANVIL, TRAP, BUTTON = _b("white_wool"), _b("anvil"), _b("oak_trapdoor"), _b("stone_button")
  v = _lab_v(); cx, cz, oy = 16, 16, 4
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      if abs(x - cx) + abs(z - cz) <= 2:
        _set(v, x, oy, z, WOOL)
  _set(v, cx, oy + 1, cz, ANVIL)
  for dx, dz in ((2, 0), (-2, 0), (0, 2), (0, -2)):
    _set(v, cx + dx, oy, cz + dz, TRAP)
    _set(v, cx + dx // 2, oy, cz + dz // 2, BUTTON)
  return v


def _estate_v():
  return _lab_v()


def _generate_epic_bases_estate_grand_dome() -> np.ndarray:
  PRISM, DPRISM, QUARTZ, GLASS, LANTERN, WATER = _b("prismarine"), _b("dark_prismarine"), _b("quartz_block"), _b("glass_pane"), _b("sea_lantern"), _b("water")
  v = _estate_v(); cx, cz, oy = 16, 16, 4
  for y in range(oy, oy + 6):
    r = 5 - abs(y - oy - 3)
    for x in range(cx - r, cx + r + 1):
      for z in range(cz - r, cz + r + 1):
        if (x - cx) ** 2 + (z - cz) ** 2 <= r * r + 2:
          _set(v, x, y, z, GLASS if (x + z) % 2 else PRISM)
  for x in range(cx - 4, cx + 5):
    _set(v, x, oy - 1, cz, DPRISM)
  _set(v, cx, oy + 2, cz, LANTERN)
  _set(v, cx + 3, oy, cz + 3, WATER)
  return v


def _generate_epic_bases_estate_stained_glass_wall() -> np.ndarray:
  PRISM, DPRISM, GLASS, PANE, QUARTZ = _b("prismarine"), _b("dark_prismarine"), _b("glass"), _b("glass_pane"), _b("quartz_block")
  v = _estate_v(); ox, oz, oy = 14, 15, 1
  for y in range(oy, oy + 9):
    for x in range(ox, ox + 6):
      _set(v, x, y, oz, PRISM if x in (ox, ox + 5) else GLASS)
      _set(v, x, y, oz + 1, PANE if y > oy + 1 else QUARTZ)
  for x in range(ox, ox + 6):
    _set(v, x, oy + 9, oz, DPRISM)
  return v


def _generate_epic_bases_estate_transfer_tunnel() -> np.ndarray:
  PRISM, GLASS, LANTERN, WATER = _b("prismarine"), _b("glass"), _b("sea_lantern"), _b("water")
  v = _estate_v(); ox, oz, oy = 11, 15, 3
  for x in range(ox, ox + 10):
    for z in range(oz, oz + 3):
      _set(v, x, oy, z, PRISM)
      _set(v, x, oy + 1, z, GLASS if z == oz + 1 else PRISM)
      _set(v, x, oy + 2, z, PRISM)
  _set(v, ox + 5, oy + 1, oz + 1, LANTERN)
  _set(v, ox + 2, oy, oz + 1, WATER)
  return v


def _generate_epic_bases_estate_observation_glass() -> np.ndarray:
  PRISM, DPRISM, GLASS, WATER, KELP = _b("prismarine"), _b("dark_prismarine"), _b("glass"), _b("water"), _b("kelp")
  v = _estate_v(); ox, oz, oy = 14, 15, 2
  for y in range(oy, oy + 3):
    _set(v, ox, y, oz, PRISM)
    _set(v, ox + 1, y, oz, DPRISM)
    _set(v, ox + 2, y, oz, PRISM)
  for y in range(oy, oy + 3):
    _set(v, ox + 1, y, oz + 1, GLASS)
  _set(v, ox + 1, oy - 1, oz + 2, WATER)
  _set(v, ox + 3, oy, oz + 2, KELP)
  return v


def _generate_epic_bases_estate_kelp_garden() -> np.ndarray:
  KELP, SAND, WATER, SEAGRASS, PRISM = _b("kelp"), _b("sand"), _b("water"), _b("seagrass"), _b("prismarine")
  v = _estate_v(); ox, oz, oy = 11, 11, 1
  for x in range(ox, ox + 10):
    for z in range(oz, oz + 8):
      _set(v, x, oy - 1, z, SAND)
      _set(v, x, oy, z, WATER)
  for x in range(ox + 1, ox + 9, 2):
    for z in range(oz + 1, oz + 7, 2):
      for y in range(oy, oy + 4):
        _set(v, x, y, z, KELP)
      _set(v, x, oy, z + 1, SEAGRASS)
  _set(v, ox + 4, oy + 1, oz + 3, PRISM)
  return v


def _generate_epic_bases_estate_skylight_tower() -> np.ndarray:
  PRISM, GLASS, LANTERN = _b("prismarine"), _b("glass"), _b("sea_lantern")
  v = _estate_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 11):
    for x in range(cx - 1, cx + 2):
      for z in range(cz - 1, cz + 2):
        if x in (cx - 1, cx + 1) or z in (cz - 1, cz + 1):
          _set(v, x, y, z, PRISM)
  for x in range(cx - 1, cx + 2):
    for z in range(cz - 1, cz + 2):
      _set(v, x, oy + 11, z, GLASS)
  _set(v, cx, oy + 5, cz, LANTERN)
  return v


def _generate_epic_bases_estate_deco_archway() -> np.ndarray:
  PRISM, QUARTZ, STAIR, PANE = _b("prismarine"), _b("quartz_block"), _b("quartz_stairs"), _b("glass_pane")
  v = _estate_v(); ox, oz, oy = 14, 14, 1
  for y in range(oy, oy + 7):
    _set(v, ox, y, oz, PRISM)
    _set(v, ox + 4, y, oz, PRISM)
  for y in range(oy + 2, oy + 6):
    _set(v, ox + 1, y, oz + 1, AIR)
    _set(v, ox + 2, y, oz + 1, AIR)
    _set(v, ox + 3, y, oz + 1, AIR)
  for x in range(ox, ox + 5):
    _set(v, x, oy + 7, oz, STAIR)
    _set(v, x, oy, oz + 1, QUARTZ)
  _set(v, ox + 2, oy + 3, oz, PANE)
  return v


def _generate_epic_bases_estate_deco_tower() -> np.ndarray:
  PRISM, DPRISM, QUARTZ, PANE, LANTERN = _b("prismarine"), _b("dark_prismarine"), _b("quartz_block"), _b("glass_pane"), _b("sea_lantern")
  v = _estate_v(); ox, oz, oy = 13, 13, 1
  for y in range(oy, oy + 12):
    for x in range(ox, ox + 6):
      for z in range(oz, oz + 6):
        edge = x in (ox, ox + 5) or z in (oz, oz + 5)
        if edge:
          _set(v, x, y, z, PRISM if y % 2 else DPRISM)
        elif x == ox + 2 and y in (oy + 2, oy + 5, oy + 8):
          _set(v, x, y, z + 2, PANE)
    if y % 4 == 0:
      for x in range(ox + 1, ox + 5):
        _set(v, x, y, oz + 1, QUARTZ)
  _set(v, ox + 3, oy + 1, oz + 3, LANTERN)
  return v


def _generate_epic_bases_estate_aquarium_lounge() -> np.ndarray:
  PRISM, BLUE, WHITE, STAIR, GLASS = _b("prismarine"), _b("blue_terracotta"), _b("white_terracotta"), _b("oak_stairs"), _b("glass")
  v = _estate_v(); ox, oz, oy = 12, 12, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 6):
      _set(v, x, oy, z, BLUE if (x + z) % 2 else WHITE)
  for y in range(oy + 1, oy + 4):
    for x in range(ox, ox + 8):
      for z in range(oz, oz + 6):
        if x in (ox, ox + 7) or z in (oz, oz + 5):
          _set(v, x, y, z, PRISM if y < oy + 3 else GLASS)
  _set(v, ox + 2, oy + 1, oz + 2, STAIR)
  _set(v, ox + 3, oy + 1, oz + 2, STAIR)
  return v


def _generate_epic_bases_estate_coral_garden() -> np.ndarray:
  BRAIN, TUBE, HORN, FIRE, SEAGRASS, PRISM, WATER = (
    _b("brain_coral_block"), _b("tube_coral_block"), _b("horn_coral_block"),
    _b("fire_coral_block"), _b("seagrass"), _b("prismarine"), _b("water"),
  )
  v = _estate_v(); ox, oz, oy = 12, 12, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 6):
      _set(v, x, oy - 1, z, PRISM)
      _set(v, x, oy, z, WATER)
  for x, z, coral in ((ox + 1, oz + 1, BRAIN), (ox + 4, oz + 2, TUBE), (ox + 6, oz + 4, HORN), (ox + 2, oz + 4, FIRE)):
    _set(v, x, oy + 1, z, coral)
    _set(v, x, oy, z + 1, SEAGRASS)
  return v


def _generate_epic_bases_estate_drowned_farm() -> np.ndarray:
  MAGMA, EGG, TRAP, GLASS, WATER, RAIL, HOPPER, CHEST, TORCH = (
    _b("magma_block"), _b("turtle_egg"), _b("oak_trapdoor"), _b("glass"),
    _b("water"), _b("powered_rail"), _b("hopper"), _b("chest"), _b("redstone_torch"),
  )
  v = _estate_v(); cx, cz, oy = 16, 16, 1
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      _set(v, x, oy - 1, z, MAGMA if abs(x - cx) + abs(z - cz) >= 2 else TRAP)
  for y in range(oy, oy + 8):
    for x in range(cx - 2, cx + 3):
      for z in range(cz - 2, cz + 3):
        if x in (cx - 2, cx + 2) or z in (cz - 2, cz + 2):
          _set(v, x, y, z, GLASS)
        else:
          _set(v, x, y, z, WATER)
  _set(v, cx, oy + 6, cz, EGG)
  _set(v, cx + 1, oy + 6, cz, EGG)
  _set(v, cx, oy - 2, cz, HOPPER)
  _set(v, cx, oy - 3, cz, CHEST)
  _set(v, cx + 2, oy - 2, cz, RAIL)
  _set(v, cx + 2, oy - 2, cz + 1, TORCH)
  return v


def _exchange_v():
  return _estate_v()


def _generate_epic_bases_exchange_support_platform() -> np.ndarray:
  OAK, SPRUCE, FENCE, STONE, MOSS, LANTERN = _b("oak_planks"), _b("spruce_planks"), _b("oak_fence"), _b("stone_bricks"), _b("mossy_stone_bricks"), _b("lantern")
  v = _exchange_v(); ox, oz, oy = 12, 14, 4
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 4):
      _set(v, x, oy, z, OAK if (x + z) % 2 else SPRUCE)
  for y in range(oy - 3, oy):
    _set(v, ox, y, oz + 2, STONE if y % 2 else MOSS)
  _set(v, ox + 5, oy + 1, oz + 1, FENCE)
  _set(v, ox + 3, oy + 1, oz + 2, LANTERN)
  return v


def _generate_epic_bases_exchange_eternal_flame() -> np.ndarray:
  STONE, NETH, FIRE, FENCE = _b("stone_bricks"), _b("netherrack"), _b("fire"), _b("oak_fence")
  v = _exchange_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 7):
    _set(v, cx, y, cz, STONE)
    _set(v, cx + 1, y, cz, FENCE if y > oy + 3 else STONE)
  _set(v, cx, oy + 7, cz, NETH)
  _set(v, cx, oy + 8, cz, FIRE)
  return v


def _generate_epic_bases_exchange_redstone_altar() -> np.ndarray:
  STONE, MOSS, RED, CHISELED = _b("stone_bricks"), _b("mossy_stone_bricks"), _b("redstone_block"), _b("chiseled_stone_bricks")
  v = _exchange_v(); cx, cz, oy = 16, 16, 1
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      _set(v, x, oy, z, MOSS if (x + z) % 2 else STONE)
  _set(v, cx, oy + 1, cz, RED)
  for x in (cx - 1, cx + 1):
    _set(v, x, oy + 1, cz, CHISELED)
  return v


def _generate_epic_bases_exchange_remnant_memorial() -> np.ndarray:
  STONE, SKULL, STAIR, VINE = _b("stone_bricks"), _b("skeleton_skull"), _b("stone_brick_stairs"), _b("vine")
  v = _exchange_v(); cx, cz, oy = 16, 16, 1
  _set(v, cx, oy, cz, STONE)
  _set(v, cx, oy + 1, cz, STAIR)
  _set(v, cx, oy + 2, cz, SKULL)
  _set(v, cx + 1, oy + 1, cz, VINE)
  return v


def _generate_epic_bases_exchange_lily_pad_path() -> np.ndarray:
  LILY, WATER, FENCE, LEAVES = _b("lily_pad"), _b("water"), _b("oak_fence"), _b("jungle_leaves")
  v = _exchange_v(); ox, oz, oy = 12, 15, 1
  for x in range(ox, ox + 8):
    _set(v, x, oy - 1, oz + 1, WATER)
    if x % 2 == 0:
      _set(v, x, oy, oz + 1, LILY)
  _set(v, ox - 1, oy + 1, oz, FENCE)
  _set(v, ox + 8, oy + 2, oz + 2, LEAVES)
  return v


def _generate_epic_bases_exchange_end_stepwell() -> np.ndarray:
  STONE, MOSS, WATER, FRAME, END, PURPUR = _b("stone_bricks"), _b("mossy_stone_bricks"), _b("water"), _b("end_portal_frame"), _b("end_stone_bricks"), _b("purpur_block")
  v = _exchange_v(); cx, cz, oy = 16, 16, 6
  for y in range(oy, oy - 5, -1):
    r = 3 + (oy - y) // 2
    for x in range(cx - r, cx + r + 1):
      for z in range(cz - r, cz + r + 1):
        if abs(x - cx) + abs(z - cz) <= r:
          _set(v, x, y, z, STONE if y % 2 else MOSS)
  for y in range(oy - 6, oy - 3, -1):
    _set(v, cx, y, cz, WATER)
  for dx, dz in ((0, -1), (0, 1), (-1, 0), (1, 0)):
    _set(v, cx + dx, oy - 7, cz + dz, FRAME)
  _set(v, cx, oy - 7, cz, END)
  _set(v, cx + 2, oy - 6, cz + 2, PURPUR)
  return v


def _generate_epic_bases_exchange_jungle_statue() -> np.ndarray:
  STONE, MOSS, COBBLE, VINE = _b("stone_bricks"), _b("mossy_stone_bricks"), _b("cobblestone"), _b("vine")
  v = _exchange_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 5):
    _set(v, cx, y, cz, STONE if y < oy + 3 else MOSS)
    _set(v, cx - 1, y, cz, COBBLE if y % 2 else MOSS)
    _set(v, cx + 1, y, cz, COBBLE)
  _set(v, cx, oy + 5, cz, MOSS)
  _set(v, cx + 1, oy + 2, cz, VINE)
  return v


def _generate_epic_bases_exchange_jungle_cabin() -> np.ndarray:
  OLOG, SLOG, ALOG, PLANK, HAY, FENCE, LANTERN = _b("oak_log"), _b("spruce_log"), _b("acacia_log"), _b("oak_planks"), _b("hay_block"), _b("oak_fence"), _b("lantern")
  v = _exchange_v(); ox, oz, oy = 13, 13, 4
  for y in range(oy - 3, oy):
    _set(v, ox, y, oz, OLOG)
    _set(v, ox + 5, y, oz + 4, SLOG)
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 5):
      _set(v, x, oy, z, PLANK)
      if x == ox + 3:
        _set(v, x, oy + 1, z, ALOG if z % 2 else OLOG)
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 5):
      _set(v, x, oy + 4, z, HAY)
  _set(v, ox + 2, oy + 2, oz + 4, LANTERN)
  _set(v, ox, oy + 1, oz, FENCE)
  return v


def _generate_epic_bases_exchange_stilt_house() -> np.ndarray:
  PLANK, FENCE, HAY, LADDER, COMPOST, LANTERN = _b("oak_planks"), _b("oak_fence"), _b("hay_block"), _b("ladder"), _b("composter"), _b("lantern")
  v = _exchange_v(); ox, oz, oy = 14, 14, 1
  for y in range(oy, oy + 5):
    for px, pz in ((ox, oz), (ox + 4, oz), (ox, oz + 4), (ox + 4, oz + 4)):
      _set(v, px, y, pz, FENCE)
  for x in range(ox, ox + 5):
    for z in range(oz, oz + 5):
      _set(v, x, oy + 5, z, PLANK)
  for x in range(ox, ox + 5):
    _set(v, x, oy + 8, oz + 2, HAY)
  _set(v, ox + 2, oy + 6, oz + 2, LADDER)
  _set(v, ox + 1, oy + 6, oz + 1, COMPOST)
  _set(v, ox + 3, oy + 7, oz + 3, LANTERN)
  return v


def _generate_epic_bases_exchange_streetlight() -> np.ndarray:
  COBBLE, WALL, LANTERN, FENCE = _b("cobblestone"), _b("stone_brick_wall"), _b("lantern"), _b("oak_fence")
  v = _exchange_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 3):
    _set(v, cx, y, cz, COBBLE)
    _set(v, cx + 1, y, cz, WALL)
  _set(v, cx, oy + 3, cz, LANTERN)
  _set(v, cx + 1, oy + 2, cz, FENCE)
  return v


def _generate_epic_bases_exchange_market_stall() -> np.ndarray:
  OAK, SPRUCE, CART, CHEST, LANTERN, FENCE = _b("oak_planks"), _b("spruce_planks"), _b("cartography_table"), _b("chest"), _b("lantern"), _b("oak_fence")
  v = _exchange_v(); ox, oz, oy = 14, 14, 2
  for x in range(ox, ox + 4):
    _set(v, x, oy, oz, OAK)
    _set(v, x, oy + 2, oz, SPRUCE)
    _set(v, x, oy + 1, oz, FENCE)
  _set(v, ox + 1, oy + 1, oz + 1, CART)
  _set(v, ox + 2, oy + 1, oz + 1, CHEST)
  _set(v, ox + 3, oy + 2, oz + 1, LANTERN)
  return v


def _generate_epic_bases_exchange_aerial_walkway() -> np.ndarray:
  PLANK, FENCE, LANTERN, LEAVES, VINE = _b("oak_planks"), _b("oak_fence"), _b("lantern"), _b("jungle_leaves"), _b("vine")
  v = _exchange_v(); ox, oz, oy = 11, 15, 5
  for x in range(ox, ox + 10):
    for z in range(oz, oz + 3):
      _set(v, x, oy, z, PLANK)
      if z == oz:
        _set(v, x, oy + 1, z, FENCE)
      if z == oz + 2:
        _set(v, x, oy + 1, z, FENCE)
  _set(v, ox + 3, oy + 2, oz + 1, LANTERN)
  _set(v, ox + 7, oy + 3, oz + 2, LEAVES)
  _set(v, ox + 9, oy + 1, oz, VINE)
  return v


def _generate_epic_bases_exchange_tiered_garden() -> np.ndarray:
  HAY, WHEAT, CARROT, PLANK, FENCE, FLOWER = _b("hay_block"), _b("wheat"), _b("carrots"), _b("oak_planks"), _b("oak_fence"), _b("dandelion")
  v = _exchange_v(); ox, oz, oy = 12, 12, 1
  for tier, (yoff, size) in enumerate(((0, 6), (1, 4), (2, 2))):
    for x in range(ox + 3 - tier, ox + 3 - tier + size):
      for z in range(oz + 2 - tier, oz + 2 - tier + size):
        _set(v, x, oy + yoff, z, HAY if tier == 0 else PLANK)
        if tier < 2:
          _set(v, x, oy + yoff + 1, z, WHEAT if (x + z) % 2 else CARROT)
  _set(v, ox + 1, oy + 1, oz + 5, FENCE)
  _set(v, ox + 6, oy + 2, oz + 1, FLOWER)
  return v


def _generate_epic_bases_exchange_cryptic_floor() -> np.ndarray:
  BLUE, WHITE, LBLUE, STONE, CHISELED = _b("blue_terracotta"), _b("white_terracotta"), _b("light_blue_terracotta"), _b("stone_bricks"), _b("chiseled_stone_bricks")
  v = _exchange_v(); ox, oz, oy = 13, 13, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 6):
      pat = (x + z) % 3
      _set(v, x, oy, z, BLUE if pat == 0 else WHITE if pat == 1 else LBLUE)
  for x in (ox, ox + 5):
    for z in range(oz, oz + 6):
      _set(v, x, oy + 1, z, STONE)
  _set(v, ox + 3, oy + 1, oz + 3, CHISELED)
  return v


def _cube_v():
  return _exchange_v()


def _generate_epic_bases_cube_force_field_maw() -> np.ndarray:
  PURPLE, PANE, OBS, WHITE, RED, SEA = _b("purple_stained_glass"), _b("purple_stained_glass_pane"), _b("obsidian"), _b("white_concrete"), _b("red_nether_bricks"), _b("sea_lantern")
  v = _cube_v(); ox, oz, oy = 14, 15, 1
  for y in range(oy, oy + 7):
    _set(v, ox, y, oz, OBS)
    _set(v, ox + 3, y, oz, OBS)
    _set(v, ox + 1, y, oz, PURPLE if y % 2 else PANE)
    _set(v, ox + 2, y, oz, PURPLE)
  for y in range(oy, oy + 8):
    _set(v, ox - 1, y, oz, WHITE if y % 2 else RED)
    _set(v, ox + 4, y, oz, WHITE)
  _set(v, ox + 2, oy + 5, oz + 1, SEA)
  return v


def _generate_epic_bases_cube_radiant_beacon() -> np.ndarray:
  ORANGE, GLOW, LAVA, OBS, RED = _b("orange_stained_glass"), _b("glowstone"), _b("lava"), _b("obsidian"), _b("red_nether_bricks")
  v = _cube_v(); cx, cz, oy = 16, 16, 1
  for x in range(cx - 3, cx + 4):
    for z in range(cz - 3, cz + 4):
      _set(v, x, oy, z, ORANGE if (x + z) % 2 else GLOW)
      _set(v, x, oy - 1, z, OBS if (x + z) % 3 else RED)
  _set(v, cx, oy + 1, cz, LAVA)
  return v


def _generate_epic_bases_cube_overgrown_tower() -> np.ndarray:
  STONE, MOSS, VINE, LEAVES, COBBLE = _b("stone_bricks"), _b("mossy_stone_bricks"), _b("vine"), _b("oak_leaves"), _b("cobblestone")
  v = _cube_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 10):
    for x in range(cx - 1, cx + 2):
      for z in range(cz - 1, cz + 2):
        _set(v, x, y, z, MOSS if y % 2 else STONE)
  for y in range(oy + 3, oy + 9):
    _set(v, cx + 2, y, cz, VINE)
    _set(v, cx - 1, y, cz + 1, LEAVES)
  _set(v, cx, oy - 1, cz, COBBLE)
  return v


def _generate_epic_bases_cube_crumbled_ruins() -> np.ndarray:
  RED, MOSS, COBBLE, GRAVEL, VINE = _b("red_terracotta"), _b("mossy_cobblestone"), _b("cobblestone"), _b("gravel"), _b("vine")
  v = _cube_v(); ox, oz, oy = 12, 13, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 6):
      _set(v, x, oy, z, GRAVEL if (x + z) % 3 == 0 else COBBLE)
      if (x + z) % 2 == 0:
        _set(v, x, oy + 1, z, RED)
      if x % 3 == 0:
        _set(v, x, oy + 2, z, MOSS)
  _set(v, ox + 2, oy + 1, oz + 4, VINE)
  return v


def _generate_epic_bases_cube_testing_lab() -> np.ndarray:
  WHITE, DIORITE, BARS, PURPLE, POL = _b("white_concrete"), _b("diorite"), _b("iron_bars"), _b("purple_stained_glass"), _b("polished_diorite")
  v = _cube_v(); ox, oz, oy = 12, 12, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 6):
      _set(v, x, oy, z, POL)
      for y in range(oy + 1, oy + 4):
        edge = x in (ox, ox + 7) or z in (oz, oz + 5)
        _set(v, x, y, z, WHITE if edge else DIORITE)
  for cx, cz in ((ox + 2, oz + 2), (ox + 5, oz + 3)):
    for y in range(oy + 1, oy + 3):
      _set(v, cx, y, cz, BARS)
    _set(v, cx, oy + 2, cz + 1, PURPLE)
  return v


def _generate_epic_bases_cube_mob_museum() -> np.ndarray:
  WHITE, BARS, PANE, POL, SEA = _b("white_concrete"), _b("iron_bars"), _b("purple_stained_glass_pane"), _b("polished_diorite"), _b("sea_lantern")
  v = _cube_v(); ox, oz, oy = 11, 11, 1
  for x in range(ox, ox + 10):
    for z in range(oz, oz + 8):
      _set(v, x, oy, z, POL)
  for x in range(ox + 1, ox + 9, 2):
    for z in range(oz + 1, oz + 7, 2):
      for y in range(oy + 1, oy + 3):
        _set(v, x, y, z, BARS)
      _set(v, x, oy + 2, z, PANE)
      _set(v, x, oy + 1, z, WHITE)
  _set(v, ox + 5, oy + 3, oz + 4, SEA)
  return v


def _generate_epic_bases_cube_circuit_wall() -> np.ndarray:
  RED, NETH, BLACK, GRAY = _b("red_nether_bricks"), _b("nether_bricks"), _b("black_concrete"), _b("gray_concrete")
  v = _cube_v(); ox, oz, oy = 12, 15, 1
  for y in range(oy, oy + 4):
    for x in range(ox, ox + 8):
      _set(v, x, y, oz, RED if y % 2 else NETH)
      _set(v, x, y, oz + 1, BLACK if x % 2 else GRAY)
  return v


def _generate_epic_bases_cube_core_engine() -> np.ndarray:
  OBS, RED, PANE, LAVA, GLASS, GLOW = _b("obsidian"), _b("red_nether_bricks"), _b("purple_stained_glass_pane"), _b("lava"), _b("glass"), _b("glowstone")
  v = _cube_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 10):
    r = 3 - abs(y - oy - 5) // 3
    for x in range(cx - r, cx + r + 1):
      for z in range(cz - r, cz + r + 1):
        if abs(x - cx) + abs(z - cz) <= r + 1:
          _set(v, x, y, z, OBS if y < oy + 7 else RED)
          if y == oy + 4 and x == cx:
            _set(v, x, y, z + 1, PANE)
  _set(v, cx, oy + 3, cz, GLASS)
  _set(v, cx, oy + 4, cz, LAVA)
  _set(v, cx + 2, oy + 8, cz, GLOW)
  return v


def _generate_epic_bases_cube_lava_curtain() -> np.ndarray:
  PANE, GLASS, LAVA, OBS, BARS = _b("glass_pane"), _b("glass"), _b("lava"), _b("obsidian"), _b("iron_bars")
  v = _cube_v(); ox, oz, oy = 15, 15, 1
  for y in range(oy, oy + 5):
    _set(v, ox, y, oz, PANE)
    _set(v, ox + 1, y, oz, LAVA if y < oy + 4 else GLASS)
    _set(v, ox + 2, y, oz, PANE)
    _set(v, ox, y, oz + 1, OBS)
  _set(v, ox + 1, oy + 2, oz + 1, BARS)
  return v


def _generate_epic_bases_cube_reinforced_shell() -> np.ndarray:
  OBS, IRON, CRY, BLACK = _b("obsidian"), _b("iron_block"), _b("crying_obsidian"), _b("black_concrete")
  v = _cube_v(); cx, cz, oy = 16, 16, 2
  for y in range(oy, oy + 5):
    for x in range(cx - 2, cx + 3):
      for z in range(cz - 2, cz + 3):
        edge = x in (cx - 2, cx + 2) or z in (cz - 2, cz + 2)
        if edge:
          _set(v, x, y, z, OBS if (x + z + y) % 2 else IRON)
        elif y == oy:
          _set(v, x, y, z, BLACK)
        else:
          _set(v, x, y, z, CRY if (x + y) % 2 else AIR)
  return v


def _generate_epic_bases_cube_automatic_doorway() -> np.ndarray:
  QUARTZ, PISTON, REP, DUST, TORCH, PLATE, STAIR = _b("quartz_block"), _b("sticky_piston"), _b("redstone_repeater"), _b("redstone_dust"), _b("redstone_torch"), _b("stone_pressure_plate"), _b("quartz_stairs")
  v = _cube_v(); ox, oz, oy = 12, 14, 1
  for x in range(ox, ox + 8):
    _set(v, x, oy, oz, QUARTZ)
    _set(v, x, oy + 3, oz, QUARTZ)
  for x in range(ox + 1, ox + 7):
    _set(v, x, oy + 1, oz, PISTON)
    _set(v, x, oy + 2, oz, QUARTZ)
  _set(v, ox + 1, oy, oz + 1, PLATE)
  _set(v, ox + 6, oy, oz + 1, PLATE)
  for i, x in enumerate(range(ox, ox + 5)):
    _set(v, x, oy - 1, oz + 1, REP)
    _set(v, x, oy - 1, oz + 2, DUST)
  _set(v, ox + 4, oy - 1, oz, TORCH)
  _set(v, ox + 3, oy + 4, oz, STAIR)
  return v


def _generate_epic_bases_cube_futuristic_streetlight() -> np.ndarray:
  OBS, GLOW, FENCE, BLACK, SEA = _b("obsidian"), _b("glowstone"), _b("warped_fence"), _b("black_concrete"), _b("sea_lantern")
  v = _cube_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 5):
    _set(v, cx, y, cz, OBS)
  _set(v, cx, oy + 5, cz, GLOW)
  _set(v, cx, oy + 6, cz, SEA)
  _set(v, cx + 1, oy + 3, cz, FENCE)
  _set(v, cx, oy - 1, cz, BLACK)
  return v


def _generate_epic_bases_cube_floating_engine() -> np.ndarray:
  OBS, PURPLE, GLOW, ROD, WHITE = _b("obsidian"), _b("purple_stained_glass"), _b("glowstone"), _b("end_rod"), _b("white_concrete")
  v = _cube_v(); cx, cz, oy = 16, 16, 6
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      for y in range(oy, oy + 3):
        edge = x in (cx - 2, cx + 2) or z in (cz - 2, cz + 2)
        if edge:
          _set(v, x, y, z, OBS if y < oy + 2 else PURPLE)
        else:
          _set(v, x, y, z, GLOW if y == oy + 1 else AIR)
  _set(v, cx, oy + 3, cz, ROD)
  _set(v, cx, oy - 1, cz, ROD)
  _set(v, cx, oy - 2, cz, WHITE)
  return v


def _ice_v():
  return _cube_v()


def _generate_epic_bases_ice_golem_outpost() -> np.ndarray:
  ICE, BLUE, QUARTZ, SNOW, SPRUCE = _b("packed_ice"), _b("blue_ice"), _b("quartz_block"), _b("snow_block"), _b("spruce_planks")
  v = _ice_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 8):
    for x in range(cx - 1, cx + 2):
      for z in range(cz - 1, cz + 2):
        edge = x in (cx - 1, cx + 1) or z in (cz - 1, cz + 1)
        _set(v, x, y, z, ICE if edge else QUARTZ if y < oy + 5 else BLUE)
  _set(v, cx, oy + 8, cz, SNOW)
  _set(v, cx + 2, oy + 3, cz, SPRUCE)
  return v


def _generate_epic_bases_ice_frozen_forum() -> np.ndarray:
  QUARTZ, PILLAR, ICE, SPRUCE, STAIR, BLUE = _b("quartz_block"), _b("quartz_pillar"), _b("packed_ice"), _b("spruce_planks"), _b("spruce_stairs"), _b("blue_ice")
  v = _ice_v(); ox, oz, oy = 11, 12, 1
  for x in range(ox, ox + 10):
    for z in range(oz, oz + 8):
      _set(v, x, oy, z, ICE)
      for y in range(oy + 1, oy + 5):
        wall = x in (ox, ox + 9) or z in (oz, oz + 7)
        _set(v, x, y, z, QUARTZ if wall else AIR)
  for x in (ox + 2, ox + 7):
    for y in range(oy + 1, oy + 6):
      _set(v, x, y, oz + 1, PILLAR)
      _set(v, x, y, oz + 6, PILLAR)
  for x in range(ox, ox + 10):
    for z in range(oz, oz + 8):
      _set(v, x, oy + 5, z, SPRUCE)
      _set(v, x, oy + 6, z, STAIR)
  _set(v, ox + 5, oy + 4, oz + 4, BLUE)
  return v


def _generate_epic_bases_ice_amphitheater() -> np.ndarray:
  ICE, STAIR, SNOW, SLAB = _b("packed_ice"), _b("quartz_stairs"), _b("snow_block"), _b("spruce_slab")
  v = _ice_v(); ox, oz, oy = 11, 12, 1
  for tier in range(4):
    y = oy + tier
    w = 8 - tier
    for x in range(ox + tier, ox + tier + w):
      for z in range(oz + tier, oz + tier + 6):
        _set(v, x, y, z, STAIR if x == ox + tier else ICE if z == oz + tier else SLAB)
  _set(v, ox + 4, oy, oz + 3, SNOW)
  return v


def _generate_epic_bases_ice_quartz_bridge() -> np.ndarray:
  QUARTZ, STAIR, SLAB, ICE, BLUE = _b("quartz_block"), _b("quartz_stairs"), _b("quartz_slab"), _b("packed_ice"), _b("blue_ice")
  v = _ice_v(); ox, oz, oy = 10, 15, 8
  for x in range(ox, ox + 12):
    _set(v, x, oy, oz, QUARTZ)
    _set(v, x, oy, oz + 1, SLAB)
    if x % 3 == 0:
      _set(v, x, oy + 1, oz, STAIR)
      _set(v, x, oy + 2, oz - 1, QUARTZ)
  for x in range(ox, ox + 12):
    _set(v, x, oy - 1, oz, ICE)
    _set(v, x, oy - 2, oz, BLUE)
  return v


def _generate_epic_bases_ice_signaling_beacon() -> np.ndarray:
  PILLAR, ICE, BLUE, SEA, QUARTZ = _b("quartz_pillar"), _b("packed_ice"), _b("blue_ice"), _b("sea_lantern"), _b("quartz_block")
  v = _ice_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 11):
    _set(v, cx, y, cz, PILLAR if y % 2 else ICE)
    if y > oy + 2:
      _set(v, cx + 1, y, cz, BLUE)
      _set(v, cx - 1, y, cz, BLUE)
  _set(v, cx, oy + 11, cz, SEA)
  _set(v, cx, oy - 1, cz, QUARTZ)
  return v


def _generate_epic_bases_ice_mountain_docks() -> np.ndarray:
  SPRUCE, FENCE, ICE, WATER, GRASS, TRAP = _b("spruce_planks"), _b("oak_fence"), _b("packed_ice"), _b("water"), _b("grass_block"), _b("spruce_trapdoor")
  v = _ice_v(); ox, oz, oy = 12, 13, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 4):
      _set(v, x, oy - 1, z, ICE)
      _set(v, x, oy - 2, z, WATER if z < oz + 2 else ICE)
  for x in range(ox, ox + 6):
    _set(v, x, oy, oz + 2, SPRUCE)
    _set(v, x, oy, oz + 3, FENCE)
  _set(v, ox + 7, oy, oz + 1, GRASS)
  _set(v, ox + 1, oy, oz + 4, TRAP)
  return v


def _generate_epic_bases_ice_ragged_spire() -> np.ndarray:
  QUARTZ, BLUE, ICE, STAIR, FENCE = _b("quartz_block"), _b("blue_ice"), _b("packed_ice"), _b("quartz_stairs"), _b("birch_fence")
  v = _ice_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 12):
    _set(v, cx, y, cz, QUARTZ)
    ang = y * 2
    _set(v, cx + 1 + (ang % 2), y, cz + 1, BLUE)
    _set(v, cx - 1, y, cz + (ang % 2), ICE)
    _set(v, cx + (ang % 2), y, cz - 1, STAIR)
    if y > oy + 8:
      _set(v, cx, y + 1, cz, FENCE)
  return v


def _generate_epic_bases_ice_frozen_tree() -> np.ndarray:
  LEAVES, LOG, SNOW, ICE, GRASS = _b("oak_leaves"), _b("birch_log"), _b("snow_block"), _b("packed_ice"), _b("grass_block")
  v = _ice_v(); cx, cz, oy = 16, 16, 1
  _set(v, cx, oy, cz, GRASS)
  _set(v, cx, oy + 1, cz, LOG)
  _set(v, cx, oy + 2, cz, LOG)
  for dx, dz in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1)):
    _set(v, cx + dx, oy + 3, cz + dz, LEAVES)
  _set(v, cx, oy + 4, cz, LEAVES)
  for x in range(cx - 1, cx + 2):
    for z in range(cz - 1, cz + 2):
      _set(v, x, oy - 1, z, ICE)
      if (x, z) != (cx, cz):
        _set(v, x, oy, z, SNOW)
  return v


def _generate_epic_bases_ice_elven_outpost() -> np.ndarray:
  QUARTZ, STAIR, FENCE, TRAP, ICE, BLUE = _b("quartz_block"), _b("birch_stairs"), _b("birch_fence"), _b("birch_trapdoor"), _b("packed_ice"), _b("blue_ice")
  v = _ice_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 9):
    for x in range(cx - 1, cx + 2):
      for z in range(cz - 1, cz + 2):
        edge = x in (cx - 1, cx + 1) or z in (cz - 1, cz + 1)
        _set(v, x, y, z, QUARTZ if edge else ICE)
  for y in (oy + 3, oy + 6):
    for x in range(cx - 2, cx + 3):
      _set(v, x, y, cz + 2, FENCE)
      _set(v, x, y, cz - 2, STAIR)
  _set(v, cx, oy + 9, cz, BLUE)
  _set(v, cx + 1, oy + 2, cz, TRAP)
  return v


def _generate_epic_bases_ice_alcove_passage() -> np.ndarray:
  QUARTZ, STAIR, BLUE, ICE, TRAP = _b("quartz_block"), _b("quartz_stairs"), _b("blue_ice"), _b("packed_ice"), _b("birch_trapdoor")
  v = _ice_v(); ox, oz, oy = 14, 15, 1
  for y in range(oy, oy + 4):
    _set(v, ox, y, oz, QUARTZ)
    _set(v, ox + 3, y, oz, QUARTZ)
    _set(v, ox + 1, y, oz, AIR if y < oy + 3 else TRAP)
    _set(v, ox + 2, y, oz, AIR if y < oy + 3 else TRAP)
  for x in range(ox, ox + 4):
    _set(v, x, oy + 3, oz, BLUE)
    _set(v, x, oy + 4, oz, STAIR)
  _set(v, ox - 1, oy, oz, ICE)
  _set(v, ox + 4, oy, oz, ICE)
  return v


def _generate_epic_bases_ice_spike() -> np.ndarray:
  PACK, BLUE, ICE_B, SNOW, WATER = _b("packed_ice"), _b("blue_ice"), _b("ice"), _b("snow_block"), _b("water")
  v = _ice_v(); cx, cz, oy = 16, 16, 1
  _set(v, cx, oy + 6, cz, WATER)
  for h, block in enumerate((ICE_B, PACK, PACK, BLUE, BLUE, PACK)):
    r = max(0, 2 - h // 2)
    for dx in range(-r, r + 1):
      for dz in range(-r, r + 1):
        if abs(dx) + abs(dz) <= r:
          _set(v, cx + dx, oy + h, cz + dz, block)
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      _set(v, x, oy - 1, z, SNOW)
  return v


def _generate_epic_bases_ice_soul_lantern() -> np.ndarray:
  LANTERN, TORCH, ICE, QUARTZ, CHAIN = _b("soul_lantern"), _b("soul_torch"), _b("packed_ice"), _b("quartz_block"), _b("chain")
  v = _ice_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 3):
    _set(v, cx, y, cz, QUARTZ)
  _set(v, cx, oy + 3, cz, CHAIN)
  _set(v, cx, oy + 4, cz, LANTERN)
  _set(v, cx + 1, oy + 1, cz, TORCH)
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 1, cz + 2):
      _set(v, x, oy - 1, z, ICE)
  return v


def _generate_epic_bases_ice_open_gazebo() -> np.ndarray:
  SPRUCE, STAIR, ICE, BLUE, FENCE, SLAB = _b("spruce_planks"), _b("spruce_stairs"), _b("packed_ice"), _b("blue_ice"), _b("oak_fence"), _b("spruce_slab")
  v = _ice_v(); ox, oz, oy = 12, 12, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 8):
      _set(v, x, oy, z, ICE if (x + z) % 2 else BLUE)
  for x in (ox, ox + 7):
    for y in range(oy + 1, oy + 5):
      _set(v, x, y, oz + 3, SPRUCE)
      _set(v, x, y, oz + 4, FENCE)
  for z in range(oz, oz + 8):
    _set(v, ox + 3, oy + 5, z, SLAB)
    _set(v, ox + 4, oy + 5, z, STAIR)
  return v


def _generate_epic_bases_ice_snowman_farm() -> np.ndarray:
  SNOW, DISP, PISTON, REP, DUST, GLASS, SPRUCE, PUMP = _b("snow_block"), _b("dispenser"), _b("sticky_piston"), _b("redstone_repeater"), _b("redstone_dust"), _b("glass"), _b("spruce_planks"), _b("carved_pumpkin")
  v = _ice_v(); ox, oz, oy = 13, 14, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 4):
      _set(v, x, oy, z, SPRUCE if x == ox else SNOW if z == oz else GLASS if x == ox + 3 else SPRUCE)
  _set(v, ox + 3, oy + 1, oz + 1, DISP)
  _set(v, ox + 3, oy + 1, oz + 2, PISTON)
  _set(v, ox + 2, oy + 1, oz + 2, SNOW)
  _set(v, ox + 3, oy + 2, oz + 2, SNOW)
  _set(v, ox + 3, oy + 3, oz + 2, PUMP)
  for i, x in enumerate(range(ox, ox + 4)):
    _set(v, x, oy - 1, oz, REP)
    _set(v, x, oy - 1, oz + 1, DUST)
  _set(v, ox + 5, oy + 1, oz + 2, PISTON)
  return v


def _hoard_v():
  return _ice_v()


def _generate_epic_bases_hoard_treasure_trove() -> np.ndarray:
  GOLD, BONE, DEEP, POL, CHEST = _b("gold_block"), _b("bone_block"), _b("deepslate_bricks"), _b("polished_deepslate"), _b("chest")
  v = _hoard_v(); ox, oz, oy = 12, 13, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 6):
      _set(v, x, oy, z, DEEP)
      h = 1 + (x + z) % 3
      for y in range(oy + 1, oy + 1 + h):
        _set(v, x, y, z, GOLD if (x + z + y) % 2 else BONE)
  _set(v, ox + 4, oy + 4, oz + 3, BONE)
  _set(v, ox + 3, oy + 3, oz + 2, BONE)
  _set(v, ox + 5, oy + 2, oz + 4, CHEST)
  _set(v, ox + 4, oy, oz + 3, POL)
  return v


def _generate_epic_bases_hoard_super_statue() -> np.ndarray:
  STONE, CHISEL, BEACON, IRON, GOLD = _b("stone_bricks"), _b("chiseled_stone_bricks"), _b("beacon"), _b("iron_block"), _b("gold_block")
  v = _hoard_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 12):
    for x in range(cx - 1, cx + 2):
      for z in range(cz - 1, cz + 2):
        _set(v, x, y, z, CHISEL if y % 3 == 0 else STONE)
  _set(v, cx, oy + 12, cz, BEACON)
  _set(v, cx + 2, oy + 6, cz, GOLD)
  _set(v, cx - 2, oy + 5, cz, IRON)
  _set(v, cx, oy + 8, cz, BEACON)
  return v


def _generate_epic_bases_hoard_coal_mine_rail() -> np.ndarray:
  RAIL, POWER, COAL, DEEP, CHEST = _b("rail"), _b("powered_rail"), _b("coal_block"), _b("deepslate_bricks"), _b("chest")
  v = _hoard_v(); ox, oz, oy = 11, 15, 1
  for x in range(ox, ox + 10):
    _set(v, x, oy, oz, DEEP)
    _set(v, x, oy + 1, oz, POWER if x % 3 == 0 else RAIL)
    _set(v, x, oy, oz + 1, COAL if x % 2 else DEEP)
  _set(v, ox, oy + 2, oz, CHEST)
  _set(v, ox + 9, oy + 2, oz, COAL)
  return v


def _generate_epic_bases_hoard_magma_lava_lake() -> np.ndarray:
  LAVA, MAGMA, DEEP, COBBLE, BLACK = _b("lava"), _b("magma_block"), _b("deepslate"), _b("cobblestone"), _b("blackstone")
  v = _hoard_v(); ox, oz, oy = 11, 12, 1
  for x in range(ox, ox + 10):
    for z in range(oz, oz + 8):
      edge = x in (ox, ox + 9) or z in (oz, oz + 7)
      _set(v, x, oy, z, COBBLE if edge else LAVA if (x + z) % 3 else MAGMA)
      _set(v, x, oy - 1, z, DEEP if edge else BLACK)
  return v


def _generate_epic_bases_hoard_lava_pathway() -> np.ndarray:
  COBBLE, SLAB, STAIR, LAVA, DEEP = _b("cobblestone"), _b("stone_brick_slab"), _b("stone_brick_stairs"), _b("lava"), _b("deepslate_bricks")
  v = _hoard_v(); ox, oz, oy = 11, 15, 1
  for x in range(ox, ox + 10):
    _set(v, x, oy, oz, COBBLE)
    _set(v, x, oy + 1, oz, SLAB)
    if x % 4 == 0:
      _set(v, x, oy + 2, oz, STAIR)
    _set(v, x, oy - 1, oz + 1, LAVA)
    _set(v, x, oy - 1, oz - 1, LAVA)
  _set(v, ox - 1, oy, oz, DEEP)
  return v


def _generate_epic_bases_hoard_support_pillar() -> np.ndarray:
  STONE, CHISEL, STAIR, DEEP, POL = _b("stone_bricks"), _b("chiseled_stone_bricks"), _b("stone_brick_stairs"), _b("deepslate_bricks"), _b("polished_deepslate")
  v = _hoard_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 10):
    for x in range(cx - 1, cx + 2):
      for z in range(cz - 1, cz + 2):
        edge = x in (cx - 1, cx + 1) or z in (cz - 1, cz + 1)
        _set(v, x, y, z, CHISEL if edge and y % 2 else STONE if edge else POL)
    if y % 3 == 0:
      _set(v, cx + 2, y, cz, STAIR)
      _set(v, cx - 2, y, cz, STAIR)
  _set(v, cx, oy - 1, cz, DEEP)
  return v


def _generate_epic_bases_hoard_lava_fountain() -> np.ndarray:
  STONE, LAVA, GLASS, LEVER, COBBLE = _b("stone_bricks"), _b("lava"), _b("glass"), _b("lever"), _b("cobblestone")
  v = _hoard_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 7):
    _set(v, cx, y, cz, STONE)
    _set(v, cx + 1, y, cz, STONE if y < oy + 5 else GLASS)
    _set(v, cx - 1, y, cz, STONE)
    if y > oy + 2:
      _set(v, cx, y, cz + 1, LAVA)
  for x in range(cx - 1, cx + 2):
    for z in range(cz - 1, cz + 2):
      _set(v, x, oy - 1, z, COBBLE)
      _set(v, x, oy, z, LAVA if x == cx and z == cz else COBBLE)
  _set(v, cx + 2, oy + 1, cz, LEVER)
  return v


def _generate_epic_bases_hoard_debris_awning() -> np.ndarray:
  STONE, STAIR, SLAB, COBBLE, OAK = _b("stone_bricks"), _b("stone_brick_stairs"), _b("stone_brick_slab"), _b("cobblestone"), _b("oak_planks")
  v = _hoard_v(); ox, oz, oy = 13, 14, 1
  for x in range(ox, ox + 6):
    _set(v, x, oy, oz, COBBLE)
    _set(v, x, oy + 1, oz + 1, STONE)
    _set(v, x, oy + 2, oz + 2, SLAB)
    if x == ox or x == ox + 5:
      _set(v, x, oy + 1, oz, STAIR)
  for x in range(ox + 1, ox + 5):
    for z in range(oz, oz + 3):
      _set(v, x, oy, z, OAK)
  return v


def _generate_epic_bases_hoard_swamp_pool() -> np.ndarray:
  WATER, MOSS, VINE, DEEP, LILY = _b("water"), _b("mossy_cobblestone"), _b("vine"), _b("deepslate"), _b("lily_pad")
  v = _hoard_v(); ox, oz, oy = 13, 13, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 6):
      edge = x in (ox, ox + 5) or z in (oz, oz + 5)
      _set(v, x, oy - 1, z, MOSS if edge else DEEP)
      _set(v, x, oy, z, WATER if not edge else MOSS)
  _set(v, ox + 2, oy, oz + 2, LILY)
  _set(v, ox + 4, oy + 1, oz + 1, VINE)
  return v


def _generate_epic_bases_hoard_cavern_hall() -> np.ndarray:
  DEEP, COBBLE, STAIR, STONE, TORCH = _b("deepslate"), _b("cobblestone"), _b("stone_brick_stairs"), _b("stone_bricks"), _b("torch")
  v = _hoard_v(); ox, oz, oy = 10, 11, 1
  for x in range(ox, ox + 12):
    for z in range(oz, oz + 10):
      _set(v, x, oy, z, COBBLE if (x + z) % 2 else DEEP)
      wall = x in (ox, ox + 11) or z in (oz, oz + 9)
      for y in range(oy + 1, oy + 6):
        if wall:
          _set(v, x, y, z, STONE)
      _set(v, x, oy + 6, z, STAIR)
  _set(v, ox + 6, oy + 3, oz + 5, TORCH)
  return v


def _generate_epic_bases_hoard_mine_shaft() -> np.ndarray:
  STAIR, RAIL, POWER, CHEST, DEEP, TORCH = _b("oak_stairs"), _b("rail"), _b("powered_rail"), _b("chest"), _b("deepslate_bricks"), _b("torch")
  v = _hoard_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 9):
    _set(v, cx, y, cz, STAIR)
    _set(v, cx + 1, y, cz, RAIL if y % 2 else POWER)
    if y % 3 == 0:
      _set(v, cx - 1, y, cz, DEEP)
  _set(v, cx, oy + 9, cz, CHEST)
  _set(v, cx + 2, oy + 4, cz, TORCH)
  return v


def _generate_epic_bases_hoard_lava_lighting() -> np.ndarray:
  GLASS, LAVA, STONE, DEEP, BARS = _b("glass"), _b("lava"), _b("stone_bricks"), _b("deepslate_bricks"), _b("iron_bars")
  v = _hoard_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 6):
    _set(v, cx, y, cz, LAVA)
    _set(v, cx + 1, y, cz, GLASS)
    _set(v, cx - 1, y, cz, GLASS)
    _set(v, cx, y, cz + 1, GLASS)
  _set(v, cx, oy - 1, cz, STONE)
  _set(v, cx, oy + 6, cz, BARS)
  _set(v, cx + 1, oy - 1, cz, DEEP)
  return v


def _generate_epic_bases_hoard_underground_chamber() -> np.ndarray:
  STONE, OAK, STAIR, TORCH, DEEP = _b("stone_bricks"), _b("oak_planks"), _b("oak_stairs"), _b("torch"), _b("deepslate_bricks")
  v = _hoard_v(); cx, cz, oy = 16, 16, 1
  for tier in range(3):
    y = oy + tier * 2
    r = 4 - tier
    for x in range(cx - r, cx + r + 1):
      for z in range(cz - r, cz + r + 1):
        if abs(x - cx) + abs(z - cz) <= r + 1:
          edge = abs(x - cx) + abs(z - cz) >= r
          _set(v, x, y, z, STONE if edge else OAK if tier == 1 else DEEP)
          if edge and tier == 0:
            _set(v, x, y + 1, z, STAIR)
  _set(v, cx, oy + 4, cz, TORCH)
  _set(v, cx + 3, oy + 2, cz, OAK)
  return v


def _generate_epic_bases_hoard_auto_smelter() -> np.ndarray:
  FURN, HOP, CHEST, STONE, DEEP, COAL = _b("furnace"), _b("hopper"), _b("chest"), _b("stone_bricks"), _b("deepslate_bricks"), _b("coal_block")
  v = _hoard_v(); ox, oz, oy = 10, 14, 1
  for i, x in enumerate(range(ox, ox + 6)):
    _set(v, x, oy, oz, STONE)
    _set(v, x, oy + 1, oz, FURN)
    _set(v, x, oy + 2, oz, HOP)
    _set(v, x, oy + 3, oz, CHEST if i % 2 else HOP)
  for x in range(ox, ox + 6):
    _set(v, x, oy + 1, oz + 1, HOP)
  _set(v, ox - 1, oy + 4, oz, CHEST)
  _set(v, ox + 6, oy + 4, oz, CHEST)
  _set(v, ox - 1, oy + 5, oz, COAL)
  _set(v, ox + 6, oy + 5, oz, DEEP)
  return v


def _generate_epic_bases_hoard_enchant_setup() -> np.ndarray:
  TABLE, BOOK, LAVA, STONE, ANVIL = _b("enchanting_table"), _b("bookshelf"), _b("lava"), _b("stone_bricks"), _b("anvil")
  v = _hoard_v(); cx, cz, oy = 16, 16, 1
  for dx in (-2, -1, 0, 1, 2):
    for dz in (-2, -1, 0, 1, 2):
      if abs(dx) == 2 or abs(dz) == 2:
        _set(v, cx + dx, oy + 1, cz + dz, BOOK)
      _set(v, cx + dx, oy, cz + dz, STONE)
  _set(v, cx, oy + 1, cz, TABLE)
  _set(v, cx + 2, oy + 1, cz, ANVIL)
  _set(v, cx - 2, oy, cz + 2, LAVA)
  _set(v, cx + 2, oy, cz - 2, LAVA)
  return v


def _sweet_v():
  return _hoard_v()


def _generate_epic_bases_sweet_flavor_factory() -> np.ndarray:
  YEL, WHT, SPRUCE, OAK, PINK = _b("yellow_concrete"), _b("white_concrete"), _b("spruce_planks"), _b("oak_planks"), _b("pink_terracotta")
  v = _sweet_v(); ox, oz, oy = 12, 13, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 6):
      _set(v, x, oy, z, OAK)
      for y in range(oy + 1, oy + 5):
        wall = x in (ox, ox + 7) or z in (oz, oz + 5)
        if wall:
          _set(v, x, y, z, YEL if (x + y) % 2 else WHT)
      _set(v, x, oy + 5, z, SPRUCE)
  _set(v, ox + 4, oy + 2, oz + 3, PINK)
  return v


def _generate_epic_bases_sweet_chocolate_bridge() -> np.ndarray:
  BRN, TERR, DARK, FENCE, WHT = _b("brown_concrete"), _b("brown_terracotta"), _b("dark_oak_planks"), _b("oak_fence"), _b("white_concrete")
  v = _sweet_v(); ox, oz, oy = 11, 15, 6
  for x in range(ox, ox + 10):
    _set(v, x, oy, oz, BRN)
    _set(v, x, oy, oz + 1, TERR)
    if x % 3 == 0:
      _set(v, x, oy + 1, oz, DARK)
      _set(v, x, oy + 2, oz - 1, BRN)
    _set(v, x, oy - 1, oz, WHT)
  _set(v, ox, oy + 1, oz + 1, FENCE)
  return v


def _generate_epic_bases_sweet_mushroom_meadow() -> np.ndarray:
  RED, PINK, MYCE, GRASS, WHT = _b("red_mushroom_block"), _b("pink_terracotta"), _b("mycelium"), _b("grass_block"), _b("white_concrete")
  v = _sweet_v(); ox, oz, oy = 12, 12, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 8):
      _set(v, x, oy - 1, z, MYCE if (x + z) % 2 else GRASS)
  for cx, cz, h in ((ox + 2, oz + 2, 4), (ox + 5, oz + 5, 5), (ox + 6, oz + 2, 3)):
    for y in range(oy, oy + h):
      _set(v, cx, y, cz, RED)
    _set(v, cx + 1, oy + h - 1, cz, PINK)
    _set(v, cx, oy + h, cz, WHT)
  return v


def _generate_epic_bases_sweet_jelly_castle() -> np.ndarray:
  ORG, YEL, GRAY, WHT, BLUE, SLIME = _b("orange_concrete"), _b("yellow_concrete"), _b("light_gray_concrete"), _b("white_concrete"), _b("blue_concrete"), _b("slime_block")
  v = _sweet_v(); ox, oz, oy = 11, 11, 1
  for x in range(ox, ox + 10):
    for z in range(oz, oz + 8):
      _set(v, x, oy, z, SLIME)
      for y in range(oy + 1, oy + 6):
        wall = x in (ox, ox + 9) or z in (oz, oz + 7)
        if wall:
          _set(v, x, y, z, GRAY if y < oy + 4 else WHT)
      _set(v, x, oy + 6, z, ORG if (x + z) % 2 else YEL)
  _set(v, ox + 5, oy + 3, oz, BLUE)
  _set(v, ox + 2, oy + 2, oz + 1, AIR)
  _set(v, ox + 7, oy + 2, oz + 5, AIR)
  return v


def _generate_epic_bases_sweet_slushie_tap() -> np.ndarray:
  BLUE_G, WATER, GRAY, WHT, BLUE = _b("light_blue_stained_glass"), _b("water"), _b("gray_concrete"), _b("white_concrete"), _b("blue_concrete")
  v = _sweet_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 5):
    _set(v, cx, y, cz, GRAY)
    _set(v, cx + 1, y, cz, BLUE_G if y < oy + 4 else WATER)
  for y in range(oy, oy + 3):
    _set(v, cx, oy + 5 - y, cz + 1, WATER)
  _set(v, cx - 1, oy, cz, WHT)
  _set(v, cx, oy + 5, cz, BLUE)
  return v


def _generate_epic_bases_sweet_rainbow_road() -> np.ndarray:
  colors = [_b("red_concrete"), _b("orange_concrete"), _b("yellow_concrete"), _b("lime_concrete"), _b("light_blue_concrete"), _b("purple_concrete")]
  v = _sweet_v(); ox, oz, oy = 10, 15, 1
  for i, x in enumerate(range(ox, ox + 12)):
    _set(v, x, oy, oz, colors[i % len(colors)])
    _set(v, x, oy, oz + 1, colors[(i + 1) % len(colors)])
    _set(v, x, oy, oz + 2, colors[(i + 2) % len(colors)])
  return v


def _generate_epic_bases_sweet_honey_moat() -> np.ndarray:
  YEL, ORG, HONEY, WHT, PINK = _b("yellow_concrete"), _b("orange_concrete"), _b("honey_block"), _b("white_concrete"), _b("pink_terracotta")
  v = _sweet_v(); cx, cz, oy = 16, 16, 1
  for x in range(cx - 4, cx + 5):
    for z in range(cz - 4, cz + 5):
      dist = abs(x - cx) + abs(z - cz)
      if 5 <= dist <= 7:
        _set(v, x, oy, z, HONEY if (x + z) % 2 else YEL)
      elif dist == 8:
        _set(v, x, oy, z, WHT if x % 2 else PINK)
      elif dist <= 4:
        _set(v, x, oy - 1, z, ORG)
  return v


def _generate_epic_bases_sweet_candy_cane_light() -> np.ndarray:
  RED, WHT, LANT, FENCE = _b("red_concrete"), _b("white_concrete"), _b("lantern"), _b("dark_oak_fence")
  v = _sweet_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 4):
    _set(v, cx, y, cz, RED if y % 2 else WHT)
  _set(v, cx, oy + 4, cz, FENCE)
  _set(v, cx, oy + 5, cz, LANT)
  _set(v, cx + 1, oy + 1, cz, WHT)
  return v


def _generate_epic_bases_sweet_doughnut_dorm() -> np.ndarray:
  BRN, WHT, GLASS, RED, YEL, LIME = _b("brown_concrete"), _b("white_concrete"), _b("light_blue_stained_glass"), _b("red_concrete"), _b("yellow_concrete"), _b("lime_concrete")
  v = _sweet_v(); cx, cz, oy = 16, 16, 1
  sprinkles = (RED, YEL, LIME, _b("pink_concrete"), _b("purple_concrete"))
  for x in range(cx - 3, cx + 4):
    for z in range(cz - 3, cz + 4):
      dist = ((x - cx) ** 2 + (z - cz) ** 2) ** 0.5
      if 2.5 <= dist <= 3.5:
        _set(v, x, oy, z, WHT)
        for y in range(oy + 1, oy + 4):
          _set(v, x, y, z, GLASS if y == oy + 2 else WHT)
        _set(v, x, oy + 4, z, BRN)
        _set(v, x, oy + 5, z, sprinkles[(x + z) % len(sprinkles)])
      elif dist <= 1.5:
        _set(v, x, oy, z, AIR)
  return v


def _generate_epic_bases_sweet_alpine_chalet() -> np.ndarray:
  SPRUCE, BLUE, WHT, RED, STAIR = _b("spruce_planks"), _b("blue_concrete"), _b("white_concrete"), _b("red_concrete"), _b("dark_oak_stairs")
  v = _sweet_v(); ox, oz, oy = 13, 14, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 5):
      _set(v, x, oy, z, SPRUCE)
      for y in range(oy + 1, oy + 4):
        wall = x in (ox, ox + 5) or z in (oz, oz + 4)
        if wall:
          _set(v, x, y, z, BLUE if y < oy + 3 else WHT)
      _set(v, x, oy + 4, z, STAIR)
  _set(v, ox, oy + 1, oz, RED)
  _set(v, ox + 5, oy + 1, oz + 4, RED)
  return v


def _generate_epic_bases_sweet_mushroom_tap() -> np.ndarray:
  RED, MYCE, WATER, BLUE, STONE = _b("red_mushroom_block"), _b("mycelium"), _b("water"), _b("light_blue_concrete"), _b("stone_bricks")
  v = _sweet_v(); cx, cz, oy = 16, 16, 1
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      _set(v, x, oy - 1, z, MYCE)
      if abs(x - cx) + abs(z - cz) <= 2:
        _set(v, x, oy, z, WATER if x == cx and z == cz else MYCE)
  for dx, dz in ((1, 1), (-1, 1), (1, -1)):
    for y in range(oy + 1, oy + 4):
      _set(v, cx + dx, y, cz + dz, RED)
  _set(v, cx, oy + 1, cz + 2, STONE)
  _set(v, cx, oy + 2, cz + 2, BLUE)
  return v


def _generate_epic_bases_sweet_lollipop_tower() -> np.ndarray:
  RED, WHT, PUR, PINK, ORG = _b("red_concrete"), _b("white_concrete"), _b("purple_concrete"), _b("pink_concrete"), _b("orange_concrete")
  v = _sweet_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 8):
    _set(v, cx, y, cz, RED if y % 2 else WHT)
    _set(v, cx + 1, y, cz, WHT if y % 2 else RED)
  for y in range(oy + 8, oy + 11):
    r = oy + 11 - y
    for dx in range(-r, r + 1):
      for dz in range(-r, r + 1):
        if abs(dx) + abs(dz) <= r:
          _set(v, cx + dx, y, cz + dz, PUR if (dx + dz) % 2 else PINK)
  _set(v, cx, oy - 1, cz, ORG)
  return v


def _generate_epic_bases_sweet_slime_carpet() -> np.ndarray:
  SLIME, PINK, BLUE, WHT, YEL = _b("slime_block"), _b("pink_carpet"), _b("light_blue_carpet"), _b("white_concrete"), _b("yellow_concrete")
  v = _sweet_v(); ox, oz, oy = 13, 13, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 6):
      for y in range(oy + 1, oy + 4):
        if x in (ox, ox + 5) or z in (oz, oz + 5):
          _set(v, x, y, z, YEL if y == oy + 3 else WHT)
      _set(v, x, oy, z, SLIME)
      _set(v, x, oy + 1, z, PINK if (x + z) % 2 else BLUE)
  return v


def _generate_epic_bases_sweet_candy_factory() -> np.ndarray:
  SPRUCE, YEL, CYAN, ORG, STAIR, BRICK = _b("spruce_planks"), _b("yellow_concrete"), _b("cyan_concrete"), _b("orange_concrete"), _b("dark_oak_stairs"), _b("brick")
  v = _sweet_v(); ox, oz, oy = 11, 11, 1
  for x in range(ox, ox + 10):
    for z in range(oz, oz + 8):
      _set(v, x, oy, z, BRICK)
      for y in range(oy + 1, oy + 6):
        wall = x in (ox, ox + 9) or z in (oz, oz + 7)
        if wall:
          _set(v, x, y, z, SPRUCE if y < oy + 4 else YEL)
        elif y < oy + 3:
          _set(v, x, y, z, CYAN if (x + z) % 2 else ORG)
      _set(v, x, oy + 6, z, STAIR)
  return v


def _generate_epic_bases_sweet_wheat_farm() -> np.ndarray:
  OAK, FARM, WHEAT, WATER, DISP, LEVER = _b("oak_planks"), _b("farmland"), _b("wheat"), _b("water"), _b("dispenser"), _b("lever")
  v = _sweet_v(); ox, oz, oy = 12, 14, 1
  for tier in range(3):
    y = oy + tier * 2
    for x in range(ox, ox + 8):
      _set(v, x, y, oz, OAK)
      _set(v, x, y + 1, oz + 1, FARM)
      _set(v, x, y + 2, oz + 1, WHEAT)
  _set(v, ox + 4, oy + 6, oz, DISP)
  _set(v, ox + 5, oy + 6, oz, LEVER)
  _set(v, ox + 3, oy + 5, oz + 1, WATER)
  return v


def _generate_epic_bases_sweet_sugarcane_farm() -> np.ndarray:
  CANE, WATER, PISTON, OBS, OAK, GLASS = _b("sugar_cane"), _b("water"), _b("piston"), _b("observer"), _b("oak_planks"), _b("glass")
  v = _sweet_v(); ox, oz, oy = 12, 14, 1
  for i, x in enumerate(range(ox, ox + 8, 2)):
    _set(v, x, oy, oz, WATER)
    for y in range(oy + 1, oy + 4):
      _set(v, x, y, oz, CANE)
    _set(v, x, oy + 4, oz, PISTON)
    _set(v, x, oy + 5, oz, OBS)
    _set(v, x, oy, oz + 1, GLASS if i % 2 else OAK)
  return v


def _generate_epic_bases_sweet_cuckoo_clock() -> np.ndarray:
  PINK, WHT, OAK, DARK, CLOCK = _b("pink_concrete"), _b("white_concrete"), _b("oak_planks"), _b("dark_oak_planks"), _b("clock")
  v = _sweet_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 5):
    _set(v, cx - 1, y, cz, PINK)
    _set(v, cx + 1, y, cz, PINK)
    _set(v, cx, y, cz, WHT if y < oy + 4 else OAK)
  _set(v, cx, oy + 3, cz, CLOCK)
  _set(v, cx, oy + 5, cz, DARK)
  return v


def _generate_epic_bases_sweet_chicken_coop() -> np.ndarray:
  GREEN, OAK, HAY, FENCE, GLASS, WHT = _b("green_carpet"), _b("oak_planks"), _b("hay_block"), _b("oak_fence"), _b("glass"), _b("white_concrete")
  v = _sweet_v(); ox, oz, oy = 13, 14, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 5):
      _set(v, x, oy, z, GREEN)
      for y in range(oy + 1, oy + 4):
        wall = x in (ox, ox + 5) or z in (oz, oz + 4)
        if wall:
          _set(v, x, y, z, OAK if y < oy + 3 else GLASS)
      _set(v, x, oy + 4, z, WHT)
  for x in range(ox + 1, ox + 5):
    _set(v, x, oy + 2, oz, HAY)
    _set(v, x, oy + 1, oz + 4, FENCE)
  return v


def _generate_epic_bases_sweet_factory_pipes() -> np.ndarray:
  GRAY, LIGHT, IRON, YEL, BRICK = _b("gray_concrete"), _b("light_gray_concrete"), _b("iron_block"), _b("yellow_concrete"), _b("brick")
  v = _sweet_v(); ox, oz, oy = 12, 14, 3
  for x in range(ox, ox + 8):
    _set(v, x, oy, oz, GRAY)
    _set(v, x, oy + 1, oz + 1, LIGHT)
    if x % 3 == 0:
      _set(v, x, oy + 2, oz, IRON)
      _set(v, x, oy, oz + 2, GRAY)
  _set(v, ox - 1, oy - 1, oz, BRICK)
  _set(v, ox + 8, oy, oz, YEL)
  return v


def _generate_epic_bases_sweet_cotton_candy_tree() -> np.ndarray:
  PINK, MAG, LOG, GRASS = _b("pink_concrete"), _b("magenta_concrete"), _b("birch_log"), _b("grass_block")
  v = _sweet_v(); cx, cz, oy = 16, 16, 1
  _set(v, cx, oy - 1, cz, GRASS)
  _set(v, cx, oy, cz, LOG)
  _set(v, cx, oy + 1, cz, LOG)
  for dx, dz in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)):
    _set(v, cx + dx, oy + 2, cz + dz, PINK if (dx + dz) % 2 else MAG)
  _set(v, cx, oy + 3, cz, MAG)
  return v


def _motel_v():
  return _sweet_v()


def _generate_epic_bases_motel_decrepit_wing() -> np.ndarray:
  CRIM, WARP, STAIR, STONE, MOSS = _b("crimson_planks"), _b("warped_planks"), _b("crimson_stairs"), _b("stone_bricks"), _b("mossy_stone_bricks")
  v = _motel_v(); ox, oz, oy = 13, 14, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 5):
      _set(v, x, oy, z, MOSS)
      for y in range(oy + 1, oy + 5):
        wall = x in (ox, ox + 5) or z in (oz, oz + 4)
        if wall:
          _set(v, x, y, z, CRIM if (x + y) % 2 else WARP)
      _set(v, x, oy + 5, z, STAIR)
  _set(v, ox + 3, oy + 2, oz + 2, STONE)
  return v


def _generate_epic_bases_motel_soul_lighting() -> np.ndarray:
  LANT, TORCH, SAND, STONE, CHAIN = _b("soul_lantern"), _b("soul_torch"), _b("soul_sand"), _b("stone_bricks"), _b("chain")
  v = _motel_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 3):
    _set(v, cx, y, cz, STONE)
  _set(v, cx, oy + 3, cz, CHAIN)
  _set(v, cx, oy + 4, cz, LANT)
  _set(v, cx + 1, oy + 1, cz, TORCH)
  _set(v, cx, oy - 1, cz, SAND)
  return v


def _generate_epic_bases_motel_bone_tree() -> np.ndarray:
  BONE, VINE, GRASS, MOSS = _b("bone_block"), _b("weeping_vines"), _b("grass_block"), _b("mossy_cobblestone")
  v = _motel_v(); cx, cz, oy = 16, 16, 1
  _set(v, cx, oy - 1, cz, MOSS)
  for y in range(oy, oy + 5):
    _set(v, cx, y, cz, BONE)
    _set(v, cx + 1, y, cz, BONE if y > oy + 2 else VINE)
  for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    _set(v, cx + dx, oy + 4, cz + dz, BONE)
    _set(v, cx + dx, oy + 3, cz + dz, VINE)
  _set(v, cx + 2, oy - 1, cz, GRASS)
  return v


def _generate_epic_bases_motel_hedge_maze() -> np.ndarray:
  LEAVES, SPRUCE, GRASS, DIRT = _b("oak_leaves"), _b("spruce_leaves"), _b("grass_block"), _b("coarse_dirt")
  v = _motel_v(); ox, oz, oy = 11, 11, 1
  for x in range(ox, ox + 10):
    for z in range(oz, oz + 10):
      _set(v, x, oy - 1, z, GRASS if (x + z) % 2 else DIRT)
      if (x % 2 == 0 and z % 3 != 0) or (z % 2 == 0 and x % 3 != 0):
        for y in range(oy, oy + 3):
          _set(v, x, y, z, LEAVES if y < oy + 2 else SPRUCE)
  return v


def _generate_epic_bases_motel_mortuary() -> np.ndarray:
  STONE, MOSS, CRACK, BARS, SOUL = _b("stone_bricks"), _b("mossy_stone_bricks"), _b("cracked_stone_bricks"), _b("iron_bars"), _b("soul_lantern")
  v = _motel_v(); ox, oz, oy = 13, 14, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 5):
      _set(v, x, oy, z, MOSS if (x + z) % 2 else STONE)
      for y in range(oy + 1, oy + 3):
        wall = x in (ox, ox + 5) or z in (oz, oz + 4)
        if wall:
          _set(v, x, y, z, CRACK if y == oy + 2 else STONE)
      _set(v, x, oy + 3, z, MOSS)
  _set(v, ox + 3, oy + 1, oz, BARS)
  _set(v, ox + 3, oy + 3, oz + 2, SOUL)
  return v


def _generate_epic_bases_motel_gothic_spire() -> np.ndarray:
  STONE, DEEP, CYAN, MAG, GLASS = _b("stone_bricks"), _b("deepslate_bricks"), _b("cyan_terracotta"), _b("magenta_terracotta"), _b("orange_stained_glass")
  v = _motel_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 12):
    for x in range(cx - 1, cx + 2):
      for z in range(cz - 1, cz + 2):
        edge = x in (cx - 1, cx + 1) or z in (cz - 1, cz + 1)
        if edge:
          _set(v, x, y, z, STONE if y < oy + 8 else DEEP)
        elif y % 3 == 0:
          _set(v, x, y, z, GLASS)
  _set(v, cx, oy + 12, cz, CYAN)
  _set(v, cx + 1, oy + 11, cz, MAG)
  return v


def _generate_epic_bases_motel_cobweb_hall() -> np.ndarray:
  WEB, BARS, STONE, MOSS, VINE = _b("cobweb"), _b("iron_bars"), _b("stone_bricks"), _b("mossy_stone_bricks"), _b("vine")
  v = _motel_v(); ox, oz, oy = 12, 15, 1
  for x in range(ox, ox + 8):
    _set(v, x, oy, oz, STONE)
    _set(v, x, oy + 1, oz, MOSS if x % 2 else STONE)
    _set(v, x, oy + 2, oz, WEB if x % 3 else BARS)
    if x % 4 == 0:
      _set(v, x, oy + 1, oz + 1, VINE)
  return v


def _generate_epic_bases_motel_graveyard_crypt() -> np.ndarray:
  STONE, MOSS, DOOR, CHISEL, BARS = _b("stone_bricks"), _b("mossy_stone_bricks"), _b("dark_oak_door"), _b("chiseled_stone_bricks"), _b("iron_bars")
  v = _motel_v(); ox, oz, oy = 14, 14, 1
  for x in range(ox, ox + 4):
    for z in range(oz, oz + 4):
      for y in range(oy, oy + 4):
        wall = x in (ox, ox + 3) or z in (oz, oz + 3)
        if wall:
          _set(v, x, y, z, CHISEL if y == oy + 3 else MOSS if (x + z) % 2 else STONE)
  _set(v, ox + 2, oy + 1, oz, DOOR)
  _set(v, ox + 1, oy + 2, oz + 2, BARS)
  return v


def _generate_epic_bases_motel_skeletal_stables() -> np.ndarray:
  STONE, PURPLE, BARS, FENCE, SOUL = _b("stone_bricks"), _b("purple_carpet"), _b("iron_bars"), _b("dark_oak_fence"), _b("soul_lantern")
  v = _motel_v(); ox, oz, oy = 12, 14, 1
  for x in range(ox, ox + 8):
    _set(v, x, oy, oz, STONE)
    _set(v, x, oy + 1, oz, BARS if x % 2 else FENCE)
    _set(v, x, oy + 2, oz, PURPLE)
    _set(v, x, oy + 3, oz, STONE)
  _set(v, ox + 4, oy + 3, oz + 1, SOUL)
  return v


def _generate_epic_bases_motel_wicked_tree() -> np.ndarray:
  LOG, WOOD, VINE, LEAVES, MOSS = _b("dark_oak_log"), _b("dark_oak_wood"), _b("vine"), _b("oak_leaves"), _b("mossy_cobblestone")
  v = _motel_v(); cx, cz, oy = 16, 16, 1
  _set(v, cx, oy - 1, cz, MOSS)
  for y in range(oy, oy + 4):
    _set(v, cx, y, cz, LOG)
    _set(v, cx + 1, y, cz, WOOD if y % 2 else VINE)
  for dx, dz in ((1, 1), (-1, 0), (0, -1)):
    _set(v, cx + dx, oy + 4, cz + dz, LEAVES)
  return v


def _generate_epic_bases_motel_prison_room() -> np.ndarray:
  BARS, PURPLE, STONE, DARK, CHAIN = _b("iron_bars"), _b("purple_carpet"), _b("stone_bricks"), _b("dark_oak_planks"), _b("chain")
  v = _motel_v(); ox, oz, oy = 13, 14, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 5):
      _set(v, x, oy, z, PURPLE)
      for y in range(oy + 1, oy + 4):
        wall = x in (ox, ox + 5) or z in (oz, oz + 4)
        _set(v, x, y, z, BARS if wall else STONE if y < oy + 3 else DARK)
  _set(v, ox + 3, oy + 2, oz, CHAIN)
  return v


def _generate_epic_bases_motel_swamp_foundation() -> np.ndarray:
  MOSS_C, MOSS_S, VINE, WATER, STONE = _b("mossy_cobblestone"), _b("mossy_stone_bricks"), _b("vine"), _b("water"), _b("stone_bricks")
  v = _motel_v(); ox, oz, oy = 12, 12, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 8):
      _set(v, x, oy - 1, z, WATER if (x + z) % 4 == 0 else MOSS_C)
      _set(v, x, oy, z, MOSS_S if x % 2 else STONE)
      if x % 3 == 0:
        _set(v, x, oy + 1, z, VINE)
  return v


def _generate_epic_bases_motel_potions_lab() -> np.ndarray:
  BREW, CHEST, WATER, STONE, CAUL, SOUL = _b("brewing_stand"), _b("chest"), _b("water"), _b("stone_bricks"), _b("cauldron"), _b("soul_lantern")
  v = _motel_v(); ox, oz, oy = 12, 14, 1
  for x in range(ox, ox + 8):
    _set(v, x, oy, oz, STONE)
    _set(v, x, oy + 1, oz, BREW if x % 2 else CHEST)
    _set(v, x, oy, oz + 1, WATER if ox + 1 <= x <= ox + 3 else STONE)
  _set(v, ox + 5, oy + 1, oz, CAUL)
  _set(v, ox + 7, oy + 2, oz, SOUL)
  return v


def _generate_epic_bases_motel_elytra_launch() -> np.ndarray:
  CANDLE, FENCE, SLAB, STONE, BARS = _b("candle"), _b("dark_oak_fence"), _b("stone_brick_slab"), _b("stone_bricks"), _b("iron_bars")
  v = _motel_v(); ox, oz, oy = 13, 14, 4
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 4):
      _set(v, x, oy, z, SLAB)
      if x == ox or x == ox + 5 or z == oz or z == oz + 3:
        _set(v, x, oy + 1, z, BARS if x == ox + 5 else FENCE)
  for x in (ox + 1, ox + 4):
    _set(v, x, oy + 1, oz + 2, CANDLE)
  _set(v, ox + 3, oy - 1, oz + 2, STONE)
  return v


def _generate_epic_bases_motel_maze_trap() -> np.ndarray:
  LEAVES, DISP, TRIP, DOOR, LAVA, BERRY = _b("oak_leaves"), _b("dispenser"), _b("tripwire_hook"), _b("iron_door"), _b("lava"), _b("sweet_berry_bush")
  v = _motel_v(); ox, oz, oy = 11, 11, 1
  for x in range(ox, ox + 10):
    for z in range(oz, oz + 10):
      if (x + z) % 3 != 0:
        _set(v, x, oy, z, LEAVES)
        _set(v, x, oy + 1, z, LEAVES)
      if x == ox + 5 and z == oz + 5:
        _set(v, x, oy, z, DISP)
        _set(v, x, oy + 1, z, LAVA)
      if x == ox + 3 and z == oz + 7:
        _set(v, x, oy, z, TRIP)
      if x == ox + 8 and z == oz + 2:
        _set(v, x, oy, z, DOOR)
      if (x + z) % 7 == 0:
        _set(v, x, oy - 1, z, BERRY)
  return v


def _generate_epic_bases_motel_secret_door() -> np.ndarray:
  BOOK, PISTON, DUST, TORCH, STONE = _b("bookshelf"), _b("sticky_piston"), _b("redstone_dust"), _b("redstone_torch"), _b("stone_bricks")
  v = _motel_v(); ox, oz, oy = 14, 15, 1
  for y in range(oy, oy + 3):
    for x in range(ox, ox + 4):
      _set(v, x, y, oz, BOOK if y < oy + 2 else STONE)
  for x in range(ox, ox + 2):
    _set(v, x, oy, oz + 1, PISTON)
    _set(v, x, oy - 1, oz + 1, DUST)
  _set(v, ox + 3, oy - 1, oz, TORCH)
  return v


def _generate_epic_bases_motel_crypt_release() -> np.ndarray:
  STONE, DOOR, DAY, DUST, GREEN, MOSS = _b("stone_bricks"), _b("iron_door"), _b("daylight_detector"), _b("redstone_dust"), _b("green_terracotta"), _b("mossy_stone_bricks")
  v = _motel_v(); ox, oz, oy = 13, 13, 1
  for x in range(ox, ox + 5):
    for z in range(oz, oz + 5):
      for y in range(oy, oy + 4):
        wall = x in (ox, ox + 4) or z in (oz, oz + 4)
        if wall:
          _set(v, x, y, z, MOSS if y == oy else STONE)
      _set(v, x, oy + 4, z, GREEN)
  _set(v, ox + 2, oy + 1, oz, DOOR)
  _set(v, ox + 2, oy + 4, oz + 2, DAY)
  _set(v, ox + 2, oy + 3, oz + 2, DUST)
  return v


def _generate_epic_bases_motel_secret_passage() -> np.ndarray:
  STONE, MOSS, BOOK, TORCH, BARS = _b("stone_bricks"), _b("mossy_stone_bricks"), _b("bookshelf"), _b("torch"), _b("iron_bars")
  v = _motel_v(); ox, oz, oy = 13, 15, 1
  for x in range(ox, ox + 6):
    _set(v, x, oy, oz, STONE)
    _set(v, x, oy + 1, oz, MOSS if x % 2 else BOOK if x == ox + 2 else STONE)
    _set(v, x, oy + 2, oz, STONE)
  _set(v, ox + 3, oy + 1, oz + 1, AIR)
  _set(v, ox + 4, oy + 1, oz + 1, TORCH)
  _set(v, ox, oy + 1, oz, BARS)
  return v


def _phoenix_v():
  return _motel_v()


def _generate_epic_bases_phoenix_curtain_wall() -> np.ndarray:
  STONE, MOSS, COBBLE, STAIR, BANNER = _b("stone_bricks"), _b("mossy_stone_bricks"), _b("cobblestone"), _b("stone_brick_stairs"), _b("blue_banner")
  v = _phoenix_v(); ox, oz, oy = 10, 15, 1
  for x in range(ox, ox + 12):
    for y in range(oy, oy + 6):
      _set(v, x, y, oz, STONE if y < oy + 4 else MOSS)
      _set(v, x, y, oz + 1, COBBLE if y % 2 else STAIR)
    if x % 4 == 0:
      _set(v, x, oy + 5, oz, BANNER)
  return v


def _generate_epic_bases_phoenix_inner_village() -> np.ndarray:
  OAK, SPRUCE, YELLOW, DARK, COBBLE = _b("oak_planks"), _b("spruce_planks"), _b("yellow_terracotta"), _b("dark_oak_planks"), _b("cobblestone")
  v = _phoenix_v(); ox, oz, oy = 12, 12, 1
  for hx, hz in ((0, 0), (4, 0), (0, 4), (4, 4)):
    for x in range(ox + hx, ox + hx + 3):
      for z in range(oz + hz, oz + hz + 3):
        _set(v, x, oy, z, COBBLE)
        for y in range(oy + 1, oy + 4):
          wall = x in (ox + hx, ox + hx + 2) or z in (oz + hz, oz + hz + 2)
          if wall:
            _set(v, x, y, z, OAK if (x + z) % 2 else SPRUCE)
        _set(v, x, oy + 4, z, YELLOW if x == ox + hx + 1 else DARK)
  return v


def _generate_epic_bases_phoenix_guardian_moat() -> np.ndarray:
  WATER, PRISM, DPRISM, STONE, SEA = _b("water"), _b("prismarine"), _b("dark_prismarine"), _b("stone_bricks"), _b("sea_lantern")
  v = _phoenix_v(); ox, oz, oy = 11, 13, 1
  for x in range(ox, ox + 10):
    for z in range(oz, oz + 6):
      edge = x in (ox, ox + 9) or z in (oz, oz + 5)
      _set(v, x, oy - 1, z, STONE if edge else WATER)
      if not edge and (x + z) % 3 == 0:
        _set(v, x, oy - 1, z, PRISM if z < oz + 3 else DPRISM)
  _set(v, ox + 5, oy - 1, oz + 3, SEA)
  return v


def _generate_epic_bases_phoenix_parapet() -> np.ndarray:
  STONE, SLAB, BLUE, ORANGE, TORCH = _b("stone_bricks"), _b("stone_brick_slab"), _b("blue_banner"), _b("orange_banner"), _b("torch")
  v = _phoenix_v(); ox, oz, oy = 11, 15, 4
  for x in range(ox, ox + 10):
    _set(v, x, oy, oz, STONE)
    _set(v, x, oy + 1, oz, SLAB if x % 2 else STONE)
    if x % 3 == 0:
      _set(v, x, oy + 2, oz, BLUE if x % 6 == 0 else ORANGE)
    _set(v, x, oy + 1, oz + 1, TORCH)
  return v


def _generate_epic_bases_phoenix_siege_farm() -> np.ndarray:
  FARM, WHEAT, CARROT, WATER, FENCE = _b("farmland"), _b("wheat"), _b("carrots"), _b("water"), _b("oak_fence")
  v = _phoenix_v(); ox, oz, oy = 12, 13, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 6):
      if x == ox or x == ox + 7 or z == oz or z == oz + 5:
        _set(v, x, oy, z, FENCE)
      else:
        _set(v, x, oy, z, FARM)
        _set(v, x, oy + 1, z, WHEAT if (x + z) % 2 else CARROT)
  _set(v, ox + 4, oy, oz + 3, WATER)
  return v


def _generate_epic_bases_phoenix_royal_chamber() -> np.ndarray:
  STONE, CARPET, OAK, BARS, LANT = _b("stone_bricks"), _b("blue_carpet"), _b("oak_planks"), _b("iron_bars"), _b("lantern")
  v = _phoenix_v(); ox, oz, oy = 13, 14, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 5):
      _set(v, x, oy, z, CARPET)
      for y in range(oy + 1, oy + 5):
        wall = x in (ox, ox + 5) or z in (oz, oz + 4)
        if wall:
          _set(v, x, y, z, STONE if y < oy + 4 else BARS)
        elif y == oy + 1:
          _set(v, x, y, z, OAK)
  _set(v, ox + 3, oy + 4, oz + 2, LANT)
  return v


def _generate_epic_bases_phoenix_control_room() -> np.ndarray:
  RED, TORCH, LEVER, STONE, LAVA = _b("redstone_block"), _b("redstone_torch"), _b("lever"), _b("stone_bricks"), _b("lava_bucket")
  v = _phoenix_v(); ox, oz, oy = 13, 14, 1
  for x in range(ox, ox + 5):
    for z in range(oz, oz + 4):
      _set(v, x, oy, z, STONE)
      _set(v, x, oy + 1, z, RED if (x + z) % 2 else STONE)
  _set(v, ox + 2, oy + 2, oz + 2, LEVER)
  _set(v, ox + 1, oy + 1, oz + 1, TORCH)
  _set(v, ox + 3, oy + 2, oz + 1, LAVA)
  return v


def _generate_epic_bases_phoenix_stables() -> np.ndarray:
  HAY, OAK, FENCE, LANT, COBBLE = _b("hay_block"), _b("oak_planks"), _b("oak_fence"), _b("lantern"), _b("cobblestone")
  v = _phoenix_v(); ox, oz, oy = 12, 14, 1
  for x in range(ox, ox + 8):
    _set(v, x, oy, oz, COBBLE)
    _set(v, x, oy + 1, oz, HAY if x % 2 else OAK)
    _set(v, x, oy + 2, oz, FENCE)
    _set(v, x, oy + 3, oz, HAY)
  _set(v, ox + 4, oy + 3, oz + 1, LANT)
  return v


def _generate_epic_bases_phoenix_stockroom() -> np.ndarray:
  CHEST, BARREL, OAK, STONE, TORCH = _b("chest"), _b("barrel"), _b("oak_planks"), _b("stone_bricks"), _b("torch")
  v = _phoenix_v(); ox, oz, oy = 12, 13, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 6):
      _set(v, x, oy, z, STONE if z == oz else OAK)
      _set(v, x, oy + 1, z, CHEST if (x + z) % 2 else BARREL)
      _set(v, x, oy + 2, z, STONE)
  _set(v, ox + 4, oy + 2, oz + 3, TORCH)
  return v


def _generate_epic_bases_phoenix_escape_tunnel() -> np.ndarray:
  STONE, TNT, GRAVEL, TORCH, BARS = _b("stone_bricks"), _b("tnt"), _b("gravel"), _b("torch"), _b("iron_bars")
  v = _phoenix_v(); ox, oz, oy = 12, 15, 1
  for x in range(ox, ox + 8):
    _set(v, x, oy, oz, STONE)
    _set(v, x, oy + 1, oz, AIR if x < ox + 6 else GRAVEL)
    if x == ox + 7:
      _set(v, x, oy, oz, TNT)
  _set(v, ox, oy + 1, oz, BARS)
  _set(v, ox + 4, oy, oz + 1, TORCH)
  return v


def _generate_epic_bases_phoenix_defense_turret() -> np.ndarray:
  STONE, MOSS, TRAP, BANNER, BARS = _b("stone_bricks"), _b("mossy_stone_bricks"), _b("iron_trapdoor"), _b("blue_banner"), _b("iron_bars")
  v = _phoenix_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 10):
    for x in range(cx - 1, cx + 2):
      for z in range(cz - 1, cz + 2):
        edge = x in (cx - 1, cx + 1) or z in (cz - 1, cz + 1)
        if edge:
          _set(v, x, y, z, MOSS if y % 2 else STONE)
        elif y == oy + 4:
          _set(v, x, y, z, BARS)
    if y % 3 == 0:
      _set(v, cx + 1, y, cz, TRAP)
  _set(v, cx, oy + 10, cz, BANNER)
  return v


def _generate_epic_bases_phoenix_flying_buttress() -> np.ndarray:
  STONE, STAIR, COBBLE, AND, MOSS = _b("stone_bricks"), _b("stone_brick_stairs"), _b("cobblestone"), _b("andesite"), _b("mossy_stone_bricks")
  v = _phoenix_v(); ox, oz, oy = 15, 15, 1
  for y in range(oy, oy + 8):
    _set(v, ox, y, oz, STONE)
    _set(v, ox + 1, y, oz, STAIR if y > oy + 2 else COBBLE)
    _set(v, ox + 2, y, oz + 1, AND if y % 2 else MOSS)
  return v


def _generate_epic_bases_phoenix_battered_wall() -> np.ndarray:
  STONE, MOSS, AND, BRICK, COBBLE = _b("stone"), _b("mossy_cobblestone"), _b("andesite"), _b("stone_bricks"), _b("cobblestone")
  blocks = (STONE, MOSS, AND, BRICK, COBBLE)
  v = _phoenix_v(); ox, oz, oy = 12, 15, 1
  for y in range(oy, oy + 5):
    for x in range(ox, ox + 8):
      _set(v, x, y, oz, blocks[(x + y) % len(blocks)])
  return v


def _generate_epic_bases_phoenix_phoenix_banner() -> np.ndarray:
  BLUE, WHT, YEL, FENCE, STONE = _b("blue_banner"), _b("white_banner"), _b("yellow_banner"), _b("oak_fence"), _b("stone_bricks")
  v = _phoenix_v(); cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 3):
    _set(v, cx, y, cz, FENCE)
  _set(v, cx, oy + 3, cz, BLUE)
  _set(v, cx + 1, oy + 3, cz, WHT)
  _set(v, cx, oy + 4, cz, YEL)
  _set(v, cx, oy - 1, cz, STONE)
  return v


def _generate_epic_bases_phoenix_roof_slating() -> np.ndarray:
  DARK, SPRUCE, STONE, COBBLE, OAK = _b("dark_oak_stairs"), _b("spruce_stairs"), _b("stone_bricks"), _b("cobblestone"), _b("oak_planks")
  v = _phoenix_v(); ox, oz, oy = 13, 14, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 4):
      _set(v, x, oy, z, OAK)
      for h in range(3):
        _set(v, x, oy + 1 + h, z, DARK if x < ox + 3 else SPRUCE)
      if x in (ox, ox + 5):
        _set(v, x, oy + 2, z, STONE)
      _set(v, x, oy + 4, z, COBBLE)
  return v


def _generate_epic_bases_phoenix_mob_house_trap() -> np.ndarray:
  OAK, SPRUCE, HAY, TRIP, COBBLE = _b("oak_planks"), _b("spruce_planks"), _b("hay_block"), _b("tripwire_hook"), _b("cobblestone")
  v = _phoenix_v(); ox, oz, oy = 13, 14, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 5):
      _set(v, x, oy, z, COBBLE)
      for y in range(oy + 1, oy + 5):
        wall = x in (ox, ox + 5) or z in (oz, oz + 4)
        if wall:
          _set(v, x, y, z, OAK if y < oy + 4 else SPRUCE)
      _set(v, x, oy + 5, z, HAY)
  _set(v, ox + 3, oy, oz + 1, TRIP)
  return v


def _generate_epic_bases_phoenix_tnt_scatterbomb() -> np.ndarray:
  OBS, TNT, TORCH, REP, PLATE = _b("obsidian"), _b("tnt"), _b("redstone_torch"), _b("redstone_repeater"), _b("stone_pressure_plate")
  v = _phoenix_v(); ox, oz, oy = 13, 14, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 4):
      _set(v, x, oy, z, OBS)
      if (x + z) % 2 == 0:
        _set(v, x, oy + 1, z, TNT)
  _set(v, ox + 3, oy - 1, oz + 2, PLATE)
  _set(v, ox + 1, oy - 1, oz, TORCH)
  _set(v, ox + 4, oy - 1, oz + 1, REP)
  return v


def _generate_epic_bases_phoenix_lava_battlement() -> np.ndarray:
  STONE, DISP, LAVA, STAIR, BARS = _b("stone_bricks"), _b("dispenser"), _b("lava_bucket"), _b("stone_brick_stairs"), _b("iron_bars")
  v = _phoenix_v(); ox, oz, oy = 12, 15, 3
  for x in range(ox, ox + 8):
    _set(v, x, oy, oz, STONE)
    _set(v, x, oy + 1, oz, STAIR if x % 2 else BARS)
    if x % 3 == 0:
      _set(v, x, oy + 2, oz, DISP)
      _set(v, x, oy + 2, oz + 1, LAVA)
  return v


def _generate_epic_bases_phoenix_trap_control_panel() -> np.ndarray:
  STONE, LAVA, LEVER, DISP, DUST = _b("stone_bricks"), _b("lava_bucket"), _b("lever"), _b("dispenser"), _b("redstone_dust")
  v = _phoenix_v(); ox, oz, oy = 14, 15, 1
  for y in range(oy, oy + 3):
    _set(v, ox, y, oz, STONE)
    _set(v, ox + 1, y, oz, STONE)
  _set(v, ox, oy + 1, oz + 1, LAVA)
  _set(v, ox + 1, oy + 1, oz + 1, LAVA)
  _set(v, ox + 2, oy + 1, oz + 1, LAVA)
  _set(v, ox + 3, oy + 1, oz, LEVER)
  _set(v, ox + 2, oy, oz, DISP)
  _set(v, ox + 2, oy - 1, oz, DUST)
  return v


def _generate_epic_bases_phoenix_castle_sconce() -> np.ndarray:
  STONE, TORCH, FRAME, SLAB = _b("stone_bricks"), _b("torch"), _b("item_frame"), _b("stone_slab")
  v = _phoenix_v(); cx, cz, oy = 16, 16, 2
  _set(v, cx, oy, cz, STONE)
  _set(v, cx, oy + 1, cz, TORCH)
  _set(v, cx, oy + 2, cz, FRAME)
  _set(v, cx, oy + 3, cz, SLAB)
  return v


def _holme_v():
  return _phoenix_v()


def _generate_epic_bases_holme_outdoor_forum() -> np.ndarray:
  SAND, SMOOTH, PILLAR, FENCE, CUT = _b("sandstone"), _b("smooth_sandstone"), _b("sandstone_pillar"), _b("oak_fence"), _b("cut_sandstone")
  v = _holme_v(); cx, cz, oy = 16, 16, 1
  for x in range(cx - 3, cx + 4):
    for z in range(cz - 3, cz + 4):
      if (x - cx) ** 2 + (z - cz) ** 2 <= 16:
        _set(v, x, oy, z, SMOOTH if (x + z) % 2 else SAND)
        if (x + z) % 4 == 0:
          _set(v, x, oy + 1, z, PILLAR)
  for px, pz in ((cx + 3, cz), (cx - 3, cz), (cx, cz + 3), (cx, cz - 3)):
    _set(v, px, oy + 1, pz, FENCE)
  _set(v, cx, oy, cz, CUT)
  return v


def _generate_epic_bases_holme_announcement_pulpit() -> np.ndarray:
  SAND, DARK, GREEN, WHT, LANT, YB = _b("sandstone"), _b("dark_oak_planks"), _b("green_bed"), _b("white_wool"), _b("lantern"), _b("yellow_banner")
  v = _holme_v(); ox, oz, oy = 14, 15, 3
  for x in range(ox, ox + 4):
    _set(v, x, oy, oz, SAND)
    _set(v, x, oy + 1, oz, DARK)
    _set(v, x, oy + 2, oz, GREEN if x % 2 else WHT)
  _set(v, ox + 2, oy + 3, oz, LANT)
  _set(v, ox + 1, oy + 2, oz + 1, YB)
  return v


def _generate_epic_bases_holme_crane_tether() -> np.ndarray:
  GRIND, FENCE, CHAIN, SAND, BARS = _b("grindstone"), _b("dark_oak_fence"), _b("chain"), _b("sandstone"), _b("iron_bars")
  v = _holme_v(); ox, oz, oy = 15, 15, 4
  for y in range(oy, oy + 5):
    _set(v, ox, y, oz, SAND)
  for y in range(oy + 2, oy + 6):
    _set(v, ox + 1, y, oz, FENCE)
    _set(v, ox + 2, y, oz, GRIND if y % 2 else CHAIN)
  _set(v, ox + 2, oy, oz, BARS)
  return v


def _generate_epic_bases_holme_raised_entryway() -> np.ndarray:
  SAND, STAIR, SMOOTH, DARK, FENCE = _b("sandstone"), _b("sandstone_stairs"), _b("smooth_sandstone"), _b("dark_oak_planks"), _b("oak_fence")
  v = _holme_v(); ox, oz, oy = 11, 15, 1
  for x in range(ox, ox + 10):
    _set(v, x, oy, oz, STAIR)
    _set(v, x, oy + 1, oz, SAND)
    _set(v, x, oy + 2, oz, SMOOTH if x % 2 else DARK)
    if x == ox or x == ox + 9:
      _set(v, x, oy + 1, oz + 1, FENCE)
  return v


def _generate_epic_bases_holme_sky_bridge() -> np.ndarray:
  SAND, SMOOTH, DARK, FENCE, SLAB = _b("sandstone"), _b("smooth_sandstone"), _b("dark_oak_planks"), _b("oak_fence"), _b("sandstone_slab")
  v = _holme_v(); ox, oz, oy = 10, 15, 8
  for x in range(ox, ox + 12):
    _set(v, x, oy, oz, DARK)
    _set(v, x, oy, oz + 1, SLAB)
    _set(v, x, oy - 1, oz, SAND)
    if x % 4 == 0:
      _set(v, x, oy + 1, oz, FENCE)
      _set(v, x, oy + 1, oz + 1, SMOOTH)
  return v


def _generate_epic_bases_holme_great_bell() -> np.ndarray:
  GOLD, YEL, BARS, FENCE, SMOOTH = _b("gold_block"), _b("yellow_concrete"), _b("iron_bars"), _b("dark_oak_fence"), _b("smooth_sandstone")
  v = _holme_v(); cx, cz, oy = 16, 16, 1
  for x in range(cx - 1, cx + 2):
    for z in range(cz - 1, cz + 2):
      _set(v, x, oy, z, SMOOTH)
      _set(v, x, oy + 4, z, BARS)
  _set(v, cx, oy + 2, cz, GOLD)
  _set(v, cx, oy + 1, cz, YEL)
  _set(v, cx, oy + 5, cz, FENCE)
  return v


def _generate_epic_bases_holme_grand_chandelier() -> np.ndarray:
  GLOW, DTRAP, OTRAP, FENCE, CHAIN = _b("glowstone"), _b("dark_oak_trapdoor"), _b("oak_trapdoor"), _b("dark_oak_fence"), _b("chain")
  v = _holme_v(); cx, cz, oy = 16, 16, 6
  _set(v, cx, oy + 3, cz, CHAIN)
  for y in range(oy, oy + 3):
    _set(v, cx, y, cz, GLOW)
    for dx, dz, trap in ((-1, 0, DTRAP), (1, 0, OTRAP), (0, -1, DTRAP), (0, 1, OTRAP)):
      _set(v, cx + dx, y, cz + dz, trap)
  _set(v, cx, oy - 1, cz, FENCE)
  return v


def _generate_epic_bases_holme_grand_library() -> np.ndarray:
  BOOK, OAK, LANT, SAND = _b("bookshelf"), _b("oak_planks"), _b("lantern"), _b("sandstone")
  v = _holme_v(); ox, oz, oy = 12, 13, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 6):
      _set(v, x, oy, z, OAK)
      for y in range(oy + 1, oy + 5):
        wall = x in (ox, ox + 7) or z in (oz, oz + 5)
        if wall:
          _set(v, x, y, z, BOOK)
  _set(v, ox + 4, oy + 4, oz + 3, LANT)
  _set(v, ox + 3, oy + 1, oz + 3, SAND)
  return v


def _generate_epic_bases_holme_block_museum() -> np.ndarray:
  STONE, GLASS, IRON, GOLD, DIA = _b("stone"), _b("glass"), _b("iron_block"), _b("gold_block"), _b("diamond_block")
  v = _holme_v(); ox, oz, oy = 12, 13, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 6):
      _set(v, x, oy, z, STONE)
      _set(v, x, oy + 1, z, GLASS if (x + z) % 3 == 0 else STONE)
      if (x + z) % 4 == 1:
        _set(v, x, oy + 2, z, IRON)
      elif (x + z) % 4 == 2:
        _set(v, x, oy + 2, z, GOLD)
      elif (x + z) % 4 == 3:
        _set(v, x, oy + 2, z, DIA)
  return v


def _generate_epic_bases_holme_forge() -> np.ndarray:
  FURN, ANVIL, SMITH, STONE, LANT = _b("furnace"), _b("anvil"), _b("smithing_table"), _b("stone_bricks"), _b("lantern")
  v = _holme_v(); ox, oz, oy = 13, 14, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 5):
      _set(v, x, oy, z, STONE)
  _set(v, ox + 1, oy + 1, oz + 2, FURN)
  _set(v, ox + 3, oy + 1, oz + 2, ANVIL)
  _set(v, ox + 4, oy + 1, oz + 1, SMITH)
  _set(v, ox + 2, oy + 2, oz + 3, LANT)
  return v


def _generate_epic_bases_holme_indoor_farm() -> np.ndarray:
  FARM, WHEAT, CARROT, WATER, SLAB, GLOW = _b("farmland"), _b("wheat"), _b("carrots"), _b("water"), _b("oak_slab"), _b("glowstone")
  v = _holme_v(); ox, oz, oy = 13, 14, 1
  for tier in range(3):
    y = oy + tier
    for x in range(ox, ox + 6):
      _set(v, x, y, oz + tier, SLAB)
      _set(v, x, y + 1, oz + tier, FARM)
      _set(v, x, y + 2, oz + tier, WHEAT if x % 2 else CARROT)
  _set(v, ox + 3, oy, oz + 1, WATER)
  _set(v, ox + 5, oy + 3, oz + 3, GLOW)
  return v


def _generate_epic_bases_holme_molten_vent() -> np.ndarray:
  LAVA, STONE, COBBLE, OBS, BARS = _b("lava"), _b("stone"), _b("cobblestone"), _b("obsidian"), _b("iron_bars")
  v = _holme_v(); ox, oz, oy = 15, 15, 1
  for y in range(oy, oy + 5):
    _set(v, ox, y, oz, LAVA if y < oy + 4 else STONE)
    _set(v, ox + 1, y, oz, COBBLE if y % 2 else OBS)
  _set(v, ox, oy + 5, oz, BARS)
  _set(v, ox - 1, oy, oz, STONE)
  return v


def _generate_epic_bases_holme_citadel_facade() -> np.ndarray:
  SAND, RED, SMOOTH, CUT, DARK = _b("sandstone"), _b("red_sandstone"), _b("smooth_sandstone"), _b("cut_red_sandstone"), _b("dark_oak_planks")
  v = _holme_v(); ox, oz, oy = 13, 15, 1
  for y in range(oy, oy + 9):
    for x in range(ox, ox + 6):
      _set(v, x, y, oz, SAND if y % 2 else RED)
      if y == oy + 3 and x % 2 == 1:
        _set(v, x, y, oz + 1, DARK)
      if y == oy + 8:
        _set(v, x, y, oz, SMOOTH)
  _set(v, ox + 3, oy + 5, oz, CUT)
  return v


def _generate_epic_bases_holme_acacia_balcony() -> np.ndarray:
  ACAC, SLAB, DARK, PANE, SAND = _b("acacia_stairs"), _b("acacia_slab"), _b("dark_oak_planks"), _b("glass_pane"), _b("sandstone")
  v = _holme_v(); ox, oz, oy = 14, 15, 3
  for x in range(ox, ox + 4):
    _set(v, x, oy, oz, DARK)
    _set(v, x, oy + 1, oz, PANE)
    _set(v, x, oy + 2, oz, ACAC)
  _set(v, ox + 1, oy + 3, oz, SLAB)
  _set(v, ox + 2, oy + 3, oz, SLAB)
  _set(v, ox, oy - 1, oz, SAND)
  return v


def _generate_epic_bases_holme_murder_hole_wall() -> np.ndarray:
  SAND, STAIR, SMOOTH, RED, NOTE = _b("sandstone"), _b("sandstone_stairs"), _b("smooth_sandstone"), _b("red_sandstone"), _b("note_block")
  v = _holme_v(); ox, oz, oy = 13, 15, 1
  for y in range(oy, oy + 5):
    for x in range(ox, ox + 6):
      _set(v, x, y, oz, STAIR if x % 2 and y == oy + 2 else SAND if (x + y) % 2 else SMOOTH)
      if y == oy + 1 and x % 3 == 1:
        _set(v, x, y, oz, RED)
  _set(v, ox + 3, oy + 4, oz, NOTE)
  return v


def _generate_epic_bases_holme_council_table() -> np.ndarray:
  OAK, GLOW, ORG, WHT, DARK = _b("oak_planks"), _b("glowstone"), _b("orange_terracotta"), _b("white_terracotta"), _b("dark_oak_planks")
  v = _holme_v(); cx, cz, oy = 16, 16, 1
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      if (x - cx) ** 2 + (z - cz) ** 2 <= 6:
        _set(v, x, oy, z, ORG if (x + z) % 2 else WHT)
        _set(v, x, oy + 1, z, OAK)
  _set(v, cx, oy + 1, cz, GLOW)
  _set(v, cx, oy - 1, cz, DARK)
  return v


def _generate_epic_bases_holme_council_chair() -> np.ndarray:
  STAIR, TRAP, BANNER, SAND = _b("dark_oak_stairs"), _b("dark_oak_trapdoor"), _b("lime_banner"), _b("sandstone")
  v = _holme_v(); cx, cz, oy = 16, 16, 1
  _set(v, cx, oy, cz, SAND)
  _set(v, cx, oy + 1, cz, STAIR)
  _set(v, cx - 1, oy + 1, cz, TRAP)
  _set(v, cx + 1, oy + 1, cz, TRAP)
  _set(v, cx, oy + 2, cz, TRAP)
  _set(v, cx, oy + 3, cz, BANNER)
  return v


def _generate_epic_bases_holme_window_shutters() -> np.ndarray:
  SAND, TRAP, PANE, BOOK, FURN = _b("sandstone"), _b("dark_oak_trapdoor"), _b("glass_pane"), _b("bookshelf"), _b("furnace")
  v = _holme_v(); ox, oz, oy = 15, 15, 1
  for y in range(oy, oy + 3):
    _set(v, ox, y, oz, SAND)
    _set(v, ox + 2, y, oz, SAND)
    if y == oy + 1:
      _set(v, ox + 1, y, oz, PANE)
  _set(v, ox - 1, oy + 1, oz, TRAP)
  _set(v, ox + 3, oy + 1, oz, TRAP)
  _set(v, ox + 1, oy, oz + 1, BOOK)
  _set(v, ox + 1, oy + 1, oz + 1, FURN)
  return v


def _generate_epic_bases_holme_banner_holder() -> np.ndarray:
  TRAP, FENCE, BANNER, SAND, SMOOTH = _b("dark_oak_trapdoor"), _b("dark_oak_fence"), _b("yellow_banner"), _b("sandstone"), _b("smooth_sandstone")
  v = _holme_v(); cx, cz, oy = 16, 16, 2
  _set(v, cx, oy, cz, SAND)
  _set(v, cx, oy + 1, cz, TRAP)
  _set(v, cx, oy + 2, cz, FENCE)
  _set(v, cx, oy + 3, cz, BANNER)
  _set(v, cx + 1, oy, cz, SMOOTH)
  return v


def _generate_epic_bases_holme_hang_lights() -> np.ndarray:
  GLOW, OTRAP, DTRAP, FENCE, CHAIN = _b("glowstone"), _b("oak_trapdoor"), _b("dark_oak_trapdoor"), _b("oak_fence"), _b("chain")
  v = _holme_v(); ox, oz, oy = 14, 15, 5
  for i, x in enumerate((ox, ox + 2, ox + 4)):
    _set(v, x, oy, oz, CHAIN)
    _set(v, x, oy - 1, oz, GLOW)
    _set(v, x, oy - 1, oz + 1, OTRAP if i % 2 else DTRAP)
    _set(v, x, oy - 2, oz, FENCE)
  return v


_GENERATORS: dict[str, object] = {
  "epic_bases_wolf_figurehead": _generate_epic_bases_wolf_figurehead,
  "epic_bases_deck_brazier": _generate_epic_bases_deck_brazier,
  "epic_bases_emerald_wolf": _generate_epic_bases_emerald_wolf,
  "epic_bases_crows_nest": _generate_epic_bases_crows_nest,
  "epic_bases_ship_flag": _generate_epic_bases_ship_flag,
  "epic_bases_ship_oars": _generate_epic_bases_ship_oars,
  "epic_bases_artillery_cannon": _generate_epic_bases_artillery_cannon,
  "epic_bases_fenrir_billowing_sails": _generate_epic_bases_fenrir_billowing_sails,
  "epic_bases_fenrir_boat_ribs": _generate_epic_bases_fenrir_boat_ribs,
  "epic_bases_fenrir_storage_cabin": _generate_epic_bases_fenrir_storage_cabin,
  "epic_bases_fenrir_thatched_roof": _generate_epic_bases_fenrir_thatched_roof,
  "epic_bases_fenrir_bunk_beds": _generate_epic_bases_fenrir_bunk_beds,
  "epic_bases_fenrir_map_table": _generate_epic_bases_fenrir_map_table,
  "epic_bases_fenrir_crossbeams": _generate_epic_bases_fenrir_crossbeams,
  "epic_bases_fenrir_throne_room": _generate_epic_bases_fenrir_throne_room,
  "epic_bases_fenrir_tnt_cannon_redstone": _generate_epic_bases_fenrir_tnt_cannon_redstone,
  "epic_bases_tomb_desert_oasis": _generate_epic_bases_tomb_desert_oasis,
  "epic_bases_tomb_water_bearer_statue": _generate_epic_bases_tomb_water_bearer_statue,
  "epic_bases_tomb_fire_bearer_statue": _generate_epic_bases_tomb_fire_bearer_statue,
  "epic_bases_tomb_grand_entrance": _generate_epic_bases_tomb_grand_entrance,
  "epic_bases_tomb_pillared_river": _generate_epic_bases_tomb_pillared_river,
  "epic_bases_tomb_fire_beacons": _generate_epic_bases_tomb_fire_beacons,
  "epic_bases_tomb_library": _generate_epic_bases_tomb_library,
  "epic_bases_tomb_tree_farm": _generate_epic_bases_tomb_tree_farm,
  "epic_bases_tomb_royal_bedchamber": _generate_epic_bases_tomb_royal_bedchamber,
  "epic_bases_tomb_lava_parkour": _generate_epic_bases_tomb_lava_parkour,
  "epic_bases_tomb_defensive_maze": _generate_epic_bases_tomb_defensive_maze,
  "epic_bases_tomb_waterfall_exit": _generate_epic_bases_tomb_waterfall_exit,
  "epic_bases_tomb_entrance_atrium": _generate_epic_bases_tomb_entrance_atrium,
  "epic_bases_tomb_daylight_doorway": _generate_epic_bases_tomb_daylight_doorway,
  "epic_bases_tomb_ladder_parkour": _generate_epic_bases_tomb_ladder_parkour,
  "epic_bases_tomb_indoor_farm": _generate_epic_bases_tomb_indoor_farm,
  "epic_bases_lab_floating_nether_portal": _generate_epic_bases_lab_floating_nether_portal,
  "epic_bases_lab_ballonet": _generate_epic_bases_lab_ballonet,
  "epic_bases_lab_propeller": _generate_epic_bases_lab_propeller,
  "epic_bases_lab_potions_tower": _generate_epic_bases_lab_potions_tower,
  "epic_bases_lab_windmill": _generate_epic_bases_lab_windmill,
  "epic_bases_lab_libratory": _generate_epic_bases_lab_libratory,
  "epic_bases_lab_fumigation_chimney": _generate_epic_bases_lab_fumigation_chimney,
  "epic_bases_lab_giant_mushroom": _generate_epic_bases_lab_giant_mushroom,
  "epic_bases_lab_victorian_tower": _generate_epic_bases_lab_victorian_tower,
  "epic_bases_airship_express": _generate_epic_bases_airship_express,
  "epic_bases_airship_engine_furnace": _generate_epic_bases_airship_engine_furnace,
  "epic_bases_airship_quarterdeck": _generate_epic_bases_airship_quarterdeck,
  "epic_bases_airship_balloon": _generate_epic_bases_airship_balloon,
  "epic_bases_airship_storage_hold": _generate_epic_bases_airship_storage_hold,
  "epic_bases_airship_propeller": _generate_epic_bases_airship_propeller,
  "epic_bases_estate_grand_dome": _generate_epic_bases_estate_grand_dome,
  "epic_bases_estate_stained_glass_wall": _generate_epic_bases_estate_stained_glass_wall,
  "epic_bases_estate_transfer_tunnel": _generate_epic_bases_estate_transfer_tunnel,
  "epic_bases_estate_observation_glass": _generate_epic_bases_estate_observation_glass,
  "epic_bases_estate_kelp_garden": _generate_epic_bases_estate_kelp_garden,
  "epic_bases_estate_skylight_tower": _generate_epic_bases_estate_skylight_tower,
  "epic_bases_estate_deco_archway": _generate_epic_bases_estate_deco_archway,
  "epic_bases_estate_deco_tower": _generate_epic_bases_estate_deco_tower,
  "epic_bases_estate_aquarium_lounge": _generate_epic_bases_estate_aquarium_lounge,
  "epic_bases_estate_coral_garden": _generate_epic_bases_estate_coral_garden,
  "epic_bases_estate_drowned_farm": _generate_epic_bases_estate_drowned_farm,
  "epic_bases_exchange_support_platform": _generate_epic_bases_exchange_support_platform,
  "epic_bases_exchange_eternal_flame": _generate_epic_bases_exchange_eternal_flame,
  "epic_bases_exchange_redstone_altar": _generate_epic_bases_exchange_redstone_altar,
  "epic_bases_exchange_remnant_memorial": _generate_epic_bases_exchange_remnant_memorial,
  "epic_bases_exchange_lily_pad_path": _generate_epic_bases_exchange_lily_pad_path,
  "epic_bases_exchange_end_stepwell": _generate_epic_bases_exchange_end_stepwell,
  "epic_bases_exchange_jungle_statue": _generate_epic_bases_exchange_jungle_statue,
  "epic_bases_exchange_jungle_cabin": _generate_epic_bases_exchange_jungle_cabin,
  "epic_bases_exchange_stilt_house": _generate_epic_bases_exchange_stilt_house,
  "epic_bases_exchange_streetlight": _generate_epic_bases_exchange_streetlight,
  "epic_bases_exchange_market_stall": _generate_epic_bases_exchange_market_stall,
  "epic_bases_exchange_aerial_walkway": _generate_epic_bases_exchange_aerial_walkway,
  "epic_bases_exchange_tiered_garden": _generate_epic_bases_exchange_tiered_garden,
  "epic_bases_exchange_cryptic_floor": _generate_epic_bases_exchange_cryptic_floor,
  "epic_bases_cube_force_field_maw": _generate_epic_bases_cube_force_field_maw,
  "epic_bases_cube_radiant_beacon": _generate_epic_bases_cube_radiant_beacon,
  "epic_bases_cube_overgrown_tower": _generate_epic_bases_cube_overgrown_tower,
  "epic_bases_cube_crumbled_ruins": _generate_epic_bases_cube_crumbled_ruins,
  "epic_bases_cube_testing_lab": _generate_epic_bases_cube_testing_lab,
  "epic_bases_cube_mob_museum": _generate_epic_bases_cube_mob_museum,
  "epic_bases_cube_circuit_wall": _generate_epic_bases_cube_circuit_wall,
  "epic_bases_cube_core_engine": _generate_epic_bases_cube_core_engine,
  "epic_bases_cube_lava_curtain": _generate_epic_bases_cube_lava_curtain,
  "epic_bases_cube_reinforced_shell": _generate_epic_bases_cube_reinforced_shell,
  "epic_bases_cube_automatic_doorway": _generate_epic_bases_cube_automatic_doorway,
  "epic_bases_cube_futuristic_streetlight": _generate_epic_bases_cube_futuristic_streetlight,
  "epic_bases_cube_floating_engine": _generate_epic_bases_cube_floating_engine,
  "epic_bases_ice_golem_outpost": _generate_epic_bases_ice_golem_outpost,
  "epic_bases_ice_frozen_forum": _generate_epic_bases_ice_frozen_forum,
  "epic_bases_ice_amphitheater": _generate_epic_bases_ice_amphitheater,
  "epic_bases_ice_quartz_bridge": _generate_epic_bases_ice_quartz_bridge,
  "epic_bases_ice_signaling_beacon": _generate_epic_bases_ice_signaling_beacon,
  "epic_bases_ice_mountain_docks": _generate_epic_bases_ice_mountain_docks,
  "epic_bases_ice_ragged_spire": _generate_epic_bases_ice_ragged_spire,
  "epic_bases_ice_frozen_tree": _generate_epic_bases_ice_frozen_tree,
  "epic_bases_ice_elven_outpost": _generate_epic_bases_ice_elven_outpost,
  "epic_bases_ice_alcove_passage": _generate_epic_bases_ice_alcove_passage,
  "epic_bases_ice_spike": _generate_epic_bases_ice_spike,
  "epic_bases_ice_soul_lantern": _generate_epic_bases_ice_soul_lantern,
  "epic_bases_ice_open_gazebo": _generate_epic_bases_ice_open_gazebo,
  "epic_bases_ice_snowman_farm": _generate_epic_bases_ice_snowman_farm,
  "epic_bases_hoard_treasure_trove": _generate_epic_bases_hoard_treasure_trove,
  "epic_bases_hoard_super_statue": _generate_epic_bases_hoard_super_statue,
  "epic_bases_hoard_coal_mine_rail": _generate_epic_bases_hoard_coal_mine_rail,
  "epic_bases_hoard_magma_lava_lake": _generate_epic_bases_hoard_magma_lava_lake,
  "epic_bases_hoard_lava_pathway": _generate_epic_bases_hoard_lava_pathway,
  "epic_bases_hoard_support_pillar": _generate_epic_bases_hoard_support_pillar,
  "epic_bases_hoard_lava_fountain": _generate_epic_bases_hoard_lava_fountain,
  "epic_bases_hoard_debris_awning": _generate_epic_bases_hoard_debris_awning,
  "epic_bases_hoard_swamp_pool": _generate_epic_bases_hoard_swamp_pool,
  "epic_bases_hoard_cavern_hall": _generate_epic_bases_hoard_cavern_hall,
  "epic_bases_hoard_mine_shaft": _generate_epic_bases_hoard_mine_shaft,
  "epic_bases_hoard_lava_lighting": _generate_epic_bases_hoard_lava_lighting,
  "epic_bases_hoard_underground_chamber": _generate_epic_bases_hoard_underground_chamber,
  "epic_bases_hoard_auto_smelter": _generate_epic_bases_hoard_auto_smelter,
  "epic_bases_hoard_enchant_setup": _generate_epic_bases_hoard_enchant_setup,
  "epic_bases_sweet_flavor_factory": _generate_epic_bases_sweet_flavor_factory,
  "epic_bases_sweet_chocolate_bridge": _generate_epic_bases_sweet_chocolate_bridge,
  "epic_bases_sweet_mushroom_meadow": _generate_epic_bases_sweet_mushroom_meadow,
  "epic_bases_sweet_jelly_castle": _generate_epic_bases_sweet_jelly_castle,
  "epic_bases_sweet_slushie_tap": _generate_epic_bases_sweet_slushie_tap,
  "epic_bases_sweet_rainbow_road": _generate_epic_bases_sweet_rainbow_road,
  "epic_bases_sweet_honey_moat": _generate_epic_bases_sweet_honey_moat,
  "epic_bases_sweet_candy_cane_light": _generate_epic_bases_sweet_candy_cane_light,
  "epic_bases_sweet_doughnut_dorm": _generate_epic_bases_sweet_doughnut_dorm,
  "epic_bases_sweet_alpine_chalet": _generate_epic_bases_sweet_alpine_chalet,
  "epic_bases_sweet_mushroom_tap": _generate_epic_bases_sweet_mushroom_tap,
  "epic_bases_sweet_lollipop_tower": _generate_epic_bases_sweet_lollipop_tower,
  "epic_bases_sweet_slime_carpet": _generate_epic_bases_sweet_slime_carpet,
  "epic_bases_sweet_candy_factory": _generate_epic_bases_sweet_candy_factory,
  "epic_bases_sweet_wheat_farm": _generate_epic_bases_sweet_wheat_farm,
  "epic_bases_sweet_sugarcane_farm": _generate_epic_bases_sweet_sugarcane_farm,
  "epic_bases_sweet_cuckoo_clock": _generate_epic_bases_sweet_cuckoo_clock,
  "epic_bases_sweet_chicken_coop": _generate_epic_bases_sweet_chicken_coop,
  "epic_bases_sweet_factory_pipes": _generate_epic_bases_sweet_factory_pipes,
  "epic_bases_sweet_cotton_candy_tree": _generate_epic_bases_sweet_cotton_candy_tree,
  "epic_bases_motel_decrepit_wing": _generate_epic_bases_motel_decrepit_wing,
  "epic_bases_motel_soul_lighting": _generate_epic_bases_motel_soul_lighting,
  "epic_bases_motel_bone_tree": _generate_epic_bases_motel_bone_tree,
  "epic_bases_motel_hedge_maze": _generate_epic_bases_motel_hedge_maze,
  "epic_bases_motel_mortuary": _generate_epic_bases_motel_mortuary,
  "epic_bases_motel_gothic_spire": _generate_epic_bases_motel_gothic_spire,
  "epic_bases_motel_cobweb_hall": _generate_epic_bases_motel_cobweb_hall,
  "epic_bases_motel_graveyard_crypt": _generate_epic_bases_motel_graveyard_crypt,
  "epic_bases_motel_skeletal_stables": _generate_epic_bases_motel_skeletal_stables,
  "epic_bases_motel_wicked_tree": _generate_epic_bases_motel_wicked_tree,
  "epic_bases_motel_prison_room": _generate_epic_bases_motel_prison_room,
  "epic_bases_motel_swamp_foundation": _generate_epic_bases_motel_swamp_foundation,
  "epic_bases_motel_potions_lab": _generate_epic_bases_motel_potions_lab,
  "epic_bases_motel_elytra_launch": _generate_epic_bases_motel_elytra_launch,
  "epic_bases_motel_maze_trap": _generate_epic_bases_motel_maze_trap,
  "epic_bases_motel_secret_door": _generate_epic_bases_motel_secret_door,
  "epic_bases_motel_crypt_release": _generate_epic_bases_motel_crypt_release,
  "epic_bases_motel_secret_passage": _generate_epic_bases_motel_secret_passage,
  "epic_bases_phoenix_curtain_wall": _generate_epic_bases_phoenix_curtain_wall,
  "epic_bases_phoenix_inner_village": _generate_epic_bases_phoenix_inner_village,
  "epic_bases_phoenix_guardian_moat": _generate_epic_bases_phoenix_guardian_moat,
  "epic_bases_phoenix_parapet": _generate_epic_bases_phoenix_parapet,
  "epic_bases_phoenix_siege_farm": _generate_epic_bases_phoenix_siege_farm,
  "epic_bases_phoenix_royal_chamber": _generate_epic_bases_phoenix_royal_chamber,
  "epic_bases_phoenix_control_room": _generate_epic_bases_phoenix_control_room,
  "epic_bases_phoenix_stables": _generate_epic_bases_phoenix_stables,
  "epic_bases_phoenix_stockroom": _generate_epic_bases_phoenix_stockroom,
  "epic_bases_phoenix_escape_tunnel": _generate_epic_bases_phoenix_escape_tunnel,
  "epic_bases_phoenix_defense_turret": _generate_epic_bases_phoenix_defense_turret,
  "epic_bases_phoenix_flying_buttress": _generate_epic_bases_phoenix_flying_buttress,
  "epic_bases_phoenix_battered_wall": _generate_epic_bases_phoenix_battered_wall,
  "epic_bases_phoenix_phoenix_banner": _generate_epic_bases_phoenix_phoenix_banner,
  "epic_bases_phoenix_roof_slating": _generate_epic_bases_phoenix_roof_slating,
  "epic_bases_phoenix_mob_house_trap": _generate_epic_bases_phoenix_mob_house_trap,
  "epic_bases_phoenix_tnt_scatterbomb": _generate_epic_bases_phoenix_tnt_scatterbomb,
  "epic_bases_phoenix_lava_battlement": _generate_epic_bases_phoenix_lava_battlement,
  "epic_bases_phoenix_trap_control_panel": _generate_epic_bases_phoenix_trap_control_panel,
  "epic_bases_phoenix_castle_sconce": _generate_epic_bases_phoenix_castle_sconce,
  "epic_bases_holme_outdoor_forum": _generate_epic_bases_holme_outdoor_forum,
  "epic_bases_holme_announcement_pulpit": _generate_epic_bases_holme_announcement_pulpit,
  "epic_bases_holme_crane_tether": _generate_epic_bases_holme_crane_tether,
  "epic_bases_holme_raised_entryway": _generate_epic_bases_holme_raised_entryway,
  "epic_bases_holme_sky_bridge": _generate_epic_bases_holme_sky_bridge,
  "epic_bases_holme_great_bell": _generate_epic_bases_holme_great_bell,
  "epic_bases_holme_grand_chandelier": _generate_epic_bases_holme_grand_chandelier,
  "epic_bases_holme_grand_library": _generate_epic_bases_holme_grand_library,
  "epic_bases_holme_block_museum": _generate_epic_bases_holme_block_museum,
  "epic_bases_holme_forge": _generate_epic_bases_holme_forge,
  "epic_bases_holme_indoor_farm": _generate_epic_bases_holme_indoor_farm,
  "epic_bases_holme_molten_vent": _generate_epic_bases_holme_molten_vent,
  "epic_bases_holme_citadel_facade": _generate_epic_bases_holme_citadel_facade,
  "epic_bases_holme_acacia_balcony": _generate_epic_bases_holme_acacia_balcony,
  "epic_bases_holme_murder_hole_wall": _generate_epic_bases_holme_murder_hole_wall,
  "epic_bases_holme_council_table": _generate_epic_bases_holme_council_table,
  "epic_bases_holme_council_chair": _generate_epic_bases_holme_council_chair,
  "epic_bases_holme_window_shutters": _generate_epic_bases_holme_window_shutters,
  "epic_bases_holme_banner_holder": _generate_epic_bases_holme_banner_holder,
  "epic_bases_holme_hang_lights": _generate_epic_bases_holme_hang_lights,
}
