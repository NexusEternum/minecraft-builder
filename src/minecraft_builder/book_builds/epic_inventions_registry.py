"""
Minecraft Epic Inventions — modular build catalog.

Full mega-scenes (whole Animal Sanctuary, research center, etc.) are reserved
for future 100³–150³ training (150³ for full chapter spreads). Only Inventive
Details modules are registered here at 32³.
"""

from __future__ import annotations

from .registry import BookBuild, BuildZone

EPIC_INVENTIONS_BUILDS: dict[str, BookBuild] = {
  "epic_inventions_mob_hospital": BookBuild(
    id="epic_inventions_mob_hospital",
    name="Mob Hospital",
    theme="modern",
    biome="badlands",
    caption=(
      "an L-shaped two story mob hospital with smooth sandstone white walls orange "
      "accents grass roof gardens balcony cutouts glass windows badlands animal sanctuary"
    ),
    palette=(
      "minecraft:smooth_sandstone",
      "minecraft:sandstone",
      "minecraft:orange_terracotta",
      "minecraft:grass_block",
      "minecraft:glass_pane",
      "minecraft:birch_fence",
      "minecraft:oak_leaves",
    ),
    zones=(
      BuildZone(
        name="L-shaped hospital shell",
        size=(20, 15, 20),
        materials=("smooth_sandstone", "sandstone", "orange_terracotta", "glass_pane"),
        features=(
          "20 by 20 footprint L-shaped two story clinic",
          "smooth sandstone cream walls orange trim bands",
          "open balcony cutouts and glass patient windows",
        ),
        interior=("birch plank ward floors", "glass recovery rooms"),
      ),
      BuildZone(
        name="roof gardens",
        size=(18, 2, 18),
        materials=("grass_block", "oak_leaves", "birch_fence"),
        features=("flat grass terrace roofs", "wood fence railings", "roof shrubbery"),
        interior=(),
      ),
    ),
    exterior_features=("badlands sanctuary medical wing", "terraced roof gardens"),
    tips=(
      "Use smooth sandstone for clean clinical walls",
      "Orange terracotta bands mark floor levels",
      "Grass blocks on flat roofs for rooftop gardens",
    ),
  ),
  "epic_inventions_sanctuary_farm": BookBuild(
    id="epic_inventions_sanctuary_farm",
    name="Sanctuary Farm",
    theme="rustic",
    biome="badlands",
    caption=(
      "a sanctuary farm module with two dark oak huts stone foundations 25 by 20 crop "
      "field wheat carrots beetroot composters bush borders badlands mob sanctuary food"
    ),
    palette=(
      "minecraft:grass_block",
      "minecraft:dirt",
      "minecraft:farmland",
      "minecraft:wheat",
      "minecraft:carrots",
      "minecraft:beetroots",
      "minecraft:dark_oak_planks",
      "minecraft:dark_oak_log",
      "minecraft:stone_bricks",
      "minecraft:composter",
      "minecraft:oak_leaves",
    ),
    zones=(
      BuildZone(
        name="twin farm huts",
        size=(8, 6, 6),
        materials=("dark_oak_planks", "dark_oak_log", "stone_bricks"),
        features=("two rustic storage barns", "stone brick foundations", "dark oak roofs"),
        interior=("composter", "barrel storage"),
      ),
      BuildZone(
        name="25 by 20 crop field",
        size=(25, 1, 20),
        materials=("farmland", "wheat", "carrots", "beetroots", "dirt"),
        features=("tilled rows", "mixed crop rotation", "leaf hedge border"),
        interior=(),
      ),
    ),
    exterior_features=("sanctuary food production plot", "badlands farm module"),
    tips=("Pair huts beside one large tilled field", "Mix wheat carrots and beetroot rows"),
  ),
  "epic_inventions_sanctuary_tower": BookBuild(
    id="epic_inventions_sanctuary_tower",
    name="Sanctuary Tower",
    theme="modern",
    biome="badlands",
    caption=(
      "a tall 8 by 8 sanctuary watchtower smooth sandstone pillar wooden observation "
      "deck oak trapdoor ladder railings pointed roof badlands mob sanctuary lookout"
    ),
    palette=(
      "minecraft:smooth_sandstone",
      "minecraft:sandstone",
      "minecraft:oak_fence",
      "minecraft:oak_trapdoor",
      "minecraft:oak_planks",
      "minecraft:ladder",
      "minecraft:dark_oak_stairs",
    ),
    zones=(
      BuildZone(
        name="8 by 8 sandstone mast",
        size=(8, 25, 8),
        materials=("smooth_sandstone", "sandstone"),
        features=("tapering white pillar", "25 blocks tall", "badlands observation mast"),
        interior=("ladder shaft",),
      ),
      BuildZone(
        name="observation deck",
        size=(8, 4, 8),
        materials=("oak_planks", "oak_fence", "oak_trapdoor", "dark_oak_stairs"),
        features=(
          "open roof deck with fence railings",
          "exterior trapdoor ladder rungs",
          "peaked dark oak cap",
        ),
        interior=(),
      ),
    ),
    exterior_features=("sanctuary perimeter lookout", "trapdoor exterior ladder"),
    tips=("Use flipped trapdoors as ladder rungs on the outside", "Widen base slightly before tapering"),
  ),
  "epic_inventions_bee_habitat": BookBuild(
    id="epic_inventions_bee_habitat",
    name="Bee Habitat",
    theme="natural",
    biome="plains",
    caption=(
      "a floating bee habitat terrain chunk 25 by 25 grass dirt pond oak trees bee nests "
      "flowers leaf canopy sanctuary naturalistic mob enclosure"
    ),
    palette=(
      "minecraft:grass_block",
      "minecraft:dirt",
      "minecraft:stone",
      "minecraft:water",
      "minecraft:oak_log",
      "minecraft:oak_leaves",
      "minecraft:bee_nest",
      "minecraft:poppy",
      "minecraft:dandelion",
      "minecraft:cornflower",
    ),
    zones=(
      BuildZone(
        name="25 by 25 terrain island",
        size=(25, 8, 25),
        materials=("grass_block", "dirt", "stone"),
        features=("organic floating chunk", "grass topped dirt layers", "stone underside"),
        interior=(),
      ),
      BuildZone(
        name="forest clearing",
        size=(20, 12, 20),
        materials=("oak_log", "oak_leaves", "water", "bee_nest", "poppy"),
        features=("central blue pond", "dense oak canopy", "bee nests under leaves", "wildflowers"),
        interior=(),
      ),
    ),
    exterior_features=("natural bee sanctuary vignette", "mini biome island"),
    tips=("Hide bee nests beneath leaf canopies", "Keep a small pond at the clearing center"),
  ),
  "epic_inventions_marine_sanctuary": BookBuild(
    id="epic_inventions_marine_sanctuary",
    name="Marine Sanctuary",
    theme="aquatic",
    biome="ocean",
    caption=(
      "a 15 by 15 marine sanctuary glass water tank kelp seagrass sand floor glowing "
      "conduit center underwater mob sanctuary aquarium column"
    ),
    palette=(
      "minecraft:light_blue_stained_glass",
      "minecraft:water",
      "minecraft:sand",
      "minecraft:kelp",
      "minecraft:seagrass",
      "minecraft:conduit",
      "minecraft:prismarine",
      "minecraft:sea_lantern",
    ),
    zones=(
      BuildZone(
        name="15 by 15 aquarium column",
        size=(15, 25, 15),
        materials=("light_blue_stained_glass", "water", "sand"),
        features=("tall glass water volume", "25 blocks tall tank", "sand gravel floor"),
        interior=(),
      ),
      BuildZone(
        name="underwater habitat",
        size=(13, 20, 13),
        materials=("kelp", "seagrass", "conduit", "prismarine", "sea_lantern"),
        features=("central glowing conduit", "kelp forest", "seagrass patches"),
        interior=(),
      ),
    ),
    exterior_features=("vertical marine exhibit tank", "conduit lit underwater column"),
    tips=("Fill with water before adding kelp", "Center a conduit on prismarine base"),
  ),
  "epic_inventions_horse_stable": BookBuild(
    id="epic_inventions_horse_stable",
    name="Horse Stable",
    theme="rustic",
    biome="plains",
    caption=(
      "a simple 10 by 8 horse stable open wooden frame roof hay bale floor oak fence "
      "gate corner posts mob sanctuary animal shelter"
    ),
    palette=(
      "minecraft:oak_fence",
      "minecraft:oak_planks",
      "minecraft:oak_slab",
      "minecraft:oak_trapdoor",
      "minecraft:hay_block",
      "minecraft:grass_block",
    ),
    zones=(
      BuildZone(
        name="10 by 8 stable shelter",
        size=(10, 6, 8),
        materials=("oak_fence", "oak_planks", "oak_slab", "oak_trapdoor", "hay_block"),
        features=(
          "four corner fence posts",
          "flat slab trapdoor roof",
          "hay bale bedding floor",
          "fence gate entry",
        ),
        interior=("hay bale floor",),
      ),
    ),
    exterior_features=("open air horse pen", "sanctuary stable module"),
    tips=("Use hay blocks for bedding", "Keep front open with fence gate"),
  ),
  "epic_inventions_forcefield_emitter": BookBuild(
    id="epic_inventions_forcefield_emitter",
    name="Forcefield Emitter",
    theme="sci_fi",
    biome="badlands",
    caption=(
      "a forcefield emitter pedestal smooth sandstone quartz gold accents red sand base "
      "tall pink stained glass energy wall badlands sanctuary shield generator"
    ),
    palette=(
      "minecraft:red_sand",
      "minecraft:smooth_sandstone",
      "minecraft:quartz_block",
      "minecraft:gold_block",
      "minecraft:pink_stained_glass",
      "minecraft:sea_lantern",
    ),
    zones=(
      BuildZone(
        name="7 by 7 emitter base",
        size=(7, 8, 7),
        materials=("red_sand", "smooth_sandstone", "quartz_block", "gold_block"),
        features=("ornate white pedestal", "gold cap accents", "red sand mesa pad"),
        interior=("sea lantern core",),
      ),
      BuildZone(
        name="pink forcefield wall",
        size=(1, 24, 7),
        materials=("pink_stained_glass", "sea_lantern"),
        features=("vertical translucent energy panel", "glowing column"),
        interior=(),
      ),
    ),
    exterior_features=("sanctuary shield emitter", "pink glass forcefield panel"),
    tips=("Stack pink stained glass for the energy wall", "Place sea lanterns inside the panel"),
  ),
  "epic_inventions_villager_housing": BookBuild(
    id="epic_inventions_villager_housing",
    name="Villager Housing",
    theme="rustic",
    biome="plains",
    caption=(
      "hillside villager housing bunker grass topped earth shelter glass skylights "
      "wooden fence pens doorways cut into dirt hill mob sanctuary underground homes"
    ),
    palette=(
      "minecraft:grass_block",
      "minecraft:dirt",
      "minecraft:stone",
      "minecraft:glass_pane",
      "minecraft:oak_fence",
      "minecraft:oak_door",
      "minecraft:daylight_detector",
      "minecraft:spruce_planks",
    ),
    zones=(
      BuildZone(
        name="16 by 16 grass hill",
        size=(16, 14, 16),
        materials=("grass_block", "dirt", "stone"),
        features=("earth sheltered mound", "grass skylight panels", "daylight detectors on roof"),
        interior=(),
      ),
      BuildZone(
        name="buried villager rooms",
        size=(12, 8, 12),
        materials=("spruce_planks", "glass_pane", "oak_door", "oak_fence"),
        features=(
          "two level hillside dwellings",
          "glass roof windows in turf",
          "fence animal pens at entrance",
        ),
        interior=("spruce plank floors", "oak door entries"),
      ),
    ),
    exterior_features=("bunker style mob housing hill", "discreet grass roof skylights"),
    tips=("Blend doors into the hillside face", "Use daylight detectors flush on grass"),
  ),
  "epic_inventions_mob_feeder": BookBuild(
    id="epic_inventions_mob_feeder",
    name="Mob Feeder",
    theme="redstone",
    biome="plains",
    caption=(
      "a 7 by 7 mob feeder redstone machine four dispensers chest hopper platform "
      "central drop chute pressure plate mob sanctuary automatic feeding station"
    ),
    palette=(
      "minecraft:grass_block",
      "minecraft:stone_bricks",
      "minecraft:smooth_sandstone",
      "minecraft:dispenser",
      "minecraft:chest",
      "minecraft:hopper",
      "minecraft:heavy_weighted_pressure_plate",
      "minecraft:oak_planks",
    ),
    zones=(
      BuildZone(
        name="7 by 7 feeder platform",
        size=(7, 7, 7),
        materials=("stone_bricks", "smooth_sandstone", "dispenser", "chest", "hopper"),
        features=(
          "four dispensers facing central chute",
          "corner chest storage",
          "raised stone platform on grass",
        ),
        interior=("hopper collection pit", "pressure plate trigger"),
      ),
    ),
    exterior_features=("automatic mob feeding station", "dispenser ring around drop chute"),
    tips=("Point dispensers inward toward the central hole", "Hide hoppers under sandstone cover"),
  ),
  "epic_inventions_water_trough": BookBuild(
    id="epic_inventions_water_trough",
    name="Automatic Water Trough",
    theme="utility",
    biome="plains",
    caption=(
      "a 20 block long automatic water trough blue water channel dark oak frame iron "
      "bar end gates mob sanctuary livestock watering station"
    ),
    palette=(
      "minecraft:water",
      "minecraft:dark_oak_planks",
      "minecraft:dark_oak_slab",
      "minecraft:iron_bars",
      "minecraft:light_blue_banner",
      "minecraft:stone_brick_slab",
      "minecraft:grass_block",
    ),
    zones=(
      BuildZone(
        name="20 by 5 water trough",
        size=(20, 5, 5),
        materials=("water", "dark_oak_planks", "dark_oak_slab", "iron_bars"),
        features=(
          "long narrow water channel",
          "dark oak plank sides",
          "iron bar end frames",
          "light blue banner accents",
        ),
        interior=(),
      ),
    ),
    exterior_features=("livestock water trough module", "automatic watering channel"),
    tips=("Line channel with dark oak planks", "Cap ends with iron bar frames"),
  ),
  "epic_inventions_pumpkin_farm": BookBuild(
    id="epic_inventions_pumpkin_farm",
    name="Pumpkin Farm",
    theme="gothic",
    biome="plains",
    caption=(
      "a 10 by 12 monster factory pumpkin farm grass plot oak tree pumpkin patch "
      "wooden fence chest storage gothic castle courtyard garden module"
    ),
    palette=(
      "minecraft:grass_block",
      "minecraft:dirt",
      "minecraft:pumpkin",
      "minecraft:oak_log",
      "minecraft:oak_leaves",
      "minecraft:oak_fence",
      "minecraft:chest",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="10 by 12 pumpkin plot",
        size=(10, 8, 12),
        materials=("grass_block", "pumpkin", "oak_fence", "chest"),
        features=("pumpkin patch rows", "corner oak tree", "fence border", "storage chest"),
        interior=(),
      ),
    ),
    exterior_features=("gothic castle courtyard farm", "pumpkin supply garden"),
    tips=("Keep plot compact beside castle walls", "Add lantern near chest"),
  ),
  "epic_inventions_enchanting_tower": BookBuild(
    id="epic_inventions_enchanting_tower",
    name="Enchanting Tower",
    theme="gothic",
    biome="plains",
    caption=(
      "a circular 20 block enchanting tower cutaway deepslate stone brick walls "
      "bookshelf library enchantment table pink carpet candles crenellated roof "
      "monster factory gothic castle library module"
    ),
    palette=(
      "minecraft:deepslate_tiles",
      "minecraft:stone_bricks",
      "minecraft:bookshelf",
      "minecraft:enchanting_table",
      "minecraft:pink_carpet",
      "minecraft:candle",
      "minecraft:lantern",
      "minecraft:purple_banner",
    ),
    zones=(
      BuildZone(
        name="20 block circular tower",
        size=(20, 18, 20),
        materials=("deepslate_tiles", "stone_bricks", "bookshelf", "pink_carpet"),
        features=(
          "circular gothic tower shell",
          "crenellated parapet with candles",
          "purple banner accents",
        ),
        interior=("bookshelf ring library", "central enchantment table platform"),
      ),
    ),
    exterior_features=("gothic castle enchanting library", "circular tower cutaway"),
    tips=("Line curved walls with bookshelves three blocks high", "Pink carpet around enchant table"),
  ),
  "epic_inventions_gothic_buttress": BookBuild(
    id="epic_inventions_gothic_buttress",
    name="Gothic Buttress",
    theme="gothic",
    biome="plains",
    caption=(
      "a gothic flying buttress stone brick deepslate tile arched support pier "
      "stone wall stairs slab bridge monster factory castle wall reinforcement module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:stone_brick_stairs",
      "minecraft:stone_brick_slab",
      "minecraft:stone_brick_wall",
      "minecraft:deepslate_tiles",
      "minecraft:polished_basalt",
    ),
    zones=(
      BuildZone(
        name="flying buttress pair",
        size=(8, 22, 12),
        materials=("stone_bricks", "stone_brick_stairs", "stone_brick_wall", "deepslate_tiles"),
        features=("arched flying buttress", "vertical pier", "slab stair arch bridge"),
        interior=(),
      ),
    ),
    exterior_features=("castle wall support buttress", "gothic arched brace"),
    tips=("Use stairs and walls for arched rib", "Pair buttresses along tall curtain walls"),
  ),
  "epic_inventions_stained_glass_window": BookBuild(
    id="epic_inventions_stained_glass_window",
    name="Gothic Stained-Glass Window",
    theme="gothic",
    biome="plains",
    caption=(
      "a tall pointed gothic stained glass window purple stained glass tinted glass "
      "stone brick deepslate tile tracery monster factory castle facade module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:deepslate_tiles",
      "minecraft:stone_brick_stairs",
      "minecraft:purple_stained_glass",
      "minecraft:black_stained_glass",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="11 by 28 gothic window",
        size=(11, 28, 3),
        materials=("stone_bricks", "deepslate_tiles", "purple_stained_glass", "black_stained_glass"),
        features=("pointed arch window frame", "purple glass tracery panels", "lantern sill"),
        interior=(),
      ),
    ),
    exterior_features=("gothic cathedral window panel", "purple stained glass tracery"),
    tips=("Layer purple and black glass for tracery pattern", "Frame with deepslate tile columns"),
  ),
  "epic_inventions_golem_maker": BookBuild(
    id="epic_inventions_golem_maker",
    name="Golem Maker",
    theme="industrial",
    biome="plains",
    caption=(
      "an 11 by 11 golem maker redstone machine lime concrete frame four pistons "
      "dispenser carved pumpkin iron block assembly repeaters monster factory "
      "automatic iron golem builder module"
    ),
    palette=(
      "minecraft:lime_concrete",
      "minecraft:redstone_dust",
      "minecraft:redstone_repeater",
      "minecraft:piston",
      "minecraft:dispenser",
      "minecraft:iron_block",
      "minecraft:carved_pumpkin",
      "minecraft:chest",
      "minecraft:lever",
    ),
    zones=(
      BuildZone(
        name="11 by 11 golem assembly core",
        size=(11, 10, 11),
        materials=("lime_concrete", "piston", "dispenser", "redstone_repeater", "redstone_dust"),
        features=(
          "cross shaped lime concrete frame",
          "four inward facing pistons",
          "top dispenser pumpkin head",
          "repeater timing circuit",
        ),
        interior=("iron block assembly pad", "redstone repeater lines"),
      ),
    ),
    exterior_features=("automatic iron golem factory core", "piston pumpkin dispenser rig"),
    tips=("Set center repeaters to four ticks", "Dispenser drops carved pumpkin on iron cross"),
  ),
  "epic_inventions_storm_catcher": BookBuild(
    id="epic_inventions_storm_catcher",
    name="Storm Catcher",
    theme="industrial",
    biome="plains",
    caption=(
      "a storm catcher lightning rod tower deepslate tile framework lime stained glass "
      "energy column copper rod lantern crown monster factory golem maker spire module"
    ),
    palette=(
      "minecraft:deepslate_tiles",
      "minecraft:polished_basalt",
      "minecraft:lime_stained_glass",
      "minecraft:lightning_rod",
      "minecraft:lantern",
      "minecraft:iron_bars",
      "minecraft:redstone_lamp",
    ),
    zones=(
      BuildZone(
        name="6 by 6 storm spire",
        size=(6, 28, 6),
        materials=("deepslate_tiles", "lime_stained_glass", "lightning_rod", "lantern"),
        features=(
          "vertical lime glass energy shaft",
          "deepslate tile exoskeleton frame",
          "copper lightning rod mast",
          "lantern ring crown",
        ),
        interior=("redstone lamp core glow",),
      ),
    ),
    exterior_features=("lightning powered storm spire", "golem factory energy tower"),
    tips=("Center lime stained glass energy column", "Cap with lightning rod for storm flavor"),
  ),
  "epic_inventions_golem_factory_ring": BookBuild(
    id="epic_inventions_golem_factory_ring",
    name="Golem Factory Ring",
    theme="gothic",
    biome="plains",
    caption=(
      "a 26 block diameter golem factory circular deepslate tile wall ring crenellations "
      "lantern torches hollow courtyard monster factory gothic castle round keep module"
    ),
    palette=(
      "minecraft:deepslate_tiles",
      "minecraft:polished_basalt",
      "minecraft:stone_bricks",
      "minecraft:lantern",
      "minecraft:redstone_torch",
      "minecraft:iron_bars",
      "minecraft:blackstone",
    ),
    zones=(
      BuildZone(
        name="26 diameter factory ring",
        size=(26, 10, 26),
        materials=("deepslate_tiles", "polished_basalt", "stone_bricks", "lantern"),
        features=(
          "circular crenellated curtain wall",
          "lantern and redstone torch glow",
          "hollow inner courtyard",
        ),
        interior=("basalt factory floor",),
      ),
    ),
    exterior_features=("round monster factory courtyard wall", "gothic industrial ring keep"),
    tips=("Keep ring hollow for golem maker center", "Alternate lanterns with redstone torch glow"),
  ),
  "epic_inventions_cat_shrine": BookBuild(
    id="epic_inventions_cat_shrine",
    name="Cat Shrine",
    theme="kawaii",
    biome="plains",
    caption=(
      "a 10 by 10 kawaii cat shrine totem white concrete grey green cat face banner "
      "gold halo water stream blue base kawaii waterways race starting finish line "
      "decor module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:gray_concrete",
      "minecraft:lime_concrete",
      "minecraft:yellow_concrete",
      "minecraft:blue_concrete",
      "minecraft:water",
      "minecraft:white_banner",
      "minecraft:gold_block",
    ),
    zones=(
      BuildZone(
        name="10 by 10 cat shrine totem",
        size=(10, 24, 10),
        materials=("white_concrete", "gray_concrete", "lime_concrete", "gold_block", "water"),
        features=("cat face banner concrete", "golden halo ring", "water stream column"),
        interior=(),
      ),
    ),
    exterior_features=("kawaii race line cat idol", "anti-cheat shrine decor"),
    tips=("Use banners and concrete for cat face", "Water stream down front of totem"),
  ),
  "epic_inventions_spectator_stands": BookBuild(
    id="epic_inventions_spectator_stands",
    name="Spectator Stands",
    theme="kawaii",
    biome="plains",
    caption=(
      "kawaii waterways spectator stands 20 by 16 white cloud tiers dark oak seating "
      "fence railings pink white striped awning wool grandstand race viewing module"
    ),
    palette=(
      "minecraft:white_wool",
      "minecraft:white_concrete",
      "minecraft:dark_oak_stairs",
      "minecraft:dark_oak_slab",
      "minecraft:dark_oak_fence",
      "minecraft:pink_wool",
      "minecraft:water",
    ),
    zones=(
      BuildZone(
        name="20 by 16 cloud grandstand",
        size=(20, 15, 16),
        materials=("white_wool", "white_concrete", "dark_oak_stairs", "pink_wool"),
        features=("three tier seating", "cloud shaped white shell", "pink white striped awning"),
        interior=("dark oak stair seats", "fence railings"),
      ),
    ),
    exterior_features=("racecourse viewing stands", "kawaii cloud grandstand"),
    tips=("Embed dark oak stairs in white cloud tiers", "Alternate pink and white wool awning"),
  ),
  "epic_inventions_rainbow_bridge": BookBuild(
    id="epic_inventions_rainbow_bridge",
    name="Rainbow Bridge",
    theme="kawaii",
    biome="plains",
    caption=(
      "a 20 block kawaii rainbow bridge white concrete sides red orange yellow green "
      "blue purple walkway segments arched water crossing racecourse module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:red_concrete",
      "minecraft:orange_concrete",
      "minecraft:yellow_concrete",
      "minecraft:lime_concrete",
      "minecraft:light_blue_concrete",
      "minecraft:blue_concrete",
      "minecraft:purple_concrete",
      "minecraft:water",
    ),
    zones=(
      BuildZone(
        name="20 by 8 rainbow arch bridge",
        size=(20, 8, 10),
        materials=(
          "white_concrete",
          "red_concrete",
          "orange_concrete",
          "yellow_concrete",
          "lime_concrete",
          "light_blue_concrete",
          "blue_concrete",
          "purple_concrete",
        ),
        features=("segmented rainbow walkway", "white arched sides", "water channel below"),
        interior=(),
      ),
    ),
    exterior_features=("kawaii race rainbow crossing", "multicolor concrete deck"),
    tips=("Lay rainbow colors in walkway segments", "White concrete arch sides over water"),
  ),
  "epic_inventions_rainbow_finish_arch": BookBuild(
    id="epic_inventions_rainbow_finish_arch",
    name="Rainbow Finish Arch",
    theme="kawaii",
    biome="plains",
    caption=(
      "a kawaii rainbow finish line arch 18 wide concentric colored rings red orange "
      "yellow green blue purple cat face water cascade white cloud frame race end gate"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:red_concrete",
      "minecraft:orange_concrete",
      "minecraft:yellow_concrete",
      "minecraft:lime_concrete",
      "minecraft:light_blue_concrete",
      "minecraft:blue_concrete",
      "minecraft:purple_concrete",
      "minecraft:water",
      "minecraft:pink_concrete",
    ),
    zones=(
      BuildZone(
        name="18 block rainbow finish gate",
        size=(18, 22, 4),
        materials=(
          "white_concrete",
          "red_concrete",
          "orange_concrete",
          "yellow_concrete",
          "lime_concrete",
          "light_blue_concrete",
          "blue_concrete",
          "purple_concrete",
          "water",
        ),
        features=("concentric rainbow ring arch", "cat face finish idol", "water mouth cascade"),
        interior=(),
      ),
    ),
    exterior_features=("race finish rainbow portal", "uphill finish line gate"),
    tips=("Stack concentric rainbow concrete rings", "Water pours from cat mouth opening"),
  ),
  "epic_inventions_floating_cloud": BookBuild(
    id="epic_inventions_floating_cloud",
    name="Floating Cloud Island",
    theme="kawaii",
    biome="plains",
    caption=(
      "a kawaii floating cloud island 20 by 14 white wool concrete pink cherry tree "
      "water pool glowstone kawaii waterways race platform module"
    ),
    palette=(
      "minecraft:white_wool",
      "minecraft:white_concrete",
      "minecraft:pink_wool",
      "minecraft:pink_concrete",
      "minecraft:dark_oak_log",
      "minecraft:water",
      "minecraft:glowstone",
    ),
    zones=(
      BuildZone(
        name="20 by 14 cloud platform",
        size=(20, 12, 14),
        materials=("white_wool", "white_concrete", "pink_wool", "water", "glowstone"),
        features=("blob shaped cloud island", "pink tree canopy", "central water pool"),
        interior=(),
      ),
    ),
    exterior_features=("kawaii cloud race island", "floating wool platform"),
    tips=("Mix white wool and concrete for clouds", "Pink wool blob tree on platform"),
  ),
  "epic_inventions_reverse_waterfall": BookBuild(
    id="epic_inventions_reverse_waterfall",
    name="Reverse Waterfall",
    theme="kawaii",
    biome="plains",
    caption=(
      "a 12 by 12 reverse waterfall white cloud tower soul sand bubble column water "
      "lift vertical race kawaii waterways anti-gravity waterfall module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:white_wool",
      "minecraft:water",
      "minecraft:soul_sand",
      "minecraft:glass",
      "minecraft:sea_lantern",
    ),
    zones=(
      BuildZone(
        name="12 by 12 bubble lift tower",
        size=(12, 26, 12),
        materials=("white_concrete", "water", "soul_sand", "glass", "sea_lantern"),
        features=("hollow cloud shaft", "soul sand bubble column", "26 block vertical lift"),
        interior=("water bubble elevator", "soul sand floor"),
      ),
    ),
    exterior_features=("upward water lift tower", "kawaii cloud bubble column"),
    tips=("Soul sand at base pushes boats upward", "White shell hides inner water column"),
  ),
  "epic_inventions_rainbow_piston_bridge": BookBuild(
    id="epic_inventions_rainbow_piston_bridge",
    name="Rainbow Piston Bridge",
    theme="kawaii",
    biome="plains",
    caption=(
      "a 24 by 16 rainbow piston bridge white floor rainbow stripe walls piston bumpers "
      "tripwire boat guide kawaii waterways race track extension module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:sea_lantern",
      "minecraft:red_concrete",
      "minecraft:orange_concrete",
      "minecraft:yellow_concrete",
      "minecraft:lime_concrete",
      "minecraft:light_blue_concrete",
      "minecraft:blue_concrete",
      "minecraft:purple_concrete",
      "minecraft:piston",
      "minecraft:water",
    ),
    zones=(
      BuildZone(
        name="24 by 16 piston water bridge",
        size=(24, 10, 16),
        materials=("white_concrete", "sea_lantern", "piston", "water"),
        features=("rainbow vertical stripe walls", "piston boat bumpers", "sea lantern floor"),
        interior=("tripwire piston edges",),
      ),
    ),
    exterior_features=("boat guide piston bridge", "rainbow walled water channel"),
    tips=("Pistons along edges keep boats centered", "Rainbow concrete vertical stripes"),
  ),
  "epic_inventions_bridge_island": BookBuild(
    id="epic_inventions_bridge_island",
    name="Bridge Island",
    theme="kawaii",
    biome="plains",
    caption=(
      "a 20 by 20 kawaii bridge island white cloud water path rainbow arch yellow "
      "checkpoint hut kawaii waterways race island module"
    ),
    palette=(
      "minecraft:white_wool",
      "minecraft:white_concrete",
      "minecraft:water",
      "minecraft:yellow_concrete",
      "minecraft:red_concrete",
      "minecraft:orange_concrete",
      "minecraft:lime_concrete",
      "minecraft:blue_concrete",
      "minecraft:purple_concrete",
    ),
    zones=(
      BuildZone(
        name="20 by 20 cloud bridge island",
        size=(20, 15, 20),
        materials=("white_wool", "white_concrete", "water", "yellow_concrete"),
        features=("cloud island water channel", "rainbow arch checkpoint", "yellow hut marker"),
        interior=(),
      ),
    ),
    exterior_features=("mid-race cloud island", "rainbow arch checkpoint"),
    tips=("Curve water through cloud island", "Small rainbow arch over channel"),
  ),
  "epic_inventions_jump_island": BookBuild(
    id="epic_inventions_jump_island",
    name="Jump Island",
    theme="kawaii",
    biome="plains",
    caption=(
      "an 18 by 18 kawaii jump island white cloud pink tree piston boat launcher "
      "redstone pad kawaii waterways race bounce module"
    ),
    palette=(
      "minecraft:white_wool",
      "minecraft:white_concrete",
      "minecraft:pink_wool",
      "minecraft:dark_oak_log",
      "minecraft:piston",
      "minecraft:sticky_piston",
      "minecraft:redstone_block",
      "minecraft:water",
      "minecraft:slime_block",
    ),
    zones=(
      BuildZone(
        name="18 by 18 boat jump island",
        size=(18, 14, 18),
        materials=("white_wool", "pink_wool", "piston", "sticky_piston", "water"),
        features=("cloud island pink tree", "piston boat launch pad", "hidden redstone bounce"),
        interior=("sticky piston launcher", "redstone block trigger"),
      ),
    ),
    exterior_features=("boat bounce jump island", "piston launch cloud pad"),
    tips=("Hide pistons under white cloud shell", "Slime or piston pad launches boats"),
  ),
  "epic_inventions_potions_lab": BookBuild(
    id="epic_inventions_potions_lab",
    name="Potions Lab",
    theme="industrial",
    biome="nether",
    caption=(
      "a paranormal facility potions lab white concrete quartz brewing stands wall "
      "dispensers central dark table nether research laboratory module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:quartz_bricks",
      "minecraft:smooth_stone",
      "minecraft:brewing_stand",
      "minecraft:dispenser",
      "minecraft:black_concrete",
      "minecraft:glass_pane",
    ),
    zones=(
      BuildZone(
        name="12 by 12 potions lab",
        size=(12, 8, 12),
        materials=("white_concrete", "quartz_bricks", "brewing_stand", "dispenser", "black_concrete"),
        features=("wall mounted dispensers", "brewing stand stations", "central research table"),
        interior=("brewing stands", "dispenser racks"),
      ),
    ),
    exterior_features=("nether dimension research lab", "potion brewing room"),
    tips=("Line walls with dispensers for ingredient storage", "Black concrete central table"),
  ),
  "epic_inventions_briefing_room": BookBuild(
    id="epic_inventions_briefing_room",
    name="Briefing Room",
    theme="industrial",
    biome="nether",
    caption=(
      "a paranormal facility briefing room white concrete yellow accents white stair "
      "seating rows lectern dark screen wall nether laboratory conference module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:quartz_bricks",
      "minecraft:yellow_concrete",
      "minecraft:smooth_quartz_stairs",
      "minecraft:lectern",
      "minecraft:black_concrete",
      "minecraft:glass_pane",
    ),
    zones=(
      BuildZone(
        name="16 by 12 briefing room",
        size=(16, 8, 12),
        materials=("white_concrete", "yellow_concrete", "smooth_quartz_stairs", "lectern"),
        features=("tiered white stair seating", "yellow trim bands", "lectern presentation front"),
        interior=("lectern", "black concrete screen wall"),
      ),
    ),
    exterior_features=("lab conference briefing hall", "scientist seating rows"),
    tips=("White stairs as auditorium seats", "Yellow concrete accent stripes on walls"),
  ),
  "epic_inventions_research_cells": BookBuild(
    id="epic_inventions_research_cells",
    name="Research Cells",
    theme="industrial",
    biome="nether",
    caption=(
      "four paranormal facility research cells white concrete green accent stripe iron "
      "door isolation pods nether laboratory specimen containment module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:green_concrete",
      "minecraft:quartz_bricks",
      "minecraft:iron_door",
      "minecraft:iron_bars",
      "minecraft:glass_pane",
      "minecraft:smooth_stone",
    ),
    zones=(
      BuildZone(
        name="four cell containment row",
        size=(16, 8, 8),
        materials=("white_concrete", "green_concrete", "iron_door", "iron_bars", "glass_pane"),
        features=("four identical isolation cells", "green concrete roof stripe", "iron door entries"),
        interior=("specimen cell interiors", "iron bar windows"),
      ),
    ),
    exterior_features=("nether lab holding cells", "green stripe containment block"),
    tips=("Repeat four equal cells in a row", "Green concrete band along roofline"),
  ),
  "epic_inventions_sword_mosaic": BookBuild(
    id="epic_inventions_sword_mosaic",
    name="Sword Mosaic",
    theme="industrial",
    biome="nether",
    caption=(
      "a paranormal facility sword mosaic floor decoration gold block blackstone outline "
      "vertical wall emblem nether laboratory decorative art module"
    ),
    palette=(
      "minecraft:gold_block",
      "minecraft:blackstone",
      "minecraft:polished_blackstone",
      "minecraft:quartz_bricks",
      "minecraft:white_concrete",
    ),
    zones=(
      BuildZone(
        name="12 by 16 sword mosaic",
        size=(12, 12, 2),
        materials=("gold_block", "blackstone", "polished_blackstone", "quartz_bricks"),
        features=("gold sword floor mosaic", "blackstone outline", "vertical wall display"),
        interior=(),
      ),
    ),
    exterior_features=("lab decorative sword emblem", "gold black mosaic art"),
    tips=("Gold blocks for blade and hilt", "Blackstone border outline"),
  ),
  "epic_inventions_corrosive_lab": BookBuild(
    id="epic_inventions_corrosive_lab",
    name="Corrosive Substances Lab",
    theme="industrial",
    biome="nether",
    caption=(
      "a paranormal facility corrosive substances lab white counters blue glass acid tank "
      "laboratory sinks machinery nether research hazardous materials module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:quartz_bricks",
      "minecraft:light_blue_stained_glass",
      "minecraft:water",
      "minecraft:cauldron",
      "minecraft:iron_bars",
      "minecraft:smooth_stone",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="14 by 14 corrosive lab",
        size=(14, 10, 14),
        materials=("white_concrete", "light_blue_stained_glass", "cauldron", "iron_bars", "water"),
        features=("central blue acid glass tank", "white counter workstations", "sink stations"),
        interior=("cauldron sinks", "lantern lighting"),
      ),
    ),
    exterior_features=("hazardous acid research room", "glass tank corrosive lab"),
    tips=("Blue stained glass tank for acid visual", "White counters around perimeter"),
  ),
  "epic_inventions_battery_power": BookBuild(
    id="epic_inventions_battery_power",
    name="Battery Power Source",
    theme="industrial",
    biome="nether",
    caption=(
      "a 10 by 10 paranormal facility battery power pillar white quartz frame glass "
      "crying obsidian core orange cross crown nether lab energy module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:quartz_bricks",
      "minecraft:glass_pane",
      "minecraft:crying_obsidian",
      "minecraft:orange_concrete",
      "minecraft:sea_lantern",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="10 by 10 battery pillar",
        size=(10, 18, 10),
        materials=("white_concrete", "quartz_bricks", "glass_pane", "crying_obsidian", "orange_concrete"),
        features=("glass enclosed obsidian core", "orange cross crown", "18 block energy pillar"),
        interior=("crying obsidian battery core", "sea lantern glow"),
      ),
    ),
    exterior_features=("nether lab power battery", "vertical energy column"),
    tips=("Crying obsidian inside glass shell", "Orange concrete cross on top"),
  ),
  "epic_inventions_vine_room": BookBuild(
    id="epic_inventions_vine_room",
    name="Vine Room",
    theme="industrial",
    biome="nether",
    caption=(
      "a 24 by 16 paranormal facility vine room red border warped vines minecart rail "
      "floor jungle research chamber nether laboratory plant module"
    ),
    palette=(
      "minecraft:red_concrete",
      "minecraft:white_concrete",
      "minecraft:warped_vines",
      "minecraft:warped_wart_block",
      "minecraft:rail",
      "minecraft:powered_rail",
      "minecraft:smooth_stone",
    ),
    zones=(
      BuildZone(
        name="24 by 16 vine chamber",
        size=(24, 8, 16),
        materials=("red_concrete", "white_concrete", "warped_vines", "warped_wart_block", "rail"),
        features=("dense warped vine forest", "red concrete wall border", "minecart rail floor grid"),
        interior=("powered rail network", "warped vine canopy"),
      ),
    ),
    exterior_features=("nether plant research room", "vine filled rail chamber"),
    tips=("Fill interior with hanging warped vines", "Red concrete thick wall frame"),
  ),
  "epic_inventions_piston_extender": BookBuild(
    id="epic_inventions_piston_extender",
    name="Double Piston Extender",
    theme="redstone",
    biome="nether",
    caption=(
      "a paranormal facility double piston extender redstone mechanism observers repeaters "
      "sticky pistons door circuit nether lab redstone module"
    ),
    palette=(
      "minecraft:smooth_stone",
      "minecraft:sticky_piston",
      "minecraft:piston",
      "minecraft:observer",
      "minecraft:redstone_repeater",
      "minecraft:redstone_dust",
      "minecraft:white_concrete",
    ),
    zones=(
      BuildZone(
        name="7 by 5 piston extender",
        size=(7, 5, 5),
        materials=("sticky_piston", "piston", "observer", "redstone_repeater", "redstone_dust"),
        features=("double piston extension", "observer trigger", "repeater timing chain"),
        interior=("redstone dust circuit",),
      ),
    ),
    exterior_features=("lab piston door mechanism", "double extender redstone"),
    tips=("Observers detect block updates", "Repeaters set piston timing"),
  ),
  "epic_inventions_nether_transport_hub": BookBuild(
    id="epic_inventions_nether_transport_hub",
    name="Nether Transport Hub",
    theme="infernal",
    biome="nether",
    caption=(
      "a 22 by 15 nether transport hub obsidian portal white gold black decorative frame "
      "minecart rail approach paranormal facility dimensional gateway module"
    ),
    palette=(
      "minecraft:obsidian",
      "minecraft:nether_portal",
      "minecraft:white_concrete",
      "minecraft:black_concrete",
      "minecraft:gold_block",
      "minecraft:quartz_bricks",
      "minecraft:rail",
      "minecraft:polished_blackstone",
    ),
    zones=(
      BuildZone(
        name="22 by 15 portal hub",
        size=(22, 25, 15),
        materials=("obsidian", "nether_portal", "white_concrete", "gold_block", "black_concrete", "rail"),
        features=("obsidian nether portal", "white gold black frame", "minecart rail entry platform"),
        interior=(),
      ),
    ),
    exterior_features=("dimensional portal transport hub", "decorated nether gateway"),
    tips=("Frame portal with white and gold accents", "Rails lead into portal platform"),
  ),
  "epic_inventions_defense_barrier": BookBuild(
    id="epic_inventions_defense_barrier",
    name="Defense Barrier",
    theme="industrial",
    biome="nether",
    caption=(
      "a paranormal facility defense barrier blackstone wall segment white banners iron "
      "bar grate nether laboratory security module"
    ),
    palette=(
      "minecraft:blackstone",
      "minecraft:polished_blackstone",
      "minecraft:white_banner",
      "minecraft:iron_bars",
      "minecraft:stone_brick_wall",
    ),
    zones=(
      BuildZone(
        name="7 by 5 defense wall",
        size=(7, 5, 5),
        materials=("blackstone", "polished_blackstone", "white_banner", "iron_bars"),
        features=("blackstone wall segment", "three white banners", "iron bar grate"),
        interior=(),
      ),
    ),
    exterior_features=("lab security barrier", "banner defended wall"),
    tips=("White banners on blackstone face", "Iron bars as window grate"),
  ),
  "epic_inventions_disposal_unit": BookBuild(
    id="epic_inventions_disposal_unit",
    name="Disposal Unit",
    theme="industrial",
    biome="nether",
    caption=(
      "a 32 block long paranormal facility disposal unit corridor white green walls blue "
      "glass floor trench nether laboratory waste chute module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:green_concrete",
      "minecraft:light_blue_stained_glass",
      "minecraft:water",
      "minecraft:iron_bars",
      "minecraft:smooth_stone",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="32 by 6 disposal corridor",
        size=(32, 6, 6),
        materials=("white_concrete", "green_concrete", "light_blue_stained_glass", "water", "iron_bars"),
        features=("long narrow disposal hall", "blue glass floor trench", "green white wall stripes"),
        interior=("water disposal trench",),
      ),
    ),
    exterior_features=("lab waste disposal corridor", "glass floor chute hall"),
    tips=("Blue glass over water trench floor", "Alternate green white wall panels"),
  ),
  "epic_inventions_backup_generator": BookBuild(
    id="epic_inventions_backup_generator",
    name="Backup Power Generator",
    theme="industrial",
    biome="nether",
    caption=(
      "a 26 by 26 paranormal facility backup generator room white grey brick green accents "
      "copper rods furnaces water tiles nether laboratory power plant module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:stone_bricks",
      "minecraft:green_concrete",
      "minecraft:copper_block",
      "minecraft:lightning_rod",
      "minecraft:furnace",
      "minecraft:water",
      "minecraft:smooth_stone",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="26 by 26 generator hall",
        size=(26, 12, 26),
        materials=("white_concrete", "stone_bricks", "green_concrete", "copper_block", "furnace", "water"),
        features=("open roof generator room", "copper rod machinery", "water cooled tile floor"),
        interior=("furnace banks", "copper lightning rod arrays"),
      ),
    ),
    exterior_features=("backup power generator hall", "copper machinery plant room"),
    tips=("Copper blocks and rods as machinery", "Green concrete trim on white walls"),
  ),
  "epic_inventions_mechanical_leg": BookBuild(
    id="epic_inventions_mechanical_leg",
    name="Mechanical Spider Leg",
    theme="steampunk",
    biome="plains",
    caption=(
      "a mechanical spider leg white iron green joint segments eight legged saloon "
      "walking western support limb steampunk mobile base module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:iron_block",
      "minecraft:lime_concrete",
      "minecraft:iron_bars",
      "minecraft:oxidized_cut_copper",
      "minecraft:stone_bricks",
    ),
    zones=(
      BuildZone(
        name="6 by 6 mechanical leg",
        size=(6, 28, 6),
        materials=("white_concrete", "iron_block", "lime_concrete", "iron_bars", "oxidized_cut_copper"),
        features=("segmented robotic leg", "green copper joints", "angled support strut"),
        interior=(),
      ),
    ),
    exterior_features=("walking saloon spider leg", "elevated steampunk limb"),
    tips=("Alternate white iron and green joint bands", "One of eight saloon support legs"),
  ),
  "epic_inventions_bunkhouse": BookBuild(
    id="epic_inventions_bunkhouse",
    name="Saloon Bunkhouse",
    theme="western",
    biome="plains",
    caption=(
      "a four story saloon bunkhouse yellow oak wood red beds chests stair bunks "
      "patron housing eight legged walking saloon dormitory module"
    ),
    palette=(
      "minecraft:oak_planks",
      "minecraft:yellow_terracotta",
      "minecraft:red_bed",
      "minecraft:chest",
      "minecraft:oak_stairs",
      "minecraft:oak_fence",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="8 by 8 four story bunkhouse",
        size=(8, 16, 8),
        materials=("oak_planks", "yellow_terracotta", "red_bed", "chest", "oak_stairs"),
        features=("four bunk floors", "red bed rows", "oak stair connections"),
        interior=("red beds", "chest storage", "shared bunkrooms"),
      ),
    ),
    exterior_features=("walking saloon patron housing", "multi story bunk tower"),
    tips=("Stack four identical bunk floors", "Yellow terracotta outer shell"),
  ),
  "epic_inventions_band_pavilion": BookBuild(
    id="epic_inventions_band_pavilion",
    name="Band Pavilion",
    theme="western",
    biome="plains",
    caption=(
      "a saloon band pavilion elevated oak platform yellow railing corner posts "
      "crate stage eight legged walking saloon music deck module"
    ),
    palette=(
      "minecraft:oak_planks",
      "minecraft:yellow_terracotta",
      "minecraft:oak_fence",
      "minecraft:oak_log",
      "minecraft:barrel",
      "minecraft:note_block",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="10 by 10 band stage",
        size=(10, 6, 10),
        materials=("oak_planks", "yellow_terracotta", "oak_fence", "barrel", "note_block"),
        features=("raised performance deck", "yellow railings", "corner log posts", "barrel stage props"),
        interior=(),
      ),
    ),
    exterior_features=("saloon musician pavilion", "elevated bandstand"),
    tips=("Oak fence railing around deck edge", "Barrels and note blocks as instruments"),
  ),
  "epic_inventions_control_sphere": BookBuild(
    id="epic_inventions_control_sphere",
    name="Control Sphere",
    theme="steampunk",
    biome="plains",
    caption=(
      "a saloon control sphere green frame glass facets wooden floor ladder redstone "
      "panels dunking stool controls eight legged walking saloon hub module"
    ),
    palette=(
      "minecraft:lime_concrete",
      "minecraft:green_concrete",
      "minecraft:glass_pane",
      "minecraft:oak_planks",
      "minecraft:ladder",
      "minecraft:lever",
      "minecraft:redstone_lamp",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="14 block control sphere",
        size=(14, 14, 14),
        materials=("lime_concrete", "green_concrete", "glass_pane", "oak_planks", "ladder"),
        features=("hollow geodesic sphere", "glass panel facets", "central control deck"),
        interior=("levers", "redstone lamp panels", "ladder access"),
      ),
    ),
    exterior_features=("walking saloon command sphere", "leg mechanism control hub"),
    tips=("Green skeleton with glass infill", "Oak floor and ladder inside"),
  ),
  "epic_inventions_saloon_stables": BookBuild(
    id="epic_inventions_saloon_stables",
    name="Saloon Stables",
    theme="western",
    biome="plains",
    caption=(
      "a 20 block saloon stables yellow oak peaked roof open arch stalls hay trough "
      "horse donkey mule pig mounts eight legged walking saloon barn module"
    ),
    palette=(
      "minecraft:oak_planks",
      "minecraft:yellow_terracotta",
      "minecraft:oak_fence",
      "minecraft:hay_block",
      "minecraft:oak_slab",
      "minecraft:lantern",
      "minecraft:water",
    ),
    zones=(
      BuildZone(
        name="20 by 8 saloon stables",
        size=(20, 8, 8),
        materials=("oak_planks", "yellow_terracotta", "oak_fence", "hay_block", "water"),
        features=("peaked roof barn", "open arch horse stalls", "food troughs"),
        interior=("hay bedding", "water troughs"),
      ),
    ),
    exterior_features=("walking saloon mount barn", "western stable row"),
    tips=("Repeat open arch stalls along length", "Hay and water in each stall"),
  ),
  "epic_inventions_ornithopter": BookBuild(
    id="epic_inventions_ornithopter",
    name="Ornithopter",
    theme="steampunk",
    biome="plains",
    caption=(
      "a saloon ornithopter scout aircraft white iron yellow wing grid wide flat "
      "body eight legged walking saloon flying machine module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:iron_block",
      "minecraft:yellow_concrete",
      "minecraft:iron_bars",
      "minecraft:oak_planks",
      "minecraft:lightning_rod",
    ),
    zones=(
      BuildZone(
        name="24 by 16 ornithopter wings",
        size=(24, 4, 16),
        materials=("white_concrete", "iron_block", "yellow_concrete", "iron_bars", "lightning_rod"),
        features=("wide flat wings", "grid wing pattern", "central scout body", "iron bar struts"),
        interior=(),
      ),
    ),
    exterior_features=("saloon scout ornithopter", "resource gathering aircraft"),
    tips=("Two ornithopters on full saloon", "Yellow and white wing grid pattern"),
  ),
  "epic_inventions_piston_bar": BookBuild(
    id="epic_inventions_piston_bar",
    name="Piston Bar Table",
    theme="western",
    biome="plains",
    caption=(
      "a wild west piston bar table orange carpet extended pistons redstone torches "
      "sandstone keg barrels drinks eight legged saloon tavern module"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:smooth_sandstone",
      "minecraft:piston",
      "minecraft:redstone_torch",
      "minecraft:orange_carpet",
      "minecraft:barrel",
      "minecraft:oak_planks",
    ),
    zones=(
      BuildZone(
        name="12 by 6 piston bar",
        size=(12, 5, 6),
        materials=("sandstone", "piston", "redstone_torch", "orange_carpet", "barrel"),
        features=("piston extended bar top", "orange carpet counter", "keg barrel storage"),
        interior=("barrel drink kegs",),
      ),
    ),
    exterior_features=("saloon piston bar counter", "redstone torch table lift"),
    tips=("Redstone torches keep pistons extended", "Orange carpet on piston table top"),
  ),
  "epic_inventions_dunking_stool": BookBuild(
    id="epic_inventions_dunking_stool",
    name="Dunking Stool",
    theme="western",
    biome="plains",
    caption=(
      "a wild west dunking stool water pool quartz border oak trapdoor arm target block "
      "entertainment eight legged saloon carnival module"
    ),
    palette=(
      "minecraft:water",
      "minecraft:smooth_quartz",
      "minecraft:quartz_block",
      "minecraft:oak_planks",
      "minecraft:oak_trapdoor",
      "minecraft:target",
      "minecraft:oak_fence",
    ),
    zones=(
      BuildZone(
        name="8 by 8 dunk tank",
        size=(8, 6, 8),
        materials=("water", "smooth_quartz", "oak_trapdoor", "target", "oak_fence"),
        features=("square dunk pool", "trapdoor seat arm", "target block trigger"),
        interior=(),
      ),
    ),
    exterior_features=("saloon dunking stool game", "wild west water tank"),
    tips=("Trapdoor seat over water pool", "Hit target to drop victim"),
  ),
  "epic_inventions_smoke_stack": BookBuild(
    id="epic_inventions_smoke_stack",
    name="Smoke Stack",
    theme="steampunk",
    biome="plains",
    caption=(
      "saloon smoke stacks oxidized copper campfire chimneys iron quartz tower "
      "trapdoor vents eight legged walking saloon ventilation module"
    ),
    palette=(
      "minecraft:oxidized_cut_copper",
      "minecraft:campfire",
      "minecraft:oak_trapdoor",
      "minecraft:iron_block",
      "minecraft:quartz_block",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="triple smoke stack set",
        size=(12, 14, 6),
        materials=("oxidized_cut_copper", "campfire", "oak_trapdoor", "iron_block", "quartz_block"),
        features=("copper campfire chimneys", "quartz iron tower stack", "trapdoor vent caps"),
        interior=(),
      ),
    ),
    exterior_features=("saloon ventilation chimneys", "campfire smoke stacks"),
    tips=("Campfires on copper stacks for smoke", "Quartz iron tower for engine exhaust"),
  ),
  "epic_inventions_waterfall_elevator": BookBuild(
    id="epic_inventions_waterfall_elevator",
    name="Waterfall Elevator",
    theme="western",
    biome="plains",
    caption=(
      "a saloon waterfall elevator oak log plank tower water column target block "
      "dispenser entrance eight legged walking saloon vertical access module"
    ),
    palette=(
      "minecraft:oak_planks",
      "minecraft:oak_log",
      "minecraft:water",
      "minecraft:target",
      "minecraft:dispenser",
      "minecraft:ladder",
      "minecraft:redstone_dust",
    ),
    zones=(
      BuildZone(
        name="5 by 5 elevator tower",
        size=(5, 24, 5),
        materials=("oak_planks", "oak_log", "water", "target", "dispenser", "ladder"),
        features=("vertical water shaft", "target triggered dispenser", "24 block oak tower"),
        interior=("swim up water column", "target at base"),
      ),
    ),
    exterior_features=("saloon bow shot entrance elevator", "waterfall access tower"),
    tips=("Hit target to trigger top dispenser water", "Only entrance to walking saloon"),
  ),
  "epic_inventions_signal_ladder": BookBuild(
    id="epic_inventions_signal_ladder",
    name="Signal Ladder",
    theme="redstone",
    biome="plains",
    caption=(
      "a redstone torch signal ladder vertical instant redstone climb oak backing "
      "target to dispenser link eight legged saloon elevator circuit module"
    ),
    palette=(
      "minecraft:oak_planks",
      "minecraft:redstone_torch",
      "minecraft:redstone_dust",
      "minecraft:target",
      "minecraft:dispenser",
      "minecraft:stone",
    ),
    zones=(
      BuildZone(
        name="3 by 24 signal ladder",
        size=(3, 24, 3),
        materials=("oak_planks", "redstone_torch", "redstone_dust", "target", "dispenser"),
        features=("vertical torch tower ladder", "instant redstone climb", "target dispenser link"),
        interior=("redstone torch chain",),
      ),
    ),
    exterior_features=("saloon elevator redstone ladder", "instant vertical signal"),
    tips=("Alternate torches up oak backing", "Connects target block to top dispenser"),
  ),
  "epic_inventions_aqueduct": BookBuild(
    id="epic_inventions_aqueduct",
    name="Jungle Aqueduct",
    theme="historical",
    biome="jungle",
    caption=(
      "a temple of wonders jungle aqueduct stone brick deepslate tiered pillars water "
      "channel hanging vines banyan tree city water transport module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:mossy_stone_bricks",
      "minecraft:deepslate",
      "minecraft:water",
      "minecraft:vine",
      "minecraft:cobblestone",
      "minecraft:birch_slab",
    ),
    zones=(
      BuildZone(
        name="16 by 8 aqueduct segment",
        size=(16, 10, 8),
        materials=("stone_bricks", "mossy_stone_bricks", "deepslate", "water", "vine"),
        features=("tiered pillar supports", "raised water channel", "hanging vines"),
        interior=(),
      ),
    ),
    exterior_features=("jungle temple aqueduct", "banyan city water bridge"),
    tips=("Use local stone and deepslate from tunnels", "Vines hang from aqueduct base"),
  ),
  "epic_inventions_cave_network": BookBuild(
    id="epic_inventions_cave_network",
    name="Cave Network",
    theme="historical",
    biome="jungle",
    caption=(
      "a temple of wonders underground cave network stone dirt tunnel wooden supports "
      "orange torch glow jungle temple tunnel system module"
    ),
    palette=(
      "minecraft:stone",
      "minecraft:dirt",
      "minecraft:oak_planks",
      "minecraft:oak_fence",
      "minecraft:torch",
      "minecraft:cobblestone",
      "minecraft:gravel",
    ),
    zones=(
      BuildZone(
        name="14 by 10 cave tunnel",
        size=(14, 8, 10),
        materials=("stone", "dirt", "oak_planks", "oak_fence", "torch", "cobblestone"),
        features=("cutaway tunnel section", "wooden shoring supports", "warm torch lighting"),
        interior=("underground passage",),
      ),
    ),
    exterior_features=("jungle temple cave network", "deep tunnel segment"),
    tips=("Mix stone and dirt cavern walls", "Oak fence and plank tunnel supports"),
  ),
  "epic_inventions_treasure_room": BookBuild(
    id="epic_inventions_treasure_room",
    name="Treasure Room",
    theme="historical",
    biome="jungle",
    caption=(
      "a temple of wonders circular treasure room deepslate gold ore walls chest "
      "gold platform lantern ceiling jungle temple underground vault module"
    ),
    palette=(
      "minecraft:deepslate",
      "minecraft:deepslate_gold_ore",
      "minecraft:gold_block",
      "minecraft:chest",
      "minecraft:lantern",
      "minecraft:polished_deepslate",
      "minecraft:chiseled_deepslate",
    ),
    zones=(
      BuildZone(
        name="10 block diameter treasure vault",
        size=(10, 8, 10),
        materials=("deepslate", "deepslate_gold_ore", "gold_block", "chest", "lantern"),
        features=("circular gold ore lined chamber", "central chest platform", "lantern ceiling"),
        interior=("treasure chest", "gold block pedestal"),
      ),
    ),
    exterior_features=("jungle temple treasure vault", "underground gold room"),
    tips=("Line walls with deepslate gold ore", "Single chest on raised gold platform"),
  ),
  "epic_inventions_temple_tower": BookBuild(
    id="epic_inventions_temple_tower",
    name="Temple Tower",
    theme="historical",
    biome="jungle",
    caption=(
      "a temple of wonders tiered tower white quartz orange accent dark trim fences "
      "slabs stairs ornate jungle temple spire module"
    ),
    palette=(
      "minecraft:quartz_block",
      "minecraft:smooth_quartz",
      "minecraft:orange_terracotta",
      "minecraft:black_concrete",
      "minecraft:quartz_stairs",
      "minecraft:quartz_slab",
      "minecraft:oak_fence",
      "minecraft:lantern",
    ),
    zones=(
      BuildZone(
        name="8 by 8 temple tower",
        size=(8, 22, 8),
        materials=("quartz_block", "smooth_quartz", "orange_terracotta", "black_concrete", "quartz_stairs"),
        features=("tapering tiered spire", "orange highlight bands", "ornate fence trim details"),
        interior=(),
      ),
    ),
    exterior_features=("jungle temple wonder tower", "ancient restored spire"),
    tips=("Taper tower with each tier inset", "Orange terracotta accent alcoves"),
  ),
  "epic_inventions_gravel_trap": BookBuild(
    id="epic_inventions_gravel_trap",
    name="Gravel Trap",
    theme="historical",
    biome="jungle",
    caption=(
      "a temple of wonders gravel trap stone brick bridge lava pools sticky piston "
      "gravel drop pressure plates signal ladder booby trap module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:gravel",
      "minecraft:lava",
      "minecraft:sticky_piston",
      "minecraft:redstone_dust",
      "minecraft:stone_pressure_plate",
      "minecraft:iron_bars",
      "minecraft:chain",
    ),
    zones=(
      BuildZone(
        name="14 by 10 gravel trap",
        size=(14, 12, 10),
        materials=("stone_bricks", "gravel", "lava", "sticky_piston", "redstone_dust", "iron_bars"),
        features=("narrow lava bridge", "overhead gravel chamber", "pressure plate triggers"),
        interior=("sticky piston gravel release", "signal ladder circuit"),
      ),
    ),
    exterior_features=("jungle temple booby trap", "gravel drop bridge trap"),
    tips=("150 gravel blocks held by sticky pistons", "Pressure plates line the bridge"),
  ),
  "epic_inventions_banyan_altar": BookBuild(
    id="epic_inventions_banyan_altar",
    name="Banyan Altar",
    theme="historical",
    biome="jungle",
    caption=(
      "a temple of wonders banyan altar smooth sandstone wide stairs cave entrance "
      "torch pillars redstone lighting mob spawner control jungle temple module"
    ),
    palette=(
      "minecraft:smooth_sandstone",
      "minecraft:sandstone",
      "minecraft:sandstone_stairs",
      "minecraft:stone_brick_wall",
      "minecraft:torch",
      "minecraft:redstone_lamp",
      "minecraft:lever",
      "minecraft:coal_block",
    ),
    zones=(
      BuildZone(
        name="16 by 12 banyan altar",
        size=(16, 10, 12),
        materials=("smooth_sandstone", "sandstone_stairs", "stone_brick_wall", "torch", "redstone_lamp"),
        features=("symmetrical wide stair approach", "dark cave altar entrance", "torch pillar rows"),
        interior=("redstone lamp spawner lighting", "lever control"),
      ),
    ),
    exterior_features=("jungle temple altar entrance", "undead infested shrine"),
    tips=("Wide sandstone stairs to cave mouth", "Redstone controls interior lighting"),
  ),
  "epic_inventions_combination_door": BookBuild(
    id="epic_inventions_combination_door",
    name="Combination Door",
    theme="historical",
    biome="jungle",
    caption=(
      "a temple of wonders combination door lime terracotta lever sequence sticky pistons "
      "deepslate gold ore candles chiseled blackstone temple gate module"
    ),
    palette=(
      "minecraft:lime_terracotta",
      "minecraft:deepslate_bricks",
      "minecraft:polished_blackstone",
      "minecraft:chiseled_deepslate",
      "minecraft:chiseled_polished_blackstone",
      "minecraft:deepslate_gold_ore",
      "minecraft:sticky_piston",
      "minecraft:lever",
      "minecraft:candle",
      "minecraft:gold_block",
    ),
    zones=(
      BuildZone(
        name="10 by 12 combination gate",
        size=(10, 14, 6),
        materials=("lime_terracotta", "deepslate_bricks", "sticky_piston", "lever", "deepslate_gold_ore"),
        features=("lever sequence puzzle door", "sticky piston gate", "decrepit gold ore facade"),
        interior=("chiseled blackstone tunnel", "signal ladder redstone"),
      ),
    ),
    exterior_features=("jungle temple combination lock gate", "ancient lever puzzle door"),
    tips=("Specific lever order opens pistons", "Candles and gold ore for decay look"),
  ),
  "epic_inventions_control_bridge": BookBuild(
    id="epic_inventions_control_bridge",
    name="Control Bridge",
    theme="sci_fi",
    biome="space",
    caption=(
      "a pathfinder space station control bridge cylindrical hub white concrete gray "
      "consoles three deck command center life support hydroponics gravity engine "
      "power management module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:gray_concrete",
      "minecraft:orange_concrete",
      "minecraft:iron_bars",
      "minecraft:sea_lantern",
      "minecraft:glass_pane",
      "minecraft:light_blue_concrete",
    ),
    zones=(
      BuildZone(
        name="10 by 10 cylindrical bridge",
        size=(10, 12, 10),
        materials=("white_concrete", "gray_concrete", "orange_concrete", "iron_bars", "sea_lantern"),
        features=("three level command deck", "circular cutaway bridge", "console stations"),
        interior=("command consoles", "crew seating", "sea lantern radiance"),
      ),
    ),
    exterior_features=("pathfinder control bridge", "space station command hub"),
    tips=("Hub manages life support and engine power", "Three stacked command levels"),
  ),
  "epic_inventions_space_engine": BookBuild(
    id="epic_inventions_space_engine",
    name="Space Engine",
    theme="sci_fi",
    biome="space",
    caption=(
      "a pathfinder space station engine bulbous reactor blue glowing core white "
      "scaffolding walkways iron bars thousands of blocks per second propulsion "
      "module"
    ),
    palette=(
      "minecraft:gray_concrete",
      "minecraft:white_concrete",
      "minecraft:water",
      "minecraft:sea_lantern",
      "minecraft:iron_bars",
      "minecraft:iron_block",
      "minecraft:orange_concrete",
    ),
    zones=(
      BuildZone(
        name="12 by 14 engine module",
        size=(12, 14, 12),
        materials=("gray_concrete", "white_concrete", "water", "sea_lantern", "iron_bars"),
        features=("bulbous engine housing", "glowing blue reactor core", "internal scaffolding"),
        interior=("reactor chamber", "walkway scaffolding", "iron bar supports"),
      ),
    ),
    exterior_features=("pathfinder propulsion engine", "intergalactic drive module"),
    tips=("Blue water or sea lantern core glow", "White scaffold walkways inside hull"),
  ),
  "epic_inventions_crew_lounge": BookBuild(
    id="epic_inventions_crew_lounge",
    name="Crew Lounge",
    theme="sci_fi",
    biome="space",
    caption=(
      "a pathfinder space station crew lounge circular relaxation room gray walls "
      "white light blue floor tiles sparse furniture astronaut rest area module"
    ),
    palette=(
      "minecraft:gray_concrete",
      "minecraft:white_concrete",
      "minecraft:light_blue_concrete",
      "minecraft:oak_planks",
      "minecraft:sea_lantern",
      "minecraft:glass_pane",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="10 block diameter lounge",
        size=(10, 6, 10),
        materials=("gray_concrete", "white_concrete", "light_blue_concrete", "oak_planks"),
        features=("circular lounge cutaway", "checker floor tiles", "sparse crew furniture"),
        interior=("relaxation seating", "sea lantern lighting"),
      ),
    ),
    exterior_features=("pathfinder crew lounge", "ring station rest area"),
    tips=("Top-down circular lounge layout", "White and light blue floor grid"),
  ),
  "epic_inventions_ring_section": BookBuild(
    id="epic_inventions_ring_section",
    name="Ring Section",
    theme="sci_fi",
    biome="space",
    caption=(
      "a pathfinder space station ring section rotating wheel cross section spokes "
      "ten floors crew quarters water gravity sensor beds hydroponics hundreds of "
      "astronauts habitat module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:gray_concrete",
      "minecraft:water",
      "minecraft:oak_planks",
      "minecraft:green_concrete",
      "minecraft:sea_lantern",
      "minecraft:iron_bars",
    ),
    zones=(
      BuildZone(
        name="16 by 12 ring cross section",
        size=(16, 14, 12),
        materials=("white_concrete", "gray_concrete", "water", "oak_planks", "green_concrete"),
        features=("rotating wheel ring cutaway", "spoke hub connection", "multi floor crew rooms"),
        interior=("beds and desks", "hydroponics green blocks", "water gravity sensor base"),
      ),
    ),
    exterior_features=("pathfinder habitat ring", "artificial gravity wheel section"),
    tips=("Water at ring base acts as gravity sensor", "Over ten floors of crew rooms"),
  ),
  "epic_inventions_hydroponics": BookBuild(
    id="epic_inventions_hydroponics",
    name="Hydroponics Room",
    theme="sci_fi",
    biome="space",
    caption=(
      "a pathfinder space station hydroponics room blue water tanks kelp berries "
      "melons automatic farm crew food production white orange hull module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:orange_concrete",
      "minecraft:water",
      "minecraft:kelp",
      "minecraft:sweet_berry_bush",
      "minecraft:melon",
      "minecraft:gray_concrete",
    ),
    zones=(
      BuildZone(
        name="14 by 10 hydroponics bay",
        size=(14, 8, 10),
        materials=("white_concrete", "orange_concrete", "water", "kelp", "sweet_berry_bush", "melon"),
        features=("row of water grow tanks", "kelp berry melon crops", "lower deck farm bay"),
        interior=("hydroponic tanks", "automatic food production"),
      ),
    ),
    exterior_features=("pathfinder hydroponics bay", "space station farm deck"),
    tips=("Central farming for long voyages", "Kelp berries and melons in water tanks"),
  ),
  "epic_inventions_berry_farm": BookBuild(
    id="epic_inventions_berry_farm",
    name="Berry Farm",
    theme="sci_fi",
    biome="space",
    caption=(
      "a pathfinder space station sweet berry farm compact rectangular vitamin c "
      "scurvy prevention automatic food source white concrete farm module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:gray_concrete",
      "minecraft:sweet_berry_bush",
      "minecraft:dirt",
      "minecraft:oak_fence",
      "minecraft:water",
      "minecraft:sea_lantern",
    ),
    zones=(
      BuildZone(
        name="8 by 6 berry farm",
        size=(8, 6, 6),
        materials=("white_concrete", "sweet_berry_bush", "dirt", "oak_fence", "water"),
        features=("compact berry rows", "enclosed farm plot", "vitamin c crop"),
        interior=("sweet berry bushes",),
      ),
    ),
    exterior_features=("pathfinder berry farm", "space station vitamin crop"),
    tips=("Sweet berries prevent scurvy outbreaks", "Compact enclosed farm plot"),
  ),
  "epic_inventions_kelp_farm": BookBuild(
    id="epic_inventions_kelp_farm",
    name="Kelp Farm",
    theme="sci_fi",
    biome="space",
    caption=(
      "a pathfinder space station kelp farm vertical glass water column observer "
      "piston auto harvest fast growing fuel food source module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:glass",
      "minecraft:water",
      "minecraft:kelp",
      "minecraft:observer",
      "minecraft:piston",
      "minecraft:hopper",
    ),
    zones=(
      BuildZone(
        name="6 by 12 kelp tower",
        size=(6, 14, 6),
        materials=("white_concrete", "glass", "water", "kelp", "observer", "piston"),
        features=("vertical glass kelp column", "observer piston harvest", "collection hopper"),
        interior=("automated kelp harvester",),
      ),
    ),
    exterior_features=("pathfinder kelp farm", "vertical auto harvest tower"),
    tips=("Observer triggers piston when kelp grows", "Kelp floats to top for collection"),
  ),
  "epic_inventions_airlock": BookBuild(
    id="epic_inventions_airlock",
    name="Airlock",
    theme="sci_fi",
    biome="space",
    caption=(
      "a pathfinder space station airlock white chamber two sealed orange heavy "
      "doors vacuum seal crew spacewalk repair module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:orange_concrete",
      "minecraft:iron_door",
      "minecraft:iron_bars",
      "minecraft:gray_concrete",
      "minecraft:sea_lantern",
      "minecraft:stone_button",
    ),
    zones=(
      BuildZone(
        name="6 by 8 airlock chamber",
        size=(6, 8, 8),
        materials=("white_concrete", "orange_concrete", "iron_door", "iron_bars", "sea_lantern"),
        features=("double sealed gate airlock", "orange heavy doors", "vacuum transition chamber"),
        interior=("two door airlock sequence",),
      ),
    ),
    exterior_features=("pathfinder airlock", "spacewalk entry chamber"),
    tips=("Two sealed gates prevent vacuum breach", "Orange doors mark heavy seals"),
  ),
  "epic_inventions_melon_farm": BookBuild(
    id="epic_inventions_melon_farm",
    name="Melon Farm",
    theme="sci_fi",
    biome="space",
    caption=(
      "a pathfinder space station melon farm observer piston auto harvest minecart "
      "collection glistening melon healing potions horizontal farm module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:gray_concrete",
      "minecraft:melon",
      "minecraft:melon_stem",
      "minecraft:observer",
      "minecraft:piston",
      "minecraft:rail",
      "minecraft:hopper_minecart",
    ),
    zones=(
      BuildZone(
        name="12 by 8 melon farm",
        size=(12, 6, 8),
        materials=("white_concrete", "melon", "melon_stem", "observer", "piston", "rail"),
        features=("horizontal melon rows", "observer piston harvest", "minecart collection rail"),
        interior=("automated melon harvester",),
      ),
    ),
    exterior_features=("pathfinder melon farm", "auto harvest crop deck"),
    tips=("Observer and piston harvest melons automatically", "Minecart collects drops"),
  ),
  "epic_inventions_solar_array": BookBuild(
    id="epic_inventions_solar_array",
    name="Solar Array",
    theme="sci_fi",
    biome="space",
    caption=(
      "a pathfinder space station solar power array 88 gold panel panels white hull "
      "star energy primary power source engine fuel intergalactic module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:gold_block",
      "minecraft:gray_concrete",
      "minecraft:iron_bars",
      "minecraft:sea_lantern",
      "minecraft:orange_concrete",
      "minecraft:lightning_rod",
    ),
    zones=(
      BuildZone(
        name="20 by 8 solar wing",
        size=(20, 6, 8),
        materials=("white_concrete", "gold_block", "gray_concrete", "iron_bars", "lightning_rod"),
        features=("long solar panel wing", "88 gold block panels", "white support truss"),
        interior=(),
      ),
    ),
    exterior_features=("pathfinder solar wing", "primary station power array"),
    tips=("88 gold panels capture star power", "Primary engine and life support fuel"),
  ),
  "epic_inventions_aquarium": BookBuild(
    id="epic_inventions_aquarium",
    name="Aquarium",
    theme="bedroom",
    biome="indoor",
    caption=(
      "a meeple paradise bedroom aquarium glass tank kelp coral water fish "
      "decorations shelf display model build module"
    ),
    palette=(
      "minecraft:glass",
      "minecraft:water",
      "minecraft:kelp",
      "minecraft:brain_coral",
      "minecraft:tube_coral",
      "minecraft:gray_concrete",
      "minecraft:sand",
    ),
    zones=(
      BuildZone(
        name="12 by 6 aquarium",
        size=(12, 6, 6),
        materials=("glass", "water", "kelp", "brain_coral", "tube_coral", "gray_concrete"),
        features=("rectangular glass tank", "kelp and coral inside", "dark gray support base"),
        interior=("fish decorations", "underwater plants"),
      ),
    ),
    exterior_features=("meeple paradise shelf aquarium", "bedroom display tank"),
    tips=("Glass blocks form transparent tank walls", "Fill with kelp and coral for fish"),
  ),
  "epic_inventions_piggy_banks": BookBuild(
    id="epic_inventions_piggy_banks",
    name="Piggy Bank Collection",
    theme="bedroom",
    biome="indoor",
    caption=(
      "a meeple paradise piggy bank collection mob head row pig chicken sheep enderman "
      "skeleton fox zombie trapdoor coin bank shelf display module"
    ),
    palette=(
      "minecraft:pink_wool",
      "minecraft:yellow_wool",
      "minecraft:white_wool",
      "minecraft:black_wool",
      "minecraft:gray_wool",
      "minecraft:orange_wool",
      "minecraft:green_wool",
      "minecraft:oak_trapdoor",
    ),
    zones=(
      BuildZone(
        name="14 block piggy bank row",
        size=(14, 6, 4),
        materials=("pink_wool", "yellow_wool", "white_wool", "black_wool", "oak_trapdoor"),
        features=("seven mob head piggy banks", "trapdoor coin slots underneath", "shelf display row"),
        interior=(),
      ),
    ),
    exterior_features=("meeple paradise piggy bank shelf", "mob coin bank collection"),
    tips=("One bank per favorite mob", "Trapdoors underneath to empty coins"),
  ),
  "epic_inventions_creeper_toy": BookBuild(
    id="epic_inventions_creeper_toy",
    name="Creeper Toy",
    theme="bedroom",
    biome="indoor",
    caption=(
      "a meeple paradise cuddly creeper toy green gray wool pink bubblegum soft "
      "plush shelf display bedroom module"
    ),
    palette=(
      "minecraft:green_wool",
      "minecraft:gray_wool",
      "minecraft:lime_wool",
      "minecraft:pink_wool",
      "minecraft:black_wool",
    ),
    zones=(
      BuildZone(
        name="6 by 8 creeper plush",
        size=(6, 8, 4),
        materials=("green_wool", "gray_wool", "lime_wool", "pink_wool", "black_wool"),
        features=("blocky creeper plush shape", "pink wool bubblegum mouth", "soft wool construction"),
        interior=(),
      ),
    ),
    exterior_features=("meeple paradise creeper toy", "cuddly plush display"),
    tips=("Green and gray wool for creeper body", "Pink wool bubblegum detail"),
  ),
  "epic_inventions_laptop": BookBuild(
    id="epic_inventions_laptop",
    name="Laptop",
    theme="bedroom",
    biome="indoor",
    caption=(
      "a meeple paradise bedroom laptop gray base black screen curly brackets "
      "minecraft gaming desk model module"
    ),
    palette=(
      "minecraft:gray_concrete",
      "minecraft:black_concrete",
      "minecraft:white_concrete",
      "minecraft:iron_trapdoor",
      "minecraft:light_gray_concrete",
    ),
    zones=(
      BuildZone(
        name="6 by 4 laptop model",
        size=(6, 4, 5),
        materials=("gray_concrete", "black_concrete", "white_concrete", "iron_trapdoor"),
        features=("open laptop shape", "black screen with bracket symbols", "desk scale model"),
        interior=(),
      ),
    ),
    exterior_features=("meeple paradise desk laptop", "minecraft gaming laptop model"),
    tips=("Gray base with angled black screen", "White brackets on screen face"),
  ),
  "epic_inventions_bonsai": BookBuild(
    id="epic_inventions_bonsai",
    name="Bonsai",
    theme="bedroom",
    biome="indoor",
    caption=(
      "a meeple paradise acacia bonsai small trimmed tree orange wood green leaves "
      "dark pot shelf plant bedroom module"
    ),
    palette=(
      "minecraft:acacia_log",
      "minecraft:acacia_leaves",
      "minecraft:terracotta",
      "minecraft:flower_pot",
      "minecraft:oak_leaves",
      "minecraft:dark_oak_planks",
    ),
    zones=(
      BuildZone(
        name="4 by 6 bonsai",
        size=(4, 6, 4),
        materials=("acacia_log", "acacia_leaves", "terracotta", "flower_pot", "dark_oak_planks"),
        features=("miniature acacia tree", "trimmed bonsai shape", "dark pot base"),
        interior=(),
      ),
    ),
    exterior_features=("meeple paradise acacia bonsai", "shelf plant display"),
    tips=("Acacia log trunk with leaf canopy", "Keep tree small with careful trimming"),
  ),
  "epic_inventions_model_village": BookBuild(
    id="epic_inventions_model_village",
    name="Model Village",
    theme="bedroom",
    biome="indoor",
    caption=(
      "a meeple paradise model village diorama tiny houses brown roofs green trees "
      "bridge water grass under bed village module"
    ),
    palette=(
      "minecraft:oak_planks",
      "minecraft:spruce_planks",
      "minecraft:grass_block",
      "minecraft:oak_leaves",
      "minecraft:water",
      "minecraft:cobblestone",
      "minecraft:oak_fence",
    ),
    zones=(
      BuildZone(
        name="12 by 8 village diorama",
        size=(12, 6, 8),
        materials=("oak_planks", "spruce_planks", "grass_block", "oak_leaves", "water", "cobblestone"),
        features=("miniature village landscape", "small houses and bridge", "grass and tree terrain"),
        interior=("tiny villager houses",),
      ),
    ),
    exterior_features=("meeple paradise model village", "under bed diorama"),
    tips=("Small scale houses with spruce roofs", "Bridge over water on grass base"),
  ),
  "epic_inventions_calendar": BookBuild(
    id="epic_inventions_calendar",
    name="Calendar",
    theme="bedroom",
    biome="indoor",
    caption=(
      "a meeple paradise wall calendar white grid red marked birthday dates "
      "bedroom important dates display module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:red_concrete",
      "minecraft:black_concrete",
      "minecraft:gray_concrete",
      "minecraft:item_frame",
    ),
    zones=(
      BuildZone(
        name="6 by 10 wall calendar",
        size=(6, 10, 2),
        materials=("white_concrete", "red_concrete", "black_concrete", "gray_concrete"),
        features=("vertical calendar grid", "red marked birthday cell", "wall mounted display"),
        interior=(),
      ),
    ),
    exterior_features=("meeple paradise wall calendar", "birthday marked date grid"),
    tips=("White grid with red birthday highlight", "Mount vertically on bedroom wall"),
  ),
  "epic_inventions_saturn_v_rocket": BookBuild(
    id="epic_inventions_saturn_v_rocket",
    name="Saturn V Rocket",
    theme="bedroom",
    biome="indoor",
    caption=(
      "a meeple paradise saturn v rocket model white concrete orange bands iron bars "
      "cauldron jets lightning rod nose shelf display module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:orange_concrete",
      "minecraft:iron_bars",
      "minecraft:stone_button",
      "minecraft:cauldron",
      "minecraft:lightning_rod",
      "minecraft:gray_concrete",
    ),
    zones=(
      BuildZone(
        name="16 by 6 rocket model",
        size=(16, 6, 6),
        materials=("white_concrete", "orange_concrete", "iron_bars", "cauldron", "lightning_rod"),
        features=("horizontal rocket model", "orange band stages", "cauldron jet engines"),
        interior=(),
      ),
    ),
    exterior_features=("meeple paradise saturn v model", "moon rocket shelf display"),
    tips=("White body with orange stage bands", "Cauldrons for jets lightning rod nose"),
  ),
  "epic_inventions_poster_run": BookBuild(
    id="epic_inventions_poster_run",
    name="Poster Run",
    theme="bedroom",
    biome="indoor",
    caption=(
      "a meeple paradise poster run rainbow flag vertical shaft winding stairs "
      "wall climbing mini game bedroom module"
    ),
    palette=(
      "minecraft:blue_wool",
      "minecraft:green_wool",
      "minecraft:yellow_wool",
      "minecraft:red_wool",
      "minecraft:oak_stairs",
      "minecraft:light_blue_wool",
      "minecraft:white_wool",
    ),
    zones=(
      BuildZone(
        name="6 by 14 rainbow shaft",
        size=(6, 14, 6),
        materials=("blue_wool", "green_wool", "yellow_wool", "red_wool", "oak_stairs", "light_blue_wool"),
        features=("rainbow gradient vertical shaft", "winding oak stair climb", "poster wall mini game"),
        interior=("scaling stair run",),
      ),
    ),
    exterior_features=("meeple paradise poster run", "rainbow wall climb course"),
    tips=("Rainbow wool gradient on shaft walls", "Oak stairs wind upward inside"),
  ),
  "epic_inventions_drawer_maze": BookBuild(
    id="epic_inventions_drawer_maze",
    name="Drawer Maze",
    theme="bedroom",
    biome="indoor",
    caption=(
      "a meeple paradise drawer maze wooden dresser labyrinth oak planks staircase "
      "next level desk access bedroom module"
    ),
    palette=(
      "minecraft:dark_oak_planks",
      "minecraft:oak_planks",
      "minecraft:birch_planks",
      "minecraft:oak_stairs",
      "minecraft:oak_fence",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="12 by 8 drawer maze",
        size=(12, 6, 8),
        materials=("dark_oak_planks", "oak_planks", "birch_planks", "oak_stairs", "oak_fence"),
        features=("dresser drawer labyrinth", "wooden maze walls", "staircase to next drawer level"),
        interior=("maze passage", "exit stairs"),
      ),
    ),
    exterior_features=("meeple paradise drawer maze", "desk drawer labyrinth"),
    tips=("Each drawer is a separate maze level", "Stairs connect drawer levels to desk"),
  ),
  "epic_inventions_parkour_wall": BookBuild(
    id="epic_inventions_parkour_wall",
    name="Parkour Wall",
    theme="bedroom",
    biome="indoor",
    caption=(
      "a meeple paradise parkour wall bed side green surface platforms ladders bridges "
      "colored blocks indoor garden climb module"
    ),
    palette=(
      "minecraft:green_wool",
      "minecraft:lime_wool",
      "minecraft:oak_planks",
      "minecraft:ladder",
      "minecraft:yellow_wool",
      "minecraft:blue_wool",
      "minecraft:oak_fence",
    ),
    zones=(
      BuildZone(
        name="14 by 12 parkour wall",
        size=(14, 12, 8),
        materials=("green_wool", "lime_wool", "oak_planks", "ladder", "yellow_wool", "blue_wool"),
        features=("bed side parkour course", "platforms ladders bridges", "multi color block obstacles"),
        interior=("indoor garden climb path",),
      ),
    ),
    exterior_features=("meeple paradise parkour wall", "bed side climb challenge"),
    tips=("Hop skip jump up bed side", "Leads to indoor garden above"),
  ),
  "epic_inventions_bed_elevator": BookBuild(
    id="epic_inventions_bed_elevator",
    name="Bed Elevator",
    theme="bedroom",
    biome="indoor",
    caption=(
      "a meeple paradise vertical travel elevator tall oak tower redstone block piston "
      "lift quickest way onto bed bedroom module"
    ),
    palette=(
      "minecraft:oak_planks",
      "minecraft:birch_planks",
      "minecraft:piston",
      "minecraft:redstone_block",
      "minecraft:observer",
      "minecraft:slime_block",
      "minecraft:oak_fence",
    ),
    zones=(
      BuildZone(
        name="6 by 20 bed elevator",
        size=(6, 20, 6),
        materials=("oak_planks", "piston", "redstone_block", "observer", "slime_block"),
        features=("tall piston elevator shaft", "redstone block activation", "vertical bed access"),
        interior=("repeating piston lift mechanism",),
      ),
    ),
    exterior_features=("meeple paradise bed elevator", "vertical travel to bed"),
    tips=("Place redstone block at bottom to activate", "Pistons carry player to bed top"),
  ),
  "epic_inventions_lamp_station": BookBuild(
    id="epic_inventions_lamp_station",
    name="Lamp Station",
    theme="bedroom",
    biome="indoor",
    caption=(
      "a meeple paradise lamp station pig head minecart track nightstand pink lamp "
      "duvet transport journal monument indoor garden module"
    ),
    palette=(
      "minecraft:pink_wool",
      "minecraft:yellow_wool",
      "minecraft:oak_planks",
      "minecraft:rail",
      "minecraft:powered_rail",
      "minecraft:glowstone",
      "minecraft:white_wool",
    ),
    zones=(
      BuildZone(
        name="10 by 10 lamp station",
        size=(10, 10, 8),
        materials=("pink_wool", "yellow_wool", "oak_planks", "rail", "glowstone", "white_wool"),
        features=("pig head minecart station", "curved lamp neck glowstone head", "nightstand rail hub"),
        interior=("minecart duvet transport",),
      ),
    ),
    exterior_features=("meeple paradise lamp station", "pig minecart nightstand hub"),
    tips=("Minecart track enters pig mouth", "Rail transport across duvet to destinations"),
  ),
  "epic_inventions_bouncy_pillow": BookBuild(
    id="epic_inventions_bouncy_pillow",
    name="Bouncy Pillow",
    theme="bedroom",
    biome="indoor",
    caption=(
      "a meeple paradise bouncy pillow giant slime blocks blue yellow white green "
      "bed jump bounce chicken beak shelf launch module"
    ),
    palette=(
      "minecraft:slime_block",
      "minecraft:blue_wool",
      "minecraft:yellow_wool",
      "minecraft:white_wool",
      "minecraft:lime_wool",
      "minecraft:green_wool",
      "minecraft:light_blue_wool",
    ),
    zones=(
      BuildZone(
        name="14 by 4 bouncy pillow",
        size=(14, 4, 10),
        materials=("slime_block", "blue_wool", "yellow_wool", "white_wool", "lime_wool", "light_blue_wool"),
        features=("giant multi color pillow top", "slime block bounce surface", "bed launch pad"),
        interior=(),
      ),
    ),
    exterior_features=("meeple paradise bouncy pillow", "slime block bed bounce pad"),
    tips=("Jump from chicken beak shelf onto pillow", "Slime blocks bounce player high"),
  ),
  "epic_inventions_tnt_rocket": BookBuild(
    id="epic_inventions_tnt_rocket",
    name="TNT Rocket",
    theme="villain",
    biome="island",
    caption=(
      "a skull mountain tnt rocket escape vehicle black white grey stages circular "
      "stone shaft yellow black hazard stripes villain lair silo module"
    ),
    palette=(
      "minecraft:black_concrete",
      "minecraft:white_concrete",
      "minecraft:gray_concrete",
      "minecraft:tnt",
      "minecraft:stone",
      "minecraft:yellow_concrete",
      "minecraft:iron_block",
    ),
    zones=(
      BuildZone(
        name="10 by 16 rocket in shaft",
        size=(10, 16, 10),
        materials=("black_concrete", "white_concrete", "gray_concrete", "tnt", "stone", "yellow_concrete"),
        features=("multi stage rocket", "circular stone silo shaft", "hazard stripe launch platform"),
        interior=("tnt rocket stages", "escape vehicle"),
      ),
    ),
    exterior_features=("skull mountain tnt rocket", "villain escape silo rocket"),
    tips=("Rocket sits at bottom of circular stone shaft", "Yellow black hazard stripes on platform"),
  ),
  "epic_inventions_combat_training": BookBuild(
    id="epic_inventions_combat_training",
    name="Combat Training Room",
    theme="villain",
    biome="underground",
    caption=(
      "a skull mountain martial combat training room dark oak floor stone walls "
      "iron bar dividers armor stands chests troop training villain lair module"
    ),
    palette=(
      "minecraft:dark_oak_planks",
      "minecraft:stone",
      "minecraft:stone_bricks",
      "minecraft:iron_bars",
      "minecraft:armor_stand",
      "minecraft:chest",
      "minecraft:torch",
    ),
    zones=(
      BuildZone(
        name="12 by 8 training room",
        size=(12, 8, 8),
        materials=("dark_oak_planks", "stone", "iron_bars", "armor_stand", "chest"),
        features=("indoor training floor", "iron bar lane dividers", "armor stand rows"),
        interior=("armor stands", "weapon chests", "troop training ground"),
      ),
    ),
    exterior_features=("skull mountain combat gym", "villain troop training room"),
    tips=("Dark oak floor with stone walls", "Iron bars divide training lanes"),
  ),
  "epic_inventions_shooting_range": BookBuild(
    id="epic_inventions_shooting_range",
    name="Shooting Range",
    theme="villain",
    biome="underground",
    caption=(
      "a skull mountain shooting range four lanes white red circle targets iron bar "
      "partitions stone walls chest back wall bow crossbow practice module"
    ),
    palette=(
      "minecraft:stone",
      "minecraft:gray_concrete",
      "minecraft:white_concrete",
      "minecraft:red_concrete",
      "minecraft:iron_bars",
      "minecraft:chest",
      "minecraft:oak_planks",
    ),
    zones=(
      BuildZone(
        name="14 by 8 shooting range",
        size=(14, 8, 8),
        materials=("stone", "white_concrete", "red_concrete", "iron_bars", "chest"),
        features=("four shooting lanes", "red circle targets", "iron bar lane partitions"),
        interior=("target wall", "ammo chests"),
      ),
    ),
    exterior_features=("skull mountain shooting range", "villain archery practice lanes"),
    tips=("White blocks with red circle targets", "Iron bars between four lanes"),
  ),
  "epic_inventions_skull_silo": BookBuild(
    id="epic_inventions_skull_silo",
    name="Skull Silo",
    theme="villain",
    biome="island",
    caption=(
      "a skull mountain giant stone skull facade glowing orange eyes splits open "
      "tnt rocket silo hidden launch cover villain island module"
    ),
    palette=(
      "minecraft:stone",
      "minecraft:stone_bricks",
      "minecraft:gray_concrete",
      "minecraft:glowstone",
      "minecraft:orange_terracotta",
      "minecraft:smooth_quartz_slab",
      "minecraft:black_concrete",
    ),
    zones=(
      BuildZone(
        name="14 by 12 skull facade",
        size=(14, 12, 10),
        materials=("stone", "stone_bricks", "glowstone", "orange_terracotta", "smooth_quartz_slab"),
        features=("massive stone skull", "glowing orange eye sockets", "splits to reveal rocket silo"),
        interior=("hidden tnt rocket shaft",),
      ),
    ),
    exterior_features=("skull mountain skull silo", "villain rocket launch facade"),
    tips=("Skull splits in two for rocket launch", "Glowstone or fire for glowing eyes"),
  ),
  "epic_inventions_fire_pit": BookBuild(
    id="epic_inventions_fire_pit",
    name="Fire Pit Lounge",
    theme="villain",
    biome="underground",
    caption=(
      "a skull mountain fire pit lounge underground cozy room central campfire "
      "dark oak benches stone walls chest corners island resort distraction module"
    ),
    palette=(
      "minecraft:stone",
      "minecraft:stone_bricks",
      "minecraft:dark_oak_planks",
      "minecraft:campfire",
      "minecraft:chest",
      "minecraft:torch",
      "minecraft:sand",
    ),
    zones=(
      BuildZone(
        name="10 by 8 fire pit room",
        size=(10, 8, 8),
        materials=("stone", "dark_oak_planks", "campfire", "chest", "torch"),
        features=("central fire pit", "four dark oak benches", "cozy underground lounge"),
        interior=("campfire seating", "corner chests"),
      ),
    ),
    exterior_features=("skull mountain fire pit", "resort guest lounge distraction"),
    tips=("Campfire center with bench ring", "Resort cover for secret lair below"),
  ),
  "epic_inventions_villain_docks": BookBuild(
    id="epic_inventions_villain_docks",
    name="Villain Docks",
    theme="villain",
    biome="island",
    caption=(
      "a skull mountain covered docks white roof stone pillars yellow boats water "
      "slips only island entry prevent aerial detection villain module"
    ),
    palette=(
      "minecraft:white_concrete",
      "minecraft:stone",
      "minecraft:sand",
      "minecraft:water",
      "minecraft:oak_boat",
      "minecraft:smooth_quartz_slab",
      "minecraft:oak_fence",
    ),
    zones=(
      BuildZone(
        name="18 by 8 covered docks",
        size=(18, 8, 8),
        materials=("white_concrete", "stone", "sand", "water", "oak_boat", "smooth_quartz_slab"),
        features=("covered dock structure", "stone pillar supports", "yellow boat slips over water"),
        interior=("boat docking slips",),
      ),
    ),
    exterior_features=("skull mountain covered docks", "island water entry point"),
    tips=("Only entry to island by water", "White roof hides activity from above"),
  ),
  "epic_inventions_hidden_door": BookBuild(
    id="epic_inventions_hidden_door",
    name="Hidden Door",
    theme="villain",
    biome="underground",
    caption=(
      "a skull mountain hidden door bookshelf wall lectern comparator redstone iron "
      "door secret lair entrance book activation villain module"
    ),
    palette=(
      "minecraft:bookshelf",
      "minecraft:lectern",
      "minecraft:comparator",
      "minecraft:redstone_dust",
      "minecraft:iron_door",
      "minecraft:stone_bricks",
      "minecraft:oak_planks",
    ),
    zones=(
      BuildZone(
        name="8 by 8 hidden entrance",
        size=(8, 8, 6),
        materials=("bookshelf", "lectern", "comparator", "redstone_dust", "iron_door"),
        features=("bookshelf disguised wall", "lectern book trigger", "comparator iron door circuit"),
        interior=("hidden iron door passage", "redstone behind shelves"),
      ),
    ),
    exterior_features=("skull mountain secret entrance", "lectern activated hidden door"),
    tips=("Place book on lectern to open door", "Comparator sends signal to hidden iron door"),
  ),
  "epic_inventions_creeper_farm": BookBuild(
    id="epic_inventions_creeper_farm",
    name="Creeper Farm",
    theme="villain",
    biome="underground",
    caption=(
      "a skull mountain creeper farm butterfly spawning chamber lava water kill "
      "channel hopper chest gunpowder collection dark oak trapdoor roof module"
    ),
    palette=(
      "minecraft:gray_concrete",
      "minecraft:white_concrete",
      "minecraft:iron_block",
      "minecraft:glass",
      "minecraft:lava",
      "minecraft:water",
      "minecraft:hopper",
      "minecraft:chest",
      "minecraft:dark_oak_trapdoor",
      "minecraft:orange_carpet",
    ),
    zones=(
      BuildZone(
        name="25 by 28 creeper farm scaled",
        size=(16, 14, 12),
        materials=("gray_concrete", "iron_block", "glass", "lava", "water", "hopper", "chest"),
        features=("butterfly spawn chamber", "lava water kill channel", "hopper chest collection"),
        interior=("dual layer butterfly platform", "trapdoor spawn ceiling"),
      ),
    ),
    exterior_features=("skull mountain creeper farm", "automatic gunpowder collector"),
    tips=("25 by 28 base with butterfly spawn layers", "Water pushes creepers into lava channel"),
  ),
  "epic_inventions_soul_campfires": BookBuild(
    id="epic_inventions_soul_campfires",
    name="Soul Campfire Alcoves",
    theme="game_show",
    biome="plains",
    caption=(
      "a diamond maze soul campfire alcoves yellow sandstone emerald blue soul fire "
      "night visibility luxury game show exterior module"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:gold_block",
      "minecraft:emerald_block",
      "minecraft:soul_campfire",
      "minecraft:blue_stained_glass",
      "minecraft:smooth_sandstone",
    ),
    zones=(
      BuildZone(
        name="8 by 8 campfire alcoves",
        size=(8, 8, 6),
        materials=("sandstone", "gold_block", "emerald_block", "soul_campfire", "blue_stained_glass"),
        features=("soul campfire alcove niches", "gold emerald trim", "visible from distance at night"),
        interior=(),
      ),
    ),
    exterior_features=("diamond maze soul campfires", "game show night beacon"),
    tips=("Soul campfires in alcoves for blue glow", "Gold and emerald luxury trim"),
  ),
  "epic_inventions_exterior_bling": BookBuild(
    id="epic_inventions_exterior_bling",
    name="Exterior Bling Ring",
    theme="game_show",
    biome="plains",
    caption=(
      "a diamond maze exterior bling circular emerald diamond ring blue glass white "
      "border glowing green center luxury game show facade module"
    ),
    palette=(
      "minecraft:emerald_block",
      "minecraft:diamond_block",
      "minecraft:blue_stained_glass",
      "minecraft:quartz_block",
      "minecraft:gold_block",
      "minecraft:sea_lantern",
    ),
    zones=(
      BuildZone(
        name="10 block diameter bling ring",
        size=(10, 4, 10),
        materials=("emerald_block", "diamond_block", "blue_stained_glass", "quartz_block", "gold_block"),
        features=("circular emerald diamond ring", "glowing green center", "blue glass white border"),
        interior=(),
      ),
    ),
    exterior_features=("diamond maze exterior ring", "game show luxury bling"),
    tips=("One ring at each end of building", "Emerald center with diamond border"),
  ),
  "epic_inventions_entrance_hall": BookBuild(
    id="epic_inventions_entrance_hall",
    name="Entrance Hall",
    theme="game_show",
    biome="plains",
    caption=(
      "a diamond maze entrance hall vaulted ceiling sandstone emerald pillars blue "
      "white floor pattern contestant gathering game show lobby module"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:smooth_sandstone",
      "minecraft:emerald_block",
      "minecraft:blue_stained_glass",
      "minecraft:quartz_block",
      "minecraft:gold_block",
      "minecraft:sea_lantern",
    ),
    zones=(
      BuildZone(
        name="14 by 10 entrance hall",
        size=(14, 12, 10),
        materials=("sandstone", "emerald_block", "blue_stained_glass", "quartz_block", "gold_block"),
        features=("vaulted ornate entrance hall", "emerald sandstone pillars", "blue white floor pattern"),
        interior=("contestant gathering lobby", "sea lantern lighting"),
      ),
    ),
    exterior_features=("diamond maze entrance hall", "game show contestant lobby"),
    tips=("Contestants gather before game starts", "Intricate blue and white floor tiles"),
  ),
  "epic_inventions_level_end": BookBuild(
    id="epic_inventions_level_end",
    name="Level End Rewards",
    theme="game_show",
    biome="plains",
    caption=(
      "a diamond maze level end rewards room white spiral staircase dispensers "
      "redstone torch prizes puzzle completion game show module"
    ),
    palette=(
      "minecraft:quartz_block",
      "minecraft:quartz_stairs",
      "minecraft:dispenser",
      "minecraft:redstone_torch",
      "minecraft:sandstone",
      "minecraft:emerald_block",
      "minecraft:chest",
    ),
    zones=(
      BuildZone(
        name="8 by 10 level end room",
        size=(8, 10, 8),
        materials=("quartz_block", "quartz_stairs", "dispenser", "redstone_torch", "sandstone"),
        features=("white spiral staircase", "dispenser reward wall", "redstone torch prizes"),
        interior=("puzzle completion rewards", "torch collection point"),
      ),
    ),
    exterior_features=("diamond maze level end", "game show reward room"),
    tips=("Completing rooms activates dispensers", "Collect redstone torches for prizes"),
  ),
  "epic_inventions_ascension_tower": BookBuild(
    id="epic_inventions_ascension_tower",
    name="Ascension Tower",
    theme="game_show",
    biome="plains",
    caption=(
      "a diamond maze ascension tower slender sandstone blue glass windows emerald "
      "accents maze route exit deeper rewards game show module"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:smooth_sandstone",
      "minecraft:blue_stained_glass",
      "minecraft:emerald_block",
      "minecraft:gold_block",
      "minecraft:quartz_stairs",
    ),
    zones=(
      BuildZone(
        name="6 by 18 ascension tower",
        size=(6, 18, 6),
        materials=("sandstone", "blue_stained_glass", "emerald_block", "gold_block", "quartz_stairs"),
        features=("tall slender tower", "vertical blue glass windows", "emerald gold accents"),
        interior=("maze vertical route", "stair ascent path"),
      ),
    ),
    exterior_features=("diamond maze ascension tower", "game show maze spire"),
    tips=("Four towers provide maze routes", "Leads to exit or deeper rewards"),
  ),
  "epic_inventions_diamond_statue": BookBuild(
    id="epic_inventions_diamond_statue",
    name="Diamond Statue",
    theme="game_show",
    biome="plains",
    caption=(
      "a diamond maze red sandstone humanoid statue glowing blue diamond outstretched "
      "hand entices players game show host monument module"
    ),
    palette=(
      "minecraft:red_sandstone",
      "minecraft:smooth_red_sandstone",
      "minecraft:diamond_block",
      "minecraft:gold_block",
      "minecraft:sea_lantern",
      "minecraft:quartz_block",
    ),
    zones=(
      BuildZone(
        name="8 by 14 diamond statue",
        size=(8, 14, 6),
        materials=("red_sandstone", "smooth_red_sandstone", "diamond_block", "gold_block", "sea_lantern"),
        features=("large humanoid statue", "outstretched hand with diamond", "entices players to join"),
        interior=(),
      ),
    ),
    exterior_features=("diamond maze host statue", "game show entrance monument"),
    tips=("Statue stands outside maze", "Glowing diamond block in outstretched hand"),
  ),
  "epic_inventions_elytra_launcher": BookBuild(
    id="epic_inventions_elytra_launcher",
    name="Elytra Launcher",
    theme="game_show",
    biome="plains",
    caption=(
      "a diamond maze elytra launcher end portal frame eye of ender slime block "
      "piston redstone repeater fireworks exit game show module"
    ),
    palette=(
      "minecraft:end_portal_frame",
      "minecraft:ender_eye",
      "minecraft:slime_block",
      "minecraft:piston",
      "minecraft:redstone_repeater",
      "minecraft:redstone_dust",
      "minecraft:obsidian",
    ),
    zones=(
      BuildZone(
        name="10 by 8 elytra launcher",
        size=(10, 8, 8),
        materials=("end_portal_frame", "ender_eye", "slime_block", "piston", "redstone_repeater"),
        features=("exploded view launch platform", "slime piston mechanism", "firework exit launch"),
        interior=("redstone repeater launch circuit",),
      ),
    ),
    exterior_features=("diamond maze elytra launcher", "game show victory exit"),
    tips=("Exit maze in style with fireworks", "Slime blocks launched by pistons"),
  ),
  "epic_inventions_riddle_clue": BookBuild(
    id="epic_inventions_riddle_clue",
    name="Riddle Clue Pillars",
    theme="game_show",
    biome="plains",
    caption=(
      "a diamond maze riddle clue pillars wood fence gate count sea lantern tops "
      "lever puzzle hint game show module"
    ),
    palette=(
      "minecraft:oak_log",
      "minecraft:dark_oak_fence_gate",
      "minecraft:sea_lantern",
      "minecraft:sandstone",
      "minecraft:lever",
      "minecraft:gold_block",
    ),
    zones=(
      BuildZone(
        name="10 by 10 riddle pillars",
        size=(10, 10, 6),
        materials=("oak_log", "dark_oak_fence_gate", "sea_lantern", "sandstone", "lever"),
        features=("three tall pillars", "varying fence gate counts", "lever puzzle visual clue"),
        interior=(),
      ),
    ),
    exterior_features=("diamond maze riddle clue", "game show puzzle hint pillars"),
    tips=("Fence count on each pillar is the clue", "Shows how many levers to pull"),
  ),
  "epic_inventions_lever_puzzle": BookBuild(
    id="epic_inventions_lever_puzzle",
    name="Lever Puzzle",
    theme="game_show",
    biome="plains",
    caption=(
      "a diamond maze lever puzzle six levers sandstone wall redstone torches "
      "repeaters hidden chest correct order game show module"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:lever",
      "minecraft:redstone_torch",
      "minecraft:redstone_repeater",
      "minecraft:redstone_dust",
      "minecraft:chest",
      "minecraft:iron_door",
    ),
    zones=(
      BuildZone(
        name="10 by 8 lever puzzle",
        size=(10, 8, 6),
        materials=("sandstone", "lever", "redstone_torch", "redstone_repeater", "chest"),
        features=("six lever sandstone wall", "redstone logic behind wall", "hidden chest reward"),
        interior=("lever sequence circuit", "door unlock mechanism"),
      ),
    ),
    exterior_features=("diamond maze lever puzzle", "game show sequence room"),
    tips=("Toggle six levers in correct order", "Opens door to hidden chest"),
  ),
  "epic_inventions_time_lock": BookBuild(
    id="epic_inventions_time_lock",
    name="Time Lock",
    theme="game_show",
    biome="plains",
    caption=(
      "a diamond maze time lock hopper comparator repeater sticky piston timer "
      "adjustable circuit puzzle countdown game show module"
    ),
    palette=(
      "minecraft:stone_bricks",
      "minecraft:hopper",
      "minecraft:comparator",
      "minecraft:redstone_repeater",
      "minecraft:sticky_piston",
      "minecraft:redstone_torch",
      "minecraft:lever",
    ),
    zones=(
      BuildZone(
        name="14 by 6 time lock circuit",
        size=(14, 6, 8),
        materials=("stone_bricks", "hopper", "comparator", "redstone_repeater", "sticky_piston", "lever"),
        features=("hopper comparator timer", "adjustable repeater delay", "locks when hopper full"),
        interior=("linear redstone clock circuit",),
      ),
    ),
    exterior_features=("diamond maze time lock", "game show countdown timer"),
    tips=("Hopper fills to trigger lock", "Move repeater to adjust time length"),
  ),
  "epic_inventions_reward_dispenser": BookBuild(
    id="epic_inventions_reward_dispenser",
    name="Reward Dispenser",
    theme="game_show",
    biome="plains",
    caption=(
      "a diamond maze reward dispenser shrine sandstone cyan redstone torch slot "
      "activates dispenser prize puzzle completion game show module"
    ),
    palette=(
      "minecraft:sandstone",
      "minecraft:cyan_terracotta",
      "minecraft:dispenser",
      "minecraft:redstone_torch",
      "minecraft:gold_block",
      "minecraft:emerald_block",
      "minecraft:quartz_block",
    ),
    zones=(
      BuildZone(
        name="6 by 8 reward shrine",
        size=(6, 8, 6),
        materials=("sandstone", "cyan_terracotta", "dispenser", "redstone_torch", "gold_block"),
        features=("reward shrine structure", "redstone torch activation slot", "dispenser prize shoot"),
        interior=("torch triggered dispenser",),
      ),
    ),
    exterior_features=("diamond maze reward shrine", "game show prize dispenser"),
    tips=("Place redstone torch in shrine slot", "Dispenser shoots reward upward"),
  ),
}

# Mega builds saved for 100³–150³ — not registered yet (150³ = full chapters):
# - epic_inventions_animal_sanctuary (full forcefield complex)
# - epic_inventions_research_center
# - epic_inventions_science_tower
# - epic_inventions_monster_factory (full gothic castle complex)
# - epic_inventions_spiky_tower (full 50+ block spire)
# - epic_inventions_grand_entrance
# - epic_inventions_infernal_entrance
# - epic_inventions_kawaii_starting_line (48+ wide race start)
# - epic_inventions_kawaii_waterways (full racecourse)
# - epic_inventions_island_splitter (50+ long fork course)
# - epic_inventions_power_generator (full epic cylindrical reactor)
# - epic_inventions_paranormal_facility (full nether lab complex)
# - epic_inventions_eight_legged_saloon (full walking saloon on 8 legs, 38+ blocks high)
# - epic_inventions_temple_of_wonders (full banyan jungle temple complex)
# - epic_inventions_meeting_circle (massive banyan tree meeting ring)
# - epic_inventions_pathfinder (full solar-powered intergalactic space station)
# - epic_inventions_meeple_paradise (full giant bedroom world)
# - epic_inventions_skull_mountain (full island villain lair and resort)
# - epic_inventions_diamond_maze (full luxury game show maze complex)
