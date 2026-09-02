"""
Minecraft Epic Builds — modular build catalog.

Full mega-scenes (whole Hanging Village, etc.) are reserved for future 150³
training. Only Inventive Details modules are registered here at 32³.
"""

from __future__ import annotations

from .registry import BookBuild, BuildZone

EPIC_BUILDS: dict[str, BookBuild] = {
  "epic_builds_hanging_tower": BookBuild(
    id="epic_builds_hanging_tower",
    name="Hanging Tower",
    theme="aerial",
    biome="mountains",
    caption=(
      "a hanging village upside down tower dark oak log dark prismarine tapering "
      "floors internal ladders trapdoor sentries cliffside aerial module"
    ),
    palette=(
      "minecraft:dark_oak_log",
      "minecraft:dark_oak_planks",
      "minecraft:dark_prismarine",
      "minecraft:dark_prismarine_stairs",
      "minecraft:ladder",
      "minecraft:oak_trapdoor",
      "minecraft:flowering_azalea_leaves",
    ),
    zones=(
      BuildZone(
        name="6 by 16 hanging tower",
        size=(6, 16, 6),
        materials=("dark_oak_log", "dark_prismarine", "ladder", "oak_trapdoor"),
        features=("tapering multi story tower", "internal ladder floors", "trapdoor sentry lookout"),
        interior=("upside down village floors", "ladder connections"),
      ),
    ),
    exterior_features=("hanging village main tower", "aerial cliffside spire"),
    tips=("Tower narrows toward bottom", "Trapdoors for sentry defense"),
  ),
  "epic_builds_landing_pad": BookBuild(
    id="epic_builds_landing_pad",
    name="Landing Pad",
    theme="aerial",
    biome="mountains",
    caption=(
      "a hanging village elytra landing pad decorative railing water bed impact "
      "absorption fireworks boost entrance platform aerial module"
    ),
    palette=(
      "minecraft:dark_oak_planks",
      "minecraft:dark_prismarine",
      "minecraft:oak_fence",
      "minecraft:water",
      "minecraft:light_blue_stained_glass",
      "minecraft:red_sandstone_wall",
    ),
    zones=(
      BuildZone(
        name="8 by 8 landing pad",
        size=(8, 6, 8),
        materials=("dark_oak_planks", "dark_prismarine", "oak_fence", "water", "red_sandstone_wall"),
        features=("open topped platform", "decorative railing", "water bed impact absorption"),
        interior=("elytra arrival room below",),
      ),
    ),
    exterior_features=("hanging village landing pad", "fireworks elytra entrance"),
    tips=("Fly in with elytra and fireworks", "Water beds prevent fall damage"),
  ),
  "epic_builds_bathhouse": BookBuild(
    id="epic_builds_bathhouse",
    name="Bathhouse",
    theme="aerial",
    biome="mountains",
    caption=(
      "a hanging village bathhouse three story dark prismarine dark oak hot bath "
      "ice pool mud sauna steam room not upside down aerial module"
    ),
    palette=(
      "minecraft:dark_prismarine",
      "minecraft:dark_oak_planks",
      "minecraft:dark_oak_log",
      "minecraft:water",
      "minecraft:ice",
      "minecraft:clay",
      "minecraft:campfire",
    ),
    zones=(
      BuildZone(
        name="12 by 8 bathhouse",
        size=(12, 10, 8),
        materials=("dark_prismarine", "dark_oak_planks", "water", "ice", "clay"),
        features=("three story cutaway bathhouse", "hot and ice pools", "sauna steam rooms"),
        interior=("two rooms per floor", "mud bath treatments"),
      ),
    ),
    exterior_features=("hanging village bathhouse", "right-side-up spa building"),
    tips=("Only building not upside down", "Hot baths ice pools mud saunas"),
  ),
  "epic_builds_mountain_corridor": BookBuild(
    id="epic_builds_mountain_corridor",
    name="Mountain Corridor",
    theme="aerial",
    biome="mountains",
    caption=(
      "a hanging village mountain corridor stone cliff carved entrance wooden "
      "prismarine door cavern storage mine escape route aerial module"
    ),
    palette=(
      "minecraft:stone",
      "minecraft:stone_bricks",
      "minecraft:dark_oak_planks",
      "minecraft:dark_prismarine",
      "minecraft:torch",
      "minecraft:chest",
    ),
    zones=(
      BuildZone(
        name="8 by 12 mountain entrance",
        size=(8, 12, 6),
        materials=("stone", "dark_oak_planks", "dark_prismarine", "torch", "chest"),
        features=("cliff carved corridor entrance", "decorative wooden prismarine door", "cavern storage access"),
        interior=("mountain mine escape route", "storage caverns"),
      ),
    ),
    exterior_features=("hanging village mountain corridor", "cliffside safe passage down"),
    tips=("Only safe way down cliffside", "Leads to farms far below"),
  ),
  "epic_builds_suspended_house": BookBuild(
    id="epic_builds_suspended_house",
    name="Suspended House",
    theme="aerial",
    biome="mountains",
    caption=(
      "a hanging village suspended house anvil chain lowest farthest ornate tiered "
      "tower pointed bottom best view aerial module"
    ),
    palette=(
      "minecraft:dark_oak_log",
      "minecraft:dark_prismarine",
      "minecraft:dark_prismarine_stairs",
      "minecraft:anvil",
      "minecraft:chain",
      "minecraft:flowering_azalea_leaves",
      "minecraft:red_sandstone_wall",
    ),
    zones=(
      BuildZone(
        name="6 by 18 suspended house",
        size=(6, 18, 6),
        materials=("dark_oak_log", "dark_prismarine", "anvil", "chain", "flowering_azalea_leaves"),
        features=("anvil chain suspension", "tapering pointed tower", "spiked ornate roof"),
        interior=("best view penthouse",),
      ),
    ),
    exterior_features=("hanging village suspended house", "lowest farthest viewpoint home"),
    tips=("Hangs by chain of anvils", "Best views in the village"),
  ),
  "epic_builds_fortress": BookBuild(
    id="epic_builds_fortress",
    name="Village Fortress",
    theme="aerial",
    biome="mountains",
    caption=(
      "a hanging village fortress heart social hub red carpet multi room cutaway "
      "largest grandest cliff corner defended aerial module"
    ),
    palette=(
      "minecraft:dark_oak_planks",
      "minecraft:red_carpet",
      "minecraft:dark_prismarine",
      "minecraft:stone_bricks",
      "minecraft:bookshelf",
      "minecraft:lantern",
      "minecraft:red_sandstone_wall",
    ),
    zones=(
      BuildZone(
        name="14 by 10 fortress",
        size=(14, 10, 10),
        materials=("dark_oak_planks", "red_carpet", "dark_prismarine", "stone_bricks", "lantern"),
        features=("multi room fortress cutaway", "red carpet social spaces", "village heart hub"),
        interior=("lounging entertainment rooms", "open interior partitions"),
      ),
    ),
    exterior_features=("hanging village fortress", "largest defended cliff building"),
    tips=("Tucked in cliff overhang corner", "Social hub with open interior spaces"),
  ),
  "epic_builds_water_elevator": BookBuild(
    id="epic_builds_water_elevator",
    name="Water Elevator",
    theme="aerial",
    biome="mountains",
    caption=(
      "a hanging village water elevator soul sand magma vertical column signs "
      "trapdoors prevent flooding up down transport aerial module"
    ),
    palette=(
      "minecraft:dark_prismarine",
      "minecraft:dark_oak_planks",
      "minecraft:water",
      "minecraft:soul_sand",
      "minecraft:magma_block",
      "minecraft:oak_sign",
      "minecraft:oak_trapdoor",
    ),
    zones=(
      BuildZone(
        name="4 by 14 water elevator",
        size=(4, 14, 4),
        materials=("dark_prismarine", "water", "soul_sand", "magma_block", "oak_trapdoor"),
        features=("vertical water column", "soul sand up magma down", "sign trapdoor flood prevention"),
        interior=("bubble elevator shaft",),
      ),
    ),
    exterior_features=("hanging village water elevator", "vertical bubble transport"),
    tips=("Soul sand pushes up magma pulls down", "Trapdoors prevent flooding"),
  ),
  "epic_builds_spiral_staircase": BookBuild(
    id="epic_builds_spiral_staircase",
    name="Spiral Staircase",
    theme="aerial",
    biome="mountains",
    caption=(
      "a hanging village spiral staircase cylindrical tower central wooden pillar "
      "winding oak stairs safe climb alternative aerial module"
    ),
    palette=(
      "minecraft:dark_oak_log",
      "minecraft:oak_stairs",
      "minecraft:dark_prismarine",
      "minecraft:stone_bricks",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="6 by 12 spiral tower",
        size=(6, 12, 6),
        materials=("dark_oak_log", "oak_stairs", "dark_prismarine", "stone_bricks"),
        features=("cylindrical cutaway tower", "central pillar winding stairs", "safe climb alternative"),
        interior=("spiral oak stair ascent",),
      ),
    ),
    exterior_features=("hanging village spiral stairs", "cylindrical stair tower"),
    tips=("Safer alternative to flying", "Wooden stairs wind around central pillar"),
  ),
  "epic_builds_message_train": BookBuild(
    id="epic_builds_message_train",
    name="Message Train",
    theme="aerial",
    biome="mountains",
    caption=(
      "a hanging village message train minecart rail cliffside hopper chest item "
      "transport ground to fortress aerial module"
    ),
    palette=(
      "minecraft:stone",
      "minecraft:rail",
      "minecraft:powered_rail",
      "minecraft:hopper_minecart",
      "minecraft:chest",
      "minecraft:hopper",
      "minecraft:dark_oak_planks",
    ),
    zones=(
      BuildZone(
        name="12 by 8 message train",
        size=(12, 8, 6),
        materials=("stone", "rail", "powered_rail", "hopper_minecart", "chest", "hopper"),
        features=("cliffside minecart rail", "hopper chest item transport", "ground to fortress route"),
        interior=("item delivery system",),
      ),
    ),
    exterior_features=("hanging village message train", "cliff minecart transport"),
    tips=("Transports items from ground to fortress", "Minecart on cliffside rails"),
  ),
  "epic_builds_bridge_supports": BookBuild(
    id="epic_builds_bridge_supports",
    name="Bridge Supports",
    theme="aerial",
    biome="mountains",
    caption=(
      "a hanging village bridge supports tall vertical yellow teal structure multi "
      "level walkways fences crossroads aerial module"
    ),
    palette=(
      "minecraft:dark_oak_log",
      "minecraft:dark_prismarine",
      "minecraft:dark_oak_planks",
      "minecraft:oak_fence",
      "minecraft:red_sandstone_wall",
      "minecraft:flowering_azalea_leaves",
    ),
    zones=(
      BuildZone(
        name="8 by 16 bridge support",
        size=(8, 16, 8),
        materials=("dark_oak_log", "dark_prismarine", "dark_oak_planks", "oak_fence", "red_sandstone_wall"),
        features=("tall vertical support tower", "multi level horizontal walkways", "village crossroads"),
        interior=("bridge connection levels",),
      ),
    ),
    exterior_features=("hanging village bridge supports", "walkway crossroads pillar"),
    tips=("Supports multiple walkway levels", "Fences and planks form crossroads"),
  ),
  "epic_builds_elytra_launcher": BookBuild(
    id="epic_builds_elytra_launcher",
    name="Elytra Launcher",
    theme="aerial",
    biome="mountains",
    caption=(
      "a hanging village elytra fireworks launcher purple concrete sticky piston "
      "slime observer dispensers crying obsidian launch pad aerial module"
    ),
    palette=(
      "minecraft:purple_concrete",
      "minecraft:sticky_piston",
      "minecraft:slime_block",
      "minecraft:observer",
      "minecraft:dispenser",
      "minecraft:crying_obsidian",
      "minecraft:redstone_repeater",
      "minecraft:stone_pressure_plate",
    ),
    zones=(
      BuildZone(
        name="8 by 10 elytra launcher",
        size=(8, 10, 8),
        materials=("purple_concrete", "sticky_piston", "slime_block", "dispenser", "crying_obsidian"),
        features=("piston slime launch pad", "dispenser elytra fireworks", "pressure plate activation"),
        interior=("redstone repeater launch circuit",),
      ),
    ),
    exterior_features=("hanging village elytra launcher", "quickest way to reach village"),
    tips=("8 by 5 base with piston slime stack", "Dispensers hold elytra and fireworks"),
  ),
  "epic_builds_earth_arena": BookBuild(
    id="epic_builds_earth_arena",
    name="Earth Arena",
    theme="arena",
    biome="plains",
    caption=(
      "a survival arena round one earth quadrant podzol coarse dirt obsidian tower "
      "melee battle pitfalls pvp colosseum module"
    ),
    palette=(
      "minecraft:podzol",
      "minecraft:coarse_dirt",
      "minecraft:grass_block",
      "minecraft:obsidian",
      "minecraft:stone_bricks",
      "minecraft:cactus",
      "minecraft:sand",
    ),
    zones=(
      BuildZone(
        name="12 by 10 earth arena",
        size=(12, 10, 10),
        materials=("podzol", "coarse_dirt", "obsidian", "stone_bricks", "cactus"),
        features=("desert earth quadrant", "central obsidian tower", "melee battle pitfalls"),
        interior=("round one pvp arena",),
      ),
    ),
    exterior_features=("survival arena earth round", "colosseum earth quadrant"),
    tips=("Two teams pitted against each other", "Contains pitfalls and cactus traps"),
  ),
  "epic_builds_nether_arena": BookBuild(
    id="epic_builds_nether_arena",
    name="Nether Arena",
    theme="arena",
    biome="nether",
    caption=(
      "a survival arena round two nether quadrant netherrack lava crimson fungus "
      "mob hordes blaze zombie skeleton colosseum module"
    ),
    palette=(
      "minecraft:netherrack",
      "minecraft:nether_bricks",
      "minecraft:lava",
      "minecraft:crimson_nylium",
      "minecraft:crimson_stem",
      "minecraft:soul_sand",
      "minecraft:magma_block",
    ),
    zones=(
      BuildZone(
        name="12 by 10 nether arena",
        size=(12, 10, 10),
        materials=("netherrack", "nether_bricks", "lava", "crimson_stem", "soul_sand"),
        features=("nether themed quadrant", "lava pools crimson fungus", "mob fighting arena"),
        interior=("round two mob horde battle",),
      ),
    ),
    exterior_features=("survival arena nether round", "colosseum nether quadrant"),
    tips=("Winning team advances here", "Battle through hordes of mobs"),
  ),
  "epic_builds_ocean_arena": BookBuild(
    id="epic_builds_ocean_arena",
    name="Ocean Arena",
    theme="arena",
    biome="ocean",
    caption=(
      "a survival arena round three ocean quadrant water parkour floating platforms "
      "towers elytra chest blue cyan colosseum module"
    ),
    palette=(
      "minecraft:water",
      "minecraft:prismarine",
      "minecraft:dark_prismarine",
      "minecraft:sea_lantern",
      "minecraft:chest",
      "minecraft:obsidian",
      "minecraft:quartz_block",
    ),
    zones=(
      BuildZone(
        name="12 by 12 ocean arena",
        size=(12, 12, 12),
        materials=("water", "prismarine", "dark_prismarine", "sea_lantern", "chest", "obsidian"),
        features=("submerged ocean quadrant", "parkour floating platforms", "tower elytra chests"),
        interior=("round three parkour course",),
      ),
    ),
    exterior_features=("survival arena ocean round", "colosseum water parkour quadrant"),
    tips=("Parkour up towers for elytra", "Avoid falling into water"),
  ),
  "epic_builds_escape_portal": BookBuild(
    id="epic_builds_escape_portal",
    name="Escape Portal",
    theme="arena",
    biome="plains",
    caption=(
      "a survival arena round four escape portal circular platform white stairs "
      "central end portal activation final round colosseum module"
    ),
    palette=(
      "minecraft:quartz_block",
      "minecraft:quartz_stairs",
      "minecraft:end_portal_frame",
      "minecraft:ender_eye",
      "minecraft:obsidian",
      "minecraft:sea_lantern",
      "minecraft:purple_concrete",
    ),
    zones=(
      BuildZone(
        name="10 by 8 escape platform",
        size=(10, 8, 10),
        materials=("quartz_block", "quartz_stairs", "end_portal_frame", "ender_eye", "obsidian"),
        features=("circular escape platform", "white cream stairs", "central portal activation"),
        interior=("round four final escape",),
      ),
    ),
    exterior_features=("survival arena escape round", "colosseum final portal"),
    tips=("Portal activates after all rounds", "Leave arena through escape portal"),
  ),
  "epic_builds_grandstand": BookBuild(
    id="epic_builds_grandstand",
    name="Grandstand",
    theme="arena",
    biome="plains",
    caption=(
      "a survival arena grandstand massive multi tier spectator seating quartz purple "
      "concrete rows pillars colosseum module"
    ),
    palette=(
      "minecraft:quartz_block",
      "minecraft:smooth_quartz",
      "minecraft:purple_concrete",
      "minecraft:purpur_block",
      "minecraft:quartz_stairs",
      "minecraft:stone_brick_stairs",
      "minecraft:sea_lantern",
    ),
    zones=(
      BuildZone(
        name="16 by 14 grandstand",
        size=(16, 14, 10),
        materials=("quartz_block", "purple_concrete", "purpur_block", "quartz_stairs", "sea_lantern"),
        features=("multi tier spectator seating", "high vertical rows", "purple cream color scheme"),
        interior=("arena audience stands",),
      ),
    ),
    exterior_features=("survival arena grandstand", "colosseum spectator seating"),
    tips=("Many rows of seats with support pillars", "Off-white and dark purple palette"),
  ),
  "epic_builds_arming_chamber": BookBuild(
    id="epic_builds_arming_chamber",
    name="Arming Chamber",
    theme="arena",
    biome="plains",
    caption=(
      "a survival arena arming chamber chest rows six weapon sets equipment respawn "
      "re-equip purple cream interior colosseum module"
    ),
    palette=(
      "minecraft:purple_concrete",
      "minecraft:quartz_block",
      "minecraft:chest",
      "minecraft:item_frame",
      "minecraft:anvil",
      "minecraft:purpur_block",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="10 by 8 arming chamber",
        size=(10, 8, 8),
        materials=("purple_concrete", "quartz_block", "chest", "item_frame", "anvil"),
        features=("chest rows weapon storage", "six equipment sets", "respawn re-equip room"),
        interior=("gladiator arming station",),
      ),
    ),
    exterior_features=("survival arena arming chamber", "colosseum equipment room"),
    tips=("Beneath or beside grandstand", "Six sets of weapons and gear"),
  ),
  "epic_builds_dueling_towers": BookBuild(
    id="epic_builds_dueling_towers",
    name="Dueling Towers",
    theme="arena",
    biome="plains",
    caption=(
      "a survival arena dueling towers tall obsidian gold accent chest tops exposed "
      "facade vulnerable climb colosseum module"
    ),
    palette=(
      "minecraft:obsidian",
      "minecraft:gold_block",
      "minecraft:chest",
      "minecraft:purple_concrete",
      "minecraft:ladder",
      "minecraft:sea_lantern",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="6 by 16 dueling tower",
        size=(6, 16, 6),
        materials=("obsidian", "gold_block", "chest", "ladder", "sea_lantern", "iron_bars"),
        features=("tall slender obsidian tower", "gold accent tops", "chest rewards exposed facade"),
        interior=("tower climb with vulnerability",),
      ),
    ),
    exterior_features=("survival arena dueling tower", "colosseum reward spire"),
    tips=("Chests on top of each tower", "Exposed facade leaves climbers vulnerable"),
  ),
  "epic_builds_cactus_pitfall": BookBuild(
    id="epic_builds_cactus_pitfall",
    name="Cactus Pitfall",
    theme="arena",
    biome="desert",
    caption=(
      "a survival arena cactus pitfall sand platform pressure plates deep hole desert "
      "trap reflex test colosseum module"
    ),
    palette=(
      "minecraft:sand",
      "minecraft:cactus",
      "minecraft:stone_pressure_plate",
      "minecraft:smooth_stone",
      "minecraft:coarse_dirt",
      "minecraft:podzol",
    ),
    zones=(
      BuildZone(
        name="6 by 6 cactus pitfall",
        size=(6, 6, 6),
        materials=("sand", "cactus", "stone_pressure_plate", "smooth_stone", "coarse_dirt"),
        features=("raised sand platform", "cactus and pressure plates", "deep square pitfall hole"),
        interior=(),
      ),
    ),
    exterior_features=("survival arena cactus trap", "desert pitfall module"),
    tips=("Test player reflexes", "Pressure plates trigger pitfall"),
  ),
  "epic_builds_nether_spawner": BookBuild(
    id="epic_builds_nether_spawner",
    name="Nether Spawner",
    theme="arena",
    biome="nether",
    caption=(
      "a survival arena nether spawner mob spawner netherrack blaze zombie skeleton "
      "continuous spawn nether round colosseum module"
    ),
    palette=(
      "minecraft:spawner",
      "minecraft:netherrack",
      "minecraft:nether_bricks",
      "minecraft:fire",
      "minecraft:iron_bars",
      "minecraft:soul_fire",
    ),
    zones=(
      BuildZone(
        name="4 by 6 nether spawner",
        size=(4, 6, 4),
        materials=("spawner", "netherrack", "nether_bricks", "fire", "iron_bars"),
        features=("mob spawner on netherrack", "continuous blaze zombie skeleton spawn", "nether round trap"),
        interior=(),
      ),
    ),
    exterior_features=("survival arena nether spawner", "mob spawn module"),
    tips=("Use in nether themed rounds", "Spawner on netherrack base"),
  ),
  "epic_builds_auto_armorer": BookBuild(
    id="epic_builds_auto_armorer",
    name="Auto Armorer",
    theme="arena",
    biome="desert",
    caption=(
      "a survival arena auto armorer sandstone hollow square four dispensers inward "
      "quick re-equip after respawn colosseum module"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:smooth_sandstone",
      "minecraft:dispenser",
      "minecraft:stone_pressure_plate",
      "minecraft:iron_block",
      "minecraft:chest",
    ),
    zones=(
      BuildZone(
        name="6 by 6 auto armorer",
        size=(6, 6, 6),
        materials=("sandstone", "dispenser", "stone_pressure_plate", "iron_block"),
        features=("hollow sandstone square", "four inward facing dispensers", "quick armor re-equip"),
        interior=(),
      ),
    ),
    exterior_features=("survival arena auto armorer", "dispenser equipment station"),
    tips=("Players re-equipped after respawn", "Dispensers face inward"),
  ),
  "epic_builds_tnt_trap": BookBuild(
    id="epic_builds_tnt_trap",
    name="TNT Trap",
    theme="arena",
    biome="plains",
    caption=(
      "a survival arena tnt trap stone pressure plate smooth stone tnt vertical "
      "explosion trap colosseum module"
    ),
    palette=(
      "minecraft:stone_pressure_plate",
      "minecraft:smooth_stone",
      "minecraft:tnt",
      "minecraft:stone",
      "minecraft:cobblestone",
    ),
    zones=(
      BuildZone(
        name="3 by 5 tnt trap",
        size=(3, 5, 3),
        materials=("stone_pressure_plate", "smooth_stone", "tnt", "stone"),
        features=("pressure plate on smooth stone", "tnt below trigger", "vertical explosion trap"),
        interior=(),
      ),
    ),
    exterior_features=("survival arena tnt trap", "explosion pitfall module"),
    tips=("Simple pressure plate tnt stack", "Test contestant reflexes"),
  ),
  "epic_builds_sinkhole": BookBuild(
    id="epic_builds_sinkhole",
    name="Sinkhole",
    theme="arena",
    biome="ocean",
    caption=(
      "a survival arena sinkhole underwater whirlpool magma blocks ocean trench blue "
      "water trap colosseum module"
    ),
    palette=(
      "minecraft:water",
      "minecraft:magma_block",
      "minecraft:prismarine",
      "minecraft:sand",
      "minecraft:sea_lantern",
      "minecraft:kelp",
    ),
    zones=(
      BuildZone(
        name="8 by 6 sinkhole",
        size=(8, 6, 8),
        materials=("water", "magma_block", "prismarine", "sand", "kelp"),
        features=("underwater whirlpool trench", "magma block bottom pull", "ocean themed trap"),
        interior=(),
      ),
    ),
    exterior_features=("survival arena sinkhole", "ocean whirlpool trap"),
    tips=("Magma blocks create whirlpool effect", "Ocean round trap module"),
  ),
  "epic_builds_sand_trap": BookBuild(
    id="epic_builds_sand_trap",
    name="Sand Trap",
    theme="arena",
    biome="desert",
    caption=(
      "a survival arena sand trap 5 by 5 pit piston pressure plate signs sand layers "
      "mob spawner piglin brute drop colosseum module"
    ),
    palette=(
      "minecraft:sand",
      "minecraft:red_sand",
      "minecraft:stone_pressure_plate",
      "minecraft:piston",
      "minecraft:spawner",
      "minecraft:oak_sign",
      "minecraft:cactus",
      "minecraft:terracotta",
    ),
    zones=(
      BuildZone(
        name="5 by 6 sand trap",
        size=(5, 6, 5),
        materials=("sand", "stone_pressure_plate", "piston", "spawner", "oak_sign", "cactus"),
        features=("5 by 5 six deep pit", "sign platform sand layers", "piston pressure plate drop"),
        interior=("mob spawner pit bottom",),
      ),
    ),
    exterior_features=("survival arena sand trap", "desert mob drop trap"),
    tips=("Signs hold sand until plate triggered", "Decorate with cactus to disguise"),
  ),
}

# Mega builds saved for 150³ — not registered yet:
# - epic_builds_hanging_village (full upside-down cliffside village complex)
# - epic_builds_survival_arena (full Roman colosseum four-quadrant arena complex)
