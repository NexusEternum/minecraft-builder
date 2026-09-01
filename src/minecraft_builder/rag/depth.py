"""
Adding Depth techniques from the Minecraft Guide to Creative.

Partial blocks and wall techniques that prevent flat, boxy builds.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DepthTechnique:
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


DEPTH_TECHNIQUES: tuple[DepthTechnique, ...] = (
  DepthTechnique(
    id="wall_decoration",
    name="wall decorative features",
    triggers=("wall", "exterior", "facade", "flat", "boxy", "detail", "depth"),
    blocks=(_b("stone_brick_stairs"), _b("stone_brick_slab"), _b("oak_stairs")),
    keywords=("stairs on wall", "slabs on wall", "decorative features"),
    tip="Attach stairs and slabs to flat walls for decorative depth",
  ),
  DepthTechnique(
    id="recessed_blocks",
    name="recessed wall blocks",
    triggers=("wall", "texture", "pattern", "depth", "recessed"),
    blocks=(_b("oak_stairs"), _b("oak_slab"), _b("cobblestone_stairs")),
    keywords=("recessed blocks", "wall texture", "mixed partial blocks"),
    tip="Replace regular wall blocks with stairs and slabs for gaps and thickness",
  ),
  DepthTechnique(
    id="window_sills",
    name="window sills and awnings",
    triggers=("window", "sill", "awning", "shutter"),
    blocks=(_b("oak_slab"), _b("stone_brick_slab"), _b("oak_trapdoor")),
    keywords=("window sill", "awning", "slab above window"),
    tip="Use slabs above and below windows for sills and awnings",
  ),
  DepthTechnique(
    id="roof_brackets",
    name="overhang support brackets",
    triggers=("roof", "overhang", "eave", "bracket", "support"),
    blocks=(_b("oak_stairs"), _b("stone_brick_stairs"), _b("spruce_stairs")),
    keywords=("upside down stairs", "roof bracket", "overhang support"),
    tip="Use upside-down stairs as brackets under roof overhangs",
  ),
  DepthTechnique(
    id="doorstep",
    name="doorstep and door frame",
    triggers=("door", "entrance", "doorway", "porch", "step"),
    blocks=(_b("oak_slab"), _b("stone_brick_stairs"), _b("oak_stairs")),
    keywords=("doorstep", "door frame detail", "entrance steps"),
    tip="Slabs and stairs make doorsteps and decorative areas above door frames",
  ),
  DepthTechnique(
    id="double_wall",
    name="double-thick walls",
    triggers=("wall", "thick", "layered", "industrial", "fortress", "castle"),
    blocks=(_b("stone_bricks"), _b("bricks"), _b("deepslate_bricks")),
    keywords=("double thick wall", "recessed pattern", "layered walls"),
    tip="Make walls two blocks thick and recess the outer layer for depth",
  ),
  DepthTechnique(
    id="glass_panes",
    name="recessed glass panes",
    triggers=("window", "glass", "recessed"),
    blocks=(_b("glass_pane"), _b("iron_bars")),
    keywords=("glass panes", "recessed windows"),
    tip="Glass panes sit mid-wall for a recessed look; blocks sit flush",
  ),
  DepthTechnique(
    id="bay_window",
    name="bay window",
    triggers=("window", "bay", "protruding", "cabin", "cottage"),
    blocks=(_b("glass_pane"), _b("oak_planks"), _b("oak_slab")),
    keywords=("bay window", "window extension"),
    tip="Extend the wall outward and set glass into it for bay-style windows",
  ),
)


def detect_depth_techniques(prompt: str) -> list[DepthTechnique]:
  lower = prompt.lower()
  matched: list[DepthTechnique] = []
  seen: set[str] = set()
  for tech in DEPTH_TECHNIQUES:
    if any(t in lower for t in tech.triggers) and tech.id not in seen:
      matched.append(tech)
      seen.add(tech.id)
  return matched


def depth_keywords(tech: DepthTechnique) -> list[str]:
  blocks = [b.removeprefix("minecraft:").replace("_", " ") for b in tech.blocks[:2]]
  return [tech.name, *list(tech.keywords[:2]), *blocks]
