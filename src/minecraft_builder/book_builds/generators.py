"""Procedural generators that recreate book builds from registry specs."""

from __future__ import annotations

import numpy as np

from ..data.palette import AIR, BlockPalette, voxels_to_palette_indices
from .registry import BookBuild, get_build


def generate_book_build(build_id: str, palette: BlockPalette | None = None) -> tuple[np.ndarray, BookBuild]:
  """Generate voxel indices for a book build. No Minecraft required."""
  build = get_build(build_id)
  palette = palette or BlockPalette()

  if build_id == "remote_outpost":
    voxels = _generate_remote_outpost()
  elif build_id == "lighting_system_house":
    voxels = _generate_lighting_system_house()
  elif build_id == "exotic_villa":
    voxels = _generate_exotic_villa()
  elif build_id == "ocean_observatory":
    voxels = _generate_ocean_observatory()
  elif build_id == "steampunk_airship":
    voxels = _generate_steampunk_airship()
  elif build_id.startswith("bite_combo_"):
    from .combination_generators import generate_combination
    voxels = generate_combination(build_id)
  elif build_id.startswith("epic_inventions_"):
    from .epic_inventions_generators import generate_epic_inventions_build
    voxels = generate_epic_inventions_build(build_id)
  elif build_id.startswith("epic_builds_"):
    from .epic_builds_generators import generate_epic_build
    voxels = generate_epic_build(build_id)
  elif build_id.startswith("epic_bases_"):
    from .epic_bases_generators import generate_epic_base
    voxels = generate_epic_base(build_id)
  elif build_id.startswith("bite_"):
    from .bite_sized_generators import generate_bite_sized
    voxels = generate_bite_sized(build_id)
  elif build_id.startswith("fortress_"):
    from .exploded_fortress_generators import generate_fortress_build
    voxels = generate_fortress_build(build_id)
  else:
    raise NotImplementedError(f"No generator for {build_id}")

  indices = voxels_to_palette_indices(voxels, palette)
  return indices, build


def _b(name: str) -> str:
  return name if name.startswith("minecraft:") else f"minecraft:{name}"


def _generate_remote_outpost() -> np.ndarray:
  """
  Simplified Remote Outpost from book dimensions:
    House: 7w x 10h x 7d
    Turret: 9w x 20h x 9d (attached on one side)
  Fits in 32³ by centering the combined footprint.
  """
  COBBLE = _b("cobblestone")
  MOSSY = _b("mossy_cobblestone")
  STONE = _b("stone_bricks")
  PLANKS = _b("dark_oak_planks")
  LOG = _b("dark_oak_log")
  DIORITE = _b("diorite")
  STAIRS = _b("dark_oak_stairs")
  GLASS = _b("glass_pane")
  AIR_B = AIR
  WOOL_B = _b("blue_wool")
  WOOL_Y = _b("yellow_wool")
  GLOW = _b("glowstone")
  FENCE = _b("cobblestone_wall")
  TRAP = _b("dark_oak_trapdoor")
  WATER = _b("water")

  # Combined footprint ~16x15, height 20 — pad into 32³
  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oy, oz = 8, 0, 8  # origin offset to center build

  hw, hh, hd = 7, 10, 7
  tw, th, td = 9, 20, 9

  # --- HOUSE (left portion) ---
  hx, hz = ox, oz
  # Foundation
  for x in range(hx, hx + hw):
    for z in range(hz, hz + hd):
      _set(v, x, oy, z, COBBLE)

  # Ground floor walls
  for y in range(oy + 1, oy + 5):
    for x in range(hx, hx + hw):
      for z in range(hz, hz + hd):
        edge = x in (hx, hx + hw - 1) or z in (hz, hz + hd - 1)
        if edge:
          _set(v, x, y, z, LOG if (x in (hx, hx+hw-1) and z in (hz, hz+hd-1)) else PLANKS)
    # Door
    _set(v, hx + 3, oy + 1, hz, AIR_B)
    _set(v, hx + 3, oy + 2, hz, AIR_B)
    # Windows
    _set(v, hx + 1, oy + 2, hz, GLASS)
    _set(v, hx + 5, oy + 2, hz, GLASS)

  # Ground floor — hollow interior (workshop)
  for x in range(hx + 1, hx + hw - 1):
    for z in range(hz + 1, hz + hd - 1):
      for y in range(oy + 1, oy + 4):
        _set(v, x, y, z, AIR_B)

  # Upper floor
  for y in range(oy + 5, oy + 9):
    for x in range(hx, hx + hw):
      for z in range(hz, hz + hd):
        edge = x in (hx, hx + hw - 1) or z in (hz, hz + hd - 1)
        if edge:
          _set(v, x, y, z, LOG if (x in (hx, hx+hw-1) and z in (hz, hz+hd-1)) else PLANKS)
  # Upper floor hollow (living quarters)
  for x in range(hx + 1, hx + hw - 1):
    for z in range(hz + 1, hz + hd - 1):
      for y in range(oy + 5, oy + 8):
        _set(v, x, y, z, AIR_B)

  # Floor between stories
  for x in range(hx, hx + hw):
    for z in range(hz, hz + hd):
      _set(v, x, oy + 4, z, PLANKS)

  # Gabled roof
  for layer in range(3):
    for x in range(hx + layer, hx + hw - layer):
      for z in range(hz + layer, hz + hd - layer):
        _set(v, x, oy + 9 + layer, z, STAIRS)

  # --- TURRET (right of house) ---
  tx, tz = hx + hw - 1, oz + 1
  for y in range(oy, oy + th):
    for x in range(tx, tx + tw):
      for z in range(tz, tz + td):
        edge = x in (tx, tx + tw - 1) or z in (tz, tz + td - 1)
        if edge:
          mat = MOSSY if (x + z + y) % 5 == 0 else COBBLE if y < 12 else STONE
          _set(v, x, y, z, mat)
        elif y < oy + 12:
          _set(v, x, y, z, AIR_B)  # hollow tower interior

  # Turret arrow slits
  for y in range(oy + 4, oy + 12, 3):
    _set(v, tx + tw - 1, y, tz + td // 2, GLASS)

  # Turret rooftop lookout
  for x in range(tx, tx + tw):
    for z in range(tz, tz + td):
      _set(v, x, oy + th - 1, z, PLANKS)
  # Battlements
  for x in range(tx, tx + tw, 2):
    for z in range(tz, tz + td, 2):
      _set(v, x, oy + th, z, STONE)

  # --- EXTERIOR FEATURES ---
  # Enclosed courtyard wall (front of house)
  for x in range(hx - 1, hx + hw + 1):
    _set(v, x, oy + 1, hz - 2, FENCE)
  for z in range(hz - 2, hz + hd):
    _set(v, hx - 1, oy + 1, z, FENCE)

  # Well at tower base
  wx, wz = tx + 2, tz + 2
  for x in range(wx, wx + 2):
    for z in range(wz, wz + 2):
      _set(v, x, oy, z, COBBLE)
      _set(v, x, oy - 1 if oy > 0 else oy, z, WATER)
  _set(v, wx, oy + 1, wz, TRAP)

  # Lamp post
  _set(v, hx - 2, oy + 1, hz + 2, FENCE)
  _set(v, hx - 2, oy + 2, hz + 2, GLOW)

  # Checkered flag on pole behind house
  px, pz = hx + 2, hz + hd + 1
  for y in range(oy + 5, oy + 12):
    _set(v, px, y, pz, FENCE)
  for dx in range(3):
    for dy in range(3):
      color = WOOL_B if (dx + dy) % 2 == 0 else WOOL_Y
      _set(v, px + 1 + dx, oy + 10 + dy, pz, color)

  return v


def _generate_lighting_system_house() -> np.ndarray:
  """Two-room house with double walls, ceiling redstone lamps, oak exterior."""
  STONE = _b("stone_bricks")
  PLANKS = _b("oak_planks")
  LOG = _b("oak_log")
  STAIRS = _b("dark_oak_stairs")
  LAMP = _b("redstone_lamp")
  LEVER = _b("lever")
  GLASS = _b("glass_pane")
  GRAY = _b("gray_concrete")
  SPRUCE = _b("spruce_planks")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oy, oz = 10, 0, 10
  w, h, d = 10, 8, 8  # inner footprint

  # Stone brick inner walls (two rooms)
  for y in range(oy, oy + 5):
    for x in range(ox, ox + w):
      for z in range(oz, oz + d):
        edge = x in (ox, ox + w - 1) or z in (oz, oz + d - 1)
        mid_wall = x == ox + w // 2 and z > oz + 1
        if edge or mid_wall:
          _set(v, x, y, z, STONE)
        else:
          _set(v, x, y, z, AIR_B)
  # Door
  _set(v, ox + w // 2, oy + 1, oz, AIR_B)
  _set(v, ox + w // 2, oy + 2, oz, AIR_B)
  # Room divider doorway
  _set(v, ox + w // 2, oy + 1, oz + d // 2, AIR_B)
  _set(v, ox + w // 2, oy + 2, oz + d // 2, AIR_B)

  # Upper floor bedroom
  for y in range(oy + 5, oy + 8):
    for x in range(ox, ox + w):
      for z in range(oz, oz + d):
        edge = x in (ox, ox + w - 1) or z in (oz, oz + d - 1)
        if edge:
          _set(v, x, y, z, GRAY)
        else:
          _set(v, x, y, z, AIR_B)
  # Floor between stories
  for x in range(ox, ox + w):
    for z in range(oz, oz + d):
      _set(v, x, oy + 4, z, SPRUCE)

  # Ceiling redstone lamps (both floors)
  for floor_y in (oy + 3, oy + 7):
    for x in range(ox + 2, ox + w - 2, 2):
      for z in range(oz + 2, oz + d - 2, 2):
        _set(v, x, floor_y, z, LAMP)

  # Lever on interior wall
  _set(v, ox + 2, oy + 2, oz + 1, LEVER)

  # Oak exterior shell (double wall — 1 block gap)
  for y in range(oy, oy + 5):
    for x in range(ox - 1, ox + w + 1):
      for z in range(oz - 1, oz + d + 1):
        outer = x in (ox - 1, ox + w) or z in (oz - 1, oz + d)
        if outer:
          corner = x in (ox - 1, ox + w) and z in (oz - 1, oz + d)
          _set(v, x, y, z, LOG if corner else PLANKS)

  # Windows in outer wall
  for wx in (ox + 2, ox + w - 3):
    _set(v, wx, oy + 2, oz - 1, GLASS)
    _set(v, wx, oy + 2, oz + d, GLASS)

  # Dark oak gabled roof
  for layer in range(3):
    for x in range(ox - 1 + layer, ox + w + 1 - layer):
      for z in range(oz - 1 + layer, oz + d + 1 - layer):
        _set(v, x, oy + 8 + layer, z, STAIRS)

  return v


def _generate_exotic_villa() -> np.ndarray:
  """
  Mediterranean exotic villa from book dimensions (scaled to fit 32³):
    Main body 12w x 10d, left tower 4w, right wing 3w, height ~16.
    White quartz colonnade, sandstone tiered roofs, pool in front.
  """
  QUARTZ = _b("quartz_block")
  PILLAR = _b("quartz_pillar")
  CHISELED = _b("chiseled_quartz_block")
  S_SAND = _b("smooth_sandstone")
  S_SLAB = _b("smooth_sandstone_slab")
  S_STAIRS = _b("smooth_sandstone_stairs")
  GLASS = _b("light_blue_stained_glass_pane")
  FENCE = _b("dark_oak_fence")
  WATER = _b("water")
  BIRCH = _b("birch_planks")
  SAND = _b("red_sand")
  TERRA = _b("terracotta")
  STONE_SLAB = _b("stone_slab")
  LEAVES = _b("oak_leaves")
  LOG = _b("birch_log")
  LAMP = _b("redstone_lamp")
  DARK = _b("dark_oak_planks")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)

  # Footprint: tower(4) + main(12) + wing(3) = 19w, depth 10
  ox, oy, oz = 6, 1, 11
  tw, mw, rw = 4, 12, 3
  total_w = tw + mw + rw
  md = 10
  ground_h = 6
  upper_h = 4
  mx = ox + tw  # main body x start

  # Mesa terrain
  for x in range(ox - 2, ox + total_w + 2):
    for z in range(oz - 10, oz + md + 3):
      _set(v, x, oy - 1, z, SAND if (x + z) % 4 < 2 else TERRA)

  def _fill_box(x0: int, y0: int, z0: int, w: int, h: int, d: int, mat: str, hollow: bool = False) -> None:
    for y in range(y0, y0 + h):
      for x in range(x0, x0 + w):
        for z in range(z0, z0 + d):
          edge = x in (x0, x0 + w - 1) or z in (z0, z0 + d - 1) or y in (y0, y0 + h - 1)
          if hollow and not edge:
            _set(v, x, y, z, AIR_B)
          else:
            _set(v, x, y, z, mat)

  # --- GROUND FLOOR ---
  # Left tower (full height ground floor)
  _fill_box(ox, oy, oz, tw, ground_h, md, QUARTZ, hollow=True)
  for x in (ox, ox + tw - 1):
    for y in range(oy, oy + ground_h):
      for z in range(oz, oz + md):
        _set(v, x, y, z, CHISELED)

  # Main body shell (open front for colonnade)
  for y in range(oy, oy + ground_h):
    for x in range(mx, mx + mw):
      for z in range(oz, oz + md):
        back = z == oz + md - 1
        side = x in (mx, mx + mw - 1)
        front_col = z == oz and y >= oy + 3
        if back or side or front_col:
          _set(v, x, y, z, QUARTZ)
        else:
          _set(v, x, y, z, AIR_B)

  # Right wing (L-shape extension)
  for y in range(oy, oy + ground_h):
    for x in range(mx + mw, ox + total_w):
      for z in range(oz + 2, oz + md):
        edge = x in (mx + mw, ox + total_w - 1) or z in (oz + 2, oz + md - 1)
        if edge:
          _set(v, x, y, z, QUARTZ)
        else:
          _set(v, x, y, z, AIR_B)

  # Colonnade pillars along front
  for x in range(mx + 1, mx + mw - 1, 3):
    for y in range(oy, oy + ground_h):
      _set(v, x, y, oz, PILLAR)

  # Arched main entrance (double-wide)
  entrance = mx + mw // 2
  for y in range(oy, oy + 3):
    for dx in (-1, 0, 1):
      _set(v, entrance + dx, y, oz, AIR_B)

  # Ground floor
  for x in range(ox + 1, ox + total_w - 1):
    for z in range(oz + 1, oz + md - 1):
      _set(v, x, oy, z, BIRCH)

  # Tall windows on sides
  for z in (oz + 2, oz + md - 3):
    for y in range(oy + 1, oy + 4):
      _set(v, mx, y, z, GLASS)
      _set(v, mx + mw - 1, y, z, GLASS)

  # --- MEZZANINE (partial floor at y+4) ---
  mez_y = oy + 4
  mez_x, mez_z = mx + 2, oz + 2
  mez_w, mez_d = 8, 6
  for x in range(mez_x, mez_x + mez_w):
    for z in range(mez_z, mez_z + mez_d):
      _set(v, x, mez_y, z, BIRCH)
  # Mezzanine front railing overlooking living area
  for x in range(mez_x, mez_x + mez_w):
    _set(v, x, mez_y + 1, mez_z, FENCE)

  # --- UPPER FLOOR (bedroom level) ---
  upper_y = oy + 5
  uw, ud = 9, 9
  ux, uz = mx + 1, oz + 1
  for y in range(upper_y, upper_y + upper_h):
    for x in range(ux, ux + uw):
      for z in range(uz, uz + ud):
        edge = x in (ux, ux + uw - 1) or z in (uz, uz + ud - 1)
        if edge:
          _set(v, x, y, z, QUARTZ)
        else:
          _set(v, x, y, z, AIR_B)

  # Upper floor slab
  for x in range(ux, ux + uw):
    for z in range(uz, uz + ud):
      _set(v, x, upper_y, z, BIRCH)

  # Shuttered windows + balconies on upper floor
  for bx in (ux + 1, ux + uw - 2):
    for y in range(upper_y + 1, upper_y + 3):
      _set(v, bx, y, uz - 1, GLASS)
      _set(v, bx, y, uz + ud, GLASS)
    # Balcony platforms
    for dx in range(3):
      _set(v, bx + dx - 1, upper_y, uz - 2, S_SLAB)
      _set(v, bx + dx - 1, upper_y + 1, uz - 2, FENCE)
      _set(v, bx + dx - 1, upper_y, uz + ud + 1, S_SLAB)
      _set(v, bx + dx - 1, upper_y + 1, uz + ud + 1, FENCE)

  # Ceiling lamps (automatic lighting — visual only)
  for x in range(ux + 2, ux + uw - 2, 2):
    for z in range(uz + 2, uz + ud - 2, 2):
      _set(v, x, upper_y + upper_h - 1, z, LAMP)

  # --- TOWER (extends above upper floor on left) ---
  tower_extra = 5
  tower_top = upper_y + upper_h + tower_extra
  for y in range(upper_y + upper_h, tower_top):
    for x in range(ox, ox + tw):
      for z in range(oz, oz + md):
        edge = x in (ox, ox + tw - 1) or z in (oz, oz + md - 1)
        if edge:
          _set(v, x, y, z, CHISELED if x in (ox, ox + tw - 1) else QUARTZ)
        else:
          _set(v, x, y, z, AIR_B)

  # --- TIERED SANDSTONE ROOFS ---
  def _tiered_roof(rx: int, rz: int, rw_: int, rd: int, base_y: int, layers: int = 3) -> None:
    for layer in range(layers):
      for x in range(rx + layer, rx + rw_ - layer):
        for z in range(rz + layer, rz + rd - layer):
          _set(v, x, base_y + layer, z, S_SLAB if layer < layers - 1 else S_STAIRS)

  _tiered_roof(ux, uz, uw, ud, upper_y + upper_h)
  _tiered_roof(mx, oz, mw, md, oy + ground_h, layers=2)
  _tiered_roof(ox, oz, tw, md, tower_top, layers=2)

  # --- SWIMMING POOL (front of villa) ---
  pool_z = oz - 6
  for x in range(mx + 2, mx + mw - 2):
    for z in range(pool_z, pool_z + 4):
      _set(v, x, oy - 1, z, WATER)
      _set(v, x, oy, z, WATER)
  # Pool surround
  for x in range(mx + 1, mx + mw - 1):
    for z in range(pool_z - 1, pool_z + 5):
      if v[x, oy, z] == AIR_B:
        _set(v, x, oy, z, STONE_SLAB)
  # Pool stairs
  _set(v, mx + mw // 2, oy, pool_z + 4, S_STAIRS)

  # Outdoor lounge seating
  for dx in range(4):
    _set(v, mx + 1 + dx, oy, pool_z - 2, DARK)
  _set(v, mx + 2, oy + 1, pool_z - 2, FENCE)

  # Retaining wall around property
  for x in range(ox - 1, ox + total_w + 1):
    _set(v, x, oy, oz - 8, STONE_SLAB)
    _set(v, x, oy, oz + md, STONE_SLAB)
  for z in range(oz - 8, oz + md + 1):
    _set(v, ox - 1, oy, z, STONE_SLAB)
    _set(v, ox + total_w, oy, z, STONE_SLAB)

  # Landscaping trees
  for tx, tz in ((ox - 1, oz - 3), (ox + total_w, oz + 2), (ox + 1, oz + md + 1)):
    for y in range(oy, oy + 4):
      _set(v, tx, y, tz, LOG)
    for dy in range(2, 5):
      for dx in range(-1, 2):
        for dz in range(-1, 2):
          if abs(dx) + abs(dz) < 2:
            _set(v, tx + dx, oy + dy, tz + dz, LEAVES)

  return v


def _generate_ocean_observatory() -> np.ndarray:
  """
  Ocean observatory from book (scaled to 32³):
    ~14-block glass dome on seafloor, 4x4 central shaft, surface platform
    with helipad, crane, and antenna. Industrial white/gray/glass palette.
  """
  GLASS = _b("glass")
  B_GLASS = _b("light_blue_stained_glass")
  QUARTZ = _b("quartz_block")
  IRON = _b("iron_block")
  STONE = _b("stone_bricks")
  ANDESITE = _b("polished_andesite")
  WATER = _b("water")
  GRAVEL = _b("gravel")
  PRISM = _b("prismarine")
  GLOW = _b("glowstone")
  ACACIA = _b("acacia_planks")
  BARS = _b("iron_bars")
  FENCE = _b("oak_fence")
  REDSTONE = _b("redstone_block")
  BLACK = _b("black_concrete")
  BROWN = _b("brown_terracotta")
  CARPET = _b("red_carpet")
  PLANKS = _b("oak_planks")
  ICE = _b("ice")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cx, cz = 16, 16
  floor_y = 2
  sea_level = 11

  def _in_circle(x: int, z: int, r: int) -> bool:
    return (x - cx) ** 2 + (z - cz) ** 2 <= r * r

  def _on_circle(x: int, z: int, r: int) -> bool:
    d2 = (x - cx) ** 2 + (z - cz) ** 2
    return (r - 1) ** 2 <= d2 <= r * r

  # Seafloor
  for x in range(4, 28):
    for z in range(4, 28):
      _set(v, x, floor_y - 1, z, GRAVEL if (x + z) % 3 else PRISM)

  # Ocean water
  for y in range(floor_y, sea_level + 1):
    for x in range(2, 30):
      for z in range(2, 30):
        if v[x, y, z] == AIR_B:
          _set(v, x, y, z, WATER)

  # --- GLASS DOME (hemisphere) ---
  dome_radii = (7, 7, 6, 6, 5, 4, 3)  # layer radii bottom to top
  for i, radius in enumerate(dome_radii):
    y = floor_y + i
    for x in range(cx - radius, cx + radius + 1):
      for z in range(cz - radius, cz + radius + 1):
        if not _in_circle(x, z, radius):
          continue
        inner_r = max(radius - 2, 2)
        if _in_circle(x, z, inner_r) and i > 0:
          if i == 1:
            _set(v, x, y, z, PLANKS if (x + z) % 5 else CARPET)
          else:
            _set(v, x, y, z, AIR_B)
        elif _on_circle(x, z, radius) or i == 0:
          mat = STONE if i == 0 else GLASS
          _set(v, x, y, z, mat)
        elif i == 0:
          _set(v, x, y, z, ANDESITE)

  dome_top = floor_y + len(dome_radii) - 1

  # Internal support columns
  for px, pz in ((cx - 3, cz - 3), (cx + 3, cz - 3), (cx - 3, cz + 3), (cx + 3, cz + 3)):
    for y in range(floor_y + 1, dome_top):
      _set(v, px, y, pz, IRON)

  # Flying buttresses (4 diagonal quartz supports)
  for dx, dz in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
    for step in range(1, 4):
      bx, bz = cx + dx * (7 + step), cz + dz * (7 + step)
      for y in range(floor_y, floor_y + 3):
        _set(v, bx, y, bz, QUARTZ)

  # --- CENTRAL SHAFT ---
  shaft_r = 2  # 4x4 interior
  shaft_top = floor_y + 16
  for y in range(dome_top, shaft_top + 1):
    for x in range(cx - shaft_r, cx + shaft_r):
      for z in range(cz - shaft_r, cz + shaft_r):
        edge = x in (cx - shaft_r, cx + shaft_r - 1) or z in (cz - shaft_r, cz + shaft_r - 1)
        if edge:
          # Blue glass window strips on two faces
          window = (x == cx - shaft_r or x == cx + shaft_r - 1) and y % 2 == 0
          _set(v, x, y, z, B_GLASS if window else QUARTZ)
        else:
          _set(v, x, y, z, AIR_B)

  # Specimen ice tanks mid-shaft
  tank_y = floor_y + 10
  for tx in (cx - 1, cx + 1):
    for tz in (cz - 1, cz + 1):
      for y in range(tank_y, tank_y + 2):
        _set(v, tx, y, tz, ICE)

  # --- SURFACE PLATFORM ---
  plat_y = shaft_top
  plat_size = 5
  for x in range(cx - plat_size, cx + plat_size):
    for z in range(cz - plat_size, cz + plat_size):
      _set(v, x, plat_y, z, STONE)
      _set(v, x, plat_y + 1, z, ANDESITE)

  # Extended wings (T-shaped dock)
  for x in range(cx - 2, cx + 3):
    for z in range(cz + plat_size, cz + plat_size + 4):
      _set(v, x, plat_y, z, STONE)
      _set(v, x, plat_y + 1, z, ANDESITE)
  for x in range(cx - plat_size - 3, cx - plat_size):
    for z in range(cz - 2, cz + 3):
      _set(v, x, plat_y, z, STONE)
      _set(v, x, plat_y + 1, z, ANDESITE)

  # Platform railings
  for x in range(cx - plat_size, cx + plat_size):
    _set(v, x, plat_y + 2, cz - plat_size, BARS)
    _set(v, x, plat_y + 2, cz + plat_size - 1, BARS)
  for z in range(cz - plat_size, cz + plat_size + 4):
    _set(v, cx - plat_size, plat_y + 2, z, BARS)
    _set(v, cx + plat_size - 1, plat_y + 2, z, BARS)

  # Under-platform glowstone (illuminate water below)
  for x in range(cx - 3, cx + 4):
    for z in range(cz - 3, cz + 4):
      _set(v, x, plat_y - 1, z, GLOW)

  # --- HELIPAD (side extension) ---
  pad_cx, pad_cz = cx + plat_size + 2, cz
  pad_r = 3
  for x in range(pad_cx - pad_r, pad_cx + pad_r + 1):
    for z in range(pad_cz - pad_r, pad_cz + pad_r + 1):
      if (x - pad_cx) ** 2 + (z - pad_cz) ** 2 <= pad_r * pad_r:
        _set(v, x, plat_y, z, BLACK if (x + z) % 2 else BROWN)
        _set(v, x, plat_y + 1, z, ANDESITE)
  # H marking
  for dz in (-1, 0, 1):
    _set(v, pad_cx, plat_y + 1, pad_cz + dz, BROWN)
  for dx in (-1, 1):
    _set(v, pad_cx + dx, plat_y + 1, pad_cz, BROWN)

  # --- CRANE (acacia arm over water) ---
  crane_x, crane_z = cx - plat_size - 2, cz + plat_size + 2
  for y in range(plat_y, plat_y + 4):
    _set(v, crane_x, y, crane_z, ACACIA)
  for arm in range(4):
    _set(v, crane_x, plat_y + 3, crane_z + arm, ACACIA)
  _set(v, crane_x, plat_y + 2, crane_z + 4, FENCE)
  _set(v, crane_x, plat_y + 1, crane_z + 4, GLOW)

  # --- ANTENNA (communication mast) ---
  for y in range(plat_y + 2, plat_y + 7):
    _set(v, cx, y, cz, QUARTZ)
  _set(v, cx, plat_y + 7, cz, BARS)
  _set(v, cx, plat_y + 8, cz, REDSTONE)

  # Clear water inside dome and shaft (overwrite)
  for y in range(floor_y + 1, dome_top + 1):
    for x in range(cx - 6, cx + 7):
      for z in range(cz - 6, cz + 7):
        if _in_circle(x, z, 5) and v[x, y, z] == WATER:
          _set(v, x, y, z, AIR_B)

  return v


def _generate_steampunk_airship() -> np.ndarray:
  """
  Steampunk airship from book dimensions (32 x 13 x 23 — fits 32³):
    Elongated green/orange balloon, dark oak hull, fence rigging, stern machinery.
  """
  GREEN = _b("green_wool")
  ORANGE = _b("orange_wool")
  BROWN = _b("brown_wool")
  PLANKS = _b("dark_oak_planks")
  STAIRS = _b("dark_oak_stairs")
  FENCE = _b("dark_oak_fence")
  TRAP = _b("dark_oak_trapdoor")
  GLOW = _b("glowstone")
  QUARTZ = _b("quartz_block")
  STONE = _b("stone_bricks")
  WALL = _b("cobblestone_wall")
  FIN = _b("light_blue_stained_glass")
  GLASS = _b("glass_pane")
  PISTON = _b("piston")
  FURNACE = _b("furnace")
  CHEST = _b("chest")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  cz = 16  # width center

  def _hull_hw(x: int) -> int:
    """Half-width of hull at position x (prow at x=0)."""
    if x < 6:
      return max(1, x // 2 + 1)
    if x > 27:
      return 5
    return 6

  deck_y = 3
  hull_top = 8
  balloon_cy = 17
  balloon_rx = 12
  balloon_ry = 5
  balloon_rz = 5

  def _in_balloon(x: int, y: int, z: int) -> bool:
    dx = (x - 16) / balloon_rx
    dy = (y - balloon_cy) / balloon_ry
    dz = (z - cz) / balloon_rz
    return dx * dx + dy * dy + dz * dz <= 1.0

  def _on_balloon_shell(x: int, y: int, z: int) -> bool:
    if not _in_balloon(x, y, z):
      return False
    for nx, ny, nz in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
      if not _in_balloon(nx, ny, nz):
        return True
    return False

  # --- HULL (main deck + keel) ---
  for x in range(32):
    hw = _hull_hw(x)
    for z in range(cz - hw, cz + hw + 1):
      # Keel / lower hull
      for y in range(0, deck_y):
        edge = z in (cz - hw, cz + hw) or y == 0
        _set(v, x, y, z, PLANKS if edge or y == 0 else AIR_B)
      # Main deck floor
      _set(v, x, deck_y, z, PISTON if (x + z) % 3 == 0 else PLANKS)
      # Hull sides
      for y in range(deck_y + 1, hull_top):
        side = z in (cz - hw, cz + hw)
        if side:
          _set(v, x, y, z, PLANKS)
        else:
          _set(v, x, y, z, AIR_B)
      # Deck railings
      if z in (cz - hw, cz + hw) and hw >= 3:
        _set(v, x, hull_top, z, FENCE)

  # Stern castle (raised rear section x=22-30)
  for x in range(22, 31):
    for z in range(cz - 4, cz + 5):
      for y in range(deck_y + 1, deck_y + 6):
        edge = z in (cz - 4, cz + 4) or x in (22, 30)
        if edge:
          _set(v, x, y, z, PLANKS)
        else:
          _set(v, x, y, z, AIR_B)
    # Bay windows on sides
    for z in (cz - 4, cz + 4):
      for y in range(deck_y + 2, deck_y + 4):
        _set(v, x, y, z, GLASS)
    # Castle roof
    for z in range(cz - 3, cz + 4):
      _set(v, x, deck_y + 6, z, STAIRS)

  # White staircase to bridge
  for y in range(deck_y, deck_y + 4):
    _set(v, 24, y, cz, QUARTZ)

  # Mechanical cog decorations on hull sides
  for x in range(10, 22, 4):
    for z_off in (-7, 7):
      zz = cz + z_off
      if 0 <= zz < 32:
        _set(v, x, deck_y + 2, zz, STAIRS)
        _set(v, x + 1, deck_y + 2, zz, PLANKS)
        _set(v, x, deck_y + 3, zz, STAIRS)

  # --- BALLOON ENVELOPE ---
  for x in range(32):
    for y in range(32):
      for z in range(32):
        if not _on_balloon_shell(x, y, z):
          continue
        # Vertical green/orange stripes
        stripe = GREEN if (x + z) % 4 < 2 else ORANGE
        # Horizontal brown rigging bands
        if y % 4 == 0:
          _set(v, x, y, z, BROWN)
        else:
          _set(v, x, y, z, stripe)

  # Dark oak trapdoor accents on rigging bands
  for x in range(6, 27, 5):
    for z in range(cz - 4, cz + 5, 3):
      y = balloon_cy - 2
      if _in_balloon(x, y, z):
        _set(v, x, y, z, TRAP)

  # --- RIGGING (fence posts deck to balloon) ---
  rig_y_top = balloon_cy - balloon_ry + 1
  for x in range(8, 26, 4):
    hw = _hull_hw(x)
    for z in (cz - hw + 1, cz + hw - 1):
      for y in range(hull_top + 1, rig_y_top):
        _set(v, x, y, z, FENCE)

  # Glowstone lanterns on deck
  for x in range(6, 28, 6):
    _set(v, x, hull_top + 1, cz, FENCE)
    _set(v, x, hull_top + 2, cz, GLOW)

  # --- STERN PROPULSION (rudders, chimneys, fins) ---
  for x in range(28, 32):
    for y in range(deck_y, deck_y + 8):
      _set(v, x, y, cz, WALL)
    # Vertical rudder fin
    for y in range(deck_y + 2, deck_y + 10):
      _set(v, 31, y, cz, QUARTZ)
    # Light blue side fins
    for z in (cz - 6, cz + 6):
      for y in range(deck_y + 3, deck_y + 6):
        _set(v, 29, y, z, FIN)

  # Chimneys
  for cx_off in (-2, 2):
    for y in range(deck_y + 6, deck_y + 10):
      _set(v, 27, y, cz + cx_off, STONE)

  # --- INTERIOR DETAIL (cargo + engine) ---
  for x in range(14, 22):
    for z in range(cz - 2, cz + 3):
      _set(v, x, deck_y + 1, z, CHEST if (x + z) % 2 else FURNACE)

  return v


def _set(v: np.ndarray, x: int, y: int, z: int, block: str) -> None:
  if 0 <= x < v.shape[0] and 0 <= y < v.shape[1] and 0 <= z < v.shape[2]:
    v[x, y, z] = block
