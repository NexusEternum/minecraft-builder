"""Procedural generators for Minecraft Epic Inventions modular builds."""

from __future__ import annotations

import numpy as np

from ..data.palette import AIR
from .epic_inventions_registry import EPIC_INVENTIONS_BUILDS


def generate_epic_inventions_build(build_id: str) -> np.ndarray:
  if build_id not in EPIC_INVENTIONS_BUILDS:
    raise KeyError(f"Unknown epic inventions build: {build_id}")
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


def _generate_epic_inventions_mob_hospital() -> np.ndarray:
  """Mob Hospital — book estimate: 20×20×15 L-shaped two-story clinic."""
  SSAND = _b("smooth_sandstone")
  SAND = _b("sandstone")
  ORANGE = _b("orange_terracotta")
  GRASS = _b("grass_block")
  GLASS = _b("glass_pane")
  FENCE = _b("birch_fence")
  LEAVES = _b("oak_leaves")
  PLANK = _b("birch_planks")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 6, 6, 1
  # L footprint: main 14×12 + wing 8×8 at back-left
  main_w, main_d = 14, 12
  wing_w, wing_d = 8, 8

  for x in range(ox, ox + main_w):
    for z in range(oz, oz + main_d):
      _set(v, x, oy, z, SAND)
  for x in range(ox, ox + wing_w):
    for z in range(oz + main_d - 2, oz + main_d - 2 + wing_d):
      _set(v, x, oy, z, SAND)

  for y in range(oy + 1, oy + 8):
    for x in range(ox, ox + main_w):
      for z in range(oz, oz + main_d):
        edge = x in (ox, ox + main_w - 1) or z in (oz, oz + main_d - 1)
        if not edge:
          _set(v, x, y, z, AIR_B)
          continue
        if y in (oy + 3, oy + 6):
          _set(v, x, y, z, ORANGE)
        elif z == oz and x in (ox + 5, ox + 6) and y <= oy + 2:
          _set(v, x, y, z, GLASS if y == oy + 2 else AIR_B)
        elif z == oz + main_d - 1 and x == ox + 7 and oy + 1 < y < oy + 4:
          _set(v, x, y, z, GLASS)
        else:
          _set(v, x, y, z, SSAND)

  # Wing walls
  wx, wz = ox, oz + main_d - 2
  for y in range(oy + 1, oy + 6):
    for x in range(wx, wx + wing_w):
      for z in range(wz, wz + wing_d):
        edge = x in (wx, wx + wing_w - 1) or z in (wz, wz + wing_d - 1)
        if edge:
          _set(v, x, y, z, SSAND if y != oy + 3 else ORANGE)
        else:
          _set(v, x, y, z, AIR_B)

  # Interior floors
  for x in range(ox + 1, ox + main_w - 1):
    for z in range(oz + 1, oz + main_d - 1):
      _set(v, x, oy + 1, z, PLANK)
      _set(v, x, oy + 4, z, PLANK)

  # Roof gardens
  for x in range(ox, ox + main_w):
    for z in range(oz, oz + main_d):
      _set(v, x, oy + 8, z, GRASS)
      if x in (ox, ox + main_w - 1) or z in (oz, oz + main_d - 1):
        _set(v, x, oy + 9, z, FENCE)
      elif (x + z) % 5 == 0:
        _set(v, x, oy + 9, z, LEAVES)
  for x in range(wx, wx + wing_w):
    for z in range(wz, wz + wing_d):
      _set(v, x, oy + 5, z, GRASS)

  return v


def _generate_epic_inventions_sanctuary_farm() -> np.ndarray:
  """Sanctuary Farm — book estimate: 25×20×8 crop plot with twin huts."""
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  FARM = _b("farmland")
  WHEAT = _b("wheat")
  CARROT = _b("carrots")
  BEET = _b("beetroots")
  DPLANK = _b("dark_oak_planks")
  DLOG = _b("dark_oak_log")
  STONE = _b("stone_bricks")
  COMP = _b("composter")
  LEAVES = _b("oak_leaves")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 3, 6, 1
  fw, fd = 25, 20

  for x in range(ox, ox + fw):
    for z in range(oz, oz + fd):
      _set(v, x, oy - 1, z, DIRT)
      _set(v, x, oy, z, GRASS)

  # Crop rows
  for x in range(ox + 6, ox + fw - 2):
    for z in range(oz + 2, oz + fd - 2):
      _set(v, x, oy, z, FARM)
      crop = WHEAT if (x + z) % 3 == 0 else CARROT if (x + z) % 3 == 1 else BEET
      _set(v, x, oy + 1, z, crop)

  # Hedge border
  for x in range(ox, ox + fw):
    for z in (oz, oz + fd - 1):
      _set(v, x, oy + 1, z, LEAVES)
  for z in range(oz, oz + fd):
    for x in (ox, ox + fw - 1):
      _set(v, x, oy + 1, z, LEAVES)

  # Twin huts
  for hx, hz in ((ox + 1, oz + 2), (ox + 1, oz + 10)):
    for x in range(hx, hx + 6):
      for z in range(hz, hz + 5):
        _set(v, x, oy, z, STONE)
    for y in range(oy + 1, oy + 5):
      for x in range(hx, hx + 6):
        for z in range(hz, hz + 5):
          edge = x in (hx, hx + 5) or z in (hz, hz + 4)
          corner = x in (hx, hx + 5) and z in (hz, hz + 4)
          if edge:
            _set(v, x, y, z, DLOG if corner else DPLANK)
          else:
            _set(v, x, y, z, AIR_B)
    for x in range(hx, hx + 6):
      for z in range(hz, hz + 5):
     	  _set(v, x, oy + 5, z, DPLANK)
    _set(v, hx + 2, oy + 1, hz + 2, COMP)

  return v


def _generate_epic_inventions_sanctuary_tower() -> np.ndarray:
  """Sanctuary Tower — book estimate: 8×8×25 watchtower."""
  SSAND = _b("smooth_sandstone")
  SAND = _b("sandstone")
  FENCE = _b("oak_fence")
  TRAP = _b("oak_trapdoor")
  PLANK = _b("oak_planks")
  LADDER = _b("ladder")
  DSTAIR = _b("dark_oak_stairs")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 12, 1
  s = 8
  cx, cz = ox + 4, oz + 4

  for y in range(oy, oy + 22):
    for x in range(ox, ox + s):
      for z in range(oz, oz + s):
        edge = x in (ox, ox + s - 1) or z in (oz, oz + s - 1)
        inset = 1 if y > oy + 4 else 0
        if edge and (x in (ox + inset, ox + s - 1 - inset) or z in (oz + inset, oz + s - 1 - inset)):
          _set(v, x, y, z, SSAND if y % 3 else SAND)
        elif not edge:
          _set(v, x, y, z, AIR_B)
    _set(v, ox + s - 1, y, cz, LADDER)

  # Exterior trapdoor ladder
  for y in range(oy + 1, oy + 20, 2):
    _set(v, ox - 1, y, cz, TRAP)

  # Observation deck
  deck_y = oy + 22
  for x in range(ox, ox + s):
    for z in range(oz, oz + s):
      _set(v, x, deck_y, z, PLANK)
      if x in (ox, ox + s - 1) or z in (oz, oz + s - 1):
        _set(v, x, deck_y + 1, z, FENCE)

  # Peaked cap
  for layer in range(2):
    for x in range(ox + layer, ox + s - layer):
      for z in range(oz + layer, oz + s - layer):
        if x in (ox + layer, ox + s - 1 - layer) or z in (oz + layer, oz + s - 1 - layer):
          _set(v, x, deck_y + 2 + layer, z, DSTAIR)

  return v


def _generate_epic_inventions_bee_habitat() -> np.ndarray:
  """Bee Habitat — book estimate: 25×25×20 terrain chunk."""
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  STONE = _b("stone")
  WATER = _b("water")
  OLOG = _b("oak_log")
  LEAVES = _b("oak_leaves")
  NEST = _b("bee_nest")
  POPPY = _b("poppy")
  DAND = _b("dandelion")
  CORN = _b("cornflower")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 3, 3, 4
  w, d = 25, 25
  cx, cz = ox + 12, oz + 12

  for x in range(ox, ox + w):
    for z in range(oz, oz + d):
      dist = abs(x - cx) + abs(z - cz)
      if dist > 14:
        continue
      for y in range(oy - 3, oy):
        _set(v, x, y, z, STONE if y < oy - 2 else DIRT)
      _set(v, x, oy, z, GRASS)

  # Pond
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      _set(v, x, oy, z, WATER)

  # Trees with bee nests
  for tx, tz in ((ox + 5, oz + 6), (ox + 18, oz + 8), (ox + 8, oz + 18), (ox + 17, oz + 17)):
    for y in range(oy + 1, oy + 6):
      _set(v, tx, y, tz, OLOG)
    for dy in range(4, 7):
      for dx in range(-2, 3):
        for dz in range(-2, 3):
          if abs(dx) + abs(dz) <= 2:
            _set(v, tx + dx, oy + dy, tz + dz, LEAVES)
    _set(v, tx, oy + 4, tz, NEST)

  # Flowers
  for x in range(ox + 2, ox + w - 2, 3):
    for z in range(oz + 2, oz + d - 2, 4):
      if v[x, oy, z] == GRASS:
        flower = POPPY if (x + z) % 3 == 0 else DAND if (x + z) % 3 == 1 else CORN
        _set(v, x, oy + 1, z, flower)

  return v


def _generate_epic_inventions_marine_sanctuary() -> np.ndarray:
  """Marine Sanctuary — book estimate: 15×15×25 glass tank."""
  GLASS = _b("light_blue_stained_glass")
  WATER = _b("water")
  SAND = _b("sand")
  KELP = _b("kelp")
  SEA = _b("seagrass")
  CONDUIT = _b("conduit")
  PRISM = _b("prismarine")
  LANTERN = _b("sea_lantern")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 8, 1
  s = 15
  cx, cz = ox + 7, oz + 7

  for y in range(oy, oy + 24):
    for x in range(ox, ox + s):
      for z in range(oz, oz + s):
        edge = x in (ox, ox + s - 1) or z in (oz, oz + s - 1) or y in (oy, oy + 23)
        if edge:
          _set(v, x, y, z, GLASS)
        else:
          _set(v, x, y, z, WATER)

  for x in range(ox + 1, ox + s - 1):
    for z in range(oz + 1, oz + s - 1):
      _set(v, x, oy, z, SAND)
      if (x + z) % 4 == 0:
        _set(v, x, oy + 1, z, SEA)

  for x in range(ox + 2, ox + s - 2, 2):
    for z in range(oz + 2, oz + s - 2, 3):
      for y in range(oy + 1, oy + 10):
        _set(v, x, y, z, KELP)

  _set(v, cx, oy, cz, PRISM)
  _set(v, cx, oy + 1, cz, LANTERN)
  _set(v, cx, oy + 2, cz, CONDUIT)

  return v


def _generate_epic_inventions_horse_stable() -> np.ndarray:
  """Horse Stable — book estimate: 10×8×6 open shelter."""
  FENCE = _b("oak_fence")
  PLANK = _b("oak_planks")
  SLAB = _b("oak_slab")
  TRAP = _b("oak_trapdoor")
  HAY = _b("hay_block")
  GRASS = _b("grass_block")
  GATE = _b("oak_fence_gate")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 12, 1
  w, d = 10, 8

  for x in range(ox, ox + w):
    for z in range(oz, oz + d):
      _set(v, x, oy - 1, z, GRASS)
      _set(v, x, oy, z, HAY)

  for y in range(oy + 1, oy + 5):
    for px, pz in ((ox, oz), (ox + w - 1, oz), (ox, oz + d - 1), (ox + w - 1, oz + d - 1)):
      _set(v, px, y, pz, FENCE)

  for x in range(ox, ox + w):
    for z in range(oz, oz + d):
      _set(v, x, oy + 5, z, SLAB if (x + z) % 2 else TRAP)

  _set(v, ox + w // 2, oy + 1, oz, GATE)

  return v


def _generate_epic_inventions_forcefield_emitter() -> np.ndarray:
  """Forcefield Emitter — book estimate: 7×7 pedestal + tall pink glass panel."""
  RSAND = _b("red_sand")
  SSAND = _b("smooth_sandstone")
  QUARTZ = _b("quartz_block")
  GOLD = _b("gold_block")
  PINK = _b("pink_stained_glass")
  LANTERN = _b("sea_lantern")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 12, 1
  s = 7
  cx, cz = ox + 3, oz + 3

  for x in range(ox, ox + s):
    for z in range(oz, oz + s):
      _set(v, x, oy - 1, z, RSAND)

  for y in range(oy, oy + 6):
    for x in range(ox + 1, ox + s - 1):
      for z in range(oz + 1, oz + s - 1):
        _set(v, x, y, z, SSAND if y < 5 else QUARTZ)
  for px, pz in ((ox + 1, oz + 1), (ox + s - 2, oz + 1), (ox + 1, oz + s - 2), (ox + s - 2, oz + s - 2)):
    for y in range(oy, oy + 7):
      _set(v, px, y, pz, QUARTZ)
  _set(v, cx, oy + 3, cz, LANTERN)
  _set(v, cx, oy + 6, cz, GOLD)

  # Pink forcefield panel
  wall_x = ox + s
  for y in range(oy + 1, oy + 28):
    for z in range(oz, oz + s):
      _set(v, wall_x, y, z, PINK)
      if y % 4 == 0:
        _set(v, wall_x - 1, y, z, LANTERN)

  return v


def _generate_epic_inventions_villager_housing() -> np.ndarray:
  """Villager Housing — book estimate: 16×16×14 earth-sheltered hill."""
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  STONE = _b("stone")
  GLASS = _b("glass_pane")
  FENCE = _b("oak_fence")
  DOOR = _b("oak_door")
  DETECT = _b("daylight_detector")
  SPLANK = _b("spruce_planks")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 8, 1
  s = 16

  for x in range(ox, ox + s):
    for z in range(oz, oz + s):
      for y in range(oy, oy + 10):
        dist = max(abs(x - (ox + 7)), abs(z - (oz + 7)))
        if dist <= 7 - y // 2:
          mat = GRASS if y == oy + 9 else DIRT if y > oy + 2 else STONE
          _set(v, x, oy + y, z, mat)

  # Skylights
  for sx, sz in ((ox + 4, oz + 4), (ox + 10, oz + 9)):
    _set(v, sx, oy + 9, sz, GLASS)
    _set(v, sx + 1, oy + 9, sz, GLASS)
    _set(v, sx, oy + 10, sz, DETECT)

  # Buried rooms
  for x in range(ox + 3, ox + 13):
    for z in range(oz + 3, oz + 11):
      for y in range(oy + 4, oy + 8):
        _set(v, x, y, z, AIR_B)
      _set(v, x, oy + 4, z, SPLANK)

  # Front entrances
  for dx, dz in ((0, 6), (0, 9)):
    for y in range(oy + 5, oy + 8):
      _set(v, ox, y, oz + dz, DOOR if y < oy + 7 else AIR_B)
    for fy in range(oy + 5, oy + 7):
      _set(v, ox - 1, fy, oz + dz - 1, FENCE)
      _set(v, ox - 1, fy, oz + dz + 1, FENCE)

  return v


def _generate_epic_inventions_mob_feeder() -> np.ndarray:
  """Mob Feeder — book estimate: 7×7×7 dispenser platform."""
  GRASS = _b("grass_block")
  STONE = _b("stone_bricks")
  SSAND = _b("smooth_sandstone")
  DISP = _b("dispenser")
  CHEST = _b("chest")
  HOPPER = _b("hopper")
  PLATE = _b("heavy_weighted_pressure_plate")
  PLANK = _b("oak_planks")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 12, 1
  s = 7
  cx, cz = ox + 3, oz + 3

  for x in range(ox - 1, ox + s + 1):
    for z in range(oz - 1, oz + s + 1):
      _set(v, x, oy - 1, z, GRASS)

  for x in range(ox, ox + s):
    for z in range(oz, oz + s):
      _set(v, x, oy, z, STONE)

  for y in range(oy + 1, oy + 3):
    for x in range(ox + 1, ox + s - 1):
      for z in range(oz + 1, oz + s - 1):
        _set(v, x, y, z, SSAND)

  _set(v, cx, oy, cz, AIR_B)
  _set(v, cx, oy - 1, cz, HOPPER)
  _set(v, cx, oy + 3, cz, PLATE)

  for dx, dz in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
    px, pz = cx + dx, cz + dz
    _set(v, px, oy + 3, pz, DISP)
    _set(v, px, oy + 4, pz, CHEST)

  return v


def _generate_epic_inventions_water_trough() -> np.ndarray:
  """Automatic Water Trough — book estimate: 20×5×5 channel."""
  GRASS = _b("grass_block")
  WATER = _b("water")
  DPLANK = _b("dark_oak_planks")
  DSLAB = _b("dark_oak_slab")
  BARS = _b("iron_bars")
  BANNER = _b("light_blue_banner")
  SLAB = _b("stone_brick_slab")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 6, 13, 1
  length, width = 20, 5

  for x in range(ox, ox + length):
    for z in range(oz, oz + width):
      _set(v, x, oy - 1, z, GRASS)

  for x in range(ox + 1, ox + length - 1):
    for z in range(oz + 1, oz + width - 1):
      _set(v, x, oy, z, WATER)

  for x in range(ox, ox + length):
    for z in (oz, oz + width - 1):
      _set(v, x, oy, z, DPLANK)
      _set(v, x, oy + 1, z, DSLAB)

  for z in range(oz, oz + width):
    for x in (ox, ox + length - 1):
      for y in range(oy, oy + 4):
        _set(v, x, y, z, BARS)
      _set(v, x, oy + 4, oz + 2, BANNER)

  for x in range(ox, ox + length, 4):
    _set(v, x, oy - 1, oz - 1, SLAB)
    _set(v, x, oy - 1, oz + width, SLAB)

  return v


def _generate_epic_inventions_pumpkin_farm() -> np.ndarray:
  """Pumpkin Farm — book estimate: 10×12×8 courtyard plot."""
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  PUMP = _b("pumpkin")
  OLOG = _b("oak_log")
  LEAVES = _b("oak_leaves")
  FENCE = _b("oak_fence")
  CHEST = _b("chest")
  LANTERN = _b("lantern")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 10, 1
  w, d = 10, 12

  for x in range(ox, ox + w):
    for z in range(oz, oz + d):
      _set(v, x, oy - 1, z, DIRT)
      _set(v, x, oy, z, GRASS)

  for x in range(ox + 2, ox + w - 1, 2):
    for z in range(oz + 2, oz + d - 1, 3):
      _set(v, x, oy + 1, z, PUMP)

  tx, tz = ox + 2, oz + 2
  for y in range(oy + 1, oy + 5):
    _set(v, tx, y, tz, OLOG)
  for dy in range(4, 7):
    for dx in range(-2, 3):
      for dz in range(-2, 3):
        if abs(dx) + abs(dz) <= 2:
          _set(v, tx + dx, oy + dy, tz + dz, LEAVES)

  for x in range(ox, ox + w):
    for z in (oz, oz + d - 1):
      _set(v, x, oy + 1, z, FENCE)
  for z in range(oz, oz + d):
    for x in (ox, ox + w - 1):
      _set(v, x, oy + 1, z, FENCE)

  _set(v, ox + w - 2, oy + 1, oz + d - 2, CHEST)
  _set(v, ox + w - 2, oy + 2, oz + d - 2, LANTERN)
  return v


def _generate_epic_inventions_enchanting_tower() -> np.ndarray:
  """Enchanting Tower — book estimate: 20 block diameter circular library."""
  DTILE = _b("deepslate_tiles")
  STONE = _b("stone_bricks")
  SHELF = _b("bookshelf")
  ENCH = _b("enchanting_table")
  CARPET = _b("pink_carpet")
  CANDLE = _b("candle")
  BANNER = _b("purple_banner")
  SLAB = _b("stone_brick_slab")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  r_outer, r_inner = 10, 7

  for x in range(cx - r_outer, cx + r_outer + 1):
    for z in range(cz - r_outer, cz + r_outer + 1):
      dist2 = (x - cx) ** 2 + (z - cz) ** 2
      if r_inner ** 2 < dist2 <= r_outer ** 2:
        _set(v, x, oy, z, STONE)
      elif dist2 <= r_inner ** 2:
        _set(v, x, oy, z, CARPET)

  for y in range(oy + 1, oy + 12):
    for x in range(cx - r_outer, cx + r_outer + 1):
      for z in range(cz - r_outer, cz + r_outer + 1):
        dist2 = (x - cx) ** 2 + (z - cz) ** 2
        if r_inner ** 2 < dist2 <= r_outer ** 2:
          if y < oy + 5 and y > oy + 1:
            _set(v, x, y, z, SHELF if y < oy + 4 else DTILE)
          else:
            _set(v, x, y, z, DTILE)
        elif dist2 <= r_inner ** 2:
          _set(v, x, y, z, AIR_B)

  _set(v, cx, oy + 1, cz, ENCH)

  for y in range(oy + 12, oy + 15):
    for x in range(cx - r_outer, cx + r_outer + 1):
      for z in range(cz - r_outer, cz + r_outer + 1):
        if (x - cx) ** 2 + (z - cz) ** 2 <= r_outer ** 2:
          edge = (x - cx) ** 2 + (z - cz) ** 2 >= (r_outer - 1) ** 2
          _set(v, x, y, z, SLAB if edge else CARPET)
          if edge and (x + z + y) % 3 == 0:
            _set(v, x, y + 1, z, CANDLE)
          if edge and x == cx + r_outer - 1:
            _set(v, x, y, z, BANNER)
  return v


def _generate_epic_inventions_gothic_buttress() -> np.ndarray:
  """Gothic Buttress — book estimate: arched flying support ~8×22×12."""
  STONE = _b("stone_bricks")
  STAIRS = _b("stone_brick_stairs")
  SLAB = _b("stone_brick_slab")
  WALL = _b("stone_brick_wall")
  DTILE = _b("deepslate_tiles")
  BASALT = _b("polished_basalt")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 10, 1

  # Main wall pier
  for y in range(oy, oy + 20):
    for x in range(ox, ox + 3):
      _set(v, x, y, oz, BASALT if y % 4 == 0 else DTILE)
  for y in range(oy, oy + 18):
    _set(v, ox + 3, y, oz, STONE)

  # Flying arch
  for step in range(8):
    y = oy + 8 + step
    _set(v, ox + 4 + step, y, oz + step, STAIRS)
    _set(v, ox + 4 + step, y, oz + step + 1, SLAB)
  for y in range(oy + 4, oy + 10):
    _set(v, ox + 11, y, oz + 7, WALL)

  # Second buttress mirror
  for y in range(oy, oy + 16):
    _set(v, ox + 12, y, oz + 10, STONE)
  for step in range(6):
    y = oy + 6 + step
    _set(v, ox + 10 - step, y, oz + 10, STAIRS)

  return v


def _generate_epic_inventions_stained_glass_window() -> np.ndarray:
  """Gothic window — book estimate: 11×28 pointed arch panel."""
  STONE = _b("stone_bricks")
  DTILE = _b("deepslate_tiles")
  STAIRS = _b("stone_brick_stairs")
  PURPLE = _b("purple_stained_glass")
  BLACK = _b("black_stained_glass")
  LANTERN = _b("lantern")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 15, 1
  w, h = 11, 28

  for y in range(oy, oy + h):
    for x in range(ox, ox + w):
      _set(v, x, y, oz, STONE if x in (ox, ox + w - 1) else DTILE)
      _set(v, x, y, oz + 1, STONE if x in (ox, ox + w - 1) else DTILE)

  # Pointed arch top
  for layer in range(6):
    inset = layer
    y = oy + h - 6 + layer
    for x in range(ox + inset, ox + w - inset):
      _set(v, x, y, oz, STAIRS)
      _set(v, x, y, oz + 1, STAIRS)

  # Glass tracery
  for y in range(oy + 3, oy + h - 4):
    for x in range(ox + 2, ox + w - 2):
      glass = PURPLE if (x + y) % 3 else BLACK
      _set(v, x, y, oz, glass)
      if y > oy + 5:
        _set(v, x, y, oz + 1, glass)

  _set(v, ox + w // 2, oy + 2, oz - 1, LANTERN)
  return v


def _generate_epic_inventions_golem_maker() -> np.ndarray:
  """Golem Maker — book estimate: 11×11×10 redstone assembly core."""
  LIME = _b("lime_concrete")
  DUST = _b("redstone_dust")
  REPEAT = _b("redstone_repeater")
  PISTON = _b("piston")
  DISP = _b("dispenser")
  IRON = _b("iron_block")
  PUMP = _b("carved_pumpkin")
  CHEST = _b("chest")
  LEVER = _b("lever")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 10, 1
  s = 11
  cx, cz = ox + 5, oz + 5

  for x in range(ox, ox + s):
    for z in range(oz, oz + s):
      _set(v, x, oy, z, LIME)

  # Cross arms
  for i in range(s):
    _set(v, ox + i, oy, cz, LIME)
    _set(v, cx, oy, oz + i, LIME)

  # Iron assembly pad
  for dx, dz in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)):
    _set(v, cx + dx, oy + 1, cz + dz, IRON)
  _set(v, cx, oy + 2, cz, PUMP)

  # Pistons facing center
  for dx, dz in ((-3, 0), (3, 0), (0, -3), (0, 3)):
    _set(v, cx + dx, oy + 1, cz + dz, PISTON)

  # Redstone lines + repeaters
  for dx in range(-4, 5):
    _set(v, cx + dx, oy, cz - 4, DUST)
    _set(v, cx + dx, oy, cz + 4, DUST)
  for dz in range(-4, 5):
    _set(v, cx - 4, oy, cz + dz, DUST)
    _set(v, cx + 4, oy, cz + dz, DUST)
  for px, pz in ((cx - 2, cz), (cx + 2, cz), (cx, cz - 2), (cx, cz + 2)):
    _set(v, px, oy, pz, REPEAT)

  _set(v, cx, oy + 3, cz, DISP)
  _set(v, ox + 1, oy + 1, oz + 1, CHEST)
  _set(v, ox + s - 2, oy + 1, oz + 1, LEVER)
  return v


def _generate_epic_inventions_storm_catcher() -> np.ndarray:
  """Storm Catcher — book estimate: 6×6×28 lightning spire."""
  DTILE = _b("deepslate_tiles")
  BASALT = _b("polished_basalt")
  LGLASS = _b("lime_stained_glass")
  ROD = _b("lightning_rod")
  LANTERN = _b("lantern")
  BARS = _b("iron_bars")
  LAMP = _b("redstone_lamp")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 13, 1
  s = 6
  cx, cz = ox + 2, oz + 2

  for y in range(oy, oy + 26):
    for px, pz in ((ox, oz), (ox + s - 1, oz), (ox, oz + s - 1), (ox + s - 1, oz + s - 1)):
      _set(v, px, y, pz, BASALT if y % 3 else DTILE)
    for px in range(ox + 1, ox + s - 1):
      _set(v, px, y, oz, BARS)
      _set(v, px, y, oz + s - 1, BARS)
    for pz in range(oz + 1, oz + s - 1):
      _set(v, ox, y, pz, BARS)
      _set(v, ox + s - 1, y, pz, BARS)
    _set(v, cx, y, cz, LGLASS if y % 2 else LAMP)

  for y in range(oy + 24, oy + 28):
    _set(v, cx, y, cz, ROD)
  for px in range(ox, ox + s):
    for pz in range(oz, oz + s):
      if (px + pz) % 2 == 0:
        _set(v, px, oy + 22, pz, LANTERN)
  return v


def _generate_epic_inventions_golem_factory_ring() -> np.ndarray:
  """Golem Factory Ring — book estimate: 26 diameter circular wall."""
  DTILE = _b("deepslate_tiles")
  BASALT = _b("polished_basalt")
  STONE = _b("stone_bricks")
  LANTERN = _b("lantern")
  RTORCH = _b("redstone_torch")
  BARS = _b("iron_bars")
  BLACK = _b("blackstone")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  r_outer, r_inner = 13, 10
  wall_h = 9

  for x in range(cx - r_outer, cx + r_outer + 1):
    for z in range(cz - r_outer, cz + r_outer + 1):
      dist2 = (x - cx) ** 2 + (z - cz) ** 2
      if dist2 <= r_inner ** 2:
        _set(v, x, oy, z, BASALT if (x + z) % 3 else BLACK)

  for y in range(oy + 1, oy + wall_h):
    for x in range(cx - r_outer, cx + r_outer + 1):
      for z in range(cz - r_outer, cz + r_outer + 1):
        dist2 = (x - cx) ** 2 + (z - cz) ** 2
        if r_inner ** 2 < dist2 <= r_outer ** 2:
          _set(v, x, y, z, DTILE if y < wall_h - 1 else STONE)
        elif dist2 <= r_inner ** 2 and y == oy + 1:
          _set(v, x, y, z, AIR_B)

  # Crenellations + glow
  for x in range(cx - r_outer, cx + r_outer + 1):
    for z in range(cz - r_outer, cz + r_outer + 1):
      dist2 = (x - cx) ** 2 + (z - cz) ** 2
      if (r_outer - 1) ** 2 <= dist2 <= r_outer ** 2 and (x + z) % 2 == 0:
        _set(v, x, oy + wall_h, z, STONE)
        _set(v, x, oy + wall_h + 1, z, LANTERN if (x + z) % 4 == 0 else RTORCH)

  # Iron bar gate opening
  for y in range(oy + 1, oy + 5):
    _set(v, cx + r_outer, y, cz, BARS)
    _set(v, cx + r_outer, y, cz + 1, AIR_B)

  return v


def _cloud_blob(v: np.ndarray, cx: int, cz: int, oy: int, rx: int, rz: int, mat: str) -> None:
  for x in range(cx - rx, cx + rx + 1):
    for z in range(cz - rz, cz + rz + 1):
      if ((x - cx) / max(rx, 1)) ** 2 + ((z - cz) / max(rz, 1)) ** 2 <= 1.0:
        _set(v, x, oy, z, mat)


def _rainbow_row(v: np.ndarray, x0: int, z: int, y: int, length: int) -> None:
  colors = (
    _b("red_concrete"),
    _b("orange_concrete"),
    _b("yellow_concrete"),
    _b("lime_concrete"),
    _b("light_blue_concrete"),
    _b("blue_concrete"),
    _b("purple_concrete"),
  )
  for i in range(length):
    _set(v, x0 + i, y, z, colors[i % len(colors)])


def _generate_epic_inventions_cat_shrine() -> np.ndarray:
  """Cat Shrine — book estimate: 10×10×24 totem."""
  WHITE = _b("white_concrete")
  GRAY = _b("gray_concrete")
  LIME = _b("lime_concrete")
  GOLD = _b("gold_block")
  YELLOW = _b("yellow_concrete")
  BLUE = _b("blue_concrete")
  WATER = _b("water")
  BANNER = _b("white_banner")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 11, 1
  cx, cz = ox + 4, oz + 4

  for y in range(oy, oy + 18):
    for x in range(ox + 2, ox + 8):
      for z in range(oz + 2, oz + 8):
        if abs(x - cx) <= 2 and abs(z - cz) <= 2:
          _set(v, x, y, z, WHITE)

  # Cat face bands
  for y in (oy + 12, oy + 14, oy + 16):
    for x in range(cx - 2, cx + 3):
      _set(v, x, y, cz, GRAY if y == oy + 14 else LIME)
  _set(v, cx - 1, oy + 13, cz, LIME)
  _set(v, cx + 1, oy + 13, cz, LIME)
  _set(v, cx, oy + 17, cz, BANNER)

  # Gold halo
  for dx in range(-3, 4):
    for dz in range(-3, 4):
      if 6 <= dx * dx + dz * dz <= 10:
        _set(v, cx + dx, oy + 18, cz + dz, GOLD)

  for y in range(oy, oy + 6):
    _set(v, cx, y, cz + 3, WATER)
  for x in range(ox + 1, ox + 9):
    for z in range(oz + 1, oz + 9):
      _set(v, x, oy, z, BLUE if (x + z) % 2 else YELLOW)
  return v


def _generate_epic_inventions_spectator_stands() -> np.ndarray:
  """Spectator Stands — book estimate: 20×16×15 cloud grandstand."""
  WHITE = _b("white_wool")
  WCONC = _b("white_concrete")
  DSTAIR = _b("dark_oak_stairs")
  DSLAB = _b("dark_oak_slab")
  FENCE = _b("dark_oak_fence")
  PINK = _b("pink_wool")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 6, 8, 1
  w, d = 20, 16

  for tier in range(3):
    ty = oy + tier * 3
    inset = tier * 2
    for x in range(ox + inset, ox + w - inset):
      for z in range(oz + inset, oz + d - inset):
        _set(v, x, ty, z, WHITE if (x + z) % 2 else WCONC)
        if z == oz + inset + 1:
          _set(v, x, ty + 1, z, DSTAIR)
        if z == oz + d - inset - 2:
          _set(v, x, ty + 2, z, FENCE)

  for x in range(ox, ox + w):
    for z in range(oz, oz + 3):
      _set(v, x, oy + 10, z, PINK if (x + z) % 2 else WHITE)
  for x in range(ox, ox + w):
    _set(v, x, oy + 11, oz, DSLAB)
  return v


def _generate_epic_inventions_rainbow_bridge() -> np.ndarray:
  """Rainbow Bridge — book estimate: 20×8×10 arch."""
  WHITE = _b("white_concrete")
  WATER = _b("water")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 6, 11, 3
  length, width = 20, 10

  for x in range(ox, ox + length):
    for z in range(oz, oz + width):
      _set(v, x, oy - 1, z, WATER)

  for x in range(ox, ox + length):
    _rainbow_row(v, x, oz + 4, oy, 1)
    for z in (oz + 2, oz + 7):
      for y in range(oy, oy + 4):
        _set(v, x, y, z, WHITE)
  for arch in range(5):
    y = oy + 4 + arch
    for x in range(ox + arch, ox + length - arch):
      _set(v, x, y, oz + 2, WHITE)
      _set(v, x, y, oz + 7, WHITE)
  return v


def _generate_epic_inventions_rainbow_finish_arch() -> np.ndarray:
  """Rainbow Finish Arch — book estimate: 18 wide ring gate."""
  WHITE = _b("white_concrete")
  PINK = _b("pink_concrete")
  WATER = _b("water")
  colors = (
    _b("red_concrete"),
    _b("orange_concrete"),
    _b("yellow_concrete"),
    _b("lime_concrete"),
    _b("light_blue_concrete"),
    _b("blue_concrete"),
    _b("purple_concrete"),
  )
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1

  for ring, mat in enumerate(colors):
    r = 8 - ring
    for y in range(oy + ring, oy + 18 - ring):
      for x in range(cx - r, cx + r + 1):
        for z in (cz - 1, cz, cz + 1):
          if abs(x - cx) == r:
            _set(v, x, y, z, mat)
  for y in range(oy + 4, oy + 10):
    for x in range(cx - 2, cx + 3):
      _set(v, x, y, cz - 2, WHITE if x != cx else PINK)
  for y in range(oy, oy + 4):
    _set(v, cx, y, cz - 2, WATER)
  return v


def _generate_epic_inventions_floating_cloud() -> np.ndarray:
  """Floating Cloud — book estimate: 20×14×12 island."""
  WHITE = _b("white_wool")
  WCONC = _b("white_concrete")
  PINK = _b("pink_wool")
  PCONC = _b("pink_concrete")
  LOG = _b("dark_oak_log")
  WATER = _b("water")
  GLOW = _b("glowstone")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 4
  _cloud_blob(v, cx, cz, oy, 10, 7, WHITE)
  _cloud_blob(v, cx - 4, cz + 2, oy, 6, 5, WCONC)
  _cloud_blob(v, cx + 5, cz - 3, oy, 5, 4, WHITE)

  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      _set(v, x, oy + 1, z, WATER)
  _set(v, cx + 6, oy + 3, cz + 4, GLOW)

  tx, tz = cx - 5, cz + 4
  for y in range(oy + 1, oy + 5):
    _set(v, tx, y, tz, LOG)
  for dx in range(-2, 3):
    for dz in range(-2, 3):
      if abs(dx) + abs(dz) <= 2:
        _set(v, tx + dx, oy + 5, tz + dz, PINK if (dx + dz) % 2 else PCONC)
  return v


def _generate_epic_inventions_reverse_waterfall() -> np.ndarray:
  """Reverse Waterfall — book estimate: 12×12×26 bubble lift."""
  WHITE = _b("white_concrete")
  WOOL = _b("white_wool")
  WATER = _b("water")
  SOUL = _b("soul_sand")
  GLASS = _b("glass")
  LANTERN = _b("sea_lantern")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 10, 1
  s = 12
  cx, cz = ox + 5, oz + 5

  for y in range(oy, oy + 24):
    for x in range(ox, ox + s):
      for z in range(oz, oz + s):
        edge = x in (ox, ox + s - 1) or z in (oz, oz + s - 1)
        if edge:
          _set(v, x, y, z, WHITE if y % 2 else WOOL)
        else:
          _set(v, x, y, z, WATER if y > oy else AIR_B)
    if y % 6 == 0:
      _set(v, ox + 1, y, oz + 1, GLASS)
      _set(v, ox + s - 2, y, oz + s - 2, GLASS)

  for x in range(ox + 1, ox + s - 1):
    for z in range(oz + 1, oz + s - 1):
      _set(v, x, oy, z, SOUL)
  _set(v, cx, oy + 12, cz, LANTERN)
  return v


def _generate_epic_inventions_rainbow_piston_bridge() -> np.ndarray:
  """Rainbow Piston Bridge — book estimate: 24×16×10 channel."""
  WHITE = _b("white_concrete")
  SEA = _b("sea_lantern")
  WATER = _b("water")
  PISTON = _b("piston")
  AIR_B = AIR
  colors = (
    _b("red_concrete"),
    _b("orange_concrete"),
    _b("yellow_concrete"),
    _b("lime_concrete"),
    _b("light_blue_concrete"),
    _b("blue_concrete"),
    _b("purple_concrete"),
  )

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 4, 8, 1
  length, width = 24, 16

  for x in range(ox, ox + length):
    for z in range(oz + 4, oz + width - 4):
      _set(v, x, oy, z, SEA if (x + z) % 2 else WHITE)
      _set(v, x, oy + 1, z, WATER)

  for x in range(ox, ox + length):
    for z in (oz + 3, oz + width - 5):
      for y in range(oy + 1, oy + 7):
        _set(v, x, y, z, colors[(x + y) % len(colors)])
    _set(v, x, oy + 1, oz + 4, PISTON)
    _set(v, x, oy + 1, oz + width - 5, PISTON)
  return v


def _generate_epic_inventions_bridge_island() -> np.ndarray:
  """Bridge Island — book estimate: 20×20×15 cloud checkpoint."""
  WHITE = _b("white_wool")
  WCONC = _b("white_concrete")
  WATER = _b("water")
  YELLOW = _b("yellow_concrete")
  AIR_B = AIR
  colors = (
    _b("red_concrete"),
    _b("orange_concrete"),
    _b("lime_concrete"),
    _b("blue_concrete"),
    _b("purple_concrete"),
  )

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 3
  _cloud_blob(v, cx, cz, oy, 10, 10, WHITE)
  _cloud_blob(v, cx + 6, cz - 4, oy, 4, 4, WCONC)

  for x in range(cx - 8, cx + 9):
    _set(v, x, oy + 1, cz, WATER)
  for i, col in enumerate(colors):
    _set(v, cx - 2 + i, oy + 4, cz - 3, col)
    _set(v, cx - 2 + i, oy + 5, cz - 3, col)

  for x in range(cx + 4, cx + 7):
    for z in range(cz + 3, cz + 6):
      for y in range(oy + 1, oy + 4):
        _set(v, x, y, z, YELLOW)
  return v


def _generate_epic_inventions_jump_island() -> np.ndarray:
  """Jump Island — book estimate: 18×18×14 piston launch."""
  WHITE = _b("white_wool")
  PINK = _b("pink_wool")
  LOG = _b("dark_oak_log")
  PISTON = _b("sticky_piston")
  RED = _b("redstone_block")
  WATER = _b("water")
  SLIME = _b("slime_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 4
  _cloud_blob(v, cx, cz, oy, 9, 9, WHITE)

  for x in range(cx - 3, cx + 4):
    for z in range(cz - 1, cz + 2):
      _set(v, x, oy + 1, z, WATER)
  _set(v, cx, oy, cz, PISTON)
  _set(v, cx, oy - 1, cz, RED)
  _set(v, cx, oy + 1, cz, SLIME)

  tx, tz = cx - 6, cz + 5
  for y in range(oy + 1, oy + 5):
    _set(v, tx, y, tz, LOG)
  for dx in range(-1, 2):
    for dz in range(-1, 2):
      _set(v, tx + dx, oy + 5, tz + dz, PINK)
  return v


def _lab_room(v: np.ndarray, ox: int, oz: int, oy: int, w: int, h: int, d: int, wall: str, trim: str | None = None) -> None:
  for y in range(oy, oy + h):
    for x in range(ox, ox + w):
      for z in range(oz, oz + d):
        edge = x in (ox, ox + w - 1) or z in (oz, oz + d - 1) or y in (oy, oy + h - 1)
        if edge:
          mat = trim if trim and y == oy + h - 1 else wall
          _set(v, x, y, z, mat)
        else:
          _set(v, x, y, z, AIR)


def _generate_epic_inventions_potions_lab() -> np.ndarray:
  WHITE = _b("white_concrete")
  QUARTZ = _b("quartz_bricks")
  STONE = _b("smooth_stone")
  BREW = _b("brewing_stand")
  DISP = _b("dispenser")
  BLACK = _b("black_concrete")
  GLASS = _b("glass_pane")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 10, 1
  w, h, d = 12, 7, 12
  _lab_room(v, ox, oz, oy, w, h, d, WHITE, QUARTZ)
  cx, cz = ox + 6, oz + 6
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      _set(v, x, oy + 1, z, BLACK)
  for px, pz in ((ox + 2, oz + 2), (ox + 9, oz + 2), (ox + 2, oz + 9), (ox + 9, oz + 9)):
    _set(v, px, oy + 2, pz, BREW)
  for x in range(ox + 1, ox + w - 1):
    if x % 2 == 0:
      _set(v, x, oy + 3, oz, DISP)
      _set(v, x, oy + 3, oz + d - 1, DISP)
  _set(v, cx, oy + 2, oz, GLASS)
  return v


def _generate_epic_inventions_briefing_room() -> np.ndarray:
  WHITE = _b("white_concrete")
  YELLOW = _b("yellow_concrete")
  STAIR = _b("smooth_quartz_stairs")
  LECT = _b("lectern")
  BLACK = _b("black_concrete")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 10, 1
  w, h, d = 16, 7, 12
  _lab_room(v, ox, oz, oy, w, h, d, WHITE, YELLOW)
  for tier in range(3):
    for x in range(ox + 2, ox + w - 2):
      _set(v, x, oy + 1 + tier, oz + 2 + tier * 2, STAIR)
  for x in range(ox + 1, ox + 4):
    for y in range(oy + 1, oy + 5):
      _set(v, x, y, oz + d - 1, BLACK)
  _set(v, ox + 7, oy + 1, oz + 2, LECT)
  return v


def _generate_epic_inventions_research_cells() -> np.ndarray:
  WHITE = _b("white_concrete")
  GREEN = _b("green_concrete")
  DOOR = _b("iron_door")
  BARS = _b("iron_bars")
  GLASS = _b("glass_pane")
  QUARTZ = _b("quartz_bricks")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 12, 1
  for i in range(4):
    cx = ox + i * 4
    for y in range(oy, oy + 7):
      for x in range(cx, cx + 4):
        for z in range(oz, oz + 6):
          edge = x in (cx, cx + 3) or z in (oz, oz + 5) or y == oy + 6
          if edge:
            _set(v, x, y, z, GREEN if y == oy + 6 else WHITE if x == cx else QUARTZ)
          else:
            _set(v, x, y, z, AIR_B)
    _set(v, cx + 1, oy + 1, oz, DOOR)
    _set(v, cx + 2, oy + 3, oz + 5, BARS)
    _set(v, cx + 1, oy + 3, oz + 5, GLASS)
  return v


def _generate_epic_inventions_sword_mosaic() -> np.ndarray:
  GOLD = _b("gold_block")
  BLACK = _b("blackstone")
  PB = _b("polished_blackstone")
  QUARTZ = _b("quartz_bricks")
  WHITE = _b("white_concrete")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 10, 1
  blade = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 6), (2, 7), (-1, 6), (-2, 7)]
  for dx, dz in blade:
    _set(v, ox + 5 + dx, oy, oz + 5 + dz, GOLD)
    for nx, nz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
      _set(v, ox + 5 + dx + nx, oy, oz + 5 + dz + nz, BLACK)
  for dx in range(-1, 2):
    for dz in range(-2, 1):
      _set(v, ox + 5 + dx, oy, oz + 2 + dz, GOLD)
  for y in range(oy + 1, oy + 10):
    for x in range(ox + 3, ox + 9):
      _set(v, x, y, oz + 9, QUARTZ if y % 2 else WHITE)
  return v


def _generate_epic_inventions_corrosive_lab() -> np.ndarray:
  WHITE = _b("white_concrete")
  QUARTZ = _b("quartz_bricks")
  BGLASS = _b("light_blue_stained_glass")
  WATER = _b("water")
  CAUL = _b("cauldron")
  BARS = _b("iron_bars")
  LANTERN = _b("lantern")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 9, 1
  w, h, d = 14, 8, 14
  _lab_room(v, ox, oz, oy, w, h, d, WHITE, QUARTZ)
  cx, cz = ox + 7, oz + 7
  for y in range(oy + 1, oy + 5):
    for x in range(cx - 2, cx + 3):
      for z in range(cz - 2, cz + 3):
        edge = x in (cx - 2, cx + 2) or z in (cz - 2, cz + 2)
        _set(v, x, y, z, BGLASS if edge else WATER)
  for px, pz in ((ox + 2, oz + 2), (ox + w - 3, oz + 2), (ox + 2, oz + d - 3)):
    _set(v, px, oy + 1, pz, CAUL)
    _set(v, px, oy + 2, pz, LANTERN)
  for x in range(ox + 1, ox + w - 1):
    _set(v, x, oy + 1, oz + 1, QUARTZ)
  _set(v, cx, oy + 5, cz, BARS)
  return v


def _generate_epic_inventions_battery_power() -> np.ndarray:
  WHITE = _b("white_concrete")
  QUARTZ = _b("quartz_bricks")
  GLASS = _b("glass_pane")
  CRY = _b("crying_obsidian")
  ORANGE = _b("orange_concrete")
  LANTERN = _b("sea_lantern")
  BARS = _b("iron_bars")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 11, 1
  s = 10
  cx, cz = ox + 4, oz + 4
  for y in range(oy, oy + 16):
    for x in range(ox, ox + s):
      for z in range(oz, oz + s):
        edge = x in (ox, ox + s - 1) or z in (oz, oz + s - 1)
        if edge:
          _set(v, x, y, z, GLASS if y > oy + 2 and y < oy + 14 else QUARTZ if (x + z) % 2 else WHITE)
        elif y < oy + 14:
          _set(v, x, y, z, CRY if (x + z) % 2 else LANTERN)
  for dx, dz in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)):
    _set(v, cx + dx, oy + 16, cz + dz, ORANGE)
  for y in range(oy + 1, oy + 15):
    _set(v, ox, y, cz, BARS)
  return v


def _generate_epic_inventions_vine_room() -> np.ndarray:
  RED = _b("red_concrete")
  WHITE = _b("white_concrete")
  VINE = _b("warped_vines")
  WART = _b("warped_wart_block")
  RAIL = _b("rail")
  PRAIL = _b("powered_rail")
  STONE = _b("smooth_stone")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 4, 8, 1
  w, d = 24, 16
  for y in range(oy, oy + 7):
    for x in range(ox, ox + w):
      for z in range(oz, oz + d):
        edge = x in (ox, ox + w - 1) or z in (oz, oz + d - 1) or y == oy + 6
        if edge:
          _set(v, x, y, z, RED if x in (ox, ox + w - 1) else WHITE)
        else:
          _set(v, x, y, z, AIR_B)
  for x in range(ox + 2, ox + w - 2, 3):
    for z in range(oz + 2, oz + d - 2, 3):
      _set(v, x, oy, z, STONE)
      _set(v, x, oy, z + 1, PRAIL if (x + z) % 2 else RAIL)
      for y in range(oy + 1, oy + 6):
        _set(v, x, y, z, VINE)
      _set(v, x, oy + 5, z, WART)
  return v


def _generate_epic_inventions_piston_extender() -> np.ndarray:
  STONE = _b("smooth_stone")
  SSTICK = _b("sticky_piston")
  PISTON = _b("piston")
  OBS = _b("observer")
  REPEAT = _b("redstone_repeater")
  DUST = _b("redstone_dust")
  WHITE = _b("white_concrete")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 13, 1
  for x in range(ox, ox + 7):
    for z in range(oz, oz + 5):
      _set(v, x, oy, z, STONE)
  _set(v, ox + 1, oy + 1, oz + 2, SSTICK)
  _set(v, ox + 2, oy + 1, oz + 2, PISTON)
  _set(v, ox + 4, oy + 1, oz + 2, OBS)
  _set(v, ox + 5, oy + 1, oz + 2, REPEAT)
  for i in range(3):
    _set(v, ox + 1 + i, oy, oz + 1, DUST)
  _set(v, ox + 3, oy + 2, oz + 2, WHITE)
  return v


def _generate_epic_inventions_nether_transport_hub() -> np.ndarray:
  OBS = _b("obsidian")
  PORTAL = _b("nether_portal")
  WHITE = _b("white_concrete")
  BLACK = _b("black_concrete")
  GOLD = _b("gold_block")
  QUARTZ = _b("quartz_bricks")
  RAIL = _b("rail")
  PB = _b("polished_blackstone")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 5, 8, 1
  px, pz = ox + 8, oz + 5
  for y in range(oy, oy + 5):
    for x in range(px - 2, px + 3):
      for z in range(pz - 1, pz + 2):
        _set(v, x, y, z, OBS)
  for y in range(oy + 1, oy + 4):
    for x in range(px - 1, px + 2):
      for z in range(pz, pz + 1):
        _set(v, x, y, z, PORTAL)
  for y in range(oy, oy + 8):
    for x in range(px - 4, px + 5):
      _set(v, x, y, pz - 3, WHITE if x % 2 == 0 else QUARTZ)
      _set(v, x, y, pz + 3, BLACK if x % 2 else GOLD)
  for x in range(ox, ox + 22):
    _set(v, x, oy + 1, oz + 2, RAIL)
    _set(v, x, oy, oz + 2, PB)
  for y in range(oy + 5, oy + 12):
    _set(v, px, y, pz, GOLD)
  return v


def _generate_epic_inventions_defense_barrier() -> np.ndarray:
  BLACK = _b("blackstone")
  PB = _b("polished_blackstone")
  BANNER = _b("white_banner")
  BARS = _b("iron_bars")
  WALL = _b("stone_brick_wall")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 13, 1
  for y in range(oy, oy + 4):
    for x in range(ox, ox + 7):
      _set(v, x, y, oz, PB if y == oy else BLACK)
  for i in range(3):
    _set(v, ox + 1 + i * 2, oy + 3, oz, BANNER)
  for y in range(oy + 1, oy + 3):
    _set(v, ox + 6, y, oz + 1, BARS)
  _set(v, ox + 3, oy + 4, oz + 2, WALL)
  return v


def _generate_epic_inventions_disposal_unit() -> np.ndarray:
  WHITE = _b("white_concrete")
  GREEN = _b("green_concrete")
  BGLASS = _b("light_blue_stained_glass")
  WATER = _b("water")
  BARS = _b("iron_bars")
  STONE = _b("smooth_stone")
  LANTERN = _b("lantern")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 0, 13, 1
  length, width = 32, 6
  for x in range(ox, ox + length):
    for z in range(oz, oz + width):
      _set(v, x, oy, z, STONE)
      _set(v, x, oy + 1, z, WATER)
      _set(v, x, oy + 2, z, BGLASS)
  for y in range(oy + 3, oy + 6):
    for x in range(ox, ox + length):
      for z in (oz, oz + width - 1):
        _set(v, x, y, z, GREEN if x % 4 < 2 else WHITE)
      if x % 8 == 0:
        _set(v, x, y, oz + 2, BARS)
  _set(v, ox + 4, oy + 4, oz + 3, LANTERN)
  return v


def _generate_epic_inventions_backup_generator() -> np.ndarray:
  WHITE = _b("white_concrete")
  STONE = _b("stone_bricks")
  GREEN = _b("green_concrete")
  COPPER = _b("copper_block")
  ROD = _b("lightning_rod")
  FURNACE = _b("furnace")
  WATER = _b("water")
  SMOOTH = _b("smooth_stone")
  LANTERN = _b("lantern")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 3, 3, 1
  s = 26
  for y in range(oy, oy + 10):
    for x in range(ox, ox + s):
      for z in range(oz, oz + s):
        edge = x in (ox, ox + s - 1) or z in (oz, oz + s - 1)
        if y == oy:
          _set(v, x, oy, z, SMOOTH if (x + z) % 3 else WATER if (x + z) % 5 == 0 else STONE)
        elif edge and y < oy + 8:
          _set(v, x, y, z, GREEN if y == oy + 7 else WHITE if x % 2 == 0 else STONE)
        elif not edge and y < oy + 8:
          _set(v, x, y, z, AIR_B)
  for px, pz in ((ox + 6, oz + 6), (ox + 18, oz + 6), (ox + 6, oz + 18), (ox + 18, oz + 18)):
    for y in range(oy + 1, oy + 5):
      _set(v, px, y, pz, COPPER if y < oy + 4 else ROD)
    _set(v, px, oy + 1, pz + 1, FURNACE)
    _set(v, px + 1, oy + 6, pz, LANTERN)
  return v


def _generate_epic_inventions_mechanical_leg() -> np.ndarray:
  WHITE = _b("white_concrete")
  IRON = _b("iron_block")
  LIME = _b("lime_concrete")
  BARS = _b("iron_bars")
  COPPER = _b("oxidized_cut_copper")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 13, 1
  for seg in range(7):
    y = oy + seg * 4
    inset = seg // 2
    for x in range(ox + inset, ox + 6 - inset):
      for z in range(oz + inset, oz + 6 - inset):
        edge = x in (ox + inset, ox + 5 - inset) or z in (oz + inset, oz + 5 - inset)
        if edge:
          _set(v, x, y, z, LIME if seg % 2 else COPPER if x == ox + inset else IRON if z == oz + inset else WHITE)
        _set(v, ox + 2, y + 1, oz + 2, BARS)
  return v


def _generate_epic_inventions_bunkhouse() -> np.ndarray:
  OAK = _b("oak_planks")
  YELLOW = _b("yellow_terracotta")
  BED = _b("red_bed")
  CHEST = _b("chest")
  STAIR = _b("oak_stairs")
  FENCE = _b("oak_fence")
  LANTERN = _b("lantern")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 12, 1
  s = 8
  for floor in range(4):
    fy = oy + floor * 4
    for y in range(fy, fy + 4):
      for x in range(ox, ox + s):
        for z in range(oz, oz + s):
          edge = x in (ox, ox + s - 1) or z in (oz, oz + s - 1) or y == fy + 3
          if edge:
            _set(v, x, y, z, YELLOW if y == fy + 3 else OAK)
          else:
            _set(v, x, y, z, AIR_B)
    for bx, bz in ((ox + 1, oz + 1), (ox + 5, oz + 1), (ox + 1, oz + 5), (ox + 5, oz + 5)):
      _set(v, bx, fy + 1, bz, BED)
      _set(v, bx + 1, fy + 1, bz, CHEST)
    for x in range(ox + 2, ox + s - 2):
      _set(v, x, fy + 1, oz + 3, STAIR)
    _set(v, ox + 3, fy + 3, oz, LANTERN)
  return v


def _generate_epic_inventions_band_pavilion() -> np.ndarray:
  OAK = _b("oak_planks")
  YELLOW = _b("yellow_terracotta")
  FENCE = _b("oak_fence")
  LOG = _b("oak_log")
  BARREL = _b("barrel")
  NOTE = _b("note_block")
  LANTERN = _b("lantern")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 11, 4
  s = 10
  for x in range(ox, ox + s):
    for z in range(oz, oz + s):
      _set(v, x, oy, z, OAK)
  for y in range(oy + 1, oy + 4):
    for x in range(ox, ox + s):
      for z in range(oz, oz + s):
        if x in (ox, ox + s - 1) or z in (oz, oz + s - 1):
          _set(v, x, y, z, FENCE if y < oy + 3 else YELLOW)
  for px, pz in ((ox, oz), (ox + s - 1, oz), (ox, oz + s - 1), (ox + s - 1, oz + s - 1)):
    for y in range(oy, oy + 4):
      _set(v, px, y, pz, LOG)
  for bx, bz in ((ox + 3, oz + 3), (ox + 5, oz + 4), (ox + 4, oz + 5)):
    _set(v, bx, oy + 1, bz, BARREL if (bx + bz) % 2 else NOTE)
  _set(v, ox + 4, oy + 4, oz + 4, LANTERN)
  return v


def _generate_epic_inventions_control_sphere() -> np.ndarray:
  LIME = _b("lime_concrete")
  GREEN = _b("green_concrete")
  GLASS = _b("glass_pane")
  OAK = _b("oak_planks")
  LADDER = _b("ladder")
  LEVER = _b("lever")
  LAMP = _b("redstone_lamp")
  BARS = _b("iron_bars")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cy, cz = 16, 10, 16
  r = 6
  for x in range(cx - r, cx + r + 1):
    for y in range(cy - r, cy + r + 1):
      for z in range(cz - r, cz + r + 1):
        d = (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2
        if (r - 1) ** 2 <= d <= r ** 2 + r:
          _set(v, x, y, z, GLASS if (x + y + z) % 3 == 0 else LIME if (x + z) % 2 else GREEN)
        elif d < (r - 1) ** 2 and y == cy:
          _set(v, x, y, z, OAK)
  for y in range(cy - 2, cy + 3):
    _set(v, cx, y, cz, LADDER)
  for lx, lz in ((cx - 2, cz), (cx + 2, cz)):
    _set(v, lx, cy + 1, lz, LEVER)
    _set(v, lx, cy + 2, lz, LAMP)
  _set(v, cx, cy + 3, cz + r, BARS)
  return v


def _generate_epic_inventions_saloon_stables() -> np.ndarray:
  OAK = _b("oak_planks")
  YELLOW = _b("yellow_terracotta")
  FENCE = _b("oak_fence")
  HAY = _b("hay_block")
  SLAB = _b("oak_slab")
  LANTERN = _b("lantern")
  WATER = _b("water")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 6, 12, 1
  length, depth = 20, 8
  for x in range(ox, ox + length):
    for z in range(oz, oz + depth):
      _set(v, x, oy, z, OAK)
  for y in range(oy + 1, oy + 6):
    for x in range(ox, ox + length):
      for z in range(oz, oz + depth):
        edge = x in (ox, ox + length - 1) or z in (oz, oz + depth - 1)
        if edge:
          _set(v, x, y, z, YELLOW if y == oy + 5 else OAK)
        else:
          _set(v, x, y, z, AIR_B)
  for i in range(4):
    sx = ox + 2 + i * 4
    for z in range(oz + 1, oz + depth - 1):
      _set(v, sx, oy + 1, z, FENCE)
      _set(v, sx, oy + 1, z, HAY if z < oz + 4 else WATER)
  for x in range(ox, ox + length):
    _set(v, x, oy + 6, oz, SLAB)
    _set(v, x, oy + 6, oz + depth - 1, SLAB)
  _set(v, ox + 2, oy + 4, oz + 3, LANTERN)
  return v


def _generate_epic_inventions_ornithopter() -> np.ndarray:
  WHITE = _b("white_concrete")
  IRON = _b("iron_block")
  YELLOW = _b("yellow_concrete")
  BARS = _b("iron_bars")
  OAK = _b("oak_planks")
  ROD = _b("lightning_rod")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 4, 10, 14
  cx, cz = ox + 12, oz + 8
  for dx in range(-11, 12):
    for dz in range(-7, 8):
      if abs(dx) + abs(dz) // 2 <= 11:
        mat = YELLOW if (dx + dz) % 3 == 0 else WHITE if abs(dx) > 4 else IRON
        _set(v, cx + dx, oy, cz + dz, mat)
        if abs(dx) % 4 == 0 and abs(dz) < 3:
          _set(v, cx + dx, oy + 1, cz + dz, BARS)
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      _set(v, x, oy + 1, z, OAK)
  _set(v, cx, oy + 2, cz, ROD)
  return v


def _generate_epic_inventions_piston_bar() -> np.ndarray:
  SAND = _b("sandstone")
  SSAND = _b("smooth_sandstone")
  PISTON = _b("piston")
  RTORCH = _b("redstone_torch")
  CARPET = _b("orange_carpet")
  BARREL = _b("barrel")
  OAK = _b("oak_planks")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 13, 1
  for x in range(ox, ox + 12):
    for z in range(oz, oz + 6):
      _set(v, x, oy, z, SAND if z in (oz, oz + 5) else SSAND)
  for x in range(ox + 1, ox + 11):
    _set(v, x, oy + 1, oz + 2, PISTON)
    _set(v, x, oy, oz + 2, RTORCH)
    _set(v, x, oy + 2, oz + 2, CARPET)
  for bx, bz in ((ox + 2, oz + 1), (ox + 8, oz + 4)):
    _set(v, bx, oy + 1, bz, BARREL)
  _set(v, ox + 5, oy + 3, oz + 3, OAK)
  return v


def _generate_epic_inventions_dunking_stool() -> np.ndarray:
  WATER = _b("water")
  QUARTZ = _b("smooth_quartz")
  QBLOCK = _b("quartz_block")
  OAK = _b("oak_planks")
  TRAP = _b("oak_trapdoor")
  TARGET = _b("target")
  FENCE = _b("oak_fence")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 12, 1
  s = 8
  for x in range(ox, ox + s):
    for z in range(oz, oz + s):
      _set(v, x, oy, z, QUARTZ)
      _set(v, x, oy + 1, z, WATER)
  for x in range(ox, ox + s):
    for z in (oz, oz + s - 1):
      _set(v, x, oy + 2, z, QBLOCK)
  for z in range(oz, oz + s):
    for x in (ox, ox + s - 1):
      _set(v, x, oy + 2, z, QBLOCK)
  _set(v, ox + 3, oy + 3, oz + 3, TRAP)
  for i in range(3):
    _set(v, ox + s, oy + 2 + i, oz + 3, OAK)
  _set(v, ox + s + 1, oy + 3, oz + 3, TARGET)
  _set(v, ox + 4, oy + 4, oz + 3, FENCE)
  return v


def _generate_epic_inventions_smoke_stack() -> np.ndarray:
  COPPER = _b("oxidized_cut_copper")
  CAMP = _b("campfire")
  TRAP = _b("oak_trapdoor")
  IRON = _b("iron_block")
  QUARTZ = _b("quartz_block")
  BARS = _b("iron_bars")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  stacks = ((10, 14, 1, 10), (14, 14, 1, 12), (18, 14, 1, 8))
  for sx, sz, oy, h in stacks:
    for y in range(oy, oy + h):
      _set(v, sx, y, sz, COPPER if y < h - 2 else IRON if sx == 18 else QUARTZ)
      if sx != 18:
        _set(v, sx + 1, y, sz, BARS if y % 3 == 0 else COPPER)
    _set(v, sx, oy + h, sz, CAMP)
    _set(v, sx, oy + h + 1, sz, TRAP)
  return v


def _generate_epic_inventions_waterfall_elevator() -> np.ndarray:
  OAK = _b("oak_planks")
  LOG = _b("oak_log")
  WATER = _b("water")
  TARGET = _b("target")
  DISP = _b("dispenser")
  LADDER = _b("ladder")
  DUST = _b("redstone_dust")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 13, 1
  s = 5
  cx, cz = ox + 2, oz + 2
  for y in range(oy, oy + 22):
    for x in range(ox, ox + s):
      for z in range(oz, oz + s):
        edge = x in (ox, ox + s - 1) or z in (oz, oz + s - 1)
        if edge:
          _set(v, x, y, z, LOG if (x + z) % 2 == 0 else OAK)
        else:
          _set(v, x, y, z, WATER if y > oy else AIR_B)
  _set(v, cx, oy, cz, TARGET)
  _set(v, cx, oy + 21, cz, DISP)
  for y in range(oy + 1, oy + 20):
    _set(v, ox + s - 1, y, cz, LADDER)
  _set(v, cx, oy, cz + 1, DUST)
  return v


def _generate_epic_inventions_signal_ladder() -> np.ndarray:
  OAK = _b("oak_planks")
  RTORCH = _b("redstone_torch")
  DUST = _b("redstone_dust")
  TARGET = _b("target")
  DISP = _b("dispenser")
  STONE = _b("stone")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 15, 15, 1
  for y in range(oy, oy + 22):
    _set(v, ox, y, oz, OAK)
    if y % 2 == 0:
      _set(v, ox + 1, y, oz, RTORCH)
    else:
      _set(v, ox - 1, y, oz, STONE)
    if y > oy:
      _set(v, ox, y, oz + 1, DUST)
  _set(v, ox, oy, oz + 1, TARGET)
  _set(v, ox, oy + 21, oz + 1, DISP)
  return v


def _generate_epic_inventions_aqueduct() -> np.ndarray:
  STONE = _b("stone_bricks")
  MOSSY = _b("mossy_stone_bricks")
  DEEP = _b("deepslate")
  WATER = _b("water")
  VINE = _b("vine")
  COBBLE = _b("cobblestone")
  BSLAB = _b("birch_slab")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 12, 6
  for tier in range(3):
    ty = oy - tier * 3
    for x in range(ox + tier, ox + 16 - tier):
      for z in (oz, oz + 7):
        _set(v, x, ty, z, STONE if tier == 0 else MOSSY if tier == 1 else DEEP)
        _set(v, x, ty - 1, z, COBBLE)
        if x % 3 == 0:
          _set(v, x, ty - 2, z, VINE)
  for x in range(ox, ox + 16):
    for z in range(oz + 1, oz + 7):
      _set(v, x, oy + 1, z, WATER)
      _set(v, x, oy, z, BSLAB if (x + z) % 2 else STONE)
  return v


def _generate_epic_inventions_cave_network() -> np.ndarray:
  STONE = _b("stone")
  DIRT = _b("dirt")
  OAK = _b("oak_planks")
  FENCE = _b("oak_fence")
  TORCH = _b("torch")
  COBBLE = _b("cobblestone")
  GRAVEL = _b("gravel")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 11, 2
  for x in range(ox, ox + 14):
    for z in range(oz, oz + 8):
      for y in range(oy, oy + 6):
        edge = x in (ox, ox + 13) or z in (oz, oz + 7) or y == oy + 5
        if edge:
          _set(v, x, y, z, STONE if y > oy + 2 else DIRT if (x + z) % 2 else COBBLE)
        else:
          _set(v, x, y, z, AIR_B)
  for x in range(ox + 2, ox + 12, 4):
    for z in range(oz + 2, oz + 6):
      for y in range(oy + 1, oy + 5):
        _set(v, x, y, z, FENCE if y < oy + 4 else OAK)
      _set(v, x, oy + 3, z, TORCH)
  _set(v, ox + 6, oy, oz + 3, GRAVEL)
  return v


def _generate_epic_inventions_treasure_room() -> np.ndarray:
  DEEP = _b("deepslate")
  GOLD_ORE = _b("deepslate_gold_ore")
  GOLD = _b("gold_block")
  CHEST = _b("chest")
  LANTERN = _b("lantern")
  POLISHED = _b("polished_deepslate")
  CHISEL = _b("chiseled_deepslate")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 3
  r = 5
  for y in range(oy, oy + 7):
    for x in range(cx - r, cx + r + 1):
      for z in range(cz - r, cz + r + 1):
        if (x - cx) ** 2 + (z - cz) ** 2 <= r ** 2:
          edge = (x - cx) ** 2 + (z - cz) ** 2 >= (r - 1) ** 2 or y == oy
          if y == oy + 6:
            _set(v, x, y, z, POLISHED)
            if (x + z) % 3 == 0:
              _set(v, x, y + 1, z, LANTERN)
          elif edge:
            _set(v, x, y, z, GOLD_ORE if y < oy + 5 else CHISEL)
          else:
            _set(v, x, y, z, AIR_B)
  for x in range(cx - 1, cx + 2):
    for z in range(cz - 1, cz + 2):
      _set(v, x, oy + 1, z, GOLD if x == cx and z == cz else POLISHED)
  _set(v, cx, oy + 2, cz, CHEST)
  return v


def _generate_epic_inventions_temple_tower() -> np.ndarray:
  QUARTZ = _b("quartz_block")
  SQUARTZ = _b("smooth_quartz")
  ORANGE = _b("orange_terracotta")
  BLACK = _b("black_concrete")
  QSTAIR = _b("quartz_stairs")
  QSLAB = _b("quartz_slab")
  FENCE = _b("oak_fence")
  LANTERN = _b("lantern")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 12, 1
  tiers = ((0, 8), (1, 6), (2, 4), (3, 3))
  for inset, h in tiers:
    wx, wz = ox + inset, oz + inset
    s = 8 - inset * 2
    for y in range(oy + sum(t[1] for t in tiers[:tiers.index((inset, h))]), oy + sum(t[1] for t in tiers[:tiers.index((inset, h)) + 1])):
      for x in range(wx, wx + s):
        for z in range(wz, wz + s):
          edge = x in (wx, wx + s - 1) or z in (wz, wz + s - 1)
          if edge:
            _set(v, x, y, z, ORANGE if y % 4 == 0 else BLACK if (x + z) % 3 == 0 else QUARTZ if y % 2 else SQUARTZ)
          elif y == oy:
            _set(v, x, y, z, QSLAB)
    for x in range(wx, wx + s):
      _set(v, x, oy + h, wz, FENCE)
      _set(v, x, oy + h, wz + s - 1, FENCE)
  _set(v, ox + 3, oy + 20, oz + 3, LANTERN)
  return v


def _generate_epic_inventions_gravel_trap() -> np.ndarray:
  STONE = _b("stone_bricks")
  GRAVEL = _b("gravel")
  LAVA = _b("lava")
  SPISTON = _b("sticky_piston")
  DUST = _b("redstone_dust")
  PLATE = _b("stone_pressure_plate")
  BARS = _b("iron_bars")
  CHAIN = _b("chain")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 11, 1
  for x in range(ox, ox + 14):
    for z in (oz, oz + 9):
      for y in range(oy, oy + 8):
        _set(v, x, y, z, STONE)
  for x in range(ox + 1, ox + 13):
    _set(v, x, oy, oz + 4, LAVA)
    _set(v, x, oy + 1, oz + 4, PLATE)
  for x in range(ox + 2, ox + 12):
    for z in range(oz + 3, oz + 6):
      for y in range(oy + 6, oy + 10):
        _set(v, x, y, z, GRAVEL)
      _set(v, x, oy + 5, z, SPISTON)
  for x in range(ox, ox + 14, 3):
    _set(v, x, oy + 3, oz + 2, BARS)
    _set(v, x, oy + 8, oz + 2, CHAIN)
  _set(v, ox + 6, oy + 4, oz + 1, DUST)
  return v


def _generate_epic_inventions_banyan_altar() -> np.ndarray:
  SSAND = _b("smooth_sandstone")
  SAND = _b("sandstone")
  SSTAIR = _b("sandstone_stairs")
  WALL = _b("stone_brick_wall")
  TORCH = _b("torch")
  LAMP = _b("redstone_lamp")
  LEVER = _b("lever")
  COAL = _b("coal_block")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 10, 1
  cx, cz = ox + 8, oz + 6
  for layer in range(5):
    inset = layer
    y = oy + layer
    for x in range(ox + inset, ox + 16 - inset):
      for z in range(oz + inset, oz + 12 - inset):
        _set(v, x, y, z, SSTAIR if layer < 4 else SSAND)
  for px, pz in ((ox + 2, oz + 2), (ox + 13, oz + 2), (ox + 2, oz + 9), (ox + 13, oz + 9)):
    for y in range(oy + 1, oy + 6):
      _set(v, px, y, pz, WALL)
    _set(v, px, oy + 4, pz, TORCH)
  for y in range(oy + 1, oy + 5):
    for x in range(cx - 2, cx + 3):
      for z in range(cz - 1, cz + 2):
        _set(v, x, y, z, COAL)
  _set(v, cx - 3, oy + 3, cz, LAMP)
  _set(v, cx + 3, oy + 3, cz, LEVER)
  return v


def _generate_epic_inventions_combination_door() -> np.ndarray:
  LIME = _b("lime_terracotta")
  DBRICK = _b("deepslate_bricks")
  PBLACK = _b("polished_blackstone")
  CDEEP = _b("chiseled_deepslate")
  CPBLACK = _b("chiseled_polished_blackstone")
  GOLD_ORE = _b("deepslate_gold_ore")
  SPISTON = _b("sticky_piston")
  LEVER = _b("lever")
  CANDLE = _b("candle")
  GOLD = _b("gold_block")
  DUST = _b("redstone_dust")
  RTORCH = _b("redstone_torch")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 14, 1
  for y in range(oy, oy + 12):
    _set(v, ox, y, oz, LIME)
    _set(v, ox + 9, y, oz, LIME)
    if y % 2 == 0:
      _set(v, ox + 1, y, oz, RTORCH)
  for y in range(oy + 2, oy + 6):
    _set(v, ox + 4, y, oz, DBRICK)
    _set(v, ox + 5, y, oz, SPISTON)
    _set(v, ox + 6, y, oz, PBLACK)
  for y in range(oy, oy + 8):
    for x in range(ox + 2, ox + 8):
      _set(v, x, y, oz + 1, CPBLACK if y > oy + 2 else CDEEP if x == ox + 4 else GOLD_ORE if (x + y) % 2 else DBRICK)
  for lx, lz in ((ox + 2, oz + 1), (ox + 3, oz + 1), (ox + 6, oz + 1)):
    _set(v, lx, oy + 4, lz, LEVER)
  _set(v, ox + 4, oy + 7, oz + 1, GOLD)
  _set(v, ox + 5, oy + 8, oz + 1, CANDLE)
  _set(v, ox + 3, oy + 5, oz + 2, DUST)
  return v


def _generate_epic_inventions_control_bridge() -> np.ndarray:
  WHITE = _b("white_concrete")
  GRAY = _b("gray_concrete")
  ORANGE = _b("orange_concrete")
  BARS = _b("iron_bars")
  LANTERN = _b("sea_lantern")
  GLASS = _b("glass_pane")
  BLUE = _b("light_blue_concrete")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 2
  r = 5
  for y in range(oy, oy + 12):
    for x in range(cx - r, cx + r + 1):
      for z in range(cz - r, cz + r + 1):
        if (x - cx) ** 2 + (z - cz) ** 2 <= r ** 2:
          edge = (x - cx) ** 2 + (z - cz) ** 2 >= (r - 1) ** 2 or y in (oy, oy + 11)
          if edge:
            _set(v, x, y, z, WHITE if y % 3 else GRAY)
          elif y in (oy + 3, oy + 7, oy + 10):
            _set(v, x, y, z, ORANGE if (x + z) % 2 else BLUE)
          else:
            _set(v, x, y, z, AIR_B)
  for angle in range(0, 360, 90):
    px = cx + int(r * 0.7 * (1 if angle == 0 else -1 if angle == 180 else 0))
    pz = cz + int(r * 0.7 * (1 if angle == 90 else -1 if angle == 270 else 0))
    _set(v, px, oy + 6, pz, LANTERN)
    _set(v, px, oy + 5, pz, BARS)
  _set(v, cx, oy + 8, cz, GLASS)
  return v


def _generate_epic_inventions_space_engine() -> np.ndarray:
  GRAY = _b("gray_concrete")
  WHITE = _b("white_concrete")
  WATER = _b("water")
  LANTERN = _b("sea_lantern")
  BARS = _b("iron_bars")
  IRON = _b("iron_block")
  ORANGE = _b("orange_concrete")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 14):
    rad = 6 - abs(y - oy - 6) // 2
    for x in range(cx - rad, cx + rad + 1):
      for z in range(cz - rad, cz + rad + 1):
        if (x - cx) ** 2 + (z - cz) ** 2 <= rad ** 2:
          edge = (x - cx) ** 2 + (z - cz) ** 2 >= (rad - 1) ** 2
          if edge:
            _set(v, x, y, z, GRAY if y < oy + 4 else WHITE)
          elif y < oy + 5:
            _set(v, x, y, z, WATER if (x - cx) ** 2 + (z - cz) ** 2 <= 4 else LANTERN if y == oy + 2 else AIR_B)
          elif (x + z + y) % 3 == 0:
            _set(v, x, y, z, BARS if y % 2 else IRON)
          else:
            _set(v, x, y, z, AIR_B)
  _set(v, cx, oy + 12, cz, ORANGE)
  return v


def _generate_epic_inventions_crew_lounge() -> np.ndarray:
  GRAY = _b("gray_concrete")
  WHITE = _b("white_concrete")
  BLUE = _b("light_blue_concrete")
  OAK = _b("oak_planks")
  LANTERN = _b("sea_lantern")
  GLASS = _b("glass_pane")
  BARS = _b("iron_bars")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 2
  r = 5
  for y in range(oy, oy + 6):
    for x in range(cx - r, cx + r + 1):
      for z in range(cz - r, cz + r + 1):
        if (x - cx) ** 2 + (z - cz) ** 2 <= r ** 2:
          if y == oy:
            _set(v, x, y, z, WHITE if (x + z) % 2 else BLUE)
          elif y == oy + 5:
            _set(v, x, y, z, GRAY)
          elif (x - cx) ** 2 + (z - cz) ** 2 >= (r - 1) ** 2:
            _set(v, x, y, z, GRAY)
          elif (x + z) % 4 == 0 and y == oy + 1:
            _set(v, x, y, z, OAK)
          else:
            _set(v, x, y, z, AIR_B)
  _set(v, cx, oy + 5, cz, LANTERN)
  _set(v, cx + r - 1, oy + 3, cz, GLASS)
  _set(v, cx - r + 1, oy + 3, cz, BARS)
  return v


def _generate_epic_inventions_ring_section() -> np.ndarray:
  WHITE = _b("white_concrete")
  GRAY = _b("gray_concrete")
  WATER = _b("water")
  OAK = _b("oak_planks")
  GREEN = _b("green_concrete")
  LANTERN = _b("sea_lantern")
  BARS = _b("iron_bars")
  BED = _b("red_bed")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 10, 2
  for y in range(oy, oy + 12):
    for x in range(ox, ox + 16):
      outer = x in (ox, ox + 15) or y in (oy, oy + 11)
      inner = x in (ox + 6, ox + 9) and y > oy + 2
      if outer:
        _set(v, x, y, oz, GRAY if y % 3 else WHITE)
        _set(v, x, y, oz + 11, GRAY if y % 3 else WHITE)
      elif inner and y < oy + 10:
        _set(v, x, y, oz + 5, BARS)
        _set(v, x, y, oz + 6, BARS)
      elif y < oy + 10 and x % 3 == 0:
        _set(v, x, y, oz + 2, OAK if y % 4 else GREEN if y % 2 else AIR_B)
        _set(v, x, y, oz + 9, OAK if y % 4 else GREEN if y % 2 else AIR_B)
  for x in range(ox + 2, ox + 14, 4):
    _set(v, x, oy + 5, oz + 5, BED)
    _set(v, x, oy + 8, oz + 6, LANTERN)
  for x in range(ox, ox + 16):
    for z in range(oz, oz + 12):
      _set(v, x, oy, z, WATER)
  return v


def _generate_epic_inventions_hydroponics() -> np.ndarray:
  WHITE = _b("white_concrete")
  ORANGE = _b("orange_concrete")
  GRAY = _b("gray_concrete")
  WATER = _b("water")
  KELP = _b("kelp")
  BERRY = _b("sweet_berry_bush")
  MELON = _b("melon")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 11, 1
  _fill_box(v, ox, oy, oz, 14, 8, 10, WHITE, hollow=True)
  for x in range(ox + 2, ox + 12, 3):
    for z in range(oz + 2, oz + 8):
      _set(v, x, oy + 1, z, WATER)
      _set(v, x, oy + 2, z, KELP if z % 2 else BERRY if x % 2 else MELON)
  for x in range(ox, ox + 14):
    _set(v, x, oy + 7, oz, ORANGE)
    _set(v, x, oy + 7, oz + 9, ORANGE)
  _set(v, ox + 6, oy + 4, oz + 4, GRAY)
  return v


def _generate_epic_inventions_berry_farm() -> np.ndarray:
  WHITE = _b("white_concrete")
  GRAY = _b("gray_concrete")
  BERRY = _b("sweet_berry_bush")
  DIRT = _b("dirt")
  FENCE = _b("oak_fence")
  WATER = _b("water")
  LANTERN = _b("sea_lantern")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 13, 1
  _fill_box(v, ox, oy, oz, 8, 6, 6, WHITE, hollow=True)
  for x in range(ox + 1, ox + 7):
    for z in range(oz + 1, oz + 5):
      _set(v, x, oy + 1, z, DIRT)
      _set(v, x, oy + 2, z, BERRY)
  for x in range(ox, ox + 8):
    _set(v, x, oy + 5, oz, GRAY)
    _set(v, x, oy + 5, oz + 5, GRAY)
  _set(v, ox + 3, oy + 1, oz, WATER)
  _set(v, ox + 4, oy + 5, oz + 2, LANTERN)
  _set(v, ox + 1, oy + 2, oz + 1, FENCE)
  return v


def _generate_epic_inventions_kelp_farm() -> np.ndarray:
  WHITE = _b("white_concrete")
  GLASS = _b("glass")
  WATER = _b("water")
  KELP = _b("kelp")
  OBS = _b("observer")
  PISTON = _b("piston")
  HOPPER = _b("hopper")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 13, 1
  for y in range(oy, oy + 14):
    for x in range(ox, ox + 6):
      for z in range(oz, oz + 6):
        edge = x in (ox, ox + 5) or z in (oz, oz + 5)
        if edge:
          _set(v, x, y, z, WHITE if y < oy + 12 else GLASS)
        elif x in (ox + 2, ox + 3) and z in (oz + 2, oz + 3):
          _set(v, x, y, z, WATER if y < oy + 10 else AIR_B)
          if y == oy + 5:
            _set(v, x, y, z, KELP)
  _set(v, ox + 2, oy + 8, oz + 2, OBS)
  _set(v, ox + 3, oy + 9, oz + 2, PISTON)
  _set(v, ox + 4, oy + 12, oz + 3, HOPPER)
  return v


def _generate_epic_inventions_airlock() -> np.ndarray:
  WHITE = _b("white_concrete")
  ORANGE = _b("orange_concrete")
  DOOR = _b("iron_door")
  BARS = _b("iron_bars")
  GRAY = _b("gray_concrete")
  LANTERN = _b("sea_lantern")
  BUTTON = _b("stone_button")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 12, 1
  _fill_box(v, ox, oy, oz, 6, 8, 8, WHITE, hollow=True)
  _set(v, ox + 2, oy + 1, oz, ORANGE)
  _set(v, ox + 2, oy + 2, oz, DOOR)
  _set(v, ox + 3, oy + 1, oz, ORANGE)
  _set(v, ox + 3, oy + 2, oz, DOOR)
  _set(v, ox + 2, oy + 1, oz + 7, ORANGE)
  _set(v, ox + 2, oy + 2, oz + 7, DOOR)
  _set(v, ox + 3, oy + 1, oz + 7, ORANGE)
  _set(v, ox + 3, oy + 2, oz + 7, DOOR)
  for y in range(oy + 3, oy + 7):
    _set(v, ox, y, oz + 3, BARS)
    _set(v, ox + 5, y, oz + 3, BARS)
  _set(v, ox + 2, oy + 6, oz + 4, LANTERN)
  _set(v, ox + 1, oy + 2, oz, BUTTON)
  _set(v, ox + 4, oy + 4, oz + 4, GRAY)
  return v


def _generate_epic_inventions_melon_farm() -> np.ndarray:
  WHITE = _b("white_concrete")
  GRAY = _b("gray_concrete")
  MELON = _b("melon")
  STEM = _b("melon_stem")
  OBS = _b("observer")
  PISTON = _b("piston")
  RAIL = _b("rail")
  CART = _b("hopper_minecart")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 12, 1
  _fill_box(v, ox, oy, oz, 12, 6, 8, WHITE, hollow=True)
  for x in range(ox + 2, ox + 10, 2):
    _set(v, x, oy + 1, oz + 2, STEM)
    _set(v, x, oy + 2, oz + 2, MELON)
    _set(v, x, oy + 2, oz + 4, OBS)
    _set(v, x, oy + 2, oz + 5, PISTON)
  for x in range(ox + 1, ox + 11):
    _set(v, x, oy + 1, oz + 6, RAIL)
  _set(v, ox + 5, oy + 1, oz + 6, CART)
  _set(v, ox + 5, oy + 5, oz, GRAY)
  return v


def _generate_epic_inventions_solar_array() -> np.ndarray:
  WHITE = _b("white_concrete")
  GOLD = _b("gold_block")
  GRAY = _b("gray_concrete")
  BARS = _b("iron_bars")
  LANTERN = _b("sea_lantern")
  ORANGE = _b("orange_concrete")
  ROD = _b("lightning_rod")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 6, 12, 8
  for x in range(ox, ox + 20):
    _set(v, x, oy, oz, WHITE)
    _set(v, x, oy, oz + 7, WHITE)
    for z in range(oz + 1, oz + 7):
      _set(v, x, oy, z, GOLD if (x + z) % 2 == 0 else GRAY)
    if x % 4 == 0:
      _set(v, x, oy - 1, oz + 3, BARS)
      _set(v, x, oy - 2, oz + 3, ROD)
  for x in range(ox + 2, ox + 18, 6):
    _set(v, x, oy + 1, oz + 3, LANTERN)
  _set(v, ox + 9, oy - 1, oz, ORANGE)
  return v


def _generate_epic_inventions_aquarium() -> np.ndarray:
  GLASS = _b("glass")
  WATER = _b("water")
  KELP = _b("kelp")
  CORAL1 = _b("brain_coral")
  CORAL2 = _b("tube_coral")
  GRAY = _b("gray_concrete")
  SAND = _b("sand")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 13, 2
  _fill_box(v, ox, oy, oz, 12, 5, 6, GLASS, hollow=True)
  for x in range(ox + 1, ox + 11):
    for z in range(oz + 1, oz + 5):
      _set(v, x, oy + 1, z, WATER)
      _set(v, x, oy, z, SAND)
      if (x + z) % 3 == 0:
        _set(v, x, oy + 2, z, KELP)
      elif (x + z) % 2 == 0:
        _set(v, x, oy + 2, z, CORAL1 if x % 2 else CORAL2)
  for x in range(ox, ox + 12):
    _set(v, x, oy - 1, oz, GRAY)
    _set(v, x, oy - 1, oz + 5, GRAY)
  return v


def _generate_epic_inventions_piggy_banks() -> np.ndarray:
  colors = [_b("pink_wool"), _b("yellow_wool"), _b("white_wool"), _b("black_wool"),
            _b("gray_wool"), _b("orange_wool"), _b("green_wool")]
  TRAP = _b("oak_trapdoor")
  OAK = _b("dark_oak_planks")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 14, 3
  for i, col in enumerate(colors):
    x = ox + i * 2
    _set(v, x, oy, oz, col)
    _set(v, x, oy + 1, oz, col)
    _set(v, x + 1, oy, oz, col)
    _set(v, x + 1, oy + 1, oz, col)
    _set(v, x, oy - 1, oz, TRAP)
    _set(v, x, oy + 2, oz, OAK)
  return v


def _generate_epic_inventions_creeper_toy() -> np.ndarray:
  GREEN = _b("green_wool")
  GRAY = _b("gray_wool")
  LIME = _b("lime_wool")
  PINK = _b("pink_wool")
  BLACK = _b("black_wool")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 14, 1
  for y in range(oy, oy + 6):
    for x in range(ox, ox + 4):
      for z in range(oz, oz + 3):
        _set(v, x, y, z, GREEN if y < oy + 4 else LIME)
  for x, z in ((ox, oz), (ox + 3, oz), (ox, oz + 2), (ox + 3, oz + 2)):
    _set(v, x, oy + 4, z, GRAY)
    _set(v, x, oy + 5, z, BLACK)
  _set(v, ox + 2, oy + 3, oz + 3, PINK)
  return v


def _generate_epic_inventions_laptop() -> np.ndarray:
  GRAY = _b("gray_concrete")
  BLACK = _b("black_concrete")
  WHITE = _b("white_concrete")
  TRAP = _b("iron_trapdoor")
  LIGHT = _b("light_gray_concrete")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 14, 2
  for x in range(ox, ox + 6):
    for z in range(oz, oz + 4):
      _set(v, x, oy, z, GRAY)
  for x in range(ox + 1, ox + 5):
    _set(v, x, oy + 1, oz + 1, BLACK)
    _set(v, x, oy + 2, oz + 1, BLACK)
    if x == ox + 2:
      _set(v, x, oy + 2, oz + 2, WHITE)
  _set(v, ox + 3, oy + 3, oz + 2, TRAP)
  _set(v, ox, oy, oz + 3, LIGHT)
  return v


def _generate_epic_inventions_bonsai() -> np.ndarray:
  LOG = _b("acacia_log")
  LEAVES = _b("acacia_leaves")
  POT = _b("flower_pot")
  TERRA = _b("terracotta")
  DARK = _b("dark_oak_planks")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 2
  _set(v, cx, oy, cz, POT)
  _set(v, cx, oy, cz + 1, TERRA)
  _set(v, cx + 1, oy, cz, DARK)
  for y in range(oy + 1, oy + 4):
    _set(v, cx, y, cz, LOG)
  for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)):
    _set(v, cx + dx, oy + 4, cz + dz, LEAVES)
    _set(v, cx + dx, oy + 5, cz + dz, LEAVES if abs(dx) + abs(dz) < 2 else AIR_B)
  return v


def _generate_epic_inventions_model_village() -> np.ndarray:
  OAK = _b("oak_planks")
  SPRUCE = _b("spruce_planks")
  GRASS = _b("grass_block")
  LEAVES = _b("oak_leaves")
  WATER = _b("water")
  COBBLE = _b("cobblestone")
  FENCE = _b("oak_fence")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 12, 1
  for x in range(ox, ox + 12):
    for z in range(oz, oz + 8):
      _set(v, x, oy, z, GRASS)
  for hx, hz in ((ox + 2, oz + 2), (ox + 7, oz + 3), (ox + 4, oz + 6)):
    for y in range(oy + 1, oy + 4):
      for x in range(hx, hx + 3):
        for z in range(hz, hz + 3):
          edge = x in (hx, hx + 2) or z in (hz, hz + 2) or y == oy + 3
          if edge:
            _set(v, x, y, z, OAK if y < oy + 3 else SPRUCE)
    _set(v, hx + 1, oy + 4, hz + 1, LEAVES)
  for x in range(ox + 5, ox + 9):
    _set(v, x, oy, oz + 4, COBBLE)
    _set(v, x, oy, oz + 5, WATER)
  _set(v, ox + 9, oy + 1, oz + 6, FENCE)
  return v


def _generate_epic_inventions_calendar() -> np.ndarray:
  WHITE = _b("white_concrete")
  RED = _b("red_concrete")
  BLACK = _b("black_concrete")
  GRAY = _b("gray_concrete")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 15, 1
  for y in range(oy, oy + 10):
    for x in range(ox, ox + 6):
      _set(v, x, y, oz, WHITE if (x + y) % 5 else RED if y == oy + 7 and x == ox + 4 else GRAY if y == oy or x == ox else WHITE)
  _set(v, ox + 2, oy + 9, oz, BLACK)
  return v


def _generate_epic_inventions_saturn_v_rocket() -> np.ndarray:
  WHITE = _b("white_concrete")
  ORANGE = _b("orange_concrete")
  BARS = _b("iron_bars")
  BUTTON = _b("stone_button")
  CAULDRON = _b("cauldron")
  ROD = _b("lightning_rod")
  GRAY = _b("gray_concrete")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 13, 4
  for x in range(ox, ox + 16):
    for z in range(oz, oz + 4):
      _set(v, x, oy, z, WHITE if x % 4 else ORANGE)
      _set(v, x, oy + 1, z, WHITE)
    if x % 3 == 0:
      _set(v, x, oy - 1, oz + 1, BARS)
      _set(v, x, oy - 1, oz + 2, BUTTON)
  for z in range(oz, oz + 4):
    _set(v, ox + 15, oy, z, ROD)
    _set(v, ox - 1, oy, z, CAULDRON)
  _set(v, ox + 7, oy - 1, oz + 1, GRAY)
  return v


def _generate_epic_inventions_poster_run() -> np.ndarray:
  colors = [_b("blue_wool"), _b("light_blue_wool"), _b("green_wool"), _b("yellow_wool"), _b("red_wool")]
  STAIR = _b("oak_stairs")
  WHITE = _b("white_wool")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 13, 1
  for y in range(oy, oy + 14):
    col = colors[min(y // 3, len(colors) - 1)]
    for x in range(ox, ox + 6):
      for z in range(oz, oz + 6):
        edge = x in (ox, ox + 5) or z in (oz, oz + 5)
        if edge:
          _set(v, x, y, z, col)
        elif (x + y) % 2 == 0:
          _set(v, x, y, z, STAIR if y % 2 else WHITE)
  return v


def _generate_epic_inventions_drawer_maze() -> np.ndarray:
  DARK = _b("dark_oak_planks")
  OAK = _b("oak_planks")
  BIRCH = _b("birch_planks")
  STAIR = _b("oak_stairs")
  FENCE = _b("oak_fence")
  TORCH = _b("torch")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 12, 1
  _fill_box(v, ox, oy, oz, 12, 5, 8, DARK, hollow=True)
  walls = [(ox + 3, oz + 2), (ox + 6, oz + 3), (ox + 4, oz + 5), (ox + 8, oz + 4), (ox + 2, oz + 6)]
  for wx, wz in walls:
    for y in range(oy + 1, oy + 4):
      _set(v, wx, y, wz, OAK if y < oy + 3 else BIRCH)
      _set(v, wx + 1, y, wz, FENCE if y == oy + 2 else AIR_B)
  _set(v, ox + 10, oy + 1, oz + 6, STAIR)
  _set(v, ox + 1, oy + 3, oz + 1, TORCH)
  return v


def _generate_epic_inventions_parkour_wall() -> np.ndarray:
  GREEN = _b("green_wool")
  LIME = _b("lime_wool")
  OAK = _b("oak_planks")
  LADDER = _b("ladder")
  YELLOW = _b("yellow_wool")
  BLUE = _b("blue_wool")
  FENCE = _b("oak_fence")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 12, 1
  for y in range(oy, oy + 12):
    for x in range(ox, ox + 14):
      _set(v, x, y, oz, GREEN if y % 2 else LIME)
  platforms = [(ox + 2, oy + 3, oz + 2, OAK), (ox + 6, oy + 5, oz + 4, YELLOW),
               (ox + 10, oy + 7, oz + 3, BLUE), (ox + 4, oy + 9, oz + 5, OAK)]
  for px, py, pz, mat in platforms:
    for dx in range(2):
      for dz in range(2):
        _set(v, px + dx, py, pz + dz, mat)
    _set(v, px, py + 1, pz, LADDER)
  _set(v, ox + 12, oy + 6, oz + 6, FENCE)
  return v


def _generate_epic_inventions_bed_elevator() -> np.ndarray:
  OAK = _b("oak_planks")
  BIRCH = _b("birch_planks")
  PISTON = _b("piston")
  RED = _b("redstone_block")
  OBS = _b("observer")
  SLIME = _b("slime_block")
  FENCE = _b("oak_fence")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 13, 1
  for y in range(oy, oy + 20):
    for x in range(ox, ox + 6):
      for z in range(oz, oz + 6):
        edge = x in (ox, ox + 5) or z in (oz, oz + 5)
        if edge:
          _set(v, x, y, z, OAK if y % 2 else BIRCH)
        elif y % 4 == 2 and x == ox + 2:
          _set(v, x, y, z + 2, PISTON if y % 8 == 2 else SLIME if y % 8 == 6 else OBS)
  _set(v, ox + 2, oy, oz + 2, RED)
  _set(v, ox + 3, oy + 18, oz + 3, FENCE)
  return v


def _generate_epic_inventions_lamp_station() -> np.ndarray:
  PINK = _b("pink_wool")
  YELLOW = _b("yellow_wool")
  OAK = _b("oak_planks")
  RAIL = _b("rail")
  PRAIL = _b("powered_rail")
  GLOW = _b("glowstone")
  WHITE = _b("white_wool")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 12, 2
  for x in range(ox + 2, ox + 6):
    for z in range(oz + 2, oz + 6):
      _set(v, x, oy, z, PINK)
      _set(v, x, oy + 1, z, PINK if x == ox + 2 and z == oz + 2 else AIR_B)
  for y in range(oy + 2, oy + 8):
    _set(v, ox + 3, y, oz + 3, PINK)
  _set(v, ox + 3, oy + 8, oz + 3, GLOW)
  _set(v, ox + 3, oy + 9, oz + 3, WHITE)
  for x in range(ox, ox + 8):
    _set(v, x, oy, oz, OAK)
    _set(v, x, oy + 1, oz + 1, RAIL if x % 2 else PRAIL)
  _set(v, ox + 7, oy + 1, oz + 2, YELLOW)
  return v


def _generate_epic_inventions_bouncy_pillow() -> np.ndarray:
  SLIME = _b("slime_block")
  BLUE = _b("blue_wool")
  YELLOW = _b("yellow_wool")
  WHITE = _b("white_wool")
  LIME = _b("lime_wool")
  GREEN = _b("green_wool")
  LBLUE = _b("light_blue_wool")
  mats = [SLIME, BLUE, YELLOW, WHITE, LIME, GREEN, LBLUE]
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 11, 2
  for x in range(ox, ox + 14):
    for z in range(oz, oz + 10):
      mat = mats[(x + z) % len(mats)]
      _set(v, x, oy, z, mat)
      if (x + z) % 3 == 0:
        _set(v, x, oy + 1, z, SLIME)
  return v


def _generate_epic_inventions_tnt_rocket() -> np.ndarray:
  BLACK = _b("black_concrete")
  WHITE = _b("white_concrete")
  GRAY = _b("gray_concrete")
  TNT = _b("tnt")
  STONE = _b("stone")
  YELLOW = _b("yellow_concrete")
  IRON = _b("iron_block")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 2
  for y in range(oy, oy + 14):
    rad = 5 + (y - oy) // 4
    for x in range(cx - rad, cx + rad + 1):
      for z in range(cz - rad, cz + rad + 1):
        if (x - cx) ** 2 + (z - cz) ** 2 <= rad ** 2:
          _set(v, x, y, z, STONE)
  for y in range(oy + 2, oy + 12):
    stage = (y - oy) // 3
    rad = 3 - stage // 2
    mat = BLACK if stage == 0 else WHITE if stage == 1 else GRAY if stage == 2 else TNT
    for x in range(cx - rad, cx + rad + 1):
      for z in range(cz - rad, cz + rad + 1):
        if (x - cx) ** 2 + (z - cz) ** 2 <= rad ** 2:
          _set(v, x, y, z, mat)
  for x in range(cx - 4, cx + 5):
    for z in range(cz - 4, cz + 5):
      _set(v, x, oy, z, YELLOW if (x + z) % 2 else BLACK)
  _set(v, cx, oy + 12, cz, IRON)
  return v


def _generate_epic_inventions_combat_training() -> np.ndarray:
  OAK = _b("dark_oak_planks")
  STONE = _b("stone")
  BRICK = _b("stone_bricks")
  BARS = _b("iron_bars")
  STAND = _b("armor_stand")
  CHEST = _b("chest")
  TORCH = _b("torch")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 12, 1
  _fill_box(v, ox, oy, oz, 12, 7, 8, STONE, hollow=True)
  for x in range(ox + 1, ox + 11):
    for z in range(oz + 1, oz + 7):
      _set(v, x, oy, z, OAK)
  for x in range(ox + 3, ox + 9, 3):
    for y in range(oy + 1, oy + 5):
      _set(v, x, y, oz + 4, BARS)
    _set(v, x, oy + 1, oz + 2, STAND)
    _set(v, x, oy + 1, oz + 6, CHEST)
  for x in (ox, ox + 11):
    for z in (oz, oz + 7):
      _set(v, x, oy + 4, z, BRICK)
      _set(v, x, oy + 5, z, TORCH)
  return v


def _generate_epic_inventions_shooting_range() -> np.ndarray:
  STONE = _b("stone")
  GRAY = _b("gray_concrete")
  WHITE = _b("white_concrete")
  RED = _b("red_concrete")
  BARS = _b("iron_bars")
  CHEST = _b("chest")
  OAK = _b("oak_planks")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 12, 1
  _fill_box(v, ox, oy, oz, 14, 7, 8, STONE, hollow=True)
  for lane in range(4):
    lx = ox + 2 + lane * 3
    for z in range(oz + 1, oz + 6):
      _set(v, lx, oy, z, GRAY)
    _set(v, lx, oy + 1, oz + 6, WHITE)
    _set(v, lx, oy + 2, oz + 6, RED)
    if lane < 3:
      for y in range(oy + 1, oy + 5):
        _set(v, lx + 2, y, oz + 3, BARS)
  for x in range(ox + 1, ox + 13):
    _set(v, x, oy + 1, oz + 7, CHEST)
  _set(v, ox + 6, oy + 5, oz + 1, OAK)
  return v


def _generate_epic_inventions_skull_silo() -> np.ndarray:
  STONE = _b("stone")
  BRICK = _b("stone_bricks")
  GRAY = _b("gray_concrete")
  GLOW = _b("glowstone")
  ORANGE = _b("orange_terracotta")
  SLAB = _b("smooth_quartz_slab")
  BLACK = _b("black_concrete")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 10):
    rad = 6 - abs(y - oy - 5) // 2
    for x in range(cx - rad, cx + rad + 1):
      for z in range(cz - rad, cz + rad + 1):
        if (x - cx) ** 2 + (z - cz) ** 2 <= rad ** 2:
          edge = (x - cx) ** 2 + (z - cz) ** 2 >= (rad - 1) ** 2
          if edge or y < oy + 3:
            _set(v, x, y, z, STONE if y < oy + 7 else BRICK)
          elif y > oy + 6:
            _set(v, x, y, z, GRAY)
  for ex, ez in ((cx - 3, cz - 2), (cx + 3, cz - 2)):
    _set(v, ex, oy + 5, ez, GLOW)
    _set(v, ex, oy + 4, ez, ORANGE)
  for x in range(cx - 2, cx + 3):
    _set(v, x, oy + 2, cz + 3, BLACK)
  _set(v, cx, oy, cz, SLAB)
  return v


def _generate_epic_inventions_fire_pit() -> np.ndarray:
  STONE = _b("stone")
  BRICK = _b("stone_bricks")
  OAK = _b("dark_oak_planks")
  FIRE = _b("campfire")
  CHEST = _b("chest")
  TORCH = _b("torch")
  SAND = _b("sand")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 12, 1
  _fill_box(v, ox, oy, oz, 10, 7, 8, STONE, hollow=True)
  cx, cz = ox + 5, oz + 4
  _set(v, cx, oy, cz, FIRE)
  for bx, bz in ((cx - 3, cz - 2), (cx + 3, cz - 2), (cx - 3, cz + 2), (cx + 3, cz + 2)):
    _set(v, bx, oy, bz, OAK)
    _set(v, bx, oy + 1, bz, OAK)
  for x in (ox, ox + 9):
    for z in (oz, oz + 7):
      _set(v, x, oy + 1, z, CHEST)
      _set(v, x, oy + 5, z, TORCH)
  _set(v, cx, oy + 6, cz, BRICK)
  _set(v, ox + 4, oy, oz + 3, SAND)
  return v


def _generate_epic_inventions_villain_docks() -> np.ndarray:
  WHITE = _b("white_concrete")
  STONE = _b("stone")
  SAND = _b("sand")
  WATER = _b("water")
  BOAT = _b("oak_boat")
  SLAB = _b("smooth_quartz_slab")
  FENCE = _b("oak_fence")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 7, 12, 3
  for x in range(ox, ox + 18):
    _set(v, x, oy + 4, oz, WHITE)
    _set(v, x, oy + 4, oz + 7, WHITE)
    if x % 4 == 0:
      for y in range(oy, oy + 4):
        _set(v, x, y, oz, STONE)
        _set(v, x, y, oz + 7, STONE)
  for slip in range(3):
    sx = ox + 3 + slip * 5
    for z in range(oz + 1, oz + 7):
      _set(v, sx, oy, z, WATER)
      _set(v, sx + 1, oy, z, WATER)
    _set(v, sx, oy + 1, oz + 3, BOAT)
    _set(v, sx, oy, oz, SLAB)
  for x in range(ox, ox + 18):
    _set(v, x, oy - 1, oz - 1, SAND)
  _set(v, ox + 8, oy + 2, oz + 3, FENCE)
  return v


def _generate_epic_inventions_hidden_door() -> np.ndarray:
  SHELF = _b("bookshelf")
  LECTERN = _b("lectern")
  COMP = _b("comparator")
  DUST = _b("redstone_dust")
  DOOR = _b("iron_door")
  BRICK = _b("stone_bricks")
  OAK = _b("oak_planks")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 14, 1
  for y in range(oy, oy + 7):
    for x in range(ox, ox + 8):
      _set(v, x, y, oz, SHELF if y < oy + 6 else BRICK)
  _set(v, ox + 3, oy + 1, oz + 1, LECTERN)
  _set(v, ox + 3, oy + 1, oz + 2, COMP)
  _set(v, ox + 4, oy + 1, oz + 2, DUST)
  _set(v, ox + 5, oy + 1, oz + 2, DOOR)
  _set(v, ox + 5, oy + 2, oz + 2, DOOR)
  for y in range(oy + 1, oy + 4):
    _set(v, ox + 6, y, oz + 3, OAK)
  return v


def _generate_epic_inventions_creeper_farm() -> np.ndarray:
  GRAY = _b("gray_concrete")
  WHITE = _b("white_concrete")
  IRON = _b("iron_block")
  GLASS = _b("glass")
  LAVA = _b("lava")
  WATER = _b("water")
  HOPPER = _b("hopper")
  CHEST = _b("chest")
  TRAP = _b("dark_oak_trapdoor")
  CARPET = _b("orange_carpet")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 10, 1
  for x in range(ox, ox + 16):
    for z in range(oz, oz + 12):
      _set(v, x, oy, z, GRAY)
  for x in range(ox + 4, ox + 12):
    for z in range(oz + 4, oz + 8):
      _set(v, x, oy + 1, z, CARPET if (x + z) % 2 else AIR_B)
      if x == ox + 7:
        _set(v, x, oy + 2, z, IRON if z % 2 else WHITE)
  for x in range(ox + 6, ox + 10):
    _set(v, x, oy + 1, oz + 2, WATER)
    _set(v, x, oy + 1, oz + 9, LAVA)
    _set(v, x, oy, oz + 5, HOPPER)
  _set(v, ox + 7, oy, oz + 5, CHEST)
  for x in range(ox + 3, ox + 13):
    for z in range(oz + 3, oz + 9):
      _set(v, x, oy + 4, z, TRAP)
      if (x + z) % 3 == 0:
        _set(v, x, oy + 3, z, GLASS)
  return v


def _generate_epic_inventions_soul_campfires() -> np.ndarray:
  SAND = _b("sandstone")
  GOLD = _b("gold_block")
  EMERALD = _b("emerald_block")
  SOUL = _b("soul_campfire")
  GLASS = _b("blue_stained_glass")
  SMOOTH = _b("smooth_sandstone")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 13, 1
  _fill_box(v, ox, oy, oz, 8, 7, 6, SAND, hollow=True)
  for ax, az in ((ox + 2, oz + 1), (ox + 5, oz + 1), (ox + 2, oz + 4), (ox + 5, oz + 4)):
    _set(v, ax, oy, az, SOUL)
    _set(v, ax, oy + 3, az, EMERALD)
    _set(v, ax - 1, oy + 1, az, GLASS)
  _set(v, ox + 3, oy + 6, oz + 2, GOLD)
  _set(v, ox + 4, oy + 6, oz + 3, SMOOTH)
  return v


def _generate_epic_inventions_exterior_bling() -> np.ndarray:
  EMERALD = _b("emerald_block")
  DIAMOND = _b("diamond_block")
  GLASS = _b("blue_stained_glass")
  QUARTZ = _b("quartz_block")
  GOLD = _b("gold_block")
  LANTERN = _b("sea_lantern")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 4
  for x in range(cx - 5, cx + 6):
    for z in range(cz - 5, cz + 6):
      d2 = (x - cx) ** 2 + (z - cz) ** 2
      if 16 <= d2 <= 25:
        _set(v, x, oy, z, DIAMOND if d2 >= 20 else GLASS)
      elif d2 <= 9:
        _set(v, x, oy, z, EMERALD)
      elif d2 <= 12:
        _set(v, x, oy, z, GOLD)
  _set(v, cx, oy + 1, cz, LANTERN)
  _set(v, cx, oy - 1, cz, QUARTZ)
  return v


def _generate_epic_inventions_entrance_hall() -> np.ndarray:
  SAND = _b("sandstone")
  SMOOTH = _b("smooth_sandstone")
  EMERALD = _b("emerald_block")
  GLASS = _b("blue_stained_glass")
  QUARTZ = _b("quartz_block")
  GOLD = _b("gold_block")
  LANTERN = _b("sea_lantern")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 11, 1
  for y in range(oy, oy + 11):
    for x in range(ox, ox + 14):
      for z in range(oz, oz + 10):
        edge = x in (ox, ox + 13) or z in (oz, oz + 9) or y == oy + 10
        if edge:
          _set(v, x, y, z, SAND if y < oy + 8 else SMOOTH)
        elif y == oy:
          _set(v, x, oy, z, QUARTZ if (x + z) % 2 else GLASS)
        else:
          _set(v, x, y, z, AIR_B)
  for px in (ox + 2, ox + 11):
    for y in range(oy + 1, oy + 9):
      _set(v, px, y, oz + 1, EMERALD if y % 3 else GOLD)
  _set(v, ox + 6, oy + 9, oz + 4, LANTERN)
  return v


def _generate_epic_inventions_level_end() -> np.ndarray:
  QUARTZ = _b("quartz_block")
  STAIR = _b("quartz_stairs")
  DISP = _b("dispenser")
  TORCH = _b("redstone_torch")
  SAND = _b("sandstone")
  EMERALD = _b("emerald_block")
  CHEST = _b("chest")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 12, 1
  _fill_box(v, ox, oy, oz, 8, 9, 8, SAND, hollow=True)
  cx, cz = ox + 4, oz + 4
  for y in range(oy + 1, oy + 8):
    for step in range(4):
      _set(v, cx + step, oy + 1 + step * 2, cz + step, STAIR)
  for x in range(ox + 1, ox + 7):
    _set(v, x, oy + 4, oz + 7, DISP)
    _set(v, x, oy + 5, oz + 7, TORCH if x % 2 else EMERALD)
  _set(v, ox + 3, oy + 1, oz + 3, CHEST)
  _set(v, ox + 6, oy + 7, oz + 6, QUARTZ)
  return v


def _generate_epic_inventions_ascension_tower() -> np.ndarray:
  SAND = _b("sandstone")
  SMOOTH = _b("smooth_sandstone")
  GLASS = _b("blue_stained_glass")
  EMERALD = _b("emerald_block")
  GOLD = _b("gold_block")
  STAIR = _b("quartz_stairs")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 13, 1
  for y in range(oy, oy + 18):
    for x in range(ox, ox + 6):
      for z in range(oz, oz + 6):
        edge = x in (ox, ox + 5) or z in (oz, oz + 5)
        if edge:
          _set(v, x, y, z, GLASS if y % 3 == 0 and x == ox + 2 else EMERALD if y % 5 == 0 else SAND)
        elif (x + z) % 3 == 0:
          _set(v, x, y, z, STAIR if y % 2 else AIR_B)
    if y % 4 == 0:
      _set(v, ox + 2, y, oz + 2, GOLD)
  _set(v, ox + 2, oy + 17, oz + 2, SMOOTH)
  return v


def _generate_epic_inventions_diamond_statue() -> np.ndarray:
  RED = _b("red_sandstone")
  SRED = _b("smooth_red_sandstone")
  DIAMOND = _b("diamond_block")
  GOLD = _b("gold_block")
  LANTERN = _b("sea_lantern")
  QUARTZ = _b("quartz_block")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  for y in range(oy, oy + 12):
    for x in range(cx - 2, cx + 3):
      for z in range(cz - 1, cz + 2):
        _set(v, x, y, z, RED if y < oy + 10 else SRED)
  for y in range(oy + 8, oy + 12):
    _set(v, cx + 3, y, cz, RED)
  _set(v, cx + 4, oy + 10, cz, DIAMOND)
  _set(v, cx + 4, oy + 11, cz, LANTERN)
  _set(v, cx, oy, cz - 1, QUARTZ)
  _set(v, cx + 1, oy + 6, cz, GOLD)
  return v


def _generate_epic_inventions_elytra_launcher() -> np.ndarray:
  FRAME = _b("end_portal_frame")
  EYE = _b("ender_eye")
  SLIME = _b("slime_block")
  PISTON = _b("piston")
  REPEATER = _b("redstone_repeater")
  DUST = _b("redstone_dust")
  OBS = _b("obsidian")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 12, 1
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 6):
      _set(v, x, oy + 4, z, FRAME if (x + z) % 2 else OBS)
  _set(v, ox + 3, oy + 4, oz + 2, EYE)
  for x in range(ox + 1, ox + 7):
    _set(v, x, oy + 2, oz + 2, SLIME)
    _set(v, x, oy + 1, oz + 2, PISTON)
    _set(v, x, oy, oz + 3, REPEATER if x % 2 else DUST)
  return v


def _generate_epic_inventions_riddle_clue() -> np.ndarray:
  LOG = _b("oak_log")
  GATE = _b("dark_oak_fence_gate")
  LANTERN = _b("sea_lantern")
  SAND = _b("sandstone")
  LEVER = _b("lever")
  GOLD = _b("gold_block")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 13, 1
  counts = (1, 3, 5)
  for i, count in enumerate(counts):
    px = ox + i * 3
    for y in range(oy, oy + 8):
      _set(v, px, y, oz + 2, LOG)
    _set(v, px, oy + 8, oz + 2, LANTERN)
    for g in range(count):
      _set(v, px + 1, oy + 2 + g * 2, oz + 2, GATE)
  _set(v, ox + 4, oy, oz, SAND)
  _set(v, ox + 7, oy + 1, oz + 4, LEVER)
  _set(v, ox + 1, oy + 9, oz + 1, GOLD)
  return v


def _generate_epic_inventions_lever_puzzle() -> np.ndarray:
  SAND = _b("sandstone")
  LEVER = _b("lever")
  RTORCH = _b("redstone_torch")
  REPEATER = _b("redstone_repeater")
  DUST = _b("redstone_dust")
  CHEST = _b("chest")
  DOOR = _b("iron_door")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 14, 1
  for i in range(6):
    _set(v, ox + i, oy + 2, oz, LEVER)
    _set(v, ox + i, oy + 2, oz + 1, RTORCH if i % 2 else REPEATER)
    _set(v, ox + i, oy + 1, oz + 2, DUST)
  _fill_box(v, ox, oy, oz, 10, 6, 4, SAND, hollow=True)
  _set(v, ox + 8, oy + 1, oz + 2, CHEST)
  _set(v, ox + 9, oy + 1, oz + 2, DOOR)
  _set(v, ox + 9, oy + 2, oz + 2, DOOR)
  return v


def _generate_epic_inventions_time_lock() -> np.ndarray:
  BRICK = _b("stone_bricks")
  HOPPER = _b("hopper")
  COMP = _b("comparator")
  REPEATER = _b("redstone_repeater")
  SPISTON = _b("sticky_piston")
  RTORCH = _b("redstone_torch")
  LEVER = _b("lever")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 12, 3
  for x in range(ox, ox + 14):
    _set(v, x, oy, oz + 2, BRICK)
    if x % 2 == 0:
      _set(v, x, oy + 1, oz + 2, HOPPER)
    else:
      _set(v, x, oy + 1, oz + 2, REPEATER)
  _set(v, ox + 6, oy + 1, oz + 3, COMP)
  _set(v, ox + 7, oy + 1, oz + 3, SPISTON)
  _set(v, ox + 8, oy + 1, oz + 3, RTORCH)
  _set(v, ox, oy + 1, oz + 1, LEVER)
  return v


def _generate_epic_inventions_reward_dispenser() -> np.ndarray:
  SAND = _b("sandstone")
  CYAN = _b("cyan_terracotta")
  DISP = _b("dispenser")
  TORCH = _b("redstone_torch")
  GOLD = _b("gold_block")
  EMERALD = _b("emerald_block")
  QUARTZ = _b("quartz_block")
  AIR_B = AIR
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 13, 1
  for y in range(oy, oy + 7):
    for x in range(ox, ox + 6):
      _set(v, x, y, oz, SAND if y < oy + 5 else CYAN)
      _set(v, x, y, oz + 5, SAND if y < oy + 5 else CYAN)
  for y in range(oy, oy + 6):
    _set(v, ox, y, oz + 2, CYAN if y % 2 else SAND)
    _set(v, ox + 5, y, oz + 2, CYAN if y % 2 else SAND)
  _set(v, ox + 2, oy + 6, oz + 2, DISP)
  _set(v, ox + 2, oy, oz + 2, TORCH)
  _set(v, ox + 3, oy + 3, oz + 2, GOLD)
  _set(v, ox + 1, oy + 4, oz + 3, EMERALD)
  _set(v, ox + 4, oy + 7, oz + 3, QUARTZ)
  return v


_GENERATORS: dict[str, object] = {
  "epic_inventions_mob_hospital": _generate_epic_inventions_mob_hospital,
  "epic_inventions_sanctuary_farm": _generate_epic_inventions_sanctuary_farm,
  "epic_inventions_sanctuary_tower": _generate_epic_inventions_sanctuary_tower,
  "epic_inventions_bee_habitat": _generate_epic_inventions_bee_habitat,
  "epic_inventions_marine_sanctuary": _generate_epic_inventions_marine_sanctuary,
  "epic_inventions_horse_stable": _generate_epic_inventions_horse_stable,
  "epic_inventions_forcefield_emitter": _generate_epic_inventions_forcefield_emitter,
  "epic_inventions_villager_housing": _generate_epic_inventions_villager_housing,
  "epic_inventions_mob_feeder": _generate_epic_inventions_mob_feeder,
  "epic_inventions_water_trough": _generate_epic_inventions_water_trough,
  "epic_inventions_pumpkin_farm": _generate_epic_inventions_pumpkin_farm,
  "epic_inventions_enchanting_tower": _generate_epic_inventions_enchanting_tower,
  "epic_inventions_gothic_buttress": _generate_epic_inventions_gothic_buttress,
  "epic_inventions_stained_glass_window": _generate_epic_inventions_stained_glass_window,
  "epic_inventions_golem_maker": _generate_epic_inventions_golem_maker,
  "epic_inventions_storm_catcher": _generate_epic_inventions_storm_catcher,
  "epic_inventions_golem_factory_ring": _generate_epic_inventions_golem_factory_ring,
  "epic_inventions_cat_shrine": _generate_epic_inventions_cat_shrine,
  "epic_inventions_spectator_stands": _generate_epic_inventions_spectator_stands,
  "epic_inventions_rainbow_bridge": _generate_epic_inventions_rainbow_bridge,
  "epic_inventions_rainbow_finish_arch": _generate_epic_inventions_rainbow_finish_arch,
  "epic_inventions_floating_cloud": _generate_epic_inventions_floating_cloud,
  "epic_inventions_reverse_waterfall": _generate_epic_inventions_reverse_waterfall,
  "epic_inventions_rainbow_piston_bridge": _generate_epic_inventions_rainbow_piston_bridge,
  "epic_inventions_bridge_island": _generate_epic_inventions_bridge_island,
  "epic_inventions_jump_island": _generate_epic_inventions_jump_island,
  "epic_inventions_potions_lab": _generate_epic_inventions_potions_lab,
  "epic_inventions_briefing_room": _generate_epic_inventions_briefing_room,
  "epic_inventions_research_cells": _generate_epic_inventions_research_cells,
  "epic_inventions_sword_mosaic": _generate_epic_inventions_sword_mosaic,
  "epic_inventions_corrosive_lab": _generate_epic_inventions_corrosive_lab,
  "epic_inventions_battery_power": _generate_epic_inventions_battery_power,
  "epic_inventions_vine_room": _generate_epic_inventions_vine_room,
  "epic_inventions_piston_extender": _generate_epic_inventions_piston_extender,
  "epic_inventions_nether_transport_hub": _generate_epic_inventions_nether_transport_hub,
  "epic_inventions_defense_barrier": _generate_epic_inventions_defense_barrier,
  "epic_inventions_disposal_unit": _generate_epic_inventions_disposal_unit,
  "epic_inventions_backup_generator": _generate_epic_inventions_backup_generator,
  "epic_inventions_mechanical_leg": _generate_epic_inventions_mechanical_leg,
  "epic_inventions_bunkhouse": _generate_epic_inventions_bunkhouse,
  "epic_inventions_band_pavilion": _generate_epic_inventions_band_pavilion,
  "epic_inventions_control_sphere": _generate_epic_inventions_control_sphere,
  "epic_inventions_saloon_stables": _generate_epic_inventions_saloon_stables,
  "epic_inventions_ornithopter": _generate_epic_inventions_ornithopter,
  "epic_inventions_piston_bar": _generate_epic_inventions_piston_bar,
  "epic_inventions_dunking_stool": _generate_epic_inventions_dunking_stool,
  "epic_inventions_smoke_stack": _generate_epic_inventions_smoke_stack,
  "epic_inventions_waterfall_elevator": _generate_epic_inventions_waterfall_elevator,
  "epic_inventions_signal_ladder": _generate_epic_inventions_signal_ladder,
  "epic_inventions_aqueduct": _generate_epic_inventions_aqueduct,
  "epic_inventions_cave_network": _generate_epic_inventions_cave_network,
  "epic_inventions_treasure_room": _generate_epic_inventions_treasure_room,
  "epic_inventions_temple_tower": _generate_epic_inventions_temple_tower,
  "epic_inventions_gravel_trap": _generate_epic_inventions_gravel_trap,
  "epic_inventions_banyan_altar": _generate_epic_inventions_banyan_altar,
  "epic_inventions_combination_door": _generate_epic_inventions_combination_door,
  "epic_inventions_control_bridge": _generate_epic_inventions_control_bridge,
  "epic_inventions_space_engine": _generate_epic_inventions_space_engine,
  "epic_inventions_crew_lounge": _generate_epic_inventions_crew_lounge,
  "epic_inventions_ring_section": _generate_epic_inventions_ring_section,
  "epic_inventions_hydroponics": _generate_epic_inventions_hydroponics,
  "epic_inventions_berry_farm": _generate_epic_inventions_berry_farm,
  "epic_inventions_kelp_farm": _generate_epic_inventions_kelp_farm,
  "epic_inventions_airlock": _generate_epic_inventions_airlock,
  "epic_inventions_melon_farm": _generate_epic_inventions_melon_farm,
  "epic_inventions_solar_array": _generate_epic_inventions_solar_array,
  "epic_inventions_aquarium": _generate_epic_inventions_aquarium,
  "epic_inventions_piggy_banks": _generate_epic_inventions_piggy_banks,
  "epic_inventions_creeper_toy": _generate_epic_inventions_creeper_toy,
  "epic_inventions_laptop": _generate_epic_inventions_laptop,
  "epic_inventions_bonsai": _generate_epic_inventions_bonsai,
  "epic_inventions_model_village": _generate_epic_inventions_model_village,
  "epic_inventions_calendar": _generate_epic_inventions_calendar,
  "epic_inventions_saturn_v_rocket": _generate_epic_inventions_saturn_v_rocket,
  "epic_inventions_poster_run": _generate_epic_inventions_poster_run,
  "epic_inventions_drawer_maze": _generate_epic_inventions_drawer_maze,
  "epic_inventions_parkour_wall": _generate_epic_inventions_parkour_wall,
  "epic_inventions_bed_elevator": _generate_epic_inventions_bed_elevator,
  "epic_inventions_lamp_station": _generate_epic_inventions_lamp_station,
  "epic_inventions_bouncy_pillow": _generate_epic_inventions_bouncy_pillow,
  "epic_inventions_tnt_rocket": _generate_epic_inventions_tnt_rocket,
  "epic_inventions_combat_training": _generate_epic_inventions_combat_training,
  "epic_inventions_shooting_range": _generate_epic_inventions_shooting_range,
  "epic_inventions_skull_silo": _generate_epic_inventions_skull_silo,
  "epic_inventions_fire_pit": _generate_epic_inventions_fire_pit,
  "epic_inventions_villain_docks": _generate_epic_inventions_villain_docks,
  "epic_inventions_hidden_door": _generate_epic_inventions_hidden_door,
  "epic_inventions_creeper_farm": _generate_epic_inventions_creeper_farm,
  "epic_inventions_soul_campfires": _generate_epic_inventions_soul_campfires,
  "epic_inventions_exterior_bling": _generate_epic_inventions_exterior_bling,
  "epic_inventions_entrance_hall": _generate_epic_inventions_entrance_hall,
  "epic_inventions_level_end": _generate_epic_inventions_level_end,
  "epic_inventions_ascension_tower": _generate_epic_inventions_ascension_tower,
  "epic_inventions_diamond_statue": _generate_epic_inventions_diamond_statue,
  "epic_inventions_elytra_launcher": _generate_epic_inventions_elytra_launcher,
  "epic_inventions_riddle_clue": _generate_epic_inventions_riddle_clue,
  "epic_inventions_lever_puzzle": _generate_epic_inventions_lever_puzzle,
  "epic_inventions_time_lock": _generate_epic_inventions_time_lock,
  "epic_inventions_reward_dispenser": _generate_epic_inventions_reward_dispenser,
}
