"""Procedural generators for Bite-Sized Builds."""

from __future__ import annotations

import numpy as np

from ..data.palette import AIR
from .bite_sized_registry import BITE_SIZED_BUILDS


def generate_bite_sized(build_id: str) -> np.ndarray:
  if build_id not in BITE_SIZED_BUILDS:
    raise KeyError(f"Unknown bite-sized build: {build_id}")
  fn = _GENERATORS.get(build_id)
  if fn is None:
    raise NotImplementedError(f"No generator for {build_id}")
  return fn()


def _b(name: str) -> str:
  return name if name.startswith("minecraft:") else f"minecraft:{name}"


def _set(v: np.ndarray, x: int, y: int, z: int, block: str) -> None:
  if 0 <= x < v.shape[0] and 0 <= y < v.shape[1] and 0 <= z < v.shape[2]:
    v[x, y, z] = block


def _green_texture(x: int, y: int, z: int, *mats: str) -> str:
  return mats[(x + y + z) % len(mats)]


def _generate_bite_creeper() -> np.ndarray:
  """
  Creeper in the Woods — book dimensions:
    Head 5×5×5, body 5×7×3, feet 2×(3×4×5), ~16 blocks tall.
  """
  GREEN = _b("green_concrete")
  LIME = _b("lime_terracotta")
  POWDER = _b("green_concrete_powder")
  WHITE = _b("white_concrete")
  GRAY = _b("gray_concrete")
  TERRA = _b("green_terracotta")
  GRASS = _b("grass_block")
  LOG = _b("oak_log")
  LEAVES = _b("oak_leaves")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz = 16, 16
  oy = 2

  body_mats = (POWDER, WHITE, LIME)
  head_mats = (GREEN, LIME, GREEN)
  foot_mats = (TERRA, GREEN)

  def _fill_box(x0: int, y0: int, z0: int, w: int, h: int, d: int, mat_fn) -> None:
    for y in range(y0, y0 + h):
      for x in range(x0, x0 + w):
        for z in range(z0, z0 + d):
          mat = mat_fn(x, y, z) if callable(mat_fn) else mat_fn
          _set(v, x, y, z, mat)

  # Feet (y 0-3): two 3×4×5 blocks with 1-block gap
  foot_y, foot_h, foot_d = oy, 4, 5
  foot_w = 3
  left_x = cx - foot_w - 1
  right_x = cx + 1
  foot_z = cz - foot_d // 2
  for fx in (left_x, right_x):
    _fill_box(fx, foot_y, foot_z, foot_w, foot_h, foot_d,
              lambda x, y, z, m=foot_mats: _green_texture(x, y, z, *m))

  # Body (y 4-10): 5×7×3 centered on x
  body_y = oy + 4
  body_w, body_h, body_d = 5, 7, 3
  body_x = cx - body_w // 2
  body_z = cz - body_d // 2
  _fill_box(body_x, body_y, body_z, body_w, body_h, body_d,
            lambda x, y, z: _green_texture(x, y, z, *body_mats))

  # Head (y 11-15): 5×5×5 cube
  head_y = oy + 11
  head_s = 5
  head_x = cx - head_s // 2
  head_z = cz - head_s // 2
  _fill_box(head_x, head_y, head_z, head_s, head_s, head_s,
            lambda x, y, z: _green_texture(x, y, z, *head_mats))

  # Creeper face on front of head (+z face)
  face_z = head_z + head_s - 1
  # Eyes
  _set(v, head_x + 1, head_y + 2, face_z, GRAY)
  _set(v, head_x + 3, head_y + 2, face_z, GRAY)
  # Mouth (2×1)
  _set(v, head_x + 1, head_y + 1, face_z, GRAY)
  _set(v, head_x + 2, head_y + 1, face_z, GRAY)

  # Forest floor and trees
  for x in range(8, 25):
    for z in range(8, 25):
      _set(v, x, oy - 1, z, GRASS)

  for tx, tz in ((10, 12), (22, 20), (11, 22), (21, 11)):
    for y in range(oy, oy + 5):
      _set(v, tx, y, tz, LOG)
    for dy in range(3, 6):
      for dx in range(-2, 3):
        for dz in range(-2, 3):
          if abs(dx) + abs(dz) < 3:
            _set(v, tx + dx, oy + dy, tz + dz, LEAVES)

  return v


def _generate_bite_toadstool_house() -> np.ndarray:
  """
  Toadstool House — book steps 1-10:
    7×8 base cottage, 3×3 mushroom stem, red mushroom cap upper room.
  """
  COBBLE = _b("cobblestone")
  MOSSY = _b("mossy_cobblestone")
  SPRUCE = _b("spruce_planks")
  STEM = _b("mushroom_stem")
  RED = _b("red_mushroom_block")
  OAK_S = _b("oak_stairs")
  OAK_SL = _b("oak_slab")
  SPRUCE_S = _b("spruce_stairs")
  SPRUCE_L = _b("spruce_log")
  GLASS = _b("glass_pane")
  LANTERN = _b("lantern")
  VINE = _b("vine")
  FENCE = _b("spruce_fence")
  DOOR = _b("oak_door")
  LADDER = _b("ladder")
  TRAP = _b("oak_trapdoor")
  BED = _b("red_bed")
  CHEST = _b("chest")
  CRAFT = _b("crafting_table")
  CARPET = _b("green_carpet")
  GRASS = _b("grass_block")
  LEAVES = _b("oak_leaves")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz = 16, 16
  oy = 1
  fw, fd = 7, 8
  fx, fz = cx - fw // 2, cz - fd // 2

  # Step 1: Foundation
  for x in range(fx, fx + fw):
    for z in range(fz, fz + fd):
      edge = x in (fx, fx + fw - 1) or z in (fz, fz + fd - 1)
      _set(v, x, oy, z, COBBLE if edge else MOSSY)
  for z in range(fz + 2, fz + fd - 2):
    _set(v, cx, oy, z, SPRUCE)
    _set(v, cx - 1, oy, z, SPRUCE)

  # Ground around house
  for x in range(fx - 2, fx + fw + 2):
    for z in range(fz - 2, fz + fd + 2):
      _set(v, x, oy - 1, z, GRASS)

  # Steps 2-3: Lower walls (4 blocks high)
  wall_h = 4
  for y in range(oy + 1, oy + 1 + wall_h):
    for x in range(fx, fx + fw):
      for z in range(fz, fz + fd):
        edge = x in (fx, fx + fw - 1) or z in (fz, fz + fd - 1)
        if edge:
          if z == fz + fd // 2 and x == cx and y < oy + 3:
            _set(v, x, y, z, AIR_B)  # door
          elif y == oy + 2 and z in (fz, fz + fd - 1) and x in (fx + 1, fx + fw - 2):
            _set(v, x, y, z, GLASS)
          else:
            _set(v, x, y, z, MOSSY if (x + z) % 2 else STEM)
        else:
          _set(v, x, y, z, AIR_B)

  _set(v, cx, oy + 1, fz + fd // 2, DOOR)
  _set(v, cx - 1, oy + 1, cz, CHEST)
  _set(v, cx + 1, oy + 1, cz, CHEST)
  _set(v, cx, oy + 1, cz, TRAP)
  _set(v, cx, oy + 2, cz, LADDER)

  # Step 4: Small oak roof over doorway
  roof_y = oy + 1 + wall_h
  for x in range(cx - 1, cx + 2):
    for z in range(fz, fz + 3):
      _set(v, x, roof_y, z, OAK_S)

  # Steps 4-5: Mushroom stem (3×3 hollow, ~9 blocks)
  stem_h = 9
  stem_y0 = roof_y
  for y in range(stem_y0, stem_y0 + stem_h):
    for x in range(cx - 1, cx + 2):
      for z in range(cz - 1, cz + 2):
        edge = x in (cx - 1, cx + 1) or z in (cz - 1, cz + 1)
        if edge:
          _set(v, x, y, z, STEM)
        else:
          _set(v, x, y, z, AIR_B)
          if y > stem_y0:
            _set(v, x, y, z, LADDER)

  # Vines on stem
  for y in range(stem_y0 + 2, stem_y0 + stem_h - 1):
    _set(v, cx + 2, y, cz, VINE)

  # Steps 6-10: Mushroom cap
  cap_y0 = stem_y0 + stem_h
  cap_r = 4  # ~9 block diameter

  for layer in range(5):
    y = cap_y0 + layer
    r = cap_r - (layer // 2)
    for x in range(cx - r, cx + r + 1):
      for z in range(cz - r, cz + r + 1):
        dist = max(abs(x - cx), abs(z - cz))
        if dist > r:
          continue
        if dist < r - 1 and layer < 3:
          if layer == 0:
            _set(v, x, y, z, CARPET if (x + z) % 3 else SPRUCE)
          else:
            _set(v, x, y, z, AIR_B)
          # Interior furniture
          if layer == 0 and x == cx and z == cz:
            _set(v, x, y, z, CRAFT)
          if layer == 0 and x == cx + 2 and z == cz:
            _set(v, x, y, z, BED)
        else:
          _set(v, x, y, z, RED)

  # Windows on four sides
  for dx, dz in ((0, cap_r), (0, -cap_r), (cap_r, 0), (-cap_r, 0)):
    wx, wz = cx + dx, cz + dz
    wy = cap_y0 + 2
    if 0 <= wx < 32 and 0 <= wz < 32:
      _set(v, wx, wy, wz, GLASS)
      _set(v, wx, wy + 1, wz, GLASS)

  # Lanterns under cap
  for dx, dz in ((2, 2), (-2, 2), (2, -2), (-2, -2)):
    _set(v, cx + dx, cap_y0 - 1, cz + dz, FENCE)
    _set(v, cx + dx, cap_y0 - 2, cz + dz, LANTERN)

  # Cap roof peak (3×3 red on top)
  top_y = cap_y0 + 5
  for x in range(cx - 1, cx + 2):
    for z in range(cz - 1, cz + 2):
      _set(v, x, top_y, z, RED)

  # Garden bushes
  for bx, bz in ((fx - 1, fz), (fx + fw, fz + 2), (fx + 1, fz + fd)):
    _set(v, bx, oy, bz, LEAVES)

  return v


def _generate_bite_alarm_system() -> np.ndarray:
  """Alarm System — 4×4 stone brick gateway with bells and pressure plates."""
  STONE = _b("stone_bricks")
  CHISELED = _b("chiseled_stone_bricks")
  ANDESITE = _b("polished_andesite_stairs")
  FLOOR = _b("stone")
  DOOR = _b("spruce_door")
  PLATE = _b("stone_pressure_plate")
  GLOW = _b("glowstone")
  BUTTON = _b("stone_button")
  BELL = _b("bell")
  OBSERVER = _b("observer")
  TORCH = _b("redstone_torch")
  DUST = _b("redstone_dust")
  SB_STAIRS = _b("stone_brick_stairs")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz = 16, 16
  oy = 2
  s = 4  # 4×4 gateway

  gx, gz = cx - s // 2, cz - s // 2

  # Foundation + redstone dust U under plates
  for x in range(gx, gx + s):
    for z in range(gz, gz + s):
      _set(v, x, oy, z, FLOOR)
  for x in range(gx, gx + s):
    _set(v, x, oy, gz, DUST)
    _set(v, x, oy, gz + s - 1, DUST)
  for z in range(gz + 1, gz + s - 1):
    _set(v, gx, oy, z, DUST)
    _set(v, gx + s - 1, oy, z, DUST)

  # Walls (3 high) + extending stone wall
  for y in range(oy + 1, oy + 4):
    for x in range(gx, gx + s):
      for z in range(gz, gz + s):
        edge = x in (gx, gx + s - 1) or z in (gz, gz + s - 1)
        if edge:
          if z == gz + 1 and x == cx and y < oy + 3:
            _set(v, x, y, z, AIR_B)
          elif z == gz + 2 and x == cx and y < oy + 3:
            _set(v, x, y, z, AIR_B)
          else:
            corner = x in (gx, gx + s - 1) and z in (gz, gz + s - 1)
            _set(v, x, y, z, CHISELED if corner and y == oy + 3 else STONE)
        else:
          _set(v, x, y, z, AIR_B)

  # Double doors
  _set(v, cx, oy + 1, gz + 1, DOOR)
  _set(v, cx, oy + 1, gz + 2, DOOR)
  _set(v, cx, oy + 2, gz + 1, DOOR)
  _set(v, cx, oy + 2, gz + 2, DOOR)

  # Pressure plates
  _set(v, cx, oy + 1, gz, PLATE)
  _set(v, cx - 1, oy + 1, gz + 1, PLATE)
  _set(v, cx + 1, oy + 1, gz + 2, PLATE)

  # Facade roof (step 1 exploded top)
  roof_y = oy + 4
  for x in range(gx, gx + s):
    for z in range(gz, gz + s):
      _set(v, x, roof_y, z, ANDESITE)
  _set(v, cx, roof_y + 1, cz, GLOW)
  _set(v, gx, roof_y, gz + 1, BUTTON)
  _set(v, gx + s - 1, roof_y, gz + 2, BUTTON)

  # Alarm mechanism (side column with bells)
  ax = gx + s + 1
  for y in range(oy + 1, oy + 5):
    _set(v, ax, y, cz, STONE)
  _set(v, ax, oy + 1, cz + 1, TORCH)
  _set(v, ax, oy + 2, cz, BELL)
  _set(v, ax, oy + 3, cz, OBSERVER)
  _set(v, ax, oy + 4, cz, BELL)
  _set(v, ax, oy + 2, cz + 1, SB_STAIRS)
  _set(v, ax, oy + 3, cz + 1, SB_STAIRS)

  # Flanking wall sections
  for x in range(gx - 6, gx):
    for y in range(oy + 1, oy + 4):
      _set(v, x, y, cz, STONE)
  for x in range(gx + s, gx + s + 6):
    for y in range(oy + 1, oy + 4):
      _set(v, x, y, cz, STONE)

  return v


def _generate_bite_combination_lock() -> np.ndarray:
  """Combination Lock — 9×5×3 lever panel with lamps, iron door, AND gate wiring."""
  STONE = _b("stone_bricks")
  ANDESITE = _b("polished_andesite")
  WALL = _b("cobblestone_wall")
  BLACK = _b("chiseled_polished_blackstone")
  BASE = _b("stone")
  DOOR = _b("iron_door")
  LEVER = _b("lever")
  LAMP = _b("redstone_lamp")
  TORCH = _b("redstone_torch")
  DUST = _b("redstone_dust")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz = 16, 16
  oy = 3
  w, h, d = 9, 5, 3
  wx, wz = cx - w // 2, cz - 1

  # Back wall and sides (3 deep)
  for y in range(oy, oy + h):
    for x in range(wx, wx + w):
      for z in range(wz, wz + d):
        front = z == wz + d - 1
        if front:
          if y == oy + 2 and x in (wx + 1, wx + 3, wx + 5, wx + 7):
            _set(v, x, y, z, LEVER)
          elif y == oy + 3 and x in (wx + 1, wx + 3, wx + 5, wx + 7):
            _set(v, x, y, z, LAMP)
          elif y == oy + 1 and x in (wx + 3, wx + 4):
            _set(v, x, y, z, AIR_B)  # iron door gap
          else:
            trim = x in (wx, wx + w - 1) or y in (oy, oy + h - 1)
            _set(v, x, y, z, BLACK if trim else STONE)
        else:
          edge = x in (wx, wx + w - 1) or y in (oy, oy + h - 1)
          if edge:
            _set(v, x, y, z, ANDESITE if y == oy else STONE)
          elif y == oy + 1 and z == wz:
            # AND gate notches behind levers
            _set(v, x, y, z, TORCH if x % 2 == 0 else BASE)
            _set(v, x, y, z + 1, DUST)
          else:
            _set(v, x, y, z, AIR_B)

  # Iron door
  _set(v, wx + 3, oy + 1, wz + d - 1, DOOR)
  _set(v, wx + 4, oy + 1, wz + d - 1, DOOR)
  _set(v, wx + 3, oy + 2, wz + d - 1, DOOR)
  _set(v, wx + 4, oy + 2, wz + d - 1, DOOR)

  # Floor
  for x in range(wx, wx + w):
    for z in range(wz, wz + d):
      _set(v, x, oy - 1, z, BASE)

  # Cobblestone wall trim on sides
  for y in range(oy, oy + h):
    _set(v, wx - 1, y, cz, WALL)
    _set(v, wx + w, y, cz, WALL)

  # Extend stone room walls
  for x in range(wx - 4, wx + w + 4):
    for y in range(oy, oy + h):
      _set(v, x, y, wz - 3, STONE)
      _set(v, x, y, wz + d + 2, STONE)

  return v


def _generate_bite_fairy_treehouse() -> np.ndarray:
  """Fairy Treehouse — giant jungle tree with octagonal platform and birch stair roof."""
  LOG = _b("jungle_log")
  SLAB = _b("jungle_slab")
  STAIRS = _b("jungle_stairs")
  TRAP = _b("acacia_trapdoor")
  WALL = _b("sandstone_wall")
  BIRCH = _b("birch_stairs")
  LANTERN = _b("soul_lantern")
  LEAVES = _b("jungle_leaves")
  VINE = _b("vine")
  CHAIN = _b("chain")
  BUTTON = _b("acacia_button")
  CRAFT = _b("crafting_table")
  CHEST = _b("chest")
  LADDER = _b("ladder")
  FENCE = _b("acacia_fence")
  GATE = _b("acacia_fence_gate")
  PLANKS = _b("spruce_planks")
  GLASS = _b("glass_pane")
  CAMP = _b("campfire")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz = 14, 16
  oy = 2

  # 2×2 jungle trunk
  for y in range(oy, oy + 14):
    for dx in range(2):
      for dz in range(2):
        _set(v, cx + dx, y, cz + dz, LOG)
        if y > oy + 4:
          _set(v, cx + dx, y, cz + dz - 1, VINE)

  # Ladder in trunk
  for y in range(oy + 1, oy + 8):
    _set(v, cx, y, cz, LADDER)

  # Octagonal platform at y+5
  plat_y = oy + 5
  for x in range(cx - 4, cx + 6):
    for z in range(cz - 4, cz + 6):
      dist = max(abs(x - cx), abs(z - cz))
      if dist <= 4:
        _set(v, x, plat_y, z, SLAB)
      if dist == 4:
        _set(v, x, plat_y + 1, z, TRAP)

  # Sandstone pillars on platform
  for px, pz in ((cx - 3, cz - 3), (cx + 4, cz - 3), (cx - 3, cz + 4), (cx + 4, cz + 4)):
    _set(v, px, plat_y + 1, pz, WALL)

  # Interior
  _set(v, cx + 3, plat_y + 1, cz + 1, CRAFT)
  _set(v, cx + 3, plat_y + 1, cz + 2, CHEST)
  _set(v, cx, plat_y, cz, TRAP)

  # Soul lanterns on corners
  for lx, lz in ((cx - 3, cz), (cx + 5, cz), (cx, cz - 3), (cx, cz + 5)):
    _set(v, lx, plat_y + 2, lz, CHAIN)
    _set(v, lx, plat_y + 1, lz, LANTERN)

  # Birch stair roofs on four sides
  roof_y = plat_y + 2
  for side in range(4):
    for layer in range(2):
      for i in range(-3 + layer, 4 - layer):
        if side == 0:
          _set(v, cx + i, roof_y + layer, cz - 4, BIRCH)
        elif side == 1:
          _set(v, cx + i, roof_y + layer, cz + 5, BIRCH)
        elif side == 2:
          _set(v, cx - 4, roof_y + layer, cz + i, BIRCH)
        else:
          _set(v, cx + 5, roof_y + layer, cz + i, BIRCH)

  # Leaf canopy
  for y in range(oy + 12, oy + 16):
    for x in range(cx - 3, cx + 5):
      for z in range(cz - 3, cz + 5):
        if abs(x - cx - 1) + abs(z - cz - 1) < 5:
          _set(v, x, y, z, LEAVES)

  # Second treehouse + bridge (extension)
  cx2 = cx + 10
  for y in range(oy, oy + 14):
    for dx in range(2):
      for dz in range(2):
        _set(v, cx2 + dx, y, cz + dz, LOG)
  for x in range(cx - 4, cx + 6):
    for z in range(cz - 4, cz + 6):
      if max(abs(x - cx), abs(z - cz)) <= 4:
        pass  # already platform
  for x in range(cx2 - 4, cx2 + 6):
    for z in range(cz - 4, cz + 6):
      dist = max(abs(x - cx2), abs(z - cz))
      if dist <= 4:
        _set(v, x, plat_y, z, PLANKS)
      if dist == 4:
        _set(v, x, plat_y + 1, z, FENCE)

  # Bridge between trees
  for x in range(cx + 5, cx2 - 3):
    _set(v, x, plat_y, cz, GATE)
    _set(v, x, plat_y, cz + 1, CAMP)

  # Enchanting room on extension platform
  _set(v, cx2, plat_y + 1, cz, _b("enchanting_table"))
  for bx in (cx2 - 1, cx2 + 1):
    _set(v, bx, plat_y + 1, cz, _b("bookshelf"))
  _set(v, cx2 + 2, plat_y + 1, cz + 1, _b("anvil"))

  return v


def _generate_bite_flying_school() -> np.ndarray:
  """Superhero Flying School — 17×17 floating island, marquee, elytra launcher pit."""
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  COBBLE = _b("cobblestone")
  END = _b("end_stone_bricks")
  END_WALL = _b("end_stone_brick_wall")
  BIRCH = _b("birch_planks")
  B_SLAB = _b("birch_slab")
  FENCE = _b("birch_fence")
  RED = _b("red_wool")
  WHITE = _b("white_wool")
  OBS = _b("obsidian")
  GLASS = _b("glass_pane")
  WCON = _b("white_concrete")
  PLATE = _b("stone_pressure_plate")
  TNT = _b("tnt")
  LANTERN = _b("lantern")
  WATER = _b("water")
  FERN = _b("large_fern")
  CHEST = _b("chest")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz = 16, 16
  oy = 10
  island = 8  # half-size 17x17

  # Floating island
  for x in range(cx - island, cx + island + 1):
    for z in range(cz - island, cz + island + 1):
      _set(v, x, oy, z, GRASS)
      for d in range(1, 4):
        if oy - d >= 0:
          mat = DIRT if d < 2 else COBBLE
          _set(v, x, oy - d, z, mat)

  # Elytra launcher pit (5×5×4 center)
  for y in range(oy - 4, oy):
    for x in range(cx - 2, cx + 3):
      for z in range(cz - 2, cz + 3):
        _set(v, x, y, z, OBS)
  _set(v, cx, oy - 4, cz, PLATE)
  for ox, oz in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)):
    _set(v, cx + ox, oy - 3, cz + oz, TNT)
  _set(v, cx, oy - 3, cz, WATER)

  # Birch launch deck surface (cover pit with planks around)
  for x in range(cx - island, cx + island + 1):
    for z in range(cz - island, cz + island + 1):
      if not (cx - 2 <= x <= cx + 2 and cz - 2 <= z <= cz + 2):
        _set(v, x, oy + 1, z, BIRCH)

  # Water landing pools (front corners)
  for px, pz in ((cx - 6, cz - 5), (cx + 6, cz - 5)):
    for x in range(px - 1, px + 2):
      for z in range(pz, pz + 2):
        _set(v, x, oy, z, WATER)
        _set(v, x, oy + 1, z, B_SLAB)

  # Marquee pillars
  for px, pz in ((cx - 4, cz - 4), (cx + 4, cz - 4), (cx - 4, cz + 4), (cx + 4, cz + 4)):
    for y in range(oy + 1, oy + 5):
      _set(v, px, y, pz, END_WALL)
      if y == oy + 4:
        _set(v, px, y, pz, FENCE)

  # Striped marquee roof rings
  for ring, color in enumerate((RED, WHITE, RED)):
    y = oy + 5 + ring
    for x in range(cx - 5 + ring, cx + 6 - ring):
      for z in range(cz - 5 + ring, cz + 6 - ring):
        edge = x in (cx - 5 + ring, cx + 5 - ring) or z in (cz - 5 + ring, cz + 5 - ring)
        if edge:
          _set(v, x, y, z, color)

  # Chest in training hall
  _set(v, cx + 3, oy + 2, cz, CHEST)

  # Glass observation deck on top
  obs_y = oy + 8
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      _set(v, x, obs_y, z, WCON)
    for y in range(obs_y + 1, obs_y + 3):
      edge = x in (cx - 2, cx + 2) or z in (cz - 2, cz + 2)
      if edge:
        _set(v, x, y, z, GLASS)

  # Walkway approach
  for x in range(cx - 2, cx + 3):
    for z in range(cz + island + 1, cz + island + 6):
      _set(v, x, oy + 1, z, END)
      _set(v, x, oy + 2, z, LANTERN if x == cx else BIRCH)

  # Ferns on perimeter
  for x in range(cx - island, cx + island + 1, 3):
    for z in (cz - island, cz + island):
      _set(v, x, oy + 1, z, FERN)

  # Lantern railings on deck
  for x in range(cx - 6, cx + 7, 6):
    _set(v, x, oy + 2, cz - 6, LANTERN)

  return v


def _generate_bite_item_destroyer() -> np.ndarray:
  """Item Destroyer — corner utility alcove with hidden dropper-to-cactus disposal."""
  SPRUCE = _b("spruce_planks")
  STONE = _b("stone_bricks")
  GRASS = _b("grass_block")
  CHEST = _b("chest")
  BARREL = _b("barrel")
  HOPPER = _b("hopper")
  DROPPER = _b("dropper")
  COMP = _b("comparator")
  OBS = _b("observer")
  PISTON = _b("sticky_piston")
  CACTUS = _b("cactus")
  SAND = _b("sand")
  LEVER = _b("lever")
  TORCH = _b("torch")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz = 14, 14
  oy = 1
  wl, wd, wh = 6, 5, 5

  # Floor
  for x in range(cx, cx + wl):
    for z in range(cz, cz + wd):
      _set(v, x, oy, z, GRASS)

  # L-shaped corner walls (5 high: stone base 2, spruce top 3)
  for y in range(oy + 1, oy + 1 + wh):
    mat = STONE if y < oy + 3 else SPRUCE
    for x in range(cx, cx + wl):
      _set(v, x, y, cz, mat)
    for z in range(cz, cz + wd):
      _set(v, cx, y, z, mat)

  # Disposal utility room — visible inputs
  _set(v, cx + 2, oy + 3, cz, CHEST)
  _set(v, cx + 3, oy + 3, cz, BARREL)
  _set(v, cx + 2, oy + 2, cz, HOPPER)
  _set(v, cx + 2, oy + 1, cz, LEVER)
  _set(v, cx + 4, oy + 3, cz, TORCH)

  # Hidden redstone chamber behind wall
  bx, bz = cx + 1, cz + 2
  _set(v, bx, oy + 1, bz, DROPPER)
  _set(v, bx - 1, oy + 1, bz, COMP)
  _set(v, bx, oy + 2, bz, OBS)
  _set(v, bx + 1, oy + 2, bz, PISTON)
  _set(v, bx + 2, oy + 1, bz, SAND)
  _set(v, bx + 2, oy + 2, bz, CACTUS)

  return v


def _generate_bite_firefighter_plane() -> np.ndarray:
  """Firefighter Plane — slime flying machine with red-white carpet wings."""
  SLIME = _b("slime_block")
  OBS = _b("observer")
  PISTON = _b("sticky_piston")
  QSTAIRS = _b("quartz_stairs")
  RED = _b("red_carpet")
  WHITE = _b("white_carpet")
  RAIL = _b("rail")
  TORCH = _b("redstone_torch")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 14

  # Engine core (central slime + pistons + observers)
  core = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (2, 1), (-1, 0), (-1, 1)]
  for dx, dz in core:
    _set(v, cx + dx, oy, cz + dz, SLIME)
  _set(v, cx, oy, cz + 2, OBS)
  _set(v, cx + 1, oy, cz + 2, PISTON)
  _set(v, cx - 1, oy, cz + 2, OBS)
  _set(v, cx, oy, cz - 2, PISTON)
  _set(v, cx + 1, oy, cz - 2, OBS)

  # Forward fuselage extension
  for i in range(3, 6):
    _set(v, cx, oy, cz + i, SLIME)
    _set(v, cx + 1, oy, cz + i, SLIME)

  # Wings with red/white checker carpet
  for side in (-1, 1):
    for i in range(-3, 4):
      wx = cx + side * 3
      wz = cz + i
      _set(v, wx, oy, wz, SLIME)
      carpet = RED if (i + side) % 2 == 0 else WHITE
      _set(v, wx, oy + 1, wz, carpet)
      if abs(i) < 3:
        _set(v, wx + side, oy, wz, SLIME)
        _set(v, wx + side, oy + 1, wz, WHITE if carpet == RED else RED)

  # Tail
  _set(v, cx, oy, cz - 3, SLIME)
  _set(v, cx + 1, oy, cz - 3, SLIME)
  _set(v, cx, oy + 1, cz - 3, QSTAIRS)

  # Cockpit (rear)
  _set(v, cx, oy + 1, cz - 1, QSTAIRS)
  _set(v, cx + 1, oy + 1, cz - 1, RAIL)
  _set(v, cx, oy + 2, cz - 1, TORCH)

  return v


def _generate_bite_shooting_gallery() -> np.ndarray:
  """Shooting Gallery — platform, target hills, colorful stalls, observation tower."""
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  LIME = _b("lime_terracotta")
  TARGET = _b("target")
  DUST = _b("redstone_dust")
  REPEATER = _b("redstone_repeater")
  LAMP = _b("redstone_lamp")
  BLACK = _b("blackstone")
  BWALL = _b("blackstone_wall")
  SSLAB = _b("spruce_slab")
  SFENCE = _b("spruce_fence")
  CHEST = _b("chest")
  LANTERN = _b("lantern")
  PINK = _b("pink_terracotta")
  CYAN = _b("cyan_terracotta")
  ORANGE = _b("orange_terracotta")
  QUARTZ = _b("quartz_block")
  DSTAIRS = _b("dark_oak_stairs")
  LEAVES = _b("oak_leaves")
  WATER = _b("water")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  oy = 1

  # Ground plane
  for x in range(4, 28):
    for z in range(4, 28):
      _set(v, x, oy - 1, z, GRASS)

  def _target_hill(tx: int, tz: int) -> None:
    """Steps 1-8: lime terracotta mechanism disguised in grass."""
    for x in range(tx, tx + 5):
      for z in range(tz, tz + 9):
        _set(v, x, oy, z, GRASS if (x == tx or x == tx + 4 or z == tz or z == tz + 8) else LIME)
    _set(v, tx + 2, oy + 1, tz + 1, TARGET)
    for i in range(4):
      _set(v, tx + 2, oy + 1, tz + 2 + i, DUST)
    for x in range(tx + 1, tx + 4):
      _set(v, x, oy + 1, tz + 5, LIME)
    _set(v, tx + 2, oy + 2, tz + 5, REPEATER)
    _set(v, tx + 1, oy + 2, tz + 5, LIME)
    _set(v, tx + 1, oy + 3, tz + 5, LIME)
    _set(v, tx + 1, oy + 4, tz + 5, LAMP)
    _set(v, tx + 2, oy + 3, tz + 5, LAMP)
    _set(v, tx + 3, oy + 3, tz + 5, LAMP)
  # Cover sides with dirt/grass mound
    for x in range(tx, tx + 5):
      for z in range(tz, tz + 9):
        if v[x, oy, z] == LIME:
          _set(v, x, oy + 1, z, DIRT)
          if (x + z) % 2 == 0:
            _set(v, x, oy + 2, z, GRASS)

  for hill in ((8, 10), (14, 12), (20, 10)):
    _target_hill(*hill)

  # Small pond and bushes
  for x in range(16, 19):
    for z in range(18, 21):
      _set(v, x, oy, z, WATER)
  for bx, bz in ((12, 20), (22, 18), (10, 16)):
    for dy in range(1, 3):
      for dx in range(-1, 2):
        for dz in range(-1, 2):
          if abs(dx) + abs(dz) < 2:
            _set(v, bx + dx, oy + dy, bz + dz, LEAVES)

  # Player platform (z=22-25, x=6-24)
  pz0, pz1 = 22, 25
  for x in range(6, 25, 3):
    for z in range(pz0, pz1 + 1):
      for y in range(oy, oy + 4):
        _set(v, x, y, z, BLACK if y < oy + 3 else AIR_B)
      _set(v, x, oy + 3, z, BWALL)
    _set(v, x, oy + 4, pz0, SSLAB)
    _set(v, x, oy + 4, pz1, SSLAB)
    for zx in range(x, min(x + 3, 25)):
      _set(v, zx, oy + 4, pz0, SSLAB)
      _set(v, zx, oy + 4, pz1, SSLAB)
      _set(v, zx, oy + 5, pz0, SFENCE)
      _set(v, zx, oy + 5, pz1, SFENCE)
    _set(v, x + 1, oy + 4, pz0 + 1, CHEST)
    _set(v, x, oy + 3, pz0, LANTERN)

  for x in range(6, 25):
    _set(v, x, oy + 4, pz0, SSLAB)
    _set(v, x, oy + 4, pz1, SSLAB)
    _set(v, x, oy + 5, pz0, SFENCE)
    _set(v, x, oy + 5, pz1, SFENCE)

  # Arcade stalls (background z=6-11)
  stall_colors = (PINK, CYAN, ORANGE, PINK)
  for i, sx in enumerate(range(7, 23, 4)):
    color = stall_colors[i % len(stall_colors)]
    for y in range(oy, oy + 5):
      for z in range(6, 11):
        block = QUARTZ if z == 6 or y == oy + 4 else color
        _set(v, sx, y, z, block)
        _set(v, sx + 1, y, z, block if z != 6 else QUARTZ)
        _set(v, sx + 2, y, z, CYAN if color == PINK else color)
    _set(v, sx + 1, oy + 5, 8, DSTAIRS)
    _set(v, sx + 1, oy + 4, 9, LANTERN)

  # Observation tower
  tx, tz = 24, 7
  for y in range(oy, oy + 11):
    for x in range(tx, tx + 3):
      for z in range(tz, tz + 3):
        block = QUARTZ if (x + z + y) % 2 == 0 else CYAN
        _set(v, x, y, z, block)
  for x in range(tx, tx + 3):
    for z in range(tz, tz + 3):
      _set(v, x, oy + 10, z, DSTAIRS)
  _set(v, tx + 1, oy + 11, tz + 1, SFENCE)
  _set(v, tx + 1, oy + 10, tz + 1, LANTERN)

  return v


# '.' = path, '#' = hay wall (16×16 book layout)
_HALLOWEEN_MAZE = (
  "################",
  "#..............#",
  "#.###.###.###..#",
  "#.#.#.....#.#.#",
  "#.#.#.###.#.#.#",
  "#...#..#..#...#",
  "###.###.#.###.#",
  "#.....#.#.....#",
  "#.###.#.#.###.#",
  "#.#...#.#...#.#",
  "#.#.#####.###.#",
  "#.#.....#.....#",
  "#.#######.####.#",
  "#..............#",
  "################",
)


def _generate_bite_halloween_maze() -> np.ndarray:
  """Halloween Maze — 16×16 hay bale walls, soul lighting, central scarecrow."""
  HAY = _b("hay_block")
  DIRT = _b("dirt")
  GRASS = _b("grass_block")
  MOSSY = _b("mossy_cobblestone")
  FENCE = _b("oak_fence")
  PUMPKIN = _b("carved_pumpkin")
  BUTTON = _b("polished_blackstone_button")
  CAMPFIRE = _b("soul_campfire")
  STORCH = _b("soul_torch")
  OTRAP = _b("oak_trapdoor")
  STRAP = _b("spruce_trapdoor")
  SKULL = _b("skeleton_skull")
  ZHEAD = _b("zombie_head")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 8, 1
  wall_h = 3

  layout = _HALLOWEEN_MAZE
  size = len(layout)

  # Outer grass pad
  for x in range(ox - 1, ox + size + 1):
    for z in range(oz - 1, oz + size + 1):
      _set(v, x, oy - 1, z, GRASS)

  for row, line in enumerate(layout):
    for col, ch in enumerate(line):
      x, z = ox + col, oz + row
      if ch == "#":
        for y in range(oy, oy + wall_h):
          _set(v, x, y, z, HAY)
      else:
        _set(v, x, oy - 1, z, DIRT)
        _set(v, x, oy, z, DIRT)

  # Wall-top decorations
  deco = (OTRAP, SKULL, ZHEAD, OTRAP)
  deco_i = 0
  for row, line in enumerate(layout):
    for col, ch in enumerate(line):
      if ch != "#":
        continue
      x, z = ox + col, oz + row
      if (x + z) % 5 == 0 and row not in (0, size - 1):
        _set(v, x, oy + wall_h, z, deco[deco_i % len(deco)])
        deco_i += 1

  # Soul campfires in path alcoves near walls
  for row in range(1, size - 1):
    for col in range(1, size - 1):
      if layout[row][col] != ".":
        continue
      x, z = ox + col, oz + row
      neighbors_wall = sum(
        layout[row + dr][col + dc] == "#"
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1))
        if 0 <= row + dr < size and 0 <= col + dc < size
      )
      if neighbors_wall >= 2 and (row + col) % 4 == 0:
        _set(v, x, oy, z, CAMPFIRE)

  # Soul torch lamp posts at corners of central courtyard (rows/cols 6-9)
  for lx, lz in ((ox + 6, oz + 6), (ox + 9, oz + 6), (ox + 6, oz + 9), (ox + 9, oz + 9)):
    if layout[lz - oz][lx - ox] == ".":
      _set(v, lx, oy, lz, FENCE)
      _set(v, lx, oy + 1, lz, STRAP)
      _set(v, lx, oy + 2, lz, STORCH)

  # Central scarecrow (center of 16×16 → offset 7,7 from maze origin → world 15,15)
  cx, cz = ox + 7, oz + 7
  for dx in range(-2, 3):
    for dz in range(-2, 3):
      _set(v, cx + dx, oy - 1, cz + dz, DIRT)
      _set(v, cx + dx, oy, cz + dz, DIRT)
  _set(v, cx, oy, cz, MOSSY)
  _set(v, cx, oy + 1, cz, FENCE)
  _set(v, cx, oy + 2, cz, PUMPKIN)
  _set(v, cx + 1, oy + 2, cz, BUTTON)

  return v


def _generate_bite_train_station() -> np.ndarray:
  """Train Station — 14×9 waiting hall, twin platforms, tracks, bridge, lighting arches."""
  SBRICK = _b("stone_bricks")
  SSLAB = _b("stone_brick_slab")
  ANDESITE = _b("andesite")
  PAND = _b("polished_andesite")
  QUARTZ = _b("smooth_quartz")
  QSTAIRS = _b("smooth_quartz_stairs")
  JPLANK = _b("jungle_planks")
  JSLAB = _b("jungle_slab")
  SPRUCE = _b("spruce_planks")
  SSTAIRS = _b("spruce_stairs")
  SSLAB2 = _b("spruce_slab")
  DIORITE = _b("diorite")
  YGLASS = _b("yellow_stained_glass_pane")
  ITRAP = _b("iron_trapdoor")
  IBARS = _b("iron_bars")
  BUTTON = _b("stone_button")
  LANTERN = _b("lantern")
  DOOR = _b("dark_oak_door")
  DTRAP = _b("dark_oak_trapdoor")
  SMOOTH = _b("smooth_stone_slab")
  RAIL = _b("rail")
  POWER = _b("powered_rail")
  ACTIV = _b("activator_rail")
  RTORCH = _b("redstone_torch")
  BELL = _b("bell")
  ANVIL = _b("anvil")
  BANNER = _b("orange_banner")
  CHISEL = _b("chiseled_stone_bricks")
  CWALL = _b("cobblestone_wall")
  SBWALL = _b("stone_brick_wall")
  JTRAP = _b("jungle_trapdoor")
  STRAP = _b("spruce_trapdoor")
  ROSE = _b("rose_bush")
  DIRT = _b("dirt")
  SBSTAIR = _b("stone_brick_stairs")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 9, 2
  length, width, wall_h = 14, 9, 5

  # Ground
  for x in range(ox - 2, ox + length + 8):
    for z in range(oz - 2, oz + width + 14):
      _set(v, x, oy - 1, z, GRASS)

  # Step 1 — foundation (14×9)
  for x in range(ox, ox + length):
    for z in range(oz, oz + width):
      edge = x in (ox, ox + length - 1) or z in (oz, oz + width - 1)
      _set(v, x, oy - 1, z, PAND if edge else ANDESITE)
      _set(v, x, oy, z, JPLANK)

  # Step 2-5 — walls with spruce pillars
  pillar_x = (ox, ox + length // 2, ox + length - 1)
  for y in range(oy + 1, oy + wall_h):
    for x in range(ox, ox + length):
      for z in range(oz, oz + width):
        edge_x = x in (ox, ox + length - 1)
        edge_z = z in (oz, oz + width - 1)
        pillar = x in pillar_x and edge_z
        if pillar:
          _set(v, x, y, z, SPRUCE)
        elif edge_x or edge_z:
          if y == oy + 2 and edge_x and z not in (oz, oz + width - 1) and (z - oz) % 3 == 1:
            _set(v, x, y, z, YGLASS)
          elif edge_z == oz and x in (ox + 5, ox + 6, ox + 7, ox + 8) and y < oy + 4:
            _set(v, x, y, z, AIR_B)  # entrance
          else:
            _set(v, x, y, z, QUARTZ if y < oy + 4 else DIORITE)
        else:
          _set(v, x, y, z, AIR_B)

  # Entrance doors and trapdoors
  for x in (ox + 5, ox + 6, ox + 7, ox + 8):
    _set(v, x, oy + 1, oz, DOOR)
    _set(v, x, oy + 2, oz, DOOR)
    _set(v, x, oy + 3, oz, DTRAP)

  # Ticket barrier (center of entrance wall inside)
  tb_x = ox + 6
  for z in (oz + 1, oz + 2):
    _set(v, tb_x, oy + 1, z, QUARTZ)
    _set(v, tb_x + 1, oy + 1, z, DIORITE)
    _set(v, tb_x, oy + 2, z, ITRAP)
    _set(v, tb_x + 1, oy + 2, z, IBARS)
    _set(v, tb_x + 1, oy + 2, z + 1, BUTTON)

  # Interior benches and lanterns
  for bx in (ox + 2, ox + length - 3):
    for bz in (oz + 2, oz + width - 3):
      _set(v, bx, oy + 1, bz, SSTAIRS)
      _set(v, bx + 1, oy + 1, bz, SSTAIRS)
  for lx in (ox + 3, ox + length - 4):
    _set(v, lx, oy + 4, oz + width // 2, LANTERN)

  # Step 6 — jungle roof
  roof_y = oy + wall_h
  for x in range(ox - 1, ox + length + 1):
    _set(v, x, roof_y, oz - 1, JPLANK)
    _set(v, x, roof_y, oz + width, JPLANK)
  for x in range(ox, ox + length):
    for z in range(oz, oz + width):
      _set(v, x, roof_y, z, JSLAB)
  for i, bx in enumerate(range(ox + 2, ox + length - 1, 3)):
    _set(v, bx, roof_y + 1, oz - 1, BANNER)

  # Step 7 — exterior column lanterns
  for x in pillar_x:
    _set(v, x, oy + wall_h, oz, SBSTAIR)
    _set(v, x, oy + wall_h - 1, oz - 1, IBARS)
    _set(v, x, oy + wall_h - 2, oz - 1, LANTERN)

  # Steps 8-9 — twin platforms and tracks (south of building)
  pz0 = oz + width
  track_len = length + 2
  for side, pz in enumerate((pz0, pz0 + 5)):
    for x in range(ox - 1, ox + length + 1):
      _set(v, x, oy - 1, pz, SBRICK)
      _set(v, x, oy, pz, SSLAB)
      _set(v, x, oy - 1, pz + 1, ANDESITE)
      if side == 0:
        _set(v, x, oy + 1, pz, ANVIL if x % 4 == 0 else AIR_B)

  # Track bed: 2-wide smooth stone between platforms
  tz = pz0 + 2
  for x in range(ox - 1, ox + length + 1):
    _set(v, x, oy, tz, SMOOTH)
    _set(v, x, oy, tz + 1, SMOOTH)
    _set(v, x, oy, pz0 + 1, RAIL)
    _set(v, x, oy, pz0 + 3, RAIL)

  # Powered rail + torch at west end, activator rail + bell at east end
  _set(v, ox - 1, oy, pz0 + 1, POWER)
  _set(v, ox - 1, oy, tz, RTORCH)
  _set(v, ox + length, oy, pz0 + 3, ACTIV)
  _set(v, ox + length, oy + 1, pz0 + 3, BELL)

  # Step 10 / extras — lighting arches over tracks
  for ax in (ox + 2, ox + length - 3):
    for y in range(oy, oy + 4):
      _set(v, ax, y, tz, CHISEL if y == oy else SBWALL if y < oy + 3 else CWALL)
    _set(v, ax, oy + 4, tz, LANTERN)
    _set(v, ax, oy + 4, tz + 1, LANTERN)

  # Connecting bridge between platforms
  bx = ox + length // 2
  for z in range(pz0, pz0 + 6):
    _set(v, bx, oy + 1, z, SSLAB2 if z % 2 == 0 else SSTAIRS)
    _set(v, bx - 1, oy + 2, z, JTRAP)
    _set(v, bx + 1, oy + 2, z, JTRAP)

  # Platform flowerpot and extra bench
  _set(v, ox + 3, oy, pz0, DIRT)
  for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
    _set(v, ox + 3 + dx, oy, pz0 + dz, STRAP)
  _set(v, ox + 3, oy + 1, pz0, ROSE)
  _set(v, ox + length - 4, oy + 1, pz0, SSTAIRS)

  return v


def _generate_bite_cart_collector() -> np.ndarray:
  """Cart Collector — cactus breaks minecarts, hoppers route items to chest."""
  HOPPER = _b("hopper")
  CHEST = _b("chest")
  RAIL = _b("rail")
  CACTUS = _b("cactus")
  SAND = _b("sand")
  STONE = _b("stone")
  GRASS = _b("grass_block")
  SLAB = _b("smooth_stone_slab")
  SSTAIR = _b("stone_stairs")
  STRAP = _b("spruce_trapdoor")
  PISTON = _b("sticky_piston")
  RBLOCK = _b("redstone_block")
  OBS = _b("observer")
  DUST = _b("redstone_dust")
  LANTERN = _b("lantern")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 14, 2
  length, depth = 9, 4

  # Ground pad
  for x in range(ox - 1, ox + length + 1):
    for z in range(oz - 1, oz + depth + 1):
      _set(v, x, oy - 1, z, GRASS)

  # Bottom layer — chest + hopper line (spouts toward chest at ox)
  _set(v, ox, oy, oz + 1, CHEST)
  for i in range(1, 5):
    _set(v, ox + i, oy, oz + 1, HOPPER)

  # Middle platform (stone border, grass interior, hopper chute)
  for x in range(ox, ox + length):
    for z in range(oz, oz + depth):
      edge = x in (ox, ox + length - 1) or z in (oz, oz + depth - 1)
      hole = x in range(ox + 1, ox + 5) and z == oz + 1
      if hole:
        _set(v, x, oy, z, AIR_B)
        _set(v, x, oy + 1, z, AIR_B)
      else:
        _set(v, x, oy + 1, z, STONE if edge else GRASS)

  # Rail approach along platform center
  for x in range(ox, ox + length - 1):
    _set(v, x, oy + 2, oz + 1, RAIL)
  _set(v, ox + length - 2, oy + 2, oz + 2, RAIL)
  _set(v, ox + length - 1, oy + 2, oz + 2, RAIL)

  # Cactus breaker at rail end
  cx, cz = ox + length - 1, oz + 2
  _set(v, cx, oy + 1, cz, SAND)
  _set(v, cx, oy + 2, cz, CACTUS)
  for dx, dz in ((-1, 0), (0, -1), (0, 1)):
    _set(v, cx + dx, oy + 2, cz + dz, STONE)
  _set(v, cx, oy + 3, cz, SLAB)
  _set(v, cx - 1, oy + 3, cz, SSTAIR)
  _set(v, cx, oy + 3, cz - 1, STRAP)
  _set(v, cx, oy + 3, cz + 1, STRAP)

  # Redstone housing beside mechanism
  _set(v, cx - 2, oy + 1, cz, PISTON)
  _set(v, cx - 2, oy + 2, cz, RBLOCK)
  _set(v, cx - 2, oy + 2, cz + 1, OBS)
  _set(v, cx - 3, oy + 2, cz, DUST)
  _set(v, cx - 3, oy + 2, cz + 1, LANTERN)

  return v


def _generate_bite_bouncy_castle() -> np.ndarray:
  """Bouncy Castle — 14×14 slime courtyard, red sandstone walls, corner tower (steps 1–10)."""
  COBBLE = _b("cobblestone")
  DIRT = _b("dirt")
  SLIME = _b("slime_block")
  SMOOTH = _b("smooth_red_sandstone")
  RSAND = _b("red_sandstone")
  SSTAIRS = _b("smooth_red_sandstone_stairs")
  RSLAB = _b("red_sandstone_slab")
  RSWALL = _b("red_sandstone_wall")
  LADDER = _b("ladder")
  YCARPET = _b("yellow_carpet")
  BCARPET = _b("light_blue_carpet")
  SLANTERN = _b("soul_lantern")
  OBANNER = _b("orange_banner")
  BBANNER = _b("light_blue_banner")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 9, 2
  size = 14
  wall_h = 6

  # Step 1 — 14×14 foundation: cobblestone outline, dirt and slime interior
  for x in range(ox, ox + size):
    for z in range(oz, oz + size):
      edge = x in (ox, ox + size - 1) or z in (oz, oz + size - 1)
      if edge:
        _set(v, x, oy, z, COBBLE)
      else:
        _set(v, x, oy, z, SLIME if (x + z) % 2 == 0 else DIRT)

  # Bouncy floor — slime with checkered carpet (book step 10)
  for x in range(ox + 1, ox + size - 1):
    for z in range(oz + 1, oz + size - 1):
      _set(v, x, oy + 1, z, SLIME)
      _set(v, x, oy + 2, z, YCARPET if (x + z) % 2 == 0 else BCARPET)

  # Steps 2–5 — sandstone and slime walls with entrance gap
  for y in range(oy + 1, oy + 1 + wall_h):
    for x in range(ox, ox + size):
      for z in range(oz, oz + size):
        edge = x in (ox, ox + size - 1) or z in (oz, oz + size - 1)
        if not edge:
          continue
        if z == oz and x in (ox + 6, ox + 7) and y < oy + 4:
          continue
        if y % 2 == 1 and (x in (ox + 1, ox + size - 2) or z in (oz + 1, oz + size - 2)):
          _set(v, x, y, z, SLIME)
        else:
          _set(v, x, y, z, SMOOTH if y % 2 == 0 else RSAND)

  # Step 4 — entrance archway (upside-down smooth red sandstone stairs)
  for x in (ox + 5, ox + 6, ox + 7, ox + 8):
    _set(v, x, oy + 4, oz, SSTAIRS)

  # Steps 6–7 — rampart walkway and upside-down stair lip
  wy = oy + 1 + wall_h
  for x in range(ox, ox + size):
    for z in range(oz, oz + size):
      if x in (ox, ox + size - 1) or z in (oz, oz + size - 1):
        _set(v, x, wy, z, RSLAB)
        _set(v, x, wy + 1, z, SSTAIRS if (x + z) % 2 == 0 else RSWALL)

  # Steps 8–9 — back corner tower (4×4) with ladder and slab platform
  tx, tz = ox + 10, oz + 10
  tower_h = 9
  for y in range(oy + 1, oy + 1 + tower_h):
    for x in range(tx, tx + 4):
      for z in range(tz, tz + 4):
        edge = x in (tx, tx + 3) or z in (tz, tz + 3)
        if edge:
          _set(v, x, y, z, SMOOTH if y % 2 == 0 else SLIME)
  for y in range(oy + 2, oy + tower_h):
    _set(v, tx + 1, y, tz + 1, LADDER)
  for x in range(tx, tx + 4):
    for z in range(tz, tz + 4):
      _set(v, x, oy + tower_h, z, RSLAB)

  # Step 10 — soul lanterns on corners, banners at entrance
  for lx, lz in ((ox, oz), (ox + size - 1, oz), (ox, oz + size - 1), (ox + size - 1, oz + size - 1)):
    _set(v, lx, wy + 2, lz, SLANTERN)
  _set(v, ox + 6, oy + 3, oz, OBANNER)
  _set(v, ox + 7, oy + 3, oz, BBANNER)

  return v


def _generate_bite_medieval_windmill() -> np.ndarray:
  """Medieval Windmill — 5×5 stone tower, spruce roof, four wool sail vanes (steps 1–10)."""
  GRASS = _b("grass_block")
  WATER = _b("water")
  COBBLE = _b("cobblestone")
  SBRICK = _b("stone_bricks")
  CHISEL = _b("chiseled_stone_bricks")
  PDIORITE = _b("polished_diorite")
  DIORITE = _b("diorite")
  DSTAIR = _b("diorite_stairs")
  CSLAB = _b("cobblestone_slab")
  CWALL = _b("cobblestone_wall")
  SPRUCE = _b("spruce_planks")
  SSTAIRS = _b("spruce_stairs")
  SSLAB = _b("spruce_slab")
  FENCE = _b("spruce_fence")
  FGATE = _b("spruce_fence_gate")
  SDOOR = _b("spruce_door")
  SBUTTON = _b("spruce_button")
  STBUTTON = _b("stone_button")
  WOOL = _b("white_wool")
  WHEAT = _b("wheat")
  HAY = _b("hay_block")
  LANTERN = _b("lantern")
  SHULKER = _b("yellow_shulker_box")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 12, 2
  fx, fz = ox + 1, oz + 1  # 5×5 tower origin

  # Step 1 — 8×7 grass base, water corners, 5×5 cobblestone foundation
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 7):
      _set(v, x, oy - 1, z, GRASS)
  for cx, cz in ((ox, oz), (ox + 7, oz), (ox, oz + 6), (ox + 7, oz + 6)):
    _set(v, cx, oy, cz, WATER)
  for x in range(fx, fx + 5):
    for z in range(fz, fz + 5):
      _set(v, x, oy, z, COBBLE)

  stones = (COBBLE, SBRICK, CHISEL, PDIORITE)

  # Step 2 — 4-high hollow mixed stone walls, fence gate window on back
  for y in range(oy + 1, oy + 5):
    for x in range(fx, fx + 5):
      for z in range(fz, fz + 5):
        edge = x in (fx, fx + 4) or z in (fz, fz + 4)
        if not edge:
          continue
        if z == fz and x == fx + 2 and y in (oy + 1, oy + 2):
          _set(v, x, y, z, SDOOR)
        elif z == fz + 4 and x == fx + 2 and y == oy + 2:
          _set(v, x, y, z, FGATE)
        else:
          _set(v, x, y, z, stones[(x + y + z) % 4])

  # Step 3 — entrance awning (spruce stairs, fences, slabs, cobblestone wall)
  ax = fx + 2
  for dx in (-1, 0, 1):
    _set(v, ax + dx, oy + 4, fz - 1, SSTAIRS)
    _set(v, ax + dx, oy + 3, fz - 1, FENCE)
  _set(v, ax, oy + 2, fz - 1, CWALL)
  _set(v, fx + 4, oy + 3, fz + 2, SSLAB)
  _set(v, fx + 4, oy + 2, fz + 2, FENCE)
  _set(v, fx + 4, oy + 1, fz + 2, CWALL)

  # Step 4 — cobblestone diamond taper, spruce + diorite stairs layer
  ty = oy + 5
  for x in range(fx + 1, fx + 4):
    for z in range(fz + 1, fz + 4):
      if (x + z) % 2 == 0:
        _set(v, x, ty, z, COBBLE)
  ty += 1
  for x in range(fx, fx + 5):
    for z in range(fz, fz + 5):
      if x in (fx, fx + 4) or z in (fz, fz + 4):
        _set(v, x, ty, z, SPRUCE if (x + z) % 2 == 0 else DSTAIR)

  # Step 5 — three more spruce/diorite layers with fence gate windows
  for layer in range(3):
    ty += 1
    for x in range(fx, fx + 5):
      for z in range(fz, fz + 5):
        if x in (fx, fx + 4) or z in (fz, fz + 4):
          if layer == 2 and z == fz + 2 and x in (fx + 1, fx + 2, fx + 3):
            _set(v, x, ty, z, FGATE)
          else:
            mat = (SPRUCE, DIORITE, PDIORITE)[(x + z + layer) % 3]
            _set(v, x, ty, z, mat)

  # Two more diorite/spruce layers + three spruce cap blocks
  for layer in range(2):
    ty += 1
    for x in range(fx, fx + 5):
      for z in range(fz, fz + 5):
        if x in (fx, fx + 4) or z in (fz, fz + 4):
          _set(v, x, ty, z, DIORITE if layer == 0 else SPRUCE)
  ty += 1
  for x in (fx + 1, fx + 2, fx + 3):
    _set(v, x, ty, fz + 2, SPRUCE)

  # Step 6 — cobblestone slab ridge roof with spruce stair slopes
  roof_y = ty + 1
  for x in range(fx + 1, fx + 4):
    _set(v, x, roof_y, fz + 2, CSLAB)
  for i in range(2):
    for x in range(fx, fx + 5):
      _set(v, x, roof_y + i, fz + 1 - i, SSTAIRS)
      _set(v, x, roof_y + i, fz + 3 + i, SSTAIRS)

  # Step 7 — spruce beam hub extending from front
  beam_y = roof_y - 1
  hub_x, hub_z = fx + 2, fz - 1
  for i in range(1, 5):
    _set(v, hub_x, beam_y, hub_z - i, SPRUCE)
  hub_z -= 4
  for dx, dz in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
    _set(v, hub_x + dx, beam_y, hub_z + dz, SPRUCE)

  def _vane(dx: int, dz: int) -> None:
    for i in range(1, 4):
      block = SPRUCE if i < 3 else FENCE
      _set(v, hub_x + dx * i, beam_y, hub_z + dz * i, block)
    for i in range(1, 3):
      _set(v, hub_x + dx * 2, beam_y + i, hub_z + dz * 2, WOOL)
      _set(v, hub_x + dx * 3, beam_y, hub_z + dz * 3, WOOL)
    _set(v, hub_x + dx * 2, beam_y, hub_z + dz * 2, SBUTTON)

  # Steps 8–9 — four wool sail vanes
  for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    _vane(dx, dz)

  # Step 10 — buttons, hanging roof fences, wheat farm props
  for x in range(fx, fx + 5, 4):
    for z in range(fz, fz + 5, 4):
      _set(v, x, roof_y + 2, z, FENCE)
      _set(v, x, roof_y + 1, z, STBUTTON)
  for x in range(ox, ox + 8):
    for z in range(oz, oz + 7):
      if not (fx <= x < fx + 5 and fz <= z < fz + 5):
        if (x + z) % 3 == 0:
          _set(v, x, oy, z, WHEAT)
  _set(v, ox + 3, oy, oz + 3, HAY)
  _set(v, ox + 4, oy + 1, oz + 3, LANTERN)
  _set(v, ox + 5, oy, oz + 4, SHULKER)

  return v


def _generate_bite_portal_toggle() -> np.ndarray:
  """Portal Toggle — obsidian portal frame with dispenser on/off redstone (book specs)."""
  OBS = _b("obsidian")
  CRY = _b("crying_obsidian")
  BLACK = _b("blackstone")
  BSTAIR = _b("blackstone_stairs")
  DISP = _b("dispenser")
  DUST = _b("redstone_dust")
  REPEATER = _b("redstone_repeater")
  PISTON = _b("sticky_piston")
  BUTTON = _b("stone_button")
  GRASS = _b("grass_block")
  PORTAL = _b("nether_portal")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 14, 2
  width, depth, height = 9, 3, 10

  # 9×3 grass foundation
  for x in range(ox, ox + width):
    for z in range(oz, oz + depth):
      _set(v, x, oy - 1, z, GRASS)
      _set(v, x, oy, z, GRASS)

  # Portal frame — 4×5 interior (6×7 outer obsidian), centered on base
  px = ox + 2
  pz = oz
  for y in range(oy + 1, oy + 6):
    for x in range(px, px + 4):
      _set(v, x, y, pz, OBS if (x + y) % 2 == 0 else CRY)
    _set(v, px - 1, y, pz, OBS)
    _set(v, px + 4, y, pz, CRY)
  for x in range(px - 1, px + 5):
    _set(v, x, oy + 6, pz, OBS)
    _set(v, x, oy, pz, OBS if x % 2 == 0 else BLACK)
  # Portal interior (4×5)
  for y in range(oy + 1, oy + 6):
    for x in range(px, px + 4):
      _set(v, x, y, pz + 1, PORTAL)

  # Blackstone decorative arch corners
  for y in range(oy + 4, oy + 7):
    _set(v, px - 1, y, pz, BSTAIR)
    _set(v, px + 4, y, pz, BSTAIR)
  for x in range(px - 1, px + 5):
    _set(v, x, oy + 7, pz, BLACK)

  # Toggle circuit behind frame (9×3 footprint, depth oz+1..oz+2)
  _set(v, ox + 1, oy + 1, oz + 2, DISP)  # flint and steel dispenser
  _set(v, ox + 7, oy + 1, oz + 2, DISP)  # water bucket dispenser
  _set(v, ox + 1, oy + 2, oz + 2, DUST)
  _set(v, ox + 2, oy + 2, oz + 2, PISTON)
  _set(v, ox + 6, oy + 2, oz + 2, REPEATER)
  _set(v, ox + 7, oy + 2, oz + 2, DUST)
  for x in range(ox + 3, ox + 6):
    _set(v, x, oy + 2, oz + 2, DUST)
  _set(v, ox + 4, oy + 1, oz, BUTTON)

  return v


def _amp_in_bowl(x: int, z: int, cx: int, cz: int, r: int) -> bool:
  return (x - cx) ** 2 + (z - cz) ** 2 <= r * r


def _generate_bite_outdoor_amphitheatre() -> np.ndarray:
  """Outdoor Amphitheatre — 16×16 semicircle, tiered seating, quartz colonnade (steps 1–11)."""
  SQUARTZ = _b("smooth_quartz")
  GRASS = _b("grass_block")
  YCONC = _b("yellow_concrete")
  BCONC = _b("blue_concrete")
  WGLAZE = _b("white_glazed_terracotta")
  QBLOCK = _b("quartz_block")
  CHISEL = _b("chiseled_quartz_block")
  CSSLAB = _b("cut_sandstone_slab")
  SSSTAIR = _b("smooth_sandstone_stairs")
  QBRICK = _b("quartz_bricks")
  QPILLAR = _b("quartz_pillar")
  RSWALL = _b("red_sandstone_wall")
  SQSLAB = _b("smooth_quartz_slab")
  SQSTAIR = _b("smooth_quartz_stairs")
  BTRAP = _b("birch_trapdoor")
  PEONY = _b("peony")
  ASTAIR = _b("acacia_stairs")
  ATRAP = _b("acacia_trapdoor")
  ABUTTON = _b("acacia_button")
  FENCE = _b("spruce_fence")
  LEAVES = _b("jungle_leaves")
  CAMPFIRE = _b("campfire")
  LANTERN = _b("lantern")
  VINE = _b("vine")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 8, 2
  size = 16
  cx, cz = ox + 8, oz + 6
  r = 7

  # Step 1 — 16×16 circular footprint: smooth quartz rim, grass interior
  for x in range(ox, ox + size):
    for z in range(oz, oz + size):
      if not _amp_in_bowl(x, z, cx, cz, r):
        continue
      dist_sq = (x - cx) ** 2 + (z - cz) ** 2
      edge = dist_sq >= (r - 1) ** 2
      _set(v, x, oy - 1, z, SQUARTZ if edge else GRASS)
      _set(v, x, oy, z, GRASS)

  # Stage mosaic — 7×7 cross pattern at front center (steps 1, 4)
  sx, sz = cx - 3, cz + 1
  mosaic = (
    (0, 0, YCONC), (1, 0, BCONC), (2, 0, WGLAZE), (3, 0, QBLOCK), (4, 0, WGLAZE), (5, 0, BCONC), (6, 0, YCONC),
    (0, 1, BCONC), (1, 1, YCONC), (2, 1, QBLOCK), (3, 1, CHISEL), (4, 1, QBLOCK), (5, 1, YCONC), (6, 1, BCONC),
    (0, 2, WGLAZE), (1, 2, QBLOCK), (2, 2, YCONC), (3, 2, BCONC), (4, 2, YCONC), (5, 2, QBLOCK), (6, 2, WGLAZE),
    (0, 3, QBLOCK), (1, 3, CHISEL), (2, 3, BCONC), (3, 3, YCONC), (4, 3, BCONC), (5, 3, CHISEL), (6, 3, QBLOCK),
    (0, 4, WGLAZE), (1, 4, QBLOCK), (2, 4, YCONC), (3, 4, BCONC), (4, 4, YCONC), (5, 4, QBLOCK), (6, 4, WGLAZE),
    (0, 5, BCONC), (1, 5, YCONC), (2, 5, QBLOCK), (3, 5, CHISEL), (4, 5, QBLOCK), (5, 5, YCONC), (6, 5, BCONC),
    (0, 6, YCONC), (1, 6, BCONC), (2, 6, WGLAZE), (3, 6, QBLOCK), (4, 6, WGLAZE), (5, 6, BCONC), (6, 6, YCONC),
  )
  for dx, dz, block in mosaic:
    _set(v, sx + dx, oy, sz + dz, block)

  # Steps 2–3 — two tiers of cut sandstone slab seating with stair benches
  for tier, lift in enumerate((1, 2)):
    seat_r = r - 2 - tier
    for x in range(ox, ox + size):
      for z in range(oz, oz + size):
        d = (x - cx) ** 2 + (z - cz) ** 2
        if seat_r ** 2 - seat_r <= d <= seat_r ** 2 + seat_r and z >= cz - 1:
          _set(v, x, oy + lift, z, CSSLAB)
          if tier == 1 and (x + z) % 3 == 0:
            _set(v, x, oy + lift + 1, z, SSSTAIR)

  # Raised backing — quartz bricks and horizontal pillars (step 2)
  for x in range(cx - 5, cx + 6):
    for z in range(cz - 4, cz):
      if _amp_in_bowl(x, z, cx, cz, r - 1):
        _set(v, x, oy + 1, z, QBRICK if (x + z) % 2 == 0 else QPILLAR)

  # Steps 5–8 — quartz pillar colonnade (21 pillars around back curve)
  pillar_xs = [cx - 6 + i for i in range(0, 13, 2)] + [cx + 7, cx + 5]
  for i, px in enumerate(pillar_xs[:21]):
    pz = cz - 5 + (i % 3)
    for y in range(oy + 1, oy + 6):
      _set(v, px, y, pz, QPILLAR)
    _set(v, px, oy + 6, pz, CHISEL)
    _set(v, px, oy + 6, pz + 1, ABUTTON)
    _set(v, px, oy + 2, pz - 1, VINE)
    if i % 2 == 0:
      _set(v, px, oy + 3, pz + 1, RSWALL)

  # Step 6 — peony planters between pillars
  for i, px in enumerate(pillar_xs[1::4]):
    _set(v, px, oy + 1, cz - 3, GRASS)
    for dx, dz in ((-1, 0), (1, 0)):
      _set(v, px + dx, oy + 1, cz - 3 + dz, BTRAP)
    _set(v, px, oy + 2, cz - 3, PEONY)
    _set(v, px, oy + 3, cz - 3, PEONY)

  # Step 7 — four acacia throne chairs on top tier
  for px in (cx - 4, cx - 1, cx + 2, cx + 5):
    _set(v, px, oy + 3, cz - 1, ASTAIR)
    _set(v, px, oy + 4, cz - 1, ATRAP)
    _set(v, px - 1, oy + 4, cz - 1, ATRAP)

  # Step 9 — connect back pillars with smooth quartz slabs and stairs
  for px in pillar_xs[:12]:
    _set(v, px, oy + 5, cz - 5, SQSLAB)
    _set(v, px, oy + 5, cz - 4, SQSTAIR)

  # Steps 10–11 — spruce fence trellis with jungle leaves and lanterns
  for px in range(cx - 5, cx + 6, 2):
    for pz in (cz - 4, cz - 2):
      _set(v, px, oy + 6, pz, FENCE)
      _set(v, px + 1, oy + 7, pz, FENCE)
      _set(v, px, oy + 7, pz, LEAVES)
      if px % 4 == 0:
        _set(v, px, oy + 6, pz + 1, LANTERN)

  # Campfires around stage edge (step 11)
  for px in (cx - 4, cx, cx + 4):
    _set(v, px, oy + 1, sz + 7, CAMPFIRE)

  return v


def _generate_bite_hidden_bunker() -> np.ndarray:
  """Hidden Bunker — 18×18 underground base, secret entrance, furnished interior."""
  COBBLE = _b("cobblestone")
  STONE = _b("stone")
  WCONC = _b("white_concrete")
  BPLANK = _b("birch_planks")
  BSTAIR = _b("birch_stairs")
  BSLAB = _b("birch_slab")
  BTRAP = _b("birch_trapdoor")
  BDOOR = _b("birch_door")
  SQSTAIR = _b("smooth_quartz_stairs")
  GLASS = _b("glass_pane")
  LADDER = _b("ladder")
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  LIME = _b("lime_terracotta")
  DUST = _b("redstone_dust")
  REPEATER = _b("redstone_repeater")
  RTORCH = _b("redstone_torch")
  PISTON = _b("sticky_piston")
  LEVER = _b("lever")
  ASTAIR = _b("acacia_stairs")
  OCARPET = _b("orange_carpet")
  BCONC = _b("black_concrete")
  GLOW = _b("glowstone")
  JPLANK = _b("jungle_planks")
  JSTAIR = _b("jungle_stairs")
  JTRAP = _b("jungle_trapdoor")
  JSLAB = _b("jungle_slab")
  SQUARTZ = _b("smooth_quartz")
  CAULDRON = _b("cauldron")
  IRON = _b("iron_block")
  IDOOR = _b("iron_door")
  SBUTTON = _b("stone_button")
  SMOKER = _b("smoker")
  CHEST = _b("chest")
  FURNACE = _b("furnace")
  RAIL = _b("rail")
  CRAFT = _b("crafting_table")
  BREW = _b("brewing_stand")
  BED = _b("white_bed")
  BANNER = _b("orange_banner")
  GCARPET = _b("gray_carpet")
  BPLATE = _b("birch_pressure_plate")
  FENCE = _b("spruce_fence")
  BOOKS = _b("bookshelf")
  BARREL = _b("barrel")
  POT = _b("flower_pot")
  SAPLING = _b("oak_sapling")
  RLAMP = _b("redstone_lamp")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 7, 7, 1
  size, inner_h = 18, 7
  lx, lz = ox + 1, oz + 1  # 2×2 ladder corner

  # Surrounding dirt shell (subterranean)
  for x in range(ox - 1, ox + size + 1):
    for z in range(oz - 1, oz + size + 1):
      for y in range(oy - 1, oy + inner_h + 2):
        outside = x < ox or x >= ox + size or z < oz or z >= oz + size
        if outside and y <= oy + inner_h + 1:
          _set(v, x, y, z, DIRT)

  # Step 1 — foundation: stone/cobble border, birch plank floor, ladder hole
  for x in range(ox, ox + size):
    for z in range(oz, oz + size):
      edge = x in (ox, ox + size - 1) or z in (oz, oz + size - 1)
      hole = lx <= x < lx + 2 and lz <= z < lz + 2
      if hole:
        _set(v, x, oy, z, AIR_B)
      else:
        _set(v, x, oy, z, STONE if edge else BPLANK)
        if edge:
          _set(v, x, oy - 1, z, COBBLE)

  # Steps 2–3 — walls: cobblestone base row, white concrete above (7 blocks tall)
  for y in range(oy + 1, oy + 1 + inner_h):
    for x in range(ox, ox + size):
      for z in range(oz, oz + size):
        edge = x in (ox, ox + size - 1) or z in (oz, oz + size - 1)
        if not edge:
          continue
        if y == oy + 1:
          _set(v, x, y, z, COBBLE)
        else:
          _set(v, x, y, z, WCONC)

  # Interior room dividers with glass panes
  div_x, div_z = ox + 9, oz + 9
  for y in range(oy + 1, oy + 5):
    for z in range(oz + 2, oz + size - 2):
      _set(v, div_x, y, z, WCONC if y < oy + 4 else GLASS)
    for x in range(ox + 2, ox + size - 2):
      _set(v, x, y, div_z, WCONC if y < oy + 4 else GLASS)

  # Raised birch mezzanine (step 2) in bedroom wing
  for x in range(div_x + 1, ox + size - 2):
    for z in range(oz + 2, div_z):
      _set(v, x, oy + 2, z, BPLANK)
      if x == div_x + 2:
        _set(v, x, oy + 1, z, BSTAIR)

  # Step 4 — ceiling with recessed smooth quartz stairs
  cy = oy + 1 + inner_h
  for x in range(ox, ox + size):
    for z in range(oz, oz + size):
      if lx <= x < lx + 2 and lz <= z < lz + 2:
        _set(v, x, cy, z, AIR_B)
      elif (x + z) % 4 == 0:
        _set(v, x, cy, z, SQSTAIR)
      else:
        _set(v, x, cy, z, WCONC)
      if (x + z) % 5 == 0:
        _set(v, x, cy - 1, z, GLOW)

  # Ladder shaft from bunker to surface
  for y in range(oy + 1, oy + 13):
    for x in range(lx, lx + 2):
      for z in range(lz, lz + 2):
        _set(v, x, y, z, AIR_B)
    _set(v, lx, y, lz, LADDER)

  # Secret entrance mechanism at surface (steps 1–6)
  sy = oy + 12
  for x in range(lx - 1, lx + 4):
    for z in range(lz - 1, lz + 4):
      _set(v, x, sy - 1, z, DIRT)
  for x in range(lx, lx + 3):
    for z in range(lz, lz + 3):
      _set(v, x, sy, z, GRASS)
  _set(v, lx + 1, sy - 2, lz, STONE)
  _set(v, lx + 2, sy - 2, lz, STONE)
  _set(v, lx + 1, sy - 2, lz + 1, DUST)
  _set(v, lx + 2, sy - 2, lz + 1, DUST)
  _set(v, lx + 3, sy - 2, lz, LIME)
  _set(v, lx + 3, sy - 2, lz + 1, REPEATER)
  _set(v, lx + 3, sy - 2, lz + 2, DUST)
  _set(v, lx + 2, sy - 2, lz + 2, PISTON)
  _set(v, lx + 2, sy - 1, lz + 2, GRASS)
  _set(v, lx, sy, lz + 2, LEVER)
  _set(v, lx + 3, sy, lz, LEVER)

  # --- Interior: Kitchen (upper-left wing) ---
  kx, kz = ox + 2, div_z + 2
  _set(v, kx, oy + 1, kz, IRON)
  _set(v, kx, oy + 2, kz, IRON)
  _set(v, kx, oy + 1, kz + 1, IDOOR)
  _set(v, kx, oy + 2, kz + 1, IDOOR)
  _set(v, kx + 1, oy + 1, kz, SBUTTON)
  _set(v, kx + 3, oy + 1, kz, SMOKER)
  _set(v, kx + 3, oy + 2, kz, SMOKER)
  for cx in (kx + 5, kx + 6):
    _set(v, cx, oy + 1, kz + 1, SQUARTZ)
    _set(v, cx, oy + 1, kz + 2, CAULDRON)
  _set(v, kx + 6, oy + 2, kz + 1, LEVER)
  for bx in range(kx + 1, kx + 5):
    _set(v, bx, oy + 3, kz + 3, JTRAP)
    _set(v, bx, oy + 2, kz + 3, GLOW if bx % 2 == 0 else CHEST)
  _set(v, kx + 2, oy + 1, kz + 4, FURNACE)
  _set(v, kx + 2, oy + 2, kz + 4, RAIL)
  _set(v, kx + 4, oy + 1, kz + 5, CRAFT)
  _set(v, kx + 5, oy + 1, kz + 5, BREW)

  # Bedroom (upper-right wing)
  bx0, bz0 = div_x + 3, oz + 3
  _set(v, bx0, oy + 1, bz0, BED)
  _set(v, bx0 + 1, oy + 1, bz0, BED)
  for x in (bx0 - 1, bx0 + 2):
    _set(v, x, oy + 2, bz0, JPLANK)
    _set(v, x, oy + 3, bz0, JTRAP)
  _set(v, bx0, oy + 3, bz0 - 1, BANNER)
  _set(v, bx0 + 1, oy + 3, bz0 - 1, BANNER)
  wx = bx0 + 4
  _set(v, wx, oy + 1, bz0, BDOOR)
  _set(v, wx, oy + 2, bz0, BDOOR)
  _set(v, wx + 1, oy + 2, bz0, BTRAP)
  _set(v, wx + 1, oy + 3, bz0, BSLAB)

  # Living room (lower-left): sofa + TV
  lx0, lz0 = ox + 3, oz + 3
  for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)):
    px, pz = lx0 + dx * 2, lz0 + dz * 2
    _set(v, px, oy + 1, pz, ASTAIR)
  for dx in range(-1, 2):
    for dz in range(-1, 2):
      _set(v, lx0 + dx, oy + 1, lz0 + dz, OCARPET)
  for dx in range(3):
    for dy in range(2):
      _set(v, ox + 3 + dx, oy + 1 + dy, oz + 2, BCONC)
  _set(v, ox + 4, oy + 1, oz + 1, BOOKS)
  _set(v, ox + 5, oy + 1, oz + 1, CHEST)
  _set(v, ox + 6, oy + 1, oz + 1, BARREL)
  _set(v, ox + 4, oy + 2, oz + 3, POT)
  _set(v, ox + 4, oy + 3, oz + 3, SAPLING)

  # Dining lobby (lower-right): piston table
  dx0, dz0 = div_x + 3, div_z + 3
  for px, pz in ((dx0, dz0), (dx0 + 2, dz0), (dx0, dz0 + 2), (dx0 + 2, dz0 + 2)):
    _set(v, px, oy, pz, RTORCH)
    _set(v, px, oy + 1, pz, PISTON)
    _set(v, px, oy + 2, pz, GCARPET)
  for px in (dx0 - 1, dx0 + 3):
    _set(v, px, oy + 1, dz0 + 1, JSTAIR)
  _set(v, dx0 + 1, oy + 2, dz0 + 3, JTRAP)
  _set(v, dx0 + 1, oy + 3, dz0 + 3, RLAMP)
  _set(v, dx0 + 2, oy + 3, dz0 + 3, LEVER)
  _set(v, dx0 + 1, oy + 2, dz0 + 4, FENCE)

  return v


def _in_circle(x: int, z: int, cx: int, cz: int, r: int) -> bool:
  return (x - cx) ** 2 + (z - cz) ** 2 <= r * r


def _generate_bite_dolphin_fountain() -> np.ndarray:
  """Dolphin Fountain — 15×15 basin, quartz pedestal, leaping prismarine dolphin (book p.78–79)."""
  SBRICK = _b("stone_bricks")
  STONE = _b("stone")
  CHISEL = _b("chiseled_stone_bricks")
  DPRISM = _b("dark_prismarine")
  DSLAB = _b("dark_prismarine_slab")
  PRISM = _b("prismarine")
  PBRICK = _b("prismarine_bricks")
  PBSTAIR = _b("prismarine_brick_stairs")
  PBSLAB = _b("prismarine_brick_slab")
  PSLAB = _b("prismarine_slab")
  QUARTZ = _b("quartz_block")
  QSTAIR = _b("quartz_stairs")
  WATER = _b("water")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 2
  outer_r, inner_r, rim_r = 7, 4, 6  # 15×15 footprint (radius 7)

  # Grass surround; 1-block-deep trench for basin
  for x in range(cx - outer_r - 1, cx + outer_r + 2):
    for z in range(cz - outer_r - 1, cz + outer_r + 2):
      _set(v, x, oy - 1, z, GRASS)

  # Octagonal basin rim — stone bricks, chiseled accents, prismarine/quartz inner border
  for x in range(cx - outer_r, cx + outer_r + 1):
    for z in range(cz - outer_r, cz + outer_r + 1):
      dist_sq = (x - cx) ** 2 + (z - cz) ** 2
      if dist_sq > outer_r ** 2:
        continue
      if dist_sq > rim_r ** 2:
        block = CHISEL if (x + z) % 5 == 0 else SBRICK if (x + z) % 2 == 0 else STONE
        _set(v, x, oy - 1, z, block)
        _set(v, x, oy, z, block)
        _set(v, x, oy + 1, z, DPRISM if (x + z) % 3 == 0 else PRISM)
      elif dist_sq > inner_r ** 2:
        _set(v, x, oy - 1, z, QUARTZ)
        _set(v, x, oy, z, QUARTZ if (x + z) % 2 == 0 else PRISM)
        _set(v, x, oy + 1, z, WATER)
      else:
        _set(v, x, oy, z, WATER)
        _set(v, x, oy + 1, z, WATER)

  # 5×5 pedestal — dark prismarine slab base, quartz stair tiers, prismarine slab cap
  px0, pz0 = cx - 2, cz - 2
  for x in range(px0, px0 + 5):
    for z in range(pz0, pz0 + 5):
      _set(v, x, oy, z, DSLAB)
  for layer in range(1, 4):
    inset = layer
    for x in range(px0 + inset, px0 + 5 - inset):
      for z in range(pz0 + inset, pz0 + 5 - inset):
        _set(v, x, oy + layer, z, QSTAIR if (x + z) % 2 == 0 else QUARTZ)
  for x in range(px0 + 1, px0 + 4):
    for z in range(pz0 + 1, pz0 + 4):
      _set(v, x, oy + 4, z, PSLAB)
  _set(v, cx, oy + 5, cz, WATER)

  # Dolphin statue — 11×5×7 leaping pose (nose +z, tail -z)
  dy = oy + 5
  # Dorsal fin
  _set(v, cx, dy + 2, cz, PBRICK)
  _set(v, cx, dy + 3, cz, PBSTAIR)
  _set(v, cx, dy + 4, cz, PBSTAIR)

  # Head and snout
  _set(v, cx, dy + 1, cz + 1, PBRICK)
  _set(v, cx, dy + 2, cz + 2, PBSLAB)
  _set(v, cx, dy + 2, cz + 3, PBRICK)
  _set(v, cx, dy + 3, cz + 4, PBSTAIR)
  _set(v, cx, dy + 2, cz + 5, PBSLAB)

  # Arched body
  body = (
    (0, 3, cz), (0, 4, cz - 1), (0, 4, cz - 2), (0, 3, cz - 3),
    (0, 2, cz - 4), (-1, 2, cz - 4), (1, 2, cz - 4),
  )
  for dx, lift, bz in body:
    _set(v, cx + dx, dy + lift, bz, PBRICK if lift % 2 == 0 else PBSTAIR)

  # Underbelly slab curve
  for i in range(1, 5):
    _set(v, cx, dy + 1, cz - i, PBSLAB)

  # Tail flukes
  _set(v, cx, dy + 1, cz - 5, PBSTAIR)
  _set(v, cx - 1, dy + 1, cz - 6, PBSLAB)
  _set(v, cx + 1, dy + 1, cz - 6, PBSLAB)
  _set(v, cx - 2, dy + 2, cz - 5, PBSLAB)
  _set(v, cx + 2, dy + 2, cz - 5, PBSLAB)

  # Pectoral fins
  _set(v, cx - 2, dy + 2, cz, PBSLAB)
  _set(v, cx + 2, dy + 2, cz, PBSLAB)

  return v


def _generate_bite_aviary_pyramid() -> np.ndarray:
  """Aviary Pyramid — 14×16 stepped glass pyramid, tree, pond, foyer (steps 1–15)."""
  GRASS = _b("grass_block")
  QBRICK = _b("quartz_bricks")
  BLACK = _b("blackstone")
  PBSTONE = _b("polished_blackstone")
  PBBRICK = _b("polished_blackstone_bricks")
  PBSTAIR = _b("polished_blackstone_stairs")
  CHISEL = _b("chiseled_polished_blackstone")
  OGLASS = _b("orange_stained_glass")
  BDOOR = _b("birch_door")
  STONE = _b("stone")
  SSLAB = _b("stone_slab")
  SSTAIR = _b("stone_stairs")
  JLOG = _b("jungle_log")
  JLEAF = _b("jungle_leaves")
  JFENCE = _b("jungle_fence")
  WATER = _b("water")
  FERN = _b("fern")
  TULIP = _b("red_tulip")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 8, 2
  width, depth = 14, 16
  cx = ox + width // 2

  # Step 1 — foundation: blackstone outer, quartz inner, grass center, 3-wide entrance
  for x in range(ox, ox + width):
    for z in range(oz, oz + depth):
      edge = x in (ox, ox + width - 1) or z in (oz, oz + depth - 1)
      mid_ring = x in (ox + 1, ox + width - 2) or z in (oz + 1, oz + depth - 2)
      if edge:
        _set(v, x, oy - 1, z, GRASS)
        _set(v, x, oy, z, BLACK)
      elif mid_ring:
        _set(v, x, oy, z, QBRICK)
      else:
        _set(v, x, oy, z, GRASS)

  # Steps 2–7 — stepped pyramid walls (4 tiers, 2 blocks high each)
  tiers = 4
  for tier in range(tiers):
    inset = tier
    x0, z0 = ox + inset, oz + inset
    x1, z1 = ox + width - 1 - inset, oz + depth - 1 - inset
    base_y = oy + 1 + tier * 2
    for y in range(base_y, base_y + 2):
      for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
          on_edge = x in (x0, x1) or z in (z0, z1)
          if not on_edge:
            continue
          corner = x in (x0, x1) and z in (z0, z1)
          entrance = z == z0 and x in (cx - 1, cx, cx + 1) and tier < 2
          if entrance and y < base_y + 2:
            if tier == 1 and y == base_y:
              _set(v, x, y, z, BDOOR)
            continue
          if corner:
            _set(v, x, y, z, PBBRICK if y == base_y else PBSTAIR)
          elif y == base_y + 1 and (x == x0 or x == x1 or z == z1):
            _set(v, x, y, z, PBSTAIR)
          else:
            _set(v, x, y, z, OGLASS)
    # Roof cap on top tier interior
    if tier == tiers - 1:
      for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
          _set(v, x, base_y + 2, z, CHISEL)

  # Step 7 — foyer porch extending from entrance
  fz = oz - 2
  for x in range(cx - 2, cx + 3):
    for z in range(fz, oz):
      edge = x in (cx - 2, cx + 2) or z == fz
      _set(v, x, oy, z, BLACK if z == fz else QBRICK)
      _set(v, x, oy + 1, z, PBBRICK if edge else OGLASS)
      if z == fz and x in (cx - 1, cx):
        _set(v, x, oy + 1, z, BDOOR)

  # Steps 8–9 — interior stone pond basin (center)
  px, pz = cx - 2, oz + depth // 2 - 1
  for x in range(px, px + 5):
    for z in range(pz, pz + 5):
      if x in (px, px + 4) or z in (pz, pz + 4):
        _set(v, x, oy + 1, z, SSTAIR if (x + z) % 2 == 0 else SSLAB)
      elif x in (px + 1, px + 3) and z in (pz + 1, pz + 3):
        _set(v, x, oy + 1, z, WATER)
      else:
        _set(v, x, oy + 1, z, STONE)
  for dx, dz in ((px - 1, pz + 2), (px + 5, pz + 2), (px + 2, pz - 1)):
    _set(v, dx, oy + 1, dz, FERN)
    _set(v, dx, oy + 2, dz, TULIP)

  # Steps 10–13 — jungle tree with perches (back-right corner)
  tx, tz = ox + width - 4, oz + depth - 4
  for y in range(oy + 1, oy + 6):
    _set(v, tx, y, tz, JLOG)
  branches = ((1, 0, oy + 4), (-1, 1, oy + 4), (0, -1, oy + 5), (2, 0, oy + 5), (-2, 1, oy + 5), (1, 2, oy + 5))
  for dx, dz, by in branches:
    _set(v, tx + dx, by, tz + dz, JLOG)
    _set(v, tx + dx, by + 1, tz + dz, JFENCE)
    for lx in range(-1, 2):
      for lz in range(-1, 2):
        if abs(lx) + abs(lz) < 2:
          _set(v, tx + dx + lx, by + 2, tz + dz + lz, JLEAF)

  # Leaves by entrance (step 10)
  for x in (cx - 2, cx + 2):
    _set(v, x, oy + 1, oz + 2, JLEAF)
    _set(v, x, oy + 2, oz + 2, JLEAF)

  return v


def _sub_hull_ring(dx: int, dy: int) -> bool:
  """5×5 ring with corners removed (book step 1)."""
  if abs(dx) > 2 or abs(dy) > 2:
    return False
  return not (abs(dx) == 2 and abs(dy) == 2)


def _generate_bite_deep_sea_submarine() -> np.ndarray:
  """Deep-Sea Submarine — concrete hull, glass nose, fins, blast furnace propeller (steps 1–8)."""
  LGRAY = _b("light_gray_concrete")
  GLASS = _b("glass")
  IRON = _b("iron_block")
  ANDESITE = _b("polished_andesite")
  ASTAIR = _b("polished_andesite_stairs")
  ASLAB = _b("polished_andesite_slab")
  AWALL = _b("polished_andesite_wall")
  BLAST = _b("blast_furnace")
  WATER = _b("water")
  EROD = _b("end_rod")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 11, 14
  length = 9

  # Water environment
  for x in range(cx - 6, cx + 7):
    for z in range(cz - 3, cz + length + 3):
      for y in range(oy - 3, oy + 6):
        _set(v, x, y, z, WATER)

  # Steps 1–2 — 9-block cylindrical hull ring
  for z in range(cz, cz + length):
    for dx in range(-2, 3):
      for dy in range(-2, 3):
        if _sub_hull_ring(dx, dy):
          _set(v, cx + dx, oy + dy, z, LGRAY)

  # Steps 3–4 — rear walls with +-shaped gap, then two more rear layers
  back = cz + length - 1
  for layer in range(3):
    bz = back - layer
    for dx in range(-2, 3):
      for dy in range(-2, 3):
        if not _sub_hull_ring(dx, dy):
          continue
        plus_gap = abs(dx) <= 1 and abs(dy) <= 1 and not (dx == 0 and dy == 0)
        if layer == 0 and plus_gap:
          continue
        if layer >= 1 and abs(dx) <= 1 and abs(dy) <= 1:
          continue
        _set(v, cx + dx, oy + dy, bz, LGRAY)

  # Step 5 — glass and iron cockpit nose
  nose = cz
  for dx in range(-1, 2):
    for dy in range(-1, 2):
      block = GLASS if abs(dx) + abs(dy) < 2 else IRON
      _set(v, cx + dx, oy + dy, nose, block)
  _set(v, cx, oy, nose, LGRAY)
  _set(v, cx, oy + 2, nose, LGRAY)
  _set(v, cx - 2, oy + 1, nose, LGRAY)
  _set(v, cx + 2, oy + 1, nose, LGRAY)

  # Step 6 — tower fin above 2-block top gap
  for z in range(cz + 3, cz + 6):
    for dx in (-1, 0, 1):
      _set(v, cx + dx, oy + 3, z, LGRAY)
    _set(v, cx, oy + 4, z, LGRAY)
  for z in (cz + 3, cz + 5):
    _set(v, cx, oy + 3, z, ASTAIR)
  _set(v, cx, oy + 5, cz + 4, EROD)

  # Step 7 — side fins
  for z in range(cz + 3, cz + 6):
    for side in (-1, 1):
      fx = cx + side * 3
      _set(v, fx, oy, z, ANDESITE)
      _set(v, fx + side, oy, z, ASLAB)
      _set(v, fx, oy - 1, z, ASTAIR)
      _set(v, fx, oy + 1, z, GLASS if z == cz + 4 else ASTAIR)

  # Step 8 — blast furnace propeller at stern
  _set(v, cx, oy + 1, back + 1, BLAST)
  for dx, dy in ((0, 2), (0, -2), (2, 1), (-2, 1)):
    _set(v, cx + dx, oy + dy, back + 1, AWALL)
    _set(v, cx + dx // 2, oy + dy // 2 + 1, back + 1, ASLAB)

  # Submarine panels — andesite inset detailing on hull sides
  for z in range(cz + 2, cz + 7):
    for side in (-1, 1):
      _set(v, cx + side * 2, oy + side, z, ASTAIR)

  return v


def _generate_bite_underwater_airlock() -> np.ndarray:
  """Underwater Airlock — trapdoor hatch, piston circuit, mounts under submarine (p.90–91)."""
  PAND = _b("polished_andesite")
  ASTAIR = _b("andesite_stairs")
  ASLAB = _b("andesite_slab")
  ATRAP = _b("acacia_trapdoor")
  PISTON = _b("sticky_piston")
  DUST = _b("redstone_dust")
  REPEATER = _b("redstone_repeater")
  LEVER = _b("lever")
  STONE = _b("stone")
  WATER = _b("water")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 11, 12

  # Underwater setting
  for x in range(cx - 4, cx + 5):
    for z in range(cz - 4, cz + 5):
      for y in range(oy - 2, oy + 5):
        _set(v, x, y, z, WATER)

  # Bottom hatch — andesite slab frame + acacia trapdoor
  for dx in range(-1, 2):
    for dz in range(-1, 2):
      _set(v, cx + dx, oy, cz + dz, ASLAB if abs(dx) + abs(dz) < 2 else PAND)
  _set(v, cx, oy + 1, cz, ATRAP)

  # Piston + andesite stairs linkage
  _set(v, cx, oy + 2, cz, PISTON)
  _set(v, cx, oy + 2, cz + 1, ASTAIR)
  _set(v, cx + 1, oy + 2, cz, ASTAIR)

  # Redstone path on polished andesite (book side/bottom views)
  for dx in range(0, 3):
    _set(v, cx + dx, oy + 3, cz + 2, PAND)
    _set(v, cx + dx, oy + 3, cz + 2, DUST)
  _set(v, cx + 2, oy + 3, cz + 2, REPEATER)
  _set(v, cx, oy + 4, cz + 1, STONE)
  _set(v, cx, oy + 5, cz + 1, LEVER)

  # Hull mounting plate above mechanism
  for dx in range(-2, 3):
    for dz in range(-2, 3):
      _set(v, cx + dx, oy + 6, cz + dz, _b("light_gray_concrete"))

  return v


def _chalet_footprint(rel_x: int, rel_z: int) -> bool:
  """L-shaped 9×11 base (book step 1)."""
  if not (0 <= rel_x < 9 and 0 <= rel_z < 11):
    return False
  if rel_z < 7:
    return True
  return rel_x < 4


def _generate_bite_tropical_chalet() -> np.ndarray:
  """Tropical Beach Chalet — stilt chalet, veranda, kitchen, dock (steps 1–8)."""
  SAND = _b("sand")
  COBBLE = _b("cobblestone")
  OLOG = _b("oak_log")
  OPLANK = _b("oak_planks")
  OFENCE = _b("oak_fence")
  ODOOR = _b("oak_door")
  OSIGN = _b("oak_sign")
  ASLAB = _b("acacia_slab")
  ASTAIR = _b("acacia_stairs")
  WCONC = _b("white_concrete")
  GCONC = _b("gray_concrete")
  SQUARTZ = _b("smooth_quartz")
  GLASS = _b("glass_pane")
  DPSLAB = _b("dark_prismarine_slab")
  BSTAIR = _b("birch_stairs")
  BTRAP = _b("birch_trapdoor")
  SCAFF = _b("scaffolding")
  FURNACE = _b("furnace")
  ARAIL = _b("activator_rail")
  QSTAIR = _b("quartz_stairs")
  TORCH = _b("torch")
  BBANNER = _b("blue_banner")
  BED = _b("bed")
  CHEST = _b("chest")
  GRAVEL = _b("gravel")
  DIRT = _b("dirt")
  CAMPFIRE = _b("campfire")
  WATER = _b("water")
  WBANNER = _b("white_banner")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 10, 4
  deck_y = oy + 3

  # Water and island surround
  for x in range(ox - 4, ox + 14):
    for z in range(oz - 4, oz + 16):
      _set(v, x, oy - 1, z, WATER)
      _set(v, x, oy - 2, z, WATER)

  # Step 1 — L-shaped sand base on cobblestone stilts
  pillar_spots = []
  for rel_x in range(9):
    for rel_z in range(11):
      if not _chalet_footprint(rel_x, rel_z):
        continue
      x, z = ox + rel_x, oz + rel_z
      for y in range(oy - 2, oy):
        _set(v, x, y, z, COBBLE)
      _set(v, x, oy, z, SAND)
      if rel_x in (0, 8) or rel_z in (0, 10) or (rel_x, rel_z) in ((0, 0), (8, 0), (0, 6), (3, 10)):
        pillar_spots.append((x, z))

  # Step 2 — ten oak columns + acacia slab floor
  for x, z in pillar_spots[:10]:
    _set(v, x, oy + 1, z, OLOG)
    _set(v, x, oy + 2, z, OLOG)
  for rel_x in range(9):
    for rel_z in range(11):
      if _chalet_footprint(rel_x, rel_z):
        _set(v, ox + rel_x, deck_y, oz + rel_z, ASLAB)

  # Kitchen tile corner (2×3 checker)
  for dx in range(2):
    for dz in range(3):
      _set(v, ox + 1 + dx, deck_y, oz + 1 + dz, WCONC if (dx + dz) % 2 == 0 else GCONC)

  # Entrance acacia stairs (front)
  for dx in (-1, 0, 1):
    _set(v, ox + 4 + dx, deck_y - 1, oz - 1, ASTAIR)

  # Steps 3–5 — walls (oak corners, white concrete, quartz accents)
  wall_h = 4
  for y in range(deck_y + 1, deck_y + 1 + wall_h):
    for rel_x in range(9):
      for rel_z in range(11):
        if not _chalet_footprint(rel_x, rel_z):
          continue
        x, z = ox + rel_x, oz + rel_z
        edge = rel_x in (0, 8) or rel_z in (0, 10) or (rel_z >= 7 and rel_x >= 4)
        if not edge:
          continue
        corner = rel_x in (0, 8) and rel_z in (0, 6)
        if rel_z == 0 and rel_x in (3, 4, 5) and y < deck_y + 3:
          _set(v, x, y, z, AIR_B)
        elif corner:
          _set(v, x, y, z, OLOG)
        elif y == deck_y + 2 and rel_z in (0, 10) and rel_x not in (0, 8):
          _set(v, x, y, z, GLASS)
        elif rel_z in (0, 10) and rel_x in (4, 5) and y == deck_y + 3:
          _set(v, x, y, z, SQUARTZ)
        else:
          _set(v, x, y, z, WCONC)

  # Oak doors at entrance
  _set(v, ox + 4, deck_y + 1, oz, ODOOR)
  _set(v, ox + 4, deck_y + 2, oz, ODOOR)

  # Veranda deck railing (front z=oz)
  for rel_x in range(9):
    if _chalet_footprint(rel_x, 0):
      _set(v, ox + rel_x, deck_y + 1, oz - 1, OPLANK)
      _set(v, ox + rel_x, deck_y + 2, oz - 1, OFENCE)
  _set(v, ox + 2, deck_y + 2, oz - 1, TORCH)
  _set(v, ox + 6, deck_y + 2, oz - 1, TORCH)
  for dx in range(3):
    _set(v, ox + 1 + dx, deck_y + 1, oz - 1, BSTAIR)

  # Kitchen stoves + scaffolding tables
  _set(v, ox + 1, deck_y + 1, oz + 1, FURNACE)
  _set(v, ox + 2, deck_y + 1, oz + 1, FURNACE)
  _set(v, ox + 1, deck_y + 2, oz + 1, ARAIL)
  _set(v, ox + 2, deck_y + 2, oz + 1, ARAIL)
  _set(v, ox + 1, deck_y + 3, oz + 1, QSTAIR)
  _set(v, ox + 2, deck_y + 3, oz + 2, SCAFF)
  _set(v, ox + 2, deck_y + 4, oz + 2, BTRAP)

  # Interior decor
  _set(v, ox + 6, deck_y + 1, oz + 5, BED)
  _set(v, ox + 7, deck_y + 1, oz + 5, CHEST)
  _set(v, ox + 6, deck_y + 3, oz + 4, BBANNER)
  _set(v, ox + 7, deck_y + 3, oz + 4, BBANNER)

  # Step 6 — tiered roof
  roof_y = deck_y + wall_h
  for rel_x in range(9):
    for rel_z in range(11):
      if not _chalet_footprint(rel_x, rel_z):
        continue
      edge = rel_x in (0, 8) or rel_z in (0, 10) or (rel_z >= 7 and rel_x >= 4)
      _set(v, ox + rel_x, roof_y, oz + rel_z, DPSLAB if edge else ASLAB)
  for layer in range(1, 3):
    for rel_x in range(layer, 9 - layer):
      for rel_z in range(layer, 11 - layer):
        if _chalet_footprint(rel_x, rel_z):
          _set(v, ox + rel_x, roof_y + layer, oz + rel_z, ASLAB)

  # Step 7 — oak pergola with sign slats over veranda
  for rel_x in (1, 7):
    for y in range(roof_y + 1, roof_y + 4):
      _set(v, ox + rel_x, y, oz - 1, OLOG)
  for rel_x in range(2, 7):
    _set(v, ox + rel_x, roof_y + 3, oz - 1, OLOG)
    _set(v, ox + rel_x, roof_y + 4, oz - 1, OSIGN)

  # Step 8 + essentials — dock, campfire, gravel path, flower bed
  for dx in range(5):
    _set(v, ox - 2, deck_y - 1, oz + 2 + dx, OPLANK)
    _set(v, ox - 2, deck_y, oz + 2 + dx, ASLAB)
  for dz in (2, 6):
    _set(v, ox - 2, deck_y + 1, oz + dz, OLOG)
    _set(v, ox - 2, deck_y + 2, oz + dz, TORCH)

  # Campfire area (3×3 sand)
  for dx in range(-1, 2):
    for dz in range(-1, 2):
      _set(v, ox + 8 + dx, oy, oz + 8 + dz, SAND)
  _set(v, ox + 8, deck_y - 2, oz + 8, COBBLE)
  _set(v, ox + 8, deck_y - 1, oz + 8, CAMPFIRE)
  for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
    _set(v, ox + 8 + dx, deck_y - 1, oz + 8 + dz, OLOG)

  # Towel rack
  _set(v, ox + 7, deck_y + 2, oz + 2, OFENCE)
  _set(v, ox + 8, deck_y + 2, oz + 2, OFENCE)
  _set(v, ox + 7, deck_y + 3, oz + 2, ASLAB)
  _set(v, ox + 7, deck_y + 3, oz + 3, BBANNER)
  _set(v, ox + 8, deck_y + 3, oz + 3, WBANNER)

  # Gravel path + flower bed
  for dx in range(3):
    _set(v, ox + 3 + dx, oy, oz - 2, GRAVEL)
  _set(v, ox + 8, oy + 1, oz + 3, DIRT)
  _set(v, ox + 8, oy + 1, oz + 4, BTRAP)
  _set(v, ox + 8, oy + 2, oz + 3, _b("poppy"))

  return v


def _generate_bite_survivalists_vault() -> np.ndarray:
  """Survivalist's Vault — 9×9 underground storage with two-floor chest walls (steps 1–10)."""
  SBRICK = _b("stone_bricks")
  COBBLE = _b("cobblestone")
  CSTAIR = _b("cobblestone_stairs")
  SBSTAIR = _b("stone_brick_stairs")
  IBARS = _b("iron_bars")
  CHEST = _b("chest")
  LADDER = _b("ladder")
  LANTERN = _b("lantern")
  PBUTTON = _b("polished_blackstone_button")
  ANVIL = _b("anvil")
  GRIND = _b("grindstone")
  FURNACE = _b("furnace")
  CRAFT = _b("crafting_table")
  CAULDRON = _b("cauldron")
  CAMPFIRE = _b("campfire")
  SSLAB = _b("spruce_slab")
  STRAP = _b("spruce_trapdoor")
  SPRUCE = _b("spruce_planks")
  BANNER = _b("red_banner")
  FRAME = _b("item_frame")
  DIRT = _b("dirt")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 11, 3
  size = 9
  cx, cz = ox + 4, oz + 4

  # Underground excavation
  for x in range(ox - 1, ox + size + 1):
    for z in range(oz - 1, oz + size + 1):
      for y in range(oy - 3, oy):
        _set(v, x, y, z, DIRT)

  # Step 1 — foundation with cobblestone stair indents
  for x in range(ox, ox + size):
    for z in range(oz, oz + size):
      edge = x in (ox, ox + size - 1) or z in (oz, oz + size - 1)
      mid_gap = (x == cx and z in (oz, oz + size - 1)) or (z == cz and x in (ox, ox + size - 1))
      if mid_gap:
        _set(v, x, oy, z, CSTAIR)
      elif edge:
        _set(v, x, oy, z, COBBLE)
      else:
        _set(v, x, oy, z, SBRICK)

  def _wall_cell(x: int, z: int) -> bool:
    return x in (ox, ox + size - 1) or z in (oz, oz + size - 1)

  def _center_gap(x: int, z: int) -> bool:
    return (x == cx and z in (oz, oz + size - 1)) or (z == cz and x in (ox, ox + size - 1))

  # Steps 2–4 — lower walls with chest alcoves and ladder
  for y in range(oy + 1, oy + 4):
    for x in range(ox, ox + size):
      for z in range(oz, oz + size):
        if not _wall_cell(x, z):
          continue
        if _center_gap(x, z) and y < oy + 3:
          if y == oy + 1 and z == oz:
            _set(v, x, y, z, SBSTAIR)  # entrance arch (step 4)
          continue
        if y == oy + 2 and not _center_gap(x, z):
          _set(v, x, y, z, IBARS if (x + z) % 3 == 0 else SBRICK)
        else:
          _set(v, x, y, z, SBRICK)

  # Ground floor chests — two double chests per side (step 3)
  for side, positions in (
    ("north", [(ox + 2, oz), (ox + 5, oz)]),
    ("south", [(ox + 2, oz + size - 1), (ox + 5, oz + size - 1)]),
    ("west", [(ox, oz + 2), (ox, oz + 5)]),
    ("east", [(ox + size - 1, oz + 2), (ox + size - 1, oz + 5)]),
  ):
    for px, pz in positions:
      _set(v, px, oy + 1, pz, CHEST)
      _set(v, px + (1 if side in ("north", "south") else 0), oy + 1, pz + (1 if side in ("east", "west") else 0), CHEST)

  # Corner ladder (step 2–6)
  for y in range(oy + 1, oy + 8):
    _set(v, ox + 1, y, oz + 1, LADDER)

  # Step 5 — interior utility center + campfire cauldron light
  _set(v, cx, oy + 1, cz, COBBLE)
  _set(v, cx, oy + 2, cz, CAULDRON)
  _set(v, cx, oy + 3, cz, CAMPFIRE)
  _set(v, cx - 2, oy + 1, cz, ANVIL)
  _set(v, cx + 2, oy + 1, cz, GRIND)
  _set(v, cx, oy + 1, cz - 2, FURNACE)
  _set(v, cx, oy + 1, cz + 2, CRAFT)
  _set(v, cx - 1, oy + 3, cz - 1, LANTERN)
  _set(v, cx + 1, oy + 3, cz + 1, PBUTTON)

  # Spruce plank ceiling accents
  for x in range(ox + 1, ox + size - 1):
    for z in range(oz + 1, oz + size - 1):
      if (x + z) % 4 == 0:
        _set(v, x, oy + 3, z, SPRUCE)

  # Steps 6–8 — second-floor balcony and upper chests
  balcony_y = oy + 4
  for x in range(ox + 1, ox + size - 1):
    for z in range(oz + 1, oz + size - 1):
      edge = x in (ox + 1, ox + size - 2) or z in (oz + 1, oz + size - 2)
      if edge:
        _set(v, x, balcony_y, z, SSLAB)
        _set(v, x, balcony_y + 1, z, STRAP)

  for x in range(ox + 2, ox + size - 2, 3):
    _set(v, x, balcony_y, oz + 2, CSTAIR)

  # Upper wall layers + chests (steps 7–8)
  for y in range(oy + 5, oy + 8):
    for x in range(ox, ox + size):
      for z in range(oz, oz + size):
        if _wall_cell(x, z):
          _set(v, x, y, z, SBRICK if y < oy + 7 else IBARS)

  for px, pz in ((ox + 2, oz + 1), (ox + 5, oz + 1), (ox + 2, oz + size - 2), (ox + 5, oz + size - 2)):
    _set(v, px, oy + 5, pz, CHEST)
    _set(v, px + 1, oy + 5, pz, CHEST)
    _set(v, px, oy + 6, pz, LANTERN)

  # Red banners and item frame labels (step 10)
  _set(v, ox + 3, oy + 3, oz + 3, BANNER)
  _set(v, ox + 5, oy + 3, oz + 5, BANNER)
  _set(v, ox + 2, oy + 2, oz, FRAME)
  _set(v, ox + 6, oy + 2, oz, FRAME)

  # Step 9 — stone brick roof
  for x in range(ox, ox + size):
    for z in range(oz, oz + size):
      _set(v, x, oy + 8, z, SBRICK)

  return v


def _generate_bite_unicorn_statue() -> np.ndarray:
  """
  Unicorn Statue — book dimensions (scaled for 32³):
    6×6 quartz pedestal with purpur trim, rearing unicorn with end rod horn.
  """
  QUARTZ = _b("smooth_quartz")
  PURPUR = _b("purpur_block")
  P_STAIRS = _b("purpur_stairs")
  P_SLAB = _b("purpur_slab")
  ROD = _b("end_rod")
  EYE = _b("polished_blackstone_button")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  ps = 6  # pedestal size (scaled from 10)

  # Grass pad
  for x in range(cx - 5, cx + 6):
    for z in range(cz - 5, cz + 6):
      _set(v, x, oy - 1, z, GRASS)

  # Pedestal — 6×6 quartz, 4 blocks tall
  px, pz = cx - 3, cz - 3
  for y in range(4):
    for x in range(px, px + ps):
      for z in range(pz, pz + ps):
        _set(v, x, oy + y, z, QUARTZ)

  # Purpur slab trim on pedestal top edge
  for x in range(px, px + ps):
    for z in range(pz, pz + ps):
      if x in (px, px + ps - 1) or z in (pz, pz + ps - 1):
        _set(v, x, oy + 4, z, P_SLAB)

  # End rod corner posts
  for x, z in ((px, pz), (px + ps - 1, pz), (px, pz + ps - 1), (px + ps - 1, pz + ps - 1)):
    _set(v, x, oy + 4, z, ROD)
    _set(v, x, oy + 5, z, ROD)

  sy = oy + 4  # statue base on pedestal top

  # Hind legs — quartz with purpur hooves
  for lx, lz in ((cx - 1, cz + 1), (cx + 1, cz + 1)):
    _set(v, lx, sy, lz, PURPUR)  # hoof
    for y in range(1, 5):
      _set(v, lx, sy + y, lz, QUARTZ)

  # Torso
  for y in range(4, 7):
    for x in range(cx - 1, cx + 2):
      for z in range(cz - 1, cz + 2):
        _set(v, x, sy + y, z, QUARTZ)

  # Front legs raised (rearing pose)
  for lx, lz, ly in ((cx - 1, cz - 2, 3), (cx + 1, cz - 2, 3), (cx - 1, cz - 3, 5), (cx + 1, cz - 3, 5)):
    _set(v, lx, sy + ly, lz, PURPUR if ly == 3 else QUARTZ)

  # Neck rising toward head
  for y in range(7, 10):
    _set(v, cx, sy + y, cz - 2, QUARTZ)
    _set(v, cx, sy + y, cz - 1, P_STAIRS)  # mane

  # Head and snout
  _set(v, cx, sy + 10, cz - 2, QUARTZ)
  _set(v, cx, sy + 10, cz - 3, QUARTZ)
  _set(v, cx - 1, sy + 10, cz - 2, EYE)
  _set(v, cx, sy + 11, cz - 2, ROD)  # horn

  # Mane along back
  for z in range(cz, cz + 2):
    _set(v, cx, sy + 8, z, P_STAIRS)
    _set(v, cx, sy + 9, z, P_STAIRS)

  # Tail — purpur blocks at rear
  for y, z in ((6, cz + 2), (7, cz + 3), (8, cz + 3)):
    _set(v, cx, sy + y, z, PURPUR)

  return v


def _generate_bite_hillside_home() -> np.ndarray:
  """
  Hillside Home — book dimensions (scaled for 32³):
    12×10 home dug into hill, furnished kitchen bedroom living room, grass roof.
  """
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  COBBLE = _b("cobblestone")
  SBRICK = _b("stone_bricks")
  STONE = _b("stone")
  D_PLANKS = _b("dark_oak_planks")
  DOOR = _b("dark_oak_door")
  S_PLANKS = _b("spruce_planks")
  S_STAIRS = _b("spruce_stairs")
  S_SLAB = _b("spruce_slab")
  S_TRAP = _b("spruce_trapdoor")
  S_FENCE = _b("spruce_fence")
  S_GATE = _b("spruce_fence_gate")
  LIME = _b("lime_concrete")
  WHITE = _b("white_concrete")
  BLACK = _b("black_concrete")
  GLASS = _b("glass_pane")
  LANTERN = _b("lantern")
  CAMP = _b("campfire")
  FURNACE = _b("furnace")
  SMOKER = _b("smoker")
  CAULDRON = _b("cauldron")
  BED = _b("red_bed")
  CHEST = _b("chest")
  BARREL = _b("barrel")
  SHELF = _b("bookshelf")
  LECTERN = _b("lectern")
  YELLOW = _b("yellow_carpet")
  RED = _b("red_carpet")
  LEAVES = _b("oak_leaves")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  bx, bz, oy = 10, 11, 2
  w, d, wh = 11, 9, 4

  # Hillside surround — grass and dirt mound
  for x in range(bx - 3, bx + w + 4):
    for z in range(bz - 4, bz + d + 5):
      _set(v, x, oy - 1, z, GRASS if z < bz else DIRT)
  for x in range(bx - 2, bx + w + 3):
    for z in range(bz - 1, bz + d + 2):
      _set(v, x, oy + wh + 1, z, DIRT)
      _set(v, x, oy + wh + 2, z, GRASS)

  # Foundation — cobblestone outline, plank interior
  for x in range(bx, bx + w):
    for z in range(bz, bz + d):
      edge = x in (bx, bx + w - 1) or z in (bz, bz + d - 1)
      if edge:
        _set(v, x, oy, z, COBBLE)
      else:
        # Kitchen checker floor (northwest corner)
        if bx + 1 <= x <= bx + 4 and bz + 1 <= z <= bz + 4:
          _set(v, x, oy, z, WHITE if (x + z) % 2 == 0 else BLACK)
        else:
          _set(v, x, oy, z, D_PLANKS)

  # Walls — lime concrete with stone brick pillars
  for y in range(1, wh + 1):
    for x in range(bx, bx + w):
      for z in range(bz, bz + d):
        edge = x in (bx, bx + w - 1) or z in (bz, bz + d - 1)
        corner = x in (bx, bx + w - 1) and z in (bz, bz + d - 1)
        if corner:
          _set(v, x, oy + y, z, SBRICK)
        elif edge and y < wh:
          if (x == bx + 5 and z == bz) or (x == bx + 3 and z == bz + d - 1):
            _set(v, x, oy + y, z, GLASS if y in (2, 3) else LIME)
          elif not (x == bx + 5 and z == bz and y < 3):
            _set(v, x, oy + y, z, LIME)
        elif y == wh and not edge:
          _set(v, x, oy + y, z, STONE)  # ceiling stone under dirt

  # Hearth / campfire (living room center-east)
  _set(v, bx + 7, oy, bz + 3, CAMP)
  _set(v, bx + 7, oy + 1, bz + 2, STONE)
  _set(v, bx + 8, oy + 1, bz + 2, STONE)

  # Kitchen interior
  _set(v, bx + 2, oy + 1, bz + 2, FURNACE)
  _set(v, bx + 3, oy + 1, bz + 2, SMOKER)
  _set(v, bx + 2, oy + 1, bz + 3, CAULDRON)
  _set(v, bx + 1, oy + 2, bz + 2, S_TRAP)
  _set(v, bx + 1, oy + 2, bz + 3, S_TRAP)

  # Bedroom (southwest)
  _set(v, bx + 2, oy + 1, bz + 7, BED)
  _set(v, bx + 3, oy + 1, bz + 7, BED)
  _set(v, bx + 1, oy + 1, bz + 6, CHEST)
  _set(v, bx + 1, oy + 1, bz + 5, SHELF)
  _set(v, bx + 2, oy + 1, bz + 5, SHELF)

  # Living room rugs and lectern
  for x in range(bx + 6, bx + 9):
    for z in range(bz + 4, bz + 7):
      _set(v, x, oy + 1, z, YELLOW if x < bx + 8 else RED)
  _set(v, bx + 8, oy + 1, bz + 5, LECTERN)
  _set(v, bx + 9, oy + 1, bz + 4, SHELF)

  # Storage nook (northeast)
  _set(v, bx + 8, oy + 1, bz + 1, BARREL)
  _set(v, bx + 9, oy + 1, bz + 1, BARREL)
  _set(v, bx + 8, oy + 2, bz + 1, BARREL)
  _set(v, bx + 9, oy + 1, bz + 2, CHEST)

  # Lanterns in corridors
  _set(v, bx + 5, oy + 3, bz + 5, LANTERN)
  _set(v, bx + 5, oy + 3, bz + 3, LANTERN)

  # Entrance — dark oak door south center
  _set(v, bx + 5, oy + 1, bz, DOOR)
  _set(v, bx + 5, oy + 2, bz, DOOR)
  _set(v, bx + 5, oy + 3, bz, LANTERN)

  # Circular arch at entrance (spruce stairs)
  for x in range(bx + 4, bx + 7):
    _set(v, x, oy + 3, bz + 1, S_STAIRS)

  # Spruce awning over entrance
  for x in range(bx + 3, bx + 8):
    _set(v, x, oy + 4, bz - 1, S_SLAB)
    _set(v, x, oy + 3, bz - 1, S_STAIRS)
  _set(v, bx + 4, oy + 2, bz - 1, S_GATE)
  _set(v, bx + 6, oy + 2, bz - 1, S_GATE)

  # Front spruce fence walkway
  for x in range(bx + 2, bx + 9):
    _set(v, x, oy, bz - 2, S_FENCE)

  # Trees on hillside
  for tx, tz in ((bx - 2, bz - 2), (bx + w + 1, bz + d)):
    for dy in range(3):
      _set(v, tx, oy + wh + 2 + dy, tz, _b("oak_log"))
    for dx in range(-1, 2):
      for dz in range(-1, 2):
        _set(v, tx + dx, oy + wh + 5, tz + dz, LEAVES)

  return v


def _generate_bite_marine_tugboat() -> np.ndarray:
  """
  Marine Tugboat — book dimensions (scaled for 32³):
    10-block red white tugboat, cabin with bed furnace chests, paddle wheel stern.
  """
  WATER = _b("water")
  GRAY = _b("gray_concrete")
  LGRAY = _b("light_gray_concrete")
  WHITE = _b("white_concrete")
  GLASS = _b("glass")
  RED = _b("red_concrete")
  RNBRICK = _b("red_nether_bricks")
  RNSTAIR = _b("red_nether_brick_stairs")
  RNSLAB = _b("red_nether_brick_slab")
  BLUE = _b("blue_stained_glass")
  GLOW = _b("glowstone")
  I_DOOR = _b("iron_door")
  I_TRAP = _b("iron_trapdoor")
  O_TRAP = _b("oak_trapdoor")
  IRON = _b("iron_block")
  LEVER = _b("lever")
  BUTTON = _b("stone_button")
  QSTAIR = _b("smooth_quartz_stairs")
  LADDER = _b("ladder")
  BED = _b("red_bed")
  FURNACE = _b("furnace")
  CHEST = _b("chest")
  BREW = _b("brewing_stand")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, wl = 16, 12, 14  # water level y
  length = 10

  # Water
  for x in range(cx - 4, cx + 5):
    for z in range(cz - 2, cz + length + 3):
      for y in range(wl - 3, wl + 8):
        _set(v, x, y, z, WATER)

  def beam(z: int) -> range:
    """Hull width tapers at bow/stern."""
    if z < cz + 2 or z > cz + length - 3:
      return range(cx - 1, cx + 2)
    return range(cx - 2, cx + 3)

  # Hull — gray underwater + white deck (steps 1-3)
  for zi, z in enumerate(range(cz, cz + length)):
    xs = list(beam(z))
    for x in xs:
      _set(v, x, wl - 2, z, GRAY)
      _set(v, x, wl - 1, z, GRAY)
      _set(v, x, wl, z, WHITE if zi % 2 == 0 else GRAY)
      if x in (xs[0], xs[-1]):
        _set(v, x, wl, z, GLASS)

  # Red trim layer + steering (step 4)
  for z in range(cz + 2, cz + length - 2):
    for x in beam(z):
      if x == cx - 2 or x == cx + 2 or z in (cz + 2, cz + length - 3):
        _set(v, x, wl + 1, z, RED if (x + z) % 2 == 0 else RNBRICK)
  _set(v, cx, wl + 1, cz + 5, IRON)
  _set(v, cx, wl + 2, cz + 5, LEVER)

  # Cabin walls (step 5-6)
  for z in range(cz + 3, cz + length - 3):
    for x in beam(z):
      if abs(x - cx) == 2:
        _set(v, x, wl + 2, z, BLUE)
      elif x == cx:
        _set(v, x, wl + 2, z, AIR_B)
      else:
        _set(v, x, wl + 2, z, RED)
  # Glowstone bow + doors
  _set(v, cx - 1, wl + 2, cz + 3, GLOW)
  _set(v, cx + 1, wl + 2, cz + 3, GLOW)
  _set(v, cx, wl + 2, cz + 3, I_DOOR)
  _set(v, cx, wl + 3, cz + 3, I_DOOR)
  _set(v, cx - 1, wl + 2, cz + 3, BUTTON)
  _set(v, cx + 1, wl + 3, cz + 3, BUTTON)

  # Cabin interior
  _set(v, cx - 1, wl + 1, cz + 5, BED)
  _set(v, cx, wl + 1, cz + 5, FURNACE)
  _set(v, cx + 1, wl + 1, cz + 5, CHEST)
  _set(v, cx + 1, wl + 1, cz + 6, CHEST)
  _set(v, cx - 1, wl + 1, cz + 6, BREW)

  # Roof (step 7)
  for z in range(cz + 2, cz + length - 2):
    for x in range(cx - 2, cx + 3):
      _set(v, x, wl + 3, z, RNSLAB if (x + z) % 2 else RED)
  _set(v, cx, wl + 4, cz + 4, RNSTAIR)

  # Smokestacks (step 8)
  for sx in (cx - 1, cx + 1):
    for y in range(2):
      _set(v, sx, wl + 4 + y, cz + 6, LGRAY)
      _set(v, sx, wl + 6 + y, cz + 6, WHITE)
  _set(v, cx - 2, wl + 2, cz + 4, I_TRAP)
  _set(v, cx + 2, wl + 2, cz + 4, I_TRAP)

  # Oak trapdoors over glowstone
  _set(v, cx - 1, wl + 3, cz + 3, O_TRAP)
  _set(v, cx + 1, wl + 3, cz + 3, O_TRAP)

  # Paddle wheel stern (step 9)
  sz = cz + length - 1
  _set(v, cx, wl, sz, IRON)
  _set(v, cx - 1, wl + 1, sz, QSTAIR)
  _set(v, cx + 1, wl + 1, sz, QSTAIR)
  _set(v, cx, wl + 2, sz, QSTAIR)

  # Ladders and bow stairs (step 10)
  for z in (cz + 4, cz + 6):
    _set(v, cx - 3, wl + 1, z, LADDER)
    _set(v, cx + 3, wl + 1, z, LADDER)
  _set(v, cx - 1, wl + 2, cz + 2, RNSTAIR)
  _set(v, cx, wl + 2, cz + 2, RNSTAIR)
  _set(v, cx + 1, wl + 2, cz + 2, RNSTAIR)

  return v


def _generate_bite_sidewalk_cafe() -> np.ndarray:
  """
  Sidewalk Cafe — book dimensions (scaled for 32³):
    12×12 brick quartz cafe, awning, outdoor tables, interior counter, roof terrace.
  """
  COBBLE = _b("cobblestone")
  P_AND = _b("polished_andesite")
  AND = _b("andesite")
  A_SLAB = _b("andesite_slab")
  PA_SLAB = _b("polished_andesite_slab")
  A_STAIR = _b("andesite_stairs")
  D_PLANKS = _b("dark_oak_planks")
  D_FENCE = _b("dark_oak_fence")
  D_STAIRS = _b("dark_oak_stairs")
  D_PLATE = _b("dark_oak_pressure_plate")
  D_DOOR = _b("dark_oak_door")
  P_DIOR = _b("polished_diorite")
  BRICK = _b("bricks")
  QBRICK = _b("quartz_bricks")
  CHISEL = _b("chiseled_quartz")
  QSTAIR = _b("quartz_stairs")
  GLASS = _b("glass_pane")
  B_DOOR = _b("birch_door")
  B_TRAP = _b("birch_trapdoor")
  YELLOW = _b("yellow_wool")
  WHITE = _b("white_wool")
  D_WALL = _b("diorite_wall")
  LANTERN = _b("lantern")
  GRASS = _b("grass_block")
  WATER = _b("water")
  POPPY = _b("poppy")
  DANDY = _b("dandelion")
  CAKE = _b("cake")
  LECTERN = _b("lectern")
  FRAME = _b("item_frame")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  bx, bz, oy = 10, 10, 1
  s = 12  # footprint
  wh = 4

  # Foundation — cobble perimeter, andesite corners, plank patio
  for x in range(bx, bx + s):
    for z in range(bz, bz + s):
      edge = x in (bx, bx + s - 1) or z in (bz, bz + s - 1)
      corner = x in (bx, bx + s - 1) and z in (bz, bz + s - 1)
      if corner:
        _set(v, x, oy, z, P_AND)
      elif edge:
        _set(v, x, oy, z, COBBLE)
      elif bx + 3 <= x <= bx + 8 and bz + 3 <= z <= bz + 8:
        _set(v, x, oy, z, D_PLANKS)  # interior plank
      else:
        _set(v, x, oy, z, AND)

  # Walls
  for y in range(1, wh + 1):
    for x in range(bx, bx + s):
      for z in range(bz, bz + s):
        edge = x in (bx, bx + s - 1) or z in (bz, bz + s - 1)
        if not edge:
          continue
        if y == 1:
          _set(v, x, oy + y, z, P_DIOR)
        elif y < wh:
          mat = BRICK if (x + z + y) % 2 == 0 else QBRICK
          if (x == bx + 5 and z == bz) or (x == bx + 6 and z == bz):
            if y == 2:
              _set(v, x, oy + y, z, GLASS)
            else:
              _set(v, x, oy + y, z, mat)
          else:
            _set(v, x, oy + y, z, mat)
        else:
          _set(v, x, oy + y, z, CHISEL if (x + z) % 2 else QSTAIR)

  # Interior checkered floor
  for x in range(bx + 1, bx + s - 1):
    for z in range(bz + 1, bz + s - 1):
      if v[x, oy + 1, z] == AIR_B:
        _set(v, x, oy + 1, z, AND if (x + z) % 2 else P_AND)

  # Serving counter (north interior wall)
  for x in range(bx + 3, bx + 9):
    _set(v, x, oy + 2, bz + s - 2, PA_SLAB)
  _set(v, bx + 5, oy + 2, bz + s - 3, LECTERN)
  _set(v, bx + 4, oy + 2, bz + s - 3, FRAME)
  _set(v, bx + 6, oy + 2, bz + s - 3, FRAME)
  _set(v, bx + 7, oy + 2, bz + s - 3, CAKE)

  # Entrance birch doors
  _set(v, bx + 5, oy + 1, bz, B_DOOR)
  _set(v, bx + 6, oy + 1, bz, B_DOOR)
  _set(v, bx + 5, oy + 2, bz, B_DOOR)
  _set(v, bx + 6, oy + 2, bz, B_TRAP)
  _set(v, bx + 5, oy + 3, bz, B_TRAP)

  # Stairs to roof (southwest corner)
  for step in range(4):
    _set(v, bx + 1, oy + 1 + step, bz + 1 + step, A_STAIR)

  # Roof terrace
  ry = oy + wh + 1
  for x in range(bx + 1, bx + s - 1):
    for z in range(bz + 1, bz + s - 1):
      _set(v, x, ry, z, A_SLAB if (x + z) % 2 else PA_SLAB)
  # Grass border on terrace
  for x in range(bx + 1, bx + s - 1):
    _set(v, x, ry + 1, bz + 1, GRASS)
    _set(v, x, ry + 1, bz + s - 2, GRASS)
  for z in range(bz + 2, bz + s - 2):
    _set(v, bx + 1, ry + 1, z, GRASS)
    _set(v, bx + s - 2, ry + 1, z, GRASS)
  # Terrace pond
  for x in range(bx + 5, bx + 7):
    for z in range(bz + 5, bz + 7):
      _set(v, x, ry, z, WATER)
      if x in (bx + 5, bx + 6) and z in (bz + 5, bz + 6):
        if x == bx + 5 or z == bz + 5:
          _set(v, x, ry - 1, z, QSTAIR)
  _set(v, bx + 8, ry + 1, bz + 8, D_WALL)
  _set(v, bx + 8, ry + 2, bz + 8, LANTERN)

  # Yellow/white striped awning (south front)
  for i, x in enumerate(range(bx + 2, bx + 10)):
    for z in (bz - 1, bz - 2):
      _set(v, x, oy + 4, z, YELLOW if i % 2 == 0 else WHITE)
      _set(v, x, oy + 3, z, D_FENCE)

  # Outdoor dining tables
  for tx, tz in ((bx + 2, bz - 3), (bx + 6, bz - 3), (bx + 9, bz - 2)):
    _set(v, tx, oy + 1, tz, D_FENCE)
    _set(v, tx, oy + 2, tz, D_PLATE)
    _set(v, tx - 1, oy + 1, tz, D_STAIRS)
    _set(v, tx + 1, oy + 1, tz, D_STAIRS)

  # Planter boxes with flowers
  for px, pz, flower in ((bx - 1, bz + 3, POPPY), (bx + s, bz + 5, DANDY), (bx + 3, bz - 1, POPPY)):
    _set(v, px, oy, pz, GRASS)
    _set(v, px, oy + 1, pz, flower)
    _set(v, px, oy + 1, pz + 1, D_FENCE)

  # Exterior lantern posts
  for lx, lz in ((bx - 1, bz), (bx + s, bz), (bx, bz - 1)):
    _set(v, lx, oy + 1, lz, D_WALL)
    _set(v, lx, oy + 2, lz, LANTERN)

  # Patio fence perimeter
  for x in range(bx, bx + s):
    _set(v, x, oy + 1, bz - 3, D_FENCE)

  return v


def _generate_bite_bee_haven() -> np.ndarray:
  """
  Bee Haven — book dimensions:
    10×7×8 bee-shaped apiary with beehives, campfires, honey floor.
  """
  YELLOW = _b("yellow_concrete")
  BROWN = _b("brown_terracotta")
  GRAY = _b("gray_concrete")
  BLUE = _b("light_blue_concrete_powder")
  COBBLE = _b("cobblestone")
  TRAP = _b("oak_trapdoor")
  DOOR = _b("oak_door")
  HIVE = _b("beehive")
  HONEY = _b("honey_block")
  CAMP = _b("campfire")
  GRASS = _b("grass_block")
  POPPY = _b("poppy")
  DANDY = _b("dandelion")
  B_LOG = _b("birch_log")
  B_LEAVES = _b("birch_leaves")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 12, 1
  length, width = 10, 7  # x × z
  height = 8  # foundation through roof

  # Meadow floor
  for x in range(ox - 2, ox + length + 2):
    for z in range(oz - 2, oz + width + 2):
      _set(v, x, oy - 1, z, GRASS)

  # Foundation (y=oy)
  for x in range(ox, ox + length):
    for z in range(oz, oz + width):
      _set(v, x, oy, z, COBBLE)

  # Walls y=oy+1 through oy+6, roof at oy+7
  for y in range(1, 7):
    wy = oy + y
    for x in range(ox, ox + length):
      for z in range(oz, oz + width):
        edge = x in (ox, ox + length - 1) or z in (oz, oz + width - 1)
        if not edge:
          continue
        if y == 1:
          _set(v, x, wy, z, GRAY)
        elif y < 6:
          # Back wall brown stripes
          if z == oz and x in (ox + 2, ox + 4, ox + 6, ox + 8):
            _set(v, x, wy, z, BROWN)
          else:
            _set(v, x, wy, z, YELLOW)
        else:
          _set(v, x, wy, z, YELLOW)

  # Roof (y=oy+7) — yellow with brown stripes
  roof_y = oy + 7
  for x in range(ox, ox + length):
    for z in range(oz, oz + width):
      stripe = z in (oz + 2, oz + 4)
      _set(v, x, roof_y, z, BROWN if stripe else YELLOW)

  # Oak trapdoors on roof edges
  for x in range(ox + 1, ox + length - 1, 3):
    _set(v, x, roof_y + 1, oz + width - 1, TRAP)

  # Front entrance (+z face) — door and 2×2 eyes
  door_x = ox + length // 2 - 1
  door_z = oz + width - 1
  _set(v, door_x, oy + 1, door_z, DOOR)
  _set(v, door_x + 1, oy + 1, door_z, DOOR)
  _set(v, door_x, oy + 2, door_z, DOOR)
  _set(v, door_x + 1, oy + 2, door_z, DOOR)
  eye_x, eye_y = ox + 2, oy + 4
  for dx in range(2):
    for dy in range(2):
      _set(v, eye_x + dx, eye_y + dy, door_z, BLUE)
      _set(v, ox + length - 3 + dx, eye_y + dy, door_z, BLUE)
  # Trapdoors above eyes
  for ex in (eye_x, ox + length - 3):
    _set(v, ex, eye_y + 2, door_z, TRAP)
    _set(v, ex + 1, eye_y + 2, door_z, TRAP)

  # Side eyes (left and right walls)
  for side_x, facing in ((ox, oz + 3), (ox + length - 1, oz + 3)):
    for dz in range(2):
      for dy in range(2):
        _set(v, side_x, eye_y + dy, facing + dz, BLUE)

  # Hollow interior + honey floor
  for x in range(ox + 1, ox + length - 1):
    for z in range(oz + 1, oz + width - 1):
      for y in range(2, 7):
        _set(v, x, oy + y, z, AIR_B)
      _set(v, x, oy + 1, z, HONEY if (x + z) % 2 else BROWN)

  # Beehives on campfires along back interior wall
  for hx in range(ox + 2, ox + length - 2, 2):
    _set(v, hx, oy + 1, oz + 1, CAMP)
    _set(v, hx, oy + 2, oz + 1, HIVE)

  # Flowers around apiary
  for fx, fz, flower in (
    (ox - 1, oz + 2, POPPY),
    (ox + length, oz + 4, DANDY),
    (ox + 3, oz - 1, POPPY),
    (ox + 7, oz + width, DANDY),
    (ox - 1, oz + width - 1, DANDY),
    (ox + length, oz + 1, POPPY),
  ):
    _set(v, fx, oy, fz, flower)

  # Birch trees
  for tx, tz in ((ox - 2, oz - 1), (ox + length + 1, oz + width)):
    for y in range(oy, oy + 5):
      _set(v, tx, y, tz, B_LOG)
    for dy in range(3, 6):
      for dx in range(-2, 3):
        for dz in range(-2, 3):
          if abs(dx) + abs(dz) < 3:
            _set(v, tx + dx, oy + dy, tz + dz, B_LEAVES)

  return v


def _generate_bite_fishing_shack() -> np.ndarray:
  """
  Fishing Shack — book dimensions:
    15×8 stilt shack over water, hay roof, interior fishing hole and bunks.
  """
  WATER = _b("water")
  COBBLE = _b("cobblestone")
  S_FENCE = _b("spruce_fence")
  S_PLANK = _b("spruce_planks")
  S_SLAB = _b("spruce_slab")
  S_STAIR = _b("spruce_stairs")
  RED = _b("red_concrete")
  WHITE = _b("white_concrete")
  D_PLANK = _b("dark_oak_planks")
  D_DOOR = _b("dark_oak_door")
  GLASS = _b("glass_pane")
  HAY = _b("hay_block")
  AND = _b("andesite")
  A_STAIR = _b("andesite_stairs")
  B_TRAP = _b("birch_trapdoor")
  BED = _b("red_bed")
  SMOKER = _b("smoker")
  O_TRAP = _b("oak_trapdoor")
  LANTERN = _b("lantern")
  BARREL = _b("barrel")
  CHEST = _b("chest")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 11, 2
  length, width = 15, 8
  deck_y = oy + 3

  # Water basin
  for x in range(ox - 1, ox + length + 1):
    for z in range(oz - 3, oz + width + 3):
      _set(v, x, oy - 1, z, WATER)
      _set(v, x, oy - 2, z, WATER)

  # Cobble footings + 3-block spruce stilts (6×3 grid)
  footing_xs = [ox + i for i in (0, 3, 6, 9, 12, 14)]
  footing_zs = [oz + i for i in (1, 4, 7)]
  for fx in footing_xs:
    for fz in footing_zs:
      _set(v, fx, oy - 2, fz, COBBLE)
      for sy in range(3):
        _set(v, fx, oy + sy, fz, S_FENCE)

  # Horizontal fence grid at deck level
  for fx in footing_xs:
    for z in range(oz, oz + width):
      _set(v, fx, deck_y, z, S_FENCE)
  for fz in footing_zs:
    for x in range(ox, ox + length):
      _set(v, x, deck_y, fz, S_FENCE)

  # Deck floor — red border, white corners, dark oak interior
  hole_x, hole_z = ox + 6, oz + 3
  for x in range(ox, ox + length):
    for z in range(oz, oz + width):
      edge = x in (ox, ox + length - 1) or z in (oz, oz + width - 1)
      corner = x in (ox, ox + length - 1) and z in (oz, oz + width - 1)
      if hole_x <= x < hole_x + 2 and hole_z <= z < hole_z + 2:
        _set(v, x, deck_y, z, AIR_B)
      elif corner:
        _set(v, x, deck_y, z, WHITE)
      elif edge:
        _set(v, x, deck_y, z, RED)
      else:
        _set(v, x, deck_y, z, D_PLANK)

  # Walls (4 blocks tall)
  wall_h = 4
  for y in range(1, wall_h + 1):
    wy = deck_y + y
    for x in range(ox, ox + length):
      for z in range(oz, oz + width):
        edge = x in (ox, ox + length - 1) or z in (oz, oz + width - 1)
        if not edge:
          continue
        corner = x in (ox, ox + length - 1) and z in (oz, oz + width - 1)
        if y == wall_h:
          _set(v, x, wy, z, WHITE)
        elif corner:
          _set(v, x, wy, z, WHITE)
        elif z == oz + width - 1 and x == ox + length // 2 and y <= 2:
          _set(v, x, wy, z, AIR_B)  # door opening
        elif y == 2 and ((x in (ox + 3, ox + 11) and z in (oz, oz + width - 1)) or
                         (z in (oz + 2, oz + 5) and x in (ox, ox + length - 1))):
          _set(v, x, wy, z, GLASS)
        else:
          _set(v, x, wy, z, RED)

  # Door
  door_x, door_z = ox + length // 2, oz + width - 1
  _set(v, door_x, deck_y + 1, door_z, D_DOOR)
  _set(v, door_x, deck_y + 2, door_z, D_DOOR)

  # Hollow interior
  for x in range(ox + 1, ox + length - 1):
    for z in range(oz + 1, oz + width - 1):
      for y in range(deck_y + 1, deck_y + wall_h):
        if v[x, y, z] not in (RED, WHITE, GLASS, D_DOOR):
          _set(v, x, y, z, AIR_B)

  # Hay bale A-frame roof + andesite trim
  roof_base = deck_y + wall_h + 1
  for layer in range(3):
    for x in range(ox + layer, ox + length - layer):
      for z in range(oz + layer, oz + width - layer):
        _set(v, x, roof_base + layer, z, HAY)
        if x in (ox + layer, ox + length - 1 - layer) or z in (oz + layer, oz + width - 1 - layer):
          _set(v, x, roof_base + layer, z, A_STAIR)

  # Chimney
  cx, cz = ox + 3, oz + 2
  for y in range(deck_y + 1, roof_base + 3):
    _set(v, cx, y, cz, AND)

  # Balcony deck (south side extension)
  for x in range(ox + 2, ox + length - 2):
    _set(v, x, deck_y, oz - 1, S_PLANK)
    _set(v, x, deck_y + 1, oz - 1, S_FENCE)
  _set(v, ox + 4, deck_y, oz - 1, BARREL)
  _set(v, ox + 10, deck_y, oz - 1, BARREL)

  # Wrap-around stairs to deck
  for step, (sx, sz) in enumerate(((ox - 1, oz - 2), (ox - 1, oz - 1), (ox, oz - 2))):
    _set(v, sx, deck_y - step, sz, S_STAIR)
    if step > 0:
      _set(v, sx, deck_y - step, sz, S_FENCE)

  # Interior furnishings
  # Bunk beds (north end)
  _set(v, ox + 2, deck_y + 1, oz + 1, BED)
  _set(v, ox + 2, deck_y + 2, oz + 1, BED)
  _set(v, ox + 1, deck_y + 1, oz + 1, B_TRAP)
  _set(v, ox + 3, deck_y + 1, oz + 1, B_TRAP)
  _set(v, ox + 1, deck_y + 2, oz + 1, B_TRAP)
  _set(v, ox + 3, deck_y + 2, oz + 1, B_TRAP)

  # Smoker hearth
  _set(v, ox + length - 3, deck_y + 1, oz + 2, SMOKER)
  _set(v, ox + length - 3, deck_y + 1, oz + 3, SMOKER)
  _set(v, ox + length - 2, deck_y + 2, oz + 2, LANTERN)

  # Fishing hole trapdoors
  for dx in range(2):
    for dz in range(2):
      _set(v, hole_x + dx, deck_y, hole_z + dz, O_TRAP)

  _set(v, ox + length - 2, deck_y + 1, oz + width - 2, CHEST)
  _set(v, ox + 5, deck_y + wall_h, oz + 4, LANTERN)

  return v


def _generate_bite_bedrock_train() -> np.ndarray:
  """
  Bedrock Train — book layout (scaled for 32³):
    11×11 embarking station, 4× mine shaft sections (4 layers each),
    disembarking station, twin corkscrew powered railways.
  """
  STONE = _b("stone")
  COBBLE = _b("cobblestone")
  OLOG = _b("oak_log")
  OPLANK = _b("oak_planks")
  OFENCE = _b("oak_fence")
  OTRAP = _b("oak_trapdoor")
  RAIL = _b("rail")
  POWER = _b("powered_rail")
  RTORCH = _b("redstone_torch")
  LANTERN = _b("lantern")
  CHEST = _b("chest")
  FURNACE = _b("furnace")
  CRAFT = _b("crafting_table")
  ANVIL = _b("anvil")
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, size = 10, 10, 11
  cx, cz = ox + size // 2, oz + size // 2

  emb_floor = 22
  shaft_bottom = 6
  dis_floor = 2
  sections = 4

  def _in_box(x: int, z: int) -> bool:
    return ox <= x < ox + size and oz <= z < oz + size

  def _is_wall(x: int, z: int) -> bool:
    return _in_box(x, z) and (x in (ox, ox + size - 1) or z in (oz, oz + size - 1))

  def _wall_mat(x: int, z: int) -> str:
    corner = x in (ox, ox + size - 1) and z in (oz, oz + size - 1)
    if corner:
      return OLOG
    if (x + z) % 4 == 0:
      return COBBLE
    return STONE

  # Surface mound
  for x in range(ox - 1, ox + size + 1):
    for z in range(oz - 1, oz + size + 1):
      _set(v, x, emb_floor + 1, z, GRASS)
      if not _in_box(x, z):
        _set(v, x, emb_floor, z, DIRT)

  # Full vertical shaft cavity + walls
  for y in range(dis_floor, emb_floor + 1):
    for x in range(ox, ox + size):
      for z in range(oz, oz + size):
        if _is_wall(x, z):
          _set(v, x, y, z, _wall_mat(x, z))
        elif y <= emb_floor:
          _set(v, x, y, z, AIR_B)

  # Embarking platform (north half floor, south half open pit)
  for x in range(ox + 1, ox + size - 1):
    for z in range(oz + 1, oz + size // 2):
      _set(v, x, emb_floor, z, OPLANK)
      if (x + z) % 5 == 0:
        _set(v, x, emb_floor - 1, z, OLOG)

  # Entrance gap (south wall, 2 blocks tall)
  door_x = cx
  for dy in (0, 1):
    _set(v, door_x, emb_floor + dy, oz + size - 1, AIR_B)
    _set(v, door_x + 1, emb_floor + dy, oz + size - 1, AIR_B)

  # Embarking station furnishings
  _set(v, ox + 2, emb_floor + 1, oz + 2, CHEST)
  _set(v, ox + 3, emb_floor + 1, oz + 2, CHEST)
  _set(v, ox + size - 3, emb_floor + 1, oz + 2, FURNACE)
  _set(v, ox + size - 4, emb_floor + 1, oz + 2, CRAFT)
  _set(v, ox + 2, emb_floor + 1, oz + 3, ANVIL)
  _set(v, cx, emb_floor + 1, oz + 3, OFENCE)
  _set(v, cx, emb_floor + 2, oz + 3, OTRAP)
  _set(v, ox + 2, emb_floor + 3, oz + 4, LANTERN)
  _set(v, ox + size - 3, emb_floor + 3, oz + 4, LANTERN)

  # Initial rails at embarking entrance
  _set(v, ox + 2, emb_floor, oz + size - 3, COBBLE)
  _set(v, ox + 3, emb_floor, oz + size - 3, COBBLE)
  _set(v, ox + 2, emb_floor, oz + size - 4, POWER)
  _set(v, ox + 3, emb_floor, oz + size - 4, POWER)
  _set(v, ox + 2, emb_floor, oz + size - 5, RAIL)
  _set(v, ox + 3, emb_floor, oz + size - 5, RAIL)
  _set(v, ox + 1, emb_floor, oz + size - 4, RTORCH)

  # Central column through shaft
  for y in range(shaft_bottom, emb_floor):
    _set(v, cx, y, cz, OLOG)

  # Mine shaft sections — tiered rings + corkscrew twin rails
  total_levels = sections * 4
  for level in range(total_levels):
    y = emb_floor - 1 - level
    if y < shaft_bottom:
      break
    layer = level % 4
    inset = 1 + layer

    # Oak plank rings (two concentric)
    for ring_inset in (inset, inset + 1):
      for x in range(ox + ring_inset, ox + size - ring_inset):
        for z in (oz + ring_inset, oz + size - 1 - ring_inset):
          _set(v, x, y, z, OPLANK)
      for z in range(oz + ring_inset, oz + size - ring_inset):
        for x in (ox + ring_inset, ox + size - 1 - ring_inset):
          _set(v, x, y, z, OPLANK)

    # Corkscrew rails — twin tracks on opposite sides, rotate by level
    side = level % 4
    inner = inset + 1
    track_a = [
      (ox + inner, oz + inner),
      (ox + size - 1 - inner, oz + inner),
      (ox + size - 1 - inner, oz + size - 1 - inner),
      (ox + inner, oz + size - 1 - inner),
    ]
    track_b = [
      (ox + inner + 1, oz + inner + 1),
      (ox + size - 2 - inner, oz + inner + 1),
      (ox + size - 2 - inner, oz + size - 2 - inner),
      (ox + inner + 1, oz + size - 2 - inner),
    ]
    ax, az = track_a[side]
    bx, bz = track_b[(side + 2) % 4]
    rail_mat = POWER if layer == 0 else RAIL
    _set(v, ax, y, az, rail_mat)
    _set(v, bx, y, bz, rail_mat)
    if layer == 0:
      _set(v, ax, y - 1, az, POWER)
      _set(v, bx, y - 1, bz, POWER)
      _set(v, ax - 1 if ax > cx else ax + 1, y, az, RTORCH)

    if level % 3 == 0:
      _set(v, ox + 2, y + 1, oz + 2, LANTERN)

  # Disembarking station floor rings at bottom
  for y in range(dis_floor, shaft_bottom + 1):
    inset = max(1, (y - dis_floor) % 3)
    for x in range(ox + inset, ox + size - inset):
      for z in (oz + inset, oz + size - 1 - inset):
        _set(v, x, y, z, OPLANK)
    for z in range(oz + inset, oz + size - inset):
      for x in (ox + inset, ox + size - 1 - inset):
        _set(v, x, y, z, OPLANK)

  # Track terminators + disembarking details
  for tx, tz in ((ox + 2, oz + size - 3), (ox + size - 3, oz + 2)):
    _set(v, tx, shaft_bottom, tz, COBBLE)
    _set(v, tx, shaft_bottom + 1, tz, CHEST)
    _set(v, tx, shaft_bottom + 2, tz, LANTERN)

  # Exit tunnel (south at bottom)
  for x in (cx, cx + 1):
    for z in range(oz + size, oz + size + 2):
      for y in range(dis_floor, shaft_bottom + 2):
        _set(v, x, y, z, AIR_B)
      _set(v, x, dis_floor - 1, z, STONE)

  return v


def _generate_bite_rainbow_stables() -> np.ndarray:
  """
  Rainbow Stables — book dimensions:
    16×16 horse barn, pink/purpur/birch, three stalls, rainbow corner patch.
  """
  COBBLE = _b("cobblestone")
  C_STAIR = _b("cobblestone_stairs")
  GRASS = _b("grass_block")
  RED = _b("red_concrete")
  ORANGE = _b("orange_concrete")
  YELLOW = _b("yellow_concrete")
  LIME = _b("lime_concrete")
  LBLUE = _b("light_blue_concrete")
  PURPLE = _b("purple_concrete")
  PINK = _b("pink_concrete")
  PURPUR = _b("purpur_block")
  BPLANK = _b("birch_planks")
  BFENCE = _b("birch_fence")
  BGATE = _b("birch_fence_gate")
  BTRAP = _b("birch_trapdoor")
  BPLATE = _b("birch_pressure_plate")
  HAY = _b("hay_block")
  QSTAIR = _b("quartz_stairs")
  PSTAIR = _b("purpur_stairs")
  PSLAB = _b("purpur_slab")
  CAULDRON = _b("cauldron")
  WATER = _b("water")
  LEAVES = _b("jungle_leaves")
  POPPY = _b("poppy")
  DANDY = _b("dandelion")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 8, 1
  s = 16
  wall_h = 4
  floor_y = oy

  # Ground extend
  for x in range(ox - 1, ox + s + 3):
    for z in range(oz - 1, oz + s + 3):
      if v[x, oy - 1, z] == AIR_B:
        _set(v, x, oy - 1, z, GRASS)

  # Step 1 — foundation
  rainbow = (RED, ORANGE, YELLOW, LIME, LBLUE, PURPLE)
  for x in range(ox, ox + s):
    for z in range(oz, oz + s):
      edge = x in (ox, ox + s - 1) or z in (oz, oz + s - 1)
      if edge:
        _set(v, x, floor_y, z, COBBLE)
      else:
        _set(v, x, floor_y, z, GRASS)
  # Rainbow 3×3 corner patch (northwest)
  for i, (dx, dz) in enumerate(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2))):
    if i < len(rainbow):
      _set(v, ox + 1 + dx, floor_y, oz + 1 + dz, rainbow[i % len(rainbow)])

  # Stall partition x positions (3 stalls along x)
  stall_xs = (ox + 4, ox + 8, ox + 12)

  # Steps 2-3 — walls: purpur pillars + birch planks, stall fences
  for y in range(1, 3):
    wy = floor_y + y
    for x in range(ox, ox + s):
      for z in range(oz, oz + s):
        edge = x in (ox, ox + s - 1) or z in (oz, oz + s - 1)
        partition = x in stall_xs and oz + 3 <= z <= oz + s - 4
        if not edge and not partition:
          continue
        pillar = (x in (ox, ox + s - 1) and z in (oz, oz + s - 1)) or x in stall_xs
        if pillar:
          _set(v, x, wy, z, PURPUR)
        else:
          _set(v, x, wy, z, BPLANK)

  # Stall front fences (south side, z = oz + s - 4 area)
  fence_z = oz + s - 5
  for x in range(ox + 2, ox + s - 2):
    if x in stall_xs:
      _set(v, x, floor_y + 1, fence_z, BGATE)
      _set(v, x, floor_y + 2, fence_z, BFENCE)
    elif (x - ox) % 4 == 0:
      _set(v, x, floor_y + 1, fence_z, BFENCE)

  # Hay bales in stalls
  for sx in (ox + 2, ox + 6, ox + 10):
    for hz in range(oz + 2, oz + 5):
      _set(v, sx, floor_y + 1, hz, HAY)
  _set(v, ox + 14, floor_y + 1, oz + 3, CAULDRON)

  # Steps 4-6 — pink concrete pillars and roof frame
  for y in range(3, wall_h + 1):
    wy = floor_y + y
    for x in range(ox, ox + s):
      for z in range(oz, oz + s):
        edge = x in (ox, ox + s - 1) or z in (oz, oz + s - 1)
        partition = x in stall_xs and oz + 2 <= z <= oz + s - 3
        if edge or partition:
          _set(v, x, wy, z, PINK)

  # Roof frame + trapdoors
  roof_y = floor_y + wall_h + 1
  for x in range(ox, ox + s):
    for z in range(oz, oz + s):
      edge = x in (ox, ox + s - 1) or z in (oz, oz + s - 1)
      if edge:
        _set(v, x, roof_y, z, PINK)
        _set(v, x, roof_y + 1, z, BTRAP)

  # Steps 7-8 — gabled purpur/quartz roof
  for layer in range(3):
    ry = roof_y + 1 + layer
    for x in range(ox + layer, ox + s - layer):
      for z in range(oz + layer, oz + s - layer):
        edge = x in (ox + layer, ox + s - 1 - layer) or z in (oz + layer, oz + s - 1 - layer)
        if edge:
          _set(v, x, ry, z, QSTAIR if layer == 0 else PSTAIR)
        else:
          _set(v, x, ry, z, PSLAB if layer < 2 else PURPUR)

  # Hollow interior above floor
  for x in range(ox + 1, ox + s - 1):
    for z in range(oz + 1, oz + s - 1):
      for y in range(floor_y + 1, roof_y):
        if v[x, y, z] in (GRASS, AIR_B):
          _set(v, x, y, z, AIR_B)

  # Step 9 — outdoor yard details
  # Colorful carpet patchwork in front (south)
  carpets = (PINK, RED, YELLOW, LBLUE, PURPLE, ORANGE)
  for i in range(6):
    for j in range(3):
      _set(v, ox + 2 + j, floor_y, oz + s + i % 3, carpets[(i + j) % len(carpets)])

  # Outdoor water trough
  for tx in range(ox + 6, ox + 9):
    _set(v, tx, floor_y, oz + s + 1, C_STAIR)
    _set(v, tx, floor_y, oz + s + 2, WATER)

  # Fence perimeter with leaves
  for x in range(ox, ox + s, 4):
    _set(v, x, floor_y + 1, oz + s + 2, BFENCE)
    _set(v, x, floor_y + 2, oz + s + 2, LEAVES)
    _set(v, x, floor_y + 1, oz + s + 3, BPLATE)

  # Flowers
  for fx, fz, flower in ((ox - 1, oz + 4, POPPY), (ox + s, oz + 8, DANDY), (ox + 5, oz + s + 3, POPPY)):
    _set(v, fx, floor_y, fz, flower)

  return v


def _generate_bite_marketplace_stall() -> np.ndarray:
  """
  Marketplace Stall — book dimensions:
    7×5 vendor stall, striped awning, lectern counter, banner curtains.
  """
  COBBLE = _b("cobblestone")
  LECTERN = _b("lectern")
  D_SLAB = _b("dark_oak_slab")
  BARREL = _b("barrel")
  DSIGN = _b("dark_oak_sign")
  P_AND = _b("polished_andesite")
  A_WALL = _b("andesite_wall")
  GREEN = _b("green_concrete")
  WHITE = _b("white_concrete")
  D_TRAP = _b("dark_oak_trapdoor")
  LANTERN = _b("lantern")
  CHAIN = _b("chain")
  BANNER = _b("green_banner")
  CHEST = _b("chest")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 13, 1
  w, d = 7, 5
  floor_y = oy

  # Grass surround
  for x in range(ox - 2, ox + w + 2):
    for z in range(oz - 2, oz + d + 2):
      _set(v, x, oy - 1, z, GRASS)

  # Cobblestone floor
  for x in range(ox, ox + w):
    for z in range(oz, oz + d):
      _set(v, x, floor_y, z, COBBLE)

  # Barrels at corners and back
  for bx, bz in ((ox, oz), (ox + w - 1, oz), (ox, oz + d - 1), (ox + w - 1, oz + d - 1),
                 (ox + w // 2, oz)):
    _set(v, bx, floor_y + 1, bz, BARREL)
    _set(v, bx, floor_y + 2, bz, DSIGN)

  # Counter — lecterns front, slabs on top, chest behind
  for x in range(ox + 1, ox + w - 1):
    _set(v, x, floor_y + 1, oz + d - 1, LECTERN)
    _set(v, x, floor_y + 2, oz + d - 1, D_SLAB)
  _set(v, ox + w // 2, floor_y + 1, oz + 1, CHEST)

  # Pillars — polished andesite base + andesite wall
  pillars = ((ox, oz), (ox + w - 1, oz), (ox, oz + d - 1), (ox + w - 1, oz + d - 1))
  for px, pz in pillars:
    _set(v, px, floor_y + 1, pz, P_AND)
    for y in range(2, 5):
      _set(v, px, floor_y + y, pz, A_WALL)

  # Green/white striped awning with overhang
  roof_y = floor_y + 5
  for x in range(ox - 1, ox + w + 1):
    for z in range(oz - 1, oz + d + 1):
      stripe = GREEN if (x + z) % 2 == 0 else WHITE
      _set(v, x, roof_y, z, stripe)
      if z == oz + d:
        _set(v, x, roof_y - 1, z, D_TRAP)
        _set(v, x, roof_y - 2, z, LANTERN)

  # Chain + banner curtains on back wall
  back_z = oz
  for x in range(ox + 1, ox + w - 1, 2):
    for y in range(floor_y + 3, floor_y + 5):
      _set(v, x, y, back_z, CHAIN)
    for y in range(floor_y + 2, floor_y + 5):
      _set(v, x + 1, y, back_z, BANNER)

  return v


def _generate_bite_floor_is_lava() -> np.ndarray:
  """
  Floor Is Lava — book dimensions (scaled for 32³):
    7×24 parkour corridor, 3 tiered sections, lava floor, three obstacles.
  """
  DIRT = _b("dirt")
  COBBLE = _b("cobblestone")
  STONE = _b("stone")
  CHISEL = _b("chiseled_polished_blackstone")
  BASALT = _b("basalt")
  PWALL = _b("prismarine_wall")
  LAVA = _b("lava")
  GOLD = _b("gold_block")
  HONEY = _b("honey_block")
  SLAB = _b("stone_slab")
  TARGET = _b("target")
  PISTON = _b("sticky_piston")
  REDSTONE = _b("redstone_dust")
  CHAIN = _b("chain")
  CTRAP = _b("crimson_trapdoor")
  SLANTERN = _b("soul_lantern")
  CHEST = _b("chest")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 4, 1
  w, length = 7, 24
  sec_len = 8

  def _section(z: int) -> int:
    return min(2, (z - oz) // sec_len)

  def _wall_h(sec: int) -> int:
    return 3 + sec * 2

  # Foundation
  for x in range(ox, ox + w):
    for z in range(oz, oz + length):
      _set(v, x, oy - 1, z, DIRT if (x + z) % 3 else COBBLE)

  # Tiered walls per section
  for z in range(oz, oz + length):
    sec = _section(z)
    wh = _wall_h(sec)
    for y in range(oy, oy + wh):
      for x in (ox, ox + w - 1):
        corner = y == oy or y == oy + wh - 1
        if corner or x == ox:
          mat = CHISEL if y in (oy, oy + wh - 1) else BASALT if y == oy + 1 else STONE
        else:
          mat = PWALL if y > oy else STONE
        _set(v, x, y, z, mat)
    for x in range(ox + 1, ox + w - 1):
      for y in range(oy, oy + wh):
        if y == oy + wh - 1 or x in (ox + 1, ox + w - 2):
          _set(v, x, y, oz, CHISEL if y == oy else PWALL if y > oy else STONE)
          _set(v, x, y, oz + length - 1, CHISEL if y == oy else PWALL if y > oy else STONE)

  # Lava floor + gold platforms
  for z in range(oz + 1, oz + length - 1):
    for x in range(ox + 1, ox + w - 1):
      _set(v, x, oy, z, LAVA)
  for px, pz in ((ox + 2, oz + 2), (ox + 4, oz + 6), (ox + 3, oz + 10),
                 (ox + 2, oz + 14), (ox + 4, oz + 18), (ox + 3, oz + 22)):
    _set(v, px, oy, pz, GOLD)
    _set(v, px, oy + 1, pz, GOLD)

  # Ceiling lanterns per section
  for sec in range(3):
    cz = oz + sec * sec_len + sec_len // 2
    for x in range(ox + 1, ox + w - 1, 2):
      hy = oy + _wall_h(sec)
      _set(v, x, hy, cz, CTRAP)
      _set(v, x, hy - 1, cz, SLANTERN)

  # Start chest
  _set(v, ox + 3, oy + 1, oz + 1, CHEST)

  # Obstacle 1 — honey wall + slabs (section 0)
  z1 = oz + 3
  for y in range(oy + 2, oy + 5):
    _set(v, ox + 1, y, z1, HONEY)
  for i, (sx, sy) in enumerate(((2, 2), (3, 3), (4, 4), (3, 5))):
    _set(v, ox + sx, oy + sy, z1 + i, SLAB)

  # Obstacle 2 — target + pistons (section 1)
  z2 = oz + 11
  _set(v, ox + 3, oy + 2, z2, TARGET)
  _set(v, ox + 3, oy + 1, z2, REDSTONE)
  for px in (ox + 2, ox + 4):
    _set(v, px, oy - 1, z2, PISTON)
    _set(v, px, oy, z2, STONE)

  # Obstacle 3 — floor honey + chain tightrope (section 2)
  z3 = oz + 18
  for dx in range(2):
    for dz in range(2):
      _set(v, ox + 2 + dx, oy, z3 + dz, HONEY)
  chain_y = oy + _wall_h(2) - 1
  for x in range(ox + 1, ox + w - 1):
    _set(v, x, chain_y, z3, CHAIN)

  # Finish platform
  for x in range(ox + 1, ox + w - 1):
    for z in range(oz + length - 2, oz + length):
      _set(v, x, oy, z, GOLD)

  return v


def _generate_bite_overworld_showroom() -> np.ndarray:
  """
  Overworld Showroom — book dimensions:
    14×14×5 underground gallery, blackstone arches, quartz trophy pedestals.
  """
  STONE = _b("stone")
  COBBLE = _b("cobblestone")
  GRANITE = _b("granite")
  PGRAN = _b("polished_granite")
  PB_BRICK = _b("polished_blackstone_bricks")
  PB_STAIR = _b("polished_blackstone_stairs")
  PB_SLAB = _b("polished_blackstone_slab")
  CHISEL = _b("chiseled_polished_blackstone")
  QPILLAR = _b("quartz_pillar")
  DWALL = _b("diorite_wall")
  GLOW = _b("glowstone")
  I_DOOR = _b("iron_door")
  BUTTON = _b("stone_button")
  LANTERN = _b("lantern")
  LECTERN = _b("lectern")
  EFRAME = _b("end_portal_frame")
  ECRYSTAL = _b("end_crystal")
  BEACON = _b("beacon")
  PRISM = _b("prismarine")
  JACK = _b("jack_o_lantern")
  EMERALD = _b("emerald_block")
  CARPET = _b("red_carpet")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 9, 1
  s = 14
  room_h = 5
  floor_y = oy

  floor_mats = (STONE, COBBLE, GRANITE, PGRAN)
  for x in range(ox, ox + s):
    for z in range(oz, oz + s):
      _set(v, x, floor_y, z, floor_mats[(x + z) % len(floor_mats)])

  # Outer stone walls
  for y in range(floor_y, floor_y + room_h + 1):
    for x in range(ox, ox + s):
      for z in range(oz, oz + s):
        edge = x in (ox, ox + s - 1) or z in (oz, oz + s - 1)
        if edge and y > floor_y:
          _set(v, x, y, z, STONE if y < floor_y + room_h else CHISEL)

  # Entrance staircase (southwest corner)
  for step in range(4):
    _set(v, ox - 1, floor_y + step, oz + step, STONE if step % 2 else PB_STAIR)
  _set(v, ox, floor_y + 1, oz, I_DOOR)
  _set(v, ox, floor_y + 2, oz, I_DOOR)
  _set(v, ox - 1, floor_y + 2, oz, BUTTON)

  # 4×4 pillar grid
  pillar_coords = []
  for i in range(4):
    for j in range(4):
      px = ox + 2 + i * 3
      pz = oz + 2 + j * 3
      pillar_coords.append((px, pz))
      for y in range(1, 4):
        _set(v, px, floor_y + y, pz, PB_BRICK)
      _set(v, px, floor_y, pz, GLOW)
      _set(v, px + 1, floor_y + 1, pz, DWALL)
      _set(v, px, floor_y + 1, pz + 1, DWALL)

  # Arches between adjacent pillars (rows)
  for i in range(4):
    for j in range(3):
      x1 = ox + 2 + i * 3
      x2 = x1 + 3
      z = oz + 2 + j * 3
      mid_x = x1 + 1
      _set(v, mid_x, floor_y + 4, z, PB_SLAB)
      _set(v, x1, floor_y + 4, z, PB_STAIR)
      _set(v, x2, floor_y + 4, z, PB_STAIR)
      _set(v, mid_x, floor_y + 3, z, LANTERN)
    for i in range(3):
      for j in range(4):
        z1 = oz + 2 + j * 3
        z2 = z1 + 3
        x = ox + 2 + i * 3
        mid_z = z1 + 1
        _set(v, x, floor_y + 4, mid_z, PB_SLAB)
        _set(v, x, floor_y + 4, z1, PB_STAIR)
        _set(v, x, floor_y + 4, z2, PB_STAIR)

  # Quartz display pedestals between pillars
  for i in range(3):
    for j in range(3):
      qx = ox + 3 + i * 3
      qz = oz + 3 + j * 3
      _set(v, qx, floor_y + 1, qz, QPILLAR)
      _set(v, qx, floor_y + 2, qz, QPILLAR)

  # Trophy displays
  _set(v, ox + 6, floor_y + 1, oz + 6, EFRAME)
  _set(v, ox + 6, floor_y + 2, oz + 6, ECRYSTAL)
  _set(v, ox + 9, floor_y + 1, oz + 9, PRISM)
  _set(v, ox + 9, floor_y + 2, oz + 9, BEACON)
  _set(v, ox + 3, floor_y + 1, oz + 9, PGRAN)
  _set(v, ox + 3, floor_y + 1, oz + 10, CARPET)
  _set(v, ox + 3, floor_y + 2, oz + 9, LECTERN)
  _set(v, ox + 9, floor_y + 2, oz + 3, JACK)
  _set(v, ox + 6, floor_y + 3, oz + 9, EMERALD)

  # Hollow interior
  for x in range(ox + 1, ox + s - 1):
    for z in range(oz + 1, oz + s - 1):
      for y in range(floor_y + 1, floor_y + room_h):
        if v[x, y, z] in (AIR_B, STONE, COBBLE, GRANITE, PGRAN):
          _set(v, x, y, z, AIR_B)

  return v


def _generate_bite_hanging_home() -> np.ndarray:
  """
  Hanging Home — jungle platform suspended by chain/grindstone from stone ceiling.
  """
  STONE = _b("stone")
  CHAIN = _b("chain")
  GRIND = _b("grindstone")
  JLOG = _b("jungle_log")
  JPLANK = _b("jungle_planks")
  JSLAB = _b("jungle_slab")
  JSTAIR = _b("jungle_stairs")
  JTRAP = _b("jungle_trapdoor")
  JFENCE = _b("jungle_fence")
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  BAMBOO = _b("bamboo")
  VINE = _b("vine")
  LEAVES = _b("jungle_leaves")
  ENCH = _b("enchanting_table")
  BOOK = _b("bookshelf")
  BED = _b("red_bed")
  BANNER = _b("white_banner")
  FURNACE = _b("furnace")
  CHEST = _b("chest")
  YCARPET = _b("yellow_carpet")
  LCARPET = _b("lime_carpet")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz = 16, 16
  plat_y = 12
  frame_y = plat_y + 4

  # Stone ceiling anchor + chain
  _set(v, cx, 27, cz, STONE)
  for y, mat in ((26, GRIND), (25, CHAIN), (24, GRIND), (23, CHAIN), (22, GRIND), (21, CHAIN)):
    _set(v, cx, y, cz, mat)

  # 3×3 plank hanging base
  for dx in range(-1, 2):
    for dz in range(-1, 2):
      _set(v, cx + dx, 20, cz + dz, JPLANK)
      _set(v, cx + dx, 19, cz + dz, JSLAB)

  # 5×5 log frame + protruding beams
  for dx in range(-2, 3):
    for dz in range(-2, 3):
      edge = abs(dx) == 2 or abs(dz) == 2
      if edge:
        _set(v, cx + dx, frame_y, cz + dz, JLOG)
        _set(v, cx + dx, frame_y + 1, cz + dz, JFENCE)
  for d in (-3, 3):
    _set(v, cx + d, frame_y, cz, JLOG)
    _set(v, cx, frame_y, cz + d, JLOG)

  # Corner pillars down to platform
  for dx, dz in ((-2, -2), (-2, 2), (2, -2), (2, 2)):
    for y in range(plat_y + 1, frame_y):
      _set(v, cx + dx, y, cz + dz, JLOG)

  # Platform floor
  for dx in range(-3, 4):
    for dz in range(-3, 4):
      if abs(dx) == 3 or abs(dz) == 3:
        _set(v, cx + dx, plat_y, cz + dz, JSLAB if (dx + dz) % 2 else GRASS)
      else:
        _set(v, cx + dx, plat_y, cz + dz, JPLANK)

  # Roof grass fill + leaves
  for dx in range(-2, 3):
    for dz in range(-2, 3):
      if abs(dx) < 2 and abs(dz) < 2:
        _set(v, cx + dx, frame_y + 1, cz + dz, GRASS)
      _set(v, cx + dx, frame_y + 2, cz + dz, LEAVES)

  # Roof sides — stairs trapdoors
  for dx in range(-2, 3):
    _set(v, cx + dx, frame_y, cz - 3, JSTAIR)
    _set(v, cx + dx, frame_y, cz + 3, JTRAP)
  for dz in range(-2, 3):
    _set(v, cx - 3, frame_y, cz + dz, JSTAIR)
    _set(v, cx + 3, frame_y, cz + dz, JTRAP)

  # Bamboo corners
  for dx, dz in ((-3, -3), (-3, 3), (3, -3), (3, 3)):
    _set(v, cx + dx, plat_y, cz + dz, DIRT)
    _set(v, cx + dx, plat_y + 1, cz + dz, BAMBOO)
    _set(v, cx + dx, plat_y + 2, cz + dz, BAMBOO)
    _set(v, cx + dx, plat_y + 3, cz + dz, JTRAP)

  # Vines on underside and sides
  for dx in range(-3, 4):
    for y in range(plat_y - 3, plat_y):
      _set(v, cx + dx, y, cz - 3, VINE)
      _set(v, cx + dx, y, cz + 3, VINE)
  for dz in range(-3, 4):
    for y in range(plat_y - 2, plat_y + 1):
      _set(v, cx - 3, y, cz + dz, VINE)
      _set(v, cx + 3, y, cz + dz, VINE)

  # Trapdoor entrance + vine ladder
  _set(v, cx, plat_y, cz + 2, JTRAP)
  for y in range(plat_y - 4, plat_y):
    _set(v, cx, y, cz + 2, VINE)

  # Interior furnishings
  _set(v, cx, plat_y + 1, cz, ENCH)
  for bx, bz in ((-2, -1), (-2, 0), (-2, 1), (-1, -2), (0, -2), (1, -2),
                 (2, -1), (2, 0), (2, 1), (-1, 2), (0, 2), (1, 2)):
    _set(v, cx + bx, plat_y + 1, cz + bz, BOOK)
    if abs(bx) + abs(bz) == 2:
      _set(v, cx + bx, plat_y + 2, cz + bz, BOOK)

  _set(v, cx - 2, plat_y + 1, cz + 2, BED)
  _set(v, cx - 2, plat_y + 2, cz + 1, BANNER)
  _set(v, cx - 2, plat_y + 2, cz + 2, CHAIN)

  _set(v, cx + 2, plat_y + 1, cz - 1, FURNACE)
  _set(v, cx + 2, plat_y + 1, cz, FURNACE)
  _set(v, cx + 2, plat_y + 1, cz + 1, CHEST)

  _set(v, cx - 1, plat_y + 1, cz - 1, BAMBOO)
  _set(v, cx, plat_y + 1, cz - 1, YCARPET)
  _set(v, cx + 1, plat_y + 1, cz - 1, LCARPET)
  _set(v, cx - 1, plat_y + 1, cz - 2, BAMBOO)
  _set(v, cx + 1, plat_y + 1, cz - 2, BAMBOO)

  # Chain railings
  for dx in range(-3, 4):
    _set(v, cx + dx, plat_y + 2, cz - 3, CHAIN)
    _set(v, cx + dx, plat_y + 2, cz + 3, CHAIN)
  for dz in range(-2, 3):
    _set(v, cx - 3, plat_y + 2, cz + dz, CHAIN)
    _set(v, cx + 3, plat_y + 2, cz + dz, CHAIN)

  return v


def _generate_bite_trader_sleigh() -> np.ndarray:
  """
  Trader Sleigh — book dimensions:
    10×4 mobile trading cabin on spruce runners with anvil mounts.
  """
  SLOG = _b("spruce_log")
  SPLANK = _b("spruce_planks")
  SSLAB = _b("spruce_slab")
  SSTAIR = _b("spruce_stairs")
  D_SLAB = _b("dark_oak_slab")
  BLUE = _b("blue_wool")
  OTRAP = _b("oak_trapdoor")
  BARREL = _b("barrel")
  ANVIL = _b("anvil")
  SDOOR = _b("spruce_door")
  BED = _b("red_bed")
  CRAFT = _b("crafting_table")
  LANTERN = _b("lantern")
  SFENCE = _b("spruce_fence")
  ASTAIR = _b("acacia_stairs")
  SNOW = _b("snow_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 14, 1
  length, width = 10, 4
  cabin_x, cabin_z = ox + 2, oz
  cabin_w, cabin_d = 6, 4
  floor_y = oy

  # Snow ground
  for x in range(ox - 1, ox + length + 1):
    for z in range(oz - 1, oz + width + 1):
      _set(v, x, oy - 1, z, SNOW)

  # Runners (two parallel skids)
  for z in (oz, oz + width - 1):
    for x in range(ox, ox + length):
      if x in (ox, ox + length - 1):
        _set(v, x, floor_y, z, SSTAIR)
      else:
        _set(v, x, floor_y, z, D_SLAB)
  _set(v, ox, floor_y, oz + 1, SSLAB)
  _set(v, ox + length - 1, floor_y, oz + 2, SSLAB)

  # Anvil chassis mounts
  for ax in (cabin_x, cabin_x + cabin_w - 1):
    for az in (cabin_z + 1, cabin_z + cabin_d - 2):
      _set(v, ax, floor_y + 1, az, ANVIL)

  # Cabin floor
  for x in range(cabin_x, cabin_x + cabin_w):
    for z in range(cabin_z, cabin_z + cabin_d):
      _set(v, x, floor_y + 1, z, SSLAB)

  # Walls — spruce log corners, barrel+trapdoor sides, blue wool top
  wall_h = 4
  for y in range(2, 2 + wall_h):
    wy = floor_y + y
    for x in range(cabin_x, cabin_x + cabin_w):
      for z in range(cabin_z, cabin_z + cabin_d):
        edge = x in (cabin_x, cabin_x + cabin_w - 1) or z in (cabin_z, cabin_z + cabin_d - 1)
        if not edge:
          continue
        corner = x in (cabin_x, cabin_x + cabin_w - 1) and z in (cabin_z, cabin_z + cabin_d - 1)
        if corner:
          _set(v, x, wy, z, SLOG)
        elif y < wall_h:
          _set(v, x, wy, z, BARREL if y == 2 else OTRAP)
        else:
          _set(v, x, wy, z, BLUE)

  # Door (south side)
  door_x = cabin_x + cabin_w // 2
  door_z = cabin_z + cabin_d - 1
  _set(v, door_x, floor_y + 2, door_z, SDOOR)
  _set(v, door_x, floor_y + 3, door_z, SDOOR)

  # Interior
  _set(v, cabin_x + 1, floor_y + 2, cabin_z + 1, BED)
  _set(v, cabin_x + 4, floor_y + 2, cabin_z + 1, CRAFT)
  _set(v, cabin_x + cabin_w - 1, floor_y + 3, cabin_z + 2, LANTERN)

  # Hollow cabin
  for x in range(cabin_x + 1, cabin_x + cabin_w - 1):
    for z in range(cabin_z + 1, cabin_z + cabin_d - 1):
      for y in range(floor_y + 2, floor_y + wall_h):
        if v[x, y, z] in (AIR_B, SSLAB):
          _set(v, x, y, z, AIR_B)

  # Front hitch + driver seat
  for z in range(cabin_z, cabin_z + cabin_d):
    _set(v, ox, floor_y + 2, z, SFENCE)
    _set(v, ox, floor_y + 3, z, SFENCE)
  _set(v, ox + 1, floor_y + 2, cabin_z + 1, ASTAIR)

  return v


def _generate_bite_space_rocket() -> np.ndarray:
  """
  Space Rocket — book dimensions:
    5×5 footprint, ~18 blocks tall, 3 interior floors, landing fins.
  """
  CAULDRON = _b("cauldron")
  IRON = _b("iron_block")
  ITRAP = _b("iron_trapdoor")
  LADDER = _b("ladder")
  GRAY = _b("gray_concrete")
  ORANGE = _b("orange_concrete")
  GLASS = _b("black_stained_glass")
  SLAB = _b("smooth_stone_slab")
  BARS = _b("iron_bars")
  BUTTON = _b("stone_button")
  FURNACE = _b("furnace")
  CHEST = _b("chest")
  BED = _b("red_bed")
  CARTO = _b("cartography_table")
  SAND = _b("sand")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz = 16, 16
  oy = 1
  r = 2  # half-width of 5×5

  # Desert pad
  for x in range(cx - 4, cx + 5):
    for z in range(cz - 4, cz + 5):
      _set(v, x, oy - 1, z, SAND)

  # Cauldron feet at corners
  for dx, dz in ((-r, -r), (-r, r), (r, -r), (r, r)):
    _set(v, cx + dx, oy, cz + dz, CAULDRON)

  # Iron cross base + trapdoor hatch
  for dx in range(-r, r + 1):
    _set(v, cx + dx, oy + 1, cz, IRON)
    _set(v, cx, oy + 1, cz + dx, IRON)
  _set(v, cx, oy + 1, cz, ITRAP)
  _set(v, cx + r, oy + 1, cz, LADDER)
  _set(v, cx + r + 1, oy + 2, cz, BUTTON)

  # Hull rings — y=2..14
  for y in range(2, 15):
    wy = oy + y
    ring_mat = GRAY if y == 2 else ORANGE if y < 12 else IRON if y % 2 == 0 else GRAY
    if 3 <= y <= 8:
      ring_mat = ORANGE
    elif 9 <= y <= 11:
      ring_mat = IRON if y % 2 == 0 else ORANGE

    for dx in range(-r, r + 1):
      for dz in range(-r, r + 1):
        edge = abs(dx) == r or abs(dz) == r
        if not edge:
          continue
        if y in (5, 6, 8) and abs(dx) == r and dz == 0:
          _set(v, cx + dx, wy, cz + dz, GLASS)
        else:
          _set(v, cx + dx, wy, cz + dz, ring_mat)

  # Nose cone taper y=15..18
  for layer, inset in enumerate((0, 1, 2, 3)):
    wy = oy + 15 + layer
    for dx in range(-r + inset, r - inset + 1):
      for dz in range(-r + inset, r - inset + 1):
        if abs(dx) == r - inset or abs(dz) == r - inset or (inset >= 2 and dx == 0 and dz == 0):
          mat = IRON if layer % 2 == 0 else GRAY
          if inset == 3:
            mat = IRON
          _set(v, cx + dx, wy, cz + dz, mat)

  # Interior floors + hollow
  for floor_y in (oy + 3, oy + 7, oy + 11):
    for dx in range(-1, 2):
      for dz in range(-1, 2):
        _set(v, cx + dx, floor_y, cz + dz, SLAB)
  for y in range(oy + 2, oy + 15):
    for dx in range(-1, 2):
      for dz in range(-1, 2):
        if v[cx + dx, y, cz + dz] == AIR_B:
          _set(v, cx + dx, y, cz + dz, AIR_B)
  for y in range(oy + 2, oy + 12):
    _set(v, cx + r - 1, y, cz, LADDER)

  # Interior furnishings
  _set(v, cx - 1, oy + 4, cz - 1, FURNACE)
  _set(v, cx + 1, oy + 4, cz - 1, CHEST)
  _set(v, cx, oy + 8, cz, BED)
  _set(v, cx - 1, oy + 8, cz + 1, CARTO)
  _set(v, cx, oy + 3, cz, BUTTON)

  # Landing leg fins
  for dx, dz in ((-3, 0), (3, 0), (0, -3), (0, 3)):
    for y in range(oy, oy + 3):
      _set(v, cx + dx, y, cz + dz, GRAY if y < 2 else IRON)
    _set(v, cx + dx, oy + 1, cz + dz, BARS)
    _set(v, cx + dx, oy, cz + dz, BUTTON)

  # Shoulder trapdoors
  for dx, dz in ((-r, -r), (-r, r), (r, -r), (r, r)):
    _set(v, cx + dx, oy + 12, cz + dz, ITRAP)

  return v


def _generate_bite_jungle_shrine() -> np.ndarray:
  """
  Jungle Shrine — book dimensions:
    12×13 tiered pyramid, central pool, vine shaft, roof arch.
  """
  SBRICK = _b("stone_bricks")
  MOSSY = _b("mossy_stone_bricks")
  COBBLE = _b("cobblestone")
  CHISEL = _b("chiseled_stone_bricks")
  M_STAIR = _b("mossy_stone_brick_stairs")
  A_STAIR = _b("polished_andesite_stairs")
  A_SLAB = _b("polished_andesite_slab")
  CWALL = _b("cobblestone_wall")
  JGATE = _b("jungle_fence_gate")
  WATER = _b("water")
  CAMP = _b("campfire")
  LANTERN = _b("lantern")
  VINE = _b("vine")
  LEAVES = _b("jungle_leaves")
  BARREL = _b("barrel")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 9, 1
  w, d = 12, 13
  cx, cz = ox + w // 2, oz + d // 2

  # Jungle ground
  for x in range(ox - 2, ox + w + 2):
    for z in range(oz - 2, oz + d + 2):
      _set(v, x, oy - 1, z, GRASS)

  mats = (SBRICK, MOSSY, COBBLE, CHISEL)

  # Base floor + 3×3 water pool
  for x in range(ox, ox + w):
    for z in range(oz, oz + d):
      if abs(x - cx) <= 1 and abs(z - cz) <= 1:
        _set(v, x, oy, z, WATER)
      else:
        _set(v, x, oy, z, mats[(x + z) % len(mats)])
  # Entrance step bump (south)
  for x in range(cx - 1, cx + 2):
    _set(v, x, oy, oz + d, SBRICK)
    _set(v, x, oy + 1, oz + d, M_STAIR)

  # Corner pillars on base
  for px, pz in ((ox, oz), (ox + w - 1, oz), (ox, oz + d - 1), (ox + w - 1, oz + d - 1)):
    _set(v, px, oy + 1, pz, CHISEL)

  # Tiered walls — 5 layers inset
  for tier in range(1, 6):
    inset = tier
    wy = oy + tier
    if inset >= w // 2 or inset >= d // 2:
      break
    for x in range(ox + inset, ox + w - inset):
      for z in range(oz + inset, oz + d - inset):
        edge = x in (ox + inset, ox + w - 1 - inset) or z in (oz + inset, oz + d - 1 - inset)
        if not edge:
          continue
        # Leave 2×2 center gap on top tier
        if tier >= 4 and abs(x - cx) <= 0 and abs(z - cz) <= 0:
          continue
        mat = MOSSY if (x + z + tier) % 3 == 0 else SBRICK
        if tier % 2 == 0:
          _set(v, x, wy, z, M_STAIR if (x + z) % 2 else A_STAIR)
        else:
          _set(v, x, wy, z, mat)
        if tier == 2 and (x, z) in ((ox + inset, cz), (ox + w - 1 - inset, cz)):
          _set(v, x, wy + 1, z, CAMP)

  # Top arch over center gap
  arch_y = oy + 6
  for dx in (-1, 0, 1):
    for dz in (-1, 0, 1):
      if abs(dx) + abs(dz) <= 1:
        _set(v, cx + dx, arch_y, cz + dz, CHISEL)
  for dx, dz in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
    _set(v, cx + dx, arch_y, cz + dz, CWALL)
    _set(v, cx + dx, arch_y + 1, cz + dz, M_STAIR)
  for dx in (-1, 0, 1):
    _set(v, cx + dx, arch_y + 2, cz, A_SLAB)
  for side in ((0, -2), (0, 2), (-2, 0)):
    _set(v, cx + side[0], arch_y, cz + side[1], JGATE)

  # Vine shaft from roof to water
  for y in range(oy + 1, arch_y):
    _set(v, cx, y, cz, VINE)
    _set(v, cx + 1, y, cz, VINE)

  # Interior barrels + campfires
  _set(v, ox + 2, oy + 1, oz + 2, BARREL)
  _set(v, ox + w - 3, oy + 1, oz + 2, BARREL)
  _set(v, ox + 2, oy + 1, oz + d - 3, CAMP)
  _set(v, ox + w - 3, oy + 1, oz + d - 3, LANTERN)

  # Exterior vines and leaves
  for x in range(ox, ox + w, 3):
    for y in range(oy + 2, oy + 5):
      _set(v, x, y, oz - 1, VINE)
      _set(v, x, oy + 5, oz - 1, LEAVES)

  return v


def _generate_bite_super_slide() -> np.ndarray:
  """
  Super Slide — book dimensions:
    19×10 four-lane stepped boat racing slide with ice slime honey.
  """
  COBBLE = _b("cobblestone")
  YELLOW = _b("yellow_concrete")
  ORANGE = _b("orange_concrete")
  LBLUE = _b("light_blue_concrete")
  BICE = _b("blue_ice")
  SLIME = _b("slime_block")
  HONEY = _b("honey_block")
  WATER = _b("water")
  BFENCE = _b("birch_fence")
  BSIGN = _b("birch_sign")
  CHEST = _b("chest")
  LANTERN = _b("sea_lantern")
  LADDER = _b("ladder")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 6, 11, 1
  length, width = 19, 10
  lane_zs = [oz + 1, oz + 3, oz + 5, oz + 7]

  # Grass surround
  for x in range(ox - 1, ox + length + 1):
    for z in range(oz - 1, oz + width + 1):
      _set(v, x, oy - 1, z, GRASS)

  # Bottom tier — cobblestone base
  for x in range(ox, ox + length):
    for z in range(oz, oz + width):
      _set(v, x, oy, z, COBBLE)

  # Landing zone (front)
  for x in range(ox, ox + 4):
    for z in lane_zs:
      _set(v, x, oy + 1, z, HONEY if x < 2 else BICE)
  for z in range(oz, oz + width):
    _set(v, ox, oy + 1, z, BFENCE)

  # Middle tier (y+3) — yellow platform + orange lanes
  mid_y = oy + 3
  for x in range(ox + 3, ox + length):
    for z in range(oz, oz + width):
      _set(v, x, mid_y, z, YELLOW)
  for z in lane_zs:
    for x in range(ox + 4, ox + 14):
      _set(v, x, mid_y + 1, z, ORANGE if x > ox + 5 else BICE)
    for x in range(ox + 5, ox + 13, 2):
      _set(v, x, mid_y + 1, z + 1, WATER)

  # Top tier (y+6) — light blue + slime
  top_y = oy + 6
  for x in range(ox + 9, ox + length):
    for z in range(oz, oz + width):
      _set(v, x, top_y, z, YELLOW)
  for z in lane_zs:
    for x in range(ox + 10, ox + 19):
      mat = LBLUE if x < ox + 17 else SLIME
      _set(v, x, top_y + 1, z, mat)
    # Start line gear
    _set(v, ox + length - 1, top_y + 2, z, CHEST)
    _set(v, ox + length - 1, top_y + 2, z + 1, LANTERN)
    _set(v, ox + length - 2, top_y + 2, z, BSIGN)

  # Lane fences
  for y in (mid_y + 1, top_y + 1):
    for x in range(ox, ox + length):
      _set(v, x, y + 1, oz, BFENCE)
      _set(v, x, y + 1, oz + width - 1, BFENCE)
      for z in (oz + 2, oz + 4, oz + 6):
        if x > ox + 3:
          _set(v, x, y + 1, z, BFENCE)

  # Return ladder on side
  for y in range(oy + 1, top_y + 2):
    _set(v, ox + length, y, oz + width - 1, LADDER)

  return v


def _oct_floor(dx: int, dz: int, radius: int) -> bool:
  if abs(dx) > radius or abs(dz) > radius:
    return False
  if radius >= 2 and abs(dx) >= radius - 1 and abs(dz) >= radius - 1:
    return False
  return True


def _oct_shell(dx: int, dz: int, radius: int) -> bool:
  if radius <= 1:
    return abs(dx) <= 1 and abs(dz) <= 1 and (dx == 0 or dz == 0) and not (dx == 0 and dz == 0)
  return _oct_floor(dx, dz, radius) and not _oct_floor(dx, dz, radius - 1)


def _generate_bite_lighthouse() -> np.ndarray:
  """
  Lighthouse — book dimensions:
    7×7 octagonal base tapering to 3×3 lantern, ~26 blocks tall on rocky island.
  """
  COBBLE = _b("cobblestone")
  STONE = _b("stone")
  SBRICK = _b("stone_bricks")
  CHISEL = _b("chiseled_stone_bricks")
  RED = _b("red_concrete")
  WHITE = _b("white_concrete")
  GPANE = _b("glass_pane")
  GLASS = _b("glass")
  SBSTAIR = _b("stone_brick_stairs")
  SBSLAB = _b("stone_brick_slab")
  SSSLAB = _b("smooth_stone_slab")
  BARS = _b("iron_bars")
  OBS = _b("observer")
  RLAMP = _b("redstone_lamp")
  DOOR = _b("dark_oak_door")
  SSTAIR = _b("spruce_stairs")
  SSLAB = _b("spruce_slab")
  LADDER = _b("ladder")
  LANTERN = _b("lantern")
  CRAFT = _b("crafting_table")
  FURNACE = _b("furnace")
  CHEST = _b("chest")
  BARREL = _b("barrel")
  CAMP = _b("campfire")
  WATER = _b("water")
  SAND = _b("sand")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz = 16, 16
  oy = 2
  stones = (COBBLE, STONE, SBRICK)

  def _fill_oct_shell(y: int, radius: int, mat) -> None:
    for dx in range(-radius, radius + 1):
      for dz in range(-radius, radius + 1):
        if _oct_shell(dx, dz, radius):
          block = mat(dx, dz) if callable(mat) else mat
          _set(v, cx + dx, y, cz + dz, block)

  def _fill_oct_solid(y: int, radius: int, mat) -> None:
    for dx in range(-radius, radius + 1):
      for dz in range(-radius, radius + 1):
        if _oct_floor(dx, dz, radius):
          block = mat(dx, dz) if callable(mat) else mat
          _set(v, cx + dx, y, cz + dz, block)

  # Rocky island + water surround
  for x in range(cx - 5, cx + 6):
    for z in range(cz - 5, cz + 6):
      dist = max(abs(x - cx), abs(z - cz))
      if dist <= 4:
        _set(v, x, oy - 1, z, stones[(x + z) % 3])
      elif dist <= 5:
        _set(v, x, oy - 1, z, SAND if (x + z) % 3 == 0 else WATER)

  # Step 1 — octagonal foundation
  _fill_oct_solid(oy, 3, lambda dx, dz: stones[(dx + dz) % 3])

  # Steps 2–4 — stone brick base, chiseled accents, red corners
  for y in range(oy + 1, oy + 3):
    for dx in range(-3, 4):
      for dz in range(-3, 4):
        if not _oct_shell(dx, dz, 3):
          continue
        if dz == 3 and abs(dx) <= 1:
          if y == oy + 1:
            _set(v, cx + dx, y, cz + dz, DOOR)
          else:
            _set(v, cx + dx, y, cz + dz, AIR_B)
        else:
          corner = abs(dx) == 3 or abs(dz) == 3
          _set(v, cx + dx, y, cz + dz, RED if corner and y == oy + 2 else SBRICK)

  for dx in range(-3, 4):
    for dz in range(-3, 4):
      if not _oct_shell(dx, dz, 3):
        continue
      if abs(dx) == 3 and abs(dz) == 3:
        _set(v, cx + dx, oy + 3, cz + dz, CHISEL)
      elif abs(dx) == 3 or abs(dz) == 3:
        _set(v, cx + dx, oy + 3, cz + dz, RED)

  # Steps 4–5 — lower red band (4 layers)
  for y in range(oy + 4, oy + 8):
    _fill_oct_shell(y, 3, RED)

  # Steps 5–6 — white middle tier (inset to radius 2)
  for y in range(oy + 8, oy + 14):
    for dx in range(-2, 3):
      for dz in range(-2, 3):
        if not _oct_shell(dx, dz, 2):
          continue
        if y in (oy + 10, oy + 12) and dz == 2 and dx == 0:
          _set(v, cx + dx, y, cz + dz, GPANE)
        else:
          _set(v, cx + dx, y, cz + dz, WHITE)

  # Steps 7–8 — upper red tier (3×3 ring)
  for y in range(oy + 14, oy + 20):
    for dx in range(-1, 2):
      for dz in range(-1, 2):
        if abs(dx) + abs(dz) == 0:
          continue
        _set(v, cx + dx, y, cz + dz, RED)

  # Step 8 — stone brick cap + stairs
  _fill_oct_shell(oy + 20, 2, SBRICK)
  for dx, dz in ((-2, 0), (2, 0), (0, -2), (0, 2)):
    _set(v, cx + dx, oy + 20, cz + dz, SBSTAIR)

  # Step 9 — balcony slab ring (extends one block out)
  for dx in range(-3, 4):
    for dz in range(-3, 4):
      if _oct_shell(dx, dz, 3):
        _set(v, cx + dx, oy + 21, cz + dz, SBSLAB if (dx + dz) % 2 == 0 else SSSLAB)

  # Steps 10–11 — observer ring + casing
  obs_ring = (
    (0, -2), (1, -2), (2, -1), (2, 0), (2, 1), (0, 2), (-2, 1), (-2, -1),
  )
  for dx, dz in obs_ring:
    _set(v, cx + dx, oy + 22, cz + dz, OBS)
  for dx in range(-2, 3):
    for dz in range(-2, 3):
      if (dx, dz) in obs_ring:
        continue
      if _oct_shell(dx, dz, 2):
        _set(v, cx + dx, oy + 22, cz + dz, WHITE if (dx + dz) % 2 else SBRICK)

  # Steps 12–13 — redstone lamp core + glass enclosure
  for y in (oy + 23, oy + 24):
    for dx in range(-1, 2):
      for dz in range(-1, 2):
        if dx == 0 and dz == 0:
          _set(v, cx, y, cz, RLAMP)
        elif abs(dx) + abs(dz) == 1:
          _set(v, cx + dx, y, cz + dz, GLASS if y == oy + 24 else RLAMP)
        else:
          _set(v, cx + dx, y, cz + dz, BARS)

  # Step 14 — domed roof
  for dx in range(-2, 3):
    for dz in range(-2, 3):
      if _oct_floor(dx, dz, 2):
        _set(v, cx + dx, oy + 25, cz + dz, SBRICK if _oct_shell(dx, dz, 2) else SSSLAB)
  _set(v, cx, oy + 26, cz, SBRICK)

  # Interior — clear hollow shaft
  for y in range(oy + 1, oy + 20):
    for dx in range(-2, 3):
      for dz in range(-2, 3):
        if _oct_floor(dx, dz, 2) and v[cx + dx, y, cz + dz] not in (DOOR, GPANE):
          if not _oct_shell(dx, dz, 3 if y < oy + 8 else 2 if y < oy + 14 else 1):
            _set(v, cx + dx, y, cz + dz, AIR_B)

  # Ground floor survival utilities
  gy = oy + 1
  _set(v, cx - 1, gy, cz - 1, CRAFT)
  _set(v, cx + 1, gy, cz - 1, FURNACE)
  _set(v, cx + 1, gy, cz, FURNACE)
  _set(v, cx - 1, gy, cz + 1, CHEST)
  _set(v, cx, gy, cz + 1, BARREL)
  _set(v, cx, gy, cz, CAMP)

  # Spiral spruce stairs hugging interior wall
  stair_y = oy + 2
  positions = [
    (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0),
  ]
  for layer in range(16):
    dx, dz = positions[layer % len(positions)]
    wy = stair_y + layer // len(positions)
    if wy >= oy + 18:
      break
    _set(v, cx + dx, wy, cz + dz, SSTAIR)
    if layer % 3 == 0:
      _set(v, cx + dx, wy + 1, cz + dz, LANTERN)

  # Central ladder through upper shaft
  for y in range(oy + 10, oy + 23):
    _set(v, cx, y, cz, LADDER)

  return v


def _generate_bite_cluck_cluck_coop() -> np.ndarray:
  """
  Cluck-Cluck Coop — book dimensions:
    11×14 fenced yard with raised 5×6 acacia coop and hopper egg collector.
  """
  GRASS = _b("grass_block")
  COBBLE = _b("cobblestone")
  PATH = _b("dirt_path")
  APLANK = _b("acacia_planks")
  ASLAB = _b("acacia_slab")
  ASTAIR = _b("acacia_stairs")
  ALOG = _b("stripped_acacia_log")
  ATRAP = _b("acacia_trapdoor")
  DFENCE = _b("dark_oak_fence")
  DGATE = _b("dark_oak_fence_gate")
  DSTAIR = _b("dark_oak_stairs")
  DSLAB = _b("dark_oak_slab")
  AND = _b("andesite")
  PAND = _b("polished_andesite")
  ASTAIRS = _b("andesite_stairs")
  ASLAB2 = _b("andesite_slab")
  HOPPER = _b("hopper")
  CHEST = _b("chest")
  CARPET = _b("yellow_carpet")
  HAY = _b("hay_block")
  LANTERN = _b("lantern")
  LEVER = _b("lever")
  BUTTON = _b("stone_button")
  TGRASS = _b("tall_grass")
  FERN = _b("fern")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 9, 1
  length, width = 11, 14
  coop_x, coop_z = ox + 3, oz + 2
  coop_w, coop_d = 5, 6
  floor_y = oy

  # Yard ground
  for x in range(ox, ox + length):
    for z in range(oz, oz + width):
      _set(v, x, floor_y - 1, z, GRASS)

  # Foundation — grass with cobble corner markers
  for x in range(ox, ox + length):
    for z in range(oz, oz + width):
      corner = x in (ox, ox + length - 1) or z in (oz, oz + width - 1)
      edge_mark = corner or (x == ox + length // 2 and z == oz) or (x == ox and z == oz + width // 2)
      _set(v, x, floor_y, z, COBBLE if edge_mark else GRASS)

  # L-shaped shovel path at front-left
  for z in range(oz + width - 4, oz + width):
    _set(v, ox + 1, floor_y, z, PATH)
  for x in range(ox + 1, ox + 4):
    _set(v, x, floor_y, oz + width - 2, PATH)

  # Collection chest and hopper chain toward coop
  chest_x, chest_z = ox + 5, oz + width - 3
  _set(v, chest_x, floor_y + 1, chest_z, CHEST)
  hopper_pts = [
    (chest_x, chest_z - 1),
    (chest_x - 1, chest_z - 1),
    (chest_x - 1, chest_z - 2),
    (chest_x, chest_z - 3),
    (chest_x + 1, chest_z - 3),
    (chest_x + 1, chest_z - 4),
    (chest_x, chest_z - 5),
    (chest_x - 1, chest_z - 6),
    (chest_x, chest_z - 7),
  ]
  for hx, hz in hopper_pts:
    _set(v, hx, floor_y + 1, hz, HOPPER)

  # Acacia support pillars under coop
  pillar_pts = (
    (coop_x, coop_z),
    (coop_x + coop_w - 1, coop_z),
    (coop_x, coop_z + coop_d - 1),
    (coop_x + coop_w - 1, coop_z + coop_d - 1),
  )
  for px, pz in pillar_pts:
    for y in range(floor_y + 1, floor_y + 4):
      _set(v, px, y, pz, ALOG)

  # Dark oak fence perimeter
  for x in range(ox, ox + length):
    for z in range(oz, oz + width):
      on_edge = x in (ox, ox + length - 1) or z in (oz, oz + width - 1)
      if not on_edge:
        continue
      gate = x in (ox + 4, ox + 5) and z == oz + width - 1
      for y in range(floor_y + 1, floor_y + 4):
        _set(v, x, y, z, DGATE if gate and y == floor_y + 2 else DFENCE)

  # Raised coop platform (y+3)
  plat_y = floor_y + 3
  for x in range(coop_x, coop_x + coop_w):
    for z in range(coop_z, coop_z + coop_d):
      edge = x in (coop_x, coop_x + coop_w - 1) or z in (coop_z, coop_z + coop_d - 1)
      _set(v, x, plat_y, z, APLANK if edge else ASLAB)

  # Floor hoppers feeding collection chain
  for hx, hz in ((coop_x + 1, coop_z + 2), (coop_x + 3, coop_z + 3)):
    _set(v, hx, plat_y + 1, hz, HOPPER)

  # Andesite base band and U-shaped coop hoppers
  base_y = plat_y + 1
  for x in range(coop_x, coop_x + coop_w):
    for z in range(coop_z, coop_z + coop_d):
      corner = x in (coop_x, coop_x + coop_w - 1) and z in (coop_z, coop_z + coop_d - 1)
      edge = x in (coop_x, coop_x + coop_w - 1) or z in (coop_z, coop_z + coop_d - 1)
      if corner:
        _set(v, x, base_y, z, PAND)
      elif edge:
        _set(v, x, base_y, z, AND)
  for x in range(coop_x + 1, coop_x + coop_w - 1):
    _set(v, x, base_y, coop_z, HOPPER)
    _set(v, x, base_y, coop_z + coop_d - 1, HOPPER)
  for z in range(coop_z + 1, coop_z + coop_d - 1):
    _set(v, coop_x, base_y, z, HOPPER)

  # Lower walls — stripped logs corners, planks, trapdoor vents, gate entrance
  for y in range(base_y + 1, base_y + 3):
    for x in range(coop_x, coop_x + coop_w):
      for z in range(coop_z, coop_z + coop_d):
        edge = x in (coop_x, coop_x + coop_w - 1) or z in (coop_z, coop_z + coop_d - 1)
        if not edge:
          continue
        corner = x in (coop_x, coop_x + coop_w - 1) and z in (coop_z, coop_z + coop_d - 1)
        front_gate = z == coop_z + coop_d - 1 and x in (coop_x + 1, coop_x + 2) and y == base_y + 1
        side_vent = z in (coop_z + 1, coop_z + coop_d - 2) and x in (coop_x, coop_x + coop_w - 1) and y == base_y + 1
        if front_gate:
          _set(v, x, y, z, DGATE)
        elif side_vent:
          _set(v, x, y, z, ATRAP)
        elif corner:
          _set(v, x, y, z, ALOG)
        else:
          _set(v, x, y, z, APLANK)

  # Interior bedding — carpet over hoppers, hay bales
  bed_y = base_y + 1
  for x in range(coop_x + 1, coop_x + coop_w - 1):
    for z in range(coop_z + 1, coop_z + coop_d - 1):
      _set(v, x, bed_y, z, CARPET)
  _set(v, coop_x + 1, bed_y + 1, coop_z + 1, HAY)
  _set(v, coop_x + coop_w - 2, bed_y + 1, coop_z + 1, HAY)

  # Upper wall band + roof framing
  top_y = base_y + 3
  for x in range(coop_x, coop_x + coop_w):
    for z in range(coop_z, coop_z + coop_d):
      edge = x in (coop_x, coop_x + coop_w - 1) or z in (coop_z, coop_z + coop_d - 1)
      if edge:
        corner = x in (coop_x, coop_x + coop_w - 1) and z in (coop_z, coop_z + coop_d - 1)
        _set(v, x, top_y, z, ALOG if corner else APLANK)
        _set(v, x, top_y + 1, z, ASTAIRS if corner else ASLAB2)

  # Pitched roof — dark oak fill, andesite trim
  roof_y = top_y + 2
  for x in range(coop_x - 1, coop_x + coop_w + 1):
    for z in range(coop_z - 1, coop_z + coop_d + 1):
      on_edge = x in (coop_x - 1, coop_x + coop_w) or z in (coop_z - 1, coop_z + coop_d)
      if on_edge:
        _set(v, x, roof_y, z, ASTAIRS if (x + z) % 2 == 0 else ASLAB2)
        _set(v, x, roof_y + 1, z, BUTTON)
      elif x in range(coop_x, coop_x + coop_w) and z in range(coop_z, coop_z + coop_d):
        _set(v, x, roof_y, z, DSTAIR if (x + z) % 2 else DSLAB)

  _set(v, coop_x + coop_w // 2, top_y + 1, coop_z + coop_d // 2, LANTERN)

  # Entrance stairs and lever
  stair_x = ox + 4
  for step, z in enumerate(range(oz + width - 1, oz + width - 5, -1)):
    _set(v, stair_x, floor_y + 1 + step, z, ASLAB)
    _set(v, stair_x + 1, floor_y + 1 + step, z, ASLAB)
  _set(v, ox + 6, floor_y + 3, oz + width - 1, LEVER)

  # Yard landscaping
  for fx, fz, plant in (
    (ox + 2, oz + 3, TGRASS),
    (ox + 7, oz + 4, FERN),
    (ox + 8, oz + width - 5, TGRASS),
    (ox + 3, oz + width - 6, FERN),
    (ox + length - 2, oz + 5, TGRASS),
  ):
    _set(v, fx, floor_y + 1, fz, plant)

  return v


def _generate_bite_norse_longhouse() -> np.ndarray:
  """
  Norse Longhouse — book dimensions:
    8×15 Viking hall, ~16 blocks tall with steep A-frame roof and loft interior.
  """
  COBBLE = _b("cobblestone")
  BIRCH = _b("birch_planks")
  BSLAB = _b("birch_slab")
  BSTAIR = _b("birch_stairs")
  BFENCE = _b("birch_fence")
  BGATE = _b("birch_fence_gate")
  SPRUCE = _b("spruce_planks")
  SSTAIR = _b("spruce_stairs")
  STRAP = _b("spruce_trapdoor")
  CHISEL = _b("chiseled_quartz_block")
  QUARTZ = _b("quartz_block")
  QSTAIR = _b("quartz_stairs")
  SAND = _b("sandstone")
  SWALL = _b("sandstone_wall")
  SSTAIRS = _b("sandstone_stairs")
  SSLAB = _b("sandstone_slab")
  LGRAY = _b("light_gray_concrete")
  GGLASS = _b("green_stained_glass_pane")
  OSTAIR = _b("oak_stairs")
  SOUL = _b("soul_lantern")
  LADDER = _b("ladder")
  CARPET = _b("green_carpet")
  PSTAIR = _b("prismarine_stairs")
  BED = _b("red_bed")
  PISTON = _b("piston")
  RTORCH = _b("redstone_torch")
  BARREL = _b("barrel")
  CHEST = _b("chest")
  BREW = _b("brewing_stand")
  SDOOR = _b("spruce_door")
  GRASS = _b("grass_block")
  SLOG = _b("spruce_log")
  SLEAVES = _b("spruce_leaves")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 8, 1
  w, d = 8, 15
  cx = ox + w // 2 - 1
  wall_h = 6
  wall_top = oy + wall_h

  # Taiga ground
  for x in range(ox - 2, ox + w + 2):
    for z in range(oz - 2, oz + d + 2):
      _set(v, x, oy - 1, z, GRASS)

  # Step 1 — cobblestone perimeter, birch plank floor, central hearth strip
  for x in range(ox, ox + w):
    for z in range(oz, oz + d):
      edge = x in (ox, ox + w - 1) or z in (oz, oz + d - 1)
      hearth = cx - 1 <= x <= cx and oz + 4 <= z <= oz + 9
      if edge:
        _set(v, x, oy, z, COBBLE)
      elif hearth:
        _set(v, x, oy, z, BSLAB)
      else:
        _set(v, x, oy, z, BIRCH)

  def _pillar_x(x: int) -> bool:
    return x in (ox, ox + 2, ox + 4, ox + w - 1)

  # Steps 2–4 — walls with spruce pillars, quartz, sandstone, concrete, windows
  for y in range(1, wall_h + 1):
    wy = oy + y
    for x in range(ox, ox + w):
      for z in range(oz, oz + d):
        edge = x in (ox, ox + w - 1) or z in (oz, oz + d - 1)
        if not edge:
          continue
        end_face = z in (oz, oz + d - 1)
        pillar = _pillar_x(x) or x in (ox, ox + w - 1)
        entrance = z == oz + d - 1 and x in (cx, cx + 1) and y <= 2

        if entrance:
          _set(v, x, wy, z, SDOOR if y <= 2 else AIR_B)
          continue
        if end_face and y <= 4:
          if pillar:
            _set(v, x, wy, z, SWALL if y >= 3 else CHISEL)
          elif y == 3 and abs(x - cx) <= 1:
            _set(v, x, wy, z, GGLASS)
          else:
            _set(v, x, wy, z, LGRAY if y >= 3 else CHISEL)
        elif pillar:
          mat = SPRUCE if y <= 3 else SAND if y == 4 else LGRAY
          _set(v, x, wy, z, mat)
        elif y in (3, 5) and not end_face and x in (ox + 1, ox + w - 2):
          _set(v, x, wy, z, GGLASS)
        elif y >= 4:
          _set(v, x, wy, z, LGRAY)
        else:
          _set(v, x, wy, z, CHISEL)

        if y in (3, 5) and not end_face:
          _set(v, x, wy + 1, z, QSTAIR)

  # Side trim — birch fences, oak stairs, soul lanterns
  for z in range(oz + 2, oz + d - 2, 3):
    for x in (ox, ox + w - 1):
      _set(v, x, wall_top, z, BFENCE)
      _set(v, x, wall_top + 1, z, SOUL)
      _set(v, x, wall_top, z + 1, OSTAIR)

  # Hollow interior
  for y in range(oy + 1, wall_top + 1):
    for x in range(ox + 1, ox + w - 1):
      for z in range(oz + 1, oz + d - 1):
        _set(v, x, y, z, AIR_B)

  # Interior quartz columns
  for px, pz in ((cx - 1, oz + 4), (cx + 1, oz + 10)):
    for y in range(oy + 1, wall_top):
      _set(v, px, y, pz, CHISEL if y < wall_top - 1 else QUARTZ)

  # Step 8 — partial loft platform
  loft_y = wall_top
  for x in range(ox + 1, ox + w - 1):
    for z in range(oz + 1, oz + d - 4):
      _set(v, x, loft_y, z, BIRCH)
  for lx, lz in ((ox + 2, oz + 5), (ox + 5, oz + 8)):
    for y in range(oy + 2, loft_y):
      _set(v, lx, y, lz, LADDER)

  # Loft bunk beds
  for bx in (ox + 1, ox + 4):
    _set(v, bx, loft_y + 1, oz + 2, BED)
    _set(v, bx + 1, loft_y + 1, oz + 2, BED)
    _set(v, bx, loft_y + 2, oz + 2, STRAP)
    _set(v, bx + 1, loft_y + 2, oz + 2, STRAP)

  # Great hall — green carpet, feast table, throne
  for z in range(oz + 5, oz + 11):
    for x in range(cx - 1, cx + 2):
      _set(v, x, oy + 1, z, CARPET)
  for tx in (cx - 1, cx + 1):
    _set(v, tx, oy + 1, oz + 7, RTORCH)
    _set(v, tx, oy + 2, oz + 7, PISTON)
  for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
    _set(v, cx + dx, oy + 1, oz + 3, PSTAIR)

  # Storage counters
  _set(v, ox + 1, oy + 1, oz + 1, BARREL)
  _set(v, ox + 2, oy + 1, oz + 1, CHEST)
  _set(v, ox + w - 2, oy + 1, oz + 1, BREW)
  _set(v, ox + w - 3, oy + 1, oz + 1, BARREL)

  # Interior soul lanterns
  for lz in (oz + 4, oz + 8, oz + 12):
    _set(v, cx, wall_top - 1, lz, SOUL)

  # Steps 10–11 — gable peaks on end walls
  for end_z in (oz, oz + d - 1):
    for layer in range(4):
      gy = wall_top + 1 + layer
      inset = layer // 2 + 1
      for x in range(ox + inset, ox + w - inset):
        _set(v, x, gy, end_z, CHISEL if x in (ox + inset, ox + w - 1 - inset) else LGRAY)
        if layer == 2 and abs(x - cx) <= 1:
          _set(v, x, gy, end_z, GGLASS)

  # Steps 11–14 — steep A-frame roof along length
  max_dist = max(cx - ox, ox + w - 1 - cx)
  for z in range(oz - 1, oz + d + 1):
    for x in range(ox, ox + w):
      dist = min(x - ox, ox + w - 1 - x)
      peak_h = 1 + (max_dist - dist) * 2
      for h in range(peak_h):
        ry = wall_top + 1 + h
        if x <= cx:
          mat = SSTAIR if h % 2 == 0 else SPRUCE
        else:
          mat = BSTAIR if h % 2 == 0 else BIRCH
        _set(v, x, ry, z, mat)
        if dist == 0 and h == peak_h - 1:
          _set(v, x, ry + 1, z, SSLAB)

  # Ridge cap and dormer alcoves
  for z in range(oz + 3, oz + d - 3, 6):
    _set(v, cx, wall_top + 7, z, SSTAIRS)
    _set(v, cx - 1, wall_top + 5, z, BFENCE)
    _set(v, cx + 1, wall_top + 5, z, BFENCE)
    _set(v, cx, wall_top + 6, z, SOUL)

  # Surrounding spruce trees
  for tx, tz in ((ox - 2, oz - 1), (ox + w + 1, oz + d)):
    for y in range(oy, oy + 5):
      _set(v, tx, y, tz, SLOG)
    for dx in range(-1, 2):
      for dz in range(-1, 2):
        _set(v, tx + dx, oy + 5, tz + dz, SLEAVES)

  return v


def _in_circle(dx: int, dz: int, r: int) -> bool:
  return dx * dx + dz * dz <= r * r


def _generate_bite_igloo_hideout() -> np.ndarray:
  """
  Igloo Hideout — book dimensions:
    13×13 underground snow bunker + 9-block surface snow dome igloo.
  """
  GRASS = _b("grass_block")
  SNOW = _b("snow_block")
  PICE = _b("packed_ice")
  CYAN = _b("cyan_wool")
  PINK = _b("pink_wool")
  ORANGE = _b("orange_wool")
  CCARPET = _b("cyan_carpet")
  PCARPET = _b("pink_carpet")
  OCARPET = _b("orange_carpet")
  SFENCE = _b("spruce_fence")
  SSTAIR = _b("spruce_stairs")
  SPLANK = _b("spruce_planks")
  SDOOR = _b("spruce_door")
  SLANTERN = _b("soul_lantern")
  SCAMP = _b("soul_campfire")
  LADDER = _b("ladder")
  RBED = _b("red_bed")
  BBED = _b("blue_bed")
  SHELF = _b("bookshelf")
  BARREL = _b("barrel")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz = 16, 16
  oy = 1
  surface = oy + 5
  ox, oz, w = cx - 6, cz - 6, 13

  # Snowy surface pad
  for x in range(cx - 8, cx + 9):
    for z in range(cz - 8, cz + 9):
      _set(v, x, surface - 1, z, GRASS if (x + z) % 5 == 0 else SNOW)

  # Underground bunker — snow walls, packed ice floor accents
  for y in range(oy, surface):
    for x in range(ox, ox + w):
      for z in range(oz, oz + w):
        edge = x in (ox, ox + w - 1) or z in (oz, oz + w - 1)
        if y == oy:
          _set(v, x, y, z, PICE if (x + z) % 3 == 0 else SNOW)
        elif edge:
          _set(v, x, y, z, SNOW)
        else:
          _set(v, x, y, z, AIR_B)

  # Wool alcoves with fence posts and soul lanterns
  alcoves = (
    (ox + 1, oz + 5, CYAN, BBED, ox + 2, oz + 5),
    (ox + w - 4, oz + 5, PINK, RBED, ox + w - 3, oz + 5),
    (ox + 5, oz + w - 4, ORANGE, RBED, ox + 5, oz + w - 3),
  )
  for ax, az, wool, bed, bx, bz in alcoves:
    for dy in range(2):
      _set(v, ax, oy + 1 + dy, az, wool)
      _set(v, ax + 1, oy + 1 + dy, az, wool)
    _set(v, ax, oy + 1, az + 1, SFENCE)
    _set(v, ax, oy + 2, az + 1, SLANTERN)
    _set(v, bx, oy + 1, bz, bed)

  # Central soul campfire and spruce stair seating
  _set(v, cx, oy + 1, cz, SCAMP)
  for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
    _set(v, cx + dx, oy + 1, cz + dz, SSTAIR)

  # Ladder shaft to surface
  lx, lz = ox + w - 2, cz
  for y in range(oy + 1, surface + 1):
    _set(v, lx, y, lz, LADDER)

  # Surface snow igloo dome
  dome_r = 4
  for layer in range(5):
    y = surface + layer
    inset = layer // 2
    r = dome_r - inset
    for dx in range(-r - 1, r + 2):
      for dz in range(-r - 1, r + 2):
        if _in_circle(dx, dz, r):
          shell = _in_circle(dx, dz, r) and not _in_circle(dx, dz, max(r - 1, 0))
          if layer < 4 and not shell and y < surface + 4:
            continue
          if shell or layer == 4:
            _set(v, cx + dx, y, cz + dz, SNOW)

  # Entrance — spruce door and plank frame (south)
  door_z = cz + dome_r
  _set(v, cx - 1, surface + 1, door_z, SDOOR)
  _set(v, cx, surface + 1, door_z, SDOOR)
  _set(v, cx + 1, surface + 1, door_z, SDOOR)
  for dx in (-2, 2):
    for y in range(surface + 1, surface + 4):
      _set(v, cx + dx, y, door_z, SPLANK)

  # Igloo interior — diamond carpet
  for dx in range(-1, 2):
    for dz in range(-1, 2):
      mat = CCARPET if abs(dx) + abs(dz) == 0 else OCARPET if abs(dx) + abs(dz) == 1 else PCARPET
      _set(v, cx + dx, surface + 1, cz + dz, mat)

  # Soul lantern chandelier
  for y in range(surface + 2, surface + 5):
    _set(v, cx, y, cz, SFENCE)
  for dx, dz in ((-2, 0), (2, 0), (0, -2), (0, 2)):
    _set(v, cx + dx, surface + 4, cz + dz, SFENCE)
    _set(v, cx + dx, surface + 3, cz + dz, SLANTERN)

  # Reading nook — bookshelves and barrels
  for y in range(surface + 1, surface + 4):
    _set(v, cx - 3, y, cz - 2, SHELF)
    _set(v, cx + 3, y, cz - 2, SHELF)
  for bx in (cx - 1, cx, cx + 1):
    _set(v, bx, surface + 1, cz - 2, SPLANK)
    _set(v, bx, surface + 2, cz - 2, BARREL if bx == cx else SPLANK)

  return v


def _generate_bite_allay_statue() -> np.ndarray:
  """
  Allay Statue — book dimensions:
    5×5×3 stone pedestal with 3×3 sea lanterns, 5-high blue body,
    5×5×5 head, 8-block wingspan light blue wool and concrete wings.
  """
  GRASS = _b("grass_block")
  STONE = _b("stone")
  SBRICK = _b("stone_bricks")
  SSTAIR = _b("stone_brick_stairs")
  CHISEL = _b("chiseled_stone_bricks")
  LANTERN = _b("sea_lantern")
  BLUE = _b("blue_wool")
  LBLUE = _b("light_blue_wool")
  LCONC = _b("light_blue_concrete")
  CCONC = _b("cyan_concrete")
  WHITE = _b("white_concrete")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 1
  bs = 5  # base footprint

  # Grass pad
  for x in range(cx - 4, cx + 5):
    for z in range(cz - 4, cz + 5):
      _set(v, x, oy - 1, z, GRASS)

  # Stone pedestal — 5×5, 3 blocks tall
  bx, bz = cx - 2, cz - 2
  for y in range(3):
    for x in range(bx, bx + bs):
      for z in range(bz, bz + bs):
        edge = x in (bx, bx + bs - 1) or z in (bz, bz + bs - 1)
        corner = x in (bx, bx + bs - 1) and z in (bz, bz + bs - 1)
        if corner:
          _set(v, x, oy + y, z, CHISEL)
        elif edge and y == 0:
          _set(v, x, oy + y, z, SSTAIR)
        else:
          _set(v, x, oy + y, z, SBRICK if y > 0 else STONE)

  # Glowing sea lantern cap — 3×3
  for x in range(cx - 1, cx + 2):
    for z in range(cz - 1, cz + 2):
      _set(v, x, oy + 3, z, LANTERN)

  # Body — 3×3 blue column, 5 blocks tall
  for y in range(4, 9):
    for x in range(cx - 1, cx + 2):
      for z in range(cz - 1, cz + 2):
        _set(v, x, oy + y, z, BLUE)

  # Wings — 8-block span, 4 blocks tall, wool top and concrete fringe
  wing_ys = range(oy + 5, oy + 9)
  for side, dx in ((-1, -1), (1, 1)):
    for y in wing_ys:
      rel = y - (oy + 5)
      for reach in range(1, 4):
        wx = cx + side * (1 + reach)
        wz = cz + (0 if reach < 3 else side)
        if rel < 2:
          _set(v, wx, y, wz, LBLUE)
        else:
          _set(v, wx, y, wz, LCONC if (reach + rel) % 2 else CCONC)

  # Head — 5×5×5, blue lower half and light blue upper half
  hy0 = oy + 9
  for y in range(5):
    for x in range(cx - 2, cx + 3):
      for z in range(cz - 2, cz + 3):
        mat = BLUE if y < 2 else LBLUE
        _set(v, x, hy0 + y, z, mat)

  # White concrete eyes on north face
  for ey in (hy0 + 2, hy0 + 3):
    _set(v, cx - 1, ey, cz - 2, WHITE)
    _set(v, cx + 1, ey, cz - 2, WHITE)

  return v


def _generate_bite_old_western_jail() -> np.ndarray:
  """
  Old Western Jail — book dimensions:
    9×9 birch sheriff office, red sandstone pillars veranda awning,
    attached andesite cobblestone jail cell with iron bars and escape tunnel.
  """
  RED_SAND = _b("red_sand")
  DEAD = _b("dead_bush")
  BIRCH = _b("birch_planks")
  BSTAIR = _b("birch_stairs")
  BSLAB = _b("birch_slab")
  BFENCE = _b("birch_fence")
  BGATE = _b("birch_fence_gate")
  RSAND = _b("smooth_red_sandstone")
  RSSTAIR = _b("smooth_red_sandstone_stairs")
  RSSLAB = _b("smooth_red_sandstone_slab")
  ABUTTON = _b("acacia_button")
  IBARS = _b("iron_bars")
  IDOOR = _b("iron_door")
  LANTERN = _b("lantern")
  SSTONE = _b("smooth_stone")
  SSSLAB = _b("smooth_stone_slab")
  AND = _b("andesite")
  ASTAIR = _b("andesite_stairs")
  COBBLE = _b("cobblestone")
  CSTAIR = _b("cobblestone_stairs")
  S_TRAP = _b("spruce_trapdoor")
  S_STAIR = _b("spruce_stairs")
  LEVER = _b("lever")
  WATER = _b("water")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 12, 2
  w, d = 9, 9
  wall_h = 7

  # Badlands ground pad
  for x in range(ox - 2, ox + w + 6):
    for z in range(oz - 5, oz + d + 3):
      _set(v, x, oy - 1, z, RED_SAND)
      if (x + z) % 7 == 0:
        _set(v, x, oy, z, DEAD)

  # Foundation — birch planks and stair trim
  for x in range(ox, ox + w):
    for z in range(oz, oz + d):
      edge = x in (ox, ox + w - 1) or z in (oz, oz + d - 1)
      _set(v, x, oy, z, BSTAIR if edge else BIRCH)

  # Corner sandstone pillars — front 8 tall, back 7 tall
  pillars = (
    (ox, oz, 8),
    (ox + w - 1, oz, 8),
    (ox, oz + d - 1, 7),
    (ox + w - 1, oz + d - 1, 7),
  )
  for px, pz, ph in pillars:
    for y in range(ph):
      _set(v, px, oy + 1 + y, pz, RSAND)

  # Birch plank walls with door and window gaps
  door_x = ox + w // 2
  for y in range(1, wall_h + 1):
    wy = oy + y
    for x in range(ox, ox + w):
      for z in range(oz, oz + d):
        edge = x in (ox, ox + w - 1) or z in (oz, oz + d - 1)
        if not edge:
          continue
        corner = x in (ox, ox + w - 1) and z in (oz, oz + d - 1)
        if corner:
          continue
        # South doorway
        if z == oz and x == door_x and y <= 2:
          continue
        # South windows
        if z == oz and y == 3 and x in (ox + 2, ox + 5, ox + w - 3):
          _set(v, x, wy, z, IBARS)
          continue
        # Side windows
        if y == 3 and ((x == ox and z in (oz + 3, oz + 5)) or (x == ox + w - 1 and z in (oz + 3, oz + 5))):
          _set(v, x, wy, z, IBARS)
          continue
        _set(v, x, wy, z, BIRCH)

  # Hollow interior
  for x in range(ox + 1, ox + w - 1):
    for z in range(oz + 1, oz + d - 1):
      for y in range(oy + 1, oy + wall_h):
        _set(v, x, y, z, AIR_B)

  # Flat birch slab roof
  roof_y = oy + wall_h + 1
  for x in range(ox, ox + w):
    for z in range(oz, oz + d):
      _set(v, x, roof_y, z, BSLAB)

  # Front sandstone facade trim and acacia button studs
  for x in range(ox + 1, ox + w - 1):
    _set(v, x, oy + wall_h, oz, RSSTAIR)
    _set(v, x, oy + wall_h + 1, oz, RSSLAB)
    if x % 2 == 0:
      _set(v, x, oy + 4, oz, ABUTTON)

  # Birch fence gate doorway
  _set(v, door_x, oy + 1, oz, BGATE)
  _set(v, door_x, oy + 2, oz, BGATE)

  # Front veranda — birch floor, fence banister, sandstone awning
  veranda_z = oz - 1
  for x in range(ox, ox + w):
    for z in range(oz - 3, oz):
      _set(v, x, oy + 1, z, BIRCH)
      if z == oz - 3:
        _set(v, x, oy + 2, z, BFENCE)
  for x in range(ox, ox + w):
    _set(v, x, oy + 4, veranda_z, RSSTAIR)
  for x in range(ox + 1, ox + w - 1, 2):
    _set(v, x, oy + 3, oz - 2, LANTERN)

  # Jail cell extension — east side
  jx, jz, jw, jd = ox + w - 1, oz + 2, 5, 5
  for x in range(jx, jx + jw):
    for z in range(jz, jz + jd):
      _set(v, x, oy + 1, z, SSSLAB)

  for y in range(2, 5):
    wy = oy + y
    for x in range(jx, jx + jw):
      for z in range(jz, jz + jd):
        edge = x in (jx, jx + jw - 1) or z in (jz, jz + jd - 1)
        if not edge:
          continue
        if x == jx + jw - 1 and z == jz + 2 and y in (2, 3):
          _set(v, x, wy, z, IBARS)
        elif x == jx and z == jz + 2 and y <= 2:
          continue  # doorway to office
        else:
          mat = AND if (x + z + y) % 2 == 0 else COBBLE
          if y == 4 and edge:
            _set(v, x, wy, z, SSSLAB)
          elif y < 4:
            _set(v, x, wy, z, ASTAIR if y == 3 and z == jz else mat)

  # Jail roof slabs
  for x in range(jx, jx + jw):
    for z in range(jz, jz + jd):
      _set(v, x, oy + 5, z, SSSLAB)

  # Iron door and lever between office and cell
  _set(v, jx, oy + 1, jz + 2, IDOOR)
  _set(v, jx, oy + 2, jz + 2, IDOOR)
  _set(v, jx - 1, oy + 2, jz + 2, LEVER)

  # Sheriff office interior — spruce desk and lantern
  _set(v, ox + 3, oy + 1, oz + 5, S_STAIR)
  _set(v, ox + 4, oy + 1, oz + 5, S_STAIR)
  _set(v, ox + 3, oy + 2, oz + 5, S_TRAP)
  _set(v, ox + 5, oy + 3, oz + 6, LANTERN)

  # Secret escape tunnel — trapdoor, shaft, water tunnel outside
  _set(v, jx + 2, oy + 1, jz + 3, S_TRAP)
  for y in range(oy, oy - 2, -1):
    _set(v, jx + 2, y, jz + 3, AIR_B)
  for x in range(jx + 2, jx + jw + 2):
    _set(v, x, oy - 1, jz + 4, WATER)
    _set(v, x, oy - 2, jz + 4, WATER)

  return v


def _oct_footprint(dx: int, dz: int, r: int = 5) -> bool:
  ax, az = abs(dx), abs(dz)
  return max(ax, az) <= r and ax + az <= r + 2


def _oct_vertices(r: int = 5) -> list[tuple[int, int]]:
  return [
    (r, 0),
    (r - 2, r - 2),
    (0, r),
    (-(r - 2), r - 2),
    (-r, 0),
    (-(r - 2), -(r - 2)),
    (0, -r),
    (r - 2, -(r - 2)),
  ]


def _generate_bite_secret_island_base() -> np.ndarray:
  """
  Secret Island Base — book dimensions:
    13×13 octagonal underwater glass aquarium, purpur pillar columns,
    dual water elevator shafts, hidden grass island with spruce tree.
  """
  WATER = _b("water")
  KELP = _b("kelp")
  SANDSTONE = _b("sandstone")
  SSLAB = _b("sandstone_slab")
  PPILLAR = _b("purpur_pillar")
  PSTAIR = _b("purpur_stairs")
  PURPUR = _b("purpur_block")
  GLASS = _b("light_blue_stained_glass_pane")
  ROD = _b("end_rod")
  SOUL = _b("soul_sand")
  MAGMA = _b("magma_block")
  DOOR = _b("spruce_door")
  SAND = _b("sand")
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  SLOG = _b("spruce_log")
  SLEAF = _b("spruce_leaves")
  STRAP = _b("spruce_trapdoor")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz = 16, 16
  oy = 7
  col_h = 8
  sea = oy + col_h + 2
  r = 5
  verts = _oct_vertices(r)

  # Ocean basin
  for x in range(cx - 10, cx + 11):
    for z in range(cz - 10, cz + 11):
      for y in range(2, sea + 1):
        _set(v, x, y, z, WATER)

  # Sandstone octagonal aquarium floor
  for dx in range(-r, r + 1):
    for dz in range(-r, r + 1):
      if _oct_footprint(dx, dz, r):
        _set(v, cx + dx, oy, cz + dz, SANDSTONE)

  # Floor ring — purpur pillars linking column bases
  for i, (vx, vz) in enumerate(verts):
    nx, nz = verts[(i + 1) % 8]
    steps = max(abs(nx - vx), abs(nz - vz))
    for t in range(steps + 1):
      fx = vx + (nx - vx) * t // max(steps, 1)
      fz = vz + (nz - vz) * t // max(steps, 1)
      _set(v, cx + fx, oy + 1, cz + fz, PPILLAR)

  # Eight purpur pillar columns with stair caps
  for vx, vz in verts:
    for y in range(col_h):
      _set(v, cx + vx, oy + 1 + y, cz + vz, PPILLAR)
    _set(v, cx + vx, oy + 1, cz + vz, PSTAIR)
    _set(v, cx + vx, oy + col_h, cz + vz, PSTAIR)

  # Glass walls between columns
  for i, (vx, vz) in enumerate(verts):
    nx, nz = verts[(i + 1) % 8]
    steps = max(abs(nx - vx), abs(nz - vz))
    for t in range(1, steps):
      fx = vx + (nx - vx) * t // steps
      fz = vz + (nz - vz) * t // steps
      for y in range(1, col_h):
        _set(v, cx + fx, oy + y, cz + fz, GLASS)

  # Dry viewing room interior
  for dx in range(-r + 1, r):
    for dz in range(-r + 1, r):
      if _oct_footprint(dx, dz, r - 1):
        for y in range(1, col_h):
          _set(v, cx + dx, oy + y, cz + dz, AIR_B)

  # Sandstone roof with twin elevator gaps
  roof_y = oy + col_h
  for dx in range(-r, r + 1):
    for dz in range(-r, r + 1):
      if _oct_footprint(dx, dz, r):
        if abs(dx) <= 1 and abs(dz) <= 1:
          continue
        _set(v, cx + dx, roof_y, cz + dz, SSLAB)

  # End rod lighting around roof edge
  for vx, vz in verts:
    _set(v, cx + vx, roof_y + 1, cz + vz, ROD)

  # Dual purpur-and-glass elevator shafts
  shaft_xs = (cx - 1, cx + 1)
  for sx in shaft_xs:
    for y in range(1, col_h + 3):
      _set(v, sx, oy + y, cz + 1, PPILLAR)
      if y < col_h:
        _set(v, sx, oy + y, cz, GLASS)
      _set(v, sx, oy + y, cz, WATER)

  _set(v, shaft_xs[0], oy + 1, cz, SOUL)
  _set(v, shaft_xs[1], oy + 1, cz, MAGMA)
  _set(v, shaft_xs[0], oy + 1, cz - 1, DOOR)
  _set(v, shaft_xs[1], oy + 1, cz - 1, DOOR)
  _set(v, shaft_xs[0], oy + 1, cz - 2, ROD)
  _set(v, shaft_xs[1], oy + 1, cz - 2, ROD)
  for y in range(2, col_h):
    _set(v, shaft_xs[0], oy + y, cz, KELP)
    _set(v, shaft_xs[1], oy + y, cz, KELP)
  for sx in shaft_xs:
    _set(v, sx, roof_y + 2, cz, STRAP)

  # Hidden surface island — sand then grass mound
  for dx in range(-2, 3):
    for dz in range(-2, 3):
      if abs(dx) + abs(dz) <= 3:
        _set(v, cx + dx, sea, cz + dz, SAND)
        _set(v, cx + dx, sea + 1, cz + dz, DIRT if abs(dx) + abs(dz) > 1 else GRASS)
        if abs(dx) + abs(dz) <= 1:
          _set(v, cx + dx, sea + 2, cz + dz, GRASS)

  # Spruce tree on island
  _set(v, cx, sea + 3, cz, SLOG)
  _set(v, cx, sea + 4, cz, SLOG)
  for dx, dz in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1)):
    _set(v, cx + dx, sea + 5, cz + dz, SLEAF)
  _set(v, cx, sea + 6, cz, SLEAF)

  return v


def _generate_bite_greenhouse() -> np.ndarray:
  """
  Greenhouse — book dimensions (scaled for 32³):
    9×13 mud brick glass greenhouse, stone brick foundation, gabled roof,
    froglights, birch interior with spruce trapdoor planters.
  """
  GRASS = _b("grass_block")
  STONE = _b("stone_bricks")
  MOSSY = _b("mossy_stone_bricks")
  CRACKED = _b("cracked_stone_bricks")
  MUD = _b("mud_bricks")
  MSTAIR = _b("mud_brick_stairs")
  MSLAB = _b("mud_brick_slab")
  MWALL = _b("mud_brick_wall")
  PBUTTON = _b("polished_blackstone_button")
  GLASS = _b("glass_pane")
  CHAIN = _b("chain")
  FROG_P = _b("pearlescent_froglight")
  FROG_O = _b("ochre_froglight")
  FROG_V = _b("verdant_froglight")
  BIRCH = _b("birch_planks")
  DIRT = _b("dirt")
  BSTAIR = _b("birch_stairs")
  BARREL = _b("barrel")
  S_TRAP = _b("spruce_trapdoor")
  AZALEA = _b("flowering_azalea_leaves")
  POPPY = _b("poppy")
  CORNFLOWER = _b("cornflower")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 10, 1
  w, l, ph = 9, 13, 7
  pxs = [ox, ox + 2, ox + 4, ox + 6, ox + w - 1]

  # Grass pad
  for x in range(ox - 2, ox + w + 3):
    for z in range(oz - 2, oz + l + 3):
      _set(v, x, oy - 1, z, GRASS)

  # Stone brick foundation outline
  for x in range(ox, ox + w):
    for z in range(oz, oz + l):
      edge = x in (ox, ox + w - 1) or z in (oz, oz + l - 1)
      if edge:
        mat = (STONE, MOSSY, CRACKED)[(x + z) % 3]
        _set(v, x, oy, z, mat)

  # Mud brick pillars on both long sides
  for px in pxs:
    for pz in (oz, oz + l - 1):
      for y in range(1, ph + 1):
        _set(v, px, oy + y, pz, MUD)
      _set(v, px, oy + 1, pz, MSTAIR)
      _set(v, px, oy + 2, pz, PBUTTON)

  # Front archway entrance — 5 blocks tall
  arch_cx = ox + w // 2
  for y in range(1, 6):
    for ax in (arch_cx - 1, arch_cx, arch_cx + 1):
      if y == 5:
        _set(v, ax, oy + y, oz, MSLAB)
      elif ax in (arch_cx - 1, arch_cx + 1) or y < 4:
        _set(v, ax, oy + y, oz, MSTAIR if y == 1 else MUD)
    _set(v, arch_cx - 1, oy + 3, oz, PBUTTON)
    _set(v, arch_cx + 1, oy + 3, oz, PBUTTON)

  # Glass walls between pillars
  for pz in (oz, oz + l - 1):
    for i in range(len(pxs) - 1):
      x0, x1 = pxs[i], pxs[i + 1]
      for x in range(x0 + 1, x1):
        for y in range(2, ph):
          if pz == oz and arch_cx - 1 <= x <= arch_cx + 1 and y < 5:
            continue
          _set(v, x, oy + y, pz, GLASS)
  for px in (ox, ox + w - 1):
    for z in range(oz + 1, oz + l - 1):
      for y in range(2, ph):
        _set(v, px, oy + y, z, GLASS)

  # Gabled roof trusses and glass infill
  roof_base = oy + ph
  truss_zs = [oz + 2, oz + 5, oz + 8, oz + 11]
  for tz in truss_zs:
    peak_y = roof_base + 3
    for layer in range(4):
      y = roof_base + layer
      inset = layer
      for x in range(ox + inset, ox + w - inset):
        if x in pxs and layer == 0:
          _set(v, x, y, tz, MSTAIR)
        elif x == ox + inset or x == ox + w - 1 - inset:
          _set(v, x, y, tz, MSTAIR)
        else:
          _set(v, x, y, tz, MSLAB if layer == 3 else GLASS)
    # Exterior hanging froglights
    frog = (FROG_P, FROG_O, FROG_V)[(tz - oz) % 3]
    _set(v, arch_cx, roof_base + 2, tz, CHAIN)
    _set(v, arch_cx, roof_base + 1, tz, frog)

  # Interior checkered dirt and birch floor
  for x in range(ox + 1, ox + w - 1):
    for z in range(oz + 1, oz + l - 1):
      _set(v, x, oy + 1, z, BIRCH if (x + z) % 2 == 0 else DIRT)

  # Spruce trapdoor plant beds
  beds = ((ox + 2, oz + 3), (ox + 5, oz + 6), (ox + 3, oz + 9))
  for bx, bz in beds:
    for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
      _set(v, bx + dx, oy + 1, bz + dz, S_TRAP)
    plant = AZALEA if bx == ox + 3 else POPPY if (bx + bz) % 2 == 0 else CORNFLOWER
    _set(v, bx, oy + 2, bz, plant)

  # Birch stair workbench and barrels
  _set(v, ox + 6, oy + 1, oz + 4, BSTAIR)
  _set(v, ox + 7, oy + 1, oz + 4, BSTAIR)
  _set(v, ox + 6, oy + 1, oz + 3, BARREL)
  _set(v, ox + 7, oy + 1, oz + 3, BARREL)

  # Interior pearlescent froglights
  for ix, iz in ((ox + 4, oz + 4), (ox + 4, oz + 8)):
    _set(v, ix, roof_base + 1, iz, CHAIN)
    _set(v, ix, roof_base, iz, FROG_P)

  return v


def _steamboat_hull(rx: int, rz: int) -> bool:
  """22×9 pill-shaped hull footprint — book dimensions."""
  if not (0 <= rx < 22 and 0 <= rz < 9):
    return False
  cz = 4
  if rx < 3:
    half = min(3, rx + 1)
  elif rx >= 19:
    half = min(3, 21 - rx)
  else:
    half = 4
  return abs(rz - cz) <= half


def _generate_bite_steamboat() -> np.ndarray:
  """
  Steamboat — book dimensions:
    22×9 hull (1 block below water), 2-block central cabin, three birch slab
    decks, 7×7 roof, 5×5 paddle wheels, twin campfire chimneys.
  """
  WATER = _b("water")
  GRAY = _b("gray_concrete")
  BLACK = _b("black_concrete")
  GLASS = _b("glass")
  QUARTZ = _b("smooth_quartz")
  QSTAIR = _b("smooth_quartz_stairs")
  BSLAB = _b("birch_slab")
  RNWALL = _b("red_nether_brick_wall")
  RNBRICK = _b("red_nether_bricks")
  RNSTAIR = _b("red_nether_brick_stairs")
  BGATE = _b("birch_fence_gate")
  BARREL = _b("barrel")
  CHEST = _b("chest")
  BLAST = _b("blast_furnace")
  SMOKER = _b("smoker")
  GRIND = _b("grindstone")
  LADDER = _b("ladder")
  LANTERN = _b("lantern")
  O_TRAP = _b("oak_trapdoor")
  CAMP = _b("campfire")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz = 5, 12
  wl = 11  # water level; hull sits 1 block below
  hull_y = wl - 1
  deck1 = wl
  cabin_h = 2
  deck2 = deck1 + cabin_h + 1
  deck3 = deck2 + 3
  roof_y = deck3 + 3
  length, width = 22, 9
  cx, cz = ox + 11, oz + 4

  # River water
  for x in range(ox - 1, ox + length + 1):
    for z in range(oz - 3, oz + width + 3):
      for y in range(hull_y - 1, wl + 6):
        _set(v, x, y, z, WATER)

  # Step 1 — gray concrete hull with glass sides (22×9, 1 below water)
  for rx in range(length):
    for rz in range(width):
      if not _steamboat_hull(rx, rz):
        continue
      x, z = ox + rx, oz + rz
      _set(v, x, hull_y, z, GRAY)
      edge = rz in (0, 8) or not _steamboat_hull(rx, rz - 1 if rz > 0 else rz) or not _steamboat_hull(rx, min(rz + 1, 8))
      if rz in (0, 8) or rx in (0, 21):
        _set(v, x, hull_y, z, GLASS if rz in (1, 7) and 2 < rx < 19 else GRAY)

  # Step 2 — engine room interior at stern
  for rx in range(16, 20):
    for rz in range(2, 7):
      if _steamboat_hull(rx, rz):
        x, z = ox + rx, oz + rz
        mat = BLAST if rz < 4 else SMOKER if rz > 4 else BARREL
        _set(v, x, hull_y, z, mat if (rx + rz) % 2 == 0 else CHEST)
  _set(v, ox + 18, hull_y, cz, GRIND)
  _set(v, ox + 19, deck1, cz + 1, LADDER)

  # Step 3 — first deck floor: quartz border, birch slab center
  for rx in range(length):
    for rz in range(width):
      if not _steamboat_hull(rx, rz):
        continue
      x, z = ox + rx, oz + rz
      edge = rz in (0, 8) or rx in (0, 21) or not _steamboat_hull(rx, max(rz - 1, 0)) or not _steamboat_hull(rx, min(rz + 1, 8))
      _set(v, x, deck1, z, QUARTZ if edge else BSLAB)

  # Step 4 — 2-block central cabin with quartz stair windows
  cabin_x0, cabin_x1 = ox + 6, ox + 16
  cabin_z0, cabin_z1 = oz + 2, oz + 6
  for y in range(cabin_h):
    wy = deck1 + 1 + y
    for x in range(cabin_x0, cabin_x1 + 1):
      for z in range(cabin_z0, cabin_z1 + 1):
        edge = x in (cabin_x0, cabin_x1) or z in (cabin_z0, cabin_z1)
        if not edge:
          _set(v, x, wy, z, AIR_B)
          continue
        if z == cabin_z0 and x == cx:
          _set(v, x, wy, z, BGATE if y == 0 else AIR_B)
        elif y == 1 and z in (cabin_z0, cabin_z1) and cabin_x0 < x < cabin_x1:
          _set(v, x, wy, z, QSTAIR)
        elif x in (cabin_x0, cabin_x1) and cabin_z0 < z < cabin_z1 and y == 1:
          _set(v, x, wy, z, GLASS)
        else:
          _set(v, x, wy, z, QUARTZ if x in (cabin_x0, cabin_x1) else GRAY)

  # Deck 2 — birch slab floor and red nether brick wall railing
  for rx in range(length):
    for rz in range(width):
      if not _steamboat_hull(rx, rz):
        continue
      x, z = ox + rx, oz + rz
      inside_cabin = cabin_x0 <= x <= cabin_x1 and cabin_z0 <= z <= cabin_z1
      if inside_cabin:
        _set(v, x, deck2, z, BSLAB)
      elif rz in (0, 8) or rx in (0, 21):
        _set(v, x, deck2, z, BSLAB)
        _set(v, x, deck2 + 1, z, RNWALL)
        if (rx + rz) % 4 == 0:
          _set(v, x, deck2 + 2, z, QUARTZ)
          _set(v, x, deck2 + 3, z, LANTERN)

  # Stern gray concrete pillars
  for z in (cz - 1, cz + 1):
    for y in range(deck2, deck3 + 2):
      _set(v, ox + 19, y, z, GRAY)

  # Deck 2 furniture — quartz armchairs and oak trapdoors
  for fx, fz in ((ox + 8, cz - 2), (ox + 14, cz + 2)):
    _set(v, fx, deck2 + 1, fz, QUARTZ)
    for dx, dz in ((-1, 0), (1, 0)):
      _set(v, fx + dx, deck2 + 1, fz + dz, O_TRAP)

  # Deck 3 — birch floor, grindstone helm, ladder up
  for rx in range(8, 15):
    for rz in range(2, 7):
      if _steamboat_hull(rx, rz):
        _set(v, ox + rx, deck3, oz + rz, BSLAB)
  _set(v, ox + 7, deck3 + 1, cz, GRIND)
  _set(v, ox + 18, deck2 + 1, cz, LADDER)
  for px in (ox + 9, ox + 13):
    for y in range(deck3, roof_y):
      _set(v, px, y, cz, QUARTZ)

  # 7×7 birch slab roof (book dimension)
  for x in range(cx - 3, cx + 4):
    for z in range(cz - 3, cz + 4):
      _set(v, x, roof_y, z, BSLAB)

  # Twin campfire chimneys with oak trapdoor casing
  for sx in (cx - 1, cx + 1):
    _set(v, sx, roof_y + 1, cz + 1, CAMP)
    for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
      _set(v, sx + dx, roof_y + 1, cz + 1 + dz, O_TRAP)
    _set(v, sx, roof_y + 2, cz + 1, BLACK)
    _set(v, sx, roof_y + 3, cz + 1, BLACK)

  # 5×5 paddle wheels on both sides (book dimension)
  wheel_x = ox + 11
  for side_z in (oz - 1, oz + width):
    for dx in range(-2, 3):
      for dy in range(-2, 3):
        dist = abs(dx) + abs(dy)
        if dist > 3:
          continue
        wy = deck1 + 1 + dy
        if dx == 0 and dy == 0:
          _set(v, wheel_x + dx, wy, side_z, QUARTZ)
        elif abs(dx) == abs(dy):
          _set(v, wheel_x + dx, wy, side_z, RNSTAIR)
        else:
          _set(v, wheel_x + dx, wy, side_z, RNBRICK)

  return v


def _pachinko_bullseye(dx: int, dz: int) -> str:
  """9×9 concentric target pattern — book step 3."""
  d = max(abs(dx - 4), abs(dz - 4))
  if dx == 4 and dz == 4:
    return "white"
  if d <= 1:
    return "yellow"
  if d == 2:
    return "red"
  if d == 3:
    return "light_blue"
  return "white"


def _generate_bite_parkour_pachinko() -> np.ndarray:
  """
  Parkour Pachinko Game — book dimensions:
    11×6×4 U-shaped base, 9×9 bullseye back wall, 8-block circular frame,
    lava floor parkour platforms sticky piston circuit and striped roof.
  """
  GRASS = _b("grass_block")
  WHITE = _b("smooth_quartz")
  QSTAIR = _b("smooth_quartz_stairs")
  LBLUE = _b("light_blue_concrete")
  YELLOW = _b("yellow_concrete")
  RED = _b("red_concrete")
  ORANGE = _b("orange_concrete")
  BLUE = _b("blue_concrete")
  DBRICK = _b("deepslate_bricks")
  DSTAIR = _b("deepslate_brick_stairs")
  DSLAB = _b("deepslate_brick_slab")
  DWALL = _b("deepslate_brick_wall")
  PISTON = _b("sticky_piston")
  DUST = _b("redstone_dust")
  BBUTTON = _b("birch_button")
  LAVA = _b("lava")
  LADDER = _b("ladder")
  LANTERN = _b("sea_lantern")
  IDOOR = _b("iron_door")
  RCARPET = _b("red_carpet")
  WCARPET = _b("white_carpet")
  AIR_B = AIR
  mats = {
    "white": WHITE,
    "yellow": YELLOW,
    "red": RED,
    "light_blue": LBLUE,
  }

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 12, 2
  bw, bd, bh = 11, 6, 4
  back_z = oz + bd - 1
  cx = ox + bw // 2
  wall_y0 = oy + bh
  wall_h = 9
  frame_r = 4  # 8-block diameter circular frame

  # Grass pad
  for x in range(ox - 1, ox + bw + 2):
    for z in range(oz - 1, oz + bd + 2):
      _set(v, x, oy - 1, z, GRASS)

  # Step 1 — 11×6×4 U-shaped quartz base with corner stripes
  for y in range(bh):
    wy = oy + y
    for x in range(ox, ox + bw):
      for z in range(oz, oz + bd):
        on_back = z == back_z
        on_left = x == ox
        on_right = x == ox + bw - 1
        if not (on_back or on_left or on_right):
          continue
        corner = (x, z) in ((ox, oz), (ox + bw - 1, oz), (ox, back_z), (ox + bw - 1, back_z))
        if corner:
          stripe = YELLOW if x == ox else LBLUE
          _set(v, x, wy, z, stripe if y % 2 == 0 else WHITE)
        else:
          _set(v, x, wy, z, WHITE)

  # Step 3 — 9×9 bullseye back wall
  wx0 = ox + 1
  for dy in range(wall_h):
    for dx in range(9):
      for dz in range(9):
        key = _pachinko_bullseye(dx, dz)
        _set(v, wx0 + dx, wall_y0 + dy, back_z, mats[key])

  # Step 2 — sticky piston circuit on left side wall
  py, pz = oy + 2, oz + 3
  _set(v, ox, py, pz, PISTON)
  _set(v, ox + 1, py, pz, RED)
  _set(v, ox, py, pz - 1, DUST)
  _set(v, ox, py + 1, pz - 1, BBUTTON)

  # Circular deepslate frame at front opening (8-block diameter)
  for z in range(oz, oz + bd):
    for x in range(ox, ox + bw):
      dx, dz = x - cx, z - (oz + bd // 2)
      dist = (dx * dx + dz * dz) ** 0.5
      if frame_r - 0.6 <= dist <= frame_r + 0.6:
        for y in range(oy + 1, wall_y0 + wall_h):
          _set(v, x, y, z, DWALL if y < wall_y0 + 4 else DSTAIR if y % 2 == 0 else DSLAB)

  # Interior lava floor
  for x in range(ox + 2, ox + bw - 2):
    for z in range(oz + 1, back_z):
      _set(v, x, oy + 1, z, LAVA)

  # Parkour platforms and quartz corner stairs
  platforms = (
    (ox + 3, oy + 3, oz + 2, BLUE),
    (ox + 7, oy + 5, oz + 3, RED),
    (ox + 5, oy + 7, oz + 4, ORANGE),
    (ox + 8, oy + 9, oz + 2, BLUE),
    (ox + 4, oy + 11, oz + 3, RED),
  )
  for px, py, pz, mat in platforms:
    _set(v, px, py, pz, mat)
  for corner in ((ox + 2, oz + 2), (ox + bw - 3, oz + 2)):
    _set(v, corner[0], oy + 4, corner[1], QSTAIR)
    _set(v, corner[0], oy + 8, corner[1], QSTAIR)

  # Sea lantern corner lights
  for lx, lz in ((ox + 2, oz + 2), (ox + bw - 3, oz + 2), (ox + 2, back_z - 1), (ox + bw - 3, back_z - 1)):
    _set(v, lx, oy + 6, lz, LANTERN)

  # Ladder on back wall inside frame
  for y in range(oy + 4, wall_y0 + wall_h - 1):
    _set(v, cx, y, back_z - 1, LADDER)

  # Roof — deepslate wall cap and red white striped awning
  roof_y = wall_y0 + wall_h
  for x in range(ox, ox + bw):
    for z in range(oz, oz + bd):
      _set(v, x, roof_y, z, WHITE)
      if x in (ox, ox + bw - 1) or z in (oz, back_z):
        _set(v, x, roof_y + 1, z, DWALL)
      inner = (ox + 1 <= x <= ox + bw - 2) and (oz + 1 <= z <= back_z - 1)
      if inner:
        _set(v, x, roof_y, z, RCARPET if (x + z) % 2 == 0 else WCARPET)

  # Roof ladder access
  _set(v, cx, roof_y + 1, oz + 2, AIR_B)
  _set(v, cx, roof_y + 2, oz + 2, LADDER)

  # Side entrance — iron door, button, quartz stairs
  door_x = ox + bw - 1
  door_z = oz + 2
  _set(v, door_x, oy + 1, door_z, IDOOR)
  _set(v, door_x, oy + 2, door_z, IDOOR)
  _set(v, door_x, oy + 2, door_z + 1, BBUTTON)
  _set(v, door_x + 1, oy + 1, door_z, QSTAIR)
  _set(v, door_x + 1, oy, door_z, QSTAIR)

  return v


def _generate_bite_horse_racecourse() -> np.ndarray:
  """
  Horse Racecourse — book dimensions:
    17×9 starting grid, 8-wide piston gate, starting arch, 12×12 ninety-degree
    turn, nether brick quartz grandstand, and trackside fences.
  """
  GRASS = _b("grass_block")
  TRACK = _b("gray_concrete")
  WHITE = _b("white_concrete")
  LGRAY = _b("light_gray_concrete")
  CPOWDER_W = _b("white_concrete_powder")
  CPOWDER_G = _b("light_gray_concrete_powder")
  RED = _b("red_concrete")
  DUST = _b("redstone_dust")
  PISTON = _b("piston")
  LEVER = _b("lever")
  NBRICK = _b("nether_bricks")
  CHISEL = _b("chiseled_nether_bricks")
  NWALL = _b("nether_brick_wall")
  NFENCE = _b("nether_brick_fence")
  NSTAIR = _b("nether_brick_stairs")
  NSLAB = _b("nether_brick_slab")
  QSTAIR = _b("smooth_quartz_stairs")
  QSLAB = _b("smooth_quartz_slab")
  BBANNER = _b("black_banner")
  WBANNER = _b("white_banner")
  LANTERN = _b("lantern")
  CHEST = _b("chest")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 6, 11, 2
  grid_l, grid_w = 17, 9
  turn_size = 12

  # Grass field
  for x in range(ox - 2, ox + grid_l + turn_size):
    for z in range(oz - 2, oz + grid_w + turn_size + 2):
      _set(v, x, oy - 1, z, GRASS)

  def on_track(x: int, z: int) -> bool:
    if ox <= x < ox + grid_l and oz <= z < oz + grid_w:
      return True
    if ox + grid_l - turn_size <= x < ox + grid_l and oz + grid_w - 1 <= z < oz + grid_w - 1 + turn_size:
      return True
    return False

  # 17×9 starting grid straight (book dimension)
  for x in range(ox, ox + grid_l):
    for z in range(oz, oz + grid_w):
      _set(v, x, oy, z, TRACK)
  for lane_z in (oz + 2, oz + 4, oz + 6):
    for x in range(ox + 2, ox + grid_l - 2, 4):
      _set(v, x, oy, lane_z, WHITE)

  # 2×6 checkered start line under arch
  for dx in range(2):
    for dz in range(6):
      mat = WHITE if (dx + dz) % 2 == 0 else TRACK
      _set(v, ox + dx, oy, oz + 1 + dz, mat)

  # 8-wide retractable gate — 3 blocks below surface (book dimension)
  gate_z0 = oz + 1
  for i in range(7):
    gz = gate_z0 + i
    _set(v, ox, oy - 3, gz, WHITE)
    _set(v, ox, oy - 2, gz, DUST)
    _set(v, ox, oy - 1, gz, PISTON)
    for gy in range(2):
      powder = CPOWDER_G if (i + gy) % 2 == 0 else CPOWDER_W
      _set(v, ox, oy + gy, gz, powder)
  lever_z = gate_z0 + 7
  _set(v, ox, oy - 3, lever_z, WHITE)
  _set(v, ox, oy - 2, lever_z, WHITE)
  _set(v, ox, oy - 1, lever_z, WHITE)
  _set(v, ox, oy, lever_z, WHITE)
  _set(v, ox, oy + 1, lever_z, LEVER)

  # Starting arch — chiseled pillars, nether brick slab arch, banners, lanterns
  for pz in (oz - 1, oz + grid_w):
    _set(v, ox, oy, pz, CHISEL)
    for y in range(1, 3):
      _set(v, ox, oy + y, pz, NWALL)
    _set(v, ox, oy + 3, pz, NBRICK)
    _set(v, ox, oy + 3, pz + (1 if pz < oz else -1), LANTERN)
    _set(v, ox - 1, oy, pz, LEVER)
  for dz in range(-1, grid_w + 1):
    z = oz + dz
    _set(v, ox, oy + 3, z, NSLAB if dz % 2 == 0 else NBRICK)
    if 0 <= dz < 6:
      _set(v, ox, oy + 2, z, BBANNER if dz % 2 == 0 else WBANNER)

  # 12×12 ninety-degree turn with red white curbing (book dimension)
  tx0 = ox + grid_l - turn_size
  tz0 = oz + grid_w - 1
  for x in range(tx0, tx0 + turn_size):
    for z in range(tz0, tz0 + turn_size):
      if x < ox + grid_l - 1 or z > tz0:
        _set(v, x, oy, z, TRACK)
      outer = x == tx0 or z == tz0 + turn_size - 1
      if outer and on_track(x, z):
        _set(v, x, oy, z, RED if (x + z) % 2 == 0 else WHITE)

  # Stadium grandstand — 7×5 tiers (book dimension)
  sx, sz = ox + 3, oz + grid_w + 1
  for x in range(sx, sx + 7):
    for z in range(sz, sz + 5):
      _set(v, x, oy - 1, z, NBRICK)
  for tier in range(3):
    tz = sz + tier
    for x in range(sx + 1, sx + 6):
      _set(v, x, oy + tier, tz, NSTAIR)
      _set(v, x, oy + tier + 1, tz, QSTAIR)
  for x in (sx, sx + 6):
    for y in range(1, 4):
      _set(v, x, oy + y, sz + 4, CHISEL if y == 3 else NBRICK)
      if y < 3:
        _set(v, x, oy + y, sz + 4, NFENCE)
  for x in range(sx, sx + 7):
    _set(v, x, oy + 4, sz + 4, QSLAB)
    if x % 2 == 0:
      _set(v, x, oy + 3, sz + 3, LANTERN)
  for y in range(3):
    _set(v, sx + 6, oy + y, sz + 2, NSTAIR)
  _set(v, sx + 7, oy, sz + 2, CHEST)

  # Trackside nether brick fences
  for x in range(ox, ox + grid_l, 4):
    for pz in (oz - 2, oz + grid_w + 1):
      _set(v, x, oy - 1, pz, NBRICK)
      _set(v, x, oy, pz, CHISEL)
      _set(v, x, oy + 1, pz, NFENCE)

  return v


def _skull_entrance_half_width(rel_y: int) -> int:
  """11-block entrance — bottom 4 at 7 wide, top 7 at 9 wide (book dimensions)."""
  return 3 if rel_y < 4 else 4  # half-width: 7 wide = ±3, 9 wide = ±4


def _generate_bite_skull_cove() -> np.ndarray:
  """
  Skull Cove — book dimensions:
    20×15×13 cliff, 12 deep cove, 11 tall entrance (top 9w bottom 7w),
    smooth quartz skull facade, jungle dock, soul lantern treasure room.
  """
  STONE = _b("stone")
  DIRT = _b("dirt")
  GRASS = _b("grass_block")
  WATER = _b("water")
  QUARTZ = _b("smooth_quartz")
  QSLAB = _b("smooth_quartz_slab")
  QSTAIR = _b("smooth_quartz_stairs")
  JPLANK = _b("jungle_planks")
  JSLAB = _b("jungle_slab")
  JSTAIR = _b("jungle_stairs")
  JFENCE = _b("jungle_fence")
  LEAVES = _b("jungle_leaves")
  VINE = _b("vine")
  SFENCE = _b("spruce_fence")
  SLANTERN = _b("soul_lantern")
  GOLD = _b("gold_block")
  CHEST = _b("chest")
  SAND = _b("sand")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 6, 8, 2
  cw, ch, cd = 20, 15, 13
  cx = ox + cw // 2
  wl = oy + 3
  mouth_y0 = wl
  cove_depth = 12
  face_z = oz

  # Water in front of cliff
  for x in range(ox - 1, ox + cw + 1):
    for z in range(face_z - 4, face_z):
      _set(v, x, wl, z, WATER)
      _set(v, x, wl - 1, z, WATER)

  # Cliff mass — stone with grass top
  for x in range(ox, ox + cw):
    for z in range(oz, oz + cd):
      for y in range(oy, oy + ch):
        _set(v, x, y, z, STONE if y < oy + ch - 2 else DIRT if y < oy + ch - 1 else GRASS)

  # Cove excavation — 12 blocks deep, stepped entrance (book dimensions)
  for dz in range(cove_depth):
    z = face_z + dz
    for rel_y in range(11):
      y = mouth_y0 + rel_y
      hw = _skull_entrance_half_width(rel_y)
      for x in range(cx - hw, cx + hw + 1):
        _set(v, x, y, z, AIR_B)
    # Widen floor chamber inside
    if dz >= 2:
      for x in range(cx - 5, cx + 6):
        for y in range(mouth_y0, mouth_y0 + 8):
          _set(v, x, y, z, AIR_B)

  # Interior sand treasure beach
  for x in range(cx - 4, cx + 5):
    for z in range(face_z + 4, face_z + cove_depth):
      _set(v, x, mouth_y0, z, SAND)
  for x, z in ((cx - 2, face_z + 8), (cx + 2, face_z + 10), (cx, face_z + 6)):
    _set(v, x, mouth_y0 + 1, z, GOLD)
  for x, z in ((cx - 3, face_z + 7), (cx + 3, face_z + 9)):
    _set(v, x, mouth_y0 + 1, z, CHEST)

  # Soul lantern ceiling lights
  for lx in (cx - 3, cx, cx + 3):
    for lz in (face_z + 5, face_z + 9):
      _set(v, lx, mouth_y0 + 7, lz, SFENCE)
      _set(v, lx, mouth_y0 + 6, lz, SLANTERN)

  # Jungle dock platform through skull mouth
  for x in range(cx - 3, cx + 4):
    for z in range(face_z - 2, face_z + 5):
      _set(v, x, wl + 1, z, JPLANK if z >= face_z else JSLAB)
      if z == face_z - 2:
        _set(v, x, wl + 2, z, JFENCE)
  for side_x in (cx - 3, cx + 3):
    _set(v, side_x, wl + 1, face_z - 1, JSTAIR)

  # Skull jaw — quartz teeth with 2-block boat gap (book step 2)
  for tooth_x in (cx - 3, cx + 3):
    _set(v, tooth_x, wl, face_z - 1, QUARTZ)
    _set(v, tooth_x, wl + 1, face_z - 1, QUARTZ)
  for x in range(cx - 2, cx + 3):
    _set(v, x, wl, face_z - 1, QSLAB)
    _set(v, x, wl + 1, face_z - 1, QSTAIR)

  # Cheekbones and nose hole (book step 3)
  for cheek_x, sign in ((cx - 5, -1), (cx + 5, 1)):
    for y in range(mouth_y0 + 2, mouth_y0 + 7):
      _set(v, cheek_x, y, face_z - 1, QUARTZ)
      _set(v, cheek_x + sign, y, face_z - 1, QSLAB if y % 2 else QSTAIR)
  for y in range(mouth_y0 + 4, mouth_y0 + 6):
    _set(v, cx, y, face_z - 1, AIR_B)
    _set(v, cx - 1, y, face_z - 1, QSLAB)
    _set(v, cx + 1, y, face_z - 1, QSLAB)

  # Eye sockets — recessed 3×3 arches (book step 4)
  for eye_x in (cx - 4, cx + 4):
    for y in range(mouth_y0 + 6, mouth_y0 + 10):
      for dz in (-1, 0):
        _set(v, eye_x, y, face_z + dz, AIR_B)
      _set(v, eye_x, y, face_z - 1, QSTAIR if y == mouth_y0 + 9 else QUARTZ)
    _set(v, eye_x, mouth_y0 + 5, face_z - 1, QSLAB)

  # Forehead and cranium cap (book step 5)
  for x in range(cx - 5, cx + 6):
    for y in range(mouth_y0 + 9, mouth_y0 + 13):
      _set(v, x, y, face_z - 1, QUARTZ if abs(x - cx) <= 4 else QSLAB)
  for x in range(cx - 4, cx + 5):
    _set(v, x, mouth_y0 + 13, face_z - 1, QSLAB)

  # Overgrowth — jungle leaves and vines (book step 6)
  for x in range(ox + 2, ox + cw - 2, 3):
    for z in (face_z - 1, oz + 2):
      _set(v, x, oy + ch - 1, z, LEAVES)
      _set(v, x, oy + ch - 2, z, VINE)
  for lx, ly in ((cx - 6, mouth_y0 + 11), (cx + 6, mouth_y0 + 10), (cx, mouth_y0 + 12)):
    _set(v, lx, ly, face_z - 1, LEAVES)
    _set(v, lx, ly - 1, face_z, VINE)

  return v


def _side_wall_height(rel_z: int, depth: int) -> int:
  """Staggered side wall tops — 3 at edges, 5 at center (book page 68)."""
  center = depth // 2
  dist = abs(rel_z - center)
  if dist == 0:
    return 5
  if dist == 1:
    return 4
  return 3


def _generate_bite_potion_factory() -> np.ndarray:
  """
  Potion Factory — book dimensions:
    15×11 footprint, 8 dark oak pillars (mid-long 5 tall), calcite copper walls,
    12 block main chimney, crimson gabled roof, brewing lab interior.
  """
  NYLIUM = _b("crimson_nylium")
  DOAK = _b("stripped_dark_oak_log")
  DSTAIR = _b("dark_oak_stairs")
  DOAK_PLANK = _b("dark_oak_planks")
  DOAK_SLAB = _b("dark_oak_slab")
  CALCITE = _b("calcite")
  COPPER = _b("oxidized_cut_copper")
  CSLAB = _b("oxidized_cut_copper_slab")
  CSTAIR = _b("oxidized_cut_copper_stairs")
  CRIMSON = _b("crimson_planks")
  CSTAIR_R = _b("crimson_stairs")
  CSLAB_R = _b("crimson_slab")
  CDOOR = _b("crimson_door")
  CTRAP = _b("crimson_trapdoor")
  OGLASS = _b("orange_stained_glass_pane")
  SOUL = _b("soul_sand")
  WART = _b("nether_wart")
  CAMP = _b("campfire")
  LANTERN = _b("lantern")
  AZALEA = _b("flowering_azalea_leaves")
  BREW = _b("brewing_stand")
  CAULDRON = _b("cauldron")
  WATER = _b("water")
  BARREL = _b("barrel")
  CRAFT = _b("crafting_table")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 10, 2
  length, depth = 15, 11
  door_x = ox + length // 2

  # Crimson forest ground pad
  for x in range(ox - 2, ox + length + 2):
    for z in range(oz - 2, oz + depth + 2):
      _set(v, x, oy - 1, z, NYLIUM)
      if (x + z) % 5 == 0:
        _set(v, x, oy, z, AZALEA)

  # Eight pillars — corners 4 tall, mid-long sides 5 tall (book step 1)
  pillars = (
    (ox, oz, 4), (ox + length - 1, oz, 4),
    (ox, oz + depth - 1, 4), (ox + length - 1, oz + depth - 1, 4),
    (ox + length // 2, oz, 5), (ox + length // 2, oz + depth - 1, 5),
    (ox, oz + depth // 2, 4), (ox + length - 1, oz + depth // 2, 4),
  )
  for px, pz, ph in pillars:
    for y in range(ph):
      _set(v, px, oy + y, pz, DOAK)
    _set(v, px, oy - 1, pz, DSTAIR)

  # Two-block wall rings — calcite bottom, copper top (book step 2)
  for x in range(ox, ox + length):
    for z in range(oz, oz + depth):
      edge = x in (ox, ox + length - 1) or z in (oz, oz + depth - 1)
      if not edge:
        continue
      if z == oz and abs(x - door_x) <= 1:
        continue
      _set(v, x, oy, z, CALCITE)
      _set(v, x, oy + 1, z, COPPER)

  # Staggered side walls on 11-block sides
  for side_x in (ox, ox + length - 1):
    for rz in range(depth):
      z = oz + rz
      top = _side_wall_height(rz, depth)
      for y in range(2, top):
        _set(v, side_x, oy + y, z, CALCITE if y < 3 else COPPER)

  # Front/back walls 3 blocks tall (skip door)
  for x in range(ox + 1, ox + length - 1):
    for z in (oz, oz + depth - 1):
      if z == oz and abs(x - door_x) <= 1:
        continue
      for y in range(2, 3):
        _set(v, x, oy + y, z, CALCITE if y == 2 else COPPER)

  # Hollow interior + calcite floor
  for x in range(ox + 1, ox + length - 1):
    for z in range(oz + 1, oz + depth - 1):
      for y in range(oy + 2, oy + 6):
        _set(v, x, y, z, AIR_B)
      _set(v, x, oy, z, CALCITE)

  # Crimson trim, orange glass windows, soul sand nether wart planters
  for x in range(ox + 2, ox + length - 2, 3):
    for z in (oz, oz + depth - 1):
      if z == oz and abs(x - door_x) <= 2:
        continue
      _set(v, x, oy + 1, z, SOUL)
      _set(v, x, oy + 2, z, OGLASS)
      _set(v, x, oy + 3, z, CSTAIR_R)
      trap_z = z - 1 if z == oz + depth - 1 else z + 1
      if oz < trap_z < oz + depth:
        _set(v, x, oy + 1, trap_z, CTRAP)

  # Main chimney — 3×3, 12 blocks tall (book step 3)
  chx, chz = ox + length - 4, oz + depth - 4
  for y in range(12):
    for dx in range(3):
      for dz in range(3):
        edge = dx in (0, 2) or dz in (0, 2)
        if y < 2 and dx == 1 and dz == 1:
          _set(v, chx + dx, oy + y, chz + dz, AIR_B)
        elif edge or y >= 10:
          mat = CSTAIR if y >= 10 and (dx + dz) % 2 else CSLAB if y >= 10 else COPPER
          _set(v, chx + dx, oy + y, chz + dz, mat)
  _set(v, chx + 1, oy + 12, chz + 1, CAMP)
  for dx, dz in ((0, 1), (2, 1), (1, 0), (1, 2)):
    _set(v, chx + dx, oy + 12, chz + dz, CTRAP)

  # Secondary chimney — ~6 blocks tall
  ch2x, ch2z = ox + 2, oz + depth - 4
  for y in range(6):
    for dx in range(2):
      for dz in range(2):
        _set(v, ch2x + dx, oy + y, ch2z + dz, COPPER if y < 5 else CSLAB)
  _set(v, ch2x, oy + 6, ch2z, CAMP)

  # Crimson gabled roof with dark oak cross beam
  roof_base = oy + 5
  for x in range(ox, ox + length):
    for z in range(oz, oz + depth):
      rel_z = z - oz
      peak = _side_wall_height(rel_z, depth)
      for layer in range(2):
        y = roof_base + layer
        inset = layer
        if ox + inset <= x <= ox + length - 1 - inset and oz + inset <= z <= oz + depth - 1 - inset:
          if x == ox + length // 2 and z == oz + depth // 2 and layer == 0:
            _set(v, x, y, z, DOAK)
          else:
            _set(v, x, y, z, CSTAIR_R if layer else CRIMSON)
  for x in range(ox + 1, ox + length - 1):
    _set(v, x, roof_base + 2, oz + depth // 2, CSLAB_R)

  # Front porch crimson door and trapdoor shutters
  _set(v, door_x, oy + 1, oz, CDOOR)
  _set(v, door_x, oy + 2, oz, CDOOR)
  for dx in (-2, 2):
    _set(v, door_x + dx, oy + 2, oz, CTRAP)

  # Corner lanterns
  for px, pz in ((ox, oz), (ox + length - 1, oz), (ox, oz + depth - 1), (ox + length - 1, oz + depth - 1)):
    _set(v, px, oy + 4, pz, LANTERN)

  # Brewing lab interior (book page 71)
  for bx in range(ox + 3, ox + 9):
    _set(v, bx, oy + 1, oz + 3, DOAK_SLAB)
    _set(v, bx, oy + 2, oz + 3, BREW)
  _set(v, ox + 2, oy + 1, oz + depth - 3, CAULDRON)
  _set(v, ox + 2, oy + 1, oz + depth - 4, CAULDRON)
  for bx, bz in ((ox + 2, oz + 2), (ox + length - 3, oz + 2), (ox + length - 3, oz + depth - 3)):
    _set(v, bx, oy + 1, bz, BARREL)
  _set(v, ox + 5, oy + 1, oz + 5, CRAFT)
  _set(v, ox + 7, oy + 2, oz + 6, AZALEA)
  _set(v, chx + 1, oy + 1, chz + 1, CAMP)

  return v


def _generate_bite_monster_truck_bus() -> np.ndarray:
  """
  Monster-Truck Bus — book dimensions:
    13×8 wheelbase, stone brick axles, 13×4 black concrete chassis,
    yellow body warped roof, 4 furnaces grille, party-bus purpur interior.
  """
  GRASS = _b("grass_block")
  LODE = _b("lodestone")
  BLACK = _b("blackstone")
  BSTAIR = _b("blackstone_stairs")
  SBWALL = _b("stone_brick_wall")
  BCONC = _b("black_concrete")
  YELLOW = _b("yellow_concrete")
  PBSTAIR = _b("polished_blackstone_brick_stairs")
  PBSLAB = _b("polished_blackstone_brick_slab")
  WPLANK = _b("warped_planks")
  WSTAIR = _b("warped_stairs")
  WSLAB = _b("warped_slab")
  WSIGN = _b("warped_sign")
  WDOOR = _b("warped_door")
  WBUTTON = _b("warped_button")
  TGLASS = _b("tinted_glass")
  FURNACE = _b("furnace")
  GFRAME = _b("glow_item_frame")
  IBAR = _b("iron_bars")
  RED = _b("redstone_block")
  LADDER = _b("ladder")
  PURPUR = _b("purpur_block")
  PSTAIR = _b("purpur_stairs")
  LIME = _b("lime_concrete")
  MAGENTA = _b("magenta_concrete")
  ROD = _b("end_rod")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 12, 2
  wheel_l, wheel_w = 13, 8
  cx0, cx1 = ox, ox + wheel_l - 1
  cz0, cz1 = oz, oz + wheel_w - 1
  chassis_z0, chassis_z1 = oz + 2, oz + 5  # 13×4 platform centered on 8-wide base

  # Grass pad
  for x in range(ox - 1, ox + wheel_l + 1):
    for z in range(oz - 1, oz + wheel_w + 2):
      _set(v, x, oy - 1, z, GRASS)

  # Step 1 — four 3×3 mega wheels (lodestone hub, blackstone edges, stair corners)
  wheel_pts = ((cx0, cz0), (cx0, cz1), (cx1, cz0), (cx1, cz1))
  for wx, wz in wheel_pts:
    for wy in (oy, oy + 1, oy + 2):
      for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
          if dx == 0 and dz == 0:
            _set(v, wx + dx, wy, wz + dz, LODE if wy == oy + 1 else BLACK)
          elif dx == 0 or dz == 0:
            _set(v, wx + dx, wy, wz + dz, BLACK)
          else:
            _set(v, wx + dx, wy, wz + dz, BSTAIR)

  # Step 2 — stone brick wall axles front and back
  for wz in range(chassis_z0, chassis_z1 + 1):
    _set(v, cx0, oy + 1, wz, SBWALL)
    _set(v, cx1, oy + 1, wz, SBWALL)

  # Step 3 — 13×4 black concrete chassis platform
  for x in range(ox, ox + wheel_l):
    for z in range(chassis_z0, chassis_z1 + 1):
      _set(v, x, oy + 2, z, BCONC)

  # Body shell — yellow concrete walls with tinted glass windows
  body_y0, body_y1 = oy + 3, oy + 6
  for y in range(body_y0, body_y1 + 1):
    for x in range(ox + 1, ox + wheel_l - 1):
      for z in range(chassis_z0, chassis_z1 + 1):
        edge = x in (ox + 1, ox + wheel_l - 2) or z in (chassis_z0, chassis_z1)
        if not edge:
          _set(v, x, y, z, AIR_B)
          continue
        if y == body_y0 + 1 and z in (chassis_z0, chassis_z1) and ox + 3 < x < ox + wheel_l - 4:
          _set(v, x, y, z, TGLASS)
        elif x == ox + 1 and z == chassis_z0 + 1 and y <= body_y0 + 1:
          continue  # windshield
        else:
          _set(v, x, y, z, YELLOW)

  # Polished blackstone trim at body base and crown
  for x in range(ox, ox + wheel_l):
    for z in range(chassis_z0 - 1, chassis_z1 + 2):
      if chassis_z0 <= z <= chassis_z1 or x in (ox, ox + wheel_l - 1):
        _set(v, x, body_y0 - 1, z, PBSTAIR if z in (chassis_z0 - 1, chassis_z1 + 1) else PBSLAB)

  # Warped side stripe above chassis (book page 64)
  for x in range(ox + 1, ox + wheel_l - 1):
    for z in (chassis_z0 - 1, chassis_z1 + 1):
      _set(v, x, body_y0 - 1, z, WPLANK)

  # Front hood — 8 yellow blocks and 4 furnace grille (book)
  for x in range(ox, ox + 4):
    for z in range(chassis_z0, chassis_z1 + 1):
      _set(v, x, body_y0, z, YELLOW)
      if x < 4:
        _set(v, x, body_y0 + 1, z, FURNACE if z in (chassis_z0 + 1, chassis_z1 - 1) else YELLOW)
  for z in (chassis_z0, chassis_z1):
    _set(v, ox, body_y0 + 1, z, GFRAME)
    _set(v, ox, body_y0 + 2, z, WSIGN)

  # Dashboard — black concrete row inside
  for z in range(chassis_z0, chassis_z1 + 1):
    _set(v, ox + 4, body_y0 + 1, z, BCONC)

  # Warped roof layers
  roof_y = body_y1 + 1
  for x in range(ox, ox + wheel_l):
    for z in range(chassis_z0 - 1, chassis_z1 + 2):
      _set(v, x, roof_y, z, WPLANK if (x + z) % 2 == 0 else WSLAB)
      if x in (ox, ox + wheel_l - 1) or z in (chassis_z0 - 1, chassis_z1 + 1):
        _set(v, x, roof_y + 1, z, WSTAIR)

  # Indicator light — iron bar and redstone block
  _set(v, ox + 2, roof_y + 1, chassis_z1 + 1, IBAR)
  _set(v, ox + 2, roof_y + 2, chassis_z1 + 1, RED)

  # Side ladder entry
  side_x = ox + wheel_l // 2
  for y in range(body_y0, body_y1 + 1):
    _set(v, side_x, y, cz1 + 1, LADDER)

  # Rear warped door and buttons
  rear_x = ox + wheel_l - 1
  mid_z = (chassis_z0 + chassis_z1) // 2
  _set(v, rear_x, body_y0, mid_z, WDOOR)
  _set(v, rear_x, body_y0 + 1, mid_z, WDOOR)
  _set(v, rear_x, body_y0 + 1, mid_z + 1, WBUTTON)
  _set(v, rear_x, body_y0 + 1, mid_z - 1, WBUTTON)

  # Party-bus interior — purpur lime magenta floor (book page 65)
  floor_mats = (PURPUR, LIME, MAGENTA)
  for x in range(ox + 2, ox + wheel_l - 2):
    for z in range(chassis_z0 + 1, chassis_z1):
      _set(v, x, body_y0, z, floor_mats[(x + z) % 3])

  # Purpur stair seats in rows
  for row_x in (ox + 5, ox + 8, ox + 10):
    for z in (chassis_z0 + 1, chassis_z1 - 1):
      _set(v, row_x, body_y0 + 1, z, PSTAIR)

  # End rod overhead grab bars
  for x in range(ox + 3, ox + wheel_l - 3, 2):
    _set(v, x, body_y1, chassis_z0 + 1, ROD)
    _set(v, x, body_y1, chassis_z1 - 1, ROD)

  return v


def _generate_bite_wishing_well() -> np.ndarray:
  """
  Wishing Well — book dimensions:
    6×3 hole 6 blocks deep, 3×3 stone well, redstone hopper comparator
    torch elevator dispenser reward, warped roof lantern azalea decor.
  """
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  SBRICK = _b("stone_bricks")
  MOSSY_B = _b("mossy_stone_bricks")
  MCOBBLE = _b("mossy_cobblestone")
  SWALL = _b("stone_brick_wall")
  SSLAB = _b("stone_brick_slab")
  WPLANK = _b("warped_planks")
  WSLAB = _b("warped_slab")
  CHEST = _b("chest")
  HOPPER = _b("hopper")
  COMP = _b("comparator")
  DUST = _b("redstone_dust")
  RTORCH = _b("redstone_torch")
  DISP = _b("dispenser")
  LANTERN = _b("lantern")
  MCARPET = _b("moss_carpet")
  AZBUSH = _b("flowering_azalea")
  AZLEAF = _b("azalea_leaves")
  STONE = _b("stone")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 14, 8
  hole_l, hole_w, hole_d = 6, 3, 6
  cx, cz = ox + 3, oz + 1

  # Grass surface around excavation
  for x in range(ox - 2, ox + hole_l + 2):
    for z in range(oz - 2, oz + hole_w + 2):
      _set(v, x, oy, z, GRASS)

  # 6×3 hole, 6 blocks deep (book excavation)
  for x in range(ox, ox + hole_l):
    for z in range(oz, oz + hole_w):
      for y in range(oy - hole_d, oy):
        _set(v, x, y, z, DIRT if y < oy - 3 else AIR_B)

  # Signal receiver — chest hopper comparator at hole end
  rx, rz = ox, oz
  _set(v, rx, oy - hole_d, rz, CHEST)
  _set(v, rx, oy - hole_d + 1, rz, HOPPER)
  _set(v, rx + 1, oy - hole_d + 1, rz, COMP)
  _set(v, rx + 2, oy - hole_d + 1, rz, STONE)
  _set(v, rx + 2, oy - hole_d + 2, rz, RTORCH)

  # Redstone torch elevator — 6 blocks up to surface (book)
  for i in range(6):
    y = oy - hole_d + 2 + i
    if i % 2 == 0:
      _set(v, rx + 2, y, rz, STONE)
    else:
      _set(v, rx + 2, y, rz, RTORCH)

  # Dispenser at surface beside well, moss carpet concealment
  disp_x, disp_z = cx + 2, cz
  _set(v, disp_x, oy, disp_z, DISP)
  _set(v, disp_x, oy + 1, disp_z, MCARPET)

  # 1×1 well shaft surface to hopper
  for y in range(oy - hole_d + 2, oy):
    _set(v, cx, y, cz, AIR_B)

  # 3×3 stone well base (book)
  base_mats = (SBRICK, MOSSY_B, MCOBBLE)
  for x in range(cx - 1, cx + 2):
    for z in range(cz - 1, cz + 2):
      if x == cx and z == cz:
        _set(v, x, oy, z, AIR_B)
        continue
      _set(v, x, oy, z, base_mats[(x + z) % 3])

  # Four corner pillars — 2 blocks tall stone brick walls
  for px, pz in ((cx - 1, cz - 1), (cx + 1, cz - 1), (cx - 1, cz + 1), (cx + 1, cz + 1)):
    for y in range(1, 3):
      _set(v, px, oy + y, pz, SWALL if y == 1 else SBRICK)

  # Warped tiered roof with center lantern
  for x in range(cx - 1, cx + 2):
    for z in range(cz - 1, cz + 2):
      _set(v, x, oy + 3, z, WSLAB if x == cx and z == cz else WPLANK)
  _set(v, cx, oy + 4, cz, WSLAB)
  _set(v, cx, oy + 2, cz, LANTERN)

  # Refill 6×3 hole with grass except mechanism and shaft
  for x in range(ox, ox + hole_l):
    for z in range(oz, oz + hole_w):
      if (x, z) in ((cx, cz), (disp_x, disp_z), (rx, rz), (rx + 1, rz), (rx + 2, rz)):
        continue
      _set(v, x, oy, z, GRASS)

  # Azalea landscaping (book)
  for ax, az in ((cx - 2, cz), (cx + 2, cz), (cx, cz - 2), (cx, cz + 2)):
    _set(v, ax, oy, az, AZBUSH)
    _set(v, ax, oy + 1, az, AZLEAF)

  return v


def _ring_dist(dx: int, dz: int) -> int:
  """Approximate ring index from center for carousel layers."""
  return int(round((dx * dx + dz * dz) ** 0.5))


def _generate_bite_carousel() -> np.ndarray:
  """
  Carousel — book dimensions:
    17×17 circular footprint, 5×5×5 mangrove glowstone hub, 13×13 sandstone
    roof, rail loop, end rod strider seats, 9×11 lava pen companion.
  """
  GRASS = _b("grass_block")
  SSSLAB = _b("smooth_sandstone_slab")
  SSTAIR = _b("smooth_sandstone_stairs")
  PBRICK = _b("prismarine_bricks")
  PSTAIR = _b("prismarine_brick_stairs")
  PSLAB = _b("prismarine_brick_slab")
  PWALL = _b("prismarine_brick_wall")
  MANG = _b("mangrove_planks")
  MSTAIR = _b("mangrove_stairs")
  MFENCE = _b("mangrove_fence")
  RED = _b("red_wool")
  YELLOW = _b("yellow_wool")
  RCARPET = _b("red_carpet")
  YCARPET = _b("yellow_carpet")
  RAIL = _b("rail")
  PRAIL = _b("powered_rail")
  RTORCH = _b("redstone_torch")
  ROD = _b("end_rod")
  SLANTERN = _b("soul_lantern")
  GLOW = _b("glowstone")
  LAVA = _b("lava")
  PGATE = _b("mangrove_fence_gate")
  LANTERN = _b("lantern")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 14, 14, 2
  outer_r = 8  # 17 block diameter

  # Grass pad under carousel
  for dx in range(-outer_r - 1, outer_r + 2):
    for dz in range(-outer_r - 1, outer_r + 2):
      _set(v, cx + dx, oy - 1, cz + dz, GRASS)

  # Step 1–2 — 17×17 base rings and wool hub (book)
  for dx in range(-outer_r, outer_r + 1):
    for dz in range(-outer_r, outer_r + 1):
      if not _in_circle(dx, dz, outer_r):
        continue
      x, z = cx + dx, cz + dz
      dist = _ring_dist(dx, dz)
      if dist >= 8:
        _set(v, x, oy, z, SSSLAB)
      elif dist == 7:
        _set(v, x, oy, z, PBRICK if (x + z) % 2 == 0 else MANG)
      elif dist == 6:
        _set(v, x, oy, z, RCARPET if (x + z) % 2 else YCARPET)
        _set(v, x, oy + 1, z, PSTAIR if dist == 6 else PWALL)
      elif dist >= 3:
        _set(v, x, oy, z, RED if (x + z) % 2 == 0 else YELLOW)
      elif dist >= 1:
        _set(v, x, oy, z, MANG if (x + z) % 2 else RED)
      else:
        _set(v, x, oy, z, YELLOW)

  # Step 3 — circular powered rail track between hub and outer ring
  for dx in range(-outer_r, outer_r + 1):
    for dz in range(-outer_r, outer_r + 1):
      dist = _ring_dist(dx, dz)
      if dist != 4:
        continue
      x, z = cx + dx, cz + dz
      _set(v, x, oy, z, RCARPET if (x + z) % 2 else YCARPET)
      _set(v, x, oy + 1, z, PRAIL if (x + z) % 3 == 0 else RAIL)
      if (x + z) % 4 == 0:
        _set(v, x, oy, z, RTORCH)

  # 5×5×5 central mangrove pillar with glowstone core (book page 77)
  for x in range(cx - 2, cx + 3):
    for z in range(cz - 2, cz + 3):
      for y in range(oy + 1, oy + 6):
        core = x == cx and z == cz
        edge = x in (cx - 2, cx + 2) or z in (cz - 2, cz + 2)
        if core:
          _set(v, x, y, z, GLOW)
        elif edge and y < oy + 5:
          _set(v, x, y, z, MSTAIR if y % 2 else MANG)
        else:
          _set(v, x, y, z, MANG if y < oy + 5 else AIR_B)

  # Prismarine overhang with soul lanterns and end rod seat hangers
  for dx in range(-7, 8):
    for dz in range(-7, 8):
      if not _in_circle(dx, dz, 7):
        continue
      x, z = cx + dx, cz + dz
      dist = _ring_dist(dx, dz)
      if dist in (6, 7):
        _set(v, x, oy + 6, z, PSLAB if dist == 7 else PSTAIR)
      if dist == 6 and (x + z) % 3 == 0:
        _set(v, x, oy + 5, z, SLANTERN)
      if dist == 5 and (x + z) % 5 == 0:
        _set(v, x, oy + 5, z, ROD)

  # 13×13 sandstone pyramid roof tapering to glowstone peak
  roof_base = oy + 7
  for layer in range(4):
    inset = layer
    r = 6 - inset
    for dx in range(-r, r + 1):
      for dz in range(-r, r + 1):
        if _in_circle(dx, dz, r):
          _set(v, cx + dx, roof_base + layer, cz + dz, SSTAIR if layer < 3 else GLOW)

  # Lava pen — 9×11 companion (book page 77)
  px, pz = cx + 10, cz - 2
  pen_w, pen_d = 9, 11
  for x in range(px, px + pen_w):
    for z in range(pz, pz + pen_d):
      _set(v, x, oy - 1, z, GRASS)
      _set(v, x, oy, z, LAVA)
  for x in range(px, px + pen_w):
    for z in range(pz, pz + pen_d):
      edge = x in (px, px + pen_w - 1) or z in (pz, pz + pen_d - 1)
      if not edge:
        continue
      if z == pz + pen_d - 1 and px + 3 <= x <= px + 5:
        _set(v, x, oy + 1, z, PGATE)
      else:
        _set(v, x, oy + 1, z, PBRICK)
        if (x, z) in ((px, pz), (px + pen_w - 1, pz), (px, pz + pen_d - 1), (px + pen_w - 1, pz + pen_d - 1)):
          _set(v, x, oy + 2, z, LANTERN)
  for x in range(px, px + 4):
    for z in range(pz, pz + 3):
      _set(v, x, oy + 3, z, PSTAIR)
      _set(v, x, oy + 4, z, PSLAB)

  return v


def _generate_bite_villager_island_head() -> np.ndarray:
  """
  Villager Island Head — book dimensions:
    5×2×2 cobble base, 3×2×6 head column with slab cap,
    3×1×3 mossy nose, recessed villager eyes, coastal cliff setting.
  """
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  WATER = _b("water")
  COBBLE = _b("cobblestone")
  MCOBBLE = _b("mossy_cobblestone")
  CSLAB = _b("cobblestone_slab")
  MCSLAB = _b("mossy_cobblestone_slab")
  MCSTAIR = _b("mossy_cobblestone_stairs")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 15, 4
  hx0, hz0 = ox + 1, oz
  front_z = oz - 1

  def _stone(x: int, y: int, z: int) -> None:
    _set(v, x, y, z, MCOBBLE if (x + y + z) % 3 == 0 else COBBLE)

  # Coastal grass cliff with ocean
  for x in range(ox - 2, ox + 8):
    for z in range(oz - 6, oz + 4):
      if z < oz - 2:
        for y in range(oy - 2, oy):
          _set(v, x, y, z, WATER)
      elif z <= oz + 2:
        _set(v, x, oy - 1, z, GRASS if z >= oz - 1 else DIRT)
        if z == oz - 1 and (x + z) % 4 == 0:
          _set(v, x, oy, z, GRASS)

  # Base foundation — 5×2×2 (book)
  for x in range(ox, ox + 5):
    for z in range(oz, oz + 2):
      for y in range(oy, oy + 2):
        _stone(x, y, z)

  # Main head column — 3×2×6 with cobblestone slab cap (book)
  eye_y = oy + 4  # 3rd block level from column bottom
  for y in range(oy + 2, oy + 8):
    for x in range(hx0, hx0 + 3):
      for z in range(hz0, hz0 + 2):
        if y == eye_y and z == hz0 and x in (hx0, hx0 + 2):
          _set(v, x, y, z, AIR_B)  # recessed villager eyes
        else:
          _stone(x, y, z)
  for x in range(hx0, hx0 + 3):
    for z in range(hz0, hz0 + 2):
      _set(v, x, oy + 8, z, CSLAB)

  # Nose assembly — 3×1×3 protruding front (book)
  for x in range(hx0, hx0 + 3):
    _set(v, x, oy + 4, front_z, MCSTAIR)
    _stone(x, oy + 5, front_z)
    _set(v, x, oy + 6, front_z, MCSLAB)

  return v


def _generate_bite_giant_grandfather_clock() -> np.ndarray:
  """
  Giant Grandfather Clock — book dimensions:
    7×7 ground chamber, +4 +6 +8 wall sections, 15 block chimney,
    copper pendulum, quartz clock face, cuckoo redstone, furnished interior.
  """
  GRASS = _b("grass_block")
  DBRICK = _b("deepslate_bricks")
  DBSTAIR = _b("deepslate_brick_stairs")
  DBSLAB = _b("deepslate_brick_slab")
  SPLANK = _b("spruce_planks")
  SLOG = _b("spruce_log")
  SSTAIR = _b("spruce_stairs")
  SSLAB = _b("spruce_slab")
  SFENCE = _b("spruce_fence")
  STRAP = _b("spruce_trapdoor")
  SDOOR = _b("spruce_door")
  SBUTTON = _b("spruce_button")
  GLASS = _b("glass_pane")
  GCONC = _b("gray_concrete")
  CHAIN = _b("chain")
  ROD = _b("lightning_rod")
  COPPER = _b("waxed_copper_block")
  CSTAIR = _b("waxed_cut_copper_stairs")
  QUARTZ = _b("smooth_quartz")
  QSLAB = _b("smooth_quartz_slab")
  BRICK = _b("bricks")
  BSTAIR = _b("brick_stairs")
  CAMP = _b("campfire")
  TORCH = _b("torch")
  RCARPET = _b("red_carpet")
  SHELF = _b("bookshelf")
  POT = _b("flower_pot")
  AZLEAF = _b("azalea_leaves")
  COBWEB = _b("cobweb")
  LADDER = _b("ladder")
  DETECTOR = _b("daylight_detector")
  DISP = _b("dispenser")
  DUST = _b("redstone_dust")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 11, 1
  s = 7
  cx, cz = ox + 3, oz + 3
  front_z, back_z = oz, oz + s - 1
  left_x = ox

  # Grass pad
  for x in range(ox - 3, ox + s + 4):
    for z in range(oz - 3, oz + s + 4):
      _set(v, x, oy - 1, z, GRASS)

  # Ground chamber — 7×7, 7 blocks high incl. deepslate foundation (book)
  for x in range(ox, ox + s):
    for z in range(oz, oz + s):
      _set(v, x, oy, z, DBRICK)
  for y in range(oy + 1, oy + 7):
    for x in range(ox, ox + s):
      for z in range(oz, oz + s):
        edge = x in (ox, ox + s - 1) or z in (oz, oz + s - 1)
        if not edge:
          _set(v, x, y, z, AIR_B)
          continue
        if z == front_z and x == cx and y <= oy + 2:
          if y <= oy + 2:
            _set(v, x, y, z, SDOOR if y > oy else SSTAIR)
          continue
        if x == ox + s - 1 and z == cz and y == oy + 3:
          _set(v, x, y, z, GLASS)
          _set(v, x, y, z - 1, STRAP)
          _set(v, x, y, z + 1, STRAP)
          continue
        _set(v, x, y, z, SPLANK if y < oy + 6 else SSLAB)

  # Ground floor interior (book page 85)
  for x in range(ox + 1, ox + s - 1):
    for z in range(oz + 1, oz + s - 1):
      _set(v, x, oy + 1, z, RCARPET)
  for sx, sz in ((ox + 1, oz + 1), (ox + s - 2, oz + 1), (ox + 1, oz + s - 2)):
    for y in range(oy + 1, oy + 4):
      _set(v, sx, y, sz, SHELF)
  _set(v, cx + 1, oy + 1, back_z - 1, BRICK)
  _set(v, cx + 1, oy + 2, back_z - 1, BRICK)
  _set(v, cx + 1, oy + 1, back_z - 2, CAMP)
  _set(v, cx - 1, oy + 1, oz + 2, BSTAIR)
  _set(v, ox + 2, oy + 3, oz + 2, POT)
  _set(v, ox + 2, oy + 4, oz + 2, AZLEAF)
  _set(v, ox + s - 2, oy + 3, oz + s - 2, COBWEB)

  # First floor ceiling with 1×1 ladder gap (book)
  ceil_y = oy + 7
  for x in range(ox, ox + s):
    for z in range(oz, oz + s):
      if (x, z) == (ox + 1, oz + 1):
        _set(v, x, ceil_y, z, AIR_B)
      else:
        _set(v, x, ceil_y, z, SPLANK if (x + z) % 2 else SSLAB)
  for y in range(oy + 1, ceil_y):
    _set(v, ox + 1, y, oz + 1, LADDER)

  # Shaft +4 and +6 sections (book pages 82–83): y oy+8..oy+17
  shaft_y1 = oy + 18
  for y in range(oy + 8, shaft_y1):
    for x in range(ox + 1, ox + s - 1):
      for z in range(oz + 1, oz + s - 1):
        edge = x in (ox + 1, ox + s - 2) or z in (oz + 1, oz + s - 2)
        if edge:
          _set(v, x, y, z, SPLANK if y % 2 else SSTAIR)
        else:
          _set(v, x, y, z, AIR_B)
    for fx, fz in ((ox + 1, oz + 1), (ox + s - 2, oz + 1)):
      _set(v, fx, y, fz, SFENCE)

  # Pendulum alcove — gray concrete backing, copper weight (book)
  for y in range(oy + 10, oy + 16):
    for x in range(cx - 1, cx + 2):
      _set(v, x, y, back_z - 1, GCONC)
  _set(v, cx, oy + 15, cz, CHAIN)
  _set(v, cx, oy + 14, cz, ROD)
  for dx, dz in ((0, 0), (-1, 0), (1, 0), (0, -1)):
    _set(v, cx + dx, oy + 12, cz + dz, COPPER if dx == 0 and dz == 0 else CSTAIR)

  # Upper +8 quartz section: y oy+18..oy+25
  upper_y1 = oy + 26
  for y in range(shaft_y1, upper_y1):
    for x in range(ox, ox + s):
      for z in range(oz, oz + s):
        edge = x in (ox, ox + s - 1) or z in (oz, oz + s - 1)
        if edge:
          if y == oy + 22 and ((x == cx and z in (front_z, back_z)) or (z == cz and x in (ox, ox + s - 1))):
            _set(v, x, y, z, GLASS)
          else:
            _set(v, x, y, z, QUARTZ if y > oy + 20 else SPLANK)
        elif y == ceil_y + 1:
          _set(v, x, y, z, AIR_B)

  # Clock face — white circle, spruce log center, buttons (book)
  face_y = oy + 26
  for dx in range(-2, 3):
    for dz in range(-1, 2):
      if abs(dx) + abs(dz) <= 2:
        _set(v, cx + dx, face_y, front_z, QUARTZ)
        if abs(dx) == 2 or abs(dz) == 1:
          _set(v, cx + dx, face_y, front_z, SBUTTON)
  _set(v, cx, face_y, front_z - 1, SLOG)

  # Cuckoo redstone — daylight detector, dispenser, dust (book)
  _set(v, cx, oy + 27, front_z - 1, DISP)
  _set(v, cx, oy + 28, cz, DETECTOR)
  _set(v, cx, oy + 27, cz, DUST)

  # Gabled roof — deepslate stairs + smooth quartz (book)
  for layer in range(3):
    inset = layer
    ry = oy + 28 + layer
    for x in range(ox + inset, ox + s - inset):
      for z in range(oz + inset, oz + s - inset):
        edge = x in (ox + inset, ox + s - 1 - inset) or z in (oz + inset, oz + s - 1 - inset)
        _set(v, x, ry, z, DBSTAIR if edge else QSLAB)

  # 15 block brick chimney on left side (book)
  ch_x = ox - 1
  for y in range(oy + 6, oy + 21):
    _set(v, ch_x, y, cz, BRICK if y < oy + 20 else BSTAIR)
    if y == oy + 6:
      _set(v, ch_x, y, cz - 1, STRAP)
      _set(v, ch_x, y, cz + 1, STRAP)
  _set(v, ch_x, oy + 20, cz, QUARTZ)
  _set(v, ch_x, oy + 21, cz, TORCH)

  return v


def _generate_bite_hot_spring() -> np.ndarray:
  """
  Hot Spring — book dimensions:
    23×22 snowy base, five tiered soul sand pools with basalt rims,
    L-shaped 8×11 chalet with cobble pillars birch slab floor granite roof,
    birch stair seating campfire bamboo azalea hedges stone wall lanterns.
  """
  SNOW = _b("snow_block")
  SNOW_L = _b("snow")
  SOUL = _b("soul_sand")
  BASALT = _b("basalt")
  CDSLAB = _b("cobbled_deepslate_slab")
  WATER = _b("water")
  SBLOG = _b("stripped_birch_log")
  BSLAB = _b("birch_slab")
  BSTAIR = _b("birch_stairs")
  BSIGN = _b("birch_sign")
  BGATE = _b("birch_fence_gate")
  COBBLE = _b("cobblestone")
  PGRAN = _b("polished_granite")
  PGSLAB = _b("polished_granite_slab")
  PGSTAIR = _b("polished_granite_stairs")
  SWALL = _b("stone_brick_wall")
  LANTERN = _b("lantern")
  CAMP = _b("campfire")
  AZLEAF = _b("flowering_azalea_leaves")
  BAMBOO = _b("bamboo")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 4, 5, 3
  bw, bd = 23, 22

  # Snow terrain base (book snowy taiga setting)
  for x in range(ox, ox + bw):
    for z in range(oz, oz + bd):
      _set(v, x, oy - 1, z, SNOW)
      if (x + z) % 4 == 0:
        _set(v, x, oy, z, SNOW_L)

  def _pool(px: int, pz: int, pr: int, py: int) -> None:
    for dx in range(-pr - 1, pr + 2):
      for dz in range(-pr - 1, pr + 2):
        dist2 = dx * dx + dz * dz
        x, z = px + dx, pz + dz
        if dist2 <= pr * pr:
          _set(v, x, py, z, SOUL)
          _set(v, x, py + 1, z, WATER)
        elif dist2 <= (pr + 1) * (pr + 1):
          _set(v, x, py, z, BASALT)
          _set(v, x, py + 1, z, BASALT if dist2 <= pr * pr + pr else WATER)
        elif dist2 <= (pr + 2) * (pr + 2) and (dx + dz) % 2 == 0:
          _set(v, x, py, z, CDSLAB)
          _set(v, x, py + 1, z, BASALT)

  # Five tiered ponds — each rising one block higher (book page 86)
  _pool(ox + 6, oz + 6, 3, oy)
  _pool(ox + 12, oz + 10, 3, oy + 1)
  _pool(ox + 17, oz + 7, 2, oy + 2)
  _pool(ox + 8, oz + 15, 3, oy + 1)
  _pool(ox + 18, oz + 17, 2, oy + 3)

  # Stone wall lantern posts around pools (book page 88)
  for lx, lz in ((ox + 4, oz + 8), (ox + 14, oz + 5), (ox + 10, oz + 18), (ox + 20, oz + 12)):
    for y in range(oy, oy + 3):
      _set(v, lx, y, lz, SWALL)
    _set(v, lx, oy + 3, lz, LANTERN)

  # Birch stairs into lower pool
  for i in range(3):
    _set(v, ox + 9 + i, oy, oz + 8 - i, BSTAIR)

  # Seating area — birch stairs with sign armrests and campfire (book page 88)
  sx, sz = ox + 2, oz + 12
  _set(v, sx, oy, sz, CAMP)
  _set(v, sx - 1, oy, sz, BSTAIR)
  _set(v, sx - 2, oy, sz, BSIGN)
  for i in range(3):
    _set(v, sx + 1 + i, oy, sz, BSTAIR)
  _set(v, sx + 4, oy, sz, BSIGN)

  # Bamboo and flowering azalea hedges
  for bx, bz in ((ox + 1, oz + 18), (ox + 20, oz + 4), (ox + 21, oz + 15)):
    _set(v, bx, oy, bz, BAMBOO)
    _set(v, bx, oy + 1, bz, BAMBOO)
  for hx in range(ox, ox + bw, 6):
    for hz in range(oz, oz + bd, 7):
      if (hx + hz) % 9 == 0:
        for dx in range(2):
          for dz in range(2):
            _set(v, hx + dx, oy, hz + dz, AZLEAF)

  # L-shaped chalet — 8×11 footprint (book page 89)
  ch_x, ch_z = ox + 14, oz + 2
  l_cells: list[tuple[int, int]] = []
  for x in range(ch_x, ch_x + 8):
    for z in range(ch_z, ch_z + 6):
      l_cells.append((x, z))
  for x in range(ch_x, ch_x + 4):
    for z in range(ch_z + 6, ch_z + 11):
      l_cells.append((x, z))

  corners = (
    (ch_x, ch_z),
    (ch_x + 7, ch_z),
    (ch_x, ch_z + 5),
    (ch_x + 7, ch_z + 5),
    (ch_x, ch_z + 10),
    (ch_x + 3, ch_z + 10),
  )
  for cx, cz in corners:
    for y in range(oy, oy + 5):
      _set(v, cx, y, cz, SBLOG)

  # Cobblestone pillars — 3 blocks front, 4 blocks back (book step 2)
  pillar_spots = (
    (ch_x + 3, ch_z, 3),
    (ch_x + 7, ch_z + 3, 3),
    (ch_x, ch_z + 3, 3),
    (ch_x, ch_z + 10, 4),
    (ch_x + 3, ch_z + 10, 4),
    (ch_x + 3, ch_z + 6, 4),
  )
  for px, pz, ph in pillar_spots:
    if (px, pz) not in corners:
      for y in range(oy, oy + ph):
        _set(v, px, y, pz, COBBLE)

  # Birch slab floor
  for x, z in l_cells:
    if (x, z) not in corners:
      _set(v, x, oy, z, BSLAB)

  # Birch fence gate trim between pillar tops (book step 3)
  trim_y = oy + 4
  for x in range(ch_x, ch_x + 8):
    if (x, ch_z) not in corners:
      _set(v, x, trim_y, ch_z, BGATE)
  for z in range(ch_z + 6, ch_z + 11):
    if (ch_x, z) not in corners:
      _set(v, ch_x, trim_y, z, BGATE)

  # Polished granite roof — sloped front 3 back 4 (book step 4)
  for x, z in l_cells:
    if (x, z) in corners:
      continue
    roof_y = oy + 4 if z < ch_z + 6 else oy + 5
    _set(v, x, roof_y, z, PGRAN if (x + z) % 2 == 0 else PGSLAB)
    if z in (ch_z, ch_z + 10) or x in (ch_x, ch_x + 7):
      _set(v, x, roof_y + 1, z, PGSTAIR)

  # Lanterns under roof
  for x in range(ch_x + 1, ch_x + 7, 2):
    for z in range(ch_z + 1, ch_z + 5, 2):
      _set(v, x, oy + 3, z, LANTERN)

  return v


def _generate_bite_wardrobe_portal() -> np.ndarray:
  """
  Wardrobe Portal — book dimensions:
    4×3×6.5 dark oak wardrobe concealing a 4×5 obsidian nether portal.
  """
  OBS = _b("obsidian")
  PORTAL = _b("nether_portal")
  PLANK = _b("dark_oak_planks")
  DOOR = _b("dark_oak_door")
  DSTAIR = _b("dark_oak_stairs")
  DSLAB = _b("dark_oak_slab")
  DTRAP = _b("dark_oak_trapdoor")
  DBUTTON = _b("dark_oak_button")
  BANNER = _b("white_banner")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 14, 14, 2
  fw, fh, fd = 4, 5, 3

  # Grass pad
  for x in range(ox - 1, ox + fw + 1):
    for z in range(oz - 1, oz + fd + 1):
      _set(v, x, oy - 1, z, GRASS)

  # Back layer — obsidian frame with portal (z = oz)
  for x in range(ox, ox + fw):
    _set(v, x, oy, oz, OBS)
    _set(v, x, oy + fh - 1, oz, OBS)
  for y in range(oy + 1, oy + fh - 1):
    _set(v, ox, y, oz, OBS)
    _set(v, ox + fw - 1, y, oz, OBS)
  for y in range(oy + 1, oy + fh - 1):
    for x in range(ox + 1, ox + fw - 1):
      _set(v, x, y, oz, PORTAL)

  # Middle layer — inner plank casing and banner curtains (z = oz + 1)
  mid_z = oz + 1
  for y in range(oy, oy + 6):
    for x in range(ox, ox + fw):
      edge = x in (ox, ox + fw - 1) or y in (oy, oy + 5)
      if edge:
        _set(v, x, y, mid_z, PLANK)
  _set(v, ox + 1, oy + 4, mid_z, BANNER)
  _set(v, ox + 2, oy + 4, mid_z, BANNER)

  # Side panels connecting back to front
  for z in range(oz, oz + fd):
    for y in range(oy, oy + 5):
      _set(v, ox, y, z, PLANK)
      _set(v, ox + fw - 1, y, z, PLANK)

  # Front facade — doors, trim, buttons (z = oz + 2)
  front_z = oz + fd - 1
  for y in range(oy, oy + 5):
    for x in range(ox, ox + fw):
      if x in (ox, ox + fw - 1):
        _set(v, x, y, front_z, PLANK)
      elif y in (oy + 1, oy + 2) and x in (ox + 1, ox + 2):
        _set(v, x, y, front_z, DOOR)
      elif y > oy:
        _set(v, x, y, front_z, PLANK)
  _set(v, ox, oy + 1, front_z, DBUTTON)
  _set(v, ox + fw - 1, oy + 1, front_z, DBUTTON)

  # Crown molding on front
  for x in range(ox, ox + fw):
    _set(v, x, oy + 5, front_z, DSTAIR)
    _set(v, x, oy + 6, front_z, DSLAB)

  # Trapdoor roof
  for x in range(ox, ox + fw):
    for z in range(oz, oz + fd):
      _set(v, x, oy + 6, z, DTRAP)

  return v


def _on_chamfer_platform(x: int, z: int, ox: int, oz: int, size: int = 6) -> bool:
  if x < ox or x >= ox + size or z < oz or z >= oz + size:
    return False
  return not (x in (ox, ox + size - 1) and z in (oz, oz + size - 1))


def _generate_bite_pig_hot_air_balloon() -> np.ndarray:
  """
  Pig Hot-Air Balloon — book dimensions:
    6×6 jungle basket, 8×8×8 pink pig-head balloon on chain tethers.
  """
  JSLAB = _b("jungle_slab")
  JSTAIR = _b("jungle_stairs")
  JLOG = _b("stripped_jungle_log")
  JFENCE = _b("jungle_fence")
  JGATE = _b("jungle_fence_gate")
  COCOA = _b("cocoa")
  PCANDLE = _b("pink_candle")
  CAMP = _b("campfire")
  CHAIN = _b("chain")
  LANTERN = _b("lantern")
  PINK = _b("pink_concrete")
  PTERRA = _b("pink_terracotta")
  WHITE = _b("white_wool")
  BLACK = _b("black_wool")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 13, 13, 3
  basket = 6
  bx0 = ox + basket // 2 - 4
  bz0 = oz + basket // 2 - 4
  by0 = oy + 6

  # Ground
  for x in range(ox - 2, ox + basket + 2):
    for z in range(oz - 2, oz + basket + 2):
      _set(v, x, oy - 1, z, GRASS)

  # Step 1 — chamfered jungle slab deck with stair rim
  for x in range(ox, ox + basket):
    for z in range(oz, oz + basket):
      if not _on_chamfer_platform(x, z, ox, oz, basket):
        continue
      edge = (
        x in (ox + 1, ox + basket - 2)
        or z in (oz + 1, oz + basket - 2)
      ) and (x in (ox, ox + basket - 1) or z in (oz, oz + basket - 1))
      _set(v, x, oy, z, JSTAIR if edge else JSLAB)

  # Step 2 — stripped log corners, fence walls, gate on front
  pillars = (
    (ox + 1, oz + 1),
    (ox + basket - 2, oz + 1),
    (ox + 1, oz + basket - 2),
    (ox + basket - 2, oz + basket - 2),
  )
  for px, pz in pillars:
    _set(v, px, oy + 1, pz, JLOG)
    _set(v, px, oy + 2, pz, COCOA)

  front_z = oz + basket - 2
  for x in range(ox + 1, ox + basket - 1):
    if x == ox + 2:
      _set(v, x, oy + 1, front_z, JGATE)
    else:
      _set(v, x, oy + 1, front_z, JFENCE)
  for z in (oz + 1, oz + basket - 2):
    for x in (ox + 1, ox + basket - 2):
      if (x, z) not in pillars:
        _set(v, x, oy + 1, z, JFENCE)

  # Pink candles on corner fence posts
  for px, pz in pillars:
    _set(v, px, oy + 2, pz, PCANDLE)

  # Lanterns on basket sides
  for lx, lz in ((ox, oz + 2), (ox + basket - 1, oz + 3)):
    _set(v, lx, oy + 1, lz, LANTERN)

  # Burner assembly — jungle stairs/slabs + campfire
  cx, cz = ox + basket // 2 - 1, oz + basket // 2 - 1
  for dx in (-1, 0):
    for dz in (-1, 0):
      _set(v, cx + dx, oy + 1, cz + dz, JSTAIR)
  _set(v, cx, oy + 1, cz, CAMP)

  # Chain corner tethers (5 blocks)
  for px, pz in pillars:
    for y in range(oy + 2, oy + 7):
      _set(v, px, y, pz, CHAIN)
  for y in range(oy + 3, oy + 6):
    _set(v, cx, y, cz, CHAIN)

  # Balloon base — 8×8 pink concrete with 2×2 center hole
  for x in range(bx0, bx0 + 8):
    for z in range(bz0, bz0 + 8):
      hole = bx0 + 3 <= x <= bx0 + 4 and bz0 + 3 <= z <= bz0 + 4
      if not hole:
        _set(v, x, by0, z, PINK)

  # Balloon walls and roof — 8×8×8 hollow cube
  for y in range(by0 + 1, by0 + 8):
    for x in range(bx0, bx0 + 8):
      for z in range(bz0, bz0 + 8):
        shell = x in (bx0, bx0 + 7) or z in (bz0, bz0 + 7) or y == by0 + 7
        if shell:
          _set(v, x, y, z, PINK)

  # Pig snout — protruding on front (+z)
  snout_z = bz0 + 8
  for x in range(bx0 + 2, bx0 + 6):
    for y in range(by0 + 2, by0 + 4):
      _set(v, x, y, snout_z, PTERRA)
      _set(v, x, y, snout_z + 1, PTERRA)

  # Pig eyes
  for ex in (bx0 + 1, bx0 + 5):
    for dy in range(2):
      _set(v, ex, by0 + 5 + dy, bz0, WHITE)
      _set(v, ex + 1, by0 + 5 + dy, bz0, WHITE)
    _set(v, ex, by0 + 6, bz0, BLACK)
    _set(v, ex + 1, by0 + 6, bz0, BLACK)

  # Pig ears on sides
  for ear_x, dx in ((bx0 - 1, 0), (bx0 + 8, 0)):
    for y in range(by0 + 5, by0 + 7):
      for dz in (-1, 0):
        _set(v, ear_x, y, bz0 + 3 + dz, PTERRA)

  return v


def _generate_bite_big_red_barn() -> np.ndarray:
  """
  Big Red Barn — book dimensions:
    12×17 red barn with birch gambrel roof and attached silo tower.
  """
  DIRT = _b("coarse_dirt")
  RED = _b("red_concrete")
  RPOW = _b("red_concrete_powder")
  RTERRA = _b("red_terracotta")
  WHITE = _b("white_concrete")
  GLASS = _b("glass_pane")
  BIRCH = _b("birch_planks")
  BSTAIR = _b("birch_stairs")
  BSLAB = _b("birch_slab")
  BFENCE = _b("birch_fence")
  BGATE = _b("birch_fence_gate")
  HAY = _b("hay_block")
  LADDER = _b("ladder")
  LANTERN = _b("lantern")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 7, 8, 1
  w, d = 12, 17
  wall_h = 7

  reds = (RED, RPOW, RTERRA)

  def _red(x: int, y: int, z: int) -> str:
    return reds[(x + y + z) % 3]

  # Surrounding grass
  for x in range(ox - 2, ox + w + 8):
    for z in range(oz - 2, oz + d + 2):
      _set(v, x, oy - 1, z, GRASS)

  # Foundation
  for x in range(ox, ox + w):
    for z in range(oz, oz + d):
      _set(v, x, oy, z, DIRT)

  pillars = ((ox, oz), (ox + w - 1, oz), (ox, oz + d - 1), (ox + w - 1, oz + d - 1))

  # Walls — red mix with white trim and corner pillars
  for y in range(oy + 1, oy + 1 + wall_h):
    for x in range(ox, ox + w):
      for z in range(oz, oz + d):
        edge = x in (ox, ox + w - 1) or z in (oz, oz + d - 1)
        if not edge:
          continue
        corner = (x, z) in pillars
        door = z == oz + d - 1 and ox + 4 <= x <= ox + 6 and y <= oy + 4
        window = (
          x in (ox, ox + w - 1)
          and z in (oz + 4, oz + 8, oz + 12)
          and y in (oy + 3, oy + 4)
        )
        brace = (x + z + y) % 4 == 0 and not corner

        if door:
          _set(v, x, y, z, AIR_B)
        elif window:
          _set(v, x, y, z, GLASS if y == oy + 4 else WHITE)
        elif corner or brace:
          _set(v, x, y, z, WHITE)
        else:
          _set(v, x, y, z, _red(x, y, z))

  # Gable peaks on short ends (x faces) — rise to 11 blocks at center z
  for end_x in (ox, ox + w - 1):
    for layer in range(4):
      gy = oy + 1 + wall_h + layer
      inset = layer // 2
      for z in range(oz + inset, oz + d - inset):
        _set(v, end_x, gy, z, WHITE if z in (oz + inset, oz + d - 1 - inset) else _red(end_x, gy, z))

  # Hollow interior
  for y in range(oy + 1, oy + 1 + wall_h):
    for x in range(ox + 1, ox + w - 1):
      for z in range(oz + 1, oz + d - 1):
        _set(v, x, y, z, AIR_B)

  # Interior stalls and hay
  for z in range(oz + 2, oz + d - 2, 4):
    for x in (ox + 2, ox + w - 3):
      _set(v, x, oy + 1, z, BFENCE)
      _set(v, x, oy + 2, z, BFENCE)
    _set(v, ox + 3, oy + 1, z, HAY)
  _set(v, ox + w // 2, oy + 5, oz + 3, LANTERN)

  # Gambrel roof — birch stairs/slabs along length
  roof_base = oy + 1 + wall_h + 3
  for z in range(oz - 1, oz + d + 1):
    for layer in range(4):
      ry = roof_base + layer
      inset = layer if layer < 2 else 3 - layer
      for x in range(ox - 1 + inset, ox + w - inset):
        mat = BSTAIR if layer % 2 == 0 else BSLAB
        _set(v, x, ry, z, mat)
  # Roof beam planks
  for z in range(oz, oz + d, 4):
    for x in range(ox + 1, ox + w - 1):
      _set(v, x, roof_base - 1, z, BIRCH)

  # Cupola vent on ridge
  cz = oz + d // 2
  for x in range(ox + 4, ox + 7):
    for z in range(cz - 1, cz + 2):
      _set(v, x, roof_base + 4, z, _red(x, roof_base + 4, z))
  _set(v, ox + 5, roof_base + 5, cz, BFENCE)
  _set(v, ox + 5, roof_base + 6, cz, BSTAIR)

  # Exterior hay stacks
  for hx, hz in ((ox + 2, oz + d - 2), (ox + w - 3, oz + 1)):
    _set(v, hx, oy + 1, hz, HAY)
    _set(v, hx, oy + 2, hz, HAY)

  # Side pen
  for x in range(ox - 1, ox + 3):
    _set(v, x, oy + 1, oz - 1, BFENCE)
    _set(v, x, oy + 2, oz - 1, BFENCE)
  _set(v, ox + 1, oy + 1, oz - 1, BGATE)

  # Attached silo — 5×5 cylinder at barn east side
  sx, sz = ox + w, oz + 4
  silo_h = 12
  for y in range(oy + 1, oy + 1 + silo_h):
    for x in range(sx, sx + 5):
      for z in range(sz, sz + 5):
        dist = max(abs(x - (sx + 2)), abs(z - (sz + 2)))
        if dist <= 2:
          if dist == 2 or y == oy + silo_h:
            _set(v, x, y, z, _red(x, y, z))
          elif y == oy + 1:
            _set(v, x, y, z, DIRT)

  # Silo conical birch roof
  for layer in range(3):
    inset = layer
    for x in range(sx + inset, sx + 5 - inset):
      for z in range(sz + inset, sz + 5 - inset):
        _set(v, x, oy + 1 + silo_h + layer, z, BSTAIR if layer < 2 else BSLAB)

  # Silo ladder
  for y in range(oy + 1, oy + silo_h + 2):
    _set(v, sx + 4, y, sz + 2, LADDER)

  return v


def _generate_bite_pagoda() -> np.ndarray:
  """
  Pagoda — book dimensions:
    15×15 four-story tapering tower with copper eaves, ~28 blocks tall.
  """
  SBRICK = _b("stone_bricks")
  MOSSY = _b("mossy_stone_bricks")
  SBSTAIR = _b("stone_brick_stairs")
  BLACK = _b("black_concrete")
  MPLANK = _b("mangrove_planks")
  MSTAIR = _b("mangrove_stairs")
  MSLAB = _b("mangrove_slab")
  MFENCE = _b("mangrove_fence")
  WHITE = _b("white_wool")
  GLASS = _b("glass_pane")
  CSTAIR = _b("oxidized_cut_copper_stairs")
  CSLAB = _b("oxidized_cut_copper_slab")
  LANTERN = _b("lantern")
  LADDER = _b("ladder")
  BARREL = _b("barrel")
  GOLD = _b("gold_block")
  ANVIL = _b("anvil")
  BARS = _b("iron_bars")
  LEAVES = _b("azalea_leaves")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 9, 1
  base = 15

  # Grass surround
  for x in range(ox - 1, ox + base + 1):
    for z in range(oz - 1, oz + base + 1):
      _set(v, x, oy - 1, z, GRASS)

  # Step 1 — stone foundation (2 high)
  for x in range(ox, ox + base):
    for z in range(oz, oz + base):
      edge = x in (ox, ox + base - 1) or z in (oz, oz + base - 1)
      _set(v, x, oy, z, BLACK if not edge else SBRICK)
      _set(v, x, oy + 1, z, MOSSY if (x + z) % 2 else SBRICK)
  _set(v, ox + 7, oy + 1, oz + base - 1, SBSTAIR)

  tiers = ((1, 11, 4), (3, 9, 4), (5, 7, 4), (7, 5, 4))
  cx, cz = ox + base // 2, oz + base // 2

  for i, (inset, inner, wall_h) in enumerate(tiers):
    wx = ox + inset
    wz = oz + inset
    wy = oy + 2 + i * 5

    # Veranda floor — mangrove planks one block wider than walls
    for x in range(wx - 1, wx + inner + 1):
      for z in range(wz - 1, wz + inner + 1):
        on_veranda = x in (wx - 1, wx + inner) or z in (wz - 1, wz + inner)
        inside = wx <= x < wx + inner and wz <= z < wz + inner
        if on_veranda or inside:
          _set(v, x, wy, z, MPLANK)

    # Walls
    for y in range(1, 1 + wall_h):
      for x in range(wx, wx + inner):
        for z in range(wz, wz + inner):
          edge = x in (wx, wx + inner - 1) or z in (wz, wz + inner - 1)
          if not edge:
            continue
          corner = x in (wx, wx + inner - 1) and z in (wz, wz + inner - 1)
          window = (
            not corner
            and y in (2, 3)
            and (x in (wx + inner // 2, wx + inner // 2 - 1) or z in (wz + inner // 2, wz + inner // 2 - 1))
          )
          if window:
            _set(v, x, wy + y, z, GLASS if y == 3 else MPLANK)
          elif corner:
            _set(v, x, wy + y, z, MPLANK)
          else:
            _set(v, x, wy + y, z, WHITE)

    # Veranda fence railings and corner lanterns
    for x in range(wx - 1, wx + inner + 1):
      _set(v, x, wy + 1, wz - 1, MFENCE)
      _set(v, x, wy + 1, wz + inner, MFENCE)
    for z in range(wz, wz + inner):
      _set(v, wx - 1, wy + 1, z, MFENCE)
      _set(v, wx + inner, wy + 1, z, MFENCE)
    for lx, lz in ((wx - 1, wz - 1), (wx + inner, wz - 1), (wx - 1, wz + inner), (wx + inner, wz + inner)):
      _set(v, lx, wy + 2, lz, LANTERN)

    # Copper eaves — flaring stair ring
    ey = wy + wall_h
    for x in range(wx - 2, wx + inner + 2):
      for z in range(wz - 2, wz + inner + 2):
        on_eave = x in (wx - 2, wx + inner + 1) or z in (wz - 2, wz + inner + 1)
        if on_eave:
          _set(v, x, ey, z, CSTAIR if (x + z) % 2 == 0 else CSLAB)

    # Interior hollow + ladder
    for y in range(1, wall_h):
      for x in range(wx + 1, wx + inner - 1):
        for z in range(wz + 1, wz + inner - 1):
          _set(v, x, wy + y, z, AIR_B)
    for y in range(wy + 1, wy + wall_h + 4):
      _set(v, cx, y, cz, LADDER)

    # Floor 1 interior decor
    if i == 0:
      for bx, bz in ((wx + 1, wz + 1), (wx + 2, wz + 1)):
        _set(v, bx, wy + 1, bz, BARREL)
      _set(v, wx + inner - 2, wy + 1, wz + 1, MSTAIR)
      _set(v, wx + 1, wy + 2, wz + inner - 2, LEAVES)
    elif i == 1:
      _set(v, wx + 1, wy + 1, wz + 1, BARREL)
      _set(v, wx + inner - 2, wy + 1, wz + inner - 2, LANTERN)
      _set(v, wx + 2, wy + 1, wz + inner - 2, MSTAIR)

  # Top fifth room + steep copper peak
  top_inset, top_inner = 9, 3
  twx, twz = ox + top_inset, oz + top_inset
  twy = oy + 2 + 4 * 5
  for x in range(twx, twx + top_inner):
    for z in range(twz, twz + top_inner):
      _set(v, x, twy, z, MPLANK)
  for y in range(1, 5):
    for x in range(twx, twx + top_inner):
      for z in range(twz, twz + top_inner):
        edge = x in (twx, twx + top_inner - 1) or z in (twz, twz + top_inner - 1)
        if edge:
          win = y in (2, 3) and x == twx + 1
          _set(v, x, twy + y, z, GLASS if win else MPLANK if (x == z) else WHITE)

  peak_y = twy + 5
  for layer in range(3):
    inset = layer
    for x in range(twx + inset, twx + top_inner - inset):
      for z in range(twz + inset, twz + top_inner - inset):
        _set(v, x, peak_y + layer, z, CSTAIR if layer < 2 else CSLAB)

  # Decorative spire
  _set(v, cx, peak_y + 3, cz, GOLD)
  for y in range(peak_y + 4, peak_y + 7):
    _set(v, cx, y, cz, ANVIL)
  _set(v, cx, peak_y + 7, cz, BARS)

  return v


def _generate_bite_magic_mirror() -> np.ndarray:
  """
  Magic Mirror — book dimensions:
    9×6 stone floor, 9×10 stone brick wall, 4×5 obsidian portal,
    5×7 smooth quartz face plate, bamboo ornate front frame.
  """
  STBR = _b("stone_bricks")
  STONE = _b("stone")
  OBS = _b("obsidian")
  PORTAL = _b("nether_portal")
  QUARTZ = _b("smooth_quartz")
  QSLAB = _b("smooth_quartz_slab")
  QSTAIR = _b("smooth_quartz_stairs")
  BSLAB = _b("bamboo_slab")
  BSTAIR = _b("bamboo_stairs")
  BPLANK = _b("bamboo_planks")
  PURPLE = _b("purple_concrete")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 14, 3
  fw, fd, wh = 9, 6, 10
  px, py = ox + 2, oy + 2
  pw, ph = 4, 5

  # 9×6 stone floor
  for x in range(ox, ox + fw):
    for z in range(oz, oz + fd):
      mat = STONE
      if z >= oz + fd - 2 and ox + 3 <= x <= ox + 5:
        mat = PURPLE if (x + z) % 2 == 0 else BPLANK
      _set(v, x, oy - 1, z, mat)

  # Stone brick wall (9×10) at back edge of floor
  wall_z = oz
  for y in range(oy, oy + wh):
    for x in range(ox, ox + fw):
      in_portal = (
        px <= x < px + pw
        and py + 1 <= y < py + ph - 1
      )
      if not in_portal:
        _set(v, x, y, wall_z, STBR)

  # Obsidian portal frame
  for x in range(px - 1, px + pw + 1):
    _set(v, x, py, wall_z, OBS)
    _set(v, x, py + ph - 1, wall_z, OBS)
  for y in range(py + 1, py + ph - 1):
    _set(v, px - 1, y, wall_z, OBS)
    _set(v, px + pw, y, wall_z, OBS)

  # Portal interior
  for y in range(py + 1, py + ph - 1):
    for x in range(px, px + pw):
      _set(v, x, y, wall_z, PORTAL)

  # Quartz face plate behind portal (5×7, centered on portal)
  fx, fy = px, py - 1
  face_w, face_h = 5, 7
  face_z = wall_z + 1
  eye_y = fy + 4
  mouth_y = fy + 1
  for y in range(fy, fy + face_h):
    for x in range(fx, fx + face_w):
      is_eye = y == eye_y and x in (fx, fx + face_w - 1)
      is_mouth = mouth_y <= y <= mouth_y + 1 and fx + 1 <= x <= fx + 3
      if is_eye or is_mouth:
        _set(v, x, y, face_z + 1, OBS)
        continue
      mat = QUARTZ
      if is_mouth and y == mouth_y:
        mat = QSTAIR
      elif y in (fy, fy + face_h - 1) or x in (fx, fx + face_w - 1):
        mat = QSLAB if (x + y) % 2 == 0 else QUARTZ
      _set(v, x, y, face_z, mat)

  # Bamboo ornate mirror frame protruding in front of wall
  frame_z = wall_z - 1
  for y in range(py - 1, py + ph):
    for x in range(px - 2, px + pw + 2):
      on_border = (
        x in (px - 2, px + pw + 1)
        or y in (py - 1, py + ph - 1)
      )
      if not on_border:
        continue
      corner = x in (px - 2, px + pw + 1) and y in (py - 1, py + ph - 1)
      mat = BSTAIR if corner or (x + y) % 2 == 0 else BSLAB
      _set(v, x, y, frame_z, mat)
  # Decorative frame nubs
  for x, y in (
    (px - 2, py + 1),
    (px + pw + 1, py + 1),
    (px + 1, py - 1),
    (px + 2, py + ph - 1),
  ):
    _set(v, x, y, frame_z, BPLANK)

  return v


def _prism_box(
  v: np.ndarray, x0: int, y0: int, z0: int, w: int, h: int, d: int, mat: str
) -> None:
  for y in range(y0, y0 + h):
    for x in range(x0, x0 + w):
      for z in range(z0, z0 + d):
        _set(v, x, y, z, mat)


def _generate_bite_mermaid_lagoon() -> np.ndarray:
  """
  Mermaid Lagoon — book dimensions:
    Twin 3×3 prismarine pillars 11 blocks apart, stepped inward layers,
    3×7 arch cap, moss and azalea trees, boulders and aquatic plants.
  """
  PRISM = _b("prismarine")
  WATER = _b("water")
  SAND = _b("sand")
  MOSS = _b("moss_block")
  MOSSC = _b("moss_carpet")
  FAZLEAVES = _b("flowering_azalea_leaves")
  AZLEAVES = _b("azalea_leaves")
  CAVEVINE = _b("cave_vines")
  DRIP = _b("big_dripleaf")
  SDRIP = _b("small_dripleaf")
  CORAL = _b("brain_coral_fan")
  SPORE = _b("spore_blossom")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 7, 11, 3
  gap = 11
  pw, pd = 3, 3
  left_x = ox
  right_x = ox + pw + gap

  # Lagoon pool and sandy edge
  for x in range(ox - 1, right_x + pw + 1):
    for z in range(oz - 1, oz + pd + 5):
      _set(v, x, oy - 1, z, WATER)
  for x in range(ox - 3, ox):
    for z in range(oz, oz + pd + 3):
      _set(v, x, oy - 1, z, SAND)

  # Left pillar — book steps 1–3 (layers step +x toward center)
  left_specs = (
    (left_x + 0, 3, 3),
    (left_x + 1, 2, 3),
    (left_x + 1, 3, 3),
    (left_x + 2, 2, 3),
    (left_x + 2, 3, 4),
    (left_x + 3, 3, 3),
  )
  y = oy
  for x0, w, d in left_specs:
    _prism_box(v, x0, y, oz, w, 1, d, PRISM)
    y += 1

  # Right pillar — mirror stepping -x toward center
  right_specs = (
    (right_x + 0, 3, 3),
    (right_x + 0, 2, 3),
    (right_x - 1, 3, 3),
    (right_x - 1, 2, 3),
    (right_x - 2, 3, 4),
    (right_x - 3, 3, 3),
  )
  y = oy
  for x0, w, d in right_specs:
    _prism_box(v, x0, y, oz, w, 1, d, PRISM)
    y += 1

  cap_y = oy + len(left_specs)
  cap_x = left_x + 3
  cap_w, cap_d = 7, 3

  # Join arch span (step 4)
  for x in range(cap_x, cap_x + cap_w):
    for z in range(oz, oz + cap_d):
      for yy in range(2):
        _set(v, x, cap_y + yy, z, PRISM)

  # 3×7 cap layer on top
  for x in range(cap_x, cap_x + cap_w):
    for z in range(oz, oz + cap_d):
      _set(v, x, cap_y + 2, z, PRISM)

  # Moss on arch top (step 7)
  for x in range(cap_x, cap_x + cap_w):
    for z in range(oz, oz + cap_d):
      _set(v, x, cap_y + 3, z, MOSS)

  # Flowering azalea trees (step 8)
  for tx in (cap_x + 1, cap_x + cap_w - 2):
    _set(v, tx, cap_y + 3, oz + 1, AZLEAVES)
    for dy in range(1, 4):
      for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
          if abs(dx) + abs(dz) + dy <= 3:
            _set(v, tx + dx, cap_y + 3 + dy, oz + 1 + dz, FAZLEAVES)

  # Prismarine boulders (steps 5–6)
  boulders = (
    (left_x + 1, oy, oz + 4, 2, 2),
    (left_x + 4, oy, oz + 1, 2, 1),
    (right_x + 1, oy, oz + 4, 2, 2),
    (cap_x + 2, oy, oz + 4, 1, 1),
    (cap_x + 4, oy - 1, oz + 5, 2, 2),
  )
  for bx, by, bz, bw, bd in boulders:
    for xi in range(bw):
      for zi in range(bd):
        h = 1 + (xi + zi) % 2
        for yy in range(h):
          _set(v, bx + xi, by + yy, bz + zi, PRISM)
        _set(v, bx + xi, by + h, bz + zi, MOSSC)

  # Cave vines and spore blossoms under arch (step 9)
  for x in range(cap_x + 1, cap_x + cap_w - 1, 2):
    _set(v, x, cap_y + 1, oz + 1, SPORE)
    for vy in range(2):
      _set(v, x, cap_y - vy, oz + 1, CAVEVINE)

  # Dripleaves and coral in water
  for x, z in ((cap_x + 1, oz + 4), (cap_x + 4, oz + 5), (right_x, oz + 4)):
    _set(v, x, oy, z, DRIP)
    _set(v, x, oy, z + 1, SDRIP)
  for x in (left_x, right_x + 2, cap_x + 5):
    _set(v, x, oy, oz + pd + 2, CORAL)

  return v


def _generate_bite_giant_beanstalk() -> np.ndarray:
  """
  Giant Beanstalk — book dimensions (32³ summary):
    Spiraling 2×2 warped wart stalk, white wool cloud, four 3×3 tuff sky towers.
  """
  WART = _b("warped_wart_block")
  WOOL = _b("white_wool")
  WGLASS = _b("white_stained_glass")
  LADDER = _b("ladder")
  CTUFF = _b("chiseled_tuff")
  TBRICK = _b("tuff_bricks")
  CTBRICK = _b("chiseled_tuff_bricks")
  TUFF = _b("tuff")
  COPPER = _b("waxed_copper_block")
  TBSTAIR = _b("tuff_brick_stairs")
  TBSLAB = _b("tuff_brick_slab")
  TBWALL = _b("tuff_brick_wall")
  CYAN = _b("cyan_wool")
  ORANGE = _b("orange_wool")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 15, 16, 2
  bx, bz = cx - 1, cz - 1
  dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))
  y = oy

  # Steps 1–5: spiraling 2×2 stalk with L-shaped leaf nubs
  for seg, (dx, dz) in enumerate(dirs * 2):
    for yy in range(2):
      for ix in range(2):
        for iz in range(2):
          _set(v, bx + ix, y + yy, bz + iz, WART)
    _set(v, bx + 2, y, bz, WART)
    _set(v, bx + 2, y, bz + 1, WART)
    _set(v, bx + 2, y + 1, bz, WART)
    y += 2
    bx += dx
    bz += dz

  cloud_y = y
  # Steps 6–7: fluffy cloud with 2×2 ladder shaft
  for cy in range(cloud_y, cloud_y + 3):
    for x in range(cx - 4, cx + 5):
      for z in range(cz - 4, cz + 5):
        if max(abs(x - cx), abs(z - cz)) > 4:
          continue
        hole = cy == cloud_y and abs(x - cx) <= 1 and abs(z - cz) <= 1
        if hole:
          continue
        edge = max(abs(x - cx), abs(z - cz)) == 4
        mat = WGLASS if edge and cy == cloud_y + 1 else WOOL
        _set(v, x, cy, z, mat)

  for ly in range(oy + 1, cloud_y):
    _set(v, cx, ly, cz, LADDER)

  tower_y = cloud_y + 3
  corners = ((cx - 3, cz - 3), (cx + 1, cz - 3), (cx - 3, cz + 1), (cx + 1, cz + 1))

  # Steps 8–11: four hollow 3×3 tuff towers with copper cores
  for idx, (tx, tz) in enumerate(corners):
    for yy in range(5):
      for dx in range(3):
        for dz in range(3):
          edge = dx in (0, 2) or dz in (0, 2)
          if edge:
            corner = dx in (0, 2) and dz in (0, 2)
            mat = CTUFF if yy == 0 and corner else TBRICK if edge else COPPER
            _set(v, tx + dx, tower_y + yy, tz + dz, mat)
          elif dx == 1 and dz == 1:
            _set(v, tx + dx, tower_y + yy, tz + dz, COPPER)
    for dx in (0, 2):
      for dz in (0, 2):
        _set(v, tx + dx, tower_y + 5, tz + dz, TBSTAIR)
        _set(v, tx + 1, tower_y + 5, tz + 1, TBSLAB)
    # Step 15 flags
    flag_color = CYAN if idx % 2 == 0 else ORANGE
    _set(v, tx + 1, tower_y + 6, tz + 1, COPPER)
    _set(v, tx + 1, tower_y + 7, tz + 1, TBWALL)
    _set(v, tx + 1, tower_y + 8, tz + 1, flag_color)

  # Steps 12–14: wall pillars and arched sides between towers
  for px, pz in ((cx - 1, cz - 1), (cx - 1, cz + 1)):
    _set(v, px, tower_y + 1, pz, CTBRICK)
    _set(v, px, tower_y + 2, pz, TUFF)
    _set(v, px, tower_y + 3, pz, TUFF)
    _set(v, px, tower_y + 4, pz, TBSLAB)

  for side_z in (cz - 2, cz + 2):
    for x in range(cx - 2, cx + 3):
      if abs(x - cx) == 1:
        _set(v, x, tower_y + 2, side_z, TBSTAIR)
      else:
        _set(v, x, tower_y + 1, side_z, TBRICK)
        _set(v, x, tower_y + 2, side_z, TBRICK if x % 2 == 0 else TUFF)

  return v


def _generate_bite_magicians_hat() -> np.ndarray:
  """
  Magician's Hat — book dimensions:
    7-tall octagonal black wool body, mangrove band, octagonal brim,
    two 3-wide 8-tall bunny ears, rabbit spawner.
  """
  BLACK = _b("black_wool")
  WHITE = _b("white_wool")
  PINK = _b("pink_wool")
  MANG = _b("mangrove_planks")
  DOOR = _b("mangrove_door")
  SPAWNER = _b("spawner")
  GRASS = _b("grass_block")
  GRAVEL = _b("gravel")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 2

  # Grass pad and gravel path
  for x in range(cx - 4, cx + 5):
    for z in range(cz - 3, cz + 6):
      _set(v, x, oy - 1, z, GRASS)
  for z in range(cz + 3, cz + 6):
    _set(v, cx, oy - 1, z, GRAVEL)
    _set(v, cx - 1, oy - 1, z, GRAVEL)

  # Body — six black wool layers + mangrove band (book 7 layers)
  for y in range(oy, oy + 6):
    for dx in range(-3, 4):
      for dz in range(-3, 4):
        if not _oct_shell(dx, dz, 3):
          continue
        if dz == 3 and abs(dx) <= 0 and y == oy + 1:
          _set(v, cx + dx, y, cz + dz, DOOR if y == oy + 1 else AIR_B)
        elif dz == 3 and dx == 0 and y in (oy + 2, oy + 3):
          _set(v, cx + dx, y, cz + dz, AIR_B)
        else:
          _set(v, cx + dx, y, cz + dz, BLACK)

  band_y = oy + 5
  for dx in range(-3, 4):
    for dz in range(-3, 4):
      if _oct_shell(dx, dz, 3):
        _set(v, cx + dx, band_y, cz + dz, MANG)

  # White wool cap inside top
  cap_y = oy + 4
  for dx in range(-2, 3):
    for dz in range(-2, 3):
      if _oct_floor(dx, dz, 2):
        _set(v, cx + dx, cap_y, cz + dz, WHITE)
  _set(v, cx, cap_y - 1, cz, SPAWNER)

  # Brim ring one block above band
  brim_y = band_y + 1
  for dx in range(-4, 5):
    for dz in range(-4, 5):
      if _oct_floor(dx, dz, 4) and not _oct_floor(dx, dz, 3):
        _set(v, cx + dx, brim_y, cz + dz, BLACK)

  ear_y = brim_y + 1
  # Straight ear (right) — 3 wide, 8 tall
  for y in range(8):
    for x in range(cx + 1, cx + 4):
      for z in range(cz - 1, cz + 2):
        mat = PINK if x == cx + 2 else WHITE
        _set(v, x, ear_y + y, z, mat)

  # Bent ear (left) — 5 up + 3 horizontal bend
  for y in range(5):
    for x in range(cx - 3, cx):
      for z in range(cz - 1, cz + 2):
        mat = PINK if x == cx - 2 else WHITE
        _set(v, x, ear_y + y, z, mat)
  bend_y = ear_y + 5
  for x in range(cx - 3, cx):
    for z in range(cz - 1, cz + 2):
      _set(v, x, bend_y, z, WHITE if x != cx - 2 else PINK)
  for i in range(3):
    for z in range(cz - 1, cz + 2):
      _set(v, cx - 3 - i, bend_y, z, WHITE)

  return v


def _generate_bite_ferocious_dragon() -> np.ndarray:
  """
  Ferocious Dragon — book dimensions (32³ summary):
    7-wide raw gold base, mangrove body/legs/tail/wings, quartz horns and membranes.
  """
  GOLD = _b("raw_gold_block")
  MANG = _b("mangrove_planks")
  MSLAB = _b("mangrove_slab")
  MSTAIR = _b("mangrove_stairs")
  MSIGN = _b("mangrove_sign")
  QUARTZ = _b("quartz_block")
  QSTAIR = _b("quartz_stairs")
  QSLAB = _b("quartz_slab")
  EYE = _b("polished_blackstone_button")
  DISP = _b("dispenser")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 3

  def _gold_disk(y: int, rad: int) -> None:
    for dx in range(-rad, rad + 1):
      for dz in range(-rad, rad + 1):
        if dx * dx + dz * dz <= rad * rad + 1:
          _set(v, cx + dx, y, cz + dz, GOLD)

  _gold_disk(oy - 1, 3)
  _gold_disk(oy, 2)
  by = oy + 1

  # Steps 2–3: zigzag front legs with quartz talons
  for lx in (cx - 2, cx + 2):
    leg = (
      (lx, by, cz + 2),
      (lx, by + 1, cz + 2),
      (lx, by + 1, cz + 3),
      (lx, by + 2, cz + 3),
      (lx, by + 2, cz + 2),
      (lx, by + 3, cz + 2),
    )
    for x, y, z in leg:
      _set(v, x, y, z, MANG)
    _set(v, lx, by, cz + 1, QSTAIR)

  # Steps 4–7: torso between legs and rear extension
  for y in range(by + 2, by + 5):
    for x in range(cx - 1, cx + 2):
      _set(v, x, y, cz + 1, MANG)
  for x in range(cx - 2, cx + 3):
    _set(v, x, by + 4, cz + 1, MSLAB)
  for z in range(cz + 2, cz + 6):
    _set(v, cx, by + 4, z, MANG)
    _set(v, cx, by + 5, z, MANG)

  # Steps 5–6: neck and head
  for y, z in ((by + 5, cz + 1), (by + 6, cz), (by + 7, cz - 1), (by + 8, cz - 2)):
    _set(v, cx, y, z, MANG)
  hy = by + 9
  for dx in (-1, 0, 1):
    for dz in (-3, -2, -1):
      _set(v, cx + dx, hy, cz + dz, MANG if dz != -3 else MSTAIR)
  _set(v, cx, hy - 1, cz - 3, DISP)
  _set(v, cx - 1, hy, cz - 3, MSIGN)
  _set(v, cx + 1, hy, cz - 3, MSIGN)
  _set(v, cx - 1, hy, cz - 2, EYE)
  _set(v, cx + 1, hy, cz - 2, EYE)
  for sx in (-1, 1):
    _set(v, cx + sx, hy + 1, cz - 2, QSTAIR)
    _set(v, cx + sx, hy + 2, cz - 2, QSLAB)

  # Step 8: hind legs
  for lx in (cx - 2, cx + 2):
    for y, z in ((by + 3, cz + 4), (by + 2, cz + 5), (by + 1, cz + 5), (by + 1, cz + 4)):
      _set(v, lx, y, z, MANG)
    _set(v, lx, by, cz + 4, QSTAIR)

  # Step 9: tail
  for y, z in ((by + 5, cz + 6), (by + 6, cz + 7), (by + 7, cz + 8), (by + 8, cz + 8)):
    _set(v, cx, y, z, MANG)

  # Step 10: spine spikes
  for y, z in ((by + 5, cz + 1), (by + 5, cz + 3), (by + 5, cz + 5), (by + 6, cz + 7), (by + 7, cz + 8)):
    _set(v, cx, y + 1, z, QSTAIR)

  # Steps 11–14: wings
  for side in (-1, 1):
    wx = cx + side * 3
    for i in range(3):
      _set(v, wx + side * i, by + 4, cz + 2, MANG)
    for dz in (-1, 0, 1):
      _set(v, wx + side * 2, by + 4, cz + 2 + dz, MANG)
    _set(v, wx + side * 2, by + 5, cz + 1, MANG)
    _set(v, wx + side * 3, by + 3, cz + 2, MANG)
    _set(v, wx + side * 2, by + 3, cz + 3, MANG)
    _set(v, wx + side * 2, by + 4, cz + 2, QUARTZ)
    _set(v, wx + side * 2, by + 3, cz + 2, QUARTZ)

  return v


def _generate_bite_bubblegum_cottage() -> np.ndarray:
  """
  Bubblegum Cottage — book dimensions (32³ summary):
    11×15 L-shaped prismarine base, birch pillars, cherry roof, cottage garden.
  """
  PBRICK = _b("prismarine_bricks")
  PSTAIR = _b("prismarine_brick_stairs")
  PWALL = _b("prismarine_brick_wall")
  SBLOG = _b("stripped_birch_log")
  WOOL = _b("white_wool")
  DIORITE = _b("diorite")
  CALCITE = _b("calcite")
  CHERRY = _b("cherry_planks")
  CSTAIR = _b("cherry_stairs")
  CSLAB = _b("cherry_slab")
  CFENCE = _b("cherry_fence")
  CTRAP = _b("cherry_trapdoor")
  BDOOR = _b("birch_door")
  BTRAP = _b("birch_trapdoor")
  BFENCE = _b("birch_fence")
  GPANE = _b("glass_pane")
  LANTERN = _b("lantern")
  AZLEAF = _b("flowering_azalea_leaves")
  VINE = _b("vine")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 7, 3

  l_cells: set[tuple[int, int]] = set()
  for x in range(ox, ox + 11):
    for z in range(oz, oz + 9):
      l_cells.add((x, z))
  for x in range(ox, ox + 4):
    for z in range(oz + 9, oz + 15):
      l_cells.add((x, z))

  wall_mats = (WOOL, DIORITE, CALCITE)

  def _perimeter(x: int, z: int) -> bool:
    return any((x + dx, z + dz) not in l_cells for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))

  # Step 1 — prismarine L foundation
  for x, z in l_cells:
    _set(v, x, oy - 1, z, PBRICK)
  for x in range(ox, ox + 3):
    _set(v, x, oy - 1, oz - 1, PSTAIR)
  for z in range(oz, oz + 6):
    for x in range(ox, ox + 2):
      _set(v, x, oy - 1, z, AIR_B)

  # Steps 2–3 — eight pillars and mixed walls
  pillars = (
    (ox, oz),
    (ox + 10, oz),
    (ox, oz + 8),
    (ox + 10, oz + 8),
    (ox, oz + 14),
    (ox + 3, oz + 14),
    (ox + 3, oz + 9),
    (ox + 10, oz + 4),
  )
  for px, pz in pillars:
    for y in range(oy, oy + 5):
      _set(v, px, y, pz, SBLOG)

  for y in range(oy, oy + 4):
    for x, z in l_cells:
      if not _perimeter(x, z):
        continue
      if x == ox + 5 and z == oz and y < oy + 3:
        _set(v, x, y, z, BDOOR if y == oy else AIR_B)
        continue
      if z == oz + 4 and x in (ox + 3, ox + 7) and y == oy + 1:
        _set(v, x, y, z, GPANE)
        continue
      _set(v, x, y, z, wall_mats[(x + y + z) % 3])

  # Step 4 — birch log beam ring
  beam_y = oy + 4
  for x, z in l_cells:
    if _perimeter(x, z):
      _set(v, x, beam_y, z, SBLOG)

  # Steps 5–7 — cherry roof with prismarine trim
  roof_y = oy + 5
  for x in range(ox, ox + 11):
    for z in range(oz, oz + 9):
      layer = min(x - ox, ox + 10 - x, z - oz, oz + 8 - z)
      if layer <= 2:
        _set(v, x, roof_y + layer, z, CHERRY if layer < 2 else CSTAIR)
      if layer == 0:
        _set(v, x, roof_y + 3, z, PBRICK)
  for x in range(ox, ox + 4):
    for z in range(oz + 9, oz + 15):
      _set(v, x, roof_y, z, CHERRY)
      _set(v, x, roof_y + 1, z, CSTAIR)
  _set(v, ox + 5, roof_y + 4, oz + 4, PSTAIR)
  _set(v, ox + 5, roof_y + 3, oz + 4, LANTERN)

  # Steps 8–11 — doorway arch, shutters, corner trim
  _set(v, ox + 4, oy + 2, oz, PWALL)
  _set(v, ox + 6, oy + 2, oz, PWALL)
  _set(v, ox + 5, oy + 3, oz, CSLAB)
  _set(v, ox + 4, oy + 3, oz, CFENCE)
  _set(v, ox + 6, oy + 3, oz, CFENCE)
  for wx in (ox + 3, ox + 7):
    _set(v, wx, oy + 1, oz + 1, CTRAP)
    _set(v, wx, oy, oz + 1, GRASS)
    _set(v, wx, oy, oz + 1, CTRAP)
  for px, pz in pillars:
    if (px, pz) in ((ox, oz), (ox + 10, oz)):
      _set(v, px, oy + 4, pz, PWALL)
      _set(v, px, oy + 5, pz, CFENCE)

  # Steps 12–14 — garden fence and landscaping
  for x in range(ox - 1, ox + 12):
    _set(v, x, oy - 1, oz - 2, BFENCE)
    if x in (ox - 1, ox + 11):
      _set(v, x, oy, oz - 2, LANTERN)
  for x in range(ox + 1, ox + 10, 3):
    for z in range(oz - 1, oz + 3):
      _set(v, x, oy, z, AZLEAF)
  for x, z in ((ox + 2, oz + 2), (ox + 8, oz + 6), (ox + 1, oz + 12)):
    _set(v, x, oy + 4, z, VINE)

  return v


def _cross(dx: int, dz: int, r: int = 2) -> bool:
  if abs(dx) > r or abs(dz) > r:
    return False
  return not (abs(dx) == r and abs(dz) == r)


def _generate_bite_enchanting_tower() -> np.ndarray:
  """
  Enchanting Tower — book dimensions:
    14-tall 5×5 cross copper tower, quartz pillars/arches, spiral oak trunk.
  """
  COPPER = _b("waxed_oxidized_cut_copper")
  QPILLAR = _b("quartz_pillar")
  QBLOCK = _b("quartz_block")
  QSTAIR = _b("quartz_stairs")
  SDOOR = _b("spruce_door")
  STRAP = _b("spruce_trapdoor")
  LADDER = _b("ladder")
  ENCH = _b("enchanting_table")
  SHELF = _b("bookshelf")
  OLOG = _b("oak_log")
  OLEAF = _b("oak_leaves")
  LANTERN = _b("lantern")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 2
  th = 14

  # Grass hill pad
  for x in range(cx - 4, cx + 5):
    for z in range(cz - 4, cz + 5):
      if (x - cx) ** 2 + (z - cz) ** 2 <= 16:
        _set(v, x, oy - 1, z, GRASS)

  # Steps 1–2 — copper cross tower + door + ladder
  for y in range(oy, oy + th):
    for dx in range(-2, 3):
      for dz in range(-2, 3):
        if not _cross(dx, dz):
          continue
        if dz == 2 and dx == 0 and y in (oy, oy + 1):
          if y == oy:
            _set(v, cx + dx, y, cz + dz, SDOOR)
          continue
        if dx == 0 and dz == 0 and oy <= y < oy + th - 1:
          _set(v, cx, y, cz, LADDER)
          continue
        _set(v, cx + dx, y, cz + dz, COPPER)

  # Step 3 — quartz corner pillars (L shapes at bounding corners)
  for corner_x, corner_z, px, pz in (
    (-2, -2, -3, -2),
    (2, -2, 2, -2),
    (-2, 2, -3, 2),
    (2, 2, 2, 2),
  ):
    for y in range(oy, oy + th + 2):
      _set(v, cx + px, y, cz + corner_z, QPILLAR)
      _set(v, cx + corner_x, y, cz + pz, QPILLAR)

  # Steps 4–5 — quartz roof deck + enchanting setup
  roof_y = oy + th
  for dx in range(-2, 3):
    for dz in range(-2, 3):
      if _cross(dx, dz):
        _set(v, cx + dx, roof_y, cz + dz, QBLOCK)
  _set(v, cx, roof_y, cz, STRAP)
  for cdx, cdz in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
    _set(v, cx + cdx, roof_y, cz + cdz, QSTAIR)
    _set(v, cx + cdx, roof_y - 1, cz + cdz, LANTERN)

  _set(v, cx, roof_y + 1, cz, ENCH)
  for dx, dz in ((0, -1), (-1, 0), (1, 0)):
    for y in range(2):
      _set(v, cx + dx, roof_y + 1 + y, cz + dz, SHELF)

  # Steps 6–7 — quartz arch crown
  arch_y = roof_y + 3
  for cdx, cdz in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
    _set(v, cx + cdx, arch_y, cz + cdz, QPILLAR)
    _set(v, cx + cdx, arch_y + 1, cz + cdz, QSTAIR)
    _set(v, cx + cdx, arch_y + 2, cz + cdz, QSTAIR)
  for dx in range(-1, 2):
    _set(v, cx + dx, arch_y + 3, cz, QSTAIR)

  # Steps 8–9 — spiral oak trunk and leaves
  spiral = (
    (2, 0),
    (2, 1),
    (1, 2),
    (0, 2),
    (-1, 2),
    (-2, 1),
    (-2, 0),
    (-2, -1),
    (-1, -2),
    (0, -2),
    (1, -2),
    (2, -1),
  )
  for i, y in enumerate(range(oy, oy + th, 2)):
    dx, dz = spiral[i % len(spiral)]
    _set(v, cx + dx, y, cz + dz, OLOG)
    _set(v, cx + dx, y + 1, cz + dz, OLOG)
    if i % 3 == 0:
      for lx, lz in ((0, 1), (1, 0), (-1, 0)):
        _set(v, cx + dx + lx, y + 1, cz + dz + lz, OLEAF)

  return v


def _wheel_plate(v: np.ndarray, wx: int, wz: int, y: int, plank: str, stair: str) -> None:
  for dx in range(3):
    for dz in range(3):
      if dx == 1 and dz == 1:
        continue
      corner = (dx in (0, 2)) and (dz in (0, 2))
      _set(v, wx + dx, y, wz + dz, stair if corner else plank)


def _generate_bite_pumpkin_carriage() -> np.ndarray:
  """
  Pumpkin Carriage — book dimensions:
    Four 3×3 jungle wheels, green concrete chassis, layered orange wool pumpkin.
  """
  JPLANK = _b("jungle_planks")
  JSTAIR = _b("jungle_stairs")
  GREEN = _b("green_concrete")
  ORANGE = _b("orange_wool")
  ADOOR = _b("acacia_door")
  VINE = _b("vine")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 7, 11, 3

  for x in range(ox - 1, ox + 16):
    for z in range(oz - 1, oz + 11):
      _set(v, x, oy - 1, z, GRASS)

  wheel_pts = ((ox, oz), (ox + 12, oz), (ox, oz + 7), (ox + 12, oz + 7))
  for wx, wz in wheel_pts:
    _wheel_plate(v, wx, wz, oy, JPLANK, JSTAIR)
    _wheel_plate(v, wx, wz, oy + 1, JPLANK, JSTAIR)

  # Steps 3–4 — green vine side rails and cross beams
  for x in range(ox + 1, ox + 12):
    _set(v, x, oy + 1, oz + 1, GREEN)
    _set(v, x, oy + 1, oz + 5, GREEN)
  for z in range(oz + 2, oz + 5):
    _set(v, ox + 6, oy + 1, z, GREEN)
    _set(v, ox + 6, oy + 2, z, GREEN)

  pcx, pcz = ox + 5, oz + 2
  # Steps 5–7 — pumpkin body layers
  for x in range(pcx, pcx + 3):
    for z in range(pcz, pcz + 3):
      _set(v, x, oy + 2, z, ORANGE)

  for x in range(pcx - 1, pcx + 4):
    for z in range(pcz - 1, pcz + 4):
      if x in (pcx - 1, pcx + 3) and z in (pcz - 1, pcz + 3):
        continue
      _set(v, x, oy + 3, z, ORANGE)

  for y in range(oy + 4, oy + 8):
    for x in range(pcx - 1, pcx + 4):
      for z in range(pcz - 1, pcz + 4):
        if x == pcx + 3 and z in (pcz + 1, pcz + 2) and y < oy + 6:
          _set(v, x, y, z, ADOOR if y == oy + 4 else AIR_B)
          continue
        dist = max(abs(x - pcx - 1), abs(z - pcz - 1))
        if dist <= 2:
          _set(v, x, y, z, ORANGE)

  # Step 8 — mirrored roof taper
  for x in range(pcx - 1, pcx + 4):
    for z in range(pcz - 1, pcz + 4):
      if x in (pcx - 1, pcx + 3) and z in (pcz - 1, pcz + 3):
        continue
      _set(v, x, oy + 8, z, ORANGE)
  for x in range(pcx, pcx + 3):
    for z in range(pcz, pcz + 3):
      _set(v, x, oy + 9, z, ORANGE)

  # Step 9 — green stem
  _set(v, pcx + 1, oy + 10, pcz + 1, GREEN)
  _set(v, pcx + 1, oy + 11, pcz + 1, GREEN)
  _set(v, pcx + 2, oy + 11, pcz + 1, GREEN)

  # Step 10 — vines
  for x, z in ((pcx - 1, pcz), (pcx + 3, pcz + 2), (pcx, pcz + 3)):
    _set(v, x, oy + 5, z, VINE)
    _set(v, x, oy + 6, z, VINE)

  return v


def _generate_bite_royal_frog() -> np.ndarray:
  """
  Royal Frog — book dimensions:
    3×3 cobble frog fountain, granite crown, water mouth channel, pond base.
  """
  COBBLE = _b("cobblestone")
  MOSSY = _b("mossy_cobblestone")
  CSTAIR = _b("cobblestone_stairs")
  MSTAIR = _b("mossy_cobblestone_stairs")
  SMOOTH = _b("smooth_stone")
  GRANITE = _b("polished_granite")
  GSTAIR = _b("polished_granite_stairs")
  SBUTTON = _b("stone_button")
  BBUTTON = _b("polished_blackstone_button")
  WATER = _b("water")
  LILY = _b("lily_pad")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 3
  mix = (COBBLE, MOSSY)

  # Pond and grass pad
  for x in range(cx - 3, cx + 4):
    for z in range(cz - 3, cz + 4):
      _set(v, x, oy - 1, z, WATER if max(abs(x - cx), abs(z - cz)) <= 2 else GRASS)
  for x in range(cx - 1, cx + 2):
    for z in range(cz - 1, cz + 2):
      _set(v, x, oy - 1, z, COBBLE)

  def _body_layer(y: int, mouth: bool, legs: bool) -> None:
    for dx in range(-1, 2):
      for dz in range(-1, 2):
        if mouth and dx == 0 and dz == 1:
          _set(v, cx + dx, y, cz + dz, WATER if y == oy else AIR_B)
          continue
        if legs and dz == 1 and dx in (-1, 1):
          _set(v, cx + dx, y, cz + dz, MSTAIR if (dx + y) % 2 == 0 else CSTAIR)
          continue
        _set(v, cx + dx, y, cz + dz, mix[(dx + dz + y) % 2])

  _body_layer(oy, mouth=True, legs=True)
  _body_layer(oy + 1, mouth=True, legs=True)
  _body_layer(oy + 2, mouth=False, legs=False)

  # Head eyes
  for dx in (-1, 1):
    _set(v, cx + dx, oy + 3, cz + 1, SMOOTH)
    _set(v, cx + dx, oy + 3, cz + 2, BBUTTON)
  for dx in range(-1, 2):
    _set(v, cx + dx, oy + 3, cz, GRANITE)

  # Crown
  for dx, dz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
    _set(v, cx + dx, oy + 4, cz + dz, GSTAIR)
  _set(v, cx - 1, oy + 4, cz, SBUTTON)
  _set(v, cx + 1, oy + 4, cz, SBUTTON)

  # Lily pads in pond
  for x, z in ((cx - 2, cz), (cx + 2, cz - 1), (cx, cz - 2)):
    _set(v, x, oy, z, LILY)

  return v


def _generate_bite_glowing_mushroom() -> np.ndarray:
  """
  Glowing Mushroom — book dimensions (32³ summary):
    Tapered mushroom stem, 15×15 sea lantern cap (scaled), soul lantern fringe.
  """
  MSTEM = _b("mushroom_stem")
  LANTERN = _b("sea_lantern")
  LBTER = _b("light_blue_terracotta")
  LBCON = _b("light_blue_concrete")
  LWOOL = _b("light_blue_wool")
  WDOOR = _b("warped_door")
  WFENCE = _b("warped_fence")
  WSLAB = _b("warped_slab")
  WPLANK = _b("warped_planks")
  SOULL = _b("soul_lantern")
  LADDER = _b("ladder")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 2

  for x in range(cx - 6, cx + 7):
    for z in range(cz - 6, cz + 7):
      _set(v, x, oy - 1, z, GRASS)

  def _stem_ring(y: int, radius: int, inset: int, height: int, nubs: bool) -> None:
    for yy in range(y, y + height):
      for dx in range(-radius, radius + 1):
        for dz in range(-radius, radius + 1):
          if not _oct_shell(dx, dz, max(1, radius - inset)):
            continue
          if dx == 0 and dz == 0:
            _set(v, cx, yy, cz, LADDER if yy < y + height - 1 else MSTEM)
            continue
          _set(v, cx + dx, yy, cz + dz, MSTEM)
      if nubs:
        for dx, dz in ((0, -radius), (0, radius), (-radius, 0), (radius, 0)):
          _set(v, cx + dx, y + height - 1, cz + dz, MSTEM)

  _stem_ring(oy, 3, 0, 3, False)
  _stem_ring(oy + 3, 3, 1, 3, True)
  _stem_ring(oy + 6, 2, 0, 4, True)
  for y in range(oy + 10, oy + 12):
    for dx, dz in ((0, -1), (0, 1), (-1, 0), (1, 0)):
      _set(v, cx + dx, y, cz + dz, MSTEM)

  # Warped entryway (step 10) — gap in stem front
  for y in range(oy, oy + 2):
    _set(v, cx, y, cz + 3, AIR_B)
  _set(v, cx, oy, cz + 3, WDOOR)
  for dx in (-1, 1):
    _set(v, cx + dx, oy + 1, cz + 3, WFENCE)
  _set(v, cx - 1, oy, cz + 3, WSLAB)
  _set(v, cx + 1, oy, cz + 3, WSLAB)
  _set(v, cx, oy, cz + 4, WPLANK)

  cap_y = oy + 12
  cap_mats = (LANTERN, LBTER, LBCON, LWOOL)

  # Steps 5–9 — glowing cap layers (scaled radius 5 ≈ 11 wide)
  for layer, rad in enumerate((5, 4, 3, 2)):
    y0 = cap_y + layer * 2
    depth = 2 if layer < 2 else 1
    for yy in range(y0, y0 + depth):
      for dx in range(-rad, rad + 1):
        for dz in range(-rad, rad + 1):
          if dx * dx + dz * dz > (rad + 0.5) ** 2:
            continue
          edge = dx * dx + dz * dz >= (rad - 0.3) ** 2
          if layer == 0 and edge:
            mat = LBTER
          elif layer == 0:
            mat = LANTERN
          else:
            mat = cap_mats[(layer + dx + dz + yy) % 4]
          _set(v, cx + dx, yy, cz + dz, mat)

  # Soul lantern fringe under cap
  for i, (dx, dz, drop) in enumerate(
    ((-3, 0, 2), (3, 0, 3), (0, -3, 2), (0, 3, 4), (-2, 2, 2))
  ):
    for d in range(drop):
      _set(v, cx + dx, cap_y - 1 - d, cz + dz, WFENCE if d < drop - 1 else SOULL)

  return v


def _boot_footprint(ox: int, oz: int) -> set[tuple[int, int]]:
  cells: set[tuple[int, int]] = set()
  cx = ox + 3
  for z in range(oz, oz + 15):
    t = (z - oz) / 14
    half_w = 2 + int(round(t * 1))
    for x in range(cx - half_w, cx + half_w + 1):
      cells.add((x, z))
  return cells


def _generate_bite_house_in_a_shoe() -> np.ndarray:
  """
  House in a Shoe — book dimensions (32³ summary):
    15-long boot sole, spruce upper, ankle tower, brick roof, chain laces.
  """
  PBBLACK = _b("polished_blackstone_bricks")
  SPRUCE = _b("spruce_planks")
  SBRICK = _b("stone_bricks")
  SWALL = _b("stone_brick_wall")
  SSTAIR = _b("stone_brick_stairs")
  CRACK = _b("cracked_stone_bricks")
  BRICK = _b("bricks")
  BSLAB = _b("brick_slab")
  ODOOR = _b("oak_door")
  OTRAP = _b("oak_trapdoor")
  GPANE = _b("glass_pane")
  CHAIN = _b("chain")
  LEAVES = _b("oak_leaves")
  LANTERN = _b("lantern")
  GRASS = _b("grass_block")
  PETAL = _b("pink_petals")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 8, 3
  foot = _boot_footprint(ox, oz)
  cx = ox + 3

  for x, z in foot:
    _set(v, x, oy - 1, z, PBBLACK)

  # Steps 2–3 — spruce walls and toe stagger
  for y in range(oy, oy + 3):
    for x, z in foot:
      if z == oz and x == cx:
        continue
      if y == oy + 1 and z in (oz + 5, oz + 9) and x in (cx - 1, cx + 1):
        _set(v, x, y, z, GPANE)
        continue
      _set(v, x, y, z, SPRUCE)

  front_cells = {(x, z) for x, z in foot if z >= oz + 10}
  for y in range(oy + 3, oy + 5):
    inset = y - oy - 2
    for x, z in front_cells:
      if x >= cx + 2 - inset:
        continue
      _set(v, x, y, z, SPRUCE)

  # Step 4 — ankle circular tower at heel
  ankle_z = oz
  for y in range(oy, oy + 4):
    for dx in range(-2, 3):
      for dz in range(-1, 2):
        if dx * dx + dz * dz <= 4:
          if dz == 0 and dx == 0 and y == oy + 1:
            _set(v, cx + dx, y, ankle_z + dz, GPANE)
          else:
            _set(v, cx + dx, y, ankle_z + dz, SPRUCE)

  # Steps 5–6 — brick roof and stone arch door
  for x in (cx - 2, cx + 2):
    for y in range(oy, oy + 4):
      _set(v, x, y, ankle_z, SWALL)
  for dx in range(-2, 3):
    for dz in range(-1, 2):
      if dx * dx + dz * dz <= 5:
        _set(v, cx + dx, oy + 4, ankle_z + dz, BRICK)
        _set(v, cx + dx, oy + 5, ankle_z + dz, BSLAB)
  _set(v, cx, oy + 4, ankle_z, LEAVES)

  for y in range(oy, oy + 3):
    _set(v, cx - 1, y, ankle_z, CRACK if y == oy else SBRICK)
    _set(v, cx + 1, y, ankle_z, SBRICK)
  _set(v, cx, oy, ankle_z, ODOOR)
  _set(v, cx - 1, oy + 3, ankle_z, SSTAIR)
  _set(v, cx + 1, oy + 3, ankle_z, SSTAIR)

  # Steps 7–9 — planters, laces, lanterns
  for wx in (cx - 1, cx + 1):
    _set(v, wx, oy, oz + 5, OTRAP)
    _set(v, wx, oy - 1, oz + 5, GRASS)
    _set(v, wx, oy, oz + 5, PETAL)
    _set(v, wx, oy + 1, oz + 5, OTRAP)

  for z in range(oz + 4, oz + 11, 2):
    _set(v, cx, oy + 3, z, CHAIN)
    _set(v, cx - 1, oy + 3, z, CHAIN)

  for z in (oz + 3, oz + 8, oz + 12):
    _set(v, cx + 2, oy + 2, z, CHAIN)
    _set(v, cx + 2, oy + 1, z, LANTERN)

  for x, z in ((cx - 2, oz + 6), (cx + 2, oz + 11)):
    _set(v, x, oy + 4, z, LEAVES)
    _set(v, x, oy + 3, z, LEAVES)

  return v


def _extrude_profile(
  v: np.ndarray,
  x0: int,
  oy: int,
  oz: int,
  cells: list[tuple[int, int, str]],
  depth: int = 3,
) -> None:
  for y, z, mat in cells:
    for dx in range(depth):
      _set(v, x0 + dx, oy + y, oz + z, mat)


def _generate_bite_alebrije_horned_chicken() -> np.ndarray:
  """Alebrije horned chicken — flat profile + mirrored legs and horns."""
  PURPUR = _b("purpur_block")
  WPLANK = _b("warped_planks")
  WSLAB = _b("warped_slab")
  WSTAIR = _b("warped_stairs")
  MPLANK = _b("mangrove_planks")
  MSTAIR = _b("mangrove_stairs")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  x0, oz, oy = 14, 10, 3
  body: list[tuple[int, int, str]] = []
  mats = (PURPUR, WPLANK, WSLAB, WSTAIR)
  for z in range(8):
    h = 3 + (z % 2)
    for y in range(h):
      body.append((y, z, mats[(y + z) % 4]))
  for z in range(8, 11):
    body.append((2, z, MSTAIR))
    body.append((3, z, WSTAIR if z % 2 == 0 else PURPUR))
  _extrude_profile(v, x0, oy, oz, body)

  for side in (0, 2):
    for y, z in ((0, 2), (1, 2), (0, 3)):
      _set(v, x0 + side, oy + y, oz + z, MPLANK if y == 1 else MSTAIR)
    for y in range(4, 8):
      _set(v, x0 + side, oy + y, oz + 5, MPLANK)

  for x in range(x0 - 1, x0 + 4):
    for z in range(oz - 2, oz + 12):
      _set(v, x, oy - 1, z, GRASS)
  return v


def _generate_bite_alebrije_winged_horse() -> np.ndarray:
  """Alebrije winged horse — warped bamboo sandstone profile with wings."""
  WPLANK = _b("warped_planks")
  WSTAIR = _b("warped_stairs")
  BAM = _b("bamboo_mosaic")
  BSLAB = _b("bamboo_mosaic_slab")
  RSAND = _b("smooth_red_sandstone")
  RSSTAIR = _b("smooth_red_sandstone_stairs")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  x0, oz, oy = 13, 9, 3
  body: list[tuple[int, int, str]] = []
  for z in range(11):
    h = 4 if 2 <= z <= 8 else 3
    for y in range(h):
      if z < 2:
        mat = RSAND
      elif z < 8:
        mat = (WPLANK, BAM, RSAND)[(y + z) % 3]
      else:
        mat = BAM if y < 2 else WSTAIR
      body.append((y, z, mat))
  _extrude_profile(v, x0, oy, oz, body, depth=3)

  for side in (0, 2):
    for y in range(3):
      _set(v, x0 + side, oy + y, oz + 4, BAM if y else RSSTAIR)
    for y, z in ((3, 5), (4, 6), (3, 7)):
      _set(v, x0 + side, oy + y, oz + z, WPLANK if y == 4 else WSTAIR)

  for x in range(x0 - 1, x0 + 4):
    for z in range(oz - 1, oz + 12):
      _set(v, x, oy - 1, z, GRASS)
  return v


def _generate_bite_alebrije_lizard() -> np.ndarray:
  """Alebrije lizard — long colorful profile with short mirrored legs."""
  BAM = _b("bamboo_mosaic")
  BSLAB = _b("bamboo_mosaic_slab")
  MPLANK = _b("mangrove_planks")
  MSTAIR = _b("mangrove_stairs")
  CHERRY = _b("cherry_planks")
  CSLAB = _b("cherry_slab")
  CSTAIR = _b("cherry_stairs")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  x0, oz, oy = 14, 8, 3
  body: list[tuple[int, int, str]] = []
  for z in range(13):
    h = 2 if z in (0, 12) else 3
    for y in range(h):
      mat = (BAM, MPLANK, CHERRY, CSTAIR)[(y + z) % 4]
      body.append((y, z, mat))
  _extrude_profile(v, x0, oy, oz, body)

  for side in (0, 2):
    for y in range(2):
      _set(v, x0 + side, oy + y, oz + 2, MSTAIR)
      _set(v, x0 + side, oy + y, oz + 9, CSLAB if y else BSLAB)

  for x in range(x0 - 1, x0 + 4):
    for z in range(oz - 1, oz + 14):
      _set(v, x, oy - 1, z, GRASS)
  return v


def _banana_wall_height(x: int, ox: int, length: int) -> int:
  edge = min(x - ox, ox + length - 1 - x)
  return 3 + min(edge, 2)


def _scoop_room(
  v: np.ndarray,
  sx: int,
  sz: int,
  oy: int,
  wool: str,
  glass: str,
  door_x: int | None,
) -> None:
  for x in range(sx, sx + 5):
    for z in range(sz, sz + 5):
      _set(v, x, oy, z, wool)
  for x in range(sx + 1, sx + 4):
    for z in range(sz + 1, sz + 4):
      _set(v, x, oy + 1, z, wool)
  for y in range(oy + 2, oy + 5):
    for x in range(sx, sx + 5):
      for z in range(sz, sz + 5):
        if x in (sx, sx + 4) or z in (sz, sz + 4):
          if door_x is not None and x == door_x and z == sz and y < oy + 4:
            continue
          if x == sx + 2 and z == sz and y == oy + 2:
            _set(v, x, y, z, glass)
          else:
            _set(v, x, y, z, wool)
  for x in range(sx + 1, sx + 4):
    for z in range(sz + 1, sz + 4):
      _set(v, x, oy + 5, z, wool)


def _generate_bite_banana_split_base() -> np.ndarray:
  """
  Banana-Split Base — book dimensions (32³ summary):
    18-wide banana shell, three 5×5 wool scoop rooms, cherry toppings.
  """
  SAND = _b("smooth_sandstone")
  SSLAB = _b("smooth_sandstone_slab")
  SSTAIR = _b("smooth_sandstone_stairs")
  QUARTZ = _b("quartz_block")
  WCONC = _b("white_concrete")
  SPRUCE = _b("spruce_planks")
  SSLAB_S = _b("spruce_slab")
  BDOOR = _b("birch_door")
  OAK = _b("oak_planks")
  PINK = _b("pink_wool")
  BLUE = _b("light_blue_wool")
  YELLOW = _b("yellow_wool")
  PGLASS = _b("pink_stained_glass")
  BGLASS = _b("light_blue_stained_glass")
  YGLASS = _b("yellow_stained_glass")
  RED = _b("red_wool")
  WFENCE = _b("warped_fence")
  SNOW = _b("snow_block")
  BTNS = (_b("warped_button"), _b("birch_button"), _b("crimson_button"), _b("acacia_button"))
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 7, 13, 3
  length = 18
  z0, z1 = oz, oz + 4

  for x in range(ox, ox + length):
    h = _banana_wall_height(x, ox, length)
    for z in (z0, z1):
      for y in range(oy, oy + h):
        mat = SAND
        if y == h - 1 + oy and (x + z) % 3 == 0:
          mat = SPRUCE if z == z0 else SSLAB_S
        if x in (ox, ox + length - 1) and y >= oy + h - 2:
          mat = QUARTZ
        if y == oy and x in (ox + 2, ox + length - 3):
          mat = SSTAIR
        _set(v, x, y, z, mat)
    if x == ox + 8:
      _set(v, x, oy, z0, BDOOR)

  for x in range(ox + 1, ox + length - 1):
    for z in range(z0 + 1, z1):
      _set(v, x, oy - 1, z, WCONC)
      _set(v, x, oy, z, OAK)

  for x in range(ox - 1, ox + length + 1):
    for z in range(oz - 1, oz + 6):
      if 0 <= x < res and 0 <= z < res and v[x, oy - 1, z] == AIR_B:
        _set(v, x, oy - 1, z, SNOW)

  _scoop_room(v, ox + 1, oz + 1, oy + 1, PINK, PGLASS, ox + 5)
  _scoop_room(v, ox + 6, oz + 1, oy + 1, BLUE, BGLASS, ox + 10)
  _scoop_room(v, ox + 11, oz + 1, oy + 1, YELLOW, YGLASS, None)

  for sx, wool in ((ox + 3, PINK), (ox + 8, BLUE), (ox + 13, YELLOW)):
    _set(v, sx, oy + 6, oz + 3, RED)
    _set(v, sx, oy + 7, oz + 3, WFENCE)

  for i, x in enumerate(range(ox + 2, ox + length - 2, 2)):
    for z in (z0, z1):
      _set(v, x, oy + 2, z, BTNS[i % 4])

  return v


def _tea_trim(dx: int, dz: int) -> str:
  return _b("yellow_concrete") if (dx + dz) % 2 == 0 else _b("light_blue_terracotta")


def _generate_bite_floating_tea_party() -> np.ndarray:
  """
  Floating Tea Party — book dimensions (32³ summary):
    Octagonal teacup pool, floating teapot house, waterfall elevator.
  """
  WHITE = _b("white_concrete")
  YELLOW = _b("yellow_concrete")
  LTBLUE = _b("light_blue_terracotta")
  PURPLE = _b("purple_wool")
  GPANE = _b("blue_stained_glass_pane")
  WATER = _b("water")
  LADDER = _b("ladder")
  GRASS = _b("grass_block")
  OAK = _b("oak_planks")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ccx, ccz, coy = 10, 21, 3
  tcx, tcz, toy = 21, 11, 12

  for x in range(4, 28):
    for z in range(4, 28):
      _set(v, x, 1, z, GRASS if (x + z) % 5 else OAK)

  for dx in range(-5, 6):
    for dz in range(-5, 6):
      if _oct_floor(dx, dz, 4):
        _set(v, ccx + dx, 2, ccz + dz, PURPLE)

  for dx in range(-2, 3):
    for dz in range(-2, 3):
      if _oct_floor(dx, dz, 2):
        _set(v, ccx + dx, coy, ccz + dz, WHITE)
  for y in range(coy + 1, coy + 3):
    for dx in range(-2, 3):
      for dz in range(-2, 3):
        if _oct_shell(dx, dz, 2):
          _set(v, ccx + dx, y, ccz + dz, WHITE)
  for dx in range(-2, 3):
    for dz in range(-2, 3):
      if _oct_shell(dx, dz, 2):
        _set(v, ccx + dx, coy + 3, ccz + dz, _tea_trim(dx, dz))
        if abs(dx) == 2 and dz == 0:
          _set(v, ccx + dx, coy + 1, ccz + dz, LTBLUE)
          _set(v, ccx + dx, coy + 2, ccz + dz, LTBLUE)
  _set(v, ccx, coy + 1, ccz + 3, LADDER)
  _set(v, ccx, coy + 2, ccz + 3, LADDER)
  for y in range(coy + 1, coy + 3):
    for dx in range(-1, 2):
      for dz in range(-1, 2):
        _set(v, ccx + dx, y, ccz + dz, WATER)

  for dx in range(-2, 3):
    for dz in range(-2, 3):
      if not _oct_floor(dx, dz, 2):
        continue
      mat = WHITE if abs(dx) <= 1 and abs(dz) <= 1 else _tea_trim(dx, dz)
      _set(v, tcx + dx, toy, tcz + dz, mat)

  for y in range(toy + 1, toy + 3):
    for dx in range(-2, 3):
      for dz in range(-2, 3):
        if _oct_shell(dx, dz, 2) and not (abs(dx) == 2 and abs(dz) == 2):
          if dz == 2 and dx == 0 and y == toy + 1:
            continue
          _set(v, tcx + dx, y, tcz + dz, WHITE)
  for y in range(toy + 3, toy + 6):
    for dx in range(-2, 3):
      for dz in range(-2, 3):
        if _oct_shell(dx, dz, 2):
          if abs(dz) == 2 and abs(dx) <= 1 and y in (toy + 3, toy + 4):
            _set(v, tcx + dx, y, tcz + dz, GPANE)
          elif dz == 2 and dx == 0 and y == toy + 3:
            continue
          else:
            _set(v, tcx + dx, y, tcz + dz, WHITE)

  for dx in range(-2, 3):
    for dz in range(-2, 3):
      if _oct_floor(dx, dz, 2):
        mat = WHITE if abs(dx) <= 1 and abs(dz) <= 1 else _tea_trim(dx, dz)
        _set(v, tcx + dx, toy + 6, tcz + dz, mat)
  _set(v, tcx, toy + 7, tcz, YELLOW)

  for y in range(toy + 2, toy + 5):
    _set(v, tcx - 3, y, tcz, LTBLUE)
    _set(v, tcx - 3, y, tcz + 1, LTBLUE)
    _set(v, tcx - 4, y, tcz + 1, LTBLUE)
  for i in range(4):
    _set(v, tcx + 2 + i, toy + 2 - min(i, 1), tcz - 1, LTBLUE)
    _set(v, tcx + 2 + i, toy + 2 - min(i, 1), tcz, LTBLUE)
  spout_x, spout_z = tcx + 5, tcz
  _set(v, spout_x, toy + 2, spout_z, WATER)
  for y in range(coy + 3, toy + 2):
    _set(v, spout_x, y, spout_z, WATER)

  return v


def _dragon_lattice(v: np.ndarray, px: int, pz: int, base_y: int, height: int) -> None:
  YELLOW = _b("yellow_concrete")
  WHITE = _b("white_concrete")
  for y in range(base_y, base_y + height):
    _set(v, px, y, pz, YELLOW)
    _set(v, px + 2, y, pz, YELLOW)
  for y in range(base_y + 1, base_y + height, 2):
    for x in range(px, px + 3):
      _set(v, x, y, pz, WHITE)


def _rail_torch(v: np.ndarray, x: int, y: int, z: int, powered: bool) -> None:
  _set(v, x, y, z, _b("powered_rail") if powered else _b("rail"))
  _set(v, x - 1, y, z, _b("redstone_torch"))


def _generate_bite_dragon_roller_coaster() -> np.ndarray:
  """
  Dragon Roller Coaster — book dimensions (32³ summary):
    Copper dragon head station, S-curved body track, twin steep drops.
  """
  COPPER = _b("oxidized_cut_copper")
  BONE = _b("bone_block")
  BLACK = _b("black_concrete")
  FROG = _b("ochre_froglight")
  YELLOW = _b("yellow_concrete")
  WHITE = _b("white_concrete")
  RAIL = _b("rail")
  POWER = _b("powered_rail")
  RTORCH = _b("redstone_torch")
  REDSAND = _b("red_sand")
  OLOG = _b("stripped_oak_log")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  hx, hz, oy = 10, 24, 2

  for x in range(2, 30):
    for z in range(2, 30):
      _set(v, x, oy - 1, z, REDSAND)

  head = (
    (0, 0), (0, 1), (0, 2),
    (-1, 1), (-1, 2), (1, 1), (1, 2),
    (-2, 2), (2, 2),
  )
  for dx, dz in head:
    _set(v, hx + dx, oy, hz + dz, COPPER)
  for dx in (-1, 0, 1):
    for dz in (1, 2):
      _set(v, hx + dx, oy + 1, hz + dz, COPPER)
  for dx in (-1, 0, 1):
    _set(v, hx + dx, oy + 1, hz, BONE)
    _set(v, hx + dx, oy, hz, BONE)
  for dx in (-1, 1):
    _set(v, hx + dx, oy + 2, hz + 1, COPPER)
    _set(v, hx + dx, oy + 2, hz + 2, YELLOW)
  _set(v, hx, oy + 2, hz + 1, BLACK)
  _set(v, hx - 1, oy + 2, hz + 2, BLACK)
  _set(v, hx + 1, oy + 2, hz + 2, FROG)
  for dx in (-1, 0, 1):
    _set(v, hx + dx, oy + 3, hz, BONE)
  for z in range(hz - 1, hz - 5, -1):
    for dx in (-1, 0, 1):
      _set(v, hx + dx, oy, z, COPPER)
    if z <= hz - 2:
      for dx in (-1, 0, 1):
        _set(v, hx + dx, oy + 1, z, COPPER)

  _rail_torch(v, hx, oy + 1, hz - 1, True)
  _rail_torch(v, hx, oy + 1, hz - 2, True)
  _set(v, hx, oy + 1, hz - 3, RAIL)
  _set(v, hx, oy + 1, hz - 4, RAIL)

  body = [
    (10, 19), (10, 18), (10, 17), (9, 16), (8, 15), (7, 14), (7, 13),
    (8, 12), (9, 11), (10, 10), (11, 9), (12, 8), (13, 8), (14, 9),
    (15, 10), (16, 11), (17, 12), (18, 13), (19, 14), (20, 15),
  ]
  for i, (x, z) in enumerate(body):
    _set(v, x, oy, z, COPPER)
    _set(v, x, oy + 1, z, COPPER if i % 4 else OLOG)
    powered = i % 3 != 2
    _rail_torch(v, x, oy + 2, z, powered)

  peak1_x, peak1_z = 17, 12
  for step in range(8):
    y = oy + 2 + step
    _set(v, peak1_x, y, peak1_z, COPPER)
    _set(v, peak1_x + 1, y, peak1_z, COPPER)
    _rail_torch(v, peak1_x, y + 1, peak1_z, step % 4 != 3)
  _dragon_lattice(v, peak1_x - 1, peak1_z + 1, oy, 8)

  peak2_x, peak2_z = 12, 8
  for step in range(5):
    y = oy + 2 + step
    _set(v, peak2_x, y, peak2_z, COPPER)
    _rail_torch(v, peak2_x, y + 1, peak2_z, True)
  _dragon_lattice(v, peak2_x - 1, peak2_z, oy, 5)

  drop_path = [(17, 11), (16, 10), (15, 10), (14, 11), (13, 12), (12, 13),
               (11, 14), (10, 15), (10, 16), (10, 17), (10, 18), (10, 19),
               (10, 20), (10, 21), (10, 22), (10, 23), (10, 24)]
  for i, (x, z) in enumerate(drop_path):
    y = max(oy + 2, oy + 9 - i // 2)
    _set(v, x, y, z, COPPER)
    _rail_torch(v, x, y + 1, z, i % 4 != 1)

  return v


def _book_roof_height(x: int, spine_x: int, max_rise: int = 3) -> int:
  return 1 + min(abs(x - spine_x) // 2, max_rise)


def _generate_bite_spellbook_shop() -> np.ndarray:
  """
  Spellbook Shop — book dimensions (32³ summary):
    13×7 pillar frame, birch walls, open-book roof, magic glass plumes.
  """
  DLOG = _b("dark_oak_log")
  SBRICK = _b("stone_bricks")
  SBSTAIR = _b("stone_brick_stairs")
  BIRCH = _b("stripped_birch_log")
  GPANE = _b("glass_pane")
  DOOR = _b("dark_oak_door")
  BNEST = _b("bee_nest")
  HONEY = _b("honeycomb_block")
  BROWN = _b("brown_concrete")
  GOLD = _b("gold_block")
  QUARTZ = _b("smooth_quartz")
  QSLAB = _b("smooth_quartz_slab")
  RED = _b("red_wool")
  LANTERN = _b("lantern")
  PURPLE = _b("purple_stained_glass_pane")
  LBLUE = _b("light_blue_stained_glass_pane")
  YELLOW = _b("yellow_stained_glass_pane")
  GRASS = _b("grass_block")
  SBWALL = _b("stone_brick_wall")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 9, 12, 2
  width, depth = 13, 7
  spine_x = ox + width // 2
  pillars_x = [ox, ox + 4, ox + 8, ox + width - 1]
  rows_z = [oz, oz + depth - 1]

  for x in range(ox - 1, ox + width + 1):
    for z in range(oz - 1, oz + depth + 1):
      _set(v, x, oy - 1, z, GRASS)

  for i, px in enumerate(pillars_x):
    for j, pz in enumerate(rows_z):
      height = 6 if i in (0, len(pillars_x) - 1) else 4
      for y in range(oy, oy + height):
        _set(v, px, y, pz, DLOG)

  for px in pillars_x:
    for pz in rows_z:
      _set(v, px, oy - 1, pz, SBRICK)
      for side in (-1, 1):
        if 0 <= px + side < res:
          _set(v, px + side, oy - 1, pz, SBSTAIR)

  for x in range(ox, ox + width):
    if x in pillars_x:
      continue
    if x in (spine_x - 1, spine_x):
      continue
    for z in range(oz, oz + depth):
      if z in rows_z:
        continue
      _set(v, x, oy, z, SBRICK)

  for x in range(ox + 1, ox + width - 1):
    if x in pillars_x:
      continue
    for z in range(oz + 1, oz + depth - 1):
      for y in (oy + 1, oy + 2):
        if x in (ox + 2, ox + 6, ox + 10) and y == oy + 2 and z == oz + 3:
          _set(v, x, y, z, GPANE)
        else:
          _set(v, x, y, z, BIRCH)
  _set(v, spine_x, oy + 1, oz, DOOR)
  _set(v, spine_x, oy + 2, oz, DOOR)
  _set(v, spine_x, oy + 3, oz, BIRCH)

  band_y = oy + 3
  for px in pillars_x:
    for pz in rows_z:
      _set(v, px, band_y, pz, BNEST)
  for x in range(ox + 1, ox + width - 1):
    for z in (oz, oz + depth - 1):
      if x not in pillars_x:
        _set(v, x, band_y, z, HONEY)
  for px, pz in ((ox, oz), (ox + width - 1, oz), (ox, oz + depth - 1), (ox + width - 1, oz + depth - 1)):
    _set(v, px + (1 if px == ox else -1), band_y, pz, SBWALL)

  roof_base = oy + 4
  for x in range(ox - 1, ox + width + 1):
    for z in range(oz - 1, oz + depth + 1):
      rise = _book_roof_height(x, spine_x)
      for layer in range(rise):
        y = roof_base + layer
        corner = x in (ox - 1, ox + width) and z in (oz - 1, oz + depth)
        mat = GOLD if corner and layer == rise - 1 else BROWN
        _set(v, x, y, z, mat)
      top_y = roof_base + rise
      _set(v, x, top_y, z, QSLAB if (x + z) % 2 else QUARTZ)

  _set(v, spine_x, roof_base + 4, oz - 1, RED)
  _set(v, spine_x, roof_base + 3, oz - 1, RED)
  for px, pz in ((ox - 1, oz - 1), (ox + width, oz - 1), (ox - 1, oz + depth), (ox + width, oz + depth)):
    _set(v, px, roof_base - 1, pz, LANTERN)

  plumes = (PURPLE, LBLUE, YELLOW, PURPLE)
  cx, cz = spine_x, oz + depth // 2
  for i, (dx, dz, dy) in enumerate(((0, 0, 5), (1, 1, 6), (0, 2, 7), (-1, 1, 6), (-2, 0, 5), (-1, -1, 6))):
    _set(v, cx + dx, roof_base + dy, cz + dz, plumes[i % len(plumes)])

  return v


def _lamp_width(z: int, cz: int) -> int:
  t = z - cz
  if t <= 0:
    return max(1, 2 + t)
  if t <= 3:
    return 2
  if t <= 6:
    return 3
  return max(1, 3 - (t - 6))


def _generate_bite_genie_lamp_boat() -> np.ndarray:
  """
  Genie-Lamp Boat — book dimensions (32³ summary):
    Yellow terracotta lamp hull, mast sails, interior deck, cobweb spout smoke.
  """
  YTER = _b("yellow_terracotta")
  CYAN = _b("cyan_terracotta")
  OAK = _b("oak_log")
  WOOL = _b("white_wool")
  BARREL = _b("barrel")
  SMOKER = _b("smoker")
  CRAFT = _b("crafting_table")
  COBWEB = _b("cobweb")
  WATER = _b("water")
  SAND = _b("sand")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, wl = 16, 13, 13

  for x in range(cx - 8, cx + 9):
    for z in range(cz - 4, cz + 12):
      _set(v, x, wl - 4, z, SAND)
      for y in range(wl - 3, wl + 1):
        _set(v, x, y, z, WATER)

  for z in range(cz - 2, cz + 9):
    half = _lamp_width(z, cz)
    for x in range(cx - half, cx + half + 1):
      _set(v, x, wl, z, YTER)
      if z >= cz and z <= cz + 6:
        _set(v, x, wl + 1, z, CYAN if z in (cz + 2, cz + 3, cz + 4) else YTER)
      if z >= cz + 1 and z <= cz + 5 and abs(x - cx) == half:
        _set(v, x, wl + 2, z, YTER)
      if z in (cz + 1, cz + 5) and abs(x - cx) <= half - 1:
        _set(v, x, wl + 2, z, YTER)
      if z in (cz + 2, cz + 3, cz + 4) and abs(x - cx) == half:
        _set(v, x, wl + 3, z, YTER)

  _set(v, cx + 3, wl + 1, cz + 7, YTER)
  _set(v, cx + 3, wl + 2, cz + 8, YTER)
  _set(v, cx + 3, wl + 3, cz + 8, YTER)
  _set(v, cx + 4, wl + 2, cz + 7, YTER)

  _set(v, cx - 1, wl + 1, cz + 3, BARREL)
  _set(v, cx + 1, wl + 1, cz + 3, SMOKER)
  _set(v, cx, wl + 1, cz + 2, CRAFT)

  mast_y = wl + 4
  for y in range(mast_y, mast_y + 5):
    _set(v, cx, y, cz + 4, OAK)
  for x in range(cx - 1, cx + 2):
    _set(v, x, mast_y + 4, cz + 4, OAK)
  for x in range(cx - 1, cx + 2):
    for z in (cz + 3, cz + 5):
      for dy in range(2):
        for dx in range(2):
          _set(v, x + dx - 1, mast_y + 2 + dy, z, WOOL)

  spout_x, spout_z = cx, cz - 2
  cob_steps = ((0, 0, 3), (1, 0, 4), (1, 1, 5), (2, 1, 6), (2, 2, 7), (1, 3, 8))
  for dx, dy, dz in cob_steps:
    _set(v, spout_x + dx, wl + dy, spout_z - dz, COBWEB)

  return v


def _generate_bite_emerald_apartments() -> np.ndarray:
  """
  Emerald Apartments — book dimensions (32³ summary):
    Emerald pillar tower, copper glass walls, entrance arch, beacon crown, apartments.
  """
  EMERALD = _b("emerald_block")
  COPPER = _b("waxed_oxidized_cut_copper")
  GLASS = _b("lime_stained_glass_pane")
  DEEPS = _b("cobbled_deepslate")
  DSTAIR = _b("cobbled_deepslate_stairs")
  DSLAB = _b("cobbled_deepslate_slab")
  DOOR = _b("birch_door")
  BEACON = _b("beacon")
  LANTERN = _b("lantern")
  GOLD = _b("gold_block")
  RAWG = _b("raw_gold_block")
  BAMBOO = _b("bamboo_block")
  SBAMBOO = _b("stripped_bamboo_block")
  MOSSY = _b("mossy_cobblestone")
  PETALS = _b("pink_petals")
  POPPY = _b("poppy")
  GRASS = _b("grass_block")
  CHERRY = _b("cherry_leaves")
  CRAFT = _b("crafting_table")
  FURNACE = _b("furnace")
  BED = _b("red_bed")
  QSTAIR = _b("quartz_stairs")
  LCARPET = _b("lime_carpet")
  GCARPET = _b("green_carpet")
  BARREL = _b("barrel")
  CHEST = _b("chest")
  WATER = _b("water")
  SOUL = _b("soul_sand")
  MAGMA = _b("magma_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 12, 13, 2
  w, d = 7, 5
  x1, x2 = ox, ox + w - 1
  z1, z2 = oz, oz + d - 1
  top = oy + 19

  for x in range(ox - 3, ox + w + 4):
    for z in range(oz - 6, oz + d + 3):
      _set(v, x, oy - 1, z, GRASS)
      if (x + z) % 7 == 0:
        _set(v, x, oy, z, CHERRY)

  for px, pz in ((x1, z1), (x2, z1), (x1, z2), (x2, z2)):
    for y in range(oy, top + 1):
      _set(v, px, y, pz, EMERALD)

  win_x = (ox + 2, ox + 3, ox + 4)
  for y in range(oy + 2, top - 1):
    for x in range(ox + 1, ox + w - 1):
      if x in win_x and y % 3 != 0:
        _set(v, x, y, z1, GLASS)
      elif y >= oy + 4:
        _set(v, x, y, z1, COPPER)
    for z in range(oz + 1, oz + d - 1):
      if y <= oy + 5:
        _set(v, x1, y, z, COPPER if z % 2 else GLASS)
        _set(v, x2, y, z, COPPER if z % 2 else GLASS)
    for x in range(ox + 1, ox + w - 1):
      _set(v, x, y, z2, COPPER)

  for y in range(oy + 3, oy + 10):
    _set(v, ox + 3, y, oz - 1, EMERALD)
    _set(v, ox + 2, y, oz - 2, EMERALD)
    _set(v, ox + 4, y, oz - 2, EMERALD)
  for x in range(ox + 2, ox + 5):
    _set(v, x, oy + 2, oz - 1, COPPER)
  _set(v, ox + 3, oy + 3, oz - 1, DOOR)
  _set(v, ox + 3, oy + 4, oz - 1, DOOR)
  _set(v, ox + 2, oy + 3, oz - 1, EMERALD)
  _set(v, ox + 4, oy + 3, oz - 1, EMERALD)

  for side_x in (ox - 2, ox + w + 1):
    for y in range(oy + 4, oy + 16):
      _set(v, side_x, y, oz + 2, EMERALD)
    for y in range(oy + 4, oy + 10):
      for z in (oz + 1, oz + 3):
        _set(v, side_x, y, z, COPPER if y % 3 else GLASS)
    for z in range(oz, oz + d):
      _set(v, side_x, oy + 10, z, DEEPS)

  roof_y = top
  for x in range(ox, ox + w):
    _set(v, x, roof_y, z1, DSTAIR)
    _set(v, x, roof_y, z2, DSTAIR)
    for z in range(z1 + 1, z2):
      _set(v, x, roof_y, z, DEEPS)
  for dx in range(-2, 3):
    for dz in range(-2, 3):
      if abs(dx) <= 2 and abs(dz) <= 2:
        _set(v, ox + 3 + dx, roof_y + 1, oz + 2 + dz, EMERALD)
  for dx in range(-1, 2):
    for dz in range(-1, 2):
      _set(v, ox + 3 + dx, roof_y + 2, oz + 2 + dz, EMERALD)
  _set(v, ox + 3, roof_y + 3, oz + 2, BEACON)
  for px, pz in ((x1, z1), (x2, z1), (x1, z2), (x2, z2)):
    _set(v, px, top, pz, LANTERN)

  road_z = oz - 4
  for x in range(ox + 1, ox + 6):
    mats = (GOLD, RAWG, BAMBOO, SBAMBOO)
    _set(v, x, oy, road_z, mats[x % len(mats)])
    _set(v, x - 1, oy, road_z, MOSSY)
    _set(v, x + 1, oy, road_z, MOSSY)
    _set(v, x, oy, road_z - 1, PETALS if x % 2 else POPPY)

  for floor_y in (oy + 4, oy + 8, oy + 12):
    for x in range(ox + 1, ox + w - 1):
      for z in range(oz + 1, oz + d - 1):
        _set(v, x, floor_y, z, DSLAB)
  _set(v, ox + 2, oy + 5, oz + 2, CRAFT)
  _set(v, ox + 4, oy + 5, oz + 2, FURNACE)
  _set(v, ox + 2, oy + 9, oz + 3, BED)
  _set(v, ox + 4, oy + 9, oz + 2, QSTAIR)
  _set(v, ox + 3, oy + 9, oz + 2, LCARPET)
  _set(v, ox + 2, oy + 13, oz + 2, BARREL)
  _set(v, ox + 4, oy + 13, oz + 3, CHEST)
  _set(v, ox + 5, oy + 3, oz + 2, WATER)
  _set(v, ox + 5, oy + 2, oz + 2, SOUL)
  _set(v, ox + 1, oy + 3, oz + 2, WATER)
  _set(v, ox + 1, oy + 2, oz + 2, MAGMA)

  return v


def _generate_bite_atlantis_abode() -> np.ndarray:
  """
  Atlantis Abode — book dimensions (32³ summary):
    7×7 sandstone underwater tower, pillar balcony, terracotta dome, sea plants.
  """
  CSAND = _b("cut_sandstone")
  SAND = _b("sandstone")
  SSLAB = _b("sandstone_slab")
  SWALL = _b("sandstone_wall")
  SSTAIR = _b("sandstone_stairs")
  ORANGE = _b("orange_terracotta")
  YELLOW = _b("yellow_terracotta")
  YCONC = _b("yellow_concrete")
  SEA = _b("sea_lantern")
  WATER = _b("water")
  SANDF = _b("sand")
  KELP = _b("kelp")
  SEAGRASS = _b("seagrass")
  PICKLE = _b("sea_pickle")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz, oy = 16, 16, 5
  rad = 3

  for x in range(4, 28):
    for z in range(4, 28):
      _set(v, x, oy - 5, z, SANDF)
      for y in range(oy - 4, oy + 16):
        _set(v, x, y, z, WATER)

  for y in range(oy, oy + 3):
    for dx in range(-rad, rad + 1):
      for dz in range(-rad, rad + 1):
        if not _oct_floor(dx, dz, rad):
          continue
        if dz == -rad and abs(dx) <= 1 and y < oy + 2:
          continue
        if abs(dx) == rad and dz == 0 and y < oy + 2:
          continue
        _set(v, cx + dx, y, cz + dz, CSAND)

  for dx in (-1, 0, 1):
    _set(v, cx + dx, oy + 2, cz - rad, SSLAB)
  for dx in (-1, 0, 1):
    if abs(dx) == rad:
      _set(v, cx + dx, oy + 1, cz, SWALL)
  for dx, dz in ((-rad, -rad), (rad, -rad), (-rad, rad), (rad, rad)):
    _set(v, cx + dx, oy, cz + dz, SSTAIR)

  for y in range(oy + 3, oy + 7):
    for dx in range(-rad, rad + 1):
      for dz in range(-rad, rad + 1):
        if _oct_shell(dx, dz, rad):
          if dz == -rad and abs(dx) <= 1 and y == oy + 4:
            continue
          _set(v, cx + dx, y, cz + dz, SAND if y < oy + 6 else CSAND)

  deck_y = oy + 7
  for dx in range(-rad, rad + 1):
    for dz in range(-rad, rad + 1):
      if _oct_shell(dx, dz, rad):
        _set(v, cx + dx, deck_y, cz + dz, CSAND)
        if _oct_shell(dx, dz, rad + 1):
          _set(v, cx + dx, deck_y, cz + dz, SSTAIR)
      elif _oct_floor(dx, dz, rad - 1):
        _set(v, cx + dx, deck_y, cz + dz, ORANGE if (dx + dz) % 2 else YELLOW)

  for dx, dz in ((-rad, 0), (rad, 0), (0, -rad), (0, rad), (-rad, -rad), (rad, rad), (-rad, rad), (rad, -rad)):
    if not _oct_floor(dx, dz, rad):
      continue
    _set(v, cx + dx, deck_y + 1, cz + dz, CSAND if abs(dx) + abs(dz) == rad else SWALL)
    _set(v, cx + dx, deck_y + 2, cz + dz, SWALL)
    _set(v, cx + dx, deck_y + 3, cz + dz, CSAND)

  arch_y = deck_y + 4
  for dx in range(-rad, rad + 1):
    for dz in range(-rad, rad + 1):
      if abs(dx) == rad or abs(dz) == rad:
        _set(v, cx + dx, arch_y, cz + dz, SSTAIR)
      elif abs(dx) == rad - 1 or abs(dz) == rad - 1:
        _set(v, cx + dx, arch_y, cz + dz, ORANGE if (dx + dz) % 2 else YELLOW)

  for layer, inset in enumerate((0, 1, 2)):
    y = arch_y + 1 + layer
    r = rad - inset
    for dx in range(-r, r + 1):
      for dz in range(-r, r + 1):
        if not _oct_floor(dx, dz, r):
          continue
        if abs(dx) == r or abs(dz) == r:
          mat = CSAND if abs(dx) + abs(dz) == r else ORANGE
        else:
          mat = YELLOW if layer % 2 else YCONC
        _set(v, cx + dx, y, cz + dz, mat)
  _set(v, cx, arch_y + 4, cz, SEA)
  for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
    _set(v, cx + dx, arch_y + 4, cz + dz, CSAND)

  for dx, dz, dy in (
    (0, -4, 0), (1, -3, 1), (-1, -2, 2), (0, 0, 3), (2, 1, 0), (-2, 2, -1),
  ):
    _set(v, cx + dx, oy + dy, cz + dz, KELP if (dx + dz) % 2 else SEAGRASS)
  for dx in range(-2, 3):
    _set(v, cx + dx, deck_y + 1, cz + rad + 1, PICKLE)

  return v


def _palace_tower(
  v: np.ndarray,
  tcx: int,
  tcz: int,
  oy: int,
  tall: bool,
  QUARTZ: str,
  SQUARTZ: str,
  QSTAIR: str,
  PRISM: str,
  PURPUR: str,
  CHERRY: str,
  CSTAIR: str,
  CSLAB: str,
  front_dz: int,
) -> None:
  body_h = 8 if tall else 5
  for y in range(2):
    for dx in range(-2, 3):
      for dz in range(-2, 3):
        if _cross(dx, dz, 2):
          _set(v, tcx + dx, oy + y, tcz + dz, QUARTZ)
          if abs(dx) == 2 and abs(dz) == 2:
            _set(v, tcx + dx, oy + y - 1, tcz + dz, QSTAIR)
  for y in range(oy + 2, oy + 2 + body_h):
    for dx in range(-2, 3):
      for dz in range(-2, 3):
        if _cross(dx, dz, 2) and (abs(dx) == 2 or abs(dz) == 2):
          _set(v, tcx + dx, y, tcz + dz, SQUARTZ)
  _set(v, tcx, oy + 3, tcz + front_dz, PRISM)
  _set(v, tcx, oy + 4, tcz + front_dz, PRISM)
  for dx, dz in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
    _set(v, tcx + dx, oy + 2 + body_h, tcz + dz, PRISM)
  ring_y = oy + 2 + body_h
  for dx in range(-2, 3):
    for dz in range(-2, 3):
      if _cross(dx, dz, 2) and (abs(dx) == 2 or abs(dz) == 2):
        _set(v, tcx + dx, ring_y, tcz + dz, PURPUR)
  for layer in range(3):
    rad = 2 - layer
    for dx in range(-rad, rad + 1):
      for dz in range(-rad, rad + 1):
        if abs(dx) == rad or abs(dz) == rad:
          mat = CSLAB if (dx + dz + layer) % 2 else CSTAIR
          _set(v, tcx + dx, ring_y + 1 + layer, tcz + dz, mat if layer > 0 else CHERRY)
    _set(v, tcx, ring_y + 1 + layer, tcz, CHERRY)


def _generate_bite_fairy_tale_palace() -> np.ndarray:
  """
  Fairy-Tale Palace — book dimensions (32³ summary):
    Twin entrance towers, courtyard wings, back towers, cherry central roof, moat.
  """
  QUARTZ = _b("quartz_block")
  SQUARTZ = _b("smooth_quartz")
  QSTAIR = _b("quartz_stairs")
  QSLAB = _b("quartz_slab")
  PRISM = _b("prismarine_wall")
  PURPUR = _b("purpur_block")
  CHERRY = _b("cherry_planks")
  CSTAIR = _b("cherry_stairs")
  CSLAB = _b("cherry_slab")
  BGLASS = _b("light_blue_stained_glass_pane")
  CFENCE = _b("cherry_fence")
  CYAN = _b("cyan_wool")
  PINK = _b("pink_wool")
  BIRCH = _b("birch_log")
  BLEAVES = _b("birch_leaves")
  LANTERN = _b("lantern")
  BOOTS = _b("diamond_boots")
  WATER = _b("water")
  GRASS = _b("grass_block")
  PETALS = _b("pink_petals")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  oy = 2
  ft1, ft2 = 10, 17
  fz = 24
  bt1, bt2 = 8, 20
  bz = 10

  for x in range(4, 28):
    for z in range(4, 28):
      edge = x in (4, 27) or z in (4, 27)
      _set(v, x, oy - 1, z, WATER if edge else GRASS)
      if not edge and (x + z) % 5 == 0:
        _set(v, x, oy - 1, z, PETALS)

  _palace_tower(v, ft1, fz, oy, False, QUARTZ, SQUARTZ, QSTAIR, PRISM, PURPUR, CHERRY, CSTAIR, CSLAB, -2)
  _palace_tower(v, ft2, fz, oy, False, QUARTZ, SQUARTZ, QSTAIR, PRISM, PURPUR, CHERRY, CSTAIR, CSLAB, -2)

  arch_y = oy + 5
  for x in range(ft1 + 1, ft2):
    _set(v, x, arch_y, fz, PURPUR)
    _set(v, x, arch_y + 1, fz, QUARTZ)
  _set(v, ft1 + 2, arch_y + 1, fz, QSLAB)
  _set(v, ft2 - 2, arch_y + 1, fz, QSLAB)

  for z in range(fz - 1, bz - 1, -1):
    for x in (ft1 - 2, ft2 + 2):
      for y in range(oy, oy + 4):
        _set(v, x, y, z, QUARTZ if y < oy + 2 else SQUARTZ)
      _set(v, x, oy + 4, z, QSTAIR)
      _set(v, x, oy + 4, z, QSLAB if z % 2 else QSTAIR)

  _palace_tower(v, bt1, bz, oy, True, QUARTZ, SQUARTZ, QSTAIR, PRISM, PURPUR, CHERRY, CSTAIR, CSLAB, 2)
  _palace_tower(v, bt2, bz, oy, True, QUARTZ, SQUARTZ, QSTAIR, PRISM, PURPUR, CHERRY, CSTAIR, CSLAB, 2)

  plat_y = oy + 8
  for x in range(bt1, bt2 + 1):
    _set(v, x, plat_y, bz, QUARTZ)
    _set(v, x, plat_y + 1, bz, PURPUR if x % 2 else QUARTZ)
  for x in range(bt1 + 3, bt2 - 2):
    _set(v, x, oy + 4, bz + 4, QSLAB)

  back_y = plat_y + 2
  for x in range(bt1 + 1, bt2):
    for y in range(back_y, back_y + 4):
      _set(v, x, y, bz, SQUARTZ if y < back_y + 3 else PURPUR)
  for x in (bt1 + 4, bt1 + 8, bt1 + 12):
    for y in range(back_y + 1, back_y + 3):
      _set(v, x, y, bz, BGLASS)
  for dx in range(-1, 2):
    for dy in range(-1, 2):
      _set(v, bt1 + 8 + dx, back_y + dy, bz, AIR_B)

  roof_y = oy + 5
  for z in range(bz + 1, fz - 2):
    for x in range(bt1 + 1, bt2):
      if (x + z) % 4 == 0:
        _set(v, x, roof_y + 1, z, BGLASS)
      mid = abs(x - 14)
      layer = min(mid // 2, 3)
      _set(v, x, roof_y + layer, z, CHERRY if layer % 2 else CSTAIR)
  _set(v, 14, roof_y + 4, 16, CHERRY)
  _set(v, 15, roof_y + 4, 16, CHERRY)

  for tcx, tcz in ((ft1, fz), (ft2, fz), (bt1, bz), (bt2, bz)):
    _set(v, tcx, oy + 10, tcz, CFENCE)
    _set(v, tcx, oy + 11, tcz, CYAN)
    _set(v, tcx + 1, oy + 11, tcz, PINK)
    _set(v, tcx, oy + 7, tcz + (2 if tcz == bz else -2), LANTERN)

  for x in range(ft1 - 1, ft2 + 2, 4):
    _set(v, x, oy, fz - 3, BIRCH)
    _set(v, x, oy + 1, fz - 3, BLEAVES)
    _set(v, x + 1, oy + 1, fz - 3, BLEAVES)

  for x in range(ft1 + 1, ft2):
    _set(v, x, oy, fz + 1, PURPUR)
  _set(v, 14, oy, fz - 4, BOOTS)

  return v


_GENERATORS: dict[str, object] = {
  "bite_creeper": _generate_bite_creeper,
  "bite_toadstool_house": _generate_bite_toadstool_house,
  "bite_alarm_system": _generate_bite_alarm_system,
  "bite_combination_lock": _generate_bite_combination_lock,
  "bite_fairy_treehouse": _generate_bite_fairy_treehouse,
  "bite_flying_school": _generate_bite_flying_school,
  "bite_item_destroyer": _generate_bite_item_destroyer,
  "bite_firefighter_plane": _generate_bite_firefighter_plane,
  "bite_shooting_gallery": _generate_bite_shooting_gallery,
  "bite_halloween_maze": _generate_bite_halloween_maze,
  "bite_train_station": _generate_bite_train_station,
  "bite_cart_collector": _generate_bite_cart_collector,
  "bite_bouncy_castle": _generate_bite_bouncy_castle,
  "bite_medieval_windmill": _generate_bite_medieval_windmill,
  "bite_portal_toggle": _generate_bite_portal_toggle,
  "bite_outdoor_amphitheatre": _generate_bite_outdoor_amphitheatre,
  "bite_hidden_bunker": _generate_bite_hidden_bunker,
  "bite_dolphin_fountain": _generate_bite_dolphin_fountain,
  "bite_aviary_pyramid": _generate_bite_aviary_pyramid,
  "bite_deep_sea_submarine": _generate_bite_deep_sea_submarine,
  "bite_underwater_airlock": _generate_bite_underwater_airlock,
  "bite_tropical_chalet": _generate_bite_tropical_chalet,
  "bite_survivalists_vault": _generate_bite_survivalists_vault,
  "bite_unicorn_statue": _generate_bite_unicorn_statue,
  "bite_hillside_home": _generate_bite_hillside_home,
  "bite_marine_tugboat": _generate_bite_marine_tugboat,
  "bite_sidewalk_cafe": _generate_bite_sidewalk_cafe,
  "bite_bee_haven": _generate_bite_bee_haven,
  "bite_fishing_shack": _generate_bite_fishing_shack,
  "bite_bedrock_train": _generate_bite_bedrock_train,
  "bite_rainbow_stables": _generate_bite_rainbow_stables,
  "bite_marketplace_stall": _generate_bite_marketplace_stall,
  "bite_floor_is_lava": _generate_bite_floor_is_lava,
  "bite_overworld_showroom": _generate_bite_overworld_showroom,
  "bite_hanging_home": _generate_bite_hanging_home,
  "bite_trader_sleigh": _generate_bite_trader_sleigh,
  "bite_space_rocket": _generate_bite_space_rocket,
  "bite_jungle_shrine": _generate_bite_jungle_shrine,
  "bite_super_slide": _generate_bite_super_slide,
  "bite_lighthouse": _generate_bite_lighthouse,
  "bite_cluck_cluck_coop": _generate_bite_cluck_cluck_coop,
  "bite_norse_longhouse": _generate_bite_norse_longhouse,
  "bite_wardrobe_portal": _generate_bite_wardrobe_portal,
  "bite_pig_hot_air_balloon": _generate_bite_pig_hot_air_balloon,
  "bite_big_red_barn": _generate_bite_big_red_barn,
  "bite_pagoda": _generate_bite_pagoda,
  "bite_igloo_hideout": _generate_bite_igloo_hideout,
  "bite_allay_statue": _generate_bite_allay_statue,
  "bite_old_western_jail": _generate_bite_old_western_jail,
  "bite_secret_island_base": _generate_bite_secret_island_base,
  "bite_greenhouse": _generate_bite_greenhouse,
  "bite_steamboat": _generate_bite_steamboat,
  "bite_parkour_pachinko": _generate_bite_parkour_pachinko,
  "bite_horse_racecourse": _generate_bite_horse_racecourse,
  "bite_skull_cove": _generate_bite_skull_cove,
  "bite_potion_factory": _generate_bite_potion_factory,
  "bite_monster_truck_bus": _generate_bite_monster_truck_bus,
  "bite_wishing_well": _generate_bite_wishing_well,
  "bite_carousel": _generate_bite_carousel,
  "bite_villager_island_head": _generate_bite_villager_island_head,
  "bite_giant_grandfather_clock": _generate_bite_giant_grandfather_clock,
  "bite_hot_spring": _generate_bite_hot_spring,
  "bite_magic_mirror": _generate_bite_magic_mirror,
  "bite_mermaid_lagoon": _generate_bite_mermaid_lagoon,
  "bite_giant_beanstalk": _generate_bite_giant_beanstalk,
  "bite_magicians_hat": _generate_bite_magicians_hat,
  "bite_ferocious_dragon": _generate_bite_ferocious_dragon,
  "bite_bubblegum_cottage": _generate_bite_bubblegum_cottage,
  "bite_enchanting_tower": _generate_bite_enchanting_tower,
  "bite_pumpkin_carriage": _generate_bite_pumpkin_carriage,
  "bite_royal_frog": _generate_bite_royal_frog,
  "bite_glowing_mushroom": _generate_bite_glowing_mushroom,
  "bite_house_in_a_shoe": _generate_bite_house_in_a_shoe,
  "bite_alebrije_horned_chicken": _generate_bite_alebrije_horned_chicken,
  "bite_alebrije_winged_horse": _generate_bite_alebrije_winged_horse,
  "bite_alebrije_lizard": _generate_bite_alebrije_lizard,
  "bite_banana_split_base": _generate_bite_banana_split_base,
  "bite_floating_tea_party": _generate_bite_floating_tea_party,
  "bite_dragon_roller_coaster": _generate_bite_dragon_roller_coaster,
  "bite_spellbook_shop": _generate_bite_spellbook_shop,
  "bite_genie_lamp_boat": _generate_bite_genie_lamp_boat,
  "bite_emerald_apartments": _generate_bite_emerald_apartments,
  "bite_fairy_tale_palace": _generate_bite_fairy_tale_palace,
  "bite_atlantis_abode": _generate_bite_atlantis_abode,
}
