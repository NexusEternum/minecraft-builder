"""
Interior furnishing module.

Places furniture from book hack recipes into hollow air regions of a voxel grid.
No ML required — works as a post-processing step after exterior generation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from ..data.palette import AIR, BlockPalette
from ..rag.furniture import FURNITURE_HACKS, FurnitureHack


class RoomType(str, Enum):
  LIVING = "living room"
  BEDROOM = "bedroom"
  KITCHEN = "kitchen"
  BATHROOM = "bathroom"
  WORKSHOP = "workshop"
  OFFICE = "office"
  GENERIC = "room"


# Default furniture sets per room type (matches book themed rooms + furniture hacks)
ROOM_FURNITURE: dict[RoomType, list[str]] = {
  RoomType.LIVING: ["sofa", "chair", "fireplace", "tv", "small_table"],
  RoomType.BEDROOM: ["four_poster", "wardrobe", "wall_carpet"],
  RoomType.KITCHEN: ["fridge", "stove", "family_table", "shelves"],
  RoomType.BATHROOM: ["toilet", "sink", "bath", "mirror"],
  RoomType.WORKSHOP: ["shelves"],  # utility blocks placed separately
  RoomType.OFFICE: ["computer", "shelves", "chair"],
  RoomType.GENERIC: ["chair", "small_table"],
}

# Minecraft utility blocks for workshop/rustic rooms
WORKSHOP_BLOCKS = (
  "minecraft:crafting_table",
  "minecraft:furnace",
  "minecraft:anvil",
  "minecraft:chest",
)


@dataclass
class PlacedBlock:
  x: int
  y: int
  z: int
  block_id: str


@dataclass
class FurnishResult:
  blocks: list[PlacedBlock]
  room_type: RoomType
  origin: tuple[int, int, int]
  size: tuple[int, int, int]


class InteriorFurnisher:
  """
  Detects interior air pockets and places furniture block-by-block.

  Usage:
    furnisher = InteriorFurnisher(palette)
    results = furnisher.furnish(voxel_indices, room_type=RoomType.LIVING)
  """

  def __init__(self, palette: BlockPalette):
    self.palette = palette
    self._hack_map = {h.id: h for h in FURNITURE_HACKS}

  def furnish(
    self,
    voxels: np.ndarray,
    room_type: RoomType | str = RoomType.GENERIC,
    max_rooms: int = 3,
  ) -> list[FurnishResult]:
    """Find hollow regions and furnish up to max_rooms of them."""
    if isinstance(room_type, str):
      room_type = RoomType(room_type) if room_type in RoomType._value2member_map_ else RoomType.GENERIC

    rooms = find_interior_rooms(voxels, max_rooms=max_rooms)
    results: list[FurnishResult] = []

    for origin, size in rooms:
      placed = self._furnish_room(origin, size, room_type, voxels)
      if placed:
        results.append(FurnishResult(placed, room_type, origin, size))

    return results

  def apply(self, voxels: np.ndarray, results: list[FurnishResult]) -> np.ndarray:
    """Write placed furniture blocks back into voxel array."""
    out = voxels.copy()
    for result in results:
      for pb in result.blocks:
        if self._is_air(out, pb.x, pb.y, pb.z):
          out[pb.x, pb.y, pb.z] = self.palette.encode(pb.block_id)
    return out

  def _furnish_room(
    self,
    origin: tuple[int, int, int],
    size: tuple[int, int, int],
    room_type: RoomType,
    voxels: np.ndarray,
  ) -> list[PlacedBlock]:
    ox, oy, oz = origin
    w, h, d = size
    if w < 3 or d < 3 or h < 3:
      return []

    placed: list[PlacedBlock] = []
    floor_y = oy  # bottom of room air space

    hack_ids = ROOM_FURNITURE.get(room_type, ROOM_FURNITURE[RoomType.GENERIC])
    cx, cz = ox + w // 2, oz + d // 2

    for i, hack_id in enumerate(hack_ids[:4]):
      hack = self._hack_map.get(hack_id)
      if not hack:
        continue
      # Stagger placements across the floor
      px = ox + 1 + (i % 2) * max(1, w - 3)
      pz = oz + 1 + (i // 2) * max(1, d - 3)
      py = floor_y
      if self._can_place(voxels, px, py, pz):
        placed.extend(self._place_hack(hack, px, py, pz))

    # Workshop extras: crafting table, furnace, anvil
    if room_type == RoomType.WORKSHOP:
      utilities = [
        (ox + 1, floor_y, oz + 1, "minecraft:crafting_table"),
        (ox + w - 2, floor_y, oz + 1, "minecraft:furnace"),
        (ox + w - 2, floor_y, oz + d - 2, "minecraft:anvil"),
        (ox + 1, floor_y, oz + d - 2, "minecraft:chest"),
      ]
      for x, y, z, bid in utilities:
        if self._can_place(voxels, x, y, z):
          placed.append(PlacedBlock(x, y, z, bid))

    # Living room: bed in bedroom corner
    if room_type == RoomType.BEDROOM:
      bx, bz = ox + w - 2, oz + d - 2
      if self._can_place(voxels, bx, floor_y, bz):
        placed.append(PlacedBlock(bx, floor_y, bz, "minecraft:red_bed"))

    # Fireplace on back wall
    if room_type in (RoomType.LIVING, RoomType.WORKSHOP):
      fx, fz = cx, oz + d - 2
      if self._can_place(voxels, fx, floor_y, fz):
        placed.extend([
          PlacedBlock(fx, floor_y, fz, "minecraft:cobblestone"),
          PlacedBlock(fx, floor_y + 1, fz, "minecraft:netherrack"),
        ])

    return placed

  def _place_hack(self, hack: FurnitureHack, x: int, y: int, z: int) -> list[PlacedBlock]:
    """Place primary block(s) from a furniture hack at position."""
    blocks = []
    for i, block in enumerate(hack.blocks[:2]):
      blocks.append(PlacedBlock(x + i, y, z, block))
    return blocks

  def _can_place(self, voxels: np.ndarray, x: int, y: int, z: int) -> bool:
    return self._is_air(voxels, x, y, z)

  def _is_air(self, voxels: np.ndarray, x: int, y: int, z: int) -> bool:
    if not (0 <= x < voxels.shape[0] and 0 <= y < voxels.shape[1] and 0 <= z < voxels.shape[2]):
      return False
    return int(voxels[x, y, z]) == 0


def find_interior_rooms(
  voxels: np.ndarray,
  max_rooms: int = 3,
  min_size: int = 3,
) -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
  """
  Find axis-aligned air regions surrounded by non-air blocks.
  Returns list of (origin, size) for each detected room.
  """
  shape = voxels.shape
  visited = np.zeros(shape, dtype=bool)
  rooms: list[tuple[tuple[int, int, int], tuple[int, int, int], int]] = []

  for x in range(shape[0]):
    for y in range(shape[1]):
      for z in range(shape[2]):
        if int(voxels[x, y, z]) != 0 or visited[x, y, z]:
          continue
        # Flood-fill this air component
        component = _flood_air(voxels, visited, x, y, z)
        if len(component) < min_size ** 2:
          continue
        xs = [p[0] for p in component]
        ys = [p[1] for p in component]
        zs = [p[2] for p in component]
        origin = (min(xs), min(ys), min(zs))
        size = (max(xs) - min(xs) + 1, max(ys) - min(ys) + 1, max(zs) - min(zs) + 1)
        # Only count as interior if surrounded on most sides
        if _is_enclosed(voxels, origin, size):
          rooms.append((origin, size, len(component)))

  rooms.sort(key=lambda r: r[2], reverse=True)
  return [(r[0], r[1]) for r in rooms[:max_rooms]]


def _flood_air(voxels, visited, sx, sy, sz) -> list[tuple[int, int, int]]:
  shape = voxels.shape
  stack = [(sx, sy, sz)]
  component = []
  while stack:
    x, y, z = stack.pop()
    if not (0 <= x < shape[0] and 0 <= y < shape[1] and 0 <= z < shape[2]):
      continue
    if visited[x, y, z] or int(voxels[x, y, z]) != 0:
      continue
    visited[x, y, z] = True
    component.append((x, y, z))
    for dx, dy, dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
      stack.append((x+dx, y+dy, z+dz))
  return component


def _is_enclosed(voxels, origin, size) -> bool:
  """Heuristic: room has solid blocks on at least 3 of 4 horizontal sides."""
  ox, oy, oz = origin
  w, h, d = size
  shape = voxels.shape
  solid_sides = 0
  for side_check in [
    [(ox - 1, oy + dy, oz + dz) for dy in range(h) for dz in range(d)],  # -x
    [(ox + w, oy + dy, oz + dz) for dy in range(h) for dz in range(d)],   # +x
    [(ox + dx, oy + dy, oz - 1) for dx in range(w) for dy in range(h)],   # -z
    [(ox + dx, oy + dy, oz + d) for dx in range(w) for dy in range(h)],   # +z
  ]:
    solids = sum(
      1 for pos in side_check
      if all(0 <= pos[i] < shape[i] for i in range(3)) and int(voxels[pos]) != 0
    )
    if solids > len(side_check) * 0.3:
      solid_sides += 1
  return solid_sides >= 2
