"""
Banners from the Minecraft Guide to Creative.

Lower-priority decor — useful when prompts mention flags, heraldry,
or formal display structures. Pattern recipes omitted (too granular for prompts).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BannerUse:
  id: str
  name: str
  aliases: tuple[str, ...]
  blocks: tuple[str, ...]
  tip: str


def _b(name: str) -> str:
  if name.startswith("minecraft:"):
    return name
  return f"minecraft:{name}"


# Pattern categories (for prompt vocabulary, not crafting recipes)
BANNER_PATTERN_TYPES: tuple[str, ...] = (
  "halves",
  "stripes",
  "cross",
  "border",
  "gradient",
  "roundel",
  "crenelated",
  "layered",
)

MAX_BANNER_LAYERS = 6

BANNER_DISPLAYS: tuple[BannerUse, ...] = (
  BannerUse(
    id="corner_flags",
    name="corner pillar flags",
    aliases=("flag", "flags", "banner", "banners", "heraldry", "coat of arms", "pavilion"),
    blocks=(_b("white_banner"), _b("stone_bricks"), _b("oak_fence")),
    tip="Tall pillars at corners with formal diagonal-split banners",
  ),
  BannerUse(
    id="wall_banner",
    name="wall hanging banner",
    aliases=("wall banner", "hanging banner", "tapestry", "wallpaper"),
    blocks=(_b("white_banner"),),
    tip="Banners as wallpaper, signs, or shrine decorations on walls",
  ),
  BannerUse(
    id="castle_post",
    name="castle banner post",
    aliases=("castle flag", "fortress banner", "battlements flag"),
    blocks=(_b("stone_bricks"), _b("cobblestone_wall"), _b("torch"), _b("white_banner")),
    tip="Stone brick post with torches and a heraldic banner",
  ),
  BannerUse(
    id="nether_post",
    name="nether banner post",
    aliases=("nether banner", "pirate flag", "skull banner"),
    blocks=(_b("nether_bricks"), _b("nether_brick_fence"), _b("skeleton_skull"), _b("white_banner")),
    tip="Nether brick post with skull-and-crossbones banner",
  ),
  BannerUse(
    id="town_square",
    name="town square banner light",
    aliases=("town square", "plaza banner", "banner lamp", "public square"),
    blocks=(_b("chiseled_stone_bricks"), _b("dark_oak_planks"), _b("redstone_lamp"), _b("black_banner")),
    tip="Chiseled stone and dark oak structure with banners and a redstone lamp",
  ),
  BannerUse(
    id="garden_flags",
    name="garden path flags",
    aliases=("garden banner", "park flag", "formal garden", "path decoration"),
    blocks=(_b("white_banner"), _b("rose_bush"), _b("stone_brick_stairs"), _b("oak_leaves")),
    tip="Banners along garden paths with roses and leaf hedges",
  ),
)

BANNER_ICONS: tuple[str, ...] = (
  "creeper charge",
  "skull and crossbones",
  "flower charge",
  "mojang logo",
)


def detect_banners(prompt: str) -> list[BannerUse]:
  lower = prompt.lower()
  matched: list[tuple[int, BannerUse]] = []
  seen: set[str] = set()
  for display in BANNER_DISPLAYS:
    for alias in sorted(display.aliases, key=len, reverse=True):
      if alias in lower and display.id not in seen:
        matched.append((len(alias), display))
        seen.add(display.id)
        break
  matched.sort(key=lambda x: x[0], reverse=True)
  return [d for _, d in matched]


def banner_keywords(display: BannerUse) -> list[str]:
  blocks = [b.removeprefix("minecraft:").replace("_", " ") for b in display.blocks[:2]]
  return [display.name, "layered banner", *blocks]
