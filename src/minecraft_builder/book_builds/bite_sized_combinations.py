"""
Bite-Sized Builds — combination challenges (book page 93) and official combos.

These teach the model to compose smaller builds into larger scenes.
"""

from __future__ import annotations

from dataclasses import dataclass

from .registry import BookBuild, BuildZone


@dataclass(frozen=True)
class CombinationBuild:
  """Links a combo training sample to its source builds."""

  build: BookBuild
  source_ids: tuple[str, ...]
  challenge: str  # book challenge text


def _combo(
  id: str,
  name: str,
  sources: tuple[str, ...],
  challenge: str,
  caption: str,
  theme: str,
  biome: str,
  palette: tuple[str, ...],
  zones: tuple[BuildZone, ...],
  exterior_features: tuple[str, ...],
  tips: tuple[str, ...] = (),
) -> CombinationBuild:
  return CombinationBuild(
    source_ids=sources,
    challenge=challenge,
    build=BookBuild(
      id=id,
      name=name,
      theme=theme,
      biome=biome,
      caption=caption,
      palette=palette,
      zones=zones,
      exterior_features=exterior_features,
      tips=tips,
    ),
  )


COMBINATION_BUILDS: dict[str, CombinationBuild] = {
  entry.build.id: entry
  for entry in (
    _combo(
      "bite_combo_submarine_airlock",
      "Submarine with Airlock",
      ("bite_deep_sea_submarine", "bite_underwater_airlock"),
      "Official book combo — airlock fits the submarine underside",
      (
        "a deep-sea submarine with an underwater airlock hatch on the hull belly, "
        "acacia trapdoor sticky piston entrance with lever and redstone for safe diving"
      ),
      "aquatic",
      "ocean",
      (
        "minecraft:light_gray_concrete",
        "minecraft:glass",
        "minecraft:polished_andesite",
        "minecraft:acacia_trapdoor",
        "minecraft:sticky_piston",
        "minecraft:redstone_dust",
        "minecraft:lever",
        "minecraft:water",
      ),
      (
        BuildZone(
          name="submarine hull",
          size=(5, 5, 9),
          materials=("light_gray_concrete", "glass", "polished_andesite"),
          features=("cylindrical submarine body", "glass cockpit nose"),
          interior=(),
        ),
        BuildZone(
          name="underside airlock hatch",
          size=(3, 4, 3),
          materials=("acacia_trapdoor", "sticky_piston", "polished_andesite", "redstone_dust", "lever"),
          features=("trapdoor opens into submarine", "auto-closing piston seal"),
          interior=("acacia trapdoor", "sticky piston", "lever"),
        ),
      ),
      ("modular underwater vehicle with diver entrance", "redstone trapdoor airlock"),
      (
        "Mount the airlock mechanism flush to the submarine underside",
        "Flick lever to open trapdoor and climb in; it closes behind you",
      ),
    ),
    _combo(
      "bite_combo_maze_creeper",
      "Maze with Creeper Centerpiece",
      ("bite_halloween_maze", "bite_creeper"),
      "Combination challenge 1 — create a maze with a creeper centerpiece",
      (
        "a halloween hay bale maze with a giant creeper statue standing in the "
        "central clearing, soul fire lighting and spooky dead-end paths"
      ),
      "halloween",
      "forest",
      (
        "minecraft:hay_block",
        "minecraft:green_concrete",
        "minecraft:soul_campfire",
        "minecraft:carved_pumpkin",
      ),
      (
        BuildZone(
          name="hay bale maze walls",
          size=(16, 3, 16),
          materials=("hay_block", "soul_campfire", "soul_torch"),
          features=("winding maze", "soul fire alcoves"),
          interior=(),
        ),
        BuildZone(
          name="creeper centerpiece",
          size=(5, 16, 5),
          materials=("green_concrete", "gray_concrete", "lime_terracotta"),
          features=("giant creeper statue in maze center"),
          interior=("gray concrete face",),
        ),
      ),
      ("maze surrounds the creeper focal point", "forest creeper statue in clearing"),
    ),
    _combo(
      "bite_combo_fountain_aviary",
      "Fountain Aviary",
      ("bite_dolphin_fountain", "bite_aviary_pyramid"),
      "Combination challenge 2 — merge the fountain and bird aviary",
      (
        "an aviary pyramid with a dolphin fountain in the interior courtyard, "
        "orange glass pyramid walls around a prismarine fountain pool"
      ),
      "nature",
      "plains",
      (
        "minecraft:orange_stained_glass",
        "minecraft:prismarine_bricks",
        "minecraft:quartz_bricks",
        "minecraft:water",
        "minecraft:jungle_leaves",
      ),
      (
        BuildZone(
          name="glass aviary pyramid",
          size=(14, 8, 16),
          materials=("orange_stained_glass", "polished_blackstone_bricks", "birch_door"),
          features=("stepped pyramid aviary", "birch door foyer"),
          interior=(),
        ),
        BuildZone(
          name="interior dolphin fountain",
          size=(15, 6, 15),
          materials=("prismarine_bricks", "quartz_block", "water"),
          features=("fountain basin inside aviary", "leaping dolphin statue"),
          interior=("water", "prismarine bricks"),
        ),
      ),
      ("fountain as aviary centerpiece", "birds and water feature combined"),
    ),
    _combo(
      "bite_combo_train_collector",
      "Train Station with Cart Collector",
      ("bite_train_station", "bite_cart_collector"),
      "Combination challenge 3 — transport system with multiple stops",
      (
        "a train station with twin rail platforms and a cart collector at the line "
        "end, cactus hopper system returns minecarts to the station chests"
      ),
      "transport",
      "plains",
      (
        "minecraft:jungle_planks",
        "minecraft:rail",
        "minecraft:hopper",
        "minecraft:chest",
        "minecraft:cactus",
      ),
      (
        BuildZone(
          name="train station hall",
          size=(14, 6, 9),
          materials=("jungle_planks", "rail", "lantern"),
          features=("waiting hall", "twin platforms"),
          interior=(),
        ),
        BuildZone(
          name="cart collector siding",
          size=(9, 3, 4),
          materials=("hopper", "chest", "cactus", "rail"),
          features=("minecart recycling at track end"),
          interior=("hopper", "chest", "cactus"),
        ),
      ),
      ("integrated railway terminal", "cart return loop at station"),
    ),
    _combo(
      "bite_combo_bunker_destroyer",
      "Bunker with Item Destroyer",
      ("bite_hidden_bunker", "bite_item_destroyer"),
      "Combination challenge 4 — hidden bunker with built-in item destroyer",
      (
        "an underground hidden bunker with a secret entrance and a built-in item "
        "destroyer disposal alcove, modern furnished rooms with cactus trash chute"
      ),
      "modern",
      "plains",
      (
        "minecraft:white_concrete",
        "minecraft:birch_planks",
        "minecraft:sticky_piston",
        "minecraft:cactus",
        "minecraft:dropper",
      ),
      (
        BuildZone(
          name="furnished bunker interior",
          size=(18, 7, 18),
          materials=("white_concrete", "birch_planks", "acacia_stairs"),
          features=("kitchen bedroom living room", "secret piston entrance"),
          interior=(),
        ),
        BuildZone(
          name="item destroyer alcove",
          size=(6, 5, 5),
          materials=("cactus", "dropper", "hopper", "spruce_planks"),
          features=("hidden disposal room", "cactus item breaker"),
          interior=("cactus", "dropper"),
        ),
      ),
      ("utility disposal built into bunker wall", "hidden redstone trash system"),
    ),
    _combo(
      "bite_combo_vault_alarm",
      "Vault with Alarm System",
      ("bite_combination_lock", "bite_alarm_system"),
      "Combination challenge 5 — add alarm security to the vault",
      (
        "a combination lock vault door with an alarm system at the security entrance, "
        "lever lock panel plus bell and observer triggered stone brick archway"
      ),
      "industrial",
      "plains",
      (
        "minecraft:stone_bricks",
        "minecraft:lever",
        "minecraft:redstone_lamp",
        "minecraft:bell",
        "minecraft:iron_trapdoor",
      ),
      (
        BuildZone(
          name="combination lock vault",
          size=(9, 5, 3),
          materials=("stone_bricks", "lever", "redstone_lamp", "iron_door"),
          features=("four lever lock panel", "iron vault door"),
          interior=("lever", "redstone lamp"),
        ),
        BuildZone(
          name="alarm entrance gate",
          size=(4, 4, 4),
          materials=("bell", "observer", "iron_trapdoor", "glowstone"),
          features=("pressure triggered bells", "security archway"),
          interior=("bell", "observer", "iron trapdoor"),
        ),
      ),
      ("layered vault security", "alarm triggers on unauthorized entry"),
    ),
    _combo(
      "bite_combo_greenhouse_wishing_well",
      "Garden with Wishing Well and Greenhouse",
      ("bite_greenhouse", "bite_wishing_well"),
      "Combination challenge 1 — garden with wishing well beside greenhouse",
      (
        "a mud brick glass greenhouse with froglights and birch planter interior "
        "merged with a stone brick wishing well redstone hopper reward garden, "
        "warped roof lantern azalea landscaping on shared grass plot"
      ),
      "garden",
      "plains",
      (
        "minecraft:mud_bricks",
        "minecraft:glass_pane",
        "minecraft:stone_bricks",
        "minecraft:warped_planks",
        "minecraft:hopper",
        "minecraft:comparator",
        "minecraft:flowering_azalea",
        "minecraft:grass_block",
      ),
      (
        BuildZone(
          name="mud brick greenhouse",
          size=(9, 10, 13),
          materials=("mud_bricks", "glass_pane", "birch_planks", "pearlescent_froglight"),
          features=("gabled glass greenhouse", "spruce trapdoor plant beds", "froglight hanging roof"),
          interior=("birch plank floor", "barrel workbench", "flowering azalea planters"),
        ),
        BuildZone(
          name="wishing well garden",
          size=(6, 6, 6),
          materials=("stone_bricks", "warped_planks", "hopper", "comparator", "dispenser"),
          features=("3 by 3 stone well", "redstone hopper reward elevator", "warped tiered roof lantern"),
          interior=("hopper comparator chest receiver", "dispenser surface reward"),
        ),
      ),
      ("greenhouse and well share one garden plot", "redstone wishing well beside glasshouse"),
    ),
    _combo(
      "bite_combo_watchtower_skull_cove",
      "Pirate Watchtower Above Skull Cove",
      ("bite_skull_cove",),
      "Combination challenge 2 — pirate spotting hideout above skull cove",
      (
        "a wooden pirate watchtower with log cross-braced fence supports and lookout "
        "cabin on a cliff edge overlooking skull cove smooth quartz skull facade "
        "jungle dock and soul lantern treasure cave"
      ),
      "pirate",
      "ocean",
      (
        "minecraft:oak_log",
        "minecraft:oak_fence",
        "minecraft:oak_planks",
        "minecraft:smooth_quartz",
        "minecraft:jungle_planks",
        "minecraft:vine",
        "minecraft:soul_lantern",
        "minecraft:water",
      ),
      (
        BuildZone(
          name="cliff-top watchtower",
          size=(5, 12, 5),
          materials=("oak_log", "oak_fence", "oak_planks", "vine"),
          features=("vertical log mast", "cross-braced fence rigging", "roofed lookout cabin"),
          interior=("oak plank lookout floor",),
        ),
        BuildZone(
          name="skull cove cliff",
          size=(20, 15, 13),
          materials=("stone", "smooth_quartz", "jungle_planks", "water"),
          features=("quartz skull facade cave mouth", "12 deep cove", "jungle dock", "treasure room"),
          interior=("soul lantern gold chest loot",),
        ),
      ),
      ("watchtower overlooks skull cliff cove", "pirate spotting hideout above cave mouth"),
    ),
    _combo(
      "bite_combo_bus_racetrack",
      "Monster-Truck Bus Racetrack",
      ("bite_monster_truck_bus", "bite_horse_racecourse"),
      "Combination challenge 3 — monster-truck bus on horse racecourse track",
      (
        "a yellow monster truck school bus on oversized black wheels parked on a "
        "U-shaped horse racecourse gray concrete track with red white checkered "
        "curbs starting gate and grandstand fences"
      ),
      "racing",
      "plains",
      (
        "minecraft:yellow_concrete",
        "minecraft:black_concrete",
        "minecraft:gray_concrete",
        "minecraft:red_concrete",
        "minecraft:white_concrete",
        "minecraft:oak_fence",
        "minecraft:tinted_glass",
      ),
      (
        BuildZone(
          name="monster truck bus",
          size=(8, 6, 12),
          materials=("yellow_concrete", "black_concrete", "tinted_glass", "warped_planks"),
          features=("oversized 3 by 3 wheels", "school bus body", "tinted glass windows"),
          interior=("warped plank seats", "warped button dashboard"),
        ),
        BuildZone(
          name="horse racecourse track",
          size=(18, 4, 16),
          materials=("gray_concrete", "red_concrete", "white_concrete", "oak_fence"),
          features=("U-shaped track", "checkered curb", "starting gate", "grandstand"),
          interior=(),
        ),
      ),
      ("bus displayed on racetrack infield", "monster truck meets horse track"),
    ),
    _combo(
      "bite_combo_steamboat_island",
      "Steamboat Trip to Secret Island Base",
      ("bite_steamboat", "bite_secret_island_base"),
      "Combination challenge 4 — steamboat voyage to secret island base",
      (
        "a gray concrete steamboat with birch slab decks paddle wheels and campfire "
        "chimneys sailing toward a hidden grass island with spruce tree above an "
        "underwater purpur pillar glass aquarium base with dual water elevators"
      ),
      "aquatic",
      "ocean",
      (
        "minecraft:gray_concrete",
        "minecraft:birch_slab",
        "minecraft:water",
        "minecraft:purpur_pillar",
        "minecraft:light_blue_stained_glass_pane",
        "minecraft:spruce_log",
        "minecraft:grass_block",
      ),
      (
        BuildZone(
          name="river steamboat",
          size=(22, 12, 9),
          materials=("gray_concrete", "birch_slab", "smooth_quartz", "campfire"),
          features=("22 by 9 hull", "7 by 7 roof deck", "5 by 5 paddle wheels", "twin chimneys"),
          interior=("engine room blast furnace smoker", "birch slab passenger decks"),
        ),
        BuildZone(
          name="secret island base",
          size=(13, 16, 13),
          materials=("purpur_pillar", "light_blue_stained_glass_pane", "water", "grass_block"),
          features=("octagonal underwater glass base", "hidden grass island", "dual water elevators"),
          interior=("spruce tree surface hideout", "kelp underwater approach"),
        ),
      ),
      ("steamboat approaches secret island in ocean cube", "riverboat plus hidden underwater base"),
    ),
    _combo(
      "bite_combo_pagoda_hot_spring",
      "Pagoda with Hot-Spring Bath",
      ("bite_pagoda", "bite_hot_spring"),
      "Combination challenge 5 — pagoda beside tiered hot spring bath",
      (
        "a four-story mangrove pagoda with oxidized copper eaves beside a tiered "
        "soul sand hot spring basalt pool cluster L-shaped birch chalet granite roof "
        "pavilion bamboo azalea gravel garden"
      ),
      "wellness",
      "plains",
      (
        "minecraft:mangrove_planks",
        "minecraft:oxidized_cut_copper_stairs",
        "minecraft:soul_sand",
        "minecraft:basalt",
        "minecraft:polished_granite",
        "minecraft:stripped_birch_log",
        "minecraft:bamboo",
        "minecraft:grass_block",
      ),
      (
        BuildZone(
          name="four-story pagoda tower",
          size=(15, 28, 15),
          materials=("mangrove_planks", "white_wool", "oxidized_cut_copper_stairs", "stone_bricks"),
          features=("15 by 15 tapering tiers", "copper eaves verandas", "gold anvil interior"),
          interior=("barrel gold anvil shrine", "ladder between floors"),
        ),
        BuildZone(
          name="tiered hot spring bath",
          size=(23, 8, 22),
          materials=("soul_sand", "basalt", "water", "polished_granite", "birch_slab"),
          features=("five tiered pools", "L-shaped chalet pavilion", "campfire seating"),
          interior=("open air chalet birch slab floor",),
        ),
      ),
      ("pagoda overlooks rocky hot spring pools", "East Asian tower plus volcanic bath"),
    ),
  )
}

# Flat BookBuild entries for BOOK_BUILDS merge
COMBINATION_BOOK_BUILDS: dict[str, BookBuild] = {
  cid: entry.build for cid, entry in COMBINATION_BUILDS.items()
}
