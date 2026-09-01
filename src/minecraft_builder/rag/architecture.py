"""
Architectural structures from the Minecraft Guide to Creative.

Named decorative/functional features added after the basic framework.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ArchitecturalFeature:
  id: str
  name: str
  aliases: tuple[str, ...]
  blocks: tuple[str, ...]
  tip: str


def _b(name: str) -> str:
  if name.startswith("minecraft:"):
    return name
  return f"minecraft:{name}"


ARCHITECTURAL_FEATURES: tuple[ArchitecturalFeature, ...] = (
  ArchitecturalFeature(
    id="arch",
    name="arch",
    aliases=("arch", "arched", "archway", "arcade"),
    blocks=(_b("stone_brick_stairs"), _b("chiseled_stone_bricks"), _b("glass_pane")),
    tip="Stone brick stairs frame arched doors and windows",
  ),
  ArchitecturalFeature(
    id="balcony",
    name="balcony",
    aliases=("balcony", "terrace", "deck"),
    blocks=(_b("oak_planks"), _b("oak_fence"), _b("glass_pane")),
    tip="Platform extending from wall with fence railings and door access",
  ),
  ArchitecturalFeature(
    id="colonnade",
    name="colonnade",
    aliases=("colonnade", "columns", "pillars", "porch columns", "classical porch"),
    blocks=(_b("quartz_pillar"), _b("quartz_block"), _b("smooth_quartz")),
    tip="Row of columns on a porch or facade for depth",
  ),
  ArchitecturalFeature(
    id="chimney",
    name="chimney",
    aliases=("chimney", "smokestack", "flue", "industrial chimney"),
    blocks=(_b("stone_bricks"), _b("cobblestone"), _b("cobweb")),
    tip="Stone brick chimney with cobwebs at top for smoke effect",
  ),
  ArchitecturalFeature(
    id="cupola",
    name="cupola",
    aliases=("cupola", "belvedere", "roof tower", "ventilation tower"),
    blocks=(_b("quartz_block"), _b("glass_pane"), _b("gold_block")),
    tip="Small tower crowning a roof for ornament or ventilation",
  ),
  ArchitecturalFeature(
    id="bay_window",
    name="bay window",
    aliases=("bay window", "bow window", "protruding window"),
    blocks=(_b("stone_brick_stairs"), _b("glass_pane"), _b("bricks")),
    tip="Window extension protruding from wall with stairs top and bottom",
  ),
  ArchitecturalFeature(
    id="cornice",
    name="cornice",
    aliases=("cornice", "molding", "trim", "eaves detail"),
    blocks=(_b("stone_brick_stairs"),),
    tip="Two upside-down stairs on top corner create a cornice flourish",
  ),
  ArchitecturalFeature(
    id="flying_buttress",
    name="flying buttress",
    aliases=("flying buttress", "buttress", "cathedral support"),
    blocks=(_b("stone_bricks"), _b("stone_brick_stairs"), _b("torch")),
    tip="Arched exterior supports for huge cathedral walls and roofs",
  ),
  ArchitecturalFeature(
    id="gable",
    name="gable",
    aliases=("gable", "gable window", "attic window", "roof pitch"),
    blocks=(_b("stone_bricks"), _b("spruce_stairs"), _b("glass_pane")),
    tip="Triangular wall between roof pitches; windows light attic space",
  ),
  ArchitecturalFeature(
    id="frieze",
    name="frieze",
    aliases=("frieze", "decorative band", "wall band", "classical trim"),
    blocks=(_b("sandstone"), _b("red_sandstone_stairs"), _b("chiseled_sandstone")),
    tip="Decorative horizontal row of blocks breaking up a plain wall",
  ),
  ArchitecturalFeature(
    id="portico",
    name="portico",
    aliases=("portico", "porch", "entrance porch", "covered entrance"),
    blocks=(_b("quartz_block"), _b("oak_planks"), _b("oak_door")),
    tip="Permanent roofed entrance with solid supports and steps",
  ),
  ArchitecturalFeature(
    id="roof_terrace",
    name="roof terrace",
    aliases=("roof terrace", "rooftop garden", "rooftop", "green roof", "parapet"),
    blocks=(_b("bricks"), _b("stone_brick_wall"), _b("grass_block"), _b("oak_fence")),
    tip="Open rooftop space with low parapet walls, often a green garden",
  ),
  ArchitecturalFeature(
    id="spire",
    name="spire",
    aliases=("spire", "steeple", "skyscraper top", "tower top", "church spire"),
    blocks=(_b("quartz_block"), _b("tinted_glass"), _b("redstone_block")),
    tip="Tapered top on churches or skyscrapers; redstone block as warning light",
  ),
)


def detect_architecture(prompt: str) -> list[ArchitecturalFeature]:
  lower = prompt.lower()
  matched: list[tuple[int, ArchitecturalFeature]] = []
  seen: set[str] = set()

  for feature in ARCHITECTURAL_FEATURES:
    for alias in sorted(feature.aliases, key=len, reverse=True):
      if alias in lower and feature.id not in seen:
        matched.append((len(alias), feature))
        seen.add(feature.id)
        break

  matched.sort(key=lambda x: x[0], reverse=True)
  return [f for _, f in matched]


def architecture_keywords(feature: ArchitecturalFeature) -> list[str]:
  blocks = [b.removeprefix("minecraft:").replace("_", " ") for b in feature.blocks[:2]]
  return [feature.name, *blocks]
