"""
Biome → build pairing from "Using the Land" (Minecraft Guide to Creative).

Helps match build style to environment. Full scene generation (structure +
terrain) is a future advanced feature — for now this enriches prompts.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BiomeGuide:
  id: str
  name: str
  aliases: tuple[str, ...]
  suitable_builds: tuple[str, ...]
  characteristics: str
  terrain_blocks: tuple[str, ...]  # for future scene generation


def _b(name: str) -> str:
  if name.startswith("minecraft:"):
    return name
  return f"minecraft:{name}"


BIOMES: dict[str, BiomeGuide] = {
  "plains": BiomeGuide(
    id="plains",
    name="plains",
    aliases=("plains", "flat", "grassland", "meadow", "field"),
    suitable_builds=("farmhouse", "mill", "industrial plant", "farm", "barn", "village"),
    characteristics="Flat grassy biome with water holes and passive mobs",
    terrain_blocks=(_b("grass_block"), _b("dirt"), _b("water"), _b("short_grass")),
  ),
  "forest": BiomeGuide(
    id="forest",
    name="forest",
    aliases=("forest", "woods", "woodland", "birch forest", "oak forest"),
    suitable_builds=("cozy cottage", "treehouse", "elven village", "cabin", "hunter lodge"),
    characteristics="Abundant trees and plants",
    terrain_blocks=(_b("grass_block"), _b("oak_log"), _b("oak_leaves"), _b("birch_log")),
  ),
  "swamp": BiomeGuide(
    id="swamp",
    name="swamp",
    aliases=("swamp", "marsh", "bog", "wetland"),
    suitable_builds=("stilted village", "pirate harbour", "harbor", "dock", "witch hut"),
    characteristics="Large bodies of water dotted with islands",
    terrain_blocks=(_b("water"), _b("lily_pad"), _b("oak_log"), _b("vine"), _b("mud")),
  ),
  "jungle": BiomeGuide(
    id="jungle",
    name="jungle",
    aliases=("jungle", "tropical", "rainforest"),
    suitable_builds=("lost temple", "botanical garden", "simple hut", "ruins", "pyramid"),
    characteristics="Tropical blocks, tall trees, vines, and dense foliage",
    terrain_blocks=(_b("jungle_log"), _b("jungle_leaves"), _b("vine"), _b("grass_block")),
  ),
  "taiga": BiomeGuide(
    id="taiga",
    name="taiga",
    aliases=("taiga", "pine forest", "cold forest", "snowy taiga", "snowy forest"),
    suitable_builds=("ski lodge", "log cabin", "mountain village", "watchtower", "outpost"),
    characteristics="Spruce trees with snowy and mountainous variants",
    terrain_blocks=(_b("grass_block"), _b("snow"), _b("spruce_log"), _b("spruce_leaves")),
  ),
  "roofed_forest": BiomeGuide(
    id="roofed_forest",
    name="roofed forest",
    aliases=("roofed forest", "dark forest", "dark oak forest", "spooky forest"),
    suitable_builds=("haunted house", "decrepit temple", "spooky build", "witch manor", "dark castle"),
    characteristics="Thick dark oak canopy, little light, large mushrooms",
    terrain_blocks=(_b("dark_oak_log"), _b("dark_oak_leaves"), _b("brown_mushroom_block"), _b("podzol")),
  ),
  "extreme_hills": BiomeGuide(
    id="extreme_hills",
    name="extreme hills",
    aliases=("extreme hills", "mountains", "mountain", "alpine", "peaks", "cliffs"),
    suitable_builds=("castle", "mountain castle", "cliff fortress", "monastery", "watchtower"),
    characteristics="Peaks and troughs — picturesque elevated terrain",
    terrain_blocks=(_b("stone"), _b("grass_block"), _b("snow"), _b("spruce_log")),
  ),
  "ice_plains": BiomeGuide(
    id="ice_plains",
    name="ice plains",
    aliases=("ice plains", "snowy plains", "snow biome", "tundra", "frozen"),
    suitable_builds=("ice palace", "isolated cabin", "igloo", "frozen fortress", "lodge"),
    characteristics="Bright white snow and minimal wildlife",
    terrain_blocks=(_b("snow_block"), _b("ice"), _b("packed_ice"), _b("snow")),
  ),
  "savanna": BiomeGuide(
    id="savanna",
    name="savanna",
    aliases=("savanna", "savannah", "acacia"),
    suitable_builds=("safari park", "acacia village", "outpost", "trading post", "hut"),
    characteristics="Dry grass and flat-topped acacia trees, wide open",
    terrain_blocks=(_b("grass_block"), _b("acacia_log"), _b("acacia_leaves"), _b("dirt")),
  ),
  "desert": BiomeGuide(
    id="desert",
    name="desert",
    aliases=("desert", "sandy", "sand dunes", "egyptian"),
    suitable_builds=("pyramid", "sphinx", "desert temple", "oasis village", "sandstone palace"),
    characteristics="Bright sandy biome with cacti and sandstone",
    terrain_blocks=(_b("sand"), _b("sandstone"), _b("cactus"), _b("dead_bush")),
  ),
  "nether": BiomeGuide(
    id="nether",
    name="nether",
    aliases=("nether", "hell", "lava lake", "nether fortress"),
    suitable_builds=("nether fortress", "demon lair", "hideaway", "alien landscape", "bastion"),
    characteristics="Dark unusual terrain with netherrack and lava",
    terrain_blocks=(_b("netherrack"), _b("nether_bricks"), _b("lava"), _b("soul_sand")),
  ),
  "end": BiomeGuide(
    id="end",
    name="the end",
    aliases=("the end", "end city", "end dimension", "ender"),
    suitable_builds=("end city", "fantasy tower", "alien structure", "end ship", "void base", "steampunk airship"),
    characteristics="End stone terrain with fantasy end cities and ships",
    terrain_blocks=(_b("end_stone"), _b("purpur_block"), _b("purpur_pillar"), _b("end_stone_bricks")),
  ),
  "mushroom_island": BiomeGuide(
    id="mushroom_island",
    name="mushroom island",
    aliases=("mushroom island", "mooshroom", "mycelium", "mushroom biome"),
    suitable_builds=("fairy cottage", "quirky build", "fantasy hut", "mushroom house"),
    characteristics="Bizarre mycelium terrain with giant mushrooms",
    terrain_blocks=(_b("mycelium"), _b("red_mushroom_block"), _b("brown_mushroom_block"), _b("mushroom_stem")),
  ),
  "ocean": BiomeGuide(
    id="ocean",
    name="ocean",
    aliases=("ocean", "underwater", "sea", "deep ocean", "coastal"),
    suitable_builds=(
      "underwater observatory", "glass dome", "lighthouse", "dock", "submarine base",
      "ocean observatory",
    ),
    characteristics="Deep water — limited surface building, spectacular underwater builds",
    terrain_blocks=(_b("water"), _b("sand"), _b("gravel"), _b("prismarine")),
  ),
  "mesa": BiomeGuide(
    id="mesa",
    name="mesa",
    aliases=("mesa", "badlands", "canyon", "wild west", "red sand"),
    suitable_builds=(
      "wild west saloon", "sheriff office", "western town", "mining town", "outpost",
      "exotic villa", "mediterranean villa", "sandstone palace",
    ),
    characteristics="Red sand and terracotta canyons",
    terrain_blocks=(_b("red_sand"), _b("terracotta"), _b("red_terracotta"), _b("orange_terracotta")),
  ),
}


def detect_biome(prompt: str) -> BiomeGuide | None:
  lower = prompt.lower()
  # Longer aliases first
  matches: list[tuple[int, BiomeGuide]] = []
  for biome in BIOMES.values():
    for alias in biome.aliases:
      if alias in lower:
        matches.append((len(alias), biome))
        break
  if not matches:
    return None
  matches.sort(key=lambda x: x[0], reverse=True)
  return matches[0][1]


def biome_keywords(biome: BiomeGuide) -> list[str]:
  """Keywords to enrich a prompt with biome-appropriate build types."""
  return [biome.name, *list(biome.suitable_builds[:3])]
