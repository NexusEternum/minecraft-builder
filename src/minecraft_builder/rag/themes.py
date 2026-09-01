"""
Block palettes from the Minecraft Guide to Creative.

Each theme maps to a curated set of blocks from the book.
Used by RAG to enrich prompts with on-theme materials.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
  name: str
  aliases: tuple[str, ...]
  blocks: tuple[str, ...]
  description: str = ""


def _b(name: str) -> str:
  """Shorthand: 'oak_planks' -> 'minecraft:oak_planks'"""
  if name.startswith("minecraft:"):
    return name
  return f"minecraft:{name}"


THEMES: dict[str, Theme] = {
  "rustic": Theme(
    name="rustic",
    aliases=("rustic", "country", "farm", "wooden", "cabin", "cottage"),
    blocks=(
      _b("cobblestone"),
      _b("dark_oak_planks"),
      _b("dark_oak_log"),
      _b("andesite"),
      _b("glass"),
    ),
    description="Warm natural materials, dark oak and stone",
  ),
  "historical": Theme(
    name="historical",
    aliases=("historical", "history", "ancient", "desert", "temple", "ruins"),
    blocks=(
      _b("sandstone"),
      _b("orange_terracotta"),
      _b("diorite"),
      _b("andesite"),
      _b("granite"),
    ),
    description="Sandstone and terracotta for ancient or desert builds",
  ),
  "fantasy": Theme(
    name="fantasy",
    aliases=("fantasy", "magical", "enchanted", "fairy", "elven", "mystical"),
    blocks=(
      _b("purpur_block"),
      _b("purpur_pillar"),
      _b("prismarine"),
      _b("prismarine_bricks"),
      _b("moss_block"),
    ),
    description="Purpur and prismarine for otherworldly structures",
  ),
  "industrial": Theme(
    name="industrial",
    aliases=("industrial", "factory", "warehouse", "urban", "modern gritty", "observatory"),
    blocks=(
      _b("stone_bricks"),
      _b("glass"),
      _b("polished_andesite"),
      _b("quartz_block"),
      _b("gravel"),
    ),
    description="Stone, quartz, and gravel for utilitarian builds",
  ),
  "steampunk": Theme(
    name="steampunk",
    aliases=("steampunk", "steam", "clockwork", "brass", "victorian", "airship", "dirigible"),
    blocks=(
      _b("stone_bricks"),
      _b("oak_log"),
      _b("glowstone"),
      _b("quartz_block"),
      _b("dark_oak_planks"),
    ),
    description="Wood, stone, and glowstone for mechanical fantasy",
  ),
  "infernal": Theme(
    name="infernal",
    aliases=("infernal", "nether", "hell", "demonic", "lava", "fortress"),
    blocks=(
      _b("nether_bricks"),
      _b("netherrack"),
      _b("nether_brick_fence"),
      _b("obsidian"),
      _b("glowstone"),
    ),
    description="Nether materials for dark, fiery structures",
  ),
  "classical": Theme(
    name="classical",
    aliases=(
      "classical", "classy", "elegant", "marble", "greco", "roman", "palace",
      "mediterranean", "exotic villa", "villa", "colonnade",
    ),
    blocks=(
      _b("quartz_block"),
      _b("diorite"),
      _b("smooth_quartz"),
      _b("chiseled_stone_bricks"),
      _b("light_blue_stained_glass"),
    ),
    description="Quartz and diorite for grand, refined architecture",
  ),
  "monochromatic": Theme(
    name="monochromatic",
    aliases=(
      "monochromatic",
      "monochrome",
      "monochromatic scale",
      "grayscale",
      "greyscale",
      "black and white",
      "neutral palette",
    ),
    blocks=(
      _b("black_concrete"),
      _b("coal_block"),
      _b("gray_concrete"),
      _b("stone_bricks"),
      _b("light_gray_concrete"),
      _b("polished_andesite"),
      _b("birch_planks"),
      _b("diorite"),
      _b("quartz_block"),
    ),
    description="Dark-to-light scale from the book aesthetics chapter",
  ),
}


def detect_themes(prompt: str) -> list[Theme]:
  """Match themes mentioned in a prompt (by name or alias)."""
  lower = prompt.lower()
  matched: list[Theme] = []
  seen: set[str] = set()

  # Check longer aliases first ("monochromatic scale" before "monochromatic")
  all_aliases: list[tuple[str, Theme]] = []
  for theme in THEMES.values():
    for alias in theme.aliases:
      all_aliases.append((alias, theme))
  all_aliases.sort(key=lambda x: len(x[0]), reverse=True)

  for alias, theme in all_aliases:
    if alias in lower and theme.name not in seen:
      matched.append(theme)
      seen.add(theme.name)

  return matched


def theme_block_names(theme: Theme, short: bool = True) -> list[str]:
  """Return human-readable block names for prompts."""
  names = []
  for block in theme.blocks:
    name = block.removeprefix("minecraft:")
    if short:
      name = name.replace("_", " ")
    names.append(name)
  return names


def themes_for_prompt(prompt: str) -> list[str]:
  """Block name strings from all detected themes."""
  blocks: list[str] = []
  seen: set[str] = set()
  for theme in detect_themes(prompt):
    for name in theme_block_names(theme):
      if name not in seen:
        blocks.append(name)
        seen.add(name)
  return blocks
