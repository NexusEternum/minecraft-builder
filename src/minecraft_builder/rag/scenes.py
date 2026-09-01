"""
Scene generation — FUTURE ADVANCED FEATURE.

A scene combines structures + terrain + linking infrastructure:
  - One or more building regions
  - Roads, parks, paths between them (linking builds)
  - Biome-matched terrain

Current model (v0.1): single structure, 32³ voxel grid.
Scene model (planned): multi-region .litematic output.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .biomes import BiomeGuide, detect_biome
from .linking import LINKING_TECHNIQUES, is_scene_request, linking_keywords
from .natural_features import NaturalFeature, detect_features


@dataclass
class SceneSpec:
  """Describes a build request that may need multiple structures + land."""

  structure_prompt: str
  biome: BiomeGuide | None
  natural_features: list[NaturalFeature] = field(default_factory=list)
  is_multi_building: bool = False
  linking_keywords: list[str] = field(default_factory=list)
  include_terrain: bool = False
  terrain_radius: int = 32  # blocks around scene (future)
  building_count: int = 1  # future: parse "3 buildings" from prompt


def parse_scene_prompt(prompt: str) -> SceneSpec:
  lower = prompt.lower()
  multi = is_scene_request(prompt)
  features = detect_features(prompt)
  biome = detect_biome(prompt)

  include_terrain = multi or any(
    phrase in lower
    for phrase in (
      "with terrain", "with land", "landscap", "surroundings", "setting", "park", "road"
    )
  )

  # Rough building count from prompt
  count = 1
  for word in ("two", "three", "four", "five", "several", "multiple"):
    if word in lower:
      count = {"two": 2, "three": 3, "four": 4, "five": 5}.get(word, 3)
      break

  return SceneSpec(
    structure_prompt=prompt,
    biome=biome,
    natural_features=features,
    is_multi_building=multi,
    linking_keywords=linking_keywords(prompt) if multi else [],
    include_terrain=include_terrain or bool(features),
    building_count=count if multi else 1,
  )


def scene_available() -> bool:
  """Multi-region scene generation not yet implemented."""
  return False
