"""
Beginner build tips from "Before You Begin" and "Beginner's Build Tips".

Lightweight prompt enrichment — not procedural rules.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BuildTip:
  id: str
  name: str
  triggers: tuple[str, ...]
  keywords: tuple[str, ...]
  advice: str


BUILD_TIPS: tuple[BuildTip, ...] = (
  BuildTip(
    id="inspiration",
    name="themed inspiration",
    triggers=("inspired", "inspiration", "based on", "style of", "themed"),
    keywords=("detailed", "themed", "authentic"),
    advice="Research real-world references for authentic themed builds",
  ),
  BuildTip(
    id="location",
    name="environment fit",
    triggers=("location", "setting", "environment", "fits", "surroundings"),
    keywords=("environment fit", "complementary setting"),
    advice="Match the build to its environment so it doesn't look out of place",
  ),
  BuildTip(
    id="depth_detail",
    name="depth and detail",
    triggers=("flat", "boxy", "simple", "basic", "wall", "house", "building"),
    keywords=("depth", "slabs", "stairs", "recessed", "detail"),
    advice="Use slabs and stairs instead of full blocks for depth in walls and floors",
  ),
  BuildTip(
    id="outside_box",
    name="creative block use",
    triggers=("creative", "unique", "detail", "furniture", "decor"),
    keywords=("stairs roof", "trapdoor windows", "fence table"),
    advice="Use blocks for unintended purposes — stairs for roofs, trapdoors for shutters",
  ),
  BuildTip(
    id="biome_choice",
    name="biome preparation",
    triggers=("biome", "where to build", "terrain", "land"),
    keywords=("biome matched", "cleared terrain"),
    advice="Choose a biome that suits your build — plains are easy, forests need clearing",
  ),
)


def detect_tips(prompt: str) -> list[BuildTip]:
  lower = prompt.lower()
  matched: list[BuildTip] = []
  seen: set[str] = set()
  for tip in BUILD_TIPS:
    if any(t in lower for t in tip.triggers) and tip.id not in seen:
      matched.append(tip)
      seen.add(tip.id)
  return matched
