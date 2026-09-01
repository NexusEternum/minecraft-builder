"""
Functional decor and lighting from the Minecraft Guide to Creative.

Light fixtures and decorative functional blocks for interior/exterior finishing.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DecorFeature:
  id: str
  name: str
  aliases: tuple[str, ...]
  blocks: tuple[str, ...]
  light_level: int | None  # reference from book
  tip: str


def _b(name: str) -> str:
  if name.startswith("minecraft:"):
    return name
  return f"minecraft:{name}"


# Full light level reference from the book (levels 1–15).
# Stored as metadata for future mob-spawn / lighting planners — not added to prompts.
LIGHT_SOURCES: dict[str, int] = {
  # Level 15
  "glowstone": 15,
  "beacon": 15,
  "jack_o_lantern": 15,
  "sunlight": 15,
  "fire": 15,
  "redstone_lamp": 15,
  "sea_lantern": 15,
  "end_portal": 15,
  "lava": 15,
  # Level 14
  "end_rod": 14,
  "torch": 14,
  # Level 13
  "furnace": 13,
  # Level 11
  "nether_portal": 11,
  # Level 9
  "redstone_ore": 9,
  # Level 7
  "redstone_torch": 7,
  "ender_chest": 7,
  # Level 4
  "moonlight": 4,
  # Level 3
  "magma_block": 3,
  # Level 1
  "end_portal_frame": 1,
  "dragon_egg": 1,
  "brewing_stand": 1,
  "brown_mushroom": 1,
}

# Mob spawn prevention requires light level >= 8 on every surface block
MOB_SAFE_LIGHT_LEVEL = 8

DECOR_FEATURES: tuple[DecorFeature, ...] = (
  DecorFeature(
    id="stained_window",
    name="colourful window",
    aliases=("stained glass", "colourful window", "colorful window", "coloured window"),
    blocks=(_b("stained_glass"), _b("glass_pane")),
    light_level=None,
    tip="Stained glass filters sunlight into coloured interior light",
  ),
  DecorFeature(
    id="chandelier",
    name="chandelier",
    aliases=("chandelier", "hanging light", "ceiling light"),
    blocks=(_b("end_rod"), _b("oak_fence"), _b("chain")),
    light_level=14,
    tip="End rods attached to fences make an ornate chandelier",
  ),
  DecorFeature(
    id="fireplace",
    name="cosy fireplace",
    aliases=("fireplace", "hearth", "cosy", "cozy fire"),
    blocks=(_b("netherrack"), _b("cobblestone"), _b("iron_bars"), _b("cobblestone_stairs")),
    light_level=15,
    tip="Netherrack fire in cobblestone surround with iron bar grate",
  ),
  DecorFeature(
    id="framed_light",
    name="framed wall light",
    aliases=("framed light", "wall light", "inset torch", "item frame light"),
    blocks=(_b("torch"), _b("stone_slab"), _b("item_frame")),
    light_level=14,
    tip="Torch and slab inside an item frame for unusual interior lighting",
  ),
  DecorFeature(
    id="beacon_light",
    name="exterior beacon light",
    aliases=("beacon light", "signal light", "roof beacon", "warning light"),
    blocks=(_b("netherrack"), _b("brick_stairs"), _b("oak_fence")),
    light_level=15,
    tip="Lit netherrack with brick stairs and fences as exterior signal light",
  ),
  DecorFeature(
    id="inset_lighting",
    name="inset glowstone",
    aliases=("inset light", "recessed light", "floor light", "hidden light"),
    blocks=(_b("glowstone"), _b("carpet"), _b("glass")),
    light_level=15,
    tip="Glowstone set flush in walls or floors, covered by carpet or glass",
  ),
  DecorFeature(
    id="lava_lamp",
    name="lava lamplight",
    aliases=("lava lamp", "lava light", "lava feature", "lava wall"),
    blocks=(_b("lava"), _b("glass"), _b("iron_bars")),
    light_level=15,
    tip="Lava poured into glass-covered wall cavities as a light feature",
  ),
  DecorFeature(
    id="lamp_post",
    name="lamp post",
    aliases=("lamp post", "street lamp", "streetlight", "lantern post"),
    blocks=(_b("netherrack"), _b("oak_fence"), _b("oak_trapdoor")),
    light_level=15,
    tip="Fence post with netherrack fire on top enclosed in trapdoors",
  ),
  DecorFeature(
    id="light_installation",
    name="arty light installation",
    aliases=("light art", "light installation", "glowing art", "modern lighting"),
    blocks=(_b("glowstone"), _b("stained_glass"), _b("sea_lantern")),
    light_level=15,
    tip="Glowstone with stained glass for colourful modern light sculptures",
  ),
)


def detect_decor(prompt: str) -> list[DecorFeature]:
  lower = prompt.lower()
  matched: list[tuple[int, DecorFeature]] = []
  seen: set[str] = set()

  for feature in DECOR_FEATURES:
    for alias in sorted(feature.aliases, key=len, reverse=True):
      if alias in lower and feature.id not in seen:
        matched.append((len(alias), feature))
        seen.add(feature.id)
        break

  # Broad lighting/decor triggers
  if not matched and any(w in lower for w in ("lighting", "light", "decor", "decoration", "interior", "cozy", "cosy")):
    return [DECOR_FEATURES[2], DECOR_FEATURES[7]]  # fireplace + lamp post as defaults

  matched.sort(key=lambda x: x[0], reverse=True)
  return [f for _, f in matched]


def decor_keywords(feature: DecorFeature) -> list[str]:
  blocks = [b.removeprefix("minecraft:").replace("_", " ") for b in feature.blocks[:2]]
  return [feature.name, *blocks]


def light_level_for_block(block_id: str) -> int | None:
  """Look up light level for a block name (reference only)."""
  key = block_id.removeprefix("minecraft:").replace(" ", "_")
  return LIGHT_SOURCES.get(key)


def mob_safe_sources() -> list[str]:
  """Blocks that emit enough light (>= 8) to prevent mob spawning."""
  return [name for name, level in LIGHT_SOURCES.items() if level >= MOB_SAFE_LIGHT_LEVEL]
