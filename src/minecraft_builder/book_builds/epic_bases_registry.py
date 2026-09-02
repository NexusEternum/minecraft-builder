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
  "epic_bases_fenrir_billowing_sails": BookBuild(
    id="epic_bases_fenrir_billowing_sails",
    name="Billowing Sails",
    theme="viking",
    biome="ocean",
    caption=(
      "fenrirs tooth viking longship billowing red white striped sails oak "
      "stairs slabs blocks catching gale multi mast naval sail module"
    ),
    palette=(
      "minecraft:red_wool",
      "minecraft:white_wool",
      "minecraft:spruce_stairs",
      "minecraft:spruce_slab",
      "minecraft:oak_fence",
      "minecraft:oak_log",
    ),
    zones=(
      BuildZone(
        name="striped sails",
        size=(6, 10, 2),
        materials=("red_wool", "white_wool", "spruce_stairs", "spruce_slab"),
        features=("red white striped sails", "stairs slabs billowing shape"),
        interior=(),
      ),
    ),
    exterior_features=("fenrir billowing sails", "longship mast sails"),
    tips=("Combine stairs slabs and blocks for gale caught sails",),
  ),
  "epic_bases_fenrir_boat_ribs": BookBuild(
    id="epic_bases_fenrir_boat_ribs",
    name="Boat Ribs Hull Frame",
    theme="viking",
    biome="ocean",
    caption=(
      "fenrirs tooth viking longship boat ribs U shaped hull skeleton "
      "spruce dark oak frame sets scale outline naval construction module"
    ),
    palette=(
      "minecraft:spruce_planks",
      "minecraft:dark_oak_planks",
      "minecraft:spruce_stairs",
      "minecraft:oak_log",
    ),
    zones=(
      BuildZone(
        name="hull ribs",
        size=(10, 4, 6),
        materials=("spruce_planks", "dark_oak_planks", "spruce_stairs"),
        features=("U shaped rib skeleton", "hull outline frame"),
        interior=(),
      ),
    ),
    exterior_features=("fenrir boat ribs", "longship hull skeleton"),
    tips=("Ribs set scale decide base size before building",),
  ),
  "epic_bases_fenrir_storage_cabin": BookBuild(
    id="epic_bases_fenrir_storage_cabin",
    name="Deck Storage Cabin",
    theme="viking",
    biome="ocean",
    caption=(
      "fenrirs tooth viking longship deck storage cabin small wooden hut "
      "spruce planks chest quick resupply naval deck module"
    ),
    palette=(
      "minecraft:spruce_planks",
      "minecraft:dark_oak_planks",
      "minecraft:chest",
      "minecraft:oak_door",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="storage cabin",
        size=(4, 3, 3),
        materials=("spruce_planks", "dark_oak_planks", "chest", "oak_door"),
        features=("small deck hut", "quick resupply storage"),
        interior=("chest storage",),
      ),
    ),
    exterior_features=("fenrir storage cabin", "longship deck hut"),
    tips=("Small cabin on deck for quick resupply",),
  ),
  "epic_bases_fenrir_thatched_roof": BookBuild(
    id="epic_bases_fenrir_thatched_roof",
    name="Thatched Hay Roof",
    theme="viking",
    biome="ocean",
    caption=(
      "fenrirs tooth viking longship thatched hay bale roof uneven rotated "
      "hay bales rough thatching deck structure naval roofing module"
    ),
    palette=(
      "minecraft:hay_block",
      "minecraft:spruce_stairs",
      "minecraft:dark_oak_stairs",
      "minecraft:spruce_planks",
    ),
    zones=(
      BuildZone(
        name="hay thatch roof",
        size=(6, 3, 5),
        materials=("hay_block", "spruce_stairs", "dark_oak_stairs"),
        features=("rotated hay bale thatch", "uneven rough roof texture"),
        interior=(),
      ),
    ),
    exterior_features=("fenrir thatched roofing", "longship hay roof"),
    tips=("Rotate hay bales for rough thatching look", "Fire hazard decorative"),
  ),
  "epic_bases_fenrir_bunk_beds": BookBuild(
    id="epic_bases_fenrir_bunk_beds",
    name="Crew Bunk Beds",
    theme="viking",
    biome="ocean",
    caption=(
      "fenrirs tooth viking longship crew bunk bed dorm stacked green beds "
      "vertical sleeping quarters fit many sailors naval interior module"
    ),
    palette=(
      "minecraft:green_bed",
      "minecraft:spruce_planks",
      "minecraft:ladder",
      "minecraft:torch",
      "minecraft:chest",
    ),
    zones=(
      BuildZone(
        name="bunk dorm",
        size=(4, 4, 3),
        materials=("green_bed", "spruce_planks", "ladder"),
        features=("stacked bunk beds", "crew sleeping dorm"),
        interior=("green beds", "ladder access"),
      ),
    ),
    exterior_features=("fenrir bunk beds", "longship crew quarters"),
    tips=("Stack beds vertically to fit maximum crew",),
  ),
  "epic_bases_fenrir_map_table": BookBuild(
    id="epic_bases_fenrir_map_table",
    name="Battle Map Table",
    theme="viking",
    biome="ocean",
    caption=(
      "fenrirs tooth viking longship battle room map table cartography tables "
      "filled map war planning naval strategy interior module"
    ),
    palette=(
      "minecraft:cartography_table",
      "minecraft:spruce_planks",
      "minecraft:dark_oak_planks",
      "minecraft:item_frame",
      "minecraft:lantern",
      "minecraft:filled_map",
    ),
    zones=(
      BuildZone(
        name="map room",
        size=(6, 2, 5),
        materials=("cartography_table", "spruce_planks", "item_frame", "lantern"),
        features=("large map table", "cartography planning surface"),
        interior=("battle room map table",),
      ),
    ),
    exterior_features=("fenrir map table", "longship battle room"),
    tips=("Cartography tables and filled maps for war planning",),
  ),
  "epic_bases_fenrir_crossbeams": BookBuild(
    id="epic_bases_fenrir_crossbeams",
    name="Deck Crossbeams",
    theme="viking",
    biome="ocean",
    caption=(
      "fenrirs tooth viking longship decorative crossbeams X shaped spruce "
      "logs supporting hay thatched roof deck structure naval module"
    ),
    palette=(
      "minecraft:spruce_log",
      "minecraft:dark_oak_log",
      "minecraft:spruce_fence",
      "minecraft:hay_block",
    ),
    zones=(
      BuildZone(
        name="crossbeam supports",
        size=(5, 4, 5),
        materials=("spruce_log", "dark_oak_log", "spruce_fence"),
        features=("X shaped crossbeams", "roof structural supports"),
        interior=(),
      ),
    ),
    exterior_features=("fenrir crossbeams", "longship deck supports"),
    tips=("Crossbeams support thatched roof structure",),
  ),
  "epic_bases_fenrir_throne_room": BookBuild(
    id="epic_bases_fenrir_throne_room",
    name="Ship Throne Room",
    theme="viking",
    biome="ocean",
    caption=(
      "fenrirs tooth viking longship throne room emerald green floor wooden "
      "pillars candles majestic captain chamber guarded by emerald wolf module"
    ),
    palette=(
      "minecraft:emerald_block",
      "minecraft:dark_oak_planks",
      "minecraft:spruce_log",
      "minecraft:candle",
      "minecraft:gold_block",
      "minecraft:red_carpet",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="throne chamber",
        size=(7, 4, 6),
        materials=("emerald_block", "dark_oak_planks", "spruce_log", "gold_block"),
        features=("emerald green floor", "wooden pillar hall", "captain throne"),
        interior=("candles", "red carpet", "lanterns"),
      ),
    ),
    exterior_features=("fenrir throne room", "longship captain chamber"),
    tips=("Emerald wolf guards entrance to throne room",),
  ),
  "epic_bases_fenrir_tnt_cannon_redstone": BookBuild(
    id="epic_bases_fenrir_tnt_cannon_redstone",
    name="TNT Cannon Redstone",
    theme="viking",
    biome="ocean",
    caption=(
      "fenrirs tooth viking longship tnt artillery cannon redstone repeaters "
      "dispensers cauldron grindstone firing circuit explosive naval weapon module"
    ),
    palette=(
      "minecraft:dark_oak_planks",
      "minecraft:dispenser",
      "minecraft:tnt",
      "minecraft:redstone_repeater",
      "minecraft:redstone_dust",
      "minecraft:redstone_torch",
      "minecraft:cauldron",
      "minecraft:grindstone",
      "minecraft:stone_button",
      "minecraft:water",
    ),
    zones=(
      BuildZone(
        name="cannon frame",
        size=(6, 3, 4),
        materials=("dark_oak_planks", "dispenser", "tnt", "cauldron", "grindstone"),
        features=("six upward dispensers", "cauldron grindstone barrel"),
        interior=("tnt loaded dispensers",),
      ),
      BuildZone(
        name="redstone circuit",
        size=(8, 2, 3),
        materials=("redstone_repeater", "redstone_dust", "redstone_torch", "stone_button"),
        features=("nine repeaters four tick delay", "firing button circuit"),
        interior=(),
      ),
    ),
    exterior_features=("fenrir tnt cannon redstone", "longship artillery mechanism"),
    tips=("Fill dispensers with TNT use water to protect ship",),
  ),
  # --- Ancient Mummy's Tomb (Professor Shelly Sande) ---
  "epic_bases_tomb_desert_oasis": BookBuild(
    id="epic_bases_tomb_desert_oasis",
    name="Desert Oasis",
    theme="desert",
    biome="desert",
    caption=(
      "an ancient mummys tomb desert oasis with tall acacia trees colorful "
      "plants pooling water and vibrant desert ecosystem exterior module"
    ),
    palette=(
      "minecraft:sand",
      "minecraft:sandstone",
      "minecraft:water",
      "minecraft:grass_block",
      "minecraft:acacia_leaves",
      "minecraft:acacia_log",
      "minecraft:cactus",
      "minecraft:dead_bush",
      "minecraft:orange_tulip",
    ),
    zones=(
      BuildZone(
        name="oasis pool",
        size=(8, 2, 8),
        materials=("sand", "water", "grass_block"),
        features=("pooling water basin", "sand ring", "lush grass patch"),
        interior=(),
      ),
      BuildZone(
        name="oasis trees",
        size=(4, 6, 4),
        materials=("acacia_log", "acacia_leaves", "cactus"),
        features=("tall acacia trees", "colorful desert plants"),
        interior=(),
      ),
    ),
    exterior_features=("desert tomb oasis", "vibrant ecosystem in dunes"),
    tips=("Trees plants and water signal rich oasis",),
  ),
  "epic_bases_tomb_water_bearer_statue": BookBuild(
    id="epic_bases_tomb_water_bearer_statue",
    name="Water Bearer Statue",
    theme="desert",
    biome="desert",
    caption=(
      "an ancient mummys tomb water bearer statue carved in red sandstone "
      "pouring water from jugs into vertical blue channel cliff facade module"
    ),
    palette=(
      "minecraft:red_sandstone",
      "minecraft:orange_terracotta",
      "minecraft:water",
      "minecraft:sandstone",
      "minecraft:smooth_sandstone",
      "minecraft:blue_stained_glass",
    ),
    zones=(
      BuildZone(
        name="water bearer figure",
        size=(4, 10, 3),
        materials=("red_sandstone", "orange_terracotta", "smooth_sandstone"),
        features=("humanoid statue with raised jugs", "carved cliff facade"),
        interior=(),
      ),
      BuildZone(
        name="water channel",
        size=(2, 8, 1),
        materials=("water", "blue_stained_glass"),
        features=("vertical water pour", "blue glass channel"),
        interior=(),
      ),
    ),
    exterior_features=("tomb water bearer statues", "cliff carved pourers"),
    tips=("Statues pour water into central channel",),
  ),
  "epic_bases_tomb_fire_bearer_statue": BookBuild(
    id="epic_bases_tomb_fire_bearer_statue",
    name="Fire Bearer Statue",
    theme="desert",
    biome="desert",
    caption=(
      "an ancient mummys tomb fire bearer statue holding campfires overlooking "
      "sandstone walkway desert temple exterior module"
    ),
    palette=(
      "minecraft:red_sandstone",
      "minecraft:orange_terracotta",
      "minecraft:campfire",
      "minecraft:sandstone",
      "minecraft:smooth_sandstone",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="fire bearer figure",
        size=(3, 8, 3),
        materials=("red_sandstone", "orange_terracotta", "campfire"),
        features=("statue holding lit campfire", "overlooks walkway"),
        interior=(),
      ),
    ),
    exterior_features=("tomb fire bearer statues", "campfire torch bearers"),
    tips=("Fire bearer statues line main walkway",),
  ),
  "epic_bases_tomb_grand_entrance": BookBuild(
    id="epic_bases_tomb_grand_entrance",
    name="Tomb Grand Entrance",
    theme="desert",
    biome="desert",
    caption=(
      "an ancient mummys tomb grand entrance ornate sandstone doorway recessed "
      "in red cliff facade with blue banners desert temple module"
    ),
    palette=(
      "minecraft:red_sandstone",
      "minecraft:sandstone",
      "minecraft:chiseled_sandstone",
      "minecraft:smooth_sandstone",
      "minecraft:blue_banner",
      "minecraft:orange_glazed_terracotta",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="cliff entrance",
        size=(8, 10, 4),
        materials=("red_sandstone", "sandstone", "chiseled_sandstone"),
        features=("recessed ornate doorway", "cliff carved facade", "blue banners"),
        interior=(),
      ),
    ),
    exterior_features=("tomb grand entrance", "imposing pharaoh doorway"),
    tips=("Recessed entrance in red sandstone cliff",),
  ),
  "epic_bases_tomb_pillared_river": BookBuild(
    id="epic_bases_tomb_pillared_river",
    name="Pillared River Walk",
    theme="desert",
    biome="desert",
    caption=(
      "an ancient mummys tomb pillared river walk with tall white quartz columns "
      "blue banners and narrow water channels between parallel walkways"
    ),
    palette=(
      "minecraft:quartz_block",
      "minecraft:quartz_pillar",
      "minecraft:smooth_quartz",
      "minecraft:blue_banner",
      "minecraft:water",
      "minecraft:sandstone",
      "minecraft:red_sandstone",
    ),
    zones=(
      BuildZone(
        name="pillar colonnade",
        size=(12, 8, 4),
        materials=("quartz_pillar", "quartz_block", "blue_banner"),
        features=("tall white columns", "blue banner flags", "parallel walkways"),
        interior=(),
      ),
      BuildZone(
        name="water channels",
        size=(12, 1, 2),
        materials=("water", "sandstone"),
        features=("narrow rivers between pillars",),
        interior=(),
      ),
    ),
    exterior_features=("rivers flanked by pillars", "tomb processional walk"),
    tips=("Water channels run between pillar rows",),
  ),
  "epic_bases_tomb_fire_beacons": BookBuild(
    id="epic_bases_tomb_fire_beacons",
    name="Desert Fire Beacons",
    theme="desert",
    biome="desert",
    caption=(
      "an ancient mummys tomb mob repelling fire beacon perimeter with "
      "campfires on sandstone pedestals around desert oasis edge"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:smooth_sandstone",
      "minecraft:campfire",
      "minecraft:sand",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="beacon ring",
        size=(10, 3, 10),
        materials=("sandstone", "campfire", "sand"),
        features=("campfire pedestals on perimeter", "mob repelling ring"),
        interior=(),
      ),
    ),
    exterior_features=("mob repelling fire beacons", "oasis perimeter campfires"),
    tips=("Strategic campfires keep mobs away from oasis",),
  ),
  "epic_bases_tomb_library": BookBuild(
    id="epic_bases_tomb_library",
    name="Tomb Library",
    theme="desert",
    biome="underground",
    caption=(
      "an ancient mummys tomb underground library with rows of bookshelves "
      "sandstone walls and ancient mystery research room interior module"
    ),
    palette=(
      "minecraft:bookshelf",
      "minecraft:sandstone",
      "minecraft:chiseled_sandstone",
      "minecraft:smooth_sandstone",
      "minecraft:torch",
      "minecraft:red_carpet",
    ),
    zones=(
      BuildZone(
        name="library shelves",
        size=(8, 4, 6),
        materials=("bookshelf", "sandstone", "red_carpet"),
        features=("rows of bookshelves", "ancient book storage"),
        interior=("bookshelf walls",),
      ),
    ),
    exterior_features=("hidden tomb library", "underground scholarly room"),
    tips=("Old books hold answers to ancient mysteries",),
  ),
  "epic_bases_tomb_tree_farm": BookBuild(
    id="epic_bases_tomb_tree_farm",
    name="Indoor Tree Farm",
    theme="desert",
    biome="underground",
    caption=(
      "an ancient mummys tomb underground indoor tree farm with acacia and "
      "oak saplings grown under sandstone ceiling base wood supply module"
    ),
    palette=(
      "minecraft:grass_block",
      "minecraft:dirt",
      "minecraft:oak_log",
      "minecraft:oak_leaves",
      "minecraft:acacia_log",
      "minecraft:acacia_leaves",
      "minecraft:sandstone",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="tree grove",
        size=(8, 6, 6),
        materials=("grass_block", "oak_log", "acacia_log", "oak_leaves", "acacia_leaves"),
        features=("indoor grown trees", "dirt floor grove"),
        interior=(),
      ),
    ),
    exterior_features=("tomb indoor tree farm", "underground wood supply"),
    tips=("Grow all wood your base needs indoors",),
  ),
  "epic_bases_tomb_royal_bedchamber": BookBuild(
    id="epic_bases_tomb_royal_bedchamber",
    name="Royal Bedchamber",
    theme="desert",
    biome="underground",
    caption=(
      "an ancient mummys tomb royal bedchamber with pharaoh sarcophagus yellow "
      "blue terracotta patterns red bed preserved mummy chamber interior module"
    ),
    palette=(
      "minecraft:yellow_terracotta",
      "minecraft:blue_terracotta",
      "minecraft:orange_glazed_terracotta",
      "minecraft:chiseled_sandstone",
      "minecraft:red_bed",
      "minecraft:sandstone",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="pharaoh chamber",
        size=(7, 4, 7),
        materials=("yellow_terracotta", "blue_terracotta", "chiseled_sandstone"),
        features=("ornate floor patterns", "stone sarcophagus alcove"),
        interior=("red bed", "mummified pharaoh resting place"),
      ),
    ),
    exterior_features=("royal tomb bedchamber", "pharaoh sarcophagus room"),
    tips=("Pharaoh preserved in stone sarcophagus for eternity",),
  ),
  "epic_bases_tomb_lava_parkour": BookBuild(
    id="epic_bases_tomb_lava_parkour",
    name="Lava Parkour Course",
    theme="desert",
    biome="underground",
    caption=(
      "an ancient mummys tomb defensive lava parkour course with hot lava pits "
      "scary jumps narrow ledges and stone pillar obstacles underground module"
    ),
    palette=(
      "minecraft:lava",
      "minecraft:stone",
      "minecraft:stone_bricks",
      "minecraft:cobblestone",
      "minecraft:netherrack",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="parkour pit",
        size=(10, 6, 8),
        materials=("lava", "stone", "stone_bricks", "cobblestone"),
        features=("lava floor pits", "narrow stone ledges", "pillar jumps"),
        interior=(),
      ),
    ),
    exterior_features=("defensive parkour course", "tomb intruder trap"),
    tips=("Hot lava scary jumps and narrow ledges challenge raiders",),
  ),
  "epic_bases_tomb_defensive_maze": BookBuild(
    id="epic_bases_tomb_defensive_maze",
    name="Defensive Maze",
    theme="desert",
    biome="underground",
    caption=(
      "an ancient mummys tomb defensive stone maze with dead ends dark nooks "
      "and hostile mob spawns underground labyrinth security module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:mossy_stone_bricks",
      "minecraft:cobblestone",
      "minecraft:torch",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="stone labyrinth",
        size=(10, 3, 10),
        materials=("stone_bricks", "mossy_stone_bricks", "cobblestone"),
        features=("winding dead end corridors", "dark nook alcoves"),
        interior=("iron bar windows",),
      ),
    ),
    exterior_features=("defensive maze", "tomb raider confusion trap"),
    tips=("Unprepared adventurers get lost among dead ends",),
  ),
  "epic_bases_tomb_waterfall_exit": BookBuild(
    id="epic_bases_tomb_waterfall_exit",
    name="Waterfall Exit",
    theme="desert",
    biome="underground",
    caption=(
      "an ancient mummys tomb waterfall exit with vertical blue water column "
      "sandstone pool and secret escape route underground module"
    ),
    palette=(
      "minecraft:water",
      "minecraft:sandstone",
      "minecraft:smooth_sandstone",
      "minecraft:blue_stained_glass",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="waterfall shaft",
        size=(4, 8, 4),
        materials=("water", "sandstone", "blue_stained_glass"),
        features=("vertical waterfall column", "pool basin", "secret exit"),
        interior=(),
      ),
    ),
    exterior_features=("waterfall exit", "tomb secret escape route"),
    tips=("Waterfall provides dramatic hidden exit",),
  ),
  "epic_bases_tomb_entrance_atrium": BookBuild(
    id="epic_bases_tomb_entrance_atrium",
    name="Entrance Atrium",
    theme="desert",
    biome="desert",
    caption=(
      "an ancient mummys tomb entrance atrium with grand sandstone arches "
      "large water pool blue banners and waterfall side entrance module"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:red_sandstone",
      "minecraft:smooth_sandstone",
      "minecraft:water",
      "minecraft:blue_banner",
      "minecraft:lantern",
      "minecraft:prismarine_bricks",
    ),
    zones=(
      BuildZone(
        name="atrium pool",
        size=(10, 6, 8),
        materials=("sandstone", "water", "blue_banner", "lantern"),
        features=("large central water pool", "grand arched entrance", "blue banners"),
        interior=(),
      ),
    ),
    exterior_features=("entrance and atrium", "3000 year old temple aesthetic"),
    tips=("Grand entrance with large reflecting pool",),
  ),
  "epic_bases_tomb_daylight_doorway": BookBuild(
    id="epic_bases_tomb_daylight_doorway",
    name="Daylight Doorway",
    theme="desert",
    biome="underground",
    caption=(
      "an ancient mummys tomb daylight sensor redstone doorway with sticky "
      "pistons repeaters signal ladder and time locked secret sandstone entrance"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:red_sandstone",
      "minecraft:sticky_piston",
      "minecraft:redstone_repeater",
      "minecraft:redstone_dust",
      "minecraft:daylight_detector",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="piston door",
        size=(6, 6, 4),
        materials=("sticky_piston", "sandstone", "red_sandstone"),
        features=("L-shaped sticky piston door", "sandstone facade"),
        interior=(),
      ),
      BuildZone(
        name="redstone circuit",
        size=(6, 8, 3),
        materials=("redstone_repeater", "redstone_dust", "daylight_detector"),
        features=("signal ladder", "daylight sensor lock", "repeater timing"),
        interior=(),
      ),
    ),
    exterior_features=("daylight doorway puzzle", "time locked tomb entrance"),
    tips=("Door opens only when daylight sensor triggers",),
  ),
  "epic_bases_tomb_ladder_parkour": BookBuild(
    id="epic_bases_tomb_ladder_parkour",
    name="Ladder Parkour",
    theme="desert",
    biome="underground",
    caption=(
      "an ancient mummys tomb ladder parkour security tower with offset ladders "
      "glowstone lighting and stone brick shaft intruder deterrent module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:ladder",
      "minecraft:glowstone",
      "minecraft:cobblestone",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="ladder shaft",
        size=(4, 12, 4),
        materials=("stone_bricks", "ladder", "glowstone"),
        features=("offset ladder climbs", "vertical security shaft"),
        interior=(),
      ),
    ),
    exterior_features=("ladder parkour tower", "tomb raider deterrent"),
    tips=("Difficult ladder jumps keep intruders out",),
  ),
  "epic_bases_tomb_indoor_farm": BookBuild(
    id="epic_bases_tomb_indoor_farm",
    name="Indoor Wheat Farm",
    theme="desert",
    biome="underground",
    caption=(
      "an ancient mummys tomb indoor wheat farm with sandstone walled crop "
      "beds water source and enclosed underground food supply module"
    ),
    palette=(
      "minecraft:wheat",
      "minecraft:farmland",
      "minecraft:water",
      "minecraft:sandstone",
      "minecraft:orange_terracotta",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="crop beds",
        size=(6, 2, 4),
        materials=("wheat", "farmland", "water", "sandstone"),
        features=("wheat crop rows", "water irrigated beds", "sandstone enclosure"),
        interior=(),
      ),
    ),
    exterior_features=("indoor farming plot", "tomb food supply"),
    tips=("Enclosed crop beds inside hidden base",),
  ),
  # --- The Lofty Lab (Dr. Atticus Spark) ---
  "epic_bases_lab_floating_nether_portal": BookBuild(
    id="epic_bases_lab_floating_nether_portal",
    name="Floating Nether Portal",
    theme="steampunk",
    biome="sky",
    caption=(
      "a lofty lab floating isolated nether portal platform obsidian frame "
      "purple portal glow orange netherrack accent sky base module"
    ),
    palette=(
      "minecraft:obsidian",
      "minecraft:netherrack",
      "minecraft:nether_portal",
      "minecraft:oak_planks",
      "minecraft:dark_oak_fence",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="portal platform",
        size=(5, 5, 5),
        materials=("obsidian", "nether_portal", "netherrack", "oak_planks"),
        features=("floating isolated platform", "obsidian portal frame", "netherrack trim"),
        interior=(),
      ),
    ),
    exterior_features=("lofty lab nether portal", "floating resource gateway"),
    tips=("Unlimited nether resources from floating portal pad",),
  ),
  "epic_bases_lab_ballonet": BookBuild(
    id="epic_bases_lab_ballonet",
    name="Lab Ballonet",
    theme="steampunk",
    biome="sky",
    caption=(
      "a lofty lab steampunk ballonet hot air balloon white brown striped "
      "fabric envelope keeping floating laboratory aloft sky module"
    ),
    palette=(
      "minecraft:white_wool",
      "minecraft:brown_wool",
      "minecraft:oak_fence",
      "minecraft:dark_oak_planks",
      "minecraft:chain",
      "minecraft:barrel",
    ),
    zones=(
      BuildZone(
        name="balloon envelope",
        size=(6, 8, 6),
        materials=("white_wool", "brown_wool", "oak_fence", "chain"),
        features=("striped hot air balloon", "fabric envelope shape", "rigging chains"),
        interior=(),
      ),
    ),
    exterior_features=("lofty lab ballonets", "floating lab lift balloons"),
    tips=("Ballonets keep the airship lab afloat",),
  ),
  "epic_bases_lab_propeller": BookBuild(
    id="epic_bases_lab_propeller",
    name="Steampunk Propeller",
    theme="steampunk",
    biome="sky",
    caption=(
      "a lofty lab steampunk propeller four blade horizontal fan oak trapdoor "
      "slab wings attached to floating platform side module"
    ),
    palette=(
      "minecraft:oak_trapdoor",
      "minecraft:oak_slab",
      "minecraft:iron_block",
      "minecraft:dark_oak_fence",
      "minecraft:oak_planks",
    ),
    zones=(
      BuildZone(
        name="propeller fan",
        size=(4, 2, 4),
        materials=("oak_trapdoor", "oak_slab", "iron_block", "dark_oak_fence"),
        features=("four blade horizontal fan", "trapdoor wing blades", "iron hub"),
        interior=(),
      ),
    ),
    exterior_features=("lofty lab propellers", "decorative steampunk fans"),
    tips=("Propellers flank floating platform sides",),
  ),
  "epic_bases_lab_potions_tower": BookBuild(
    id="epic_bases_lab_potions_tower",
    name="Potions Tower",
    theme="steampunk",
    biome="sky",
    caption=(
      "a lofty lab potions room tower white concrete walls dark oak timber "
      "frame tall glass windows brewing stand sky laboratory module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:green_concrete",
      "minecraft:dark_oak_log",
      "minecraft:glass_pane",
      "minecraft:brewing_stand",
      "minecraft:cauldron",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="potions tower",
        size=(5, 10, 5),
        materials=("white_concrete", "dark_oak_log", "glass_pane", "green_concrete"),
        features=("tall tower with windows", "half timber white walls", "brewing room"),
        interior=("brewing stand", "cauldron"),
      ),
    ),
    exterior_features=("lofty lab potions room", "tower brewing laboratory"),
    tips=("Tall windowed tower for potion research",),
  ),
  "epic_bases_lab_windmill": BookBuild(
    id="epic_bases_lab_windmill",
    name="Lab Windmill",
    theme="steampunk",
    biome="sky",
    caption=(
      "a lofty lab windmill sail attachment wooden blade fan on white concrete "
      "building side steampunk sky laboratory module"
    ),
    palette=(
      "minecraft:oak_trapdoor",
      "minecraft:oak_fence",
      "minecraft:white_concrete",
      "minecraft:dark_oak_planks",
      "minecraft:barrel",
    ),
    zones=(
      BuildZone(
        name="windmill sail",
        size=(4, 5, 2),
        materials=("oak_trapdoor", "oak_fence", "white_concrete"),
        features=("wooden sail blades", "side mounted windmill", "steampunk accent"),
        interior=(),
      ),
    ),
    exterior_features=("lofty lab windmill", "building mounted sail fan"),
    tips=("Windmill decor on laboratory exterior wall",),
  ),
  "epic_bases_lab_libratory": BookBuild(
    id="epic_bases_lab_libratory",
    name="Libratory",
    theme="steampunk",
    biome="sky",
    caption=(
      "a lofty lab libratory cutaway room dense bookshelves enchanting table "
      "anvil white walls dark oak steep roof research library module"
    ),
    palette=(
      "minecraft:bookshelf",
      "minecraft:enchanting_table",
      "minecraft:anvil",
      "minecraft:white_concrete",
      "minecraft:dark_oak_stairs",
      "minecraft:dark_oak_planks",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="libratory interior",
        size=(8, 6, 6),
        materials=("bookshelf", "white_concrete", "dark_oak_stairs", "dark_oak_planks"),
        features=("dense bookshelf walls", "steep dark oak roof", "enchanting study"),
        interior=("enchanting table", "anvil", "bookshelves"),
      ),
    ),
    exterior_features=("lofty lab libratory", "library enchantment workshop"),
    tips=("Combine library enchanting and anvil repair in one room",),
  ),
  "epic_bases_lab_fumigation_chimney": BookBuild(
    id="epic_bases_lab_fumigation_chimney",
    name="Fumigation Chimney",
    theme="steampunk",
    biome="sky",
    caption=(
      "a lofty lab fumigation hut tall narrow stone brick chimney stack "
      "cobblestone smoke vent steampunk laboratory roof module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:cobblestone",
      "minecraft:cobblestone_wall",
      "minecraft:campfire",
      "minecraft:dark_oak_stairs",
    ),
    zones=(
      BuildZone(
        name="chimney stack",
        size=(2, 8, 2),
        materials=("stone_bricks", "cobblestone_wall", "campfire"),
        features=("tall narrow chimney", "fumigation smoke vent"),
        interior=(),
      ),
    ),
    exterior_features=("lofty lab fumigation hut", "laboratory chimney"),
    tips=("Tall chimney for fumigation hut aesthetic",),
  ),
  "epic_bases_lab_giant_mushroom": BookBuild(
    id="epic_bases_lab_giant_mushroom",
    name="Giant Mushroom Roof",
    theme="steampunk",
    biome="sky",
    caption=(
      "a lofty lab giant red mushroom cap roof white spotted terracotta "
      "building topper steampunk colorful industrial accent module"
    ),
    palette=(
      "minecraft:red_mushroom_block",
      "minecraft:white_wool",
      "minecraft:white_concrete",
      "minecraft:dark_oak_planks",
      "minecraft:green_concrete",
    ),
    zones=(
      BuildZone(
        name="mushroom cap",
        size=(6, 4, 6),
        materials=("red_mushroom_block", "white_wool", "white_concrete"),
        features=("giant red mushroom roof", "white spot accents", "whimsical topper"),
        interior=(),
      ),
    ),
    exterior_features=("lofty lab giant mushroom", "colorful roof accent"),
    tips=("Giant mushroom adds color to industrial theme",),
  ),
  "epic_bases_lab_victorian_tower": BookBuild(
    id="epic_bases_lab_victorian_tower",
    name="Victorian Lab Tower",
    theme="steampunk",
    biome="sky",
    caption=(
      "a lofty lab victorian tower stacked gabled roofs white concrete "
      "dark oak half timber framing blue glass windows sky laboratory module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:dark_oak_log",
      "minecraft:dark_oak_stairs",
      "minecraft:light_blue_stained_glass",
      "minecraft:green_concrete",
      "minecraft:lantern",
      "minecraft:ladder",
    ),
    zones=(
      BuildZone(
        name="victorian tower",
        size=(6, 14, 6),
        materials=("white_concrete", "dark_oak_log", "dark_oak_stairs", "light_blue_stained_glass"),
        features=("stacked gabled roofs", "half timber framing", "multi level tower"),
        interior=("ladder between floors", "lantern lighting"),
      ),
    ),
    exterior_features=("lofty lab victorian architecture", "tall stacked gables"),
    tips=("Half timber white walls with smooth stone edges",),
  ),
  # --- Airship Express ---
  "epic_bases_airship_express": BookBuild(
    id="epic_bases_airship_express",
    name="Airship Express Hull",
    theme="steampunk",
    biome="sky",
    caption=(
      "a lofty lab airship express compact green hull wooden deck fence "
      "supports connecting balloon symmetrical steampunk sky ship module"
    ),
    palette=(
      "minecraft:green_concrete",
      "minecraft:dark_oak_planks",
      "minecraft:oak_fence",
      "minecraft:spruce_stairs",
      "minecraft:barrel",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="airship hull",
        size=(8, 3, 4),
        materials=("green_concrete", "dark_oak_planks", "oak_fence"),
        features=("compact boat hull deck", "symmetrical sides", "fence balloon rigging"),
        interior=(),
      ),
    ),
    exterior_features=("airship express hull", "small speedy steampunk ship"),
    tips=("Build one side then mirror for symmetry",),
  ),
  "epic_bases_airship_engine_furnace": BookBuild(
    id="epic_bases_airship_engine_furnace",
    name="Airship Engine Furnace",
    theme="steampunk",
    biome="sky",
    caption=(
      "a lofty lab airship engine furnace stone base campfire trapdoor cover "
      "lever smoke release steampunk propulsion module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:campfire",
      "minecraft:oak_trapdoor",
      "minecraft:lever",
      "minecraft:iron_block",
    ),
    zones=(
      BuildZone(
        name="engine box",
        size=(3, 2, 3),
        materials=("stone_bricks", "campfire", "oak_trapdoor", "lever"),
        features=("campfire engine core", "trapdoor smoke cover", "lever release"),
        interior=("campfire engine",),
      ),
    ),
    exterior_features=("airship engine furnace", "thematic smoke propulsion"),
    tips=("Campfire under trapdoor powers airship thematically",),
  ),
  "epic_bases_airship_quarterdeck": BookBuild(
    id="epic_bases_airship_quarterdeck",
    name="Airship Quarterdeck",
    theme="steampunk",
    biome="sky",
    caption=(
      "a lofty lab airship quarterdeck rear deck lectern captain wheel "
      "dark oak planks lantern steampunk ship stern module"
    ),
    palette=(
      "minecraft:dark_oak_planks",
      "minecraft:lectern",
      "minecraft:oak_fence",
      "minecraft:lantern",
      "minecraft:barrel",
    ),
    zones=(
      BuildZone(
        name="quarterdeck",
        size=(4, 2, 3),
        materials=("dark_oak_planks", "lectern", "oak_fence", "lantern"),
        features=("rear captain deck", "lectern wheel helm", "stern railing"),
        interior=("lectern captain wheel",),
      ),
    ),
    exterior_features=("airship quarterdeck", "captain helm stern"),
    tips=("Lectern serves as decorative captain wheel",),
  ),
  "epic_bases_airship_balloon": BookBuild(
    id="epic_bases_airship_balloon",
    name="Airship Main Balloon",
    theme="steampunk",
    biome="sky",
    caption=(
      "a lofty lab airship main balloon white gold layered trapdoor slab "
      "fence rounded envelope cylindrical lift bag module"
    ),
    palette=(
      "minecraft:white_wool",
      "minecraft:yellow_wool",
      "minecraft:oak_trapdoor",
      "minecraft:oak_slab",
      "minecraft:oak_fence",
      "minecraft:chain",
    ),
    zones=(
      BuildZone(
        name="main balloon",
        size=(6, 8, 6),
        materials=("white_wool", "yellow_wool", "oak_trapdoor", "oak_slab", "oak_fence"),
        features=("layered rounded balloon", "white gold stripes", "trapdoor texture"),
        interior=(),
      ),
    ),
    exterior_features=("airship express balloon", "main lift envelope"),
    tips=("Layer trapdoors slabs and fences for rounded balloon",),
  ),
  "epic_bases_airship_storage_hold": BookBuild(
    id="epic_bases_airship_storage_hold",
    name="Airship Storage Hold",
    theme="steampunk",
    biome="sky",
    caption=(
      "a lofty lab airship storage hold hollow hull chest compartment "
      "lantern lit under deck cargo bay steampunk module"
    ),
    palette=(
      "minecraft:dark_oak_planks",
      "minecraft:chest",
      "minecraft:lantern",
      "minecraft:green_concrete",
      "minecraft:oak_trapdoor",
    ),
    zones=(
      BuildZone(
        name="cargo hold",
        size=(6, 3, 4),
        materials=("dark_oak_planks", "chest", "lantern", "green_concrete"),
        features=("hollow under deck storage", "chest cargo bay"),
        interior=("double chests", "lantern lighting"),
      ),
    ),
    exterior_features=("airship storage space", "under deck cargo"),
    tips=("Store chests in hollow hull below deck",),
  ),
  "epic_bases_airship_propeller": BookBuild(
    id="epic_bases_airship_propeller",
    name="Airship Propeller",
    theme="steampunk",
    biome="sky",
    caption=(
      "a lofty lab airship decorative propeller white wool ring anvil hub "
      "trapdoor blades steampunk thematic fan module"
    ),
    palette=(
      "minecraft:white_wool",
      "minecraft:anvil",
      "minecraft:oak_trapdoor",
      "minecraft:stone_button",
      "minecraft:iron_block",
    ),
    zones=(
      BuildZone(
        name="propeller ring",
        size=(4, 1, 4),
        materials=("white_wool", "anvil", "oak_trapdoor", "stone_button"),
        features=("circular propeller ring", "anvil center hub", "trapdoor blades"),
        interior=(),
      ),
    ),
    exterior_features=("airship propellers", "steampunk decorative fans"),
    tips=("Thematic propellers not functional in game",),
  ),
  # --- The Sunken Estate (Maria Trench) ---
  "epic_bases_estate_grand_dome": BookBuild(
    id="epic_bases_estate_grand_dome",
    name="Grand Underwater Dome",
    theme="underwater",
    biome="ocean",
    caption=(
      "a sunken estate grand underwater dome prismarine dark prismarine "
      "quartz lattice glass panes expansive palace crown ocean module"
    ),
    palette=(
      "minecraft:prismarine",
      "minecraft:dark_prismarine",
      "minecraft:quartz_block",
      "minecraft:glass_pane",
      "minecraft:sea_lantern",
      "minecraft:water",
    ),
    zones=(
      BuildZone(
        name="grand dome",
        size=(10, 8, 10),
        materials=("prismarine", "dark_prismarine", "quartz_block", "glass_pane"),
        features=("broad expansive glass dome", "prismarine lattice frame", "palace crown"),
        interior=(),
      ),
    ),
    exterior_features=("sunken estate grand dome", "underwater palace pinnacle"),
    tips=("Pinnacle of deep sea base awe inspiring dome",),
  ),
  "epic_bases_estate_stained_glass_wall": BookBuild(
    id="epic_bases_estate_stained_glass_wall",
    name="Stained Glass Facade",
    theme="underwater",
    biome="ocean",
    caption=(
      "a sunken estate grand stained glass window wall prismarine frame "
      "tall glass panels light filled underwater palace exterior module"
    ),
    palette=(
      "minecraft:prismarine",
      "minecraft:dark_prismarine",
      "minecraft:glass",
      "minecraft:glass_pane",
      "minecraft:quartz_block",
      "minecraft:water",
    ),
    zones=(
      BuildZone(
        name="glass facade",
        size=(6, 10, 2),
        materials=("prismarine", "glass", "glass_pane", "quartz_block"),
        features=("tall stained glass windows", "prismarine frame", "light filled wall"),
        interior=(),
      ),
    ),
    exterior_features=("grand stained glass windows", "underwater palace facade"),
    tips=("Large glass sections bring light to interior",),
  ),
  "epic_bases_estate_transfer_tunnel": BookBuild(
    id="epic_bases_estate_transfer_tunnel",
    name="Transfer Tunnel",
    theme="underwater",
    biome="ocean",
    caption=(
      "a sunken estate glass enclosed transfer tunnel connecting underwater "
      "towers prismarine walkway ocean darkness connector module"
    ),
    palette=(
      "minecraft:prismarine",
      "minecraft:dark_prismarine",
      "minecraft:glass",
      "minecraft:sea_lantern",
      "minecraft:water",
    ),
    zones=(
      BuildZone(
        name="glass tunnel",
        size=(10, 3, 3),
        materials=("prismarine", "glass", "sea_lantern"),
        features=("enclosed glass walkway", "connects domes and towers"),
        interior=("sea lantern lighting",),
      ),
    ),
    exterior_features=("transfer tunnels", "underwater connector walkways"),
    tips=("Move through ocean darkness between structures",),
  ),
  "epic_bases_estate_observation_glass": BookBuild(
    id="epic_bases_estate_observation_glass",
    name="Marine Observation Glass",
    theme="underwater",
    biome="ocean",
    caption=(
      "a sunken estate marine observation glass flat viewing panel "
      "prismarine wall inset window underwater sea life viewing module"
    ),
    palette=(
      "minecraft:prismarine",
      "minecraft:dark_prismarine",
      "minecraft:glass",
      "minecraft:water",
      "minecraft:kelp",
    ),
    zones=(
      BuildZone(
        name="observation panel",
        size=(4, 3, 1),
        materials=("prismarine", "glass", "water"),
        features=("flat marine viewing glass", "wall inset observation window"),
        interior=(),
      ),
    ),
    exterior_features=("marine observation glass", "underwater viewing panels"),
    tips=("Flat glass surfaces for watching surrounding sea",),
  ),
  "epic_bases_estate_kelp_garden": BookBuild(
    id="epic_bases_estate_kelp_garden",
    name="Kelp Garden",
    theme="underwater",
    biome="ocean",
    caption=(
      "a sunken estate kelp garden dense kelp stalks surrounding palace base "
      "sand dunes underwater landscaping ocean exterior module"
    ),
    palette=(
      "minecraft:kelp",
      "minecraft:sand",
      "minecraft:prismarine",
      "minecraft:water",
      "minecraft:seagrass",
    ),
    zones=(
      BuildZone(
        name="kelp bed",
        size=(10, 6, 8),
        materials=("kelp", "sand", "seagrass", "water"),
        features=("dense vertical kelp stalks", "sand dune floor"),
        interior=(),
      ),
    ),
    exterior_features=("kelp gardens", "underwater estate landscaping"),
    tips=("Kelp never stops growing around palace base",),
  ),
  "epic_bases_estate_skylight_tower": BookBuild(
    id="epic_bases_estate_skylight_tower",
    name="Skylight Tower",
    theme="underwater",
    biome="ocean",
    caption=(
      "a sunken estate skylight tower tall prismarine shaft transparent "
      "glass top bringing light into underwater base connector module"
    ),
    palette=(
      "minecraft:prismarine",
      "minecraft:dark_prismarine",
      "minecraft:glass",
      "minecraft:sea_lantern",
      "minecraft:water",
    ),
    zones=(
      BuildZone(
        name="skylight shaft",
        size=(3, 12, 3),
        materials=("prismarine", "glass", "sea_lantern"),
        features=("tall narrow tower", "transparent glass skylight cap"),
        interior=("light shaft to interior",),
      ),
    ),
    exterior_features=("skylight tower", "underwater light connector"),
    tips=("Glass top brings daylight into deep base",),
  ),
  "epic_bases_estate_deco_archway": BookBuild(
    id="epic_bases_estate_deco_archway",
    name="Art Deco Archway",
    theme="underwater",
    biome="ocean",
    caption=(
      "a sunken estate art deco archway pointed prismarine quartz spiral "
      "arch entrance small windows soaring columns underwater module"
    ),
    palette=(
      "minecraft:prismarine",
      "minecraft:dark_prismarine",
      "minecraft:quartz_block",
      "minecraft:quartz_stairs",
      "minecraft:glass_pane",
    ),
    zones=(
      BuildZone(
        name="deco arch",
        size=(5, 8, 3),
        materials=("prismarine", "quartz_block", "quartz_stairs", "glass_pane"),
        features=("pointed art deco arch", "spiraling archway", "small windows"),
        interior=(),
      ),
    ),
    exterior_features=("art deco archway", "underwater skyscraper entrance"),
    tips=("Art deco small windows and soaring columns",),
  ),
  "epic_bases_estate_deco_tower": BookBuild(
    id="epic_bases_estate_deco_tower",
    name="Art Deco Tower",
    theme="underwater",
    biome="ocean",
    caption=(
      "a sunken estate art deco tower multi story prismarine quartz "
      "arched windows vertical white accents underwater skyscraper module"
    ),
    palette=(
      "minecraft:prismarine",
      "minecraft:dark_prismarine",
      "minecraft:quartz_block",
      "minecraft:quartz_stairs",
      "minecraft:glass_pane",
      "minecraft:sea_lantern",
    ),
    zones=(
      BuildZone(
        name="deco tower",
        size=(6, 14, 6),
        materials=("prismarine", "dark_prismarine", "quartz_block", "glass_pane"),
        features=("multi story art deco tower", "arched window rows", "white vertical stripes"),
        interior=("sea lantern lobby",),
      ),
    ),
    exterior_features=("art deco tower section", "underwater skyscraper facade"),
    tips=("Resemble underwater art deco skyscrapers",),
  ),
  "epic_bases_estate_aquarium_lounge": BookBuild(
    id="epic_bases_estate_aquarium_lounge",
    name="Aquarium Lounge",
    theme="underwater",
    biome="ocean",
    caption=(
      "a sunken estate aquarium lounge interior brown couch seating "
      "decorative floor tiling prismarine walls fish viewing room module"
    ),
    palette=(
      "minecraft:prismarine",
      "minecraft:dark_prismarine",
      "minecraft:quartz_block",
      "minecraft:blue_terracotta",
      "minecraft:white_terracotta",
      "minecraft:oak_stairs",
      "minecraft:glass",
    ),
    zones=(
      BuildZone(
        name="lounge room",
        size=(8, 4, 6),
        materials=("prismarine", "blue_terracotta", "white_terracotta", "oak_stairs"),
        features=("decorative checkerboard tiling", "couch seating alcove", "glass fish views"),
        interior=("lounge seating", "aquarium viewing"),
      ),
    ),
    exterior_features=("aquarium lounge", "underwater estate interior"),
    tips=("Two block tile patterns for visual distinction",),
  ),
  "epic_bases_estate_coral_garden": BookBuild(
    id="epic_bases_estate_coral_garden",
    name="Indoor Coral Garden",
    theme="underwater",
    biome="ocean",
    caption=(
      "a sunken estate indoor coral garden pink blue yellow coral blocks "
      "seagrass lush underwater conservatory decorative room module"
    ),
    palette=(
      "minecraft:brain_coral_block",
      "minecraft:tube_coral_block",
      "minecraft:horn_coral_block",
      "minecraft:fire_coral_block",
      "minecraft:seagrass",
      "minecraft:prismarine",
      "minecraft:water",
    ),
    zones=(
      BuildZone(
        name="coral conservatory",
        size=(8, 4, 6),
        materials=("brain_coral_block", "tube_coral_block", "horn_coral_block", "seagrass"),
        features=("colorful coral clusters", "lush indoor garden", "conservatory room"),
        interior=(),
      ),
    ),
    exterior_features=("indoor coral garden", "underwater estate decor"),
    tips=("Corals add color and do not need water to survive",),
  ),
  "epic_bases_estate_drowned_farm": BookBuild(
    id="epic_bases_estate_drowned_farm",
    name="Drowned Mob Farm",
    theme="underwater",
    biome="ocean",
    caption=(
      "a sunken estate drowned mob farm turtle egg trapdoor magma ring "
      "glass villager chamber hopper collection trident gold farm module"
    ),
    palette=(
      "minecraft:magma_block",
      "minecraft:turtle_egg",
      "minecraft:oak_trapdoor",
      "minecraft:glass",
      "minecraft:water",
      "minecraft:powered_rail",
      "minecraft:hopper",
      "minecraft:chest",
      "minecraft:redstone_torch",
    ),
    zones=(
      BuildZone(
        name="spawn chamber",
        size=(5, 12, 5),
        materials=("magma_block", "turtle_egg", "oak_trapdoor", "glass", "water"),
        features=("5x5 drowned spawn pit", "turtle egg bait", "magma kill ring"),
        interior=("villager bait chamber",),
      ),
      BuildZone(
        name="collection room",
        size=(5, 2, 5),
        materials=("hopper", "chest", "powered_rail", "redstone_torch"),
        features=("hopper chest loot collection", "powered rail minecart"),
        interior=("trident gold loot",),
      ),
    ),
    exterior_features=("drowned mob farm", "underwater trident farm"),
    tips=("5x5 wide 12 blocks tall villager bait drowned farm",),
  ),
  # --- The Exchange (Kat Seeker) ---
  "epic_bases_exchange_support_platform": BookBuild(
    id="epic_bases_exchange_support_platform",
    name="Pyramid Support Platform",
    theme="jungle",
    biome="jungle",
    caption=(
      "the exchange jungle pyramid wooden support platform observation research "
      "room built into stone temple side field research station module"
    ),
    palette=(
      "minecraft:oak_planks",
      "minecraft:spruce_planks",
      "minecraft:oak_fence",
      "minecraft:stone_bricks",
      "minecraft:mossy_stone_bricks",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="observation platform",
        size=(6, 3, 4),
        materials=("oak_planks", "spruce_planks", "oak_fence", "stone_bricks"),
        features=("wood platform on pyramid side", "research observation room"),
        interior=("lantern lighting",),
      ),
    ),
    exterior_features=("exchange support structures", "pyramid research platforms"),
    tips=("Wooden platforms serve as observation and research rooms",),
  ),
  "epic_bases_exchange_eternal_flame": BookBuild(
    id="epic_bases_exchange_eternal_flame",
    name="Eternal Flame Tower",
    theme="jungle",
    biome="jungle",
    caption=(
      "the exchange eternal flame tower netherrack fire never extinguished "
      "imported nether block jungle research beacon module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:cobblestone",
      "minecraft:netherrack",
      "minecraft:fire",
      "minecraft:oak_fence",
    ),
    zones=(
      BuildZone(
        name="flame tower",
        size=(3, 8, 3),
        materials=("stone_bricks", "netherrack", "fire", "oak_fence"),
        features=("tall stone tower", "eternal netherrack flame top"),
        interior=(),
      ),
    ),
    exterior_features=("eternal flame beacon", "exchange research tower"),
    tips=("Netherrack flame imported through End portal",),
  ),
  "epic_bases_exchange_redstone_altar": BookBuild(
    id="epic_bases_exchange_redstone_altar",
    name="Redstone Altar",
    theme="jungle",
    biome="jungle",
    caption=(
      "the exchange redstone altar ancient time tracking experiment glowing "
      "redstone block stone platform jungle research module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:mossy_stone_bricks",
      "minecraft:redstone_block",
      "minecraft:redstone_torch",
      "minecraft:chiseled_stone_bricks",
    ),
    zones=(
      BuildZone(
        name="altar platform",
        size=(4, 2, 4),
        materials=("stone_bricks", "redstone_block", "chiseled_stone_bricks"),
        features=("glowing redstone altar", "ancient time experiment"),
        interior=(),
      ),
    ),
    exterior_features=("redstone altar", "exchange archaeology experiment"),
    tips=("Experimenting with altars to track passing time",),
  ),
  "epic_bases_exchange_remnant_memorial": BookBuild(
    id="epic_bases_exchange_remnant_memorial",
    name="Remnant Memorial",
    theme="jungle",
    biome="jungle",
    caption=(
      "the exchange remnant memorial skeleton skull statue stone pedestal "
      "fallen adventurer tribute jungle village module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:cobblestone",
      "minecraft:skeleton_skull",
      "minecraft:stone_brick_stairs",
      "minecraft:vine",
    ),
    zones=(
      BuildZone(
        name="skull memorial",
        size=(2, 3, 2),
        materials=("stone_bricks", "skeleton_skull", "stone_brick_stairs"),
        features=("skull head statue", "stone pedestal memorial"),
        interior=(),
      ),
    ),
    exterior_features=("remnant memorial statues", "fallen adventurer tribute"),
    tips=("Skeleton heads memorial for lost explorers",),
  ),
  "epic_bases_exchange_lily_pad_path": BookBuild(
    id="epic_bases_exchange_lily_pad_path",
    name="Lily Pad Path",
    theme="jungle",
    biome="jungle",
    caption=(
      "the exchange lily pad path water walkway stepping stones jungle "
      "village pond crossing research station module"
    ),
    palette=(
      "minecraft:lily_pad",
      "minecraft:water",
      "minecraft:jungle_leaves",
      "minecraft:vine",
      "minecraft:oak_fence",
    ),
    zones=(
      BuildZone(
        name="pond crossing",
        size=(8, 1, 3),
        materials=("lily_pad", "water", "oak_fence"),
        features=("lily pad stepping path", "water village crossing"),
        interior=(),
      ),
    ),
    exterior_features=("lily pad paths", "jungle water walkways"),
    tips=("Lily pads form paths across village ponds",),
  ),
  "epic_bases_exchange_end_stepwell": BookBuild(
    id="epic_bases_exchange_end_stepwell",
    name="End Portal Stepwell",
    theme="jungle",
    biome="jungle",
    caption=(
      "the exchange end portal stepwell descending stone stairs underground "
      "end portal room chorus pillars water basin stronghold module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:mossy_stone_bricks",
      "minecraft:end_portal_frame",
      "minecraft:end_stone_bricks",
      "minecraft:water",
      "minecraft:purpur_block",
    ),
    zones=(
      BuildZone(
        name="stepwell shaft",
        size=(8, 6, 8),
        materials=("stone_bricks", "mossy_stone_bricks", "water"),
        features=("descending stair well", "builds down toward portal"),
        interior=(),
      ),
      BuildZone(
        name="portal chamber",
        size=(5, 3, 5),
        materials=("end_portal_frame", "end_stone_bricks", "purpur_block"),
        features=("end portal frame", "underground portal room"),
        interior=("chorus pillar accents",),
      ),
    ),
    exterior_features=("end portal stepwell", "exchange dig site core"),
    tips=("Stepwell descends to repaired End portal",),
  ),
  "epic_bases_exchange_jungle_statue": BookBuild(
    id="epic_bases_exchange_jungle_statue",
    name="Jungle Stone Statue",
    theme="jungle",
    biome="jungle",
    caption=(
      "the exchange jungle stone statue aged mossy artifact aztec mayan "
      "inspired carved figure temple decor research module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:mossy_stone_bricks",
      "minecraft:cobblestone",
      "minecraft:vine",
    ),
    zones=(
      BuildZone(
        name="ancient statue",
        size=(3, 6, 3),
        materials=("stone_bricks", "mossy_stone_bricks", "vine"),
        features=("tall blocky statue", "aged mossy artifact look"),
        interior=(),
      ),
    ),
    exterior_features=("jungle stone statue", "aztec mayan artifact decor"),
    tips=("Statues look like aged jungle artifacts",),
  ),
  "epic_bases_exchange_jungle_cabin": BookBuild(
    id="epic_bases_exchange_jungle_cabin",
    name="Jungle Stilt Cabin",
    theme="jungle",
    biome="jungle",
    caption=(
      "the exchange jungle stilt cabin yellow hay roof oak spruce acacia "
      "log variety wooden platform over water research hut module"
    ),
    palette=(
      "minecraft:oak_log",
      "minecraft:spruce_log",
      "minecraft:acacia_log",
      "minecraft:oak_planks",
      "minecraft:hay_block",
      "minecraft:oak_fence",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="stilt cabin",
        size=(6, 5, 5),
        materials=("oak_log", "spruce_log", "acacia_log", "hay_block", "oak_planks"),
        features=("multi log type walls", "yellow hay roof", "platform over water"),
        interior=("lantern lighting",),
      ),
    ),
    exterior_features=("jungle research cabin", "stilt platform hut"),
    tips=("Mix oak spruce acacia logs for variety",),
  ),
  "epic_bases_exchange_stilt_house": BookBuild(
    id="epic_bases_exchange_stilt_house",
    name="Trading Stilt House",
    theme="jungle",
    biome="jungle",
    caption=(
      "the exchange trading village stilt house yellow hay tiered roof wooden "
      "poles crop space below villager shelter jungle module"
    ),
    palette=(
      "minecraft:oak_planks",
      "minecraft:oak_fence",
      "minecraft:hay_block",
      "minecraft:ladder",
      "minecraft:composter",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="village stilt house",
        size=(5, 6, 5),
        materials=("oak_planks", "oak_fence", "hay_block", "ladder"),
        features=("tall stilt poles", "tiered hay roof", "crop space below"),
        interior=("composter job block",),
      ),
    ),
    exterior_features=("trading stilt houses", "exchange village homes"),
    tips=("Stilts maximize crop space and villager safety",),
  ),
  "epic_bases_exchange_streetlight": BookBuild(
    id="epic_bases_exchange_streetlight",
    name="Jungle Streetlight",
    theme="jungle",
    biome="jungle",
    caption=(
      "the exchange jungle streetlight stone pillar lantern posts mob "
      "prevention lighting trading village path module"
    ),
    palette=(
      "minecraft:cobblestone",
      "minecraft:stone_brick_wall",
      "minecraft:lantern",
      "minecraft:oak_fence",
    ),
    zones=(
      BuildZone(
        name="lantern post",
        size=(2, 4, 2),
        materials=("cobblestone", "stone_brick_wall", "lantern", "oak_fence"),
        features=("stone pillar streetlight", "lantern mob prevention"),
        interior=(),
      ),
    ),
    exterior_features=("jungle streetlights", "village path lighting"),
    tips=("Lighting keeps mobs from spawning in village",),
  ),
  "epic_bases_exchange_market_stall": BookBuild(
    id="epic_bases_exchange_market_stall",
    name="Villager Market Stall",
    theme="jungle",
    biome="jungle",
    caption=(
      "the exchange villager market stall wooden roof counter cartographer "
      "trading post thriving economy jungle village module"
    ),
    palette=(
      "minecraft:oak_planks",
      "minecraft:spruce_planks",
      "minecraft:cartography_table",
      "minecraft:chest",
      "minecraft:lantern",
      "minecraft:oak_fence",
    ),
    zones=(
      BuildZone(
        name="market stall",
        size=(4, 3, 3),
        materials=("oak_planks", "spruce_planks", "cartography_table", "oak_fence"),
        features=("open front trading stall", "wooden counter roof"),
        interior=("cartography table", "chest storage"),
      ),
    ),
    exterior_features=("villager market stall", "exchange trading economy"),
    tips=("Provide job blocks like cartography tables for villagers",),
  ),
  "epic_bases_exchange_aerial_walkway": BookBuild(
    id="epic_bases_exchange_aerial_walkway",
    name="Aerial Walkway",
    theme="jungle",
    biome="jungle",
    caption=(
      "the exchange aerial walkway wooden bridge oak fence barriers lantern "
      "posts connecting platforms jungle research village module"
    ),
    palette=(
      "minecraft:oak_planks",
      "minecraft:oak_fence",
      "minecraft:lantern",
      "minecraft:jungle_leaves",
      "minecraft:vine",
    ),
    zones=(
      BuildZone(
        name="bridge span",
        size=(10, 2, 3),
        materials=("oak_planks", "oak_fence", "lantern"),
        features=("elevated wooden bridge", "fence barrier railings"),
        interior=("lantern posts",),
      ),
    ),
    exterior_features=("aerial walkways", "exchange platform bridges"),
    tips=("Barriers prevent falling from aerial walkways",),
  ),
  "epic_bases_exchange_tiered_garden": BookBuild(
    id="epic_bases_exchange_tiered_garden",
    name="Tiered Crop Garden",
    theme="jungle",
    biome="jungle",
    caption=(
      "the exchange tiered crop garden yellow hay pyramid terraces wheat "
      "carrots flowering foliage jungle village farm module"
    ),
    palette=(
      "minecraft:hay_block",
      "minecraft:wheat",
      "minecraft:carrots",
      "minecraft:oak_planks",
      "minecraft:oak_fence",
      "minecraft:dandelion",
    ),
    zones=(
      BuildZone(
        name="tiered terraces",
        size=(8, 4, 6),
        materials=("hay_block", "wheat", "carrots", "oak_planks"),
        features=("stepped crop terraces", "flowering foliage edges"),
        interior=(),
      ),
    ),
    exterior_features=("tiered garden pyramid", "exchange crop terraces"),
    tips=("Tiered gardens around ancient pyramid",),
  ),
  "epic_bases_exchange_cryptic_floor": BookBuild(
    id="epic_bases_exchange_cryptic_floor",
    name="Cryptic Floor Engraving",
    theme="jungle",
    biome="jungle",
    caption=(
      "the exchange cryptic floor engraving blue white maze tile pattern "
      "aztec decorative stone floor research chamber module"
    ),
    palette=(
      "minecraft:blue_terracotta",
      "minecraft:white_terracotta",
      "minecraft:light_blue_terracotta",
      "minecraft:stone_bricks",
      "minecraft:chiseled_stone_bricks",
    ),
    zones=(
      BuildZone(
        name="engraved floor",
        size=(6, 1, 6),
        materials=("blue_terracotta", "white_terracotta", "light_blue_terracotta"),
        features=("maze floor pattern", "cryptic engravings"),
        interior=(),
      ),
    ),
    exterior_features=("cryptic floor patterns", "exchange decorative tiling"),
    tips=("Floor patterns add aesthetic mystery",),
  ),
  # --- The Cube (Steven Stargazer) ---
  "epic_bases_cube_force_field_maw": BookBuild(
    id="epic_bases_cube_force_field_maw",
    name="Cube Force Field Maw",
    theme="sci-fi",
    biome="wasteland",
    caption=(
      "the cube force field maw glowing purple barrier narrow entry white "
      "obsidian frame alien crash site fortress entrance module"
    ),
    palette=(
      "minecraft:purple_stained_glass",
      "minecraft:purple_stained_glass_pane",
      "minecraft:obsidian",
      "minecraft:white_concrete",
      "minecraft:red_nether_bricks",
      "minecraft:sea_lantern",
    ),
    zones=(
      BuildZone(
        name="force field gate",
        size=(4, 8, 2),
        materials=("purple_stained_glass", "obsidian", "white_concrete"),
        features=("glowing purple force field wall", "narrow impregnable entry"),
        interior=(),
      ),
    ),
    exterior_features=("cube maw force field", "alien fortress entrance"),
    tips=("Purple glass force field blocks entry without elytra",),
  ),
  "epic_bases_cube_radiant_beacon": BookBuild(
    id="epic_bases_cube_radiant_beacon",
    name="Radiant Beacon Base",
    theme="sci-fi",
    biome="wasteland",
    caption=(
      "the cube radiant lighting orange glow beacon molten light base "
      "mob attracting crash site alien structure module"
    ),
    palette=(
      "minecraft:orange_stained_glass",
      "minecraft:glowstone",
      "minecraft:lava",
      "minecraft:obsidian",
      "minecraft:red_nether_bricks",
    ),
    zones=(
      BuildZone(
        name="radiant base glow",
        size=(6, 2, 6),
        materials=("orange_stained_glass", "glowstone", "lava"),
        features=("bright orange beacon glow", "radiant lighting foundation"),
        interior=(),
      ),
    ),
    exterior_features=("radiant lighting beacon", "cube orange glow"),
    tips=("Orange glow acts as beacon for mobs",),
  ),
  "epic_bases_cube_overgrown_tower": BookBuild(
    id="epic_bases_cube_overgrown_tower",
    name="Overgrown Ruin Tower",
    theme="sci-fi",
    biome="wasteland",
    caption=(
      "the cube overgrown vegetation tower leafy vines abandoned city "
      "ruin spire crash site exterior module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:mossy_stone_bricks",
      "minecraft:vine",
      "minecraft:oak_leaves",
      "minecraft:cobblestone",
    ),
    zones=(
      BuildZone(
        name="overgrown spire",
        size=(4, 12, 4),
        materials=("stone_bricks", "mossy_stone_bricks", "vine", "oak_leaves"),
        features=("vine covered tower", "abandoned overgrown ruin"),
        interior=(),
      ),
    ),
    exterior_features=("overgrown vegetation tower", "crashed city ruin"),
    tips=("Leaf blocks and vines show abandoned decay",),
  ),
  "epic_bases_cube_crumbled_ruins": BookBuild(
    id="epic_bases_cube_crumbled_ruins",
    name="Crumbled Ruins",
    theme="sci-fi",
    biome="wasteland",
    caption=(
      "the cube crumbled ruins reddish decayed structures damaged before "
      "crash mossy cobble crash site debris module"
    ),
    palette=(
      "minecraft:red_terracotta",
      "minecraft:mossy_cobblestone",
      "minecraft:cobblestone",
      "minecraft:gravel",
      "minecraft:vine",
    ),
    zones=(
      BuildZone(
        name="ruin debris",
        size=(8, 3, 6),
        materials=("red_terracotta", "mossy_cobblestone", "gravel", "vine"),
        features=("crumbled decayed walls", "pre crash damage ruins"),
        interior=(),
      ),
    ),
    exterior_features=("crumbled ruins", "crash site debris"),
    tips=("Ruins damaged before the cube crash landed",),
  ),
  "epic_bases_cube_testing_lab": BookBuild(
    id="epic_bases_cube_testing_lab",
    name="Mob Testing Lab",
    theme="sci-fi",
    biome="wasteland",
    caption=(
      "the cube mob testing lab white diorite room purple iron bar holding "
      "chambers block property examination alien research module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:diorite",
      "minecraft:iron_bars",
      "minecraft:purple_stained_glass",
      "minecraft:polished_diorite",
    ),
    zones=(
      BuildZone(
        name="holding chambers",
        size=(8, 4, 6),
        materials=("white_concrete", "iron_bars", "purple_stained_glass"),
        features=("reinforced holding chambers", "mob block testing cells"),
        interior=("examination chambers",),
      ),
    ),
    exterior_features=("testing lab chambers", "cube mob research"),
    tips=("Test block properties and mob behavior in chambers",),
  ),
  "epic_bases_cube_mob_museum": BookBuild(
    id="epic_bases_cube_mob_museum",
    name="Mob Examination Gallery",
    theme="sci-fi",
    biome="wasteland",
    caption=(
      "the cube mob examination gallery purple caged sections collected "
      "animals museum white walls alien specimen collection module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:iron_bars",
      "minecraft:purple_stained_glass_pane",
      "minecraft:polished_diorite",
      "minecraft:sea_lantern",
    ),
    zones=(
      BuildZone(
        name="specimen gallery",
        size=(10, 4, 8),
        materials=("white_concrete", "iron_bars", "purple_stained_glass_pane"),
        features=("many small purple caged sections", "mob collection museum"),
        interior=("animal specimen cells",),
      ),
    ),
    exterior_features=("mob examination gallery", "cube specimen museum"),
    tips=("Collect all roaming mobs for examination",),
  ),
  "epic_bases_cube_circuit_wall": BookBuild(
    id="epic_bases_cube_circuit_wall",
    name="Circuit Board Wall",
    theme="sci-fi",
    biome="wasteland",
    caption=(
      "the cube circuit board wall grooved red nether brick brown pattern "
      "endless alien technology base exterior texture module"
    ),
    palette=(
      "minecraft:red_nether_bricks",
      "minecraft:nether_bricks",
      "minecraft:black_concrete",
      "minecraft:gray_concrete",
    ),
    zones=(
      BuildZone(
        name="circuit texture",
        size=(8, 4, 1),
        materials=("red_nether_bricks", "nether_bricks", "black_concrete"),
        features=("horizontal grooved circuit pattern", "alien tech wall texture"),
        interior=(),
      ),
    ),
    exterior_features=("circuit board design", "alien grooved walls"),
    tips=("Base looks like endless grooved circuit board",),
  ),
  "epic_bases_cube_core_engine": BookBuild(
    id="epic_bases_cube_core_engine",
    name="Core Cube Engine",
    theme="sci-fi",
    biome="wasteland",
    caption=(
      "the cube core engine tiered obsidian red nether brick tower molten "
      "lava glass core purple panes alien power plant module"
    ),
    palette=(
      "minecraft:obsidian",
      "minecraft:red_nether_bricks",
      "minecraft:purple_stained_glass_pane",
      "minecraft:lava",
      "minecraft:glass",
      "minecraft:glowstone",
    ),
    zones=(
      BuildZone(
        name="engine tower",
        size=(6, 12, 6),
        materials=("obsidian", "red_nether_bricks", "purple_stained_glass_pane"),
        features=("tiered core cube engine", "obsidian encasement", "purple glass contrast"),
        interior=("molten lava core",),
      ),
    ),
    exterior_features=("core cube engine", "alien power tower"),
    tips=("Lava encased in glass for molten core effect",),
  ),
  "epic_bases_cube_lava_curtain": BookBuild(
    id="epic_bases_cube_lava_curtain",
    name="Lava Curtain Force Field",
    theme="sci-fi",
    biome="wasteland",
    caption=(
      "the cube lava curtain force field glass pane walls containing lava "
      "layer defensive barrier alien fortress module"
    ),
    palette=(
      "minecraft:glass_pane",
      "minecraft:glass",
      "minecraft:lava",
      "minecraft:obsidian",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="lava curtain",
        size=(4, 5, 1),
        materials=("glass_pane", "lava", "obsidian"),
        features=("lava layer between glass walls", "force field curtain"),
        interior=(),
      ),
    ),
    exterior_features=("lava curtain force field", "cube defensive barrier"),
    tips=("Contain lava between glass panel walls",),
  ),
  "epic_bases_cube_reinforced_shell": BookBuild(
    id="epic_bases_cube_reinforced_shell",
    name="Reinforced Obsidian Shell",
    theme="sci-fi",
    biome="wasteland",
    caption=(
      "the cube reinforced structure obsidian iron block layered shell "
      "virtually impregnable fortress crash site module"
    ),
    palette=(
      "minecraft:obsidian",
      "minecraft:iron_block",
      "minecraft:crying_obsidian",
      "minecraft:black_concrete",
    ),
    zones=(
      BuildZone(
        name="reinforced cube shell",
        size=(5, 5, 5),
        materials=("obsidian", "iron_block", "crying_obsidian"),
        features=("obsidian iron layered walls", "impregnable fortress shell"),
        interior=(),
      ),
    ),
    exterior_features=("reinforced structure", "cube obsidian shell"),
    tips=("Obsidian and iron make virtually impregnable walls",),
  ),
  "epic_bases_cube_automatic_doorway": BookBuild(
    id="epic_bases_cube_automatic_doorway",
    name="Automatic Doorway",
    theme="sci-fi",
    biome="wasteland",
    caption=(
      "the cube automatic doorway sticky piston quartz redstone repeater "
      "pressure plate futuristic redstone entrance alien base module"
    ),
    palette=(
      "minecraft:quartz_block",
      "minecraft:sticky_piston",
      "minecraft:redstone_repeater",
      "minecraft:redstone_dust",
      "minecraft:redstone_torch",
      "minecraft:stone_pressure_plate",
      "minecraft:quartz_stairs",
    ),
    zones=(
      BuildZone(
        name="piston doorway",
        size=(8, 5, 3),
        materials=("quartz_block", "sticky_piston", "stone_pressure_plate"),
        features=("8 wide automatic door", "sticky piston quartz panels"),
        interior=(),
      ),
      BuildZone(
        name="redstone circuit",
        size=(8, 4, 2),
        materials=("redstone_repeater", "redstone_dust", "redstone_torch"),
        features=("repeater timing circuit", "pressure plate trigger"),
        interior=(),
      ),
    ),
    exterior_features=("automatic doorway", "cube futuristic entrance"),
    tips=("7 step build with sticky pistons and quartz",),
  ),
  "epic_bases_cube_futuristic_streetlight": BookBuild(
    id="epic_bases_cube_futuristic_streetlight",
    name="Futuristic Streetlight",
    theme="sci-fi",
    biome="wasteland",
    caption=(
      "the cube futuristic streetlight tall thin obsidian pole glowstone "
      "warped wood accent alien base path lighting module"
    ),
    palette=(
      "minecraft:obsidian",
      "minecraft:glowstone",
      "minecraft:warped_fence",
      "minecraft:black_concrete",
      "minecraft:sea_lantern",
    ),
    zones=(
      BuildZone(
        name="alien streetlight",
        size=(2, 6, 2),
        materials=("obsidian", "glowstone", "warped_fence", "sea_lantern"),
        features=("tall thin futuristic pole", "elevated detail lighting"),
        interior=(),
      ),
    ),
    exterior_features=("futuristic streetlights", "cube path lighting"),
    tips=("Streetlights elevate build detail and prevent mobs",),
  ),
  "epic_bases_cube_floating_engine": BookBuild(
    id="epic_bases_cube_floating_engine",
    name="Floating Engine Cube",
    theme="sci-fi",
    biome="wasteland",
    caption=(
      "the cube floating engine secondary obsidian purple glass cube glowing "
      "yellow rod antenna alien power component module"
    ),
    palette=(
      "minecraft:obsidian",
      "minecraft:purple_stained_glass",
      "minecraft:glowstone",
      "minecraft:end_rod",
      "minecraft:white_concrete",
    ),
    zones=(
      BuildZone(
        name="engine cube",
        size=(4, 4, 4),
        materials=("obsidian", "purple_stained_glass", "glowstone", "end_rod"),
        features=("floating obsidian cube", "glowing rod antenna", "purple glass panels"),
        interior=("yellow glowing core",),
      ),
    ),
    exterior_features=("floating engine cube", "secondary power component"),
    tips=("Smaller standalone engine cube with glowing rods",),
  ),
  # --- Glistening Ice Palace (Aldur Bluetouch) ---
  "epic_bases_ice_golem_outpost": BookBuild(
    id="epic_bases_ice_golem_outpost",
    name="Snow Golem Outpost",
    theme="fantasy",
    biome="snowy_peaks",
    caption=(
      "glistening ice palace snow golem outpost perimeter tower manned "
      "guard post snowy peaks frost king base defense module"
    ),
    palette=(
      "minecraft:packed_ice",
      "minecraft:blue_ice",
      "minecraft:quartz_block",
      "minecraft:snow_block",
      "minecraft:spruce_planks",
    ),
    zones=(
      BuildZone(
        name="outpost tower",
        size=(4, 8, 4),
        materials=("packed_ice", "quartz_block", "snow_block", "spruce_planks"),
        features=("narrow fortified outpost", "snow golem guard tower"),
        interior=(),
      ),
    ),
    exterior_features=("snow golem outpost", "ice palace perimeter guard"),
    tips=("Outposts manned by snow golems surround the base",),
  ),
  "epic_bases_ice_frozen_forum": BookBuild(
    id="epic_bases_ice_frozen_forum",
    name="Frozen Forum Hall",
    theme="fantasy",
    biome="snowy_peaks",
    caption=(
      "glistening ice palace frozen forum grand hall peaked wooden roof "
      "white quartz pillars elven gathering hall snowy peaks module"
    ),
    palette=(
      "minecraft:quartz_block",
      "minecraft:quartz_pillar",
      "minecraft:packed_ice",
      "minecraft:spruce_planks",
      "minecraft:spruce_stairs",
      "minecraft:blue_ice",
    ),
    zones=(
      BuildZone(
        name="forum hall",
        size=(10, 8, 8),
        materials=("quartz_block", "quartz_pillar", "spruce_planks", "packed_ice"),
        features=("peaked wooden roof", "white stone pillars", "grand forum hall"),
        interior=("gathering hall",),
      ),
    ),
    exterior_features=("frozen forum", "ice palace central hall"),
    tips=("Forum uses quartz pillars and peaked spruce roof",),
  ),
  "epic_bases_ice_amphitheater": BookBuild(
    id="epic_bases_ice_amphitheater",
    name="Ice Amphitheater",
    theme="fantasy",
    biome="snowy_peaks",
    caption=(
      "glistening ice palace amphitheater tiered open air seating hillside "
      "natural light venue no torches ice build snowy peaks module"
    ),
    palette=(
      "minecraft:packed_ice",
      "minecraft:blue_ice",
      "minecraft:quartz_stairs",
      "minecraft:snow_block",
      "minecraft:spruce_slab",
    ),
    zones=(
      BuildZone(
        name="amphitheater tiers",
        size=(10, 5, 8),
        materials=("packed_ice", "quartz_stairs", "snow_block", "spruce_slab"),
        features=("semi circular tiered seating", "open air hillside venue"),
        interior=(),
      ),
    ),
    exterior_features=("ice amphitheater", "open air natural light venue"),
    tips=("Open air venues avoid melting ice with light sources",),
  ),
  "epic_bases_ice_quartz_bridge": BookBuild(
    id="epic_bases_ice_quartz_bridge",
    name="Quartz Arch Bridge",
    theme="fantasy",
    biome="snowy_peaks",
    caption=(
      "glistening ice palace temple run arch white quartz bridge connecting "
      "structures icy chasm span elven walkway snowy peaks module"
    ),
    palette=(
      "minecraft:quartz_block",
      "minecraft:quartz_stairs",
      "minecraft:quartz_slab",
      "minecraft:packed_ice",
      "minecraft:blue_ice",
    ),
    zones=(
      BuildZone(
        name="arch bridge",
        size=(12, 4, 3),
        materials=("quartz_block", "quartz_stairs", "packed_ice"),
        features=("arched white quartz bridge", "connects palace structures"),
        interior=(),
      ),
    ),
    exterior_features=("quartz arch bridge", "temple run walkway"),
    tips=("Arch bridges connect each structure across chasms",),
  ),
  "epic_bases_ice_signaling_beacon": BookBuild(
    id="epic_bases_ice_signaling_beacon",
    name="Signaling Beacon Spire",
    theme="fantasy",
    biome="snowy_peaks",
    caption=(
      "glistening ice palace signaling beacon tall decorative spire bright "
      "light beacon frost king ice palace landmark snowy peaks module"
    ),
    palette=(
      "minecraft:quartz_block",
      "minecraft:quartz_pillar",
      "minecraft:sea_lantern",
      "minecraft:packed_ice",
      "minecraft:blue_ice",
    ),
    zones=(
      BuildZone(
        name="beacon spire",
        size=(3, 12, 3),
        materials=("quartz_pillar", "packed_ice", "sea_lantern"),
        features=("tall decorative spire", "bright signaling beacon light"),
        interior=(),
      ),
    ),
    exterior_features=("signaling beacon", "ice palace landmark spire"),
    tips=("Beacon spire marks the palace from afar",),
  ),
  "epic_bases_ice_mountain_docks": BookBuild(
    id="epic_bases_ice_mountain_docks",
    name="Mountain Docks",
    theme="fantasy",
    biome="snowy_peaks",
    caption=(
      "glistening ice palace mountain docks lowest level frozen water wooden "
      "pier greenery cliff base landing snowy peaks module"
    ),
    palette=(
      "minecraft:spruce_planks",
      "minecraft:oak_fence",
      "minecraft:packed_ice",
      "minecraft:water",
      "minecraft:grass_block",
      "minecraft:spruce_trapdoor",
    ),
    zones=(
      BuildZone(
        name="dock pier",
        size=(8, 3, 6),
        materials=("spruce_planks", "oak_fence", "water", "packed_ice"),
        features=("wooden dock pier", "frozen water landing", "cliff base level"),
        interior=(),
      ),
    ),
    exterior_features=("mountain docks", "ice palace cliff landing"),
    tips=("Docks sit at the lowest palace level near frozen water",),
  ),
  "epic_bases_ice_ragged_spire": BookBuild(
    id="epic_bases_ice_ragged_spire",
    name="Ragged Ice Spire",
    theme="fantasy",
    biome="snowy_peaks",
    caption=(
      "glistening ice palace ragged sculpting spiral ice spire elven tower "
      "hand carved blue ice ribs white quartz core snowy peaks module"
    ),
    palette=(
      "minecraft:quartz_block",
      "minecraft:blue_ice",
      "minecraft:packed_ice",
      "minecraft:quartz_stairs",
      "minecraft:birch_fence",
    ),
    zones=(
      BuildZone(
        name="ragged spire",
        size=(5, 14, 5),
        materials=("quartz_block", "blue_ice", "packed_ice", "birch_fence"),
        features=("spiraling ragged ice ribs", "thin vertical spires", "elven tower"),
        interior=(),
      ),
    ),
    exterior_features=("ragged ice spire", "hand carved spiral ice"),
    tips=("Place ice blocks by hand spiraling around quartz core",),
  ),
  "epic_bases_ice_frozen_tree": BookBuild(
    id="epic_bases_ice_frozen_tree",
    name="Frozen Accent Tree",
    theme="fantasy",
    biome="snowy_peaks",
    caption=(
      "glistening ice palace frozen accent tree splash of green snow covered "
      "oak leaves birch wood elven nature blend snowy peaks module"
    ),
    palette=(
      "minecraft:oak_leaves",
      "minecraft:birch_log",
      "minecraft:snow_block",
      "minecraft:packed_ice",
      "minecraft:grass_block",
    ),
    zones=(
      BuildZone(
        name="accent tree",
        size=(3, 5, 3),
        materials=("oak_leaves", "birch_log", "snow_block", "packed_ice"),
        features=("small snow covered tree", "green accent on ice palette"),
        interior=(),
      ),
    ),
    exterior_features=("frozen accent tree", "elven nature blend"),
    tips=("Trees add splash of green to blue and white palette",),
  ),
  "epic_bases_ice_elven_outpost": BookBuild(
    id="epic_bases_ice_elven_outpost",
    name="Elven Outpost Tower",
    theme="fantasy",
    biome="snowy_peaks",
    caption=(
      "glistening ice palace elven outpost tower narrow birch fence balcony "
      "quartz multi tier perimeter depth snowy peaks frost king module"
    ),
    palette=(
      "minecraft:quartz_block",
      "minecraft:birch_stairs",
      "minecraft:birch_fence",
      "minecraft:birch_trapdoor",
      "minecraft:packed_ice",
      "minecraft:blue_ice",
    ),
    zones=(
      BuildZone(
        name="elven outpost",
        size=(4, 10, 4),
        materials=("quartz_block", "birch_stairs", "birch_fence", "packed_ice"),
        features=("narrow multi tier tower", "birch balcony framing", "perimeter outpost"),
        interior=("small guard room",),
      ),
    ),
    exterior_features=("elven outpost tower", "birch detailed perimeter tower"),
    tips=("Vary tower sizes for bespoke elven architecture",),
  ),
  "epic_bases_ice_alcove_passage": BookBuild(
    id="epic_bases_ice_alcove_passage",
    name="Ice Alcove Passage",
    theme="fantasy",
    biome="snowy_peaks",
    caption=(
      "glistening ice palace alcove passage rounded doorway white quartz "
      "blue ice roof dotted entrances depth elven snowy peaks module"
    ),
    palette=(
      "minecraft:quartz_block",
      "minecraft:quartz_stairs",
      "minecraft:blue_ice",
      "minecraft:packed_ice",
      "minecraft:birch_trapdoor",
    ),
    zones=(
      BuildZone(
        name="alcove entrance",
        size=(4, 4, 3),
        materials=("quartz_block", "blue_ice", "birch_trapdoor"),
        features=("rounded alcove doorway", "blue ice roof cap"),
        interior=(),
      ),
    ),
    exterior_features=("ice alcove passage", "elven rounded doorways"),
    tips=("Dot alcoves around build for depth and detail",),
  ),
  "epic_bases_ice_spike": BookBuild(
    id="epic_bases_ice_spike",
    name="Natural Ice Spike",
    theme="fantasy",
    biome="snowy_peaks",
    caption=(
      "glistening ice palace natural ice spike frozen water bucket high "
      "cold biome spike decoration elven snowy peaks module"
    ),
    palette=(
      "minecraft:packed_ice",
      "minecraft:blue_ice",
      "minecraft:ice",
      "minecraft:snow_block",
      "minecraft:water",
    ),
    zones=(
      BuildZone(
        name="ice spike",
        size=(3, 8, 3),
        materials=("packed_ice", "blue_ice", "ice", "snow_block"),
        features=("tall natural ice spike", "frozen water formation"),
        interior=(),
      ),
    ),
    exterior_features=("natural ice spike", "frozen water decoration"),
    tips=("Place water buckets high in cold biome for natural spikes",),
  ),
  "epic_bases_ice_soul_lantern": BookBuild(
    id="epic_bases_ice_soul_lantern",
    name="Soul Fire Ice Lighting",
    theme="fantasy",
    biome="snowy_peaks",
    caption=(
      "glistening ice palace soul fire lantern low light ice safe lighting "
      "soul torch lamp does not melt ice snowy peaks module"
    ),
    palette=(
      "minecraft:soul_lantern",
      "minecraft:soul_torch",
      "minecraft:packed_ice",
      "minecraft:quartz_block",
      "minecraft:chain",
    ),
    zones=(
      BuildZone(
        name="soul lighting",
        size=(3, 4, 3),
        materials=("soul_lantern", "soul_torch", "packed_ice", "chain"),
        features=("soul fire lantern post", "low light safe for ice"),
        interior=(),
      ),
    ),
    exterior_features=("soul fire ice lighting", "non melting lantern"),
    tips=("Soul fire has lower light and won't melt ice blocks",),
  ),
  "epic_bases_ice_open_gazebo": BookBuild(
    id="epic_bases_ice_open_gazebo",
    name="Open Air Ice Gazebo",
    theme="fantasy",
    biome="snowy_peaks",
    caption=(
      "glistening ice palace open air gazebo conservatory arched wooden "
      "ice structure natural daylight no internal torches snowy peaks module"
    ),
    palette=(
      "minecraft:spruce_planks",
      "minecraft:spruce_stairs",
      "minecraft:packed_ice",
      "minecraft:blue_ice",
      "minecraft:oak_fence",
      "minecraft:spruce_slab",
    ),
    zones=(
      BuildZone(
        name="open gazebo",
        size=(8, 6, 8),
        materials=("spruce_planks", "packed_ice", "spruce_stairs", "oak_fence"),
        features=("open air arched structure", "conservatory gazebo", "no roof lighting needed"),
        interior=(),
      ),
    ),
    exterior_features=("open air ice gazebo", "natural light conservatory"),
    tips=("Open air venues harness daylight without melting ice",),
  ),
  "epic_bases_ice_snowman_farm": BookBuild(
    id="epic_bases_ice_snowman_farm",
    name="Snow Golem Farm",
    theme="fantasy",
    biome="snowy_peaks",
    caption=(
      "glistening ice palace snow golem farm redstone dispenser pumpkin "
      "sticky piston semi automatic snowman soldiers frost king module"
    ),
    palette=(
      "minecraft:snow_block",
      "minecraft:dispenser",
      "minecraft:sticky_piston",
      "minecraft:redstone_repeater",
      "minecraft:redstone_dust",
      "minecraft:glass",
      "minecraft:spruce_planks",
      "minecraft:carved_pumpkin",
    ),
    zones=(
      BuildZone(
        name="golem assembler",
        size=(6, 5, 4),
        materials=("snow_block", "dispenser", "sticky_piston", "glass"),
        features=("9 step redstone farm", "pumpkin dispenser snow block pistons"),
        interior=(),
      ),
      BuildZone(
        name="redstone circuit",
        size=(6, 4, 3),
        materials=("redstone_repeater", "redstone_dust", "sticky_piston"),
        features=("repeater timing chain", "button activated cycle"),
        interior=(),
      ),
    ),
    exterior_features=("snow golem farm", "semi automatic soldier spawner"),
    tips=("Place pumpkin in dispenser and snow under pistons",),
  ),
  # --- The Shimmering Hoard (Flint Scree) ---
  "epic_bases_hoard_treasure_trove": BookBuild(
    id="epic_bases_hoard_treasure_trove",
    name="Treasure Trove",
    theme="dwarven",
    biome="underground",
    caption=(
      "shimmering hoard treasure trove gold block pile bone dragon skeleton "
      "guarded dwarven forge lord underground hoard module"
    ),
    palette=(
      "minecraft:gold_block",
      "minecraft:bone_block",
      "minecraft:deepslate_bricks",
      "minecraft:polished_deepslate",
      "minecraft:chest",
    ),
    zones=(
      BuildZone(
        name="treasure pile",
        size=(8, 4, 6),
        materials=("gold_block", "bone_block", "chest"),
        features=("massive gold pile", "bone dragon skeleton atop treasure"),
        interior=(),
      ),
    ),
    exterior_features=("treasure trove", "dragon guarded gold hoard"),
    tips=("Bone dragon skeleton guards the treasure trove",),
  ),
  "epic_bases_hoard_super_statue": BookBuild(
    id="epic_bases_hoard_super_statue",
    name="Super Statue Beacon",
    theme="dwarven",
    biome="underground",
    caption=(
      "shimmering hoard super statue giant stone figure beacon inside head "
      "speed jump boost status effects dwarven underground module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:chiseled_stone_bricks",
      "minecraft:beacon",
      "minecraft:iron_block",
      "minecraft:gold_block",
    ),
    zones=(
      BuildZone(
        name="giant statue",
        size=(5, 14, 4),
        materials=("stone_bricks", "chiseled_stone_bricks", "gold_block"),
        features=("giant blocky statue", "hammer wielding figure"),
        interior=("beacon in head chamber",),
      ),
    ),
    exterior_features=("super statue beacon", "giant dwarven statue"),
    tips=("Beacons inside statues give visitors status effects",),
  ),
  "epic_bases_hoard_coal_mine_rail": BookBuild(
    id="epic_bases_hoard_coal_mine_rail",
    name="Coal Mine Cart Rail",
    theme="dwarven",
    biome="underground",
    caption=(
      "shimmering hoard coal mine cart rail powered rail supply line "
      "brings coal to forge dwarven underground transport module"
    ),
    palette=(
      "minecraft:rail",
      "minecraft:powered_rail",
      "minecraft:minecart",
      "minecraft:coal_block",
      "minecraft:deepslate_bricks",
      "minecraft:chest",
    ),
    zones=(
      BuildZone(
        name="mine rail line",
        size=(10, 2, 3),
        materials=("rail", "powered_rail", "coal_block", "chest"),
        features=("mine cart coal supply rail", "powered rail transport"),
        interior=(),
      ),
    ),
    exterior_features=("coal mine cart rail", "forge supply line"),
    tips=("Mine carts bring coal supply to the smelting forge",),
  ),
  "epic_bases_hoard_magma_lava_lake": BookBuild(
    id="epic_bases_hoard_magma_lava_lake",
    name="Magma Lava Lake",
    theme="dwarven",
    biome="underground",
    caption=(
      "shimmering hoard magma lava lake orange glow nether magma blocks "
      "enhanced lava pool dwarven underground cavern module"
    ),
    palette=(
      "minecraft:lava",
      "minecraft:magma_block",
      "minecraft:deepslate",
      "minecraft:cobblestone",
      "minecraft:blackstone",
    ),
    zones=(
      BuildZone(
        name="lava lake",
        size=(10, 2, 8),
        materials=("lava", "magma_block", "deepslate", "cobblestone"),
        features=("large lava lake pool", "magma block orange glow"),
        interior=(),
      ),
    ),
    exterior_features=("magma lava lake", "underground lava pool"),
    tips=("Magma blocks from Nether enhance lava glow",),
  ),
  "epic_bases_hoard_lava_pathway": BookBuild(
    id="epic_bases_hoard_lava_pathway",
    name="Lava Lake Pathway",
    theme="dwarven",
    biome="underground",
    caption=(
      "shimmering hoard raised pathway over lava lake no burnt toes safe "
      "walkway cobblestone bridge dwarven underground module"
    ),
    palette=(
      "minecraft:cobblestone",
      "minecraft:stone_brick_slab",
      "minecraft:stone_brick_stairs",
      "minecraft:lava",
      "minecraft:deepslate_bricks",
    ),
    zones=(
      BuildZone(
        name="raised walkway",
        size=(10, 2, 3),
        materials=("cobblestone", "stone_brick_slab", "lava"),
        features=("raised pathway over lava", "safe walkway bridge"),
        interior=(),
      ),
    ),
    exterior_features=("lava lake pathway", "raised safe walkway"),
    tips=("Build raised pathways over lava to save space safely",),
  ),
  "epic_bases_hoard_support_pillar": BookBuild(
    id="epic_bases_hoard_support_pillar",
    name="Ornate Support Pillar",
    theme="dwarven",
    biome="underground",
    caption=(
      "shimmering hoard ornate support pillar stone column arch realistic "
      "columns support tall cavern ceiling dwarven underground module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:chiseled_stone_bricks",
      "minecraft:stone_brick_stairs",
      "minecraft:deepslate_bricks",
      "minecraft:polished_deepslate",
    ),
    zones=(
      BuildZone(
        name="support column",
        size=(3, 10, 3),
        materials=("stone_bricks", "chiseled_stone_bricks", "stone_brick_stairs"),
        features=("heavy ornate pillar", "realistic support column"),
        interior=(),
      ),
    ),
    exterior_features=("ornate support pillar", "cavern ceiling column"),
    tips=("Add columns and arches to support tall underground ceilings",),
  ),
  "epic_bases_hoard_lava_fountain": BookBuild(
    id="epic_bases_hoard_lava_fountain",
    name="Lava Fountain",
    theme="dwarven",
    biome="underground",
    caption=(
      "shimmering hoard lava fountain redirected lava spring stone tower "
      "falling lava pool valve controlled flow dwarven module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:lava",
      "minecraft:glass",
      "minecraft:lever",
      "minecraft:cobblestone",
    ),
    zones=(
      BuildZone(
        name="lava fountain",
        size=(4, 8, 4),
        materials=("stone_bricks", "lava", "glass", "lever"),
        features=("tall lava fall fountain", "redirected lava spring"),
        interior=(),
      ),
    ),
    exterior_features=("lava fountain", "controlled lava flow display"),
    tips=("Use levers as valves to control lava fountain flow",),
  ),
  "epic_bases_hoard_debris_awning": BookBuild(
    id="epic_bases_hoard_debris_awning",
    name="Debris Protection Awning",
    theme="dwarven",
    biome="underground",
    caption=(
      "shimmering hoard debris protection stone awning overhead cave safety "
      "workspace shelter dwarven underground build module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:stone_brick_stairs",
      "minecraft:stone_brick_slab",
      "minecraft:cobblestone",
      "minecraft:oak_planks",
    ),
    zones=(
      BuildZone(
        name="stone awning",
        size=(6, 3, 4),
        materials=("stone_bricks", "stone_brick_stairs", "stone_brick_slab"),
        features=("overhead stone awning", "debris protection shelter"),
        interior=("protected workspace",),
      ),
    ),
    exterior_features=("debris protection awning", "cave safety overhead"),
    tips=("Overhead protection mimics real cave safety",),
  ),
  "epic_bases_hoard_swamp_pool": BookBuild(
    id="epic_bases_hoard_swamp_pool",
    name="Swamp Water Pool",
    theme="dwarven",
    biome="underground",
    caption=(
      "shimmering hoard swamp water pool murky greenish water below swamp "
      "biome sunken pool unique atmosphere dwarven underground module"
    ),
    palette=(
      "minecraft:water",
      "minecraft:mossy_cobblestone",
      "minecraft:vine",
      "minecraft:deepslate",
      "minecraft:lily_pad",
    ),
    zones=(
      BuildZone(
        name="swamp pool",
        size=(6, 2, 6),
        materials=("water", "mossy_cobblestone", "vine", "lily_pad"),
        features=("murky swamp colored water", "sunken pool chamber"),
        interior=(),
      ),
    ),
    exterior_features=("swamp water pool", "murky underground pool"),
    tips=("Building below swamp biome changes water color",),
  ),
  "epic_bases_hoard_cavern_hall": BookBuild(
    id="epic_bases_hoard_cavern_hall",
    name="Natural Cavern Hall",
    theme="dwarven",
    biome="underground",
    caption=(
      "shimmering hoard natural cavern hall expanded circular grand hall "
      "double lip ledge architectural style dwarven underground module"
    ),
    palette=(
      "minecraft:deepslate",
      "minecraft:cobblestone",
      "minecraft:stone_brick_stairs",
      "minecraft:stone_bricks",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="cavern hall",
        size=(12, 8, 10),
        materials=("deepslate", "cobblestone", "stone_bricks", "stone_brick_stairs"),
        features=("expanded natural cavern", "double lip ledge roof", "grand hall"),
        interior=(),
      ),
    ),
    exterior_features=("natural cavern hall", "expanded underground grand hall"),
    tips=("Expand naturally formed caverns into grand halls",),
  ),
  "epic_bases_hoard_mine_shaft": BookBuild(
    id="epic_bases_hoard_mine_shaft",
    name="Mine Shaft Cart System",
    theme="dwarven",
    biome="underground",
    caption=(
      "shimmering hoard mine shaft spiral staircase nine cart powered rail "
      "shaft resource transport dwarven underground module"
    ),
    palette=(
      "minecraft:oak_stairs",
      "minecraft:rail",
      "minecraft:powered_rail",
      "minecraft:chest",
      "minecraft:deepslate_bricks",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="mine shaft",
        size=(4, 10, 4),
        materials=("oak_stairs", "rail", "powered_rail", "chest"),
        features=("spiral staircase shaft", "nine cart powered rail system"),
        interior=(),
      ),
    ),
    exterior_features=("mine shaft cart system", "vertical resource transport"),
    tips=("Nine cart shaft with powered rails transports resources",),
  ),
  "epic_bases_hoard_lava_lighting": BookBuild(
    id="epic_bases_hoard_lava_lighting",
    name="Lava Glass Lighting",
    theme="dwarven",
    biome="underground",
    caption=(
      "shimmering hoard lava lighting flowing lava contained in glass column "
      "underground base illumination dwarven cavern module"
    ),
    palette=(
      "minecraft:glass",
      "minecraft:lava",
      "minecraft:stone_bricks",
      "minecraft:deepslate_bricks",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="lava light column",
        size=(2, 6, 2),
        materials=("glass", "lava", "stone_bricks"),
        features=("lava contained in glass", "flowing lava light column"),
        interior=(),
      ),
    ),
    exterior_features=("lava glass lighting", "underground lava illumination"),
    tips=("Contain flowing lava in glass to light the base",),
  ),
  "epic_bases_hoard_underground_chamber": BookBuild(
    id="epic_bases_hoard_underground_chamber",
    name="Multi-Level Cavern Chamber",
    theme="dwarven",
    biome="underground",
    caption=(
      "shimmering hoard multi level underground chamber circular room "
      "wooden supports staircases torches dwarven cavern module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:oak_planks",
      "minecraft:oak_stairs",
      "minecraft:torch",
      "minecraft:deepslate_bricks",
    ),
    zones=(
      BuildZone(
        name="circular chamber",
        size=(10, 6, 10),
        materials=("stone_bricks", "oak_planks", "oak_stairs", "torch"),
        features=("circular multi level room", "wooden supports", "tiered staircases"),
        interior=(),
      ),
    ),
    exterior_features=("multi level cavern chamber", "circular underground room"),
    tips=("Multi level chambers add depth to underground bases",),
  ),
  "epic_bases_hoard_auto_smelter": BookBuild(
    id="epic_bases_hoard_auto_smelter",
    name="Automatic Smelting Station",
    theme="dwarven",
    biome="underground",
    caption=(
      "shimmering hoard automatic smelting station hopper furnace chest "
      "seven step ore coal processing dwarven forge module"
    ),
    palette=(
      "minecraft:furnace",
      "minecraft:hopper",
      "minecraft:chest",
      "minecraft:stone_bricks",
      "minecraft:deepslate_bricks",
      "minecraft:coal_block",
    ),
    zones=(
      BuildZone(
        name="smelter array",
        size=(12, 4, 4),
        materials=("furnace", "hopper", "chest", "stone_bricks"),
        features=("six furnace smelter line", "hopper fed automatic processing"),
        interior=(),
      ),
      BuildZone(
        name="input chests",
        size=(4, 3, 2),
        materials=("chest", "hopper"),
        features=("coal input chimney", "ore input chimney"),
        interior=(),
      ),
    ),
    exterior_features=("automatic smelting station", "hopper furnace array"),
    tips=("Coal goes in left chimney ores in right chimney",),
  ),
  "epic_bases_hoard_enchant_setup": BookBuild(
    id="epic_bases_hoard_enchant_setup",
    name="Enchantment Forge Setup",
    theme="dwarven",
    biome="underground",
    caption=(
      "shimmering hoard enchantment table setup bookshelves fortune efficiency "
      "lava pools netherite forge dwarven underground module"
    ),
    palette=(
      "minecraft:enchanting_table",
      "minecraft:bookshelf",
      "minecraft:lava",
      "minecraft:stone_bricks",
      "minecraft:anvil",
    ),
    zones=(
      BuildZone(
        name="enchant room",
        size=(5, 3, 5),
        materials=("enchanting_table", "bookshelf", "lava", "anvil"),
        features=("enchantment table surrounded by bookshelves", "lava pool accents"),
        interior=("fortune efficiency enchanting",),
      ),
    ),
    exterior_features=("enchantment forge setup", "bookshelf enchant room"),
    tips=("Fortune and Efficiency enchantments for mining",),
  ),
  # --- Sweet Kingdom (Miss Lolly Delight) ---
  "epic_bases_sweet_flavor_factory": BookBuild(
    id="epic_bases_sweet_flavor_factory",
    name="Flavor Factory",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom flavor factory gingerbread building yellow white striped "
      "walls brown roof confectioners inventing candyland module"
    ),
    palette=(
      "minecraft:yellow_concrete",
      "minecraft:white_concrete",
      "minecraft:spruce_planks",
      "minecraft:oak_planks",
      "minecraft:pink_terracotta",
    ),
    zones=(
      BuildZone(
        name="flavor factory",
        size=(8, 6, 6),
        materials=("yellow_concrete", "white_concrete", "spruce_planks"),
        features=("gingerbread striped walls", "brown candy roof", "confectioner factory"),
        interior=("flavor inventing workshop",),
      ),
    ),
    exterior_features=("flavor factory", "sweet kingdom gingerbread building"),
    tips=("Confectioners always busy inventing new flavors",),
  ),
  "epic_bases_sweet_chocolate_bridge": BookBuild(
    id="epic_bases_sweet_chocolate_bridge",
    name="Chocolate Bridge",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom chocolate bridge arched brown block bridge candyland "
      "river crossing confectioner paradise module"
    ),
    palette=(
      "minecraft:brown_concrete",
      "minecraft:brown_terracotta",
      "minecraft:dark_oak_planks",
      "minecraft:oak_fence",
      "minecraft:white_concrete",
    ),
    zones=(
      BuildZone(
        name="chocolate arch bridge",
        size=(10, 4, 3),
        materials=("brown_concrete", "brown_terracotta", "dark_oak_planks"),
        features=("arched chocolate block bridge", "brown candy crossing"),
        interior=(),
      ),
    ),
    exterior_features=("chocolate bridge", "candyland river crossing"),
    tips=("Latest addition — a bridge made of chocolate",),
  ),
  "epic_bases_sweet_mushroom_meadow": BookBuild(
    id="epic_bases_sweet_mushroom_meadow",
    name="Mushroom Meadows",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom mushroom meadows oversized red pink mushroom structures "
      "candyland forest meadow candy queen module"
    ),
    palette=(
      "minecraft:red_mushroom_block",
      "minecraft:pink_terracotta",
      "minecraft:mycelium",
      "minecraft:grass_block",
      "minecraft:white_concrete",
    ),
    zones=(
      BuildZone(
        name="mushroom field",
        size=(8, 6, 8),
        materials=("red_mushroom_block", "pink_terracotta", "mycelium"),
        features=("oversized red mushrooms", "pink mushroom structures"),
        interior=(),
      ),
    ),
    exterior_features=("mushroom meadows", "giant candy mushrooms"),
    tips=("Mushrooms are vegetables — yuck",),
  ),
  "epic_bases_sweet_jelly_castle": BookBuild(
    id="epic_bases_sweet_jelly_castle",
    name="Bouncy Jelly Castle",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom bouncy jelly castle orange conical roofs gray walls white "
      "frosting extra large doorways slime bouncy candyland module"
    ),
    palette=(
      "minecraft:orange_concrete",
      "minecraft:yellow_concrete",
      "minecraft:light_gray_concrete",
      "minecraft:white_concrete",
      "minecraft:blue_concrete",
      "minecraft:slime_block",
    ),
    zones=(
      BuildZone(
        name="jelly castle",
        size=(10, 10, 8),
        materials=("orange_concrete", "light_gray_concrete", "white_concrete", "slime_block"),
        features=("orange conical roofs", "white frosting trim", "extra large doorways"),
        interior=("bouncy slime floor rooms",),
      ),
    ),
    exterior_features=("bouncy jelly castle", "candyland hilltop castle"),
    tips=("Extra large doorways for bouncing guests",),
  ),
  "epic_bases_sweet_slushie_tap": BookBuild(
    id="epic_bases_sweet_slushie_tap",
    name="Slushie Tap",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom slushie tap blue sugary waterfall decorative opening "
      "thick sugary goodness candyland module"
    ),
    palette=(
      "minecraft:light_blue_stained_glass",
      "minecraft:water",
      "minecraft:gray_concrete",
      "minecraft:white_concrete",
      "minecraft:blue_concrete",
    ),
    zones=(
      BuildZone(
        name="slushie spill",
        size=(4, 6, 3),
        materials=("light_blue_stained_glass", "water", "gray_concrete"),
        features=("blue slushie waterfall", "decorative sugary tap opening"),
        interior=(),
      ),
    ),
    exterior_features=("slushie tap", "sugary blue waterfall"),
    tips=("Thick with sugary goodness",),
  ),
  "epic_bases_sweet_rainbow_road": BookBuild(
    id="epic_bases_sweet_rainbow_road",
    name="Rainbow Road",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom rainbow road multi colored striped path red orange yellow "
      "green blue purple candyland entrance module"
    ),
    palette=(
      "minecraft:red_concrete",
      "minecraft:orange_concrete",
      "minecraft:yellow_concrete",
      "minecraft:lime_concrete",
      "minecraft:light_blue_concrete",
      "minecraft:purple_concrete",
    ),
    zones=(
      BuildZone(
        name="rainbow path",
        size=(12, 1, 3),
        materials=("red_concrete", "orange_concrete", "yellow_concrete", "lime_concrete", "light_blue_concrete", "purple_concrete"),
        features=("vibrant rainbow striped path", "candyland entrance road"),
        interior=(),
      ),
    ),
    exterior_features=("rainbow road", "follow to candyland"),
    tips=("Follow the rainbow road to Candyland",),
  ),
  "epic_bases_sweet_honey_moat": BookBuild(
    id="epic_bases_sweet_honey_moat",
    name="Honey Moat",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom honey moat golden yellow liquid surrounding outer walls "
      "candy kingdom defensive sweet moat module"
    ),
    palette=(
      "minecraft:yellow_concrete",
      "minecraft:orange_concrete",
      "minecraft:honey_block",
      "minecraft:white_concrete",
      "minecraft:pink_terracotta",
    ),
    zones=(
      BuildZone(
        name="honey moat ring",
        size=(10, 2, 10),
        materials=("yellow_concrete", "honey_block", "orange_concrete"),
        features=("golden honey moat", "surrounds kingdom walls"),
        interior=(),
      ),
    ),
    exterior_features=("honey moat", "golden sweet defensive ring"),
    tips=("Golden honey moat surrounds outer walls",),
  ),
  "epic_bases_sweet_candy_cane_light": BookBuild(
    id="epic_bases_sweet_candy_cane_light",
    name="Candy Cane Lamppost",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom candy cane lamppost red white striped pillar lantern "
      "dark oak fence post candyland lighting module"
    ),
    palette=(
      "minecraft:red_concrete",
      "minecraft:white_concrete",
      "minecraft:lantern",
      "minecraft:dark_oak_fence",
      "minecraft:red_terracotta",
    ),
    zones=(
      BuildZone(
        name="candy cane post",
        size=(2, 5, 2),
        materials=("red_concrete", "white_concrete", "lantern", "dark_oak_fence"),
        features=("red white striped candy cane", "lantern lamppost"),
        interior=(),
      ),
    ),
    exterior_features=("candy cane light", "striped candy lamppost"),
    tips=("Candy canes as support pillars and lampposts",),
  ),
  "epic_bases_sweet_doughnut_dorm": BookBuild(
    id="epic_bases_sweet_doughnut_dorm",
    name="Doughnut Dorms",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom doughnut dorms circular chocolate glazed building "
      "sprinkle roof factory worker housing candyland module"
    ),
    palette=(
      "minecraft:brown_concrete",
      "minecraft:white_concrete",
      "minecraft:light_blue_stained_glass",
      "minecraft:red_concrete",
      "minecraft:yellow_concrete",
      "minecraft:lime_concrete",
    ),
    zones=(
      BuildZone(
        name="doughnut building",
        size=(8, 5, 8),
        materials=("brown_concrete", "white_concrete", "light_blue_stained_glass"),
        features=("circular doughnut shape", "chocolate glaze sprinkle roof"),
        interior=("factory worker dorms",),
      ),
    ),
    exterior_features=("doughnut dorms", "on site worker housing"),
    tips=("On site dorms for flavor factory workers",),
  ),
  "epic_bases_sweet_alpine_chalet": BookBuild(
    id="epic_bases_sweet_alpine_chalet",
    name="Alpine Candy Chalet",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom alpine chalet steep brown roof blue walls candy cane "
      "corner pillars mountain hut candyland module"
    ),
    palette=(
      "minecraft:spruce_planks",
      "minecraft:blue_concrete",
      "minecraft:white_concrete",
      "minecraft:red_concrete",
      "minecraft:dark_oak_stairs",
    ),
    zones=(
      BuildZone(
        name="candy chalet",
        size=(6, 6, 5),
        materials=("spruce_planks", "blue_concrete", "white_concrete", "red_concrete"),
        features=("steep sloped roof", "candy cane corner pillars"),
        interior=("cozy mountain hut",),
      ),
    ),
    exterior_features=("alpine candy chalet", "remote mountain hut"),
    tips=("Thick walls and sloped roofs for mountain snow",),
  ),
  "epic_bases_sweet_mushroom_tap": BookBuild(
    id="epic_bases_sweet_mushroom_tap",
    name="Yucky Mushroom Tap",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom yucky mushroom tap secret red mushroom island blue pool "
      "persistent fungi flushed candyland module"
    ),
    palette=(
      "minecraft:red_mushroom_block",
      "minecraft:mycelium",
      "minecraft:water",
      "minecraft:light_blue_concrete",
      "minecraft:stone_bricks",
    ),
    zones=(
      BuildZone(
        name="mushroom island",
        size=(6, 4, 6),
        materials=("red_mushroom_block", "mycelium", "water"),
        features=("red spotted mushrooms", "central blue pool tap"),
        interior=(),
      ),
    ),
    exterior_features=("yucky mushroom tap", "secret fungi island"),
    tips=("Persistent fungi occasionally flushed away",),
  ),
  "epic_bases_sweet_lollipop_tower": BookBuild(
    id="epic_bases_sweet_lollipop_tower",
    name="Lollipop Tower",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom lollipop tower candy cane striped stem purple pink round "
      "top tall candy decoration candyland module"
    ),
    palette=(
      "minecraft:red_concrete",
      "minecraft:white_concrete",
      "minecraft:purple_concrete",
      "minecraft:pink_concrete",
      "minecraft:orange_concrete",
    ),
    zones=(
      BuildZone(
        name="lollipop spire",
        size=(3, 12, 3),
        materials=("red_concrete", "white_concrete", "purple_concrete", "pink_concrete"),
        features=("candy cane striped stem", "round lollipop top"),
        interior=(),
      ),
    ),
    exterior_features=("lollipop tower", "tall candy decoration"),
    tips=("Striped stem with rounded lollipop crown",),
  ),
  "epic_bases_sweet_slime_carpet": BookBuild(
    id="epic_bases_sweet_slime_carpet",
    name="Slime Bouncy Floor",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom slime carpet bouncy floor slime blocks carpet jelly castle "
      "room bounce candyland module"
    ),
    palette=(
      "minecraft:slime_block",
      "minecraft:pink_carpet",
      "minecraft:light_blue_carpet",
      "minecraft:white_concrete",
      "minecraft:yellow_concrete",
    ),
    zones=(
      BuildZone(
        name="bouncy room",
        size=(6, 4, 6),
        materials=("slime_block", "pink_carpet", "light_blue_carpet", "white_concrete"),
        features=("slime block bouncy floor", "carpet topped bounce room"),
        interior=(),
      ),
    ),
    exterior_features=("slime bouncy floor", "jelly castle bounce room"),
    tips=("Slime blocks and carpet make floors bouncy",),
  ),
  "epic_bases_sweet_candy_factory": BookBuild(
    id="epic_bases_sweet_candy_factory",
    name="Candy Factory Complex",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom candy factory multi story cutaway sugar wheat dairy farms "
      "compact flavor factory industrial candyland module"
    ),
    palette=(
      "minecraft:spruce_planks",
      "minecraft:yellow_concrete",
      "minecraft:cyan_concrete",
      "minecraft:orange_concrete",
      "minecraft:dark_oak_stairs",
      "minecraft:brick",
    ),
    zones=(
      BuildZone(
        name="factory building",
        size=(10, 8, 8),
        materials=("spruce_planks", "yellow_concrete", "cyan_concrete", "brick"),
        features=("multi story factory", "tiered brown roof chimneys"),
        interior=("sugar wheat dairy farms inside",),
      ),
    ),
    exterior_features=("candy factory complex", "industrial flavor factory"),
    tips=("Packs all ingredient farms into one compact building",),
  ),
  "epic_bases_sweet_wheat_farm": BookBuild(
    id="epic_bases_sweet_wheat_farm",
    name="Tiered Wheat Farm",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom tiered wheat farm water dispenser lever three tier "
      "farmland harvest replant candy factory module"
    ),
    palette=(
      "minecraft:oak_planks",
      "minecraft:farmland",
      "minecraft:wheat",
      "minecraft:water",
      "minecraft:dispenser",
      "minecraft:lever",
    ),
    zones=(
      BuildZone(
        name="tiered farm",
        size=(8, 4, 4),
        materials=("oak_planks", "farmland", "wheat", "dispenser", "lever"),
        features=("three tier farmland", "lever activated water dispensers"),
        interior=(),
      ),
    ),
    exterior_features=("tiered wheat farm", "lever harvest farm"),
    tips=("Pull lever to harvest then replant seeds",),
  ),
  "epic_bases_sweet_sugarcane_farm": BookBuild(
    id="epic_bases_sweet_sugarcane_farm",
    name="Auto Sugar Cane Farm",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom auto sugar cane farm observer piston stacked sugar mass "
      "produce candy factory redstone module"
    ),
    palette=(
      "minecraft:sugar_cane",
      "minecraft:water",
      "minecraft:piston",
      "minecraft:observer",
      "minecraft:oak_planks",
      "minecraft:glass",
    ),
    zones=(
      BuildZone(
        name="sugarcane farm",
        size=(8, 4, 3),
        materials=("sugar_cane", "piston", "observer", "water", "glass"),
        features=("observer piston auto harvest", "stacked sugar cane rows"),
        interior=(),
      ),
    ),
    exterior_features=("auto sugar cane farm", "mass produce sugar"),
    tips=("Observer activates piston when cane grows too high",),
  ),
  "epic_bases_sweet_cuckoo_clock": BookBuild(
    id="epic_bases_sweet_cuckoo_clock",
    name="Cuckoo Clock",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom cuckoo clock pink framed clock house wooden bird break "
      "time cookie break factory candyland module"
    ),
    palette=(
      "minecraft:pink_concrete",
      "minecraft:white_concrete",
      "minecraft:oak_planks",
      "minecraft:dark_oak_planks",
      "minecraft:clock",
    ),
    zones=(
      BuildZone(
        name="cuckoo clock",
        size=(3, 5, 2),
        materials=("pink_concrete", "white_concrete", "oak_planks", "clock"),
        features=("pink framed clock house", "cuckoo bird break time"),
        interior=(),
      ),
    ),
    exterior_features=("cuckoo clock", "factory break time bell"),
    tips=("Cuckoo calls workers for cookie break",),
  ),
  "epic_bases_sweet_chicken_coop": BookBuild(
    id="epic_bases_sweet_chicken_coop",
    name="Luxury Chicken Coop",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom luxury chicken coop green carpet nest perches egg "
      "collection baking quality candy factory module"
    ),
    palette=(
      "minecraft:green_carpet",
      "minecraft:oak_planks",
      "minecraft:hay_block",
      "minecraft:oak_fence",
      "minecraft:glass",
      "minecraft:white_concrete",
    ),
    zones=(
      BuildZone(
        name="chicken coop",
        size=(6, 4, 5),
        materials=("green_carpet", "oak_planks", "hay_block", "oak_fence"),
        features=("soft green carpet floor", "wall nest perches"),
        interior=("egg collection room",),
      ),
    ),
    exterior_features=("luxury chicken coop", "quality egg baking supply"),
    tips=("Good quality eggs essential for baking",),
  ),
  "epic_bases_sweet_factory_pipes": BookBuild(
    id="epic_bases_sweet_factory_pipes",
    name="Factory Pipe Network",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom factory pipe network gray concrete L pipes decorative "
      "industrial flavor factory interconnected candyland module"
    ),
    palette=(
      "minecraft:gray_concrete",
      "minecraft:light_gray_concrete",
      "minecraft:iron_block",
      "minecraft:yellow_concrete",
      "minecraft:brick",
    ),
    zones=(
      BuildZone(
        name="pipe network",
        size=(8, 4, 4),
        materials=("gray_concrete", "light_gray_concrete", "iron_block"),
        features=("L shaped gray concrete pipes", "decorative industrial network"),
        interior=(),
      ),
    ),
    exterior_features=("factory pipe network", "industrial candy pipes"),
    tips=("Pipes are decorative not functional but fit factory theme",),
  ),
  "epic_bases_sweet_cotton_candy_tree": BookBuild(
    id="epic_bases_sweet_cotton_candy_tree",
    name="Cotton Candy Tree",
    theme="candy",
    biome="forest",
    caption=(
      "sweet kingdom cotton candy tree bright pink leaf blocks fluffy candy "
      "trees scattered candyland forest decoration module"
    ),
    palette=(
      "minecraft:pink_concrete",
      "minecraft:magenta_concrete",
      "minecraft:birch_log",
      "minecraft:grass_block",
      "minecraft:oak_leaves",
    ),
    zones=(
      BuildZone(
        name="cotton candy tree",
        size=(3, 5, 3),
        materials=("pink_concrete", "magenta_concrete", "birch_log"),
        features=("fluffy pink leaf blocks", "cotton candy tree decoration"),
        interior=(),
      ),
    ),
    exterior_features=("cotton candy trees", "pink fluffy candy trees"),
    tips=("Scatter pink fluffy trees throughout kingdom",),
  ),
  # --- The Macabre Motel (Rita the Reanimator) ---
  "epic_bases_motel_decrepit_wing": BookBuild(
    id="epic_bases_motel_decrepit_wing",
    name="Decrepit Wood Wing",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel decrepit wood wing crimson warped wood scare house "
      "nether wood spooky side structure haunted motel module"
    ),
    palette=(
      "minecraft:crimson_planks",
      "minecraft:warped_planks",
      "minecraft:crimson_stairs",
      "minecraft:stone_bricks",
      "minecraft:mossy_stone_bricks",
    ),
    zones=(
      BuildZone(
        name="decrepit wing",
        size=(6, 6, 5),
        materials=("crimson_planks", "warped_planks", "mossy_stone_bricks"),
        features=("crimson warped wood scare house", "decrepit side structure"),
        interior=(),
      ),
    ),
    exterior_features=("decrepit wood wing", "nether wood scare house"),
    tips=("Crimson and warped wood perfect for scare houses",),
  ),
  "epic_bases_motel_soul_lighting": BookBuild(
    id="epic_bases_motel_soul_lighting",
    name="Soul Fire Lighting",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel soul fire lighting blue ominous soul lantern torch "
      "nether soul powered haunted motel window module"
    ),
    palette=(
      "minecraft:soul_lantern",
      "minecraft:soul_torch",
      "minecraft:soul_sand",
      "minecraft:stone_bricks",
      "minecraft:chain",
    ),
    zones=(
      BuildZone(
        name="soul light post",
        size=(2, 4, 2),
        materials=("soul_lantern", "soul_torch", "stone_bricks", "chain"),
        features=("blue soul fire lighting", "ominous nether powered glow"),
        interior=(),
      ),
    ),
    exterior_features=("soul fire lighting", "haunted blue motel lights"),
    tips=("Blue lighting powered by souls from the Nether",),
  ),
  "epic_bases_motel_bone_tree": BookBuild(
    id="epic_bases_motel_bone_tree",
    name="Bone Tree",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel bone tree white skeletal tree red weeping vines "
      "courtyard spook haunted motel decoration module"
    ),
    palette=(
      "minecraft:bone_block",
      "minecraft:weeping_vines",
      "minecraft:weeping_vines_plant",
      "minecraft:grass_block",
      "minecraft:mossy_cobblestone",
    ),
    zones=(
      BuildZone(
        name="bone tree",
        size=(4, 7, 4),
        materials=("bone_block", "weeping_vines", "mossy_cobblestone"),
        features=("white skeletal bone tree", "red weeping vines branches"),
        interior=(),
      ),
    ),
    exterior_features=("bone tree", "skeletal courtyard tree"),
    tips=("Red weeping vines hang from bone branches",),
  ),
  "epic_bases_motel_hedge_maze": BookBuild(
    id="epic_bases_motel_hedge_maze",
    name="Hedge Maze",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel hedge maze green leaf block labyrinth front courtyard "
      "navigate at own risk haunted motel entrance module"
    ),
    palette=(
      "minecraft:oak_leaves",
      "minecraft:spruce_leaves",
      "minecraft:dark_oak_leaves",
      "minecraft:grass_block",
      "minecraft:coarse_dirt",
    ),
    zones=(
      BuildZone(
        name="leaf maze",
        size=(10, 3, 10),
        materials=("oak_leaves", "spruce_leaves", "grass_block"),
        features=("complex hedge leaf maze", "courtyard labyrinth entrance"),
        interior=(),
      ),
    ),
    exterior_features=("hedge maze", "macabre motel labyrinth"),
    tips=("Enter the maze at your own risk",),
  ),
  "epic_bases_motel_mortuary": BookBuild(
    id="epic_bases_motel_mortuary",
    name="Moonlit Mortuary",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel moonlit mortuary low stone building front base "
      "house of the dead haunted motel mortuary module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:mossy_stone_bricks",
      "minecraft:cracked_stone_bricks",
      "minecraft:iron_bars",
      "minecraft:soul_lantern",
    ),
    zones=(
      BuildZone(
        name="mortuary",
        size=(6, 3, 5),
        materials=("stone_bricks", "mossy_stone_bricks", "iron_bars", "soul_lantern"),
        features=("low stone mortuary building", "moonlit front structure"),
        interior=("undead remains chamber",),
      ),
    ),
    exterior_features=("moonlit mortuary", "house of the dead entrance"),
    tips=("Mortuary at the front base of the haunted motel",),
  ),
  "epic_bases_motel_gothic_spire": BookBuild(
    id="epic_bases_motel_gothic_spire",
    name="Gothic Motel Spire",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel gothic spire tall narrow tower cyan magenta roof "
      "phantoms circling overhead haunted mansion module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:deepslate_bricks",
      "minecraft:cyan_terracotta",
      "minecraft:magenta_terracotta",
      "minecraft:orange_stained_glass",
    ),
    zones=(
      BuildZone(
        name="gothic spire",
        size=(4, 14, 4),
        materials=("stone_bricks", "cyan_terracotta", "magenta_terracotta", "orange_stained_glass"),
        features=("tall narrow gothic spire", "glowing orange windows"),
        interior=(),
      ),
    ),
    exterior_features=("gothic motel spire", "phantom circling tower"),
    tips=("Tall spires where phantoms circle overhead",),
  ),
  "epic_bases_motel_cobweb_hall": BookBuild(
    id="epic_bases_motel_cobweb_hall",
    name="Cobweb Corridor",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel cobweb corridor sticky situation iron bars uneven "
      "web patterns slow intruders haunted motel trap module"
    ),
    palette=(
      "minecraft:cobweb",
      "minecraft:iron_bars",
      "minecraft:stone_bricks",
      "minecraft:mossy_stone_bricks",
      "minecraft:vine",
    ),
    zones=(
      BuildZone(
        name="web corridor",
        size=(8, 3, 3),
        materials=("cobweb", "iron_bars", "stone_bricks", "vine"),
        features=("uneven cobweb patterns", "slows movement to fifteen percent"),
        interior=(),
      ),
    ),
    exterior_features=("cobweb corridor", "sticky tricky motel paths"),
    tips=("Scatter cobwebs in uneven patterns to confuse intruders",),
  ),
  "epic_bases_motel_graveyard_crypt": BookBuild(
    id="epic_bases_motel_graveyard_crypt",
    name="Graveyard Crypt",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel graveyard crypt stone tomb dark oak door decrepit "
      "gravestones extravagant crypt haunted motel module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:mossy_stone_bricks",
      "minecraft:dark_oak_door",
      "minecraft:chiseled_stone_bricks",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="stone crypt",
        size=(4, 4, 4),
        materials=("stone_bricks", "mossy_stone_bricks", "dark_oak_door", "chiseled_stone_bricks"),
        features=("small stone crypt tomb", "decrepit graveyard structure"),
        interior=("crypt chamber",),
      ),
    ),
    exterior_features=("graveyard crypt", "haunted stone tomb"),
    tips=("Mix decrepit gravestones and extravagant crypts",),
  ),
  "epic_bases_motel_skeletal_stables": BookBuild(
    id="epic_bases_motel_skeletal_stables",
    name="Skeletal Horse Stables",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel skeletal horse stables magenta awnings iron bar gates "
      "custom skeleton horse barn thunder lightning module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:purple_carpet",
      "minecraft:iron_bars",
      "minecraft:dark_oak_fence",
      "minecraft:soul_lantern",
    ),
    zones=(
      BuildZone(
        name="skeleton stables",
        size=(8, 4, 4),
        materials=("stone_bricks", "purple_carpet", "iron_bars", "dark_oak_fence"),
        features=("open bay skeleton horse stables", "magenta awnings iron gates"),
        interior=("skeleton horse bays",),
      ),
    ),
    exterior_features=("skeletal stables", "skeleton horse barn"),
    tips=("Thunderstorms generate skeleton horsemen for stables",),
  ),
  "epic_bases_motel_wicked_tree": BookBuild(
    id="epic_bases_motel_wicked_tree",
    name="Wicked Gnarled Tree",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel wicked gnarled tree dark oak twisted branches spooky "
      "forest decoration haunted motel module"
    ),
    palette=(
      "minecraft:dark_oak_log",
      "minecraft:dark_oak_wood",
      "minecraft:vine",
      "minecraft:oak_leaves",
      "minecraft:mossy_cobblestone",
    ),
    zones=(
      BuildZone(
        name="gnarled tree",
        size=(4, 6, 4),
        materials=("dark_oak_log", "dark_oak_wood", "vine", "oak_leaves"),
        features=("twisted gnarled brown tree", "wicked forest decoration"),
        interior=(),
      ),
    ),
    exterior_features=("wicked gnarled tree", "spooky forest tree"),
    tips=("Custom gnarled trees add foreboding atmosphere",),
  ),
  "epic_bases_motel_prison_room": BookBuild(
    id="epic_bases_motel_prison_room",
    name="Princess Prison Room",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel princess prison room iron bars zombie locked apartment "
      "purple carpet dining trapped staff haunted motel module"
    ),
    palette=(
      "minecraft:iron_bars",
      "minecraft:purple_carpet",
      "minecraft:stone_bricks",
      "minecraft:dark_oak_planks",
      "minecraft:chain",
    ),
    zones=(
      BuildZone(
        name="prison apartment",
        size=(6, 4, 5),
        materials=("iron_bars", "purple_carpet", "stone_bricks", "chain"),
        features=("iron bar locked room", "zombie princess prison"),
        interior=("trapped staff chamber",),
      ),
    ),
    exterior_features=("princess prison room", "locked zombie apartment"),
    tips=("Princess and staff turned zombie locked away",),
  ),
  "epic_bases_motel_swamp_foundation": BookBuild(
    id="epic_bases_motel_swamp_foundation",
    name="Swamp Foundation",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel swamp foundation mossy cobblestone vines blend building "
      "into swampland haunted motel base module"
    ),
    palette=(
      "minecraft:mossy_cobblestone",
      "minecraft:mossy_stone_bricks",
      "minecraft:vine",
      "minecraft:water",
      "minecraft:stone_bricks",
    ),
    zones=(
      BuildZone(
        name="swamp base",
        size=(8, 2, 8),
        materials=("mossy_cobblestone", "mossy_stone_bricks", "vine", "water"),
        features=("mossy cobblestone swamp blend", "vine covered foundation"),
        interior=(),
      ),
    ),
    exterior_features=("swamp foundation", "mossy motel base blend"),
    tips=("Mossy cobblestone and vines blend into swampland",),
  ),
  "epic_bases_motel_potions_lab": BookBuild(
    id="epic_bases_motel_potions_lab",
    name="Potions Laboratory",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel potions laboratory brewing stands chest trough endless "
      "water splash potions bad luck weakness haunted motel module"
    ),
    palette=(
      "minecraft:brewing_stand",
      "minecraft:chest",
      "minecraft:water",
      "minecraft:stone_bricks",
      "minecraft:cauldron",
      "minecraft:soul_lantern",
    ),
    zones=(
      BuildZone(
        name="potions room",
        size=(8, 3, 4),
        materials=("brewing_stand", "chest", "water", "cauldron"),
        features=("long potions laboratory", "three wide water trough source"),
        interior=("splash potion brewing",),
      ),
    ),
    exterior_features=("potions laboratory", "witch concoction room"),
    tips=("Add gunpowder for splash potions of bad luck",),
  ),
  "epic_bases_motel_elytra_launch": BookBuild(
    id="epic_bases_motel_elytra_launch",
    name="Elytra Launch Patio",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel elytra launch patio candle poles outdoor flight start "
      "fireworks travel instead broomstick haunted motel module"
    ),
    palette=(
      "minecraft:candle",
      "minecraft:dark_oak_fence",
      "minecraft:stone_brick_slab",
      "minecraft:stone_bricks",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="launch patio",
        size=(6, 3, 4),
        materials=("candle", "dark_oak_fence", "stone_brick_slab", "stone_bricks"),
        features=("candle lit outdoor patio", "elytra flight launch point"),
        interior=(),
      ),
    ),
    exterior_features=("elytra launch patio", "flight starting balcony"),
    tips=("Use fireworks and elytra instead of broomstick",),
  ),
  "epic_bases_motel_maze_trap": BookBuild(
    id="epic_bases_motel_maze_trap",
    name="Macabre Maze Traps",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel maze traps leaf maze tripwire dispenser lava iron door "
      "sweet berries hidden rooms haunted motel module"
    ),
    palette=(
      "minecraft:oak_leaves",
      "minecraft:dispenser",
      "minecraft:tripwire_hook",
      "minecraft:iron_door",
      "minecraft:lava",
      "minecraft:sweet_berry_bush",
    ),
    zones=(
      BuildZone(
        name="trapped maze",
        size=(10, 3, 10),
        materials=("oak_leaves", "dispenser", "tripwire_hook", "iron_door", "lava"),
        features=("leaf maze with traps", "tripwire arrows lava dispensers"),
        interior=("hidden maze rooms",),
      ),
    ),
    exterior_features=("macabre maze traps", "hazardous leaf labyrinth"),
    tips=("Trip wires arrows lava dispensers and berry bushes",),
  ),
  "epic_bases_motel_secret_door": BookBuild(
    id="epic_bases_motel_secret_door",
    name="Bookshelf Secret Door",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel bookshelf secret door sticky piston redstone hidden "
      "passage safe route haunted motel redstone module"
    ),
    palette=(
      "minecraft:bookshelf",
      "minecraft:sticky_piston",
      "minecraft:redstone_dust",
      "minecraft:redstone_torch",
      "minecraft:stone_bricks",
    ),
    zones=(
      BuildZone(
        name="hidden door",
        size=(4, 3, 2),
        materials=("bookshelf", "sticky_piston", "redstone_dust", "redstone_torch"),
        features=("two by two bookshelf secret door", "sticky piston redstone"),
        interior=("hidden safe passage",),
      ),
    ),
    exterior_features=("bookshelf secret door", "hidden redstone passage"),
    tips=("Safe route known only to the builder",),
  ),
  "epic_bases_motel_crypt_release": BookBuild(
    id="epic_bases_motel_crypt_release",
    name="Daylight Crypt Release",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel daylight crypt release sensor stone doors time locked "
      "opens at night releases inhabitants haunted motel module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:iron_door",
      "minecraft:daylight_detector",
      "minecraft:redstone_dust",
      "minecraft:green_terracotta",
      "minecraft:mossy_stone_bricks",
    ),
    zones=(
      BuildZone(
        name="time locked crypt",
        size=(5, 4, 5),
        materials=("stone_bricks", "iron_door", "daylight_detector", "green_terracotta"),
        features=("ornate stone crypt building", "daylight sensor locked doors"),
        interior=("mob release chamber",),
      ),
    ),
    exterior_features=("daylight crypt release", "night opening stone crypt"),
    tips=("Doors time locked with daylight sensor open at sunset",),
  ),
  "epic_bases_motel_secret_passage": BookBuild(
    id="epic_bases_motel_secret_passage",
    name="Hidden Wall Passage",
    theme="horror",
    biome="dark_forest",
    caption=(
      "macabre motel hidden wall passage secret path built into wall safe "
      "route navigate maze haunted motel module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:mossy_stone_bricks",
      "minecraft:bookshelf",
      "minecraft:torch",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="wall passage",
        size=(6, 3, 2),
        materials=("stone_bricks", "bookshelf", "torch", "mossy_stone_bricks"),
        features=("hidden passageway in wall", "builder only safe route"),
        interior=(),
      ),
    ),
    exterior_features=("hidden wall passage", "secret maze navigation route"),
    tips=("Secret path built into wall avoids maze hazards",),
  ),
  # --- Phoenix Castle (Sir Cornelius Luckless) ---
  "epic_bases_phoenix_curtain_wall": BookBuild(
    id="epic_bases_phoenix_curtain_wall",
    name="Curtain Wall",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle curtain wall steep unscalable stone fortification outer "
      "defense repel invaders paranoid knight module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:mossy_stone_bricks",
      "minecraft:cobblestone",
      "minecraft:stone_brick_stairs",
      "minecraft:blue_banner",
    ),
    zones=(
      BuildZone(
        name="curtain wall",
        size=(12, 6, 2),
        materials=("stone_bricks", "mossy_stone_bricks", "stone_brick_stairs"),
        features=("steep unscalable outer wall", "thick stone fortification"),
        interior=(),
      ),
    ),
    exterior_features=("curtain wall", "phoenix castle outer defense"),
    tips=("Steep walls stop the most arduous invaders",),
  ),
  "epic_bases_phoenix_inner_village": BookBuild(
    id="epic_bases_phoenix_inner_village",
    name="Inner Castle Village",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle inner village golden roof houses cluster inside walls "
      "maze like planning dead ends castle grounds module"
    ),
    palette=(
      "minecraft:oak_planks",
      "minecraft:spruce_planks",
      "minecraft:yellow_terracotta",
      "minecraft:dark_oak_planks",
      "minecraft:cobblestone",
    ),
    zones=(
      BuildZone(
        name="village houses",
        size=(8, 5, 8),
        materials=("oak_planks", "spruce_planks", "yellow_terracotta", "dark_oak_planks"),
        features=("golden roof village houses", "maze like castle grounds layout"),
        interior=(),
      ),
    ),
    exterior_features=("inner castle village", "golden roof dwellings"),
    tips=("Lay out grounds with dead ends to confuse invaders",),
  ),
  "epic_bases_phoenix_guardian_moat": BookBuild(
    id="epic_bases_phoenix_guardian_moat",
    name="Guardian Moat",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle guardian moat water filled vicious guardians gate "
      "guardians first line defense paranoid knight module"
    ),
    palette=(
      "minecraft:water",
      "minecraft:prismarine",
      "minecraft:dark_prismarine",
      "minecraft:stone_bricks",
      "minecraft:sea_lantern",
    ),
    zones=(
      BuildZone(
        name="guardian moat",
        size=(10, 3, 6),
        materials=("water", "prismarine", "stone_bricks", "sea_lantern"),
        features=("deep water moat ring", "guardian inhabited defense"),
        interior=(),
      ),
    ),
    exterior_features=("guardian moat", "water moat gate defense"),
    tips=("Vicious guardians live in the moat",),
  ),
  "epic_bases_phoenix_parapet": BookBuild(
    id="epic_bases_phoenix_parapet",
    name="Manned Parapet",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle manned parapet crenelations blue orange banners day "
      "night watch archer positions paranoid knight module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:stone_brick_slab",
      "minecraft:blue_banner",
      "minecraft:orange_banner",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="parapet walk",
        size=(10, 3, 2),
        materials=("stone_bricks", "stone_brick_slab", "blue_banner", "torch"),
        features=("crenelated parapet walkway", "manned day and night"),
        interior=(),
      ),
    ),
    exterior_features=("manned parapet", "banner lined battlements"),
    tips=("Parapet manned lest we get caught unaware",),
  ),
  "epic_bases_phoenix_siege_farm": BookBuild(
    id="epic_bases_phoenix_siege_farm",
    name="Siege Supply Farm",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle siege supply farm crops within castle walls never "
      "succumb to siege wheat carrots paranoid knight module"
    ),
    palette=(
      "minecraft:farmland",
      "minecraft:wheat",
      "minecraft:carrots",
      "minecraft:water",
      "minecraft:oak_fence",
    ),
    zones=(
      BuildZone(
        name="siege crops",
        size=(8, 2, 6),
        materials=("farmland", "wheat", "carrots", "water", "oak_fence"),
        features=("walled crop fields", "siege supply farming"),
        interior=(),
      ),
    ),
    exterior_features=("siege supply farm", "castle interior crops"),
    tips=("Many crops grow within walls for siege survival",),
  ),
  "epic_bases_phoenix_royal_chamber": BookBuild(
    id="epic_bases_phoenix_royal_chamber",
    name="Royal Chamber",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle royal chamber safest high room balcony archers "
      "paranoid knight defensive bedroom module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:blue_carpet",
      "minecraft:oak_planks",
      "minecraft:iron_bars",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="royal room",
        size=(6, 5, 5),
        materials=("stone_bricks", "blue_carpet", "oak_planks", "iron_bars"),
        features=("high safest royal chamber", "archer balcony overlook"),
        interior=("royal bedchamber",),
      ),
    ),
    exterior_features=("royal chamber", "safest castle room"),
    tips=("Safest room with balcony for archers",),
  ),
  "epic_bases_phoenix_control_room": BookBuild(
    id="epic_bases_phoenix_control_room",
    name="Trap Control Room",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle trap control room redstone mechanisms central panel "
      "activate castle traps paranoid knight module"
    ),
    palette=(
      "minecraft:redstone_block",
      "minecraft:redstone_torch",
      "minecraft:lever",
      "minecraft:stone_bricks",
      "minecraft:lava_bucket",
    ),
    zones=(
      BuildZone(
        name="control room",
        size=(5, 3, 4),
        materials=("redstone_block", "lever", "lava_bucket", "stone_bricks"),
        features=("central trap control panel", "redstone mechanism hub"),
        interior=(),
      ),
    ),
    exterior_features=("trap control room", "castle redstone hub"),
    tips=("Control room activates traps around the base",),
  ),
  "epic_bases_phoenix_stables": BookBuild(
    id="epic_bases_phoenix_stables",
    name="Castle Stables",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle stables hay horse bays riders bring horses "
      "paranoid knight castle interior module"
    ),
    palette=(
      "minecraft:hay_block",
      "minecraft:oak_planks",
      "minecraft:oak_fence",
      "minecraft:lantern",
      "minecraft:cobblestone",
    ),
    zones=(
      BuildZone(
        name="horse stables",
        size=(8, 4, 4),
        materials=("hay_block", "oak_planks", "oak_fence", "cobblestone"),
        features=("hay filled horse bays", "rider stable area"),
        interior=("horse stalls",),
      ),
    ),
    exterior_features=("castle stables", "hay horse bays"),
    tips=("Riders bring horses to the castle stables",),
  ),
  "epic_bases_phoenix_stockroom": BookBuild(
    id="epic_bases_phoenix_stockroom",
    name="Supply Stockroom",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle supply stockroom rows of chests stockpile siege "
      "supplies lower level storage paranoid knight module"
    ),
    palette=(
      "minecraft:chest",
      "minecraft:barrel",
      "minecraft:oak_planks",
      "minecraft:stone_bricks",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="stockroom",
        size=(8, 3, 6),
        materials=("chest", "barrel", "oak_planks", "stone_bricks"),
        features=("rows of storage chests", "siege supply stockpile"),
        interior=(),
      ),
    ),
    exterior_features=("supply stockroom", "castle chest storage"),
    tips=("Stockpile supplies in lower level stockroom",),
  ),
  "epic_bases_phoenix_escape_tunnel": BookBuild(
    id="epic_bases_phoenix_escape_tunnel",
    name="Escape Tunnel",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle escape tunnel last resort tnt gravel arched exit "
      "foundation secret retreat paranoid knight module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:tnt",
      "minecraft:gravel",
      "minecraft:torch",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="escape tunnel",
        size=(8, 2, 2),
        materials=("stone_bricks", "tnt", "gravel", "torch"),
        features=("arched foundation escape tunnel", "tnt gravel last resort"),
        interior=(),
      ),
    ),
    exterior_features=("escape tunnel", "last resort retreat passage"),
    tips=("Blow TNT and gravel to block passage behind retreat",),
  ),
  "epic_bases_phoenix_defense_turret": BookBuild(
    id="epic_bases_phoenix_defense_turret",
    name="Defense Turret",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle defense turret arrow slit windows trapdoor mechanisms "
      "slender stone tower blue banners module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:mossy_stone_bricks",
      "minecraft:iron_trapdoor",
      "minecraft:blue_banner",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="defense turret",
        size=(3, 10, 3),
        materials=("stone_bricks", "mossy_stone_bricks", "iron_trapdoor", "iron_bars"),
        features=("arrow slit windows", "trapdoor defense mechanisms"),
        interior=(),
      ),
    ),
    exterior_features=("defense turret", "slender castle tower"),
    tips=("Arrow slits and trapdoors for tower defense",),
  ),
  "epic_bases_phoenix_flying_buttress": BookBuild(
    id="epic_bases_phoenix_flying_buttress",
    name="Flying Buttress",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle flying buttress buttress bastion fortification visual "
      "warning stone support paranoid knight module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:stone_brick_stairs",
      "minecraft:cobblestone",
      "minecraft:andesite",
      "minecraft:mossy_stone_bricks",
    ),
    zones=(
      BuildZone(
        name="flying buttress",
        size=(4, 8, 2),
        materials=("stone_bricks", "stone_brick_stairs", "cobblestone"),
        features=("tall narrow buttress bastion", "fortification support arch"),
        interior=(),
      ),
    ),
    exterior_features=("flying buttress", "castle fortification support"),
    tips=("Buttress bastions warn enemies visually",),
  ),
  "epic_bases_phoenix_battered_wall": BookBuild(
    id="epic_bases_phoenix_battered_wall",
    name="Battered Fortification Wall",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle battered fortification weathered stone mossy cobble "
      "andesite mixed blocks worn wall paranoid knight module"
    ),
    palette=(
      "minecraft:stone",
      "minecraft:mossy_cobblestone",
      "minecraft:andesite",
      "minecraft:stone_bricks",
      "minecraft:cobblestone",
    ),
    zones=(
      BuildZone(
        name="battered wall",
        size=(8, 5, 1),
        materials=("stone", "mossy_cobblestone", "andesite", "stone_bricks"),
        features=("weathered mixed stone wall", "battered fortification texture"),
        interior=(),
      ),
    ),
    exterior_features=("battered fortification", "weathered castle wall"),
    tips=("Alternate stone types for weathered look avoid parkour gaps",),
  ),
  "epic_bases_phoenix_phoenix_banner": BookBuild(
    id="epic_bases_phoenix_phoenix_banner",
    name="Phoenix Banner",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle phoenix banner blue white yellow checkered flag "
      "run away to live another day motto paranoid knight module"
    ),
    palette=(
      "minecraft:blue_banner",
      "minecraft:white_banner",
      "minecraft:yellow_banner",
      "minecraft:oak_fence",
      "minecraft:stone_bricks",
    ),
    zones=(
      BuildZone(
        name="banner post",
        size=(2, 4, 2),
        materials=("blue_banner", "white_banner", "yellow_banner", "oak_fence"),
        features=("phoenix checkered banner", "castle emblem flag post"),
        interior=(),
      ),
    ),
    exterior_features=("phoenix banner", "castle emblem flag"),
    tips=("Motto run away to live another day",),
  ),
  "epic_bases_phoenix_roof_slating": BookBuild(
    id="epic_bases_phoenix_roof_slating",
    name="Roof Slating",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle roof slating wooden stair slopes stone gable ends "
      "traditional peaked roof paranoid knight module"
    ),
    palette=(
      "minecraft:dark_oak_stairs",
      "minecraft:spruce_stairs",
      "minecraft:stone_bricks",
      "minecraft:cobblestone",
      "minecraft:oak_planks",
    ),
    zones=(
      BuildZone(
        name="peaked roof",
        size=(6, 4, 4),
        materials=("dark_oak_stairs", "spruce_stairs", "stone_bricks"),
        features=("wooden stair roof slopes", "stone gable end faces"),
        interior=(),
      ),
    ),
    exterior_features=("roof slating", "traditional castle peaked roof"),
    tips=("Lines of wooden staircases with stone gable faces",),
  ),
  "epic_bases_phoenix_mob_house_trap": BookBuild(
    id="epic_bases_phoenix_mob_house_trap",
    name="Mob House Trap",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle mob house trap innocent villager dwelling tripwire "
      "zombies skeletons creepers ensnare invaders module"
    ),
    palette=(
      "minecraft:oak_planks",
      "minecraft:spruce_planks",
      "minecraft:hay_block",
      "minecraft:tripwire_hook",
      "minecraft:cobblestone",
    ),
    zones=(
      BuildZone(
        name="trap house",
        size=(6, 5, 5),
        materials=("oak_planks", "hay_block", "tripwire_hook", "cobblestone"),
        features=("innocent looking house trap", "tripwire triggered mob house"),
        interior=("zombie skeleton creeper trap",),
      ),
    ),
    exterior_features=("mob house trap", "tripwire villager decoy"),
    tips=("Looks like villager dwelling but full of hostile mobs",),
  ),
  "epic_bases_phoenix_tnt_scatterbomb": BookBuild(
    id="epic_bases_phoenix_tnt_scatterbomb",
    name="TNT Scatterbomb Trap",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle tnt scatterbomb trap obsidian redstone perimeter "
      "out with a bang adversary breach module"
    ),
    palette=(
      "minecraft:obsidian",
      "minecraft:tnt",
      "minecraft:redstone_torch",
      "minecraft:redstone_repeater",
      "minecraft:stone_pressure_plate",
    ),
    zones=(
      BuildZone(
        name="scatterbomb",
        size=(6, 3, 4),
        materials=("obsidian", "tnt", "redstone_torch", "redstone_repeater"),
        features=("tnt scatterbomb redstone trap", "perimeter breach defense"),
        interior=(),
      ),
    ),
    exterior_features=("tnt scatterbomb", "perimeter explosive trap"),
    tips=("Dispatches adversaries who breach the perimeter",),
  ),
  "epic_bases_phoenix_lava_battlement": BookBuild(
    id="epic_bases_phoenix_lava_battlement",
    name="Lava Battlement Dispenser",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle lava battlement dispenser wall scaling defense "
      "lava filled dispensers paranoid knight module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:dispenser",
      "minecraft:lava_bucket",
      "minecraft:stone_brick_stairs",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="lava battlement",
        size=(8, 3, 2),
        materials=("stone_bricks", "dispenser", "lava_bucket", "stone_brick_stairs"),
        features=("dispenser lined battlements", "lava wall scaling defense"),
        interior=(),
      ),
    ),
    exterior_features=("lava battlement", "dispenser wall defense"),
    tips=("Lava filled dispensers attack wall scalers",),
  ),
  "epic_bases_phoenix_trap_control_panel": BookBuild(
    id="epic_bases_phoenix_trap_control_panel",
    name="Trap Control Panel",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle trap control panel lava buckets lever central "
      "activate base traps stone room paranoid knight module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:lava_bucket",
      "minecraft:lever",
      "minecraft:dispenser",
      "minecraft:redstone_dust",
    ),
    zones=(
      BuildZone(
        name="control panel",
        size=(4, 3, 3),
        materials=("stone_bricks", "lava_bucket", "lever", "dispenser"),
        features=("wall mounted lava bucket panel", "lever trap activation"),
        interior=(),
      ),
    ),
    exterior_features=("trap control panel", "central lever activation"),
    tips=("Central panel activates traps around the castle",),
  ),
  "epic_bases_phoenix_castle_sconce": BookBuild(
    id="epic_bases_phoenix_castle_sconce",
    name="Castle Wall Sconce",
    theme="medieval",
    biome="mountains",
    caption=(
      "phoenix castle wall sconce torch item frame slab decorative "
      "lighting fixture stone block paranoid knight module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:torch",
      "minecraft:item_frame",
      "minecraft:stone_slab",
      "minecraft:wall_torch",
    ),
    zones=(
      BuildZone(
        name="wall sconce",
        size=(2, 2, 1),
        materials=("stone_bricks", "torch", "item_frame", "stone_slab"),
        features=("decorative wall sconce light", "torch frame slab fixture"),
        interior=(),
      ),
    ),
    exterior_features=("castle wall sconce", "decorative torch lighting"),
    tips=("Place torch then frame then slab for sconce",),
  ),
  # --- Craftholme (Escher Wonder) ---
  "epic_bases_holme_outdoor_forum": BookBuild(
    id="epic_bases_holme_outdoor_forum",
    name="Outdoor Forum",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme outdoor forum circular open air platform sandstone pillars "
      "architecture school citadel mountain module"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:smooth_sandstone",
      "minecraft:sandstone_pillar",
      "minecraft:oak_fence",
      "minecraft:cut_sandstone",
    ),
    zones=(
      BuildZone(
        name="forum platform",
        size=(8, 2, 8),
        materials=("sandstone", "sandstone_pillar", "smooth_sandstone", "oak_fence"),
        features=("circular open air forum", "pillar supported platform"),
        interior=(),
      ),
    ),
    exterior_features=("outdoor forum", "craftholme gathering platform"),
    tips=("Circular forum for open air discussions",),
  ),
  "epic_bases_holme_announcement_pulpit": BookBuild(
    id="epic_bases_holme_announcement_pulpit",
    name="Announcement Pulpit",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme announcement pulpit balcony daily news broadcast green white "
      "striped awning lantern sandstone citadel module"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:dark_oak_planks",
      "minecraft:green_bed",
      "minecraft:white_wool",
      "minecraft:lantern",
      "minecraft:yellow_banner",
    ),
    zones=(
      BuildZone(
        name="pulpit balcony",
        size=(4, 4, 3),
        materials=("sandstone", "dark_oak_planks", "green_bed", "lantern", "yellow_banner"),
        features=("protruding announcement pulpit", "striped awning balcony"),
        interior=(),
      ),
    ),
    exterior_features=("announcement pulpit", "daily news broadcast balcony"),
    tips=("Daily announcements broadcast from the pulpit",),
  ),
  "epic_bases_holme_crane_tether": BookBuild(
    id="epic_bases_holme_crane_tether",
    name="Crane and Tether",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme crane tether grindstone chain dangling construction arm "
      "sandstone tower building equipment citadel module"
    ),
    palette=(
      "minecraft:grindstone",
      "minecraft:dark_oak_fence",
      "minecraft:chain",
      "minecraft:sandstone",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="construction crane",
        size=(4, 6, 2),
        materials=("grindstone", "dark_oak_fence", "chain", "sandstone", "iron_bars"),
        features=("wooden crane arm", "grindstone chain tether effect"),
        interior=(),
      ),
    ),
    exterior_features=("crane and tether", "citadel construction arm"),
    tips=("Stack grindstones for chain crane effect",),
  ),
  "epic_bases_holme_raised_entryway": BookBuild(
    id="epic_bases_holme_raised_entryway",
    name="Raised Entryway Bridge",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme raised entryway bridge bottleneck intruders tight vulnerable "
      "sandstone stairs defensive entrance citadel module"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:sandstone_stairs",
      "minecraft:smooth_sandstone",
      "minecraft:dark_oak_planks",
      "minecraft:oak_fence",
    ),
    zones=(
      BuildZone(
        name="entry bridge",
        size=(10, 3, 3),
        materials=("sandstone", "sandstone_stairs", "dark_oak_planks", "oak_fence"),
        features=("raised bridge entryway", "bottleneck defensive stairs"),
        interior=(),
      ),
    ),
    exterior_features=("raised entryway", "defensive bottleneck bridge"),
    tips=("Bridges bottleneck intruders into vulnerable position",),
  ),
  "epic_bases_holme_sky_bridge": BookBuild(
    id="epic_bases_holme_sky_bridge",
    name="Citadel Sky Bridge",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme sky bridge long horizontal walkway connecting tower levels "
      "sandstone dark wood rail citadel module"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:smooth_sandstone",
      "minecraft:dark_oak_planks",
      "minecraft:oak_fence",
      "minecraft:sandstone_slab",
    ),
    zones=(
      BuildZone(
        name="sky walkway",
        size=(12, 2, 3),
        materials=("sandstone", "dark_oak_planks", "oak_fence", "sandstone_slab"),
        features=("long horizontal sky bridge", "connects tower levels"),
        interior=(),
      ),
    ),
    exterior_features=("citadel sky bridge", "tower connecting walkway"),
    tips=("Bridges connect high tower sections",),
  ),
  "epic_bases_holme_great_bell": BookBuild(
    id="epic_bases_holme_great_bell",
    name="Great Bell",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme great bell golden bell open air frame citadel top pealing "
      "valleys architecture school module"
    ),
    palette=(
      "minecraft:gold_block",
      "minecraft:yellow_concrete",
      "minecraft:iron_bars",
      "minecraft:dark_oak_fence",
      "minecraft:smooth_sandstone",
    ),
    zones=(
      BuildZone(
        name="bell tower",
        size=(4, 6, 4),
        materials=("gold_block", "iron_bars", "dark_oak_fence", "smooth_sandstone"),
        features=("large golden bell", "open air bell frame"),
        interior=(),
      ),
    ),
    exterior_features=("great bell", "citadel bell tower"),
    tips=("Bell pealing resonates through the valleys",),
  ),
  "epic_bases_holme_grand_chandelier": BookBuild(
    id="epic_bases_holme_grand_chandelier",
    name="Grand Chandelier",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme grand chandelier multi tier glowstone trapdoor old fashioned "
      "cavernous hall lighting council chamber module"
    ),
    palette=(
      "minecraft:glowstone",
      "minecraft:dark_oak_trapdoor",
      "minecraft:oak_trapdoor",
      "minecraft:dark_oak_fence",
      "minecraft:chain",
    ),
    zones=(
      BuildZone(
        name="chandelier fixture",
        size=(3, 5, 3),
        materials=("glowstone", "dark_oak_trapdoor", "oak_trapdoor", "dark_oak_fence", "chain"),
        features=("multi tier chandelier", "glowstone trapdoor soft light"),
        interior=(),
      ),
    ),
    exterior_features=("grand chandelier", "classy hall lighting"),
    tips=("Glowstone surrounded by trapdoors on fence chain",),
  ),
  "epic_bases_holme_grand_library": BookBuild(
    id="epic_bases_holme_grand_library",
    name="Grand Library",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme grand library floor to ceiling bookshelves architecture "
      "school prestigious study room citadel module"
    ),
    palette=(
      "minecraft:bookshelf",
      "minecraft:oak_planks",
      "minecraft:lantern",
      "minecraft:sandstone",
      "minecraft:ladder",
    ),
    zones=(
      BuildZone(
        name="library hall",
        size=(8, 5, 6),
        materials=("bookshelf", "oak_planks", "sandstone", "lantern"),
        features=("floor to ceiling bookshelves", "grand study library"),
        interior=("architecture school library",),
      ),
    ),
    exterior_features=("grand library", "prestigious study hall"),
    tips=("Students conceive epic bases in these rooms",),
  ),
  "epic_bases_holme_block_museum": BookBuild(
    id="epic_bases_holme_block_museum",
    name="Block Museum",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme block museum display all minecraft blocks study collection "
      "architecture school citadel module"
    ),
    palette=(
      "minecraft:stone",
      "minecraft:oak_planks",
      "minecraft:glass",
      "minecraft:iron_block",
      "minecraft:gold_block",
      "minecraft:diamond_block",
    ),
    zones=(
      BuildZone(
        name="block gallery",
        size=(8, 4, 6),
        materials=("stone", "glass", "iron_block", "gold_block", "diamond_block"),
        features=("displayed block specimens", "study all game blocks"),
        interior=("block collection museum",),
      ),
    ),
    exterior_features=("block museum", "minecraft block gallery"),
    tips=("Students study every block in the game",),
  ),
  "epic_bases_holme_forge": BookBuild(
    id="epic_bases_holme_forge",
    name="Citadel Forge",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme citadel forge furnaces anvil crafting workspace architecture "
      "school lower tower module"
    ),
    palette=(
      "minecraft:furnace",
      "minecraft:anvil",
      "minecraft:smithing_table",
      "minecraft:stone_bricks",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="forge workshop",
        size=(6, 3, 5),
        materials=("furnace", "anvil", "smithing_table", "stone_bricks"),
        features=("furnace crafting forge", "anvil smithing workspace"),
        interior=("crafting workshop",),
      ),
    ),
    exterior_features=("citadel forge", "architecture school workshop"),
    tips=("Forge for student crafting projects",),
  ),
  "epic_bases_holme_indoor_farm": BookBuild(
    id="epic_bases_holme_indoor_farm",
    name="Indoor Terraced Farm",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme indoor terraced farm nether crop research green tiers "
      "architecture school tower farm module"
    ),
    palette=(
      "minecraft:farmland",
      "minecraft:wheat",
      "minecraft:carrots",
      "minecraft:water",
      "minecraft:oak_slab",
      "minecraft:glowstone",
    ),
    zones=(
      BuildZone(
        name="terraced farm",
        size=(6, 4, 4),
        materials=("farmland", "wheat", "carrots", "water", "oak_slab", "glowstone"),
        features=("terraced indoor crop tiers", "nether research farm"),
        interior=(),
      ),
    ),
    exterior_features=("indoor terraced farm", "tower crop research"),
    tips=("Research project for growing crops indoors",),
  ),
  "epic_bases_holme_molten_vent": BookBuild(
    id="epic_bases_holme_molten_vent",
    name="Molten Vent Defense",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme molten vent lava flowing mountain exterior natural defense "
      "intruders citadel base module"
    ),
    palette=(
      "minecraft:lava",
      "minecraft:stone",
      "minecraft:cobblestone",
      "minecraft:obsidian",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="lava vent",
        size=(4, 6, 2),
        materials=("lava", "stone", "cobblestone", "obsidian"),
        features=("lava flowing down mountain", "natural molten defense"),
        interior=(),
      ),
    ),
    exterior_features=("molten vent", "lava mountain defense"),
    tips=("Lava vent acts as natural intruder defense",),
  ),
  "epic_bases_holme_citadel_facade": BookBuild(
    id="epic_bases_holme_citadel_facade",
    name="Citadel Facade",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme citadel facade sandstone red sandstone tall thick walls "
      "narrow windows elevated entryway module"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:red_sandstone",
      "minecraft:smooth_sandstone",
      "minecraft:cut_red_sandstone",
      "minecraft:dark_oak_planks",
    ),
    zones=(
      BuildZone(
        name="tower facade",
        size=(6, 10, 4),
        materials=("sandstone", "red_sandstone", "smooth_sandstone", "dark_oak_planks"),
        features=("tall thick sandstone walls", "red sandstone accents narrow windows"),
        interior=(),
      ),
    ),
    exterior_features=("citadel facade", "sandstone tower exterior"),
    tips=("Sandstone and red sandstone cohesive exterior",),
  ),
  "epic_bases_holme_acacia_balcony": BookBuild(
    id="epic_bases_holme_acacia_balcony",
    name="Acacia Roof Balcony",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme acacia roof balcony peaked orange roof large windows fresh "
      "air sandstone tower module"
    ),
    palette=(
      "minecraft:acacia_stairs",
      "minecraft:acacia_slab",
      "minecraft:dark_oak_planks",
      "minecraft:glass_pane",
      "minecraft:sandstone",
    ),
    zones=(
      BuildZone(
        name="wooden balcony",
        size=(4, 4, 3),
        materials=("acacia_stairs", "dark_oak_planks", "glass_pane", "sandstone"),
        features=("peaked acacia roof balcony", "large window fresh air"),
        interior=(),
      ),
    ),
    exterior_features=("acacia roof balcony", "tower wooden balcony"),
    tips=("Acacia slab peaked roof with large windows",),
  ),
  "epic_bases_holme_murder_hole_wall": BookBuild(
    id="epic_bases_holme_murder_hole_wall",
    name="Murder Hole Window Wall",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme murder hole window wall staircase slit narrow tall windows "
      "shoot out difficult shoot in sandstone module"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:sandstone_stairs",
      "minecraft:smooth_sandstone",
      "minecraft:red_sandstone",
      "minecraft:note_block",
    ),
    zones=(
      BuildZone(
        name="murder hole wall",
        size=(6, 5, 1),
        materials=("sandstone", "sandstone_stairs", "smooth_sandstone", "note_block"),
        features=("staircase slit murder holes", "narrow defensive windows"),
        interior=(),
      ),
    ),
    exterior_features=("murder hole wall", "defensive slit windows"),
    tips=("Stairs create gaps easy to shoot out difficult to shoot in",),
  ),
  "epic_bases_holme_council_table": BookBuild(
    id="epic_bases_holme_council_table",
    name="Council Round Table",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme council round table circular glowstone center arthurian equal "
      "status twelve guild chamber module"
    ),
    palette=(
      "minecraft:oak_planks",
      "minecraft:glowstone",
      "minecraft:orange_terracotta",
      "minecraft:white_terracotta",
      "minecraft:dark_oak_planks",
    ),
    zones=(
      BuildZone(
        name="round table",
        size=(6, 2, 6),
        materials=("oak_planks", "glowstone", "orange_terracotta", "white_terracotta"),
        features=("circular council table", "central recessed glowstone light"),
        interior=(),
      ),
    ),
    exterior_features=("council round table", "equal status chamber table"),
    tips=("Circular table implies no head equal status",),
  ),
  "epic_bases_holme_council_chair": BookBuild(
    id="epic_bases_holme_council_chair",
    name="Council Guild Chair",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme council guild chair trapdoor stair block banner great chair "
      "twelve guild leaders chamber module"
    ),
    palette=(
      "minecraft:dark_oak_stairs",
      "minecraft:dark_oak_trapdoor",
      "minecraft:lime_banner",
      "minecraft:sandstone",
    ),
    zones=(
      BuildZone(
        name="guild chair",
        size=(2, 3, 2),
        materials=("dark_oak_stairs", "dark_oak_trapdoor", "creeper_banner"),
        features=("trapdoor stair banner chair", "great guild leader seat"),
        interior=(),
      ),
    ),
    exterior_features=("council guild chair", "trapdoor stair seat"),
    tips=("Stair seat with trapdoor arms and banner back",),
  ),
  "epic_bases_holme_window_shutters": BookBuild(
    id="epic_bases_holme_window_shutters",
    name="Trapdoor Window Shutters",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme trapdoor window shutters decorative closeable windows block "
      "water sandstone tower module"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:dark_oak_trapdoor",
      "minecraft:glass_pane",
      "minecraft:bookshelf",
      "minecraft:furnace",
    ),
    zones=(
      BuildZone(
        name="shutter window",
        size=(3, 3, 1),
        materials=("sandstone", "dark_oak_trapdoor", "glass_pane"),
        features=("trapdoor decorative shutters", "recessed window opening"),
        interior=(),
      ),
    ),
    exterior_features=("trapdoor shutters", "closeable tower windows"),
    tips=("Trapdoors as shutters block water when closed",),
  ),
  "epic_bases_holme_banner_holder": BookBuild(
    id="epic_bases_holme_banner_holder",
    name="Banner Wall Holder",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme banner wall holder trapdoor fence compact mounting council "
      "chamber decorative module"
    ),
    palette=(
      "minecraft:dark_oak_trapdoor",
      "minecraft:dark_oak_fence",
      "minecraft:yellow_banner",
      "minecraft:sandstone",
      "minecraft:smooth_sandstone",
    ),
    zones=(
      BuildZone(
        name="banner mount",
        size=(2, 3, 1),
        materials=("dark_oak_trapdoor", "dark_oak_fence", "yellow_banner", "sandstone"),
        features=("trapdoor fence banner mount", "compact wall holder"),
        interior=(),
      ),
    ),
    exterior_features=("banner wall holder", "decorative banner mount"),
    tips=("Trapdoor flat on wall fence post banner hanging",),
  ),
  "epic_bases_holme_hang_lights": BookBuild(
    id="epic_bases_holme_hang_lights",
    name="Ceiling Hang Lights",
    theme="academic",
    biome="mountains",
    caption=(
      "craftholme ceiling hang lights glowstone trapdoor fence chain high ceiling "
      "lighting logistical solution module"
    ),
    palette=(
      "minecraft:glowstone",
      "minecraft:oak_trapdoor",
      "minecraft:dark_oak_trapdoor",
      "minecraft:oak_fence",
      "minecraft:chain",
    ),
    zones=(
      BuildZone(
        name="hang light trio",
        size=(4, 4, 2),
        materials=("glowstone", "oak_trapdoor", "dark_oak_trapdoor", "oak_fence", "chain"),
        features=("suspended glowstone lights", "trapdoor wrapped fence chain"),
        interior=(),
      ),
    ),
    exterior_features=("ceiling hang lights", "high ceiling lighting"),
    tips=("Fence chains suspend glowstone trapdoor lights",),
  ),
}

# Mega builds saved for 150³ — not registered yet:
# - epic_bases_fenrirs_tooth (full viking longship with multiple decks and sails)
# - epic_bases_ancient_mummys_tomb (full desert temple cliff complex exterior)
# - epic_bases_lofty_lab (full floating steampunk laboratory airship complex)
# - epic_bases_sunken_estate (full underwater palace exterior)
# - epic_bases_the_exchange (full jungle End portal research complex)
# - epic_bases_the_cube (full alien crash site geometric fortress)
# - epic_bases_glistening_ice_palace (full snowy peaks ice palace complex)
# - epic_bases_shimmering_hoard (full dwarven underground treasure hoard complex)
# - epic_bases_sweet_kingdom (full candyland confectioner paradise complex)
# - epic_bases_macabre_motel (full haunted gothic motel forest complex)
# - epic_bases_phoenix_castle (full defensive medieval castle outpost complex)
# - epic_bases_craftholme (full vertical architecture school citadel complex)
