"""Procedural generators for Minecraft Exploded Builds: Medieval Fortress."""

from __future__ import annotations

import numpy as np

from ..data.palette import AIR
from .exploded_fortress_registry import FORTRESS_BUILDS


def generate_fortress_build(build_id: str) -> np.ndarray:
  if build_id not in FORTRESS_BUILDS:
    raise KeyError(f"Unknown fortress build: {build_id}")
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
        edge = x in (x0, x0 + w - 1) or z in (z0, z0 + d - 1)
        if hollow and not edge:
          continue
        _set(v, x, y, z, mat)


def _generate_fortress_turret() -> np.ndarray:
  """
  Castle Turret — book dimensions (exploded build page):
    7x7 base, 5x5 core tower 12 blocks tall, corner pillars 7 blocks,
    crenellated 7x7 battlement crown with spruce fence corbels.
  """
  STONE = _b("stone_bricks")
  STAIRS = _b("stone_brick_stairs")
  SLAB = _b("stone_brick_slab")
  PLANKS = _b("spruce_planks")
  FENCE = _b("spruce_fence")
  LADDER = _b("ladder")
  TORCH = _b("torch")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz = 16, 16
  oy = 1

  base = 7
  core = 5
  tower_h = 12
  pillar_h = 7

  bx = cx - base // 2
  bz = cz - base // 2
  tx = cx - core // 2
  tz = cz - core // 2

  # Grass pad under base
  for x in range(bx - 1, bx + base + 1):
    for z in range(bz - 1, bz + base + 1):
      _set(v, x, oy - 1, z, GRASS)

  # 7x7 stone base with slab trim on outer edge
  for x in range(bx, bx + base):
    for z in range(bz, bz + base):
      edge = x in (bx, bx + base - 1) or z in (bz, bz + base - 1)
      _set(v, x, oy, z, SLAB if edge else STONE)

  # Corner buttress pillars (stone brick stairs)
  corners = (
    (bx, bz),
    (bx + base - 1, bz),
    (bx, bz + base - 1),
    (bx + base - 1, bz + base - 1),
  )
  for px, pz in corners:
    for y in range(oy + 1, oy + 1 + pillar_h):
      _set(v, px, y, pz, STAIRS)

  # 5x5 hollow tower core
  for y in range(oy + 1, oy + 1 + tower_h):
    for x in range(tx, tx + core):
      for z in range(tz, tz + core):
        edge = x in (tx, tx + core - 1) or z in (tz, tz + core - 1)
        if edge:
          _set(v, x, y, z, STONE)
        else:
          _set(v, x, y, z, AIR_B)

  # Arrow loop slits on each face (1-block openings)
  slit_y = (oy + 4, oy + 8)
  for y in slit_y:
    _set(v, tx + core // 2, y, tz, AIR_B)  # north
    _set(v, tx + core // 2, y, tz + core - 1, AIR_B)  # south
    _set(v, tx, y, tz + core // 2, AIR_B)  # west
    _set(v, tx + core - 1, y, tz + core // 2, AIR_B)  # east

  # Interior spruce plank platforms
  for floor_y in (oy + 4, oy + 8):
    for x in range(tx + 1, tx + core - 1):
      for z in range(tz + 1, tz + core - 1):
        _set(v, x, floor_y, z, PLANKS)

  # Ladder up interior wall
  for y in range(oy + 1, oy + tower_h):
    _set(v, tx + 1, y, tz + 1, LADDER)

  # Spruce fence corbels under battlement overhang
  crown_y = oy + 1 + tower_h
  for x in range(bx, bx + base):
    for z in range(bz, bz + base):
      edge = x in (bx, bx + base - 1) or z in (bz, bz + base - 1)
      if edge:
        _set(v, x, crown_y - 1, z, FENCE)

  # Battlement platform (7x7)
  for x in range(bx, bx + base):
    for z in range(bz, bz + base):
      _set(v, x, crown_y, z, STONE)

  # Crenellations — alternating merlons on perimeter
  for x in range(bx, bx + base):
    for z in range(bz, bz + base):
      on_edge = x in (bx, bx + base - 1) or z in (bz, bz + base - 1)
      if on_edge and (x + z) % 2 == 0:
        _set(v, x, crown_y + 1, z, STONE)
        _set(v, x, crown_y + 2, z, SLAB)

  # Torches on corner merlons
  for px, pz in corners:
    _set(v, px, crown_y + 2, pz, TORCH)

  return v


def _wall_mat(x: int, z: int, y: int) -> str:
  STONE = _b("stone_bricks")
  COBBLE = _b("cobblestone")
  MOSSY = _b("mossy_stone_bricks")
  if (x + z + y) % 7 == 0:
    return MOSSY
  if (x + z) % 3 == 0:
    return COBBLE
  return STONE


def _build_wall_segment(
  v: np.ndarray,
  x0: int,
  z0: int,
  length: int,
  thickness: int,
  height: int,
  oy: int,
  *,
  along_x: bool,
  exterior_side: str,
) -> None:
  """Build a hollow wall segment with arrow slits and interior corridor."""
  STONE = _b("stone_bricks")
  PLANKS = _b("spruce_planks")
  FENCE = _b("spruce_fence")
  SLAB = _b("stone_brick_slab")
  LADDER = _b("ladder")
  TORCH = _b("torch")
  AIR_B = AIR

  for i in range(length):
    for t in range(thickness):
      for y in range(height):
        if along_x:
          x, z = x0 + i, z0 + t
        else:
          x, z = x0 + t, z0 + i

        outer = t == 0 if exterior_side in ("north", "west") else t == thickness - 1
        inner = t == thickness - 1 if exterior_side in ("north", "west") else t == 0
        shell = outer or inner

        if shell:
          _set(v, x, oy + y, z, _wall_mat(x, z, y))
        elif y == 0:
          _set(v, x, oy, z, STONE)  # floor of corridor
        else:
          _set(v, x, oy + y, z, AIR_B)

        # Arrow slits on exterior face
        if outer and y in (2, 4) and i % 4 == 2:
          _set(v, x, oy + y, z, AIR_B)

    # Ladder inside corridor every 4 blocks
    if i % 4 == 1:
      if along_x:
        lx, lz = x0 + i, z0 + 1
      else:
        lx, lz = x0 + 1, z0 + i
      for y in range(1, height):
        _set(v, lx, oy + y, lz, LADDER)

  # Walkway and crenellations on top
  top_y = oy + height
  for i in range(length):
    for t in range(thickness):
      if along_x:
        x, z = x0 + i, z0 + t
      else:
        x, z = x0 + t, z0 + i
      _set(v, x, top_y, z, PLANKS)
      outer = t == 0 if exterior_side in ("north", "west") else t == thickness - 1
      inner = t == thickness - 1 if exterior_side in ("north", "west") else t == 0
      if outer and i % 2 == 0:
        _set(v, x, top_y + 1, z, STONE)
        _set(v, x, top_y + 2, z, SLAB)
      if inner:
        _set(v, x, top_y + 1, z, FENCE)
      if outer and i % 6 == 0:
        _set(v, x, top_y + 2, z, TORCH)


def _generate_fortress_outer_wall() -> np.ndarray:
  """
  Outer Wall corner — book dimensions (scaled for 32³):
    L-shaped corner, 5x5 tower, two 11-block wall arms, 3 thick, 8 tall.
    Interior walkways, arrow slits, crenellations, courtyard path.
  """
  STONE = _b("stone_bricks")
  COBBLE = _b("cobblestone")
  MOSSY = _b("mossy_stone_bricks")
  STAIRS = _b("stone_brick_stairs")
  SLAB = _b("stone_brick_slab")
  PLANKS = _b("spruce_planks")
  S_STAIRS = _b("spruce_stairs")
  FENCE = _b("spruce_fence")
  DOOR = _b("oak_door")
  LADDER = _b("ladder")
  TORCH = _b("torch")
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  FLOWER = _b("oxeye_daisy")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  oy = 1

  # L-corner placement — tower at (8,8), walls extend +X and +Z
  tx, tz = 8, 8
  tower = 5
  wall_len = 11
  wall_thick = 3
  wall_h = 8

  # Ground — grass courtyard inside L, dirt outside
  for x in range(7, 25):
    for z in range(7, 25):
      inside = x >= tx + 1 and z >= tz + 1
      _set(v, x, oy - 1, z, GRASS if inside else DIRT)

  # Corner tower (5x5 hollow)
  for y in range(wall_h):
    for x in range(tx, tx + tower):
      for z in range(tz, tz + tower):
        edge = x in (tx, tx + tower - 1) or z in (tz, tz + tower - 1)
        if edge:
          mat = MOSSY if (x + z) % 4 == 0 else COBBLE if (x + z) % 3 == 0 else STONE
          _set(v, x, oy + y, z, mat)
        else:
          _set(v, x, oy + y, z, AIR_B if y > 0 else STONE)

  # Arrow slits on tower exterior
  for y in (oy + 2, oy + 4, oy + 6):
    _set(v, tx, y, tz + 2, AIR_B)
    _set(v, tx + 2, y, tz, AIR_B)

  # Oak door facing courtyard
  _set(v, tx + 2, oy + 1, tz + tower - 1, DOOR)
  _set(v, tx + 2, oy + 2, tz + tower - 1, DOOR)

  # Interior spruce stairs winding up tower
  for step in range(6):
    _set(v, tx + 1, oy + 1 + step, tz + 1 + step, S_STAIRS)

  # Ladder in tower
  for y in range(1, wall_h):
    _set(v, tx + 3, oy + y, tz + 3, LADDER)

  # Wall along +X (north face exterior)
  _build_wall_segment(
    v, tx + tower, tz, wall_len, wall_thick, wall_h, oy,
    along_x=True, exterior_side="north",
  )

  # Wall along +Z (west face exterior)
  _build_wall_segment(
    v, tx, tz + tower, wall_len, wall_thick, wall_h, oy,
    along_x=False, exterior_side="west",
  )

  # Tower battlement top
  top_y = oy + wall_h
  for x in range(tx, tx + tower):
    for z in range(tz, tz + tower):
      _set(v, x, top_y, z, PLANKS)
      on_edge = x in (tx, tx + tower - 1) or z in (tz, tz + tower - 1)
      if on_edge:
        if (x + z) % 2 == 0:
          _set(v, x, top_y + 1, z, STONE)
          _set(v, x, top_y + 2, z, SLAB)
        else:
          _set(v, x, top_y + 1, z, FENCE)

  # Torches on tower corners
  for px, pz in ((tx, tz), (tx + tower - 1, tz), (tx, tz + tower - 1)):
    _set(v, px, top_y + 2, pz, TORCH)

  # Stone brick stair base trim along walls
  for i in range(wall_len):
    _set(v, tx + tower + i, tz, oy - 1, STAIRS)
    _set(v, tx, tz + tower + i, oy - 1, STAIRS)

  # Courtyard cobblestone path
  for x in range(tx + 2, tx + tower + 4):
    _set(v, x, oy, tz + 3, COBBLE)
  for z in range(tz + 2, tz + tower + 4):
    _set(v, tx + 3, oy, z, COBBLE)

  # Flowers in courtyard
  for fx, fz in ((tx + 4, tz + 4), (tx + 6, tz + 5), (tx + 5, tz + 7)):
    _set(v, fx, oy, fz, FLOWER)

  return v


def _generate_fortress_portcullis() -> np.ndarray:
  """
  Portcullis Gatehouse — book dimensions (scaled for 32³):
    14-wide gatehouse, 8-wide spruce fence gate, gravel counterweight,
    piston redstone engine in 3-block pit, crenellated stone walls.
  """
  STONE = _b("stone_bricks")
  COBBLE = _b("cobblestone")
  SLAB = _b("stone_brick_slab")
  PLANKS = _b("spruce_planks")
  GATE = _b("spruce_fence")
  GRAVEL = _b("gravel")
  PISTON = _b("piston")
  STICKY = _b("sticky_piston")
  R_TORCH = _b("redstone_torch")
  REPEATER = _b("redstone_repeater")
  DUST = _b("redstone_dust")
  LEVER = _b("lever")
  HOPPER = _b("hopper")
  DROPPER = _b("dropper")
  TORCH = _b("torch")
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  oy = 1

  gx = 9  # gatehouse origin x
  gz = 12
  gate_w = 8
  tower_w = 3
  depth = 7
  height = 10
  total_w = tower_w + gate_w + tower_w  # 14

  gate_x0 = gx + tower_w
  gate_x1 = gate_x0 + gate_w

  # Ground
  for x in range(gx - 1, gx + total_w + 1):
    for z in range(gz - 2, gz + depth + 2):
      _set(v, x, oy - 1, z, GRASS if z < gz + depth else DIRT)

  # 3-block-deep mechanism pit under gate
  for x in range(gate_x0, gate_x1):
    for z in range(gz + 1, gz + depth - 1):
      for y in range(oy - 3, oy):
        _set(v, x, y, z, COBBLE)

  # Side towers (flanking gatehouse walls)
  for side_x in (gx, gx + total_w - tower_w):
    for y in range(height):
      for z in range(gz, gz + depth):
        edge = z in (gz, gz + depth - 1) or side_x in (gx, gx + total_w - tower_w)
        shell = z in (gz, gz + depth - 1) or (
          side_x == gx and z > gz
        ) or (
          side_x == gx + total_w - tower_w and z > gz
        )
        if shell or y == 0:
          mat = COBBLE if (side_x + z + y) % 4 == 0 else STONE
          _set(v, side_x, oy + y, z, mat)
          if side_x == gx + total_w - tower_w:
            _set(v, side_x + 1, oy + y, z, mat)
          if side_x == gx:
            _set(v, side_x + 2, oy + y, z, mat)
        else:
          _set(v, side_x + (1 if side_x == gx + total_w - tower_w else 0), oy + y, z, AIR_B)

  # Fill back and front walls connecting towers
  for y in range(height):
    for x in range(gx, gx + total_w):
      for z in (gz, gz + depth - 1):
        if gate_x0 <= x < gate_x1 and y < 7:
          continue  # gate opening
        _set(v, x, oy + y, z, STONE if (x + z) % 3 else COBBLE)

  # Portcullis gate — spruce fence grid (closed position)
  gate_h = 6
  for y in range(gate_h):
    for x in range(gate_x0, gate_x1):
      _set(v, x, oy + y, gz + 3, GATE)
  # Gravel counterweight row at gate base
  for x in range(gate_x0, gate_x1):
    _set(v, x, oy, gz + 3, GRAVEL)

  # Gravel column in left tower (counterweight shaft)
  for y in range(oy, oy + 7):
    _set(v, gx + 1, oy + y, gz + 3, GRAVEL)

  # Arrow slits on tower faces
  for y in (oy + 2, oy + 5, oy + 8):
    _set(v, gx, y, gz + 3, AIR_B)
    _set(v, gx + total_w - 1, y, gz + 3, AIR_B)

  # Upper guard floor
  floor_y = oy + 7
  for x in range(gx, gx + total_w):
    for z in range(gz + 1, gz + depth - 1):
      _set(v, x, floor_y, z, PLANKS)

  # Redstone engine on upper floor (left side)
  mech_x = gx + 1
  mech_z = gz + 1
  _set(v, mech_x, floor_y + 1, mech_z, LEVER)
  _set(v, mech_x + 1, floor_y + 1, mech_z, DUST)
  _set(v, mech_x + 2, floor_y + 1, mech_z, REPEATER)
  _set(v, mech_x + 3, floor_y + 1, mech_z, DROPPER)
  _set(v, mech_x + 4, floor_y + 1, mech_z, HOPPER)
  # Redstone torch tower
  for y in range(1, 6):
    _set(v, gx, oy + y, gz + 5, R_TORCH)

  # Pistons above gate (down-facing) and below (up-facing)
  piston_y_top = oy + 8
  piston_y_bot = oy - 1
  for x in range(gate_x0, gate_x1):
    _set(v, x, piston_y_top, gz + 3, PISTON)
    _set(v, x, piston_y_bot, gz + 3, STICKY)
    _set(v, x, piston_y_top, gz + 4, DUST)

  # Crenellations on top
  top_y = oy + height
  for x in range(gx, gx + total_w):
    for z in range(gz, gz + depth):
      _set(v, x, top_y, z, SLAB)
      if (x + z) % 2 == 0:
        _set(v, x, top_y + 1, z, STONE)

  # Torches on battlements
  for x in range(gx, gx + total_w, 3):
    _set(v, x, top_y + 2, gz, TORCH)
    _set(v, x, top_y + 2, gz + depth - 1, TORCH)

  # Interior torches
  _set(v, gx + total_w - 2, oy + 4, gz + 5, TORCH)
  _set(v, gx + 2, oy + 4, gz + 5, TORCH)

  return v


def _stone_mat(x: int, z: int, y: int) -> str:
  STONE = _b("stone_bricks")
  MOSSY = _b("mossy_stone_bricks")
  CRACKED = _b("cracked_stone_bricks")
  CHISELED = _b("chiseled_stone_bricks")
  COBBLE = _b("cobblestone")
  r = (x + z + y) % 11
  if r == 0:
    return CHISELED
  if r in (3, 7):
    return MOSSY
  if r in (5, 9):
    return CRACKED
  if r == 2:
    return COBBLE
  return STONE


def _generate_fortress_keep() -> np.ndarray:
  """
  Castle Keep — book dimensions (scaled for 32³):
    12x12 main shell, four 3x3 corner towers, 10-block walls,
    crenellated roof deck, central lookout, tiered hill base.
  """
  STONE = _b("stone_bricks")
  MOSSY = _b("mossy_stone_bricks")
  STAIRS = _b("stone_brick_stairs")
  SLAB = _b("stone_brick_slab")
  PLANKS = _b("spruce_planks")
  FENCE = _b("spruce_fence")
  DOOR = _b("spruce_door")
  RED = _b("red_carpet")
  WHITE = _b("white_carpet")
  BANNER = _b("red_banner")
  TORCH = _b("torch")
  GRASS = _b("grass_block")
  DIRT = _b("dirt")
  COBBLE = _b("cobblestone")
  BOOKS = _b("bookshelf")
  BED = _b("red_bed")
  LADDER = _b("ladder")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz = 10, 10
  oy = 2
  keep = 12
  wall_h = 10

  # Tiered hill base
  for x in range(ox - 2, ox + keep + 2):
    for z in range(oz - 2, oz + keep + 2):
      _set(v, x, oy - 2, z, COBBLE if (x + z) % 3 == 0 else STONE)
      _set(v, x, oy - 1, z, GRASS if abs(x - ox - keep // 2) < 7 and abs(z - oz - keep // 2) < 7 else DIRT)

  # Main keep walls (12x12 hollow, 2-block thick walls)
  for y in range(wall_h):
    for x in range(ox, ox + keep):
      for z in range(oz, oz + keep):
        edge_x = x in (ox, ox + keep - 1)
        edge_z = z in (oz, oz + keep - 1)
        inner_x = x in (ox + 1, ox + keep - 2)
        inner_z = z in (oz + 1, oz + keep - 2)
        shell = edge_x or edge_z
        inner_shell = (edge_x and not edge_z) or (edge_z and not edge_x) or (inner_x and edge_z) or (inner_z and edge_x)

        if shell or (y == 0 and inner_x and inner_z):
          if shell:
            _set(v, x, oy + y, z, _stone_mat(x, z, y))
          elif y == 0:
            _set(v, x, oy, z, COBBLE)
        elif inner_x and inner_z:
          _set(v, x, oy + y, z, AIR_B)

  # Corner towers (3x3 protruding at each corner)
  tower_h = wall_h + 2
  tower_offsets = (
    (ox - 1, oz - 1),
    (ox + keep - 2, oz - 1),
    (ox - 1, oz + keep - 2),
    (ox + keep - 2, oz + keep - 2),
  )
  for tx, tz in tower_offsets:
    for y in range(tower_h):
      for dx in range(3):
        for dz in range(3):
          x, z = tx + dx, tz + dz
          edge = dx in (0, 2) or dz in (0, 2)
          if edge or y == 0:
            _set(v, x, oy + y, z, _stone_mat(x, z, y))
          else:
            _set(v, x, oy + y, z, AIR_B)
    # Banner on tower
    _set(v, tx + 1, oy + 6, tz + (0 if tz < oz else 2), BANNER)
    # Ladder inside tower
    _set(v, tx + 1, oy + 1, tz + 1, LADDER)

  # Arrow slits and putlog holes on walls
  for y in (oy + 3, oy + 6):
    _set(v, ox + keep // 2, y, oz, AIR_B)
    _set(v, ox + keep // 2, y, oz + keep - 1, AIR_B)
    _set(v, ox, y, oz + keep // 2, AIR_B)
    _set(v, ox + keep - 1, y, oz + keep // 2, AIR_B)
  for x in range(ox + 2, ox + keep - 2, 3):
    _set(v, x, oy + 4, oz + 1, AIR_B)
    _set(v, x, oy + 4, oz + keep - 2, AIR_B)

  # Entrance (south face) with recessed door
  door_x = ox + keep // 2
  door_z = oz + keep - 1
  _set(v, door_x, oy + 1, door_z, DOOR)
  _set(v, door_x, oy + 2, door_z, DOOR)
  _set(v, door_x - 1, oy + 1, door_z, STAIRS)
  _set(v, door_x + 1, oy + 1, door_z, STAIRS)
  _set(v, door_x, oy + 3, door_z - 1, TORCH)

  # Stone bridge approach
  for z in range(oz + keep, oz + keep + 3):
    for x in range(door_x - 2, door_x + 3):
      _set(v, x, oy, z, STONE)
      _set(v, x, oy + 1, z, COBBLE if (x + z) % 2 else STONE)

  # Interior floors and rooms
  for x in range(ox + 2, ox + keep - 2):
    for z in range(oz + 2, oz + keep - 2):
      _set(v, x, oy, z, RED)
  # Dining area (white carpet center)
  for x in range(ox + 4, ox + 8):
    for z in range(oz + 4, oz + 8):
      _set(v, x, oy, z, WHITE)
  # Bookshelves (library)
  for x in range(ox + 2, ox + 5):
    _set(v, x, oy + 1, oz + 2, BOOKS)
    _set(v, x, oy + 2, oz + 2, BOOKS)
  # Guest beds
  for bx, bz in ((ox + 2, oz + 8), (ox + 8, oz + 8), (ox + 8, oz + 2)):
    _set(v, bx, oy + 1, bz, BED)

  # Stone stair corbels under battlements
  corbel_y = oy + wall_h - 1
  for x in range(ox, ox + keep):
    for z in range(oz, oz + keep):
      if x in (ox, ox + keep - 1) or z in (oz, oz + keep - 1):
        _set(v, x, corbel_y, z, STAIRS)

  # Roof deck (spruce planks)
  roof_y = oy + wall_h
  for x in range(ox, ox + keep):
    for z in range(oz, oz + keep):
      _set(v, x, roof_y, z, PLANKS)

  # Crenellations on perimeter
  for x in range(ox, ox + keep):
    for z in range(oz, oz + keep):
      on_edge = x in (ox, ox + keep - 1) or z in (oz, oz + keep - 1)
      if on_edge and (x + z) % 2 == 0:
        _set(v, x, roof_y + 1, z, STONE)
        _set(v, x, roof_y + 2, z, SLAB)
      elif on_edge:
        _set(v, x, roof_y + 1, z, FENCE)

  # Central lookout tower on roof
  cx, cz = ox + keep // 2 - 2, oz + keep // 2 - 2
  for y in range(3):
    for x in range(cx, cx + 4):
      for z in range(cz, cz + 4):
        edge = x in (cx, cx + 3) or z in (cz, cz + 3)
        if edge:
          _set(v, x, roof_y + 1 + y, z, STONE)
  for x in range(cx, cx + 4):
    for z in range(cz, cz + 4):
      if (x + z) % 2 == 0 and (x in (cx, cx + 3) or z in (cz, cz + 3)):
        _set(v, x, roof_y + 4, z, SLAB)

  # Torches on battlements
  for x in range(ox, ox + keep, 3):
    _set(v, x, roof_y + 3, oz, TORCH)
    _set(v, x, roof_y + 3, oz + keep - 1, TORCH)

  return v


def _generate_fortress_throne_room() -> np.ndarray:
  """
  Throne Room — book dimensions (scaled for 32³):
    11x12 hall, 5 blocks tall, raised plinth, spruce throne,
    balcony, red carpet runner, chiseled stone accents.
  """
  STONE = _b("stone_bricks")
  CHISELED = _b("chiseled_stone_bricks")
  CRACKED = _b("cracked_stone_bricks")
  RAW = _b("stone")
  STAIRS = _b("stone_brick_stairs")
  SLAB = _b("stone_brick_slab")
  S_STAIRS = _b("spruce_stairs")
  S_SLAB = _b("spruce_slab")
  FENCE = _b("spruce_fence")
  DOOR = _b("spruce_door")
  PLANKS = _b("spruce_planks")
  RED = _b("red_carpet")
  TERRA = _b("red_terracotta")
  GLASS = _b("glass_pane")
  RED_GLASS = _b("red_stained_glass_pane")
  SKULL = _b("skeleton_skull")
  PAINT = _b("painting")
  TORCH = _b("torch")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 10, 2
  rw, rd, rh = 11, 12, 5

  def wall_block(x: int, z: int, y: int) -> str:
    if (x + z) % 5 == 0:
      return CHISELED
    if (x + z + y) % 7 == 0:
      return CRACKED
    return STONE

  # Floor — stone with red carpet runner and terracotta accents near throne
  for x in range(ox + 1, ox + rw - 1):
    for z in range(oz + 1, oz + rd - 1):
      _set(v, x, oy, z, RAW)
  for z in range(oz + 2, oz + rd - 2):
    _set(v, ox + rw // 2, oy, z, RED)
  for x in range(ox + 3, ox + 8):
    for z in range(oz + rd - 5, oz + rd - 2):
      _set(v, x, oy, z, TERRA)

  # Walls
  for y in range(1, rh):
    for x in range(ox, ox + rw):
      for z in range(oz, oz + rd):
        edge = x in (ox, ox + rw - 1) or z in (oz, oz + rd - 1)
        if edge:
          _set(v, x, oy + y, z, wall_block(x, z, y))

  # Ceiling
  for x in range(ox, ox + rw):
    for z in range(oz, oz + rd):
      _set(v, x, oy + rh, z, STONE)

  # Windows
  for z in (oz + 3, oz + rd - 4):
    _set(v, ox, oy + 2, z, GLASS)
    _set(v, ox + rw - 1, oy + 2, z, RED_GLASS)
  for x in (ox + 3, ox + rw - 4):
    _set(v, x, oy + 2, oz, GLASS)
    _set(v, x, oy + 3, oz + rd - 1, RED_GLASS)

  # Entrance doors (south)
  _set(v, ox + 3, oy + 1, oz, DOOR)
  _set(v, ox + 3, oy + 2, oz, DOOR)
  _set(v, ox + 6, oy + 1, oz, DOOR)
  _set(v, ox + 6, oy + 2, oz, DOOR)
  _set(v, ox + 4, oy + 2, oz + 1, PAINT)

  # Raised throne plinth at north end
  plinth_z0 = oz + rd - 4
  for step in range(2):
    for x in range(ox + 3, ox + 8):
      for z in range(plinth_z0 + step, plinth_z0 + 2):
        _set(v, x, oy + 1 + step, z, STAIRS if step == 0 else SLAB)
        if step == 1:
          _set(v, x - 1, oy + 1, z, STAIRS)
          _set(v, x + 1, oy + 1, z, STAIRS)

  # Spruce throne on plinth
  tx, tz = ox + 5, oz + rd - 3
  _set(v, tx, oy + 3, tz, S_STAIRS)
  _set(v, tx, oy + 4, tz, S_SLAB)
  _set(v, tx, oy + 5, tz - 1, SKULL)
  _set(v, tx - 1, oy + 5, tz - 1, SKULL)

  # Balcony on west wall
  bal_x = ox + 1
  for z in range(oz + 4, oz + 8):
    _set(v, bal_x, oy + 3, z, PLANKS)
    _set(v, bal_x, oy + 4, z, FENCE)
  _set(v, bal_x, oy + 1, oz + 5, DOOR)
  _set(v, bal_x, oy + 2, oz + 5, DOOR)

  # Torch sconces on spruce fence posts
  for z in (oz + 2, oz + rd - 3):
    _set(v, ox + rw - 2, oy + 1, z, FENCE)
    _set(v, ox + rw - 2, oy + 2, z, TORCH)
  _set(v, ox + 2, oy + 1, oz + rd - 6, FENCE)
  _set(v, ox + 2, oy + 2, oz + rd - 6, TORCH)

  # Side railings along raised walkway
  for z in range(oz + 3, oz + rd - 3):
    _set(v, ox + 2, oy + 2, z, FENCE)
    _set(v, ox + rw - 3, oy + 2, z, FENCE)

  return v


def _generate_fortress_barracks() -> np.ndarray:
  """
  Barracks — book dimensions (scaled for 32³):
    10x8 two-story building, sand training courtyard, spruce roof,
    diorite upper walls, loft beds, hay lean-to.
  """
  COBBLE = _b("cobblestone")
  STONE = _b("stone_bricks")
  DIORITE = _b("diorite")
  LOG = _b("dark_oak_log")
  D_STAIRS = _b("dark_oak_stairs")
  D_FENCE = _b("dark_oak_fence")
  DOOR = _b("dark_oak_door")
  PLANKS = _b("spruce_planks")
  S_STAIRS = _b("spruce_stairs")
  S_FENCE = _b("spruce_fence")
  SAND = _b("sand")
  GLASS = _b("glass_pane")
  LADDER = _b("ladder")
  BED = _b("red_bed")
  CHEST = _b("chest")
  TORCH = _b("torch")
  LAMP = _b("redstone_lamp")
  HAY = _b("hay_block")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  bx, bz, oy = 11, 14, 1
  bw, bd, gh = 10, 8, 4  # ground floor height

  # Grass base
  for x in range(bx - 3, bx + bw + 6):
    for z in range(bz - 6, bz + bd + 2):
      _set(v, x, oy - 1, z, GRASS)

  # Training courtyard (south of building)
  cy0, cx0 = bz - 5, bx + 2
  cw, cd = 6, 5
  for x in range(cx0, cx0 + cw):
    for z in range(cy0, cy0 + cd):
      _set(v, x, oy, z, SAND)
  for x in range(cx0 - 1, cx0 + cw + 1):
    for z in range(cy0 - 1, cy0 + cd + 1):
      if x in (cx0 - 1, cx0 + cw) or z in (cy0 - 1, cy0 + cd):
        _set(v, x, oy + 1, z, D_FENCE)
  _set(v, cx0 + 3, oy + 1, cy0 + 2, LAMP)

  # Cobblestone foundation
  for x in range(bx, bx + bw):
    for z in range(bz, bz + bd):
      _set(v, x, oy, z, COBBLE)

  # Ground floor walls (stone brick)
  for y in range(1, gh):
    for x in range(bx, bx + bw):
      for z in range(bz, bz + bd):
        edge = x in (bx, bx + bw - 1) or z in (bz, bz + bd - 1)
        if edge:
          _set(v, x, oy + y, z, STONE)
        else:
          _set(v, x, oy + y, z, AIR_B)

  # Ground floor interior — spruce planks, chests, crafting feel
  for x in range(bx + 1, bx + bw - 1):
    for z in range(bz + 1, bz + bd - 1):
      _set(v, x, oy, z, PLANKS)
  _set(v, bx + 2, oy + 1, bz + 2, CHEST)
  _set(v, bx + 3, oy + 1, bz + 2, CHEST)
  _set(v, bx + 6, oy + 1, bz + 5, TORCH)

  # Door and window
  _set(v, bx + 4, oy + 1, bz, DOOR)
  _set(v, bx + 4, oy + 2, bz, DOOR)
  _set(v, bx + 7, oy + 2, bz + 3, GLASS)

  # Upper floor (diorite + dark oak timber frame, overhangs 1 block)
  upper_y = oy + gh
  for y in range(3):
    for x in range(bx - 1, bx + bw + 1):
      for z in range(bz - 1, bz + bd + 1):
        edge = x in (bx - 1, bx + bw) or z in (bz - 1, bz + bd)
        corner = (x in (bx - 1, bx + bw) and z in (bz - 1, bz + bd))
        if corner:
          _set(v, x, upper_y + y, z, LOG)
        elif edge:
          _set(v, x, upper_y + y, z, DIORITE if y < 2 else PLANKS)
        elif y == 0 and bx <= x < bx + bw and bz <= z < bz + bd:
          _set(v, x, upper_y, z, PLANKS)

  # Loft beds
  for bx_pos in range(bx + 2, bx + 7, 2):
    _set(v, bx_pos, upper_y + 1, bz + 2, BED)
    _set(v, bx_pos, upper_y + 1, bz + 3, CHEST)

  # Ladder to loft
  for y in range(1, 4):
    _set(v, bx + 1, oy + y, bz + 6, LADDER)

  # Roof balcony (center top)
  roof_y = upper_y + 3
  bal_x, bal_z = bx + 4, bz + 3
  for x in range(bal_x, bal_x + 3):
    for z in range(bal_z, bal_z + 3):
      _set(v, x, roof_y, z, PLANKS)
      if x in (bal_x, bal_x + 2) or z in (bal_z, bal_z + 2):
        _set(v, x, roof_y + 1, z, D_FENCE)
  _set(v, bal_x + 1, roof_y + 1, bal_z + 1, TORCH)
  _set(v, bal_x + 2, roof_y, bal_z + 1, CHEST)

  # Spruce stair peaked roof
  for layer in range(3):
    for x in range(bx + layer - 1, bx + bw - layer + 1):
      for z in range(bz + layer - 1, bz + bd - layer + 1):
        if bx + layer - 1 <= x < bx + bw - layer + 1 and bz + layer - 1 <= z < bz + bd - layer + 1:
          _set(v, x, roof_y + 1 + layer, z, S_STAIRS)

  # Hay lean-to on east side
  for x in range(bx + bw, bx + bw + 3):
    for z in range(bz + 2, bz + 6):
      _set(v, x, oy, z, COBBLE)
      _set(v, x, oy + 1, z, HAY)
    for z in range(bz + 1, bz + 7):
      _set(v, x, oy + 2, z, S_STAIRS)

  return v


def _generate_fortress_enchanting_room() -> np.ndarray:
  """
  Enchanting Room — book dimensions (scaled for 32³):
    10x9 hall, 5x5 nether brick enchant platform, bookshelf U-shape,
    L-shaped spruce balcony, brewing station, red nether brick accents.
  """
  STONE = _b("stone_bricks")
  NETHER = _b("nether_bricks")
  N_SLAB = _b("nether_brick_slab")
  RED_NETHER = _b("red_nether_bricks")
  PLANKS = _b("spruce_planks")
  DARK = _b("dark_oak_planks")
  FENCE = _b("spruce_fence")
  SLAB = _b("spruce_slab")
  BOOKS = _b("bookshelf")
  TABLE = _b("enchanting_table")
  BREW = _b("brewing_stand")
  CAULDRON = _b("cauldron")
  CHEST = _b("chest")
  GLASS = _b("glass_pane")
  LADDER = _b("ladder")
  PAINT = _b("painting")
  TORCH = _b("torch")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 11, 11, 2
  rw, rd, rh = 10, 9, 6

  # Floor — stone with nether brick border
  for x in range(ox + 1, ox + rw - 1):
    for z in range(oz + 1, oz + rd - 1):
      edge = x in (ox + 1, ox + rw - 2) or z in (oz + 1, oz + rd - 2)
      _set(v, x, oy, z, NETHER if edge else STONE)

  # Walls
  for y in range(1, rh):
    for x in range(ox, ox + rw):
      for z in range(oz, oz + rd):
        edge = x in (ox, ox + rw - 1) or z in (oz, oz + rd - 1)
        if not edge:
          continue
        # Red nether brick stripes mid-wall
        if y in (2, 3) and (x + z) % 3 == 0:
          _set(v, x, oy + y, z, RED_NETHER)
        elif (x + z) % 4 == 0 and y < rh - 1:
          _set(v, x, oy + y, z, DARK)
        else:
          _set(v, x, oy + y, z, STONE if y == 0 or y == rh - 1 else PLANKS)

  # Ceiling beams
  for x in range(ox, ox + rw):
    for z in range(oz, oz + rd):
      _set(v, x, oy + rh, z, STONE)
  for x in range(ox + 1, ox + rw - 1, 3):
    _set(v, x, oy + rh, oz + rd // 2, SLAB)

  # Windows
  for z in (oz + 2, oz + rd - 3):
    _set(v, ox, oy + 2, z, GLASS)
    _set(v, ox + rw - 1, oy + 2, z, GLASS)

  # 5x5 enchantment platform (center-north)
  px0, pz0 = ox + 3, oz + 2
  for x in range(px0, px0 + 5):
    for z in range(pz0, pz0 + 5):
      _set(v, x, oy, z, NETHER)
  # Enchanting table center
  _set(v, px0 + 2, oy + 1, pz0 + 2, TABLE)
  # Bookshelf U-shape (2 high on three sides)
  for x in range(px0, px0 + 5):
    for z in (pz0, pz0 + 4):
      if not (x == px0 + 2 and z == pz0 + 2):
        _set(v, x, oy + 1, z, BOOKS)
        _set(v, x, oy + 2, z, BOOKS)
  for z in range(pz0 + 1, pz0 + 4):
    _set(v, px0, oy + 1, z, BOOKS)
    _set(v, px0, oy + 2, z, BOOKS)
    _set(v, px0 + 4, oy + 1, z, BOOKS)
    _set(v, px0 + 4, oy + 2, z, BOOKS)

  # Brewing station (east wall)
  _set(v, ox + rw - 3, oy + 1, oz + 5, PLANKS)
  _set(v, ox + rw - 2, oy + 1, oz + 5, BREW)
  _set(v, ox + rw - 2, oy + 1, oz + 6, CAULDRON)
  _set(v, ox + rw - 3, oy + 1, oz + 7, CHEST)
  _set(v, ox + rw - 3, oy + 1, oz + 6, CHEST)

  # Paintings and torches
  _set(v, ox + 1, oy + 2, oz + 5, PAINT)
  _set(v, ox + 1, oy + 2, oz + 7, PAINT)
  _set(v, ox + 2, oy + 2, oz + 1, TORCH)
  _set(v, ox + rw - 2, oy + 2, oz + 1, TORCH)

  # L-shaped upper balcony
  bal_y = oy + 4
  for x in range(ox + 1, ox + 7):
    _set(v, x, bal_y, oz + rd - 2, PLANKS)
    _set(v, x, bal_y + 1, oz + rd - 2, FENCE)
    _set(v, x, bal_y + 2, oz + rd - 2, TORCH)
  for z in range(oz + 1, oz + 5):
    _set(v, ox + 1, bal_y, z, PLANKS)
    _set(v, ox + 1, bal_y + 1, z, FENCE)

  # Ladder to balcony
  for y in range(1, 3):
    _set(v, ox + rw - 2, oy + y, oz + rd - 3, LADDER)

  return v


def _dungeon_stone(x: int, z: int, y: int) -> str:
  COBBLE = _b("cobblestone")
  MOSSY_C = _b("mossy_cobblestone")
  STONE = _b("stone_bricks")
  MOSSY_S = _b("mossy_stone_bricks")
  ANDESITE = _b("andesite")
  r = (x + z + y) % 9
  if r == 0:
    return ANDESITE
  if r in (2, 6):
    return MOSSY_C
  if r in (4, 8):
    return MOSSY_S
  if r == 3:
    return STONE
  return COBBLE


def _generate_fortress_dungeon() -> np.ndarray:
  """
  Dungeon — book dimensions (scaled for 32³):
    12x11 underground prison, iron bar cells, guard station,
    stone brick stairs, ladder to lower level.
  """
  COBBLE = _b("cobblestone")
  MOSSY_C = _b("mossy_cobblestone")
  STONE = _b("stone_bricks")
  MOSSY_S = _b("mossy_stone_bricks")
  SMOOTH = _b("smooth_stone")
  BARS = _b("iron_bars")
  I_DOOR = _b("iron_door")
  FENCE = _b("spruce_fence")
  GATE = _b("spruce_fence_gate")
  TRAP = _b("spruce_trapdoor")
  LADDER = _b("ladder")
  CHEST = _b("chest")
  BED = _b("red_bed")
  CAULDRON = _b("cauldron")
  TORCH = _b("torch")
  DUST = _b("redstone_dust")
  STAIRS = _b("stone_brick_stairs")
  RAW = _b("stone")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 10, 10, 1
  dw, dd, dh = 12, 11, 5

  # Outer shell and floor
  for y in range(dh):
    for x in range(ox, ox + dw):
      for z in range(oz, oz + dd):
        edge = x in (ox, ox + dw - 1) or z in (oz, oz + dd - 1)
        if edge:
          _set(v, x, oy + y, z, _dungeon_stone(x, z, y))
        elif y == 0:
          _set(v, x, oy, z, SMOOTH if (x + z) % 2 else COBBLE)
        else:
          _set(v, x, oy + y, z, AIR_B)

  # Ceiling
  for x in range(ox, ox + dw):
    for z in range(oz, oz + dd):
      _set(v, x, oy + dh, z, STONE)

  # Arrow slit windows high on walls
  for x in (ox + 3, ox + 8):
    _set(v, x, oy + 3, oz, BARS)
    _set(v, x, oy + 3, oz + dd - 1, BARS)

  # Cell 1 (west side)
  cx1, cz1 = ox + 1, oz + 2
  cw, cd, ch = 4, 5, 4
  for y in range(1, ch):
    for x in range(cx1, cx1 + cw):
      _set(v, x, oy + y, cz1 + cd - 1, BARS)  # iron bar front
  _set(v, cx1 + 1, oy + 1, cz1 + cd - 1, I_DOOR)
  _set(v, cx1 + 1, oy + 2, cz1 + cd - 1, I_DOOR)
  _set(v, cx1 + 1, oy + 1, cz1 + 1, BED)
  _set(v, cx1 + 2, oy + 1, cz1 + 1, BED)
  _set(v, cx1 + 3, oy + 1, cz1 + 3, CAULDRON)
  _set(v, cx1 + 2, oy + 1, cz1 + 2, DUST)
  _set(v, cx1 + 3, oy + 2, cz1 + 2, TORCH)

  # Cell 2 (east side)
  cx2 = ox + dw - 5
  for y in range(1, ch):
    for x in range(cx2, cx2 + cw):
      _set(v, x, oy + y, cz1 + cd - 1, BARS)
  _set(v, cx2 + 2, oy + 1, cz1 + cd - 1, I_DOOR)
  _set(v, cx2 + 2, oy + 2, cz1 + cd - 1, I_DOOR)
  _set(v, cx2 + 1, oy + 1, cz1 + 2, BED)
  _set(v, cx2 + 2, oy + 1, cz1 + 3, DUST)

  # Guard station (center corridor)
  gx, gz = ox + 5, oz + 5
  _set(v, gx, oy + 1, gz, FENCE)
  _set(v, gx + 1, oy + 1, gz, GATE)
  _set(v, gx + 2, oy + 1, gz, FENCE)
  _set(v, gx + 3, oy + 1, gz + 1, CHEST)
  _set(v, gx, oy + 3, gz + 2, TORCH)

  # Stone brick stairs to upper landing
  for step in range(3):
    _set(v, ox + dw - 3, oy + 1 + step, oz + 8 + step, STAIRS)
  _set(v, ox + dw - 4, oy + 2, oz + 9, FENCE)

  # Ladder hole to lower level
  hole_x, hole_z = ox + 3, oz + 8
  _set(v, hole_x, oy, hole_z, TRAP)
  for y in range(-3, 0):
    _set(v, hole_x, oy + y, hole_z, LADDER)
    for dx in (-1, 0, 1):
      for dz in (-1, 0, 1):
        _set(v, hole_x + dx, oy + y, hole_z + dz, RAW if (dx + dz) % 2 else COBBLE)

  return v


def _generate_fortress_village_house() -> np.ndarray:
  """
  Village House — book dimensions (scaled for 32³):
    10x8 cobblestone base, timber-framed upper floor, dark oak roof,
    furnished ground floor kitchen and upper bedroom, garden and balcony.
  """
  COBBLE = _b("cobblestone")
  C_STAIRS = _b("cobblestone_stairs")
  LOG = _b("dark_oak_log")
  D_PLANKS = _b("dark_oak_planks")
  D_STAIRS = _b("dark_oak_stairs")
  D_SLAB = _b("dark_oak_slab")
  D_FENCE = _b("dark_oak_fence")
  O_PLANKS = _b("oak_planks")
  TRAP = _b("oak_trapdoor")
  DOOR = _b("oak_door")
  GLASS = _b("glass_pane")
  S_FENCE = _b("spruce_fence")
  RED = _b("red_carpet")
  BLUE = _b("blue_carpet")
  BED = _b("red_bed")
  FURNACE = _b("furnace")
  SMOKER = _b("smoker")
  CHEST = _b("chest")
  CRAFT = _b("crafting_table")
  PAINT = _b("painting")
  TORCH = _b("torch")
  GRAVEL = _b("gravel")
  GRASS = _b("grass_block")
  POPPY = _b("poppy")
  DAISY = _b("oxeye_daisy")
  WHEAT = _b("wheat")
  CARROT = _b("carrots")
  COMPOST = _b("composter")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  bx, bz, oy = 11, 12, 1
  bw, bd = 10, 8
  gh, uh = 4, 5  # ground and upper floor heights

  # Landscaping
  for x in range(bx - 2, bx + bw + 4):
    for z in range(bz - 4, bz + bd + 3):
      _set(v, x, oy - 1, z, GRASS)
  # Gravel path to door
  for z in range(bz - 3, bz):
    _set(v, bx + 4, oy - 1, z, GRAVEL)
    _set(v, bx + 5, oy - 1, z, GRAVEL)

  # Ground floor shell — cobblestone with log corners
  for y in range(gh):
    for x in range(bx, bx + bw):
      for z in range(bz, bz + bd):
        corner = x in (bx, bx + bw - 1) and z in (bz, bz + bd - 1)
        edge = x in (bx, bx + bw - 1) or z in (bz, bz + bd - 1)
        if corner:
          _set(v, x, oy + y, z, LOG)
        elif edge:
          _set(v, x, oy + y, z, COBBLE)
        elif y == 0:
          _set(v, x, oy, z, O_PLANKS)
        else:
          _set(v, x, oy + y, z, AIR_B)

  # Ground floor interior
  for x in range(bx + 2, bx + 7):
    for z in range(bz + 2, bz + 6):
      _set(v, x, oy, z, RED)
  # Kitchen alcove (north wall)
  _set(v, bx + 2, oy + 1, bz + 1, FURNACE)
  _set(v, bx + 3, oy + 1, bz + 1, SMOKER)
  _set(v, bx + 4, oy + 1, bz + 1, CHEST)
  _set(v, bx + 7, oy + 1, bz + 5, CRAFT)
  _set(v, bx + 2, oy + 2, bz + 4, PAINT)
  _set(v, bx + 7, oy + 2, bz + 3, PAINT)
  _set(v, bx + 6, oy + 2, bz + 1, TORCH)

  # Door and fenestral windows (slits)
  _set(v, bx + 4, oy + 1, bz, DOOR)
  _set(v, bx + 4, oy + 2, bz, DOOR)
  _set(v, bx + 1, oy + 2, bz + 3, AIR_B)  # fenestral slit
  _set(v, bx + 1, oy + 3, bz + 3, AIR_B)
  _set(v, bx + bw - 2, oy + 2, bz + 5, GLASS)

  # Stairs to upper floor
  for step in range(4):
    _set(v, bx + 1, oy + 1 + step, bz + bd - 2 - step, D_STAIRS)

  # Upper floor — timber frame (logs corners, oak plank infill, overhangs 1)
  uy = oy + gh
  for y in range(uh):
    for x in range(bx - 1, bx + bw + 1):
      for z in range(bz - 1, bz + bd + 1):
        corner = x in (bx - 1, bx + bw) and z in (bz - 1, bz + bd)
        edge = x in (bx - 1, bx + bw) or z in (bz - 1, bz + bd)
        if corner:
          _set(v, x, uy + y, z, LOG)
        elif edge and y < uh - 1:
          _set(v, x, uy + y, z, O_PLANKS)
        elif y == 0 and bx <= x < bx + bw and bz <= z < bz + bd:
          _set(v, x, uy, z, O_PLANKS)

  # Upper floor interior — bedroom
  _set(v, bx + 3, uy + 1, bz + 2, BED)
  for x in range(bx + 4, bx + 7):
    for z in range(bz + 3, bz + 6):
      _set(v, x, uy, z, BLUE)
  _set(v, bx + 6, uy + 1, bz + 5, CHEST)
  _set(v, bx + 2, uy + 2, bz + 4, PAINT)
  _set(v, bx + 7, uy + 2, bz + 3, PAINT)
  # Stair opening railing
  for x in range(bx, bx + 3):
    _set(v, x, uy + 1, bz + bd - 3, S_FENCE)

  # Upper windows
  for x in (bx + 2, bx + 6):
    _set(v, x, uy + 2, bz - 1, GLASS)
    _set(v, x, uy + 3, bz - 1, GLASS)

  # Side balcony
  bal_z = bz + bd
  for x in range(bx + 2, bx + 6):
    _set(v, x, uy + 1, bal_z, D_SLAB)
    _set(v, x, uy + 2, bal_z, D_FENCE)
  _set(v, bx + 4, uy + 2, bal_z, TORCH)

  # Gabled roof with overhang
  roof_base = uy + uh
  for layer in range(4):
    for x in range(bx - 1 + layer, bx + bw + 1 - layer):
      for z in range(bz - 1 + layer, bz + bd + 1 - layer):
        _set(v, x, roof_base + layer, z, D_STAIRS)

  # Flower planters (trapdoor raised beds)
  for fx, fz, flower in ((bx - 1, bz + 1, POPPY), (bx + bw, bz + 2, DAISY), (bx + 2, bz - 2, POPPY)):
    _set(v, fx, oy, fz, GRASS)
    _set(v, fx, oy + 1, fz, flower)
    _set(v, fx, oy + 1, fz + 1, TRAP)

  # Vegetable garden (east side)
  for x in range(bx + bw + 1, bx + bw + 4):
    for z in range(bz + 1, bz + 5):
      _set(v, x, oy, z, WHEAT if z % 2 == 0 else CARROT)
      if x == bx + bw + 1 or z in (bz + 1, bz + 4):
        _set(v, x, oy + 1, z, D_FENCE)
  _set(v, bx + bw + 2, oy + 1, bz + 5, COMPOST)

  # Entrance step
  _set(v, bx + 4, oy, bz - 1, C_STAIRS)
  _set(v, bx + 5, oy, bz - 1, C_STAIRS)
  _set(v, bx + 3, oy + 2, bz, TORCH)

  return v


def _generate_fortress_market_square() -> np.ndarray:
  """
  Market Square — book dimensions (scaled for 32³):
    16x16 grass plaza, cobblestone cross paths, central well,
    four furnished stalls (blacksmith, grocer, bakery, alchemist).
  """
  GRASS = _b("grass_block")
  GRAVEL = _b("gravel")
  COBBLE = _b("cobblestone")
  S_BRICK = _b("stone_bricks")
  WATER = _b("water")
  D_LOG = _b("dark_oak_log")
  D_FENCE = _b("dark_oak_fence")
  D_PLANKS = _b("dark_oak_planks")
  D_SLAB = _b("dark_oak_slab")
  S_LOG = _b("spruce_log")
  S_PLANKS = _b("spruce_planks")
  S_STAIRS = _b("spruce_stairs")
  S_SLAB = _b("spruce_slab")
  WHITE = _b("white_wool")
  ORANGE = _b("orange_wool")
  BLUE = _b("blue_wool")
  W_CARPET = _b("white_carpet")
  B_CARPET = _b("black_carpet")
  BLAST = _b("blast_furnace")
  FURNACE = _b("furnace")
  CHEST = _b("chest")
  BREW = _b("brewing_stand")
  CAULDRON = _b("cauldron")
  CUTTER = _b("stonecutter")
  ANVIL = _b("anvil")
  CAKE = _b("cake")
  TORCH = _b("torch")
  POPPY = _b("poppy")
  DAISY = _b("oxeye_daisy")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 8, 8, 1
  sq = 16  # 16x16 square

  # Grass foundation
  for x in range(ox, ox + sq):
    for z in range(oz, oz + sq):
      _set(v, x, oy - 1, z, GRASS)

  # Cross paths — cobblestone with gravel accents
  cx, cz = ox + 8, oz + 8
  for z in range(oz, oz + sq):
    for x in (cx - 1, cx):
      _set(v, x, oy, z, COBBLE)
  for x in range(ox, ox + sq):
    for z in (cz - 1, cz):
      _set(v, x, oy, z, COBBLE)
  # Gravel corners on path intersections
  for dx, dz in ((-2, -2), (1, -2), (-2, 1), (1, 1)):
    _set(v, cx + dx, oy, cz + dz, GRAVEL)

  # Central well (stone brick ring, water, fence posts)
  for x in range(cx - 2, cx + 2):
    for z in range(cz - 2, cz + 2):
      edge = x in (cx - 2, cx + 1) or z in (cz - 2, cz + 1)
      if edge:
        _set(v, x, oy, z, S_BRICK)
        _set(v, x, oy + 1, z, S_BRICK)
      else:
        _set(v, x, oy, z, WATER)
  for x, z in ((cx - 2, cz - 2), (cx + 1, cz - 2), (cx - 2, cz + 1), (cx + 1, cz + 1)):
    _set(v, x, oy + 2, z, D_FENCE)
    _set(v, x, oy + 1, z, POPPY if x < cx else DAISY)

  # --- North stall: Grocer / general goods (faces south) ---
  gx0, gz0 = ox + 2, oz
  gw, gd = 12, 4
  for x in range(gx0, gx0 + gw):
    for z in range(gz0, gz0 + gd):
      corner = x in (gx0, gx0 + gw - 1) and z in (gz0, gz0 + gd - 1)
      back = z == gz0
      if corner:
        _set(v, x, oy + 1, z, S_LOG)
        _set(v, x, oy + 2, z, S_LOG)
        _set(v, x, oy + 3, z, S_LOG)
        _set(v, x, oy + 4, z, S_LOG)
      elif back:
        _set(v, x, oy + 1, z, COBBLE)
        _set(v, x, oy + 2, z, S_PLANKS)
        _set(v, x, oy + 3, z, S_PLANKS)
      elif z == gz0 + gd - 1:
        _set(v, x, oy + 1, z, S_STAIRS)  # front counter
        _set(v, x, oy + 2, z, B_CARPET)
  # Interior — chest wall (6 chests in 2 rows)
  for i, (cx2, cz2) in enumerate(
    ((gx0 + 2, gz0 + 1), (gx0 + 4, gz0 + 1), (gx0 + 6, gz0 + 1),
     (gx0 + 2, gz0 + 2), (gx0 + 4, gz0 + 2), (gx0 + 6, gz0 + 2))
  ):
    _set(v, cx2, oy + 1, cz2, CHEST)
    _set(v, cx2, oy, cz2, S_PLANKS)
  _set(v, gx0 + 1, oy + 3, gz0 + 2, TORCH)
  _set(v, gx0 + gw - 2, oy + 3, gz0 + 2, TORCH)
  # Blue/white checkered canopy roof
  for x in range(gx0 - 1, gx0 + gw + 1):
    for z in range(gz0 - 1, gz0 + gd):
      _set(v, x, oy + 5, z, BLUE if (x + z) % 2 == 0 else WHITE)

  # --- South stall: Blacksmith (faces north) ---
  bx0, bz0 = ox + 2, oz + sq - 4
  for x in range(bx0, bx0 + gw):
    for z in range(bz0, bz0 + gd):
      corner = x in (bx0, bx0 + gw - 1) and z in (bz0, bz0 + gd - 1)
      back = z == bz0 + gd - 1
      if corner:
        _set(v, x, oy + 1, z, D_LOG)
        _set(v, x, oy + 2, z, D_LOG)
        _set(v, x, oy + 3, z, D_LOG)
      elif back:
        _set(v, x, oy + 1, z, COBBLE)
      elif z == bz0:
        _set(v, x, oy + 1, z, WHITE)  # white counter
  # Interior
  _set(v, bx0 + 3, oy + 1, bz0 + 3, BLAST)
  _set(v, bx0 + 4, oy + 1, bz0 + 3, BLAST)
  _set(v, bx0 + 5, oy + 1, bz0 + 3, CHEST)
  _set(v, bx0 + 6, oy + 1, bz0 + 3, CHEST)
  _set(v, bx0 + 1, oy + 2, bz0 + 2, TORCH)
  # Roof — dark oak slab with white/orange wool strip
  for x in range(bx0, bx0 + gw):
    _set(v, x, oy + 4, bz0, D_SLAB)
    _set(v, x, oy + 5, bz0 + 1, WHITE if x % 2 == 0 else ORANGE)

  # --- West stall: Bakery (faces east) ---
  by_x0, by_z0 = ox, oz + 2
  by_w, by_d = 4, 12
  for x in range(by_x0, by_x0 + by_w):
    for z in range(by_z0, by_z0 + by_d):
      if x == by_x0 or z in (by_z0, by_z0 + by_d - 1):
        _set(v, x, oy + 1, z, D_FENCE)
        if (x == by_x0 and z == by_z0) or (x == by_x0 and z == by_z0 + by_d - 1):
          _set(v, x, oy + 2, z, TORCH)
      elif x == by_x0 + by_w - 1:
        _set(v, x, oy + 1, z, W_CARPET)  # counter facing east
  # Interior — furnaces and cake display
  for fz in (by_z0 + 2, by_z0 + 5, by_z0 + 8):
    _set(v, by_x0 + 1, oy + 1, fz, FURNACE)
    _set(v, by_x0 + 1, oy, fz, S_PLANKS)
  _set(v, by_x0 + 1, oy + 1, by_z0 + 10, CHEST)
  _set(v, by_x0 + 2, oy + 1, by_z0 + 6, S_SLAB)
  _set(v, by_x0 + 2, oy + 2, by_z0 + 6, CAKE)

  # --- East stall: Alchemist (faces west) ---
  ax0, az0 = ox + sq - 4, oz + 2
  for x in range(ax0, ax0 + by_w):
    for z in range(az0, az0 + by_d):
      if x == ax0 + by_w - 1 or z in (az0, az0 + by_d - 1):
        _set(v, x, oy + 1, z, D_FENCE)
        if x == ax0 + by_w - 1 and z == az0:
          _set(v, x, oy + 2, z, TORCH)
      elif x == ax0:
        _set(v, x, oy + 1, z, D_PLANKS)  # counter
  # Interior
  _set(v, ax0 + 2, oy + 1, az0 + 4, BREW)
  _set(v, ax0 + 2, oy + 1, az0 + 6, CAULDRON)
  _set(v, ax0 + 2, oy + 1, az0 + 8, CUTTER)
  _set(v, ax0 + 2, oy + 1, az0 + 10, ANVIL)

  # Corner flowers between stalls
  for fx, fz, flower in (
    (ox + 1, oz + 1, POPPY),
    (ox + sq - 2, oz + 1, DAISY),
    (ox + 1, oz + sq - 2, DAISY),
    (ox + sq - 2, oz + sq - 2, POPPY),
  ):
    _set(v, fx, oy, fz, flower)

  # Perimeter torch posts at path ends
  for tx, tz in ((cx, oz), (cx, oz + sq - 1), (ox, cz), (ox + sq - 1, cz)):
    _set(v, tx, oy + 1, tz, D_FENCE)
    _set(v, tx, oy + 2, tz, TORCH)

  return v


def _in_tavern_footprint(x: int, z: int, bx: int, bz: int) -> bool:
  """L-shaped tavern footprint: main 11x8 wing + 4x5 southeast extension."""
  in_main = bx <= x <= bx + 10 and bz <= z <= bz + 7
  in_wing = bx + 7 <= x <= bx + 10 and bz + 8 <= z <= bz + 12
  return in_main or in_wing


def _generate_fortress_travelers_tavern() -> np.ndarray:
  """
  Travelers' Tavern — book dimensions (scaled for 32³):
    L-shaped 11x8 + 4x5 wing, cobblestone ground floor tavern with bar,
    furnished upper bedroom, porch, chimneys, and gabled roof.
  """
  COBBLE = _b("cobblestone")
  S_BRICK = _b("stone_bricks")
  C_WALL = _b("cobblestone_wall")
  DIORITE = _b("diorite")
  S_LOG = _b("spruce_log")
  S_PLANKS = _b("spruce_planks")
  S_STAIRS = _b("spruce_stairs")
  D_STAIRS = _b("dark_oak_stairs")
  D_LOG = _b("dark_oak_log")
  GREEN = _b("green_terracotta")
  G_CARPET = _b("green_carpet")
  O_PLANKS = _b("oak_planks")
  TRAP = _b("oak_trapdoor")
  O_FENCE = _b("oak_fence")
  DOOR = _b("oak_door")
  GLASS = _b("glass_pane")
  PISTON = _b("piston")
  BED = _b("red_bed")
  CHEST = _b("chest")
  PAINT = _b("painting")
  FRAME = _b("item_frame")
  TORCH = _b("torch")
  FURNACE = _b("furnace")
  BARREL = _b("barrel")
  GRASS = _b("grass_block")
  POPPY = _b("poppy")
  ORCHID = _b("blue_orchid")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  bx, bz, oy = 10, 11, 1
  gh, uh = 4, 4  # ground and upper floor wall heights

  def footprint(x: int, z: int) -> bool:
    return _in_tavern_footprint(x, z, bx, bz)

  # Landscaping
  for x in range(bx - 2, bx + 14):
    for z in range(bz - 3, bz + 15):
      _set(v, x, oy - 1, z, GRASS)

  # Front walkway
  for x in range(bx, bx + 11):
    _set(v, x, oy - 1, bz - 2, S_BRICK)
    _set(v, x, oy - 1, bz - 1, COBBLE)

  # Raised porch
  for x in range(bx + 3, bx + 7):
    for z in range(bz - 1, bz):
      _set(v, x, oy, z, O_PLANKS)

  # Ground floor shell — cobblestone with log corners
  for y in range(gh):
    for x in range(bx - 1, bx + 12):
      for z in range(bz - 1, bz + 14):
        if not footprint(x, z):
          continue
        edge = not footprint(x - 1, z) or not footprint(x + 1, z) or not footprint(x, z - 1) or not footprint(x, z + 1)
        corner = footprint(x, z) and sum(
          footprint(x + dx, z + dz) for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1))
        ) <= 2
        if edge and corner:
          _set(v, x, oy + y, z, S_LOG)
        elif edge:
          _set(v, x, oy + y, z, COBBLE)
        elif y == 0:
          _set(v, x, oy, z, S_PLANKS)

  # Ground floor interior — L-shaped bar with green carpet
  # Bar along north and west walls of main wing
  for x in range(bx + 2, bx + 9):
    _set(v, x, oy + 1, bz + 2, S_PLANKS)
    _set(v, x, oy + 2, bz + 2, G_CARPET)
  for z in range(bz + 3, bz + 7):
    _set(v, bx + 2, oy + 1, z, S_PLANKS)
    _set(v, bx + 2, oy + 2, z, G_CARPET)
  _set(v, bx + 8, oy + 2, bz + 2, TRAP)  # bar gate
  # Piston stools
  _set(v, bx + 5, oy + 1, bz + 4, PISTON)
  _set(v, bx + 6, oy + 1, bz + 4, PISTON)
  # Kitchen alcove (east wall)
  _set(v, bx + 9, oy + 1, bz + 4, FURNACE)
  _set(v, bx + 9, oy + 1, bz + 5, BARREL)
  _set(v, bx + 9, oy + 1, bz + 6, BARREL)
  # Torches
  _set(v, bx + 4, oy + 2, bz + 6, TORCH)
  _set(v, bx + 8, oy + 2, bz + 6, TORCH)

  # Stairs to upper floor (southwest corner)
  for step in range(4):
    _set(v, bx + 1, oy + 1 + step, bz + 6 - step, D_STAIRS)

  # Door and windows
  _set(v, bx + 5, oy + 1, bz - 1, DOOR)
  _set(v, bx + 5, oy + 2, bz - 1, DOOR)
  _set(v, bx + 3, oy + 2, bz - 1, GLASS)
  _set(v, bx + 7, oy + 2, bz - 1, GLASS)
  _set(v, bx - 1, oy + 2, bz + 4, GLASS)
  _set(v, bx + 3, oy + 3, bz - 1, TRAP)  # shutter
  _set(v, bx + 7, oy + 3, bz - 1, TRAP)

  # Upper floor — wattle and daub (diorite + green terracotta, log frame, overhangs 1)
  uy = oy + gh

  def upper_footprint(x: int, z: int) -> bool:
    return _in_tavern_footprint(x, z, bx - 1, bz - 1)

  for y in range(uh):
    for x in range(bx - 1, bx + 12):
      for z in range(bz - 1, bz + 14):
        if not upper_footprint(x, z):
          continue
        edge = (
          not upper_footprint(x - 1, z)
          or not upper_footprint(x + 1, z)
          or not upper_footprint(x, z - 1)
          or not upper_footprint(x, z + 1)
        )
        corner = upper_footprint(x, z) and sum(
          upper_footprint(x + dx, z + dz) for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1))
        ) <= 2
        if corner and edge:
          _set(v, x, uy + y, z, D_LOG)
        elif edge and y < uh - 1:
          fill = GREEN if y >= 2 else DIORITE
          _set(v, x, uy + y, z, fill)
        elif y == 0 and footprint(x, z):
          _set(v, x, uy, z, S_PLANKS)

  # Upper floor interior — bedroom
  _set(v, bx + 4, uy + 1, bz + 3, BED)
  _set(v, bx + 6, uy + 1, bz + 4, CHEST)
  _set(v, bx + 4, uy + 2, bz + 3, PAINT)
  _set(v, bx + 3, uy + 1, bz + 5, TORCH)

  # Upper windows
  _set(v, bx + 5, uy + 2, bz - 1, GLASS)
  _set(v, bx + 5, uy + 3, bz - 1, GLASS)
  _set(v, bx + 10, uy + 2, bz + 10, GLASS)

  # Gabled roof
  roof_base = uy + uh
  for layer in range(4):
    for x in range(bx - 1 + layer, bx + 11 - layer):
      for z in range(bz - 1 + layer, bz + 13 - layer):
        if upper_footprint(x, z):
          _set(v, x, roof_base + layer, z, S_STAIRS if layer % 2 == 0 else D_STAIRS)

  # Chimneys
  for cy in range(roof_base, roof_base + 3):
    _set(v, bx + 3, cy, bz + 2, C_WALL)
    _set(v, bx + 8, cy, bz + 9, C_WALL)

  # Flower boxes under front windows
  for fx, flower in ((bx + 3, POPPY), (bx + 7, ORCHID)):
    _set(v, fx, oy, bz - 1, GRASS)
    _set(v, fx, oy + 1, bz - 1, flower)
    _set(v, fx - 1, oy + 1, bz - 1, TRAP)
    _set(v, fx + 1, oy + 1, bz - 1, TRAP)

  # Side fenced garden
  for x in range(bx - 1, bx + 2):
    for z in range(bz + 9, bz + 12):
      _set(v, x, oy, z, GRASS)
      if x == bx - 1 or z == bz + 11:
        _set(v, x, oy + 1, z, O_FENCE)
  _set(v, bx, oy + 1, bz + 10, POPPY)

  # Tavern sign on fence post
  _set(v, bx - 1, oy + 1, bz - 1, O_FENCE)
  _set(v, bx - 1, oy + 2, bz - 1, FRAME)
  _set(v, bx + 2, oy + 2, bz - 1, TORCH)

  return v


def _generate_fortress_cathedral() -> np.ndarray:
  """
  Cathedral — book dimensions (scaled for 32³):
    12x15 stone nave, spruce plank aisle, dark oak pew rows, altar,
    buttressed walls, stained glass, bell tower with note block bells.
  """
  STONE = _b("stone_bricks")
  CHISELED = _b("chiseled_stone_bricks")
  CRACKED = _b("cracked_stone_bricks")
  COBBLE = _b("cobblestone")
  S_STAIRS = _b("stone_brick_stairs")
  S_SLAB = _b("stone_brick_slab")
  S_WALL = _b("stone_brick_wall")
  S_PLANKS = _b("spruce_planks")
  SP_STAIRS = _b("spruce_stairs")
  D_STAIRS = _b("dark_oak_stairs")
  Y_GLASS = _b("yellow_stained_glass")
  O_GLASS = _b("orange_stained_glass")
  BARS = _b("iron_bars")
  DOOR = _b("spruce_door")
  WOOL = _b("white_wool")
  TORCH = _b("torch")
  LANTERN = _b("lantern")
  LADDER = _b("ladder")
  NOTE = _b("note_block")
  REDSTONE = _b("redstone_wire")
  R_TORCH = _b("redstone_torch")
  REPEATER = _b("repeater")
  GRASS = _b("grass_block")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  bx, bz, oy = 8, 7, 1
  bw, bd = 12, 15  # nave width x depth
  wh = 6  # wall height

  # Grass foundation
  for x in range(bx - 2, bx + bw + 3):
    for z in range(bz - 2, bz + bd + 3):
      _set(v, x, oy - 1, z, GRASS)

  # Floor — stone with spruce plank center aisle
  for x in range(bx, bx + bw):
    for z in range(bz, bz + bd):
      aisle = bx + 4 <= x <= bx + 7
      _set(v, x, oy, z, S_PLANKS if aisle else STONE)

  # Nave walls
  for y in range(1, wh + 1):
    for x in range(bx, bx + bw):
      for z in range(bz, bz + bd):
        edge = x in (bx, bx + bw - 1) or z in (bz, bz + bd - 1)
        if not edge:
          continue
        # Mixed stone texture
        mat = CRACKED if (x + z + y) % 5 == 0 else STONE
        if y == wh and z not in (bz, bz + bd - 1):
          _set(v, x, oy + y, z, S_STAIRS)  # wall top trim
        else:
          _set(v, x, oy + y, z, mat)

  # Interior pillars (colonnade along aisle edges)
  for z in range(bz + 2, bz + bd - 2, 3):
    for px in (bx + 3, bx + 8):
      for y in range(1, wh):
        _set(v, px, oy + y, z, CHISELED)
      _set(v, px, oy + wh - 1, z, LANTERN)

  # Pew rows — dark oak stairs flanking aisle
  for z in range(bz + 2, bz + bd - 4, 2):
    for px in (bx + 1, bx + 2, bx + 9, bx + 10):
      _set(v, px, oy + 1, z, D_STAIRS)

  # Altar at north end
  for x in range(bx + 4, bx + 8):
    _set(v, x, oy + 1, bz + bd - 2, WOOL)
  _set(v, bx + 5, oy + 2, bz + bd - 2, TORCH)
  _set(v, bx + 6, oy + 2, bz + bd - 2, TORCH)

  # Entrance door (south)
  _set(v, bx + 5, oy + 1, bz, DOOR)
  _set(v, bx + 6, oy + 1, bz, DOOR)
  _set(v, bx + 5, oy + 2, bz, DOOR)
  _set(v, bx + 6, oy + 2, bz, DOOR)

  # Rose window above entrance
  for dx, dz in ((0, 0), (1, 0), (0, 1), (1, 1)):
    _set(v, bx + 4 + dx, oy + 4, bz, Y_GLASS)
    _set(v, bx + 6 + dx, oy + 4, bz, Y_GLASS)

  # Apse stained glass (north back wall)
  pattern = (
    (O_GLASS, Y_GLASS, O_GLASS),
    (Y_GLASS, Y_GLASS, Y_GLASS),
    (O_GLASS, Y_GLASS, O_GLASS),
  )
  for dz, row in enumerate(pattern):
    for dx, glass in enumerate(row):
      _set(v, bx + 4 + dx, oy + 3, bz + bd - 1 + dz, glass)
      _set(v, bx + 4 + dx, oy + 4, bz + bd - 1 + dz, glass)

  # Side windows (iron bars)
  for z in range(bz + 3, bz + bd - 3, 4):
    _set(v, bx, oy + 3, z, BARS)
    _set(v, bx, oy + 4, z, BARS)
    _set(v, bx + bw - 1, oy + 3, z, BARS)
    _set(v, bx + bw - 1, oy + 4, z, BARS)

  # Exterior buttresses
  for z in range(bz + 2, bz + bd - 2, 4):
    for side in (bx - 1, bx + bw):
      for y in range(1, wh + 1):
        _set(v, side, oy + y, z, COBBLE)
        _set(v, side, oy + y, z + 1, COBBLE)

  # Steep A-frame roof
  roof_base = oy + wh + 1
  for layer in range(5):
    for x in range(bx + layer, bx + bw - layer):
      for z in range(bz + layer, bz + bd - layer):
        _set(v, x, roof_base + layer, z, SP_STAIRS)

  # Roof edge stone trim and finials
  for x in range(bx, bx + bw):
    _set(v, x, roof_base, bz, S_SLAB)
    _set(v, x, roof_base, bz + bd - 1, S_SLAB)
  _set(v, bx + 5, roof_base + 5, bz, S_WALL)
  _set(v, bx + 6, roof_base + 5, bz, S_WALL)
  _set(v, bx + 5, roof_base + 5, bz + bd - 1, S_WALL)
  _set(v, bx + 6, roof_base + 5, bz + bd - 1, S_WALL)

  # Bell tower (southwest corner, 4x4)
  tx, tz = bx, bz - 3
  th = 10
  for y in range(th):
    for x in range(tx, tx + 4):
      for z in range(tz, tz + 4):
        edge = x in (tx, tx + 3) or z in (tz, tz + 3)
        if edge:
          _set(v, x, oy + y, z, STONE)
  # Tower floors and ladder
  for floor_y in (3, 6, 8):
    for x in range(tx + 1, tx + 3):
      for z in range(tz + 1, tz + 3):
        _set(v, x, oy + floor_y, z, S_PLANKS)
  for y in range(1, th - 1):
    _set(v, tx + 2, oy + y, tz + 1, LADDER)
  # Note block bells on top platform
  _set(v, tx + 1, oy + 9, tz + 1, NOTE)
  _set(v, tx + 2, oy + 9, tz + 1, NOTE)
  _set(v, tx + 1, oy + 9, tz + 2, NOTE)
  _set(v, tx + 2, oy + 9, tz + 2, NOTE)
  _set(v, tx + 1, oy + 8, tz + 2, REPEATER)
  _set(v, tx + 2, oy + 8, tz + 1, REDSTONE)
  _set(v, tx + 1, oy + 8, tz + 1, R_TORCH)
  # Crenellated crown
  for x in range(tx, tx + 4):
    for z in range(tz, tz + 4):
      if (x + z) % 2 == 0:
        _set(v, x, oy + th, z, S_SLAB)
  _set(v, tx + 1, oy + th - 2, tz + 2, TORCH)

  return v


def _generate_fortress_castle_bits() -> np.ndarray:
  """
  Castle Finishing Touches — eight small props arranged on a grass courtyard:
    beacon, flag, notice board, carts, storage hold, signpost, guard post, well.
  """
  GRASS = _b("grass_block")
  COBBLE = _b("cobblestone")
  STONE = _b("stone_bricks")
  S_STAIRS = _b("stone_brick_stairs")
  S_SLAB = _b("stone_brick_slab")
  CHISELED = _b("chiseled_stone_bricks")
  C_WALL = _b("cobblestone_wall")
  D_PLANKS = _b("dark_oak_planks")
  D_STAIRS = _b("dark_oak_stairs")
  D_SLAB = _b("dark_oak_slab")
  S_PLANKS = _b("spruce_planks")
  S_FENCE = _b("spruce_fence")
  S_TRAP = _b("spruce_trapdoor")
  S_SLAB_W = _b("spruce_slab")
  O_FENCE = _b("oak_fence")
  O_GATE = _b("oak_fence_gate")
  O_SIGN = _b("oak_sign")
  O_TRAP = _b("oak_trapdoor")
  O_SLAB = _b("oak_slab")
  LADDER = _b("ladder")
  NETHERRACK = _b("netherrack")
  TORCH = _b("torch")
  RED = _b("red_wool")
  WHITE = _b("white_wool")
  HAY = _b("hay_block")
  BARREL = _b("barrel")
  O_LOG = _b("oak_log")
  WATER = _b("water")
  TALL_GRASS = _b("short_grass")
  BUTTON = _b("stone_button")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  oy = 1

  # Grass courtyard pad
  for x in range(6, 28):
    for z in range(6, 28):
      _set(v, x, oy - 1, z, GRASS)

  # --- Beacon (northwest) ---
  bx, bz = 8, 8
  for y in range(8):
    for x in range(bx, bx + 3):
      for z in range(bz, bz + 3):
        edge = x in (bx, bx + 2) or z in (bz, bz + 2)
        if edge:
          _set(v, x, oy + y, z, COBBLE if y < 4 else STONE)
  # Decorative wood band
  for x in range(bx, bx + 3):
    for z in range(bz, bz + 3):
      if x == bx + 1 and z == bz + 1:
        continue
      _set(v, x, oy + 4, z, D_PLANKS)
  # Fire brazier top
  _set(v, bx + 1, oy + 8, bz + 1, NETHERRACK)
  for x, z in ((bx, bz), (bx + 2, bz), (bx, bz + 2), (bx + 2, bz + 2)):
    _set(v, x, oy + 9, z, D_STAIRS)
    _set(v, x, oy + 10, z, TORCH)

  # --- Flag pole (north center) ---
  fx, fz = 19, 7
  for x in range(fx, fx + 2):
    for z in range(fz, fz + 2):
      _set(v, x, oy, z, COBBLE)
  for y in range(1, 12):
    _set(v, fx, oy + y, fz, S_FENCE)
  for y in range(1, 6):
    _set(v, fx + 1, oy + y, fz, LADDER)
  # Checkered flag (offset wave)
  flag = ((RED, WHITE, RED), (WHITE, RED, WHITE), (RED, WHITE, RED))
  for dz, row in enumerate(flag):
    for dx, wool in enumerate(row):
      _set(v, fx + 1 + dx, oy + 9 - dz, fz + 1 + dz, wool)
  _set(v, fx, oy + 12, fz, S_SLAB_W)
  _set(v, fx, oy + 13, fz, TORCH)

  # --- Notice board (northeast) ---
  nx, nz = 23, 18
  for x in range(nx, nx + 3):
    for z in range(nz, nz + 3):
      _set(v, x, oy, z, S_SLAB)
  for x, z in ((nx, nz), (nx + 2, nz), (nx, nz + 2), (nx + 2, nz + 2)):
    _set(v, x, oy + 1, z, C_WALL)
    _set(v, x, oy + 2, z, C_WALL)
  _set(v, nx + 1, oy + 1, nz + 1, O_LOG)
  _set(v, nx + 1, oy + 2, nz + 1, O_TRAP)
  _set(v, nx, oy + 2, nz + 1, S_TRAP)
  _set(v, nx + 2, oy + 2, nz + 1, S_TRAP)
  _set(v, nx + 1, oy, nz + 1, TALL_GRASS)
  for x, z in ((nx, nz), (nx + 2, nz), (nx, nz + 2), (nx + 2, nz + 2)):
    _set(v, x, oy + 3, z, O_SLAB)
    _set(v, x, oy + 4, z, TORCH)

  # --- Hay carts (south) ---
  for cx, cz, loaded in ((9, 23, True), (14, 24, False)):
    for x in range(cx, cx + 3):
      _set(v, x, oy, cz, S_SLAB_W)
      _set(v, x, oy + 1, cz, S_TRAP)
      _set(v, x, oy + 1, cz + 1, S_TRAP)
    _set(v, cx - 1, oy + 1, cz, O_FENCE)  # hitch
    if loaded:
      _set(v, cx, oy + 1, cz + 1, HAY)
      _set(v, cx + 1, oy + 2, cz + 1, HAY)

  # --- Storage hold (west) ---
  sx, sz = 7, 16
  for x in range(sx, sx + 5):
    for z in range(sz, sz + 3):
      _set(v, x, oy, z, COBBLE)
  _set(v, sx + 1, oy + 1, sz, O_GATE)
  _set(v, sx + 2, oy + 1, sz, O_GATE)
  _set(v, sx + 1, oy + 1, sz + 1, BARREL)
  _set(v, sx + 2, oy + 1, sz + 1, BARREL)
  _set(v, sx + 3, oy + 1, sz + 1, O_LOG)
  _set(v, sx + 3, oy + 2, sz + 1, O_LOG)
  for x, z in ((sx, sz), (sx + 4, sz), (sx, sz + 2), (sx + 4, sz + 2)):
    _set(v, x, oy + 1, z, O_FENCE)
    _set(v, x, oy + 2, z, O_FENCE)
    _set(v, x, oy + 3, z, S_SLAB)

  # --- Signpost (east) ---
  gx, gz = 25, 12
  for x in range(gx, gx + 3):
    _set(v, x, oy, gz, S_SLAB)
  _set(v, gx + 1, oy + 1, gz, CHISELED)
  _set(v, gx + 1, oy + 2, gz, STONE)
  _set(v, gx + 1, oy + 3, gz, C_WALL)
  _set(v, gx, oy + 2, gz, O_SIGN)
  _set(v, gx + 2, oy + 2, gz, O_SIGN)
  _set(v, gx, oy + 3, gz, TORCH)
  _set(v, gx + 2, oy + 3, gz, TORCH)

  # --- Guard post (southeast) ---
  px, pz = 22, 22
  for x in range(px, px + 3):
    for z in range(pz, pz + 3):
      for y in range(3):
        _set(v, x, oy + y, z, COBBLE)
  for x in range(px, px + 3):
    for z in range(pz, pz + 3):
      _set(v, x, oy + 3, z, S_PLANKS)
  for x, z in ((px, pz), (px + 2, pz), (px, pz + 2), (px + 2, pz + 2)):
    _set(v, x, oy + 4, z, S_FENCE)
    _set(v, x, oy + 5, z, S_FENCE)
    _set(v, x, oy + 4, z, TORCH)
  _set(v, px, oy + 5, pz + 1, S_STAIRS)
  _set(v, px + 1, oy + 5, pz + 2, S_STAIRS)
  _set(v, px + 2, oy + 5, pz + 1, S_STAIRS)

  # --- Village well (center) ---
  wx, wz = 14, 14
  for x in range(wx, wx + 4):
    for z in range(wz, wz + 4):
      edge = x in (wx, wx + 3) or z in (wz, wz + 3)
      if edge:
        _set(v, x, oy, z, COBBLE)
      else:
        _set(v, x, oy, z, WATER)
  for x, z in ((wx, wz), (wx + 3, wz), (wx, wz + 3), (wx + 3, wz + 3)):
    for y in range(1, 4):
      _set(v, x, oy + y, z, O_FENCE)
    _set(v, x, oy + 4, z, TORCH)
  # Trellis frame
  for x in range(wx, wx + 4):
    _set(v, x, oy + 3, wz, O_FENCE)
    _set(v, x, oy + 3, wz + 3, O_FENCE)
  for z in range(wz, wz + 4):
    _set(v, wx, oy + 3, z, O_FENCE)
    _set(v, wx + 3, oy + 3, z, O_FENCE)

  return v


def _generate_fortress_lava_trap() -> np.ndarray:
  """
  Lava Trap Room — book dimensions (scaled for 32³):
    9x9 stone brick trap chamber, trapped chest bait, ceiling dispensers,
    piston door seal, redstone circuit with yellow wool wiring.
  """
  STONE = _b("stone_bricks")
  COBBLE = _b("cobblestone")
  CHISELED = _b("chiseled_stone_bricks")
  S_STAIRS = _b("stone_brick_stairs")
  DISP = _b("dispenser")
  S_PISTON = _b("sticky_piston")
  PISTON = _b("piston")
  REDSTONE = _b("redstone_wire")
  R_TORCH = _b("redstone_torch")
  REPEATER = _b("repeater")
  T_CHEST = _b("trapped_chest")
  LAVA = _b("lava")
  YELLOW = _b("yellow_wool")
  BARS = _b("iron_bars")
  LEVER = _b("lever")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  bx, bz, oy = 11, 11, 1
  sz = 9  # exterior footprint
  wh = 5  # wall height

  # Cobblestone foundation pad
  for x in range(bx - 1, bx + sz + 1):
    for z in range(bz - 1, bz + sz + 1):
      _set(v, x, oy - 1, z, COBBLE)

  # Floor and walls
  for y in range(wh):
    for x in range(bx, bx + sz):
      for z in range(bz, bz + sz):
        edge = x in (bx, bx + sz - 1) or z in (bz, bz + sz - 1)
        if y == 0:
          _set(v, x, oy, z, STONE if edge else COBBLE)
        elif edge:
          _set(v, x, oy + y, z, STONE)

  # Entrance opening (south wall)
  _set(v, bx + 4, oy + 1, bz, AIR_B)
  _set(v, bx + 4, oy + 2, bz, AIR_B)
  _set(v, bx + 3, oy + 1, bz, AIR_B)
  _set(v, bx + 5, oy + 1, bz, AIR_B)

  # Trap chamber interior — trapped chest bait
  _set(v, bx + 4, oy + 1, bz + 4, T_CHEST)
  _set(v, bx + 4, oy, bz + 4, REPEATER)
  # Lava column in chamber center
  _set(v, bx + 4, oy + 1, bz + 5, LAVA)
  _set(v, bx + 4, oy + 2, bz + 5, LAVA)
  _set(v, bx + 3, oy + 1, bz + 5, BARS)
  _set(v, bx + 5, oy + 1, bz + 5, BARS)

  # Piston door seal (flanking entrance inside)
  for y in range(3):
    _set(v, bx + 3, oy + 1 + y, bz + 1, S_PISTON)
    _set(v, bx + 5, oy + 1 + y, bz + 1, S_PISTON)
  _set(v, bx + 3, oy + 1, bz + 1, STONE)
  _set(v, bx + 5, oy + 1, bz + 1, STONE)

  # Ceiling — 3x3 dispenser grid
  cy = oy + wh
  for x in range(bx + 3, bx + 6):
    for z in range(bz + 3, bz + 6):
      _set(v, x, cy, z, DISP)
  # Lava reservoir trough above dispensers
  for x in range(bx + 2, bx + 7):
    for z in range(bz + 2, bz + 7):
      edge = x in (bx + 2, bx + 6) or z in (bz + 2, bz + 6)
      if edge:
        _set(v, x, cy + 1, z, CHISELED)
      else:
        _set(v, x, cy + 1, z, LAVA)
  # Sticky pistons holding lava (face down)
  for x in range(bx + 3, bx + 6):
    for z in range(bz + 3, bz + 6):
      _set(v, x, cy + 2, z, S_PISTON)

  # Redstone circuit — yellow wool paths on floor and exterior
  for x in range(bx + 2, bx + 7):
    _set(v, x, oy, bz + 2, YELLOW)
    _set(v, x, oy + 1, bz + 2, REDSTONE)
  # Vertical torch ladder (west exterior)
  for y in range(1, 5):
    _set(v, bx - 1, oy + y, bz + 4, YELLOW if y % 2 == 0 else R_TORCH)
  # Roof redstone
  for x in range(bx + 2, bx + 7):
    _set(v, x, cy + 2, bz + 3, YELLOW)
    _set(v, x, cy + 3, bz + 3, REDSTONE)
  # Exterior ledge wiring
  for z in range(bz + 2, bz + 7):
    _set(v, bx + sz, oy + 3, z, REDSTONE)
  _set(v, bx + sz, oy + 2, bz + 4, R_TORCH)
  _set(v, bx, oy + 3, bz + 4, LEVER)

  # Wall trim stairs on corners
  for x, z in ((bx, bz), (bx + sz - 1, bz), (bx, bz + sz - 1), (bx + sz - 1, bz + sz - 1)):
    _set(v, x, oy + 1, z, S_STAIRS)

  return v


def _generate_fortress_hidden_pitfall() -> np.ndarray:
  """
  Hidden Pitfall — book dimensions (scaled for 32³):
    stone brick hallway with tripwire, 2x2 piston floor trap,
    redstone repeater circuit below, cactus pit.
  """
  STONE = _b("stone_bricks")
  COBBLE = _b("cobblestone")
  DOOR = _b("spruce_door")
  S_PISTON = _b("sticky_piston")
  PISTON = _b("piston")
  REDSTONE = _b("redstone_wire")
  R_TORCH = _b("redstone_torch")
  REPEATER = _b("repeater")
  YELLOW = _b("yellow_wool")
  HOOK = _b("tripwire_hook")
  STRING = _b("string")
  PAINT = _b("painting")
  TORCH = _b("torch")
  CACTUS = _b("cactus")
  LEVER = _b("lever")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  bx, bz, oy = 11, 12, 5  # room floor at oy, mechanism below
  w, d = 9, 7
  wh = 3

  # Deep pit below mechanism
  for y in range(oy - 4, oy):
    for x in range(bx + 3, bx + 6):
      for z in range(bz + 2, bz + 5):
        _set(v, x, y, z, AIR_B)
  for x in range(bx + 3, bx + 6):
    for z in range(bz + 2, bz + 5):
      _set(v, x, oy - 4, z, CACTUS)

  # Redstone mechanism layer (oy-1)
  for x in range(bx, bx + w):
    for z in range(bz, bz + d):
      _set(v, x, oy - 1, z, YELLOW)
  # Perimeter redstone loop
  for x in range(bx + 1, bx + w - 1):
    _set(v, x, oy - 1, bz + 1, REDSTONE)
    _set(v, x, oy - 1, bz + d - 2, REDSTONE)
  for z in range(bz + 1, bz + d - 1):
    _set(v, bx + 1, oy - 1, z, REDSTONE)
    _set(v, bx + w - 2, oy - 1, z, REDSTONE)
  # Repeaters at varied delays
  for x, z in ((bx + 2, bz + 2), (bx + w - 3, bz + 2)):
    _set(v, x, oy - 1, z, REPEATER)
  for x, z in ((bx + 2, bz + d - 3), (bx + w - 3, bz + d - 3)):
    _set(v, x, oy - 1, z, REPEATER)
  # Torch inverter (front section default-on)
  _set(v, bx + 4, oy - 1, bz + d - 2, STONE)
  _set(v, bx + 4, oy, bz + d - 2, R_TORCH)

  # Vertical sticky pistons under trap floor (oy level)
  trap = [(bx + 3, bz + 3), (bx + 4, bz + 3), (bx + 3, bz + 4), (bx + 4, bz + 4)]
  for x, z in trap:
    _set(v, x, oy, z, S_PISTON)
  # Horizontal pistons flanking trap (pull aside sequence)
  for x in (bx + 2, bx + 5):
    for z in (bz + 3, bz + 4):
      _set(v, x, oy, z, PISTON)

  # Room shell — walls and floor
  for y in range(wh):
    for x in range(bx, bx + w):
      for z in range(bz, bz + d):
        edge = x in (bx, bx + w - 1) or z in (bz, bz + d - 1)
        is_trap = (x, z) in trap
        if y == 0:
          if is_trap:
            _set(v, x, oy + 1, z, STONE)  # piston-held floor block
          elif not edge:
            _set(v, x, oy + 1, z, STONE)
        elif edge:
          _set(v, x, oy + 1 + y, z, STONE)

  # Entrance door (south)
  _set(v, bx + 3, oy + 1, bz, DOOR)
  _set(v, bx + 4, oy + 1, bz, DOOR)
  _set(v, bx + 3, oy + 2, bz, DOOR)
  _set(v, bx + 4, oy + 2, bz, DOOR)

  # Tripwire across hallway
  _set(v, bx + 1, oy + 2, bz + 2, HOOK)
  _set(v, bx + w - 2, oy + 2, bz + 2, HOOK)
  for x in range(bx + 2, bx + w - 2):
    _set(v, x, oy + 1, bz + 2, STRING)

  # Chamber interior decor
  _set(v, bx + 1, oy + 2, bz + 4, TORCH)
  _set(v, bx + w - 2, oy + 2, bz + 4, TORCH)
  _set(v, bx + w - 2, oy + 2, bz + 5, PAINT)

  # Test lever on exterior
  _set(v, bx, oy + 2, bz + 3, LEVER)
  # Cobble foundation rim
  for x in range(bx - 1, bx + w + 1):
    for z in range(bz - 1, bz + d + 1):
      _set(v, x, oy, z, COBBLE)

  return v


def _generate_fortress_arrow_gauntlet() -> np.ndarray:
  """
  Arrow Gauntlet — book dimensions (scaled for 32³):
    8x12 stone hallway, dispenser walls, pressure plate floor,
    redstone pulse grid below, dark oak trim and doors.
  """
  STONE = _b("stone_bricks")
  CHISELED = _b("chiseled_stone_bricks")
  COBBLE = _b("cobblestone")
  D_LOG = _b("dark_oak_log")
  D_PLANKS = _b("dark_oak_planks")
  S_PLANKS = _b("spruce_planks")
  S_STAIRS = _b("spruce_stairs")
  DISP = _b("dispenser")
  PLATE = _b("stone_pressure_plate")
  REDSTONE = _b("redstone_wire")
  R_TORCH = _b("redstone_torch")
  REPEATER = _b("repeater")
  YELLOW = _b("yellow_wool")
  DOOR = _b("dark_oak_door")
  TORCH = _b("torch")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  bx, bz, fy = 10, 9, 3  # floor y
  w, d = 8, 12
  wh = 4

  # Foundation
  for x in range(bx - 1, bx + w + 1):
    for z in range(bz - 1, bz + d + 1):
      _set(v, x, fy - 2, z, COBBLE)

  # Redstone grid layer (fy-1)
  for x in range(bx, bx + w):
    for z in range(bz, bz + d):
      _set(v, x, fy - 1, z, YELLOW)
      if (x + z) % 2 == 0:
        _set(v, x, fy - 1, z, REDSTONE)

  # Pulse clock at center of grid
  cx, cz = bx + 4, bz + 6
  _set(v, cx, fy - 1, cz, STONE)
  _set(v, cx + 2, fy - 1, cz, STONE)
  _set(v, cx + 1, fy - 1, cz, REDSTONE)
  _set(v, cx, fy, cz, R_TORCH)
  _set(v, cx + 2, fy, cz, R_TORCH)
  _set(v, cx + 3, fy - 1, cz, REPEATER)

  # Walls and floor
  for y in range(wh):
    for x in range(bx, bx + w):
      for z in range(bz, bz + d):
        edge = x in (bx, bx + w - 1) or z in (bz, bz + d - 1)
        if y == 0 and not edge:
          _set(v, x, fy, z, STONE)
          _set(v, x, fy + 1, z, PLATE)
        elif edge:
          mat = CHISELED if (x + z) % 4 == 0 else STONE
          _set(v, x, fy + y, z, mat)

  # Dark oak trim — base and ceiling
  for x in range(bx, bx + w):
    for z in range(bz, bz + d):
      if x in (bx, bx + w - 1) or z in (bz, bz + d - 1):
        _set(v, x, fy, z, D_LOG)
        _set(v, x, fy + wh - 1, z, D_PLANKS)

  # Spruce stair trim on wall tops
  for x in range(bx, bx + w):
    _set(v, x, fy + wh, bz, S_STAIRS)
    _set(v, x, fy + wh, bz + d - 1, S_STAIRS)

  # Dispensers on both walls — staggered at head height
  for i, z in enumerate(range(bz + 2, bz + d - 2, 2)):
    if i % 2 == 0:
      _set(v, bx + 1, fy + 2, z, DISP)
      _set(v, bx + w - 2, fy + 2, z + 1, DISP)
    else:
      _set(v, bx + 1, fy + 2, z + 1, DISP)
      _set(v, bx + w - 2, fy + 2, z, DISP)
    # Redstone behind dispensers
    _set(v, bx, fy - 1, z, REDSTONE)
    _set(v, bx + w - 1, fy - 1, z, REDSTONE)

  # Entrance walkway (south)
  for x in range(bx + 2, bx + 6):
    _set(v, x, fy, bz - 1, S_PLANKS)

  # Exit double doors (north)
  _set(v, bx + 3, fy + 1, bz + d - 1, DOOR)
  _set(v, bx + 4, fy + 1, bz + d - 1, DOOR)
  _set(v, bx + 3, fy + 2, bz + d - 1, DOOR)
  _set(v, bx + 4, fy + 2, bz + d - 1, DOOR)
  _set(v, bx + 2, fy + 2, bz + d - 2, TORCH)
  _set(v, bx + 5, fy + 2, bz + d - 2, TORCH)

  return v


def _generate_fortress_arrow_catapult() -> np.ndarray:
  """
  Arrow Catapult — book dimensions (scaled for 32³):
    yellow wool launch pad with slime pistons, TNT/arrow dispensers,
    elevated reloading walkway, redstone timing circuit.
  """
  GRASS = _b("grass_block")
  YELLOW = _b("yellow_wool")
  DISP = _b("dispenser")
  S_PISTON = _b("sticky_piston")
  SLIME = _b("slime_block")
  TNT = _b("tnt")
  REDSTONE = _b("redstone_wire")
  R_TORCH = _b("redstone_torch")
  R_BLOCK = _b("redstone_block")
  REPEATER = _b("repeater")
  COMP = _b("comparator")
  O_FENCE = _b("oak_fence")
  D_FENCE = _b("dark_oak_fence")
  LADDER = _b("ladder")
  BUTTON = _b("stone_button")
  HOOK = _b("tripwire_hook")
  STRING = _b("string")
  D_PLANKS = _b("dark_oak_planks")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  bx, bz, oy = 12, 12, 1
  ps = 7  # platform size

  # Grass field
  for x in range(bx - 3, bx + ps + 4):
    for z in range(bz - 3, bz + ps + 4):
      _set(v, x, oy - 1, z, GRASS)

  # Fence post supports under platform corners
  for x, z in ((bx, bz), (bx + ps - 1, bz), (bx, bz + ps - 1), (bx + ps - 1, bz + ps - 1)):
    _set(v, x, oy, z, O_FENCE)
    _set(v, x, oy + 1, z, O_FENCE)

  # Yellow wool launch platform (5x5 on 7x7)
  for x in range(bx + 1, bx + ps - 1):
    for z in range(bz + 1, bz + ps - 1):
      _set(v, x, oy + 2, z, YELLOW)

  # Slime catapult — 2x2 pistons, 3x3 slime pad
  for x in range(bx + 2, bx + 4):
    for z in range(bz + 2, bz + 4):
      _set(v, x, oy + 2, z, S_PISTON)
  for x in range(bx + 2, bx + 5):
    for z in range(bz + 2, bz + 5):
      _set(v, x, oy + 3, z, SLIME)

  # Upward dispensers around platform edge
  for x, z in (
    (bx + 1, bz + 3), (bx + 5, bz + 3), (bx + 3, bz + 1), (bx + 3, bz + 5),
    (bx + 1, bz + 1), (bx + 5, bz + 5),
  ):
    _set(v, x, oy + 3, z, DISP)

  # TNT dispensers row (2 blocks above platform east side)
  for z in range(bz + 2, bz + 5):
    _set(v, bx + 5, oy + 4, z, DISP)
    _set(v, bx + 5, oy + 5, z, TNT)  # loaded ammo visible

  # Timing circuit — repeater line south of platform
  for x in range(bx, bx + 8):
    _set(v, x, oy + 2, bz - 2, YELLOW)
    if x < bx + 7:
      _set(v, x, oy + 2, bz - 2, REPEATER)
  _set(v, bx + 7, oy + 2, bz - 2, BUTTON)
  _set(v, bx + 3, oy + 2, bz - 2, REDSTONE)

  # Elevated walkway pillar + ladder (west side)
  wy = oy + 10
  for y in range(oy + 2, wy + 1):
    _set(v, bx - 1, y, bz + 3, D_FENCE)
    _set(v, bx, y, bz + 3, LADDER)

  # Walkway platform (T-shape)
  for x in range(bx, bx + ps):
    _set(v, x, wy, bz + 2, D_PLANKS)
    _set(v, x, wy, bz + 4, D_PLANKS)
  for z in range(bz + 1, bz + 6):
    _set(v, bx + 3, wy, z, D_PLANKS)

  # Downward arrow dispensers at cross ends
  for x, z in ((bx, bz + 3), (bx + ps - 1, bz + 3), (bx + 3, bz), (bx + 3, bz + ps - 1)):
    _set(v, x, wy - 1, z, DISP)

  # T-shaped redstone on walkway + comparator clock
  for x in range(bx, bx + ps):
    _set(v, x, wy + 1, bz + 3, REDSTONE)
  for z in range(bz + 1, bz + 6):
    _set(v, bx + 3, wy + 1, z, REDSTONE)
  _set(v, bx + 1, wy + 1, bz + 3, R_BLOCK)
  _set(v, bx + 2, wy + 1, bz + 3, COMP)

  # Tripwire automation (scaled front lines)
  for x in range(bx - 2, bx + ps + 2):
    _set(v, x, oy, bz + ps + 3, STRING)
    _set(v, x, oy, bz + ps + 6, STRING)
  _set(v, bx - 2, oy + 1, bz + ps + 3, HOOK)
  _set(v, bx + ps + 1, oy + 1, bz + ps + 3, HOOK)
  _set(v, bx - 2, oy + 1, bz + ps + 6, HOOK)
  _set(v, bx + ps + 1, oy + 1, bz + ps + 6, HOOK)

  return v


_GENERATORS: dict[str, object] = {
  "fortress_turret": _generate_fortress_turret,
  "fortress_outer_wall": _generate_fortress_outer_wall,
  "fortress_portcullis": _generate_fortress_portcullis,
  "fortress_keep": _generate_fortress_keep,
  "fortress_throne_room": _generate_fortress_throne_room,
  "fortress_barracks": _generate_fortress_barracks,
  "fortress_enchanting_room": _generate_fortress_enchanting_room,
  "fortress_dungeon": _generate_fortress_dungeon,
  "fortress_village_house": _generate_fortress_village_house,
  "fortress_market_square": _generate_fortress_market_square,
  "fortress_travelers_tavern": _generate_fortress_travelers_tavern,
  "fortress_cathedral": _generate_fortress_cathedral,
  "fortress_castle_bits": _generate_fortress_castle_bits,
  "fortress_lava_trap": _generate_fortress_lava_trap,
  "fortress_hidden_pitfall": _generate_fortress_hidden_pitfall,
  "fortress_arrow_gauntlet": _generate_fortress_arrow_gauntlet,
  "fortress_arrow_catapult": _generate_fortress_arrow_catapult,
}
