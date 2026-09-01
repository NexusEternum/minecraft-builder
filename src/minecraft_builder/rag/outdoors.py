"""
Outdoor spaces and landscaping from the Minecraft Guide to Creative.

Feeds scene generation and exterior prompt enrichment.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LandscapeFeature:
  id: str
  name: str
  aliases: tuple[str, ...]
  blocks: tuple[str, ...]
  tip: str


@dataclass(frozen=True)
class TreeDesign:
  id: str
  name: str
  aliases: tuple[str, ...]
  blocks: tuple[str, ...]
  tip: str


@dataclass(frozen=True)
class OutdoorStructure:
  id: str
  name: str
  aliases: tuple[str, ...]
  blocks: tuple[str, ...]
  tip: str


def _b(name: str) -> str:
  if name.startswith("minecraft:"):
    return name
  return f"minecraft:{name}"


# Tree sapling clearance (blocks of air needed above) — reference metadata
TREE_CLEARANCE: dict[str, int] = {
  "oak": 6,
  "birch": 7,
  "jungle": 8,
  "spruce": 8,
  "acacia": 8,
  "dark_oak": 8,
  "giant_jungle": 12,
  "giant_spruce": 16,
}

LANDSCAPE_FEATURES: tuple[LandscapeFeature, ...] = (
  LandscapeFeature("water", "water feature", ("pond", "stream", "fountain", "water feature", "lake", "bridge"), (_b("water"), _b("lily_pad"), _b("oak_planks")), "Ponds, streams, fountains — add bridges and lily pads"),
  LandscapeFeature("fences", "fencing", ("fence", "fences", "garden fence", "enclosure"), (_b("oak_fence"), _b("oak_fence_gate")), "Mark edges and create gated entrances"),
  LandscapeFeature("flowers", "flower beds", ("flowers", "flower bed", "garden flowers", "floral"), (_b("poppy"), _b("dandelion"), _b("cornflower")), "Coloured flower patches in patterns or highlights"),
  LandscapeFeature("hedges", "hedges", ("hedge", "hedges", "topiary", "leaf wall"), (_b("oak_leaves"), _b("birch_leaves")), "Leaf block partitions — flexible geometric shapes"),
  LandscapeFeature("paths", "garden paths", ("path", "pathway", "walkway", "garden path"), (_b("stone_bricks"), _b("gravel")), "Stone and gravel paths connecting garden areas"),
  LandscapeFeature("garden_lighting", "garden lighting", ("garden torch", "path lighting", "outdoor lighting"), (_b("torch"), _b("oak_fence")), "Torches on fence posts along paths"),
)

CUSTOM_TREES: tuple[TreeDesign, ...] = (
  TreeDesign("spherical", "spherical tree", ("spherical tree", "round tree", "topiary tree"), (_b("oak_log"), _b("oak_leaves")), "Log trunk with cuboid leaf sphere — formal gardens"),
  TreeDesign("spooky", "spooky tree", ("spooky tree", "dead tree", "haunted tree", "halloween tree"), (_b("dark_oak_log"), _b("jack_o_lantern")), "Gnarled dark wood branches with jack-o-lanterns"),
  TreeDesign("bonsai", "bonsai tree", ("bonsai", "ornamental tree"), (_b("dark_oak_log"), _b("oak_leaves")), "Thick winding trunk with small leaf clusters at branch ends"),
  TreeDesign("candyfloss", "candyfloss tree", ("candyfloss", "candy tree", "fantasy tree", "pink tree"), (_b("birch_fence"), _b("pink_wool")), "Thin post with pink/purple wool layers as canopy"),
)

OUTDOOR_STRUCTURES: tuple[OutdoorStructure, ...] = (
  OutdoorStructure("gazebo", "gazebo", ("gazebo", "bandstand", "pavilion", "meeting point"), (_b("quartz_block"), _b("quartz_stairs"), _b("oak_planks")), "Elevated deck or circular pavilion for social space"),
  OutdoorStructure("greenhouse", "greenhouse", ("greenhouse", "glass house", "conservatory"), (_b("glass"), _b("oak_planks"), _b("dirt")), "Glass-walled structure for plants"),
  OutdoorStructure("garden_bridge", "garden bridge", ("garden bridge", "wooden bridge", "footbridge"), (_b("oak_planks"), _b("oak_fence")), "Simple bridge over stream or pond"),
  OutdoorStructure("garden_arch", "garden arch", ("garden arch", "wooden arch", "gateway"), (_b("oak_fence"), _b("oak_log")), "Archway gateway between garden sections"),
  OutdoorStructure("hedge_maze", "hedge maze", ("maze", "hedge maze", "labyrinth"), (_b("oak_leaves"), _b("diamond_block")), "Leaf block walls — mark floor route first"),
  OutdoorStructure("domed_temple", "domed garden temple", ("garden temple", "domed structure", "garden shrine"), (_b("quartz_block"), _b("quartz_stairs")), "White circular domed structure with pillars"),
)


def detect_landscape(prompt: str) -> list[LandscapeFeature]:
  lower = prompt.lower()
  return [f for f in LANDSCAPE_FEATURES if any(a in lower for a in f.aliases)]


def detect_custom_trees(prompt: str) -> list[TreeDesign]:
  lower = prompt.lower()
  if "tree" in lower or "garden" in lower or "forest" in lower:
    matched = [t for t in CUSTOM_TREES if any(a in lower for a in t.aliases)]
    if matched:
      return matched
  return []


def detect_outdoor_structures(prompt: str) -> list[OutdoorStructure]:
  lower = prompt.lower()
  matched: list[OutdoorStructure] = []
  seen: set[str] = set()
  for s in OUTDOOR_STRUCTURES:
    if any(a in lower for a in s.aliases) and s.id not in seen:
      matched.append(s)
      seen.add(s.id)
  # Garden/outdoor scene → default features
  if not matched and any(w in lower for w in ("garden", "outdoor", "landscap", "backyard", "yard")):
    return [OUTDOOR_STRUCTURES[0], OUTDOOR_STRUCTURES[2]]  # gazebo + bridge
  return matched


def outdoor_keywords(item: LandscapeFeature | TreeDesign | OutdoorStructure) -> list[str]:
  blocks = [b.removeprefix("minecraft:").replace("_", " ") for b in item.blocks[:2]]
  return [item.name, *blocks]
