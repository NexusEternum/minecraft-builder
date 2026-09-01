"""
Build framework from the Minecraft Guide to Creative.

The 7-step process for constructing a building from foundation to landscaping.
Used for prompt enrichment and as a blueprint for future procedural generation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BuildStep:
  step: int
  name: str
  triggers: tuple[str, ...]
  blocks: tuple[str, ...]
  instruction: str


@dataclass(frozen=True)
class FrameworkPalette:
  name: str
  blocks: tuple[str, ...]


def _b(name: str) -> str:
  if name.startswith("minecraft:"):
    return name
  return f"minecraft:{name}"


# Example palette from the book's L-shaped house tutorial
DEFAULT_FRAMEWORK_PALETTE = FrameworkPalette(
  name="oak cottage",
  blocks=(
    _b("cobblestone"),
    _b("oak_planks"),
    _b("dark_oak_log"),
    _b("dark_oak_stairs"),
    _b("glass_pane"),
    _b("oak_door"),
  ),
)


BUILD_STEPS: tuple[BuildStep, ...] = (
  BuildStep(
    step=1,
    name="foundation",
    triggers=("foundation", "base", "start", "begin", "layout", "footprint"),
    blocks=(_b("cobblestone"),),
    instruction="Mark the base with cobblestone and place doors in desired locations",
  ),
  BuildStep(
    step=2,
    name="ground floor frame",
    triggers=("ground floor", "first floor", "frame", "framework", "pillars"),
    blocks=(_b("dark_oak_log"), _b("oak_planks")),
    instruction="Build corner pillars up, fill floors, leave space for stairs",
  ),
  BuildStep(
    step=3,
    name="upper floor frame",
    triggers=("second floor", "upper floor", "overhang", "expand", "story"),
    blocks=(_b("dark_oak_log"), _b("oak_planks")),
    instruction="Extend corner pillars; optionally overhang the upper floor outward",
  ),
  BuildStep(
    step=4,
    name="walls and windows",
    triggers=("wall", "window", "exterior"),
    blocks=(_b("oak_planks"), _b("glass_pane")),
    instruction="Fill walls with planks, leave gaps for windows",
  ),
  BuildStep(
    step=5,
    name="windows and roof scaffold",
    triggers=("roof", "scaffold", "glass"),
    blocks=(_b("glass_pane"), _b("dirt")),
    instruction="Add glass panes; use temporary dirt blocks as roof scaffolding",
  ),
  BuildStep(
    step=6,
    name="roof",
    triggers=("roof", "stairs", "gable", "eave", "overhang"),
    blocks=(_b("dark_oak_stairs"),),
    instruction="Place stairs on bottom half of scaffold blocks; add eave overhangs",
  ),
  BuildStep(
    step=7,
    name="landscaping",
    triggers=("landscap", "garden", "path", "scene", "surroundings", "yard"),
    blocks=(_b("cobblestone"), _b("torch"), _b("oak_leaves"), _b("short_grass")),
    instruction="Add paths, torches, flower beds, trees around the build",
  ),
)


def detect_framework_steps(prompt: str) -> list[BuildStep]:
  lower = prompt.lower()
  matched: list[BuildStep] = []
  seen: set[int] = set()
  for step in BUILD_STEPS:
    if any(t in lower for t in step.triggers) and step.step not in seen:
      matched.append(step)
      seen.add(step.step)
  return matched


def framework_keywords(prompt: str) -> list[str]:
  """Keywords from matched build steps + default palette."""
  lower = prompt.lower()
  kws: list[str] = []
  seen: set[str] = set()

  # Whole-house / framework prompts get the tutorial palette
  house_words = ("house", "cottage", "home", "building", "l-shaped", "two story", "two-story")
  if any(w in lower for w in house_words):
    for block in DEFAULT_FRAMEWORK_PALETTE.blocks:
      name = block.removeprefix("minecraft:").replace("_", " ")
      if name not in seen:
        kws.append(name)
        seen.add(name)

  for step in detect_framework_steps(prompt):
    if step.name not in seen:
      kws.append(step.name)
      seen.add(step.name)
    for block in step.blocks[:2]:
      name = block.removeprefix("minecraft:").replace("_", " ")
      if name not in seen:
        kws.append(name)
        seen.add(name)

  return kws
