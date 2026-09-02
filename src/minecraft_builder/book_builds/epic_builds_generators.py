"""Procedural generators for Minecraft Epic Builds modular builds."""

from __future__ import annotations

import numpy as np

from ..data.palette import AIR
from .epic_builds_registry import EPIC_BUILDS


def generate_epic_build(build_id: str) -> np.ndarray:
  if build_id not in EPIC_BUILDS:
    raise KeyError(f"Unknown epic build: {build_id}")
  fn = _GENERATORS.get(build_id)
  if fn is None:
    raise NotImplementedError(f"No generator for {build_id}")
  return fn()


def _b(name: str) -> str:
  return name if name.startswith("minecraft:") else f"minecraft:{name}"


def _set(v: np.ndarray, x: int, y: int, z: int, block: str) -> None:
  if 0 <= x < v.shape[0] and 0 <= y < v.shape[1] and 0 <= z < v.shape[2]:
    v[x, y, z] = block


def _fill_box(
  v: np.ndarray,
  x0: int,
  y0: int,
  z0: int,
  w: int,
  h: int,
  d: int,
  mat: str,
  *,
  hollow: bool = False,
) -> None:
  for y in range(y0, y0 + h):
    for x in range(x0, x0 + w):
      for z in range(z0, z0 + d):
        edge = x in (x0, x0 + w - 1) or z in (z0, z0 + d - 1) or y in (y0, y0 + h - 1)
        if hollow and not edge:
          continue
        _set(v, x, y, z, mat)


def _generate_epic_builds_hanging_tower() -> np.ndarray:
  LOG = _b("dark_oak_log")
  PLANK = _b("dark_oak_planks")
  DEEP = _b("dark_prismarine")
  STAIR = _b("dark_prismarine_stairs")
  LADDER = _b("ladder")
  TRAP = _b("oak_trapdoor")
  LEAVES = _b("flowering_azalea_leaves")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 16):
    rad = 3 - (y - oy) // 5
    for x in range(cx - rad, cx + rad + 1):
      for z in range(cz - rad, cz + rad + 1):
        if (x - cx) ** 2 + (z - cz) ** 2 <= rad ** 2:
          edge = (x - cx) ** 2 + (z - cz) ** 2 >= (rad - 1) ** 2
          if edge:
            _set(v, x, y, z, LOG if y % 3 else DEEP)
          elif x == cx and z == cz:
            _set(v, x, y, z, LADDER)
    if y % 4 == 0:
      _set(v, cx + rad - 1, y, cz, TRAP)
  _set(v, cx, oy + 15, cz, STAIR)
  _set(v, cx + 1, oy + 14, cz, LEAVES)
  return v


def _generate_epic_builds_landing_pad() -> np.ndarray:
  PLANK = _b("dark_oak_planks")
  DEEP = _b("dark_prismarine")
  FENCE = _b("oak_fence")
  WATER = _b("water")
  GLASS = _b("light_blue_stained_glass")
  WALL = _b("red_sandstone_wall")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 12, 4
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 8):
      _set(v, x, oy, z, PLANK)
      if x in (ox, ox + 7) or z in (oz, oz + 7):
        _set(v, x, oy + 1, z, FENCE)
      else:
        _set(v, x, oy - 1, z, WATER if (x + z) % 2 else GLASS)
  for x in range(ox, ox + 8):
    _set(v, x, oy - 2, oz, WALL)
    _set(v, x, oy - 2, oz + 7, WALL)
  _set(v, ox + 3, oy + 1, oz + 3, DEEP)
  return v


def _generate_epic_builds_bathhouse() -> np.ndarray:
  DEEP = _b("dark_prismarine")
  PLANK = _b("dark_oak_planks")
  LOG = _b("dark_oak_log")
  WATER = _b("water")
  ICE = _b("ice")
  CLAY = _b("clay")
  FIRE = _b("campfire")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 12, 1
  _fill_box(v, ox, oy, oz, 12, 9, 8, DEEP, hollow=True)
  for floor in range(3):
    fy = oy + floor * 3
    for x in range(ox + 1, ox + 11, 5):
      for z in range(oz + 1, oz + 7):
        _set(v, x, fy, z, PLANK)
        _set(v, x + 1, fy + 1, z + 2, WATER if floor == 0 else ICE if floor == 1 else CLAY)
    _set(v, ox + 5, fy + 1, oz + 4, FIRE if floor == 2 else LOG)
  return v


def _generate_epic_builds_mountain_corridor() -> np.ndarray:
  STONE = _b("stone")
  BRICK = _b("stone_bricks")
  PLANK = _b("dark_oak_planks")
  DEEP = _b("dark_prismarine")
  TORCH = _b("torch")
  CHEST = _b("chest")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 14, 1
  for y in range(oy, oy + 12):
    for x in range(ox, ox + 8):
      _set(v, x, y, oz, STONE)
      _set(v, x, y, oz + 5, STONE)
  for y in range(oy + 2, oy + 10):
    for z in range(oz + 1, oz + 5):
      _set(v, ox + 1, y, z, AIR_B)
      _set(v, ox + 6, y, z, BRICK)
  _set(v, ox + 3, oy + 3, oz, PLANK)
  _set(v, ox + 4, oy + 3, oz, DEEP)
  _set(v, ox + 2, oy + 5, oz + 2, TORCH)
  _set(v, ox + 5, oy + 2, oz + 3, CHEST)
  return v


def _generate_epic_builds_suspended_house() -> np.ndarray:
  LOG = _b("dark_oak_log")
  DEEP = _b("dark_prismarine")
  STAIR = _b("dark_prismarine_stairs")
  ANVIL = _b("anvil")
  CHAIN = _b("chain")
  LEAVES = _b("flowering_azalea_leaves")
  WALL = _b("red_sandstone_wall")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  _set(v, cx, oy + 16, cz, ANVIL)
  _set(v, cx, oy + 15, cz, CHAIN)
  for y in range(oy, oy + 14):
    rad = 2 + (14 - y) // 4
    for x in range(cx - rad, cx + rad + 1):
      for z in range(cz - rad, cz + rad + 1):
        if abs(x - cx) + abs(z - cz) <= rad:
          _set(v, x, y, z, LOG if y % 2 else DEEP)
  _set(v, cx, oy + 13, cz, STAIR)
  _set(v, cx + 1, oy + 12, cz, LEAVES)
  _set(v, cx - 1, oy + 4, cz, WALL)
  return v


def _generate_epic_builds_fortress() -> np.ndarray:
  PLANK = _b("dark_oak_planks")
  CARPET = _b("red_carpet")
  DEEP = _b("dark_prismarine")
  BRICK = _b("stone_bricks")
  SHELF = _b("bookshelf")
  LANTERN = _b("lantern")
  WALL = _b("red_sandstone_wall")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 11, 1
  _fill_box(v, ox, oy, oz, 14, 9, 10, BRICK, hollow=True)
  for x in range(ox + 1, ox + 13):
    for z in range(oz + 1, oz + 9):
      _set(v, x, oy, z, PLANK)
      if (x + z) % 3 == 0:
        _set(v, x, oy + 1, z, CARPET)
  for x in range(ox + 3, ox + 11, 4):
    _set(v, x, oy + 1, oz + 4, SHELF)
    _set(v, x, oy + 5, oz + 4, LANTERN)
  _set(v, ox, oy + 4, oz, DEEP)
  _set(v, ox + 13, oy + 4, oz + 9, WALL)
  return v


def _generate_epic_builds_water_elevator() -> np.ndarray:
  DEEP = _b("dark_prismarine")
  WATER = _b("water")
  SOUL = _b("soul_sand")
  MAGMA = _b("magma_block")
  TRAP = _b("oak_trapdoor")
  PLANK = _b("dark_oak_planks")
  SIGN = _b("oak_sign")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 14):
    for x in range(cx - 1, cx + 2):
      for z in range(cz - 1, cz + 2):
        edge = x in (cx - 1, cx + 1) or z in (cz - 1, cz + 1)
        if edge:
          _set(v, x, y, z, DEEP)
        else:
          _set(v, x, y, z, WATER)
    if y == oy:
      _set(v, cx, oy, cz, SOUL)
    if y == oy + 13:
      _set(v, cx, oy + 13, cz, MAGMA)
    if y % 4 == 0:
      _set(v, cx + 1, y, cz, TRAP)
      _set(v, cx - 1, y, cz, SIGN)
  _set(v, cx + 2, oy + 6, cz, PLANK)
  return v


def _generate_epic_builds_spiral_staircase() -> np.ndarray:
  LOG = _b("dark_oak_log")
  STAIR = _b("oak_stairs")
  DEEP = _b("dark_prismarine")
  BRICK = _b("stone_bricks")
  TORCH = _b("torch")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 12):
    rad = 3
    for x in range(cx - rad, cx + rad + 1):
      for z in range(cz - rad, cz + rad + 1):
        if (x - cx) ** 2 + (z - cz) ** 2 <= rad ** 2:
          edge = (x - cx) ** 2 + (z - cz) ** 2 >= (rad - 1) ** 2
          if edge:
            _set(v, x, y, z, BRICK if y % 2 else DEEP)
          else:
            _set(v, x, y, z, AIR_B)
    _set(v, cx, y, cz, LOG)
    angle = y % 4
    _set(v, cx + angle - 1, y, cz + 1, STAIR)
    _set(v, cx + 1, y, cz + angle - 1, STAIR)
  _set(v, cx + 2, oy + 8, cz, TORCH)
  return v


def _generate_epic_builds_message_train() -> np.ndarray:
  STONE = _b("stone")
  RAIL = _b("rail")
  PRAIL = _b("powered_rail")
  CART = _b("hopper_minecart")
  CHEST = _b("chest")
  HOPPER = _b("hopper")
  PLANK = _b("dark_oak_planks")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 13, 2
  for x in range(ox, ox + 12):
    _set(v, x, oy - 1, oz + 2, STONE)
    _set(v, x, oy, oz + 2, RAIL if x % 2 else PRAIL)
  _set(v, ox + 5, oy, oz + 2, CART)
  _set(v, ox, oy, oz + 3, CHEST)
  _set(v, ox, oy - 1, oz + 3, HOPPER)
  for y in range(oy, oy + 6):
    _set(v, ox + 11, y, oz + 1, PLANK)
  return v


def _generate_epic_builds_bridge_supports() -> np.ndarray:
  LOG = _b("dark_oak_log")
  DEEP = _b("dark_prismarine")
  PLANK = _b("dark_oak_planks")
  FENCE = _b("oak_fence")
  WALL = _b("red_sandstone_wall")
  LEAVES = _b("flowering_azalea_leaves")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 16):
    _set(v, cx, y, cz, LOG)
    _set(v, cx + 1, y, cz, DEEP)
  for level in range(4):
    ly = oy + 3 + level * 4
    for dx in range(-3, 4):
      for dz in range(-2, 3):
        _set(v, cx + dx, ly, cz + dz, PLANK if dx != 0 else FENCE)
    _set(v, cx + 3, ly, cz, WALL)
  _set(v, cx + 2, oy + 14, cz + 1, LEAVES)
  return v


def _generate_epic_builds_elytra_launcher() -> np.ndarray:
  PURPLE = _b("purple_concrete")
  SPISTON = _b("sticky_piston")
  SLIME = _b("slime_block")
  OBS = _b("observer")
  DISP = _b("dispenser")
  COBS = _b("crying_obsidian")
  REPEATER = _b("redstone_repeater")
  PLATE = _b("stone_pressure_plate")
  RTORCH = _b("redstone_torch")
  DUST = _b("redstone_dust")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 12, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 5):
      _set(v, x, oy, z, PURPLE)
  _set(v, ox + 3, oy + 1, oz + 2, SPISTON)
  _set(v, ox + 3, oy + 2, oz + 2, SLIME)
  _set(v, ox + 4, oy + 1, oz + 3, OBS)
  _set(v, ox + 5, oy + 2, oz + 2, DISP)
  _set(v, ox + 2, oy + 2, oz + 2, DISP)
  for x, z in ((ox + 2, oz + 1), (ox + 4, oz + 1), (ox + 3, oz + 3)):
    _set(v, x, oy + 1, z, COBS)
  _set(v, ox + 1, oy + 1, oz + 2, REPEATER)
  _set(v, ox + 3, oy + 1, oz + 1, PLATE)
  _set(v, ox + 2, oy + 1, oz + 3, RTORCH)
  _set(v, ox + 4, oy + 1, oz + 4, DUST)
  return v


def _generate_epic_builds_earth_arena() -> np.ndarray:
  PODZOL = _b("podzol")
  DIRT = _b("coarse_dirt")
  GRASS = _b("grass_block")
  OBS = _b("obsidian")
  BRICK = _b("stone_bricks")
  CACTUS = _b("cactus")
  SAND = _b("sand")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 11, 1
  for x in range(ox, ox + 12):
    for z in range(oz, oz + 10):
      _set(v, x, oy, z, PODZOL if (x + z) % 2 else DIRT)
  for y in range(oy + 1, oy + 8):
    _set(v, ox + 5, y, oz + 4, OBS)
  _set(v, ox + 2, oy + 1, oz + 2, CACTUS)
  _set(v, ox + 9, oy, oz + 7, SAND)
  _set(v, ox + 1, oy + 1, oz + 8, BRICK)
  return v


def _generate_epic_builds_nether_arena() -> np.ndarray:
  NETH = _b("netherrack")
  BRICK = _b("nether_bricks")
  LAVA = _b("lava")
  STEM = _b("crimson_stem")
  SOUL = _b("soul_sand")
  MAGMA = _b("magma_block")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 11, 1
  for x in range(ox, ox + 12):
    for z in range(oz, oz + 10):
      _set(v, x, oy, z, NETH if (x + z) % 3 else BRICK)
  for x in range(ox + 3, ox + 9):
    _set(v, x, oy, oz + 4, LAVA)
    _set(v, x, oy + 1, oz + 5, STEM)
  _set(v, ox + 5, oy, oz + 2, SOUL)
  _set(v, ox + 8, oy, oz + 7, MAGMA)
  return v


def _generate_epic_builds_ocean_arena() -> np.ndarray:
  WATER = _b("water")
  PRISM = _b("prismarine")
  DEEP = _b("dark_prismarine")
  LANTERN = _b("sea_lantern")
  CHEST = _b("chest")
  OBS = _b("obsidian")
  QUARTZ = _b("quartz_block")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 10, 1
  for x in range(ox, ox + 12):
    for z in range(oz, oz + 12):
      for y in range(oy, oy + 5):
        _set(v, x, y, z, WATER if y < oy + 4 else AIR_B)
  for px, pz in ((ox + 3, oz + 3), (ox + 8, oz + 5), (ox + 5, oz + 9)):
    for y in range(oy, oy + 6):
      _set(v, px, y, pz, OBS if y < oy + 5 else CHEST)
    _set(v, px, oy + 4, pz, LANTERN)
  _set(v, ox + 6, oy + 2, oz + 6, PRISM)
  _set(v, ox + 7, oy + 3, oz + 7, DEEP)
  _set(v, ox + 4, oy + 5, oz + 4, QUARTZ)
  return v


def _generate_epic_builds_escape_portal() -> np.ndarray:
  QUARTZ = _b("quartz_block")
  STAIR = _b("quartz_stairs")
  FRAME = _b("end_portal_frame")
  EYE = _b("ender_eye")
  OBS = _b("obsidian")
  LANTERN = _b("sea_lantern")
  PURPLE = _b("purple_concrete")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 2
  for y in range(oy, oy + 6):
    for x in range(cx - 4, cx + 5):
      for z in range(cz - 4, cz + 5):
        if (x - cx) ** 2 + (z - cz) ** 2 <= 16:
          _set(v, x, y, z, QUARTZ if y == oy else STAIR if y == oy + 1 else AIR_B)
  for angle, (dx, dz) in enumerate(((3, 0), (0, 3), (-3, 0), (0, -3))):
    _set(v, cx + dx, oy, cz + dz, FRAME)
    if angle == 0:
      _set(v, cx + dx, oy, cz + dz, EYE)
  _set(v, cx, oy + 1, cz, OBS)
  _set(v, cx, oy + 5, cz, LANTERN)
  _set(v, cx + 4, oy + 3, cz, PURPLE)
  return v


def _generate_epic_builds_grandstand() -> np.ndarray:
  QUARTZ = _b("quartz_block")
  SMOOTH = _b("smooth_quartz")
  PURPLE = _b("purple_concrete")
  PURPUR = _b("purpur_block")
  STAIR = _b("quartz_stairs")
  SBSTAIR = _b("stone_brick_stairs")
  LANTERN = _b("sea_lantern")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 11, 1
  for tier in range(5):
    ty = oy + tier * 2
    for x in range(ox, ox + 16):
      for z in range(oz, oz + 3):
        _set(v, x, ty, oz + z, QUARTZ if tier % 2 else PURPLE)
        _set(v, x, ty + 1, oz + z, STAIR if z == 0 else SBSTAIR)
    _set(v, ox + 7, ty + 2, oz + 1, LANTERN)
  _set(v, ox, oy, oz, PURPUR)
  _set(v, ox + 15, oy + 8, oz + 2, SMOOTH)
  return v


def _generate_epic_builds_arming_chamber() -> np.ndarray:
  PURPLE = _b("purple_concrete")
  QUARTZ = _b("quartz_block")
  CHEST = _b("chest")
  FRAME = _b("item_frame")
  ANVIL = _b("anvil")
  PURPUR = _b("purpur_block")
  LANTERN = _b("lantern")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 12, 1
  _fill_box(v, ox, oy, oz, 10, 7, 8, PURPLE, hollow=True)
  for x in range(ox + 1, ox + 9, 2):
    for z in range(oz + 1, oz + 7, 2):
      _set(v, x, oy + 1, z, CHEST)
      _set(v, x, oy + 2, z, FRAME)
  _set(v, ox + 4, oy + 1, oz + 4, ANVIL)
  _set(v, ox + 5, oy + 5, oz + 3, LANTERN)
  _set(v, ox, oy + 3, oz, QUARTZ)
  _set(v, ox + 9, oy + 3, oz + 7, PURPUR)
  return v


def _generate_epic_builds_dueling_towers() -> np.ndarray:
  OBS = _b("obsidian")
  GOLD = _b("gold_block")
  CHEST = _b("chest")
  PURPLE = _b("purple_concrete")
  LADDER = _b("ladder")
  LANTERN = _b("sea_lantern")
  BARS = _b("iron_bars")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 16):
    for x in range(cx - 2, cx + 3):
      for z in range(cz - 2, cz + 3):
        edge = x in (cx - 2, cx + 2) or z in (cz - 2, cz + 2)
        if edge:
          _set(v, x, y, z, OBS if y < oy + 14 else GOLD)
        elif x == cx and z == cz:
          _set(v, x, y, z, LADDER)
        elif not edge and y % 4 == 0:
          _set(v, x, y, z, BARS)
  _set(v, cx, oy + 15, cz, CHEST)
  _set(v, cx + 1, oy + 14, cz, LANTERN)
  _set(v, cx - 3, oy + 8, cz, PURPLE)
  return v


def _generate_epic_builds_cactus_pitfall() -> np.ndarray:
  SAND = _b("sand")
  CACTUS = _b("cactus")
  PLATE = _b("stone_pressure_plate")
  STONE = _b("smooth_stone")
  DIRT = _b("coarse_dirt")
  PODZOL = _b("podzol")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 13, 1
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 6):
      _set(v, x, oy, z, SAND)
  for y in range(oy - 4, oy):
    for x in range(ox + 1, ox + 5):
      for z in range(oz + 1, oz + 5):
        _set(v, x, y, z, AIR_B)
  _set(v, ox + 2, oy, oz + 2, CACTUS)
  _set(v, ox + 3, oy, oz + 3, PLATE)
  _set(v, ox + 4, oy, oz + 2, STONE)
  _set(v, ox + 1, oy - 1, oz + 1, DIRT)
  _set(v, ox + 5, oy, oz + 5, PODZOL)
  return v


def _generate_epic_builds_nether_spawner() -> np.ndarray:
  SPAWN = _b("spawner")
  NETH = _b("netherrack")
  BRICK = _b("nether_bricks")
  FIRE = _b("fire")
  BARS = _b("iron_bars")
  SFIRE = _b("soul_fire")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 14, 14, 1
  for x in range(ox, ox + 4):
    for z in range(oz, oz + 4):
      _set(v, x, oy, z, NETH)
  _set(v, ox + 1, oy + 1, oz + 1, SPAWN)
  _set(v, ox + 2, oy + 2, oz + 1, BRICK)
  _set(v, ox, oy + 1, oz + 2, BARS)
  _set(v, ox + 3, oy + 2, oz, FIRE)
  _set(v, ox + 1, oy + 3, oz + 2, SFIRE)
  return v


def _generate_epic_builds_auto_armorer() -> np.ndarray:
  SAND = _b("sandstone")
  SMOOTH = _b("smooth_sandstone")
  DISP = _b("dispenser")
  PLATE = _b("stone_pressure_plate")
  IRON = _b("iron_block")
  CHEST = _b("chest")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 13, 1
  _fill_box(v, ox, oy, oz, 6, 5, 6, SAND, hollow=True)
  for x, z in ((ox, oz + 2), (ox + 5, oz + 2), (ox + 2, oz), (ox + 2, oz + 5)):
    _set(v, x, oy + 2, z, DISP)
  _set(v, ox + 2, oy, oz + 2, PLATE)
  _set(v, ox + 3, oy + 1, oz + 3, IRON)
  _set(v, ox + 1, oy + 1, oz + 1, CHEST)
  _set(v, ox + 4, oy + 4, oz + 4, SMOOTH)
  return v


def _generate_epic_builds_tnt_trap() -> np.ndarray:
  PLATE = _b("stone_pressure_plate")
  SMOOTH = _b("smooth_stone")
  TNT = _b("tnt")
  STONE = _b("stone")
  COBBLE = _b("cobblestone")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 4):
    _set(v, cx, y, cz, TNT if y < oy + 2 else SMOOTH if y == oy + 2 else PLATE)
  _set(v, cx - 1, oy, cz, STONE)
  _set(v, cx + 1, oy + 1, cz, COBBLE)
  return v


def _generate_epic_builds_sinkhole() -> np.ndarray:
  WATER = _b("water")
  MAGMA = _b("magma_block")
  PRISM = _b("prismarine")
  SAND = _b("sand")
  KELP = _b("kelp")
  LANTERN = _b("sea_lantern")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 12, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 8):
      for y in range(oy, oy + 4):
        _set(v, x, y, z, WATER)
  for x in range(ox + 2, ox + 6):
    for z in range(oz + 2, oz + 6):
      for y in range(oy - 2, oy):
        _set(v, x, y, z, AIR_B)
      _set(v, x, oy - 2, z, MAGMA)
  _set(v, ox + 3, oy + 1, oz + 3, PRISM)
  _set(v, ox + 7, oy, oz + 7, SAND)
  _set(v, ox + 4, oy + 2, oz + 4, KELP)
  _set(v, ox + 2, oy + 3, oz + 5, LANTERN)
  return v


def _generate_epic_builds_sand_trap() -> np.ndarray:
  SAND = _b("sand")
  RSAND = _b("red_sand")
  PLATE = _b("stone_pressure_plate")
  PISTON = _b("piston")
  SPAWN = _b("spawner")
  SIGN = _b("oak_sign")
  CACTUS = _b("cactus")
  TERRA = _b("terracotta")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 13, 1
  for y in range(oy - 5, oy):
    for x in range(ox, ox + 5):
      for z in range(oz, oz + 5):
        if y == oy - 5:
          _set(v, x, y, z, TERRA)
        elif y == oy - 1:
          _set(v, x, y, z, SIGN)
        else:
          _set(v, x, y, z, AIR_B)
  _set(v, ox + 2, oy - 5, oz + 2, SPAWN)
  _set(v, ox + 2, oy - 3, oz + 2, PISTON)
  _set(v, ox + 2, oy, oz + 2, PLATE)
  for x in range(ox, ox + 5):
    for z in range(oz, oz + 5):
      _set(v, x, oy, z, SAND if (x + z) % 2 else RSAND)
      _set(v, x, oy + 1, z, SAND)
  _set(v, ox, oy + 2, oz, CACTUS)
  return v


_GENERATORS: dict[str, object] = {
  "epic_builds_hanging_tower": _generate_epic_builds_hanging_tower,
  "epic_builds_landing_pad": _generate_epic_builds_landing_pad,
  "epic_builds_bathhouse": _generate_epic_builds_bathhouse,
  "epic_builds_mountain_corridor": _generate_epic_builds_mountain_corridor,
  "epic_builds_suspended_house": _generate_epic_builds_suspended_house,
  "epic_builds_fortress": _generate_epic_builds_fortress,
  "epic_builds_water_elevator": _generate_epic_builds_water_elevator,
  "epic_builds_spiral_staircase": _generate_epic_builds_spiral_staircase,
  "epic_builds_message_train": _generate_epic_builds_message_train,
  "epic_builds_bridge_supports": _generate_epic_builds_bridge_supports,
  "epic_builds_elytra_launcher": _generate_epic_builds_elytra_launcher,
  "epic_builds_earth_arena": _generate_epic_builds_earth_arena,
  "epic_builds_nether_arena": _generate_epic_builds_nether_arena,
  "epic_builds_ocean_arena": _generate_epic_builds_ocean_arena,
  "epic_builds_escape_portal": _generate_epic_builds_escape_portal,
  "epic_builds_grandstand": _generate_epic_builds_grandstand,
  "epic_builds_arming_chamber": _generate_epic_builds_arming_chamber,
  "epic_builds_dueling_towers": _generate_epic_builds_dueling_towers,
  "epic_builds_cactus_pitfall": _generate_epic_builds_cactus_pitfall,
  "epic_builds_nether_spawner": _generate_epic_builds_nether_spawner,
  "epic_builds_auto_armorer": _generate_epic_builds_auto_armorer,
  "epic_builds_tnt_trap": _generate_epic_builds_tnt_trap,
  "epic_builds_sinkhole": _generate_epic_builds_sinkhole,
  "epic_builds_sand_trap": _generate_epic_builds_sand_trap,
}
