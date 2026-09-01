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
  )
}

# Flat BookBuild entries for BOOK_BUILDS merge
COMBINATION_BOOK_BUILDS: dict[str, BookBuild] = {
  cid: entry.build for cid, entry in COMBINATION_BUILDS.items()
}
