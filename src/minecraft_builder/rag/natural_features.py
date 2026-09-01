"""
Natural features from "Natural Features" (Minecraft Guide to Creative).

Landmarks and terrain elements that inspire scene composition.
Feeds prompt enrichment now; scene generation later.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NaturalFeature:
  id: str
  name: str
  aliases: tuple[str, ...]
  suitable_builds: tuple[str, ...]
  blocks: tuple[str, ...]
  tip: str


def _b(name: str) -> str:
  if name.startswith("minecraft:"):
    return name
  return f"minecraft:{name}"


NATURAL_FEATURES: tuple[NaturalFeature, ...] = (
  NaturalFeature(
    id="river_lake",
    name="river or lake",
    aliases=("river", "lake", "stream", "pond", "waterfall base"),
    suitable_builds=("water mill", "bridge", "dock", "fishing hut", "lakeside cabin"),
    blocks=(_b("water"), _b("oak_planks"), _b("oak_log"), _b("cobblestone")),
    tip="Build water mills and bridges beside rivers and lakes",
  ),
  NaturalFeature(
    id="village",
    name="village",
    aliases=("village", "hamlet", "town square", "trading"),
    suitable_builds=("village house", "market stall", "farm plot", "well", "church"),
    blocks=(_b("oak_planks"), _b("cobblestone"), _b("hay_block"), _b("wheat")),
    tip="Extend or modernize existing village buildings",
  ),
  NaturalFeature(
    id="mineshaft",
    name="abandoned mineshaft",
    aliases=("mineshaft", "mine", "mining", "underground", "tunnel"),
    suitable_builds=("industrial build", "mine entrance", "ore processing", "factory", "mining terminal"),
    blocks=(_b("oak_planks"), _b("oak_fence"), _b("rail"), _b("iron_ore")),
    tip="Mineshafts are a perfect front for industrial builds",
  ),
  NaturalFeature(
    id="waterfall",
    name="waterfall",
    aliases=("waterfall", "cascade", "falls"),
    suitable_builds=("cliff house", "bridge over waterfall", "mountain retreat", "temple"),
    blocks=(_b("water"), _b("stone"), _b("mossy_cobblestone"), _b("spruce_log")),
    tip="Build atop or across an impressive waterfall",
  ),
  NaturalFeature(
    id="temple",
    name="desert or jungle temple",
    aliases=("temple", "desert temple", "jungle temple", "ancient ruins", "ruins"),
    suitable_builds=("historical build", "ancient centerpiece", "archaeological site", "monument"),
    blocks=(_b("sandstone"), _b("mossy_cobblestone"), _b("cobblestone"), _b("chiseled_stone_bricks")),
    tip="Temples are perfect centrepieces for historical or ancient builds",
  ),
  NaturalFeature(
    id="lava",
    name="lava",
    aliases=("lava", "lava moat", "lava river", "volcanic", "hellish"),
    suitable_builds=("evil castle", "dark fortress", "nether portal room", "volcano base"),
    blocks=(_b("lava"), _b("obsidian"), _b("nether_bricks"), _b("blackstone")),
    tip="Lava rivers around a castle add danger and defense",
  ),
  NaturalFeature(
    id="stronghold",
    name="stronghold",
    aliases=("stronghold", "end portal", "secret lair", "underground fortress"),
    suitable_builds=("secret lair", "underground base", "library", "dungeon"),
    blocks=(_b("stone_bricks"), _b("mossy_stone_bricks"), _b("cracked_stone_bricks"), _b("bookshelf")),
    tip="Strongholds make excellent secret lairs with libraries and portals",
  ),
  NaturalFeature(
    id="custom_terrain",
    name="custom terrain",
    aliases=("custom terrain", "candyland", "moon crater", "floating island", "terraform"),
    suitable_builds=("fantasy landscape", "moon base", "candy world", "sky city"),
    blocks=(_b("quartz_block"), _b("snow_block"), _b("concrete"), _b("wool")),
    tip="Build your own terrain — moon craters, candylands, snowy stone cities",
  ),
)


def detect_features(prompt: str) -> list[NaturalFeature]:
  lower = prompt.lower()
  matched: list[tuple[int, NaturalFeature]] = []
  seen: set[str] = set()

  for feature in NATURAL_FEATURES:
    for alias in sorted(feature.aliases, key=len, reverse=True):
      if alias in lower and feature.id not in seen:
        matched.append((len(alias), feature))
        seen.add(feature.id)
        break

  matched.sort(key=lambda x: x[0], reverse=True)
  return [f for _, f in matched]


def feature_keywords(feature: NaturalFeature) -> list[str]:
  names = [b.removeprefix("minecraft:").replace("_", " ") for b in feature.blocks[:2]]
  return [feature.name, *list(feature.suitable_builds[:2]), *names]
