"""
Walls, floors, and interior decor from the Minecraft Guide to Creative.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InteriorTechnique:
  id: str
  name: str
  aliases: tuple[str, ...]
  blocks: tuple[str, ...]
  room_types: tuple[str, ...]
  tip: str


@dataclass(frozen=True)
class InteriorDecor:
  id: str
  name: str
  aliases: tuple[str, ...]
  blocks: tuple[str, ...]
  tip: str


def _b(name: str) -> str:
  if name.startswith("minecraft:"):
    return name
  return f"minecraft:{name}"


# Walls & floors (page 44–45)
WALL_FLOOR_TECHNIQUES: tuple[InteriorTechnique, ...] = (
  InteriorTechnique(
    id="area_rug",
    name="area rug",
    aliases=("area rug", "rug", "carpet rug", "living room floor"),
    blocks=(_b("white_carpet"), _b("oak_planks")),
    room_types=("living room", "lounge", "hall"),
    tip="Carpet blocks over wooden floorboards in open living spaces",
  ),
  InteriorTechnique(
    id="wall_carpet",
    name="wall-to-wall carpet",
    aliases=("wall to wall carpet", "bedroom carpet", "carpeted floor", "cozy floor"),
    blocks=(_b("red_carpet"), _b("wool")),
    room_types=("bedroom", "den"),
    tip="Full carpet coverage for cosy bedrooms with bold colour",
  ),
  InteriorTechnique(
    id="partial_wall",
    name="partial wall divider",
    aliases=("open plan", "partial wall", "room divider", "glass divider", "half wall"),
    blocks=(_b("glass_pane"), _b("oak_fence"), _b("iron_bars")),
    room_types=("living room", "study", "library"),
    tip="Glass, fences, or iron bars divide rooms without closing them off",
  ),
  InteriorTechnique(
    id="checkerboard",
    name="checkerboard floor",
    aliases=("checkerboard", "checkered floor", "kitchen floor", "tile floor", "black and white floor"),
    blocks=(_b("quartz_block"), _b("black_concrete")),
    room_types=("kitchen", "hallway", "foyer"),
    tip="Alternating white and black blocks for classic kitchen/hallway tiles",
  ),
  InteriorTechnique(
    id="feature_wall",
    name="feature wall",
    aliases=("feature wall", "accent wall", "coloured wall", "bathroom wall"),
    blocks=(_b("prismarine"), _b("cyan_terracotta"), _b("bricks")),
    room_types=("bathroom", "bedroom", "living room"),
    tip="Add a colourful layer on interior walls over exposed brick or stone",
  ),
  InteriorTechnique(
    id="mosaic_floor",
    name="mosaic tiles",
    aliases=("mosaic", "mosaic floor", "terracotta floor", "foyer floor", "formal floor"),
    blocks=(_b("orange_terracotta"), _b("yellow_terracotta"), _b("green_terracotta"), _b("red_terracotta")),
    room_types=("foyer", "hallway", "entrance"),
    tip="Terracotta blocks arranged as mosaic patterns for formal areas",
  ),
  InteriorTechnique(
    id="double_wall",
    name="double-thick interior walls",
    aliases=("interior wall", "two block wall", "interior design", "wall layer"),
    blocks=(_b("stone_bricks"), _b("bricks"), _b("oak_planks")),
    room_types=(),
    tip="Exterior wall outside, separate interior pattern inside — two blocks thick",
  ),
)

# Room types from the cutaway example
ROOM_TYPES: dict[str, tuple[str, ...]] = {
  "living room": ("living room", "lounge", "sitting room"),
  "bedroom": ("bedroom", "master bedroom", "sleeping"),
  "library": ("library", "study", "bookshelf room"),
  "kitchen": ("kitchen", "cooking"),
  "bathroom": ("bathroom", "washroom", "ensuite"),
  "foyer": ("foyer", "entrance hall", "hallway", "entryway"),
}

# Paintings & item frames (page 46–47)
INTERIOR_DECOR: tuple[InteriorDecor, ...] = (
  InteriorDecor(
    id="paintings",
    name="paintings",
    aliases=("painting", "paintings", "art", "gallery", "museum", "art wall"),
    blocks=(_b("painting"),),
    tip="26 paintings from 1x1 to 4x4 — size depends on wall space",
  ),
  InteriorDecor(
    id="secret_painting",
    name="secret painting door",
    aliases=("secret door", "hidden door", "secret entrance", "hidden passage"),
    blocks=(_b("painting"), _b("oak_door")),
    tip="Place a painting over a 1x2 gap to conceal a secret entrance",
  ),
  InteriorDecor(
    id="item_frames",
    name="item frame displays",
    aliases=("item frame", "item frames", "display", "plinth", "exhibit", "museum display"),
    blocks=(_b("item_frame"), _b("quartz_block")),
    tip="Item frames on walls or quartz plinths for heads, maps, and artefacts",
  ),
  InteriorDecor(
    id="rotated_sign",
    name="rotated arrow sign",
    aliases=("signpost", "arrow sign", "direction sign", "wayfinding"),
    blocks=(_b("item_frame"), _b("arrow")),
    tip="Rotate an arrow in an item frame for a stylish signpost",
  ),
)


def detect_wall_floor(prompt: str) -> list[InteriorTechnique]:
  lower = prompt.lower()
  matched: list[InteriorTechnique] = []
  seen: set[str] = set()

  for tech in WALL_FLOOR_TECHNIQUES:
    if any(a in lower for a in tech.aliases) and tech.id not in seen:
      matched.append(tech)
      seen.add(tech.id)

  # Room type triggers matching techniques
  for room, aliases in ROOM_TYPES.items():
    if any(a in lower for a in aliases):
      for tech in WALL_FLOOR_TECHNIQUES:
        if room in tech.room_types and tech.id not in seen:
          matched.append(tech)
          seen.add(tech.id)

  return matched


def detect_interior_decor(prompt: str) -> list[InteriorDecor]:
  lower = prompt.lower()
  matched: list[InteriorDecor] = []
  seen: set[str] = set()
  for decor in INTERIOR_DECOR:
    if any(a in lower for a in decor.aliases) and decor.id not in seen:
      matched.append(decor)
      seen.add(decor.id)
  return matched


def interior_keywords(tech: InteriorTechnique | InteriorDecor) -> list[str]:
  blocks = [b.removeprefix("minecraft:").replace("_", " ") for b in tech.blocks[:2]]
  return [tech.name, *blocks]
