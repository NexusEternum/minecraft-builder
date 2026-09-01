"""
Color wheel and color theory from the Minecraft Guide to Creative (Aesthetics chapter).

Used to suggest harmonious block combinations when enriching prompts.
"""

from __future__ import annotations

from dataclasses import dataclass


def _b(name: str) -> str:
  if name.startswith("minecraft:"):
    return name
  return f"minecraft:{name}"


@dataclass(frozen=True)
class ColorEntry:
  name: str
  block: str
  hue_group: str  # position on the wheel


# Blocks around the color wheel (clockwise from purple/magenta)
COLOR_WHEEL: tuple[ColorEntry, ...] = (
  ColorEntry("purple wool", _b("purple_wool"), "purple"),
  ColorEntry("magenta wool", _b("magenta_wool"), "magenta"),
  ColorEntry("pink wool", _b("pink_wool"), "pink"),
  ColorEntry("pink terracotta", _b("pink_terracotta"), "pink"),
  ColorEntry("red terracotta", _b("red_terracotta"), "red"),
  ColorEntry("red wool", _b("red_wool"), "red"),
  ColorEntry("red mushroom block", _b("red_mushroom_block"), "red"),
  ColorEntry("redstone block", _b("redstone_block"), "red"),
  ColorEntry("orange terracotta", _b("orange_terracotta"), "orange"),
  ColorEntry("orange wool", _b("orange_wool"), "orange"),
  ColorEntry("yellow terracotta", _b("yellow_terracotta"), "yellow"),
  ColorEntry("gold block", _b("gold_block"), "yellow"),
  ColorEntry("yellow wool", _b("yellow_wool"), "yellow"),
  ColorEntry("melon", _b("melon_block"), "yellow"),
  ColorEntry("lime wool", _b("lime_wool"), "green"),
  ColorEntry("emerald block", _b("emerald_block"), "green"),
  ColorEntry("green wool", _b("green_wool"), "green"),
  ColorEntry("prismarine bricks", _b("prismarine_bricks"), "teal"),
  ColorEntry("cyan wool", _b("cyan_wool"), "cyan"),
  ColorEntry("packed ice", _b("packed_ice"), "blue"),
  ColorEntry("light blue wool", _b("light_blue_wool"), "blue"),
  ColorEntry("lapis block", _b("lapis_block"), "blue"),
  ColorEntry("blue wool", _b("blue_wool"), "blue"),
  ColorEntry("blue terracotta", _b("blue_terracotta"), "blue"),
)

# Monochromatic scale from the book (dark → light)
MONOCHROMATIC_SCALE: tuple[str, ...] = (
  _b("black_concrete"),
  _b("coal_block"),
  _b("gray_concrete"),
  _b("stone_bricks"),
  _b("light_gray_concrete"),
  _b("polished_andesite"),
  _b("birch_planks"),
  _b("diorite"),
  _b("quartz_block"),
)

# Book examples for each scheme type
ANALOGOUS_EXAMPLES: tuple[tuple[str, str], ...] = (
  (_b("blue_terracotta"), _b("light_blue_wool")),
  (_b("green_wool"), _b("emerald_block")),
  (_b("yellow_wool"), _b("gold_block")),
  (_b("red_wool"), _b("red_mushroom_block")),
)

COMPLEMENTARY_EXAMPLES: tuple[tuple[str, str], ...] = (
  (_b("purple_wool"), _b("melon_block")),
  (_b("blue_wool"), _b("orange_wool")),
  (_b("red_wool"), _b("cyan_wool")),
  (_b("gold_block"), _b("blue_terracotta")),
)

TRIADIC_EXAMPLES: tuple[tuple[str, str, str], ...] = (
  (_b("red_wool"), _b("gold_block"), _b("blue_wool")),
  (_b("orange_wool"), _b("green_wool"), _b("purple_wool")),
  (_b("red_terracotta"), _b("lime_wool"), _b("lapis_block")),
  (_b("yellow_terracotta"), _b("prismarine_bricks"), _b("redstone_block")),
)

SCHEME_ALIASES: dict[str, str] = {
  "analogous": "analogue",
  "analogue": "analogue",
  "adjacent": "analogue",
  "complementary": "complementary",
  "complement": "complementary",
  "contrast": "complementary",
  "triadic": "triadic",
  "triangle": "triadic",
  "monochromatic": "monochromatic",
  "monochrome": "monochromatic",
  "grayscale": "monochromatic",
  "greyscale": "monochromatic",
}


def detect_color_scheme(prompt: str) -> str | None:
  lower = prompt.lower()
  for alias, scheme in SCHEME_ALIASES.items():
    if alias in lower:
      return scheme
  return None


def blocks_for_scheme(scheme: str) -> list[str]:
  """Return human-readable block names for a color scheme."""
  if scheme == "analogue":
    blocks = []
    for a, b in ANALOGOUS_EXAMPLES:
      blocks.extend([_short(a), _short(b)])
    return _dedupe(blocks)[:6]

  if scheme == "complementary":
    blocks = []
    for a, b in COMPLEMENTARY_EXAMPLES:
      blocks.extend([_short(a), _short(b)])
    return _dedupe(blocks)[:6]

  if scheme == "triadic":
    blocks = []
    for a, b, c in TRIADIC_EXAMPLES:
      blocks.extend([_short(a), _short(b), _short(c)])
    return _dedupe(blocks)[:6]

  if scheme == "monochromatic":
    return [_short(b) for b in MONOCHROMATIC_SCALE[:6]]

  return []


def wheel_blocks_for_hue(hue: str) -> list[str]:
  """Get blocks from the color wheel matching a hue group."""
  return [_short(e.block) for e in COLOR_WHEEL if hue in e.hue_group or e.hue_group in hue]


def _short(block_id: str) -> str:
  return block_id.removeprefix("minecraft:").replace("_", " ")


def _dedupe(items: list[str]) -> list[str]:
  seen: set[str] = set()
  out: list[str] = []
  for item in items:
    if item not in seen:
      out.append(item)
      seen.add(item)
  return out
