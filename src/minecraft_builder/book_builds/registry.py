"""
Catalog of builds from the Minecraft Guide to Creative.

Use for: training captions, blueprint templates, validation targets.
If you recreate a build as .litematic, drop it in data/book_builds/ with matching id.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BuildZone:
  name: str
  size: tuple[int, int, int]  # width, height, depth
  materials: tuple[str, ...]
  features: tuple[str, ...]
  interior: tuple[str, ...] = ()


@dataclass(frozen=True)
class BookBuild:
  id: str
  name: str
  theme: str
  biome: str
  caption: str  # for training data
  palette: tuple[str, ...]
  zones: tuple[BuildZone, ...]
  exterior_features: tuple[str, ...]
  tips: tuple[str, ...] = ()


BOOK_BUILDS: dict[str, BookBuild] = {
  "remote_outpost": BookBuild(
    id="remote_outpost",
    name="Remote Outpost",
    theme="rustic",
    biome="extreme_hills",
    caption=(
      "a remote outpost with a two-story dark oak house and tall cobblestone turret "
      "on a mountain, diorite and mossy cobblestone, enclosed courtyard with well"
    ),
    palette=(
      "minecraft:diorite",
      "minecraft:cobblestone",
      "minecraft:mossy_cobblestone",
      "minecraft:dark_oak_planks",
      "minecraft:dark_oak_log",
      "minecraft:blue_wool",
      "minecraft:yellow_wool",
    ),
    zones=(
      BuildZone(
        name="workshop ground floor",
        size=(7, 10, 7),
        materials=("dark_oak_planks", "dark_oak_log", "diorite", "cobblestone"),
        features=("gabled roof", "dark oak stairs", "ground floor door"),
        interior=("crafting table", "furnace", "anvil", "fireplace", "blue carpet"),
      ),
      BuildZone(
        name="watchtower",
        size=(9, 20, 9),
        materials=("cobblestone", "mossy_cobblestone", "stone_bricks"),
        features=("arrow slits", "spiral staircase", "rooftop lookout", "trapdoor"),
        interior=("spiral stairs", "ladder", "tower landings"),
      ),
      BuildZone(
        name="bedroom",
        size=(7, 4, 7),
        materials=("dark_oak_planks",),
        features=("upper floor of house",),
        interior=("red bed", "chest", "chair", "table", "blue carpet", "torch"),
      ),
    ),
    exterior_features=(
      "checkered wool flag on cobblestone wall pole",
      "glowstone lamp post with trapdoors",
      "cobblestone wall enclosed courtyard",
      "well with trapdoor cover",
      "small oak tree",
      "ground torches",
    ),
    tips=(
      "Offset wool flag blocks at different depths for a billowing effect",
      "Tower has no ground-level entrance — access from house only",
      "Minimal torch lighting to stay hidden at night",
    ),
  ),
  "lighting_system_house": BookBuild(
    id="lighting_system_house",
    name="Lighting System House",
    theme="rustic",
    biome="plains",
    caption=(
      "a two-room house with hidden redstone ceiling lighting, stone brick inner walls, "
      "oak log exterior, dark oak stair roof with attic wiring space, lever-controlled lamps"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:oak_planks",
      "minecraft:oak_log",
      "minecraft:dark_oak_stairs",
      "minecraft:redstone_lamp",
      "minecraft:redstone_dust",
      "minecraft:lever",
      "minecraft:gray_concrete",
    ),
    zones=(
      BuildZone(
        name="kitchen dining room",
        size=(10, 5, 8),
        materials=("stone_bricks", "oak_planks", "spruce_planks"),
        features=("two rooms", "double wall gap", "kitchen", "dining area"),
        interior=("furnace", "cauldron", "chest", "crafting table", "floor redstone lamps"),
      ),
      BuildZone(
        name="bedroom",
        size=(10, 4, 8),
        materials=("gray_concrete", "oak_planks"),
        features=("bedroom", "attic redstone space", "daylight sensor roof"),
        interior=("red bed", "double chest", "automatic ceiling lamps", "paintings"),
      ),
    ),
    exterior_features=(
      "oak plank walls with oak log corners",
      "dark oak stair gabled roof",
      "glass windows",
      "security lamp on fence post at entrance",
      "oak door",
    ),
    tips=(
      "Build inner stone wall + outer oak wall with 1-block gap for redstone",
      "Torch tower carries lever signal vertically to ceiling lamp grid",
      "Attic space above ceiling hides redstone dust runs",
      "Redstone torch under each lamp is simpler than dust circuits",
    ),
  ),
  "exotic_villa": BookBuild(
    id="exotic_villa",
    name="Exotic Villa",
    theme="classical",
    biome="mesa",
    caption=(
      "a mediterranean exotic villa with white quartz colonnades and sandstone tiered roofs, "
      "blue stained glass shutter windows, dark oak balcony railings, swimming pool and "
      "outdoor lounge, mezzanine floor, grand piano living room and luxurious bedroom"
    ),
    palette=(
      "minecraft:quartz_block",
      "minecraft:quartz_pillar",
      "minecraft:chiseled_quartz_block",
      "minecraft:smooth_sandstone",
      "minecraft:smooth_sandstone_slab",
      "minecraft:light_blue_stained_glass_pane",
      "minecraft:dark_oak_fence",
      "minecraft:birch_planks",
      "minecraft:red_sand",
      "minecraft:terracotta",
      "minecraft:water",
    ),
    zones=(
      BuildZone(
        name="living room",
        size=(17, 6, 10),
        materials=("quartz_block", "quartz_pillar", "smooth_sandstone", "birch_planks"),
        features=("colonnade", "arched doorways", "open living area", "bathroom"),
        interior=("grand piano", "white couch", "fireplace", "swimming pool access", "bathroom tiles"),
      ),
      BuildZone(
        name="mezzanine kitchen",
        size=(9, 3, 8),
        materials=("quartz_block", "birch_planks"),
        features=("utility kitchen", "overlooking living area", "compact stair access"),
        interior=("furnace", "crafting table", "chest"),
      ),
      BuildZone(
        name="bedroom",
        size=(9, 4, 9),
        materials=("quartz_block", "smooth_sandstone_slab"),
        features=("balconies", "shuttered windows", "tiered roof"),
        interior=("four-poster bed", "wardrobe", "double chest", "automatic ceiling lamps"),
      ),
      BuildZone(
        name="roof tower",
        size=(4, 5, 10),
        materials=("quartz_block", "chiseled_quartz_block"),
        features=("central tower", "stepped sandstone roof", "daylight sensor lighting"),
        interior=(),
      ),
    ),
    exterior_features=(
      "white monochromatic quartz facade",
      "ground floor colonnade with quartz pillars",
      "tiered smooth sandstone flat roofs",
      "blue stained glass shutter windows",
      "dark oak fence balcony railings",
      "rectangular swimming pool with stone slab surround",
      "outdoor lounge with dark oak seating",
      "mesa red sand and terracotta terrain",
      "birch trees and leaf landscaping",
      "low stone retaining wall",
    ),
    tips=(
      "Monochromatic white palette — any accent color stands out dramatically",
      "Colonnades add depth; chiseled quartz pillars mimic classical columns",
      "Tiered sandstone slab roofs create shallow pyramid caps",
      "Mezzanine between ground and first floor maximizes vertical space",
      "Inverted daylight sensors on roof auto-toggle ceiling lamps at night",
      "Build on mesa biome peak for mediterranean hot-climate feel",
    ),
  ),
  "ocean_observatory": BookBuild(
    id="ocean_observatory",
    name="Ocean Observatory",
    theme="industrial",
    biome="ocean",
    caption=(
      "an ocean observatory with underwater glass dome, white iron central shaft, "
      "surface docking platform with helipad crane and antenna, industrial stone "
      "and quartz, bunk beds research station and ice specimen tanks"
    ),
    palette=(
      "minecraft:glass",
      "minecraft:light_blue_stained_glass",
      "minecraft:quartz_block",
      "minecraft:iron_block",
      "minecraft:stone_bricks",
      "minecraft:polished_andesite",
      "minecraft:water",
      "minecraft:prismarine",
      "minecraft:glowstone",
      "minecraft:acacia_planks",
    ),
    zones=(
      BuildZone(
        name="underwater living dome",
        size=(14, 8, 14),
        materials=("glass", "iron_block", "stone_bricks", "polished_andesite"),
        features=("glass hemisphere", "flying buttresses", "open-plan interior"),
        interior=("bunk beds", "research computers", "botanical garden", "pool table", "chests"),
      ),
      BuildZone(
        name="elevator shaft",
        size=(4, 10, 4),
        materials=("quartz_block", "iron_block", "light_blue_stained_glass"),
        features=("vertical shaft", "glass windows", "ladder transport"),
        interior=("ladder", "specimen ice tanks"),
      ),
      BuildZone(
        name="docking platform",
        size=(11, 3, 11),
        materials=("stone_bricks", "polished_andesite", "iron_bars"),
        features=("docking port", "helipad", "crane", "communication mast"),
        interior=("chests", "crafting table", "cargo loading area"),
      ),
    ),
    exterior_features=(
      "hemispherical glass dome on ocean floor",
      "iron and stone foundation ring",
      "white quartz flying buttresses",
      "vertical blue glass window shaft",
      "stone brick surface platform above water",
      "circular helipad with H marking",
      "acacia wood crane with glowstone light",
      "iron bar antenna with redstone tip",
      "glowstone under-platform sea lighting",
      "deep ocean water surrounding structure",
    ),
    tips=(
      "Build at ocean biome edge so land resources stay accessible",
      "Use glass blocks not panes — easier to shape the dome hemisphere",
      "Stack concentric circles 7→7→6→5→4→3 for dome curvature",
      "Flying buttresses and internal columns suggest deep-sea strength",
      "Open-plan dome interior maximizes observation space",
      "Shaft houses vertical transport between dome and surface port",
    ),
  ),
  "steampunk_airship": BookBuild(
    id="steampunk_airship",
    name="Steampunk Airship",
    theme="steampunk",
    biome="end",
    caption=(
      "a steampunk airship with green and orange striped balloon envelope, dark oak ship "
      "hull with mechanical cogs, glowstone lanterns, engine room furnaces, galley kitchen "
      "and cargo storage, quartz stern propulsion fins"
    ),
    palette=(
      "minecraft:green_wool",
      "minecraft:orange_wool",
      "minecraft:brown_wool",
      "minecraft:dark_oak_planks",
      "minecraft:dark_oak_stairs",
      "minecraft:dark_oak_fence",
      "minecraft:dark_oak_trapdoor",
      "minecraft:glowstone",
      "minecraft:quartz_block",
      "minecraft:stone_bricks",
      "minecraft:cobblestone_wall",
      "minecraft:light_blue_stained_glass",
    ),
    zones=(
      BuildZone(
        name="balloon envelope",
        size=(24, 11, 11),
        materials=("green_wool", "orange_wool", "brown_wool", "dark_oak_trapdoor"),
        features=("elongated ovoid envelope", "vertical stripes", "horizontal rigging bands"),
        interior=(),
      ),
      BuildZone(
        name="main deck",
        size=(32, 6, 13),
        materials=("dark_oak_planks", "dark_oak_stairs", "dark_oak_fence"),
        features=("tapered prow", "deck railings", "mechanical cog decoration"),
        interior=("industrial piston flooring", "glowstone lanterns"),
      ),
      BuildZone(
        name="bridge stern castle",
        size=(9, 5, 7),
        materials=("dark_oak_planks", "quartz_block", "glass_pane"),
        features=("raised bridge", "bay windows", "short spires", "white staircase"),
        interior=("grandfather clock", "maps", "banners"),
      ),
      BuildZone(
        name="engine room cargo hold",
        size=(28, 4, 11),
        materials=("dark_oak_planks", "spruce_planks", "stone_bricks"),
        features=("inverted triangular keel", "cargo hold", "engine room"),
        interior=("furnaces", "chests", "shulker boxes", "galley kitchen"),
      ),
    ),
    exterior_features=(
      "green and orange striped wool balloon",
      "dark oak horizontal rigging straps with trapdoors",
      "fence post suspension rigging to hull",
      "tapered wooden ship prow",
      "mechanical cog decorations on hull sides",
      "glowstone lantern posts on deck",
      "quartz and cobblestone stern chimneys and rudders",
      "light blue stained glass propulsion fins",
      "raised stern castle with bay windows",
    ),
    tips=(
      "Triadic palette: green balloon, brown rigging, dark oak hull",
      "Duplicate widest balloon circle along length to elongate the envelope",
      "Suspend balloon 2-3 blocks above deck on fence post rigging",
      "Piston heads sideways create industrial grid flooring",
      "Pack engine room with furnaces for cramped steam-power feel",
      "Ideal landscape: End City biome for sci-fi floating aesthetic",
    ),
  ),
}


def get_build(build_id: str) -> BookBuild:
  if build_id not in BOOK_BUILDS:
    raise KeyError(f"Unknown book build: {build_id}. Available: {list(BOOK_BUILDS)}")
  return BOOK_BUILDS[build_id]


def match_build(prompt: str) -> BookBuild | None:
  lower = prompt.lower()
  for build in BOOK_BUILDS.values():
    if build.id.replace("_", " ") in lower or build.name.lower() in lower:
      return build
  # Fuzzy matches
  if any(w in lower for w in ("outpost", "watchtower", "turret")) and "remote" in lower:
    return BOOK_BUILDS["remote_outpost"]
  if any(w in lower for w in ("lighting system", "redstone light", "hidden lighting")):
    return BOOK_BUILDS.get("lighting_system_house")
  if any(w in lower for w in ("exotic villa", "mediterranean villa", "classical villa")):
    return BOOK_BUILDS.get("exotic_villa")
  if "villa" in lower and any(w in lower for w in ("exotic", "mediterranean", "quartz", "colonnade")):
    return BOOK_BUILDS.get("exotic_villa")
  if any(w in lower for w in ("ocean observatory", "underwater observatory", "glass dome observatory")):
    return BOOK_BUILDS.get("ocean_observatory")
  if "observatory" in lower and any(w in lower for w in ("ocean", "underwater", "sea", "glass dome")):
    return BOOK_BUILDS.get("ocean_observatory")
  if any(w in lower for w in ("steampunk airship", "steam airship", "sky ship")):
    return BOOK_BUILDS.get("steampunk_airship")
  if "airship" in lower or ("steampunk" in lower and any(w in lower for w in ("ship", "balloon", "dirigible"))):
    return BOOK_BUILDS.get("steampunk_airship")
  return None


def _zone_room_line(zone: BuildZone) -> str | None:
  """Format a zone as 'room name: furniture, blocks, ...' for training captions."""
  label = zone.name.replace("_", " ")
  if zone.interior:
    return f"{label}: {', '.join(zone.interior)}"
  if zone.features:
    return f"{label}: {', '.join(zone.features[:4])}"
  return None


def build_caption(build: BookBuild) -> str:
  """Rich training caption: description + palette + exterior + named rooms."""
  blocks = ", ".join(
    p.removeprefix("minecraft:").replace("_", " ")
    for p in build.palette[:10]
  )
  features = ", ".join(build.exterior_features[:4])

  room_lines = [line for z in build.zones if (line := _zone_room_line(z))]

  parts = [build.caption.rstrip(".")]
  if blocks:
    parts.append(blocks)
  if features:
    parts.append(features)
  if room_lines:
    parts.append("; ".join(room_lines))
  return ", ".join(parts)


# Merge bite-sized builds as they are added from book photos
from .bite_sized_registry import BITE_SIZED_BUILDS  # noqa: E402
from .bite_sized_combinations import COMBINATION_BOOK_BUILDS  # noqa: E402
from .exploded_fortress_registry import FORTRESS_BUILDS  # noqa: E402
from .epic_inventions_registry import EPIC_INVENTIONS_BUILDS  # noqa: E402
from .epic_builds_registry import EPIC_BUILDS  # noqa: E402
from .epic_bases_registry import EPIC_BASES  # noqa: E402

BOOK_BUILDS.update(BITE_SIZED_BUILDS)
BOOK_BUILDS.update(COMBINATION_BOOK_BUILDS)
BOOK_BUILDS.update(FORTRESS_BUILDS)
BOOK_BUILDS.update(EPIC_INVENTIONS_BUILDS)
BOOK_BUILDS.update(EPIC_BUILDS)
BOOK_BUILDS.update(EPIC_BASES)
