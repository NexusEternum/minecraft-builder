"""
Minecraft Epic Bases — modular build catalog.

Full mega-scenes (whole Fenrir's Tooth longship, etc.) are reserved for future
150³ training. Exterior detail modules are registered here at 32³.
"""

from __future__ import annotations

from .registry import BookBuild, BuildZone

EPIC_BASES: dict[str, BookBuild] = {
  "epic_bases_wolf_figurehead": BookBuild(
    id="epic_bases_wolf_figurehead",
    name="Wolf Figurehead",
    theme="viking",
    biome="ocean",
    caption=(
      "a fenrirs tooth viking longship wolf figurehead grey stone carved bow "
      "intimidating figurehead naval exterior module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:andesite",
      "minecraft:polished_andesite",
      "minecraft:gray_concrete",
      "minecraft:spruce_planks",
      "minecraft:dark_oak_planks",
    ),
    zones=(
      BuildZone(
        name="6 by 8 wolf figurehead",
        size=(6, 8, 6),
        materials=("stone_bricks", "andesite", "polished_andesite", "spruce_planks"),
        features=("stylized wolf head bow carving", "grey stone figurehead", "intimidating ship prow"),
        interior=(),
      ),
    ),
    exterior_features=("fenrirs tooth wolf figurehead", "viking ship bow carving"),
    tips=("Strike fear with intimidating figurehead", "Grey stone wolf at ship bow"),
  ),
  "epic_bases_deck_brazier": BookBuild(
    id="epic_bases_deck_brazier",
    name="Deck Brazier",
    theme="viking",
    biome="ocean",
    caption=(
      "a fenrirs tooth viking longship deck brazier campfire lantern railing "
      "warm deck lighting naval exterior module"
    ),
    palette=(
      "minecraft:spruce_planks",
      "minecraft:dark_oak_fence",
      "minecraft:campfire",
      "minecraft:lantern",
      "minecraft:oak_trapdoor",
      "minecraft:chain",
    ),
    zones=(
      BuildZone(
        name="4 by 6 deck brazier",
        size=(4, 6, 4),
        materials=("spruce_planks", "dark_oak_fence", "campfire", "lantern", "chain"),
        features=("lit deck brazier post", "railing mounted fire", "warm ship lighting"),
        interior=(),
      ),
    ),
    exterior_features=("fenrirs tooth deck brazier", "viking ship deck lighting"),
    tips=("Braziers line ship railings", "Campfire or lantern warm glow"),
  ),
  "epic_bases_emerald_wolf": BookBuild(
    id="epic_bases_emerald_wolf",
    name="Emerald Wolf Statue",
    theme="viking",
    biome="ocean",
    caption=(
      "a fenrirs tooth viking longship emerald wolf statue glowing green wolf "
      "midship deck ornament naval exterior module"
    ),
    palette=(
      "minecraft:emerald_block",
      "minecraft:sea_lantern",
      "minecraft:spruce_planks",
      "minecraft:dark_oak_planks",
      "minecraft:stone_bricks",
      "minecraft:gold_block",
    ),
    zones=(
      BuildZone(
        name="4 by 6 emerald wolf",
        size=(4, 6, 4),
        materials=("emerald_block", "sea_lantern", "spruce_planks", "stone_bricks", "gold_block"),
        features=("glowing green wolf statue", "midship deck ornament", "emerald block carving"),
        interior=(),
      ),
    ),
    exterior_features=("fenrirs tooth emerald wolf", "viking ship deck statue"),
    tips=("Small glowing emerald wolf on deck", "Midship ornament"),
  ),
  "epic_bases_crows_nest": BookBuild(
    id="epic_bases_crows_nest",
    name="Crow's Nest",
    theme="viking",
    biome="ocean",
    caption=(
      "a fenrirs tooth viking longship crows nest mast lookout box eagle eye "
      "drowned threat warning naval exterior module"
    ),
    palette=(
      "minecraft:oak_fence",
      "minecraft:spruce_planks",
      "minecraft:dark_oak_planks",
      "minecraft:ladder",
      "minecraft:oak_trapdoor",
      "minecraft:lantern",
      "minecraft:oak_log",
    ),
    zones=(
      BuildZone(
        name="4 by 10 crows nest",
        size=(4, 10, 4),
        materials=("oak_fence", "spruce_planks", "ladder", "oak_trapdoor", "oak_log", "lantern"),
        features=("mast top lookout box", "fence railing nest", "ladder access"),
        interior=("lookout post",),
      ),
    ),
    exterior_features=("fenrirs tooth crows nest", "viking ship mast lookout"),
    tips=("Post ally in lookout to warn crew", "Top of highest mast"),
  ),
  "epic_bases_ship_flag": BookBuild(
    id="epic_bases_ship_flag",
    name="Ship Flag",
    theme="viking",
    biome="ocean",
    caption=(
      "a fenrirs tooth viking longship red white striped flag mast banner "
      "rear mast naval exterior module"
    ),
    palette=(
      "minecraft:red_wool",
      "minecraft:white_wool",
      "minecraft:oak_fence",
      "minecraft:spruce_fence",
      "minecraft:oak_log",
      "minecraft:barrier",
    ),
    zones=(
      BuildZone(
        name="3 by 8 ship flag",
        size=(3, 8, 3),
        materials=("red_wool", "white_wool", "oak_fence", "spruce_fence", "oak_log"),
        features=("red white striped sail flag", "rear mast banner", "fence mast pole"),
        interior=(),
      ),
    ),
    exterior_features=("fenrirs tooth ship flag", "viking longship banner"),
    tips=("Red and white flag from rear mast", "Striped wool banner"),
  ),
  "epic_bases_ship_oars": BookBuild(
    id="epic_bases_ship_oars",
    name="Ship Oars",
    theme="viking",
    biome="ocean",
    caption=(
      "a fenrirs tooth viking longship oars wooden poles hull side rowing "
      "longship naval exterior module"
    ),
    palette=(
      "minecraft:spruce_planks",
      "minecraft:dark_oak_planks",
      "minecraft:oak_fence",
      "minecraft:spruce_stairs",
      "minecraft:water",
      "minecraft:dark_oak_log",
    ),
    zones=(
      BuildZone(
        name="10 by 4 ship oars",
        size=(10, 4, 6),
        materials=("spruce_planks", "dark_oak_planks", "oak_fence", "spruce_stairs", "water"),
        features=("long oars from hull sides", "wooden poles in water", "viking rowing banks"),
        interior=(),
      ),
    ),
    exterior_features=("fenrirs tooth ship oars", "viking longship rowing poles"),
    tips=("Oars protrude from hull into water", "Along ship sides"),
  ),
  "epic_bases_artillery_cannon": BookBuild(
    id="epic_bases_artillery_cannon",
    name="Artillery Cannon",
    theme="viking",
    biome="ocean",
    caption=(
      "a fenrirs tooth viking longship artillery cannon tnt fueled stern weapon "
      "explosive powerhouse naval exterior module"
    ),
    palette=(
      "minecraft:dark_oak_planks",
      "minecraft:stone_bricks",
      "minecraft:iron_block",
      "minecraft:tnt",
      "minecraft:dispenser",
      "minecraft:oak_stairs",
      "minecraft:water",
    ),
    zones=(
      BuildZone(
        name="6 by 6 artillery cannon",
        size=(6, 6, 6),
        materials=("dark_oak_planks", "stone_bricks", "iron_block", "tnt", "dispenser"),
        features=("stern mounted cannon", "tnt fueled artillery", "explosive deck weapon"),
        interior=(),
      ),
    ),
    exterior_features=("fenrirs tooth artillery cannon", "viking ship stern weapon"),
    tips=("TNT-fueled cannon at ship stern", "More explosive than creepers"),
  ),
}

# Mega builds saved for 150³ — not registered yet:
# - epic_bases_fenrirs_tooth (full viking longship with multiple decks and sails)
