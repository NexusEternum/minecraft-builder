"""
Linking Builds — combining multiple structures into scenes.

From the Minecraft Guide to Creative. Enriches multi-building / city prompts
and defines the spec for future multi-region scene generation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LinkingTechnique:
  id: str
  name: str
  triggers: tuple[str, ...]
  blocks: tuple[str, ...]
  keywords: tuple[str, ...]
  tip: str


def _b(name: str) -> str:
  if name.startswith("minecraft:"):
    return name
  return f"minecraft:{name}"


# Prompt phrases that indicate a multi-building scene request
SCENE_TRIGGERS: tuple[str, ...] = (
  "scene",
  "city",
  "town",
  "downtown",
  "urban",
  "district",
  "city block",
  "cityscape",
  "multiple buildings",
  "several buildings",
  "linking builds",
  "bigger build",
  "campus",
  "street",
  "neighborhood",
  "neighbourhood",
  "village scene",
  "town square",
  "plaza",
  "terraced",
  "row houses",
  "skybridge",
  "sky bridge",
  "courtyard",
)

LINKING_TECHNIQUES: tuple[LinkingTechnique, ...] = (
  LinkingTechnique(
    id="infrastructure",
    name="roads and paths",
    triggers=("road", "street", "path", "sidewalk", "pavement", "infrastructure", "city"),
    blocks=(_b("gray_concrete"), _b("stone_slab"), _b("white_concrete")),
    keywords=("road", "sidewalk", "city streets"),
    tip="Simple roads with paths on either side create city-style streets",
  ),
  LinkingTechnique(
    id="level_integration",
    name="stair integration",
    triggers=("staircase", "raised door", "street level", "steps", "plaza entrance"),
    blocks=(_b("stone_brick_stairs"), _b("stone_brick_slab"), _b("cobblestone")),
    keywords=("stairs to street", "raised entrance"),
    tip="Add staircases from raised doors down to street level",
  ),
  LinkingTechnique(
    id="overhang_space",
    name="under-overhang public space",
    triggers=("overhang", "car park", "carpark", "parking", "pilotis", "stilt"),
    blocks=(_b("quartz_pillar"), _b("gray_concrete"), _b("stone_brick_slab")),
    keywords=("under overhang", "public space below", "car park"),
    tip="Use space under a smaller ground floor as public area or car park",
  ),
  LinkingTechnique(
    id="gap_features",
    name="park between buildings",
    triggers=("park", "garden", "fountain", "plaza", "between buildings", "negative space"),
    blocks=(_b("grass_block"), _b("oak_leaves"), _b("water"), _b("stone_brick_slab")),
    keywords=("central park", "pathways", "fountain", "benches"),
    tip="Fill gaps between buildings with parks connected by pathways",
  ),
  LinkingTechnique(
    id="fire_escape",
    name="fire escape",
    triggers=("fire escape", "multi-storey", "multistory", "apartment", "office building"),
    blocks=(_b("iron_bars"), _b("stone_slab"), _b("ladder")),
    keywords=("fire escape", "iron bar balconies", "exterior ladder"),
    tip="Multi-storey buildings get fire escapes from iron bars, slabs, and ladders",
  ),
  LinkingTechnique(
    id="terraced_row",
    name="terraced row houses",
    triggers=("terraced", "row house", "row houses", "townhouse", "adjacent", "no gap"),
    blocks=(_b("bricks"), _b("white_concrete"), _b("glass_pane")),
    keywords=("terraced houses", "buildings touching", "no negative space"),
    tip="Place builds directly next to each other like terraced houses to avoid gaps",
  ),
  LinkingTechnique(
    id="subterranean",
    name="subway entrance",
    triggers=("subway", "underground", "cellar", "basement entrance", "tunnel entrance"),
    blocks=(_b("stone_brick_stairs"), _b("stone_bricks"), _b("iron_bars")),
    keywords=("subway entrance", "cellar stairs", "below street"),
    tip="Use space beneath ground level for subway or cellar entrances",
  ),
  LinkingTechnique(
    id="joining_arch",
    name="arch between buildings",
    triggers=("arch between", "joining arch", "connect buildings", "archway link"),
    blocks=(_b("stone_brick_stairs"), _b("chiseled_stone_bricks"), _b("stone_bricks")),
    keywords=("decorative arch", "arch between buildings"),
    tip="Fill the gap between two buildings with a decorative arch",
  ),
  LinkingTechnique(
    id="skybridge",
    name="skybridge overpass",
    triggers=("skybridge", "sky bridge", "overpass", "walkway between", "aerial bridge"),
    blocks=(_b("quartz_block"), _b("glass_pane"), _b("iron_bars")),
    keywords=("skybridge", "overpass", "walkway between towers"),
    tip="Turn an arch into a wide overpass or skybridge between tall buildings",
  ),
  LinkingTechnique(
    id="courtyard",
    name="decorative courtyard",
    triggers=("courtyard", "plaza garden", "empty space", "decorative garden", "atrium"),
    blocks=(_b("quartz_block"), _b("water"), _b("stone_brick_slab"), _b("oak_leaves")),
    keywords=("decorative courtyard", "purposeful empty space", "plaza fountain"),
    tip="When gaps remain, make them deliberate decorative gardens or courtyards",
  ),
)


def is_scene_request(prompt: str) -> bool:
  lower = prompt.lower()
  return any(t in lower for t in SCENE_TRIGGERS)


def detect_linking_techniques(prompt: str) -> list[LinkingTechnique]:
  lower = prompt.lower()
  matched: list[LinkingTechnique] = []
  seen: set[str] = set()

  # Scene requests activate all linking techniques as general guidance
  if is_scene_request(prompt):
    return list(LINKING_TECHNIQUES)

  for tech in LINKING_TECHNIQUES:
    if any(t in lower for t in tech.triggers) and tech.id not in seen:
      matched.append(tech)
      seen.add(tech.id)
  return matched


def linking_keywords(prompt: str) -> list[str]:
  kws: list[str] = []
  seen: set[str] = set()
  for tech in detect_linking_techniques(prompt):
    for word in (tech.name, *tech.keywords[:2]):
      if word not in seen:
        kws.append(word)
        seen.add(word)
    for block in tech.blocks[:1]:
      name = block.removeprefix("minecraft:").replace("_", " ")
      if name not in seen:
        kws.append(name)
        seen.add(name)
  return kws
