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
}
