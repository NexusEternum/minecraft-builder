"""
Furniture hacks from the Minecraft Guide to Creative.

Block-combination recipes for interior detail. Enriches prompts;
actual placement requires interior training data or a future furniture layer.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FurnitureHack:
  id: str
  name: str
  aliases: tuple[str, ...]
  blocks: tuple[str, ...]
  room: str
  tip: str


def _b(name: str) -> str:
  if name.startswith("minecraft:"):
    return name
  return f"minecraft:{name}"


FURNITURE_HACKS: tuple[FurnitureHack, ...] = (
  # Seating
  FurnitureHack("chair", "armchair", ("chair", "armchair", "seating"), (_b("oak_stairs"), _b("oak_sign")), "living room", "Stair with signs on sides as armrests"),
  FurnitureHack("sofa", "sofa", ("sofa", "couch", "settee"), (_b("acacia_stairs"), _b("acacia_sign")), "living room", "Row of stairs with sign armrests at each end"),
  # Tables
  FurnitureHack("small_table", "piston table", ("small table", "side table"), (_b("piston"), _b("redstone_torch")), "living room", "Redstone torch under extended piston as table"),
  FurnitureHack("dining_table", "dining table", ("dining table", "formal table", "dinner table"), (_b("oak_slab"), _b("red_carpet"), _b("light_weighted_pressure_plate")), "dining room", "Long slab table with carpet runner and gold plates as settings"),
  FurnitureHack("family_table", "carpet table", ("family table", "kitchen table"), (_b("oak_fence"), _b("blue_carpet")), "kitchen", "Fence legs with carpet tabletop"),
  FurnitureHack("ping_pong", "ping pong table", ("ping pong", "table tennis"), (_b("green_carpet"), _b("oak_fence"), _b("glass_pane")), "game room", "Green carpet on fences with glass pane net"),
  FurnitureHack("pool_table", "pool table", ("pool table", "billiards"), (_b("green_wool"), _b("oak_trapdoor"), _b("snowball")), "game room", "Green wool with trapdoor rails and snowballs as balls"),
  # Bedroom
  FurnitureHack("bunk_bed", "bunk bed", ("bunk bed", "bunkbed"), (_b("red_bed"), _b("oak_slab"), _b("ladder")), "bedroom", "Two beds stacked with slabs and ladder"),
  FurnitureHack("four_poster", "four poster bed", ("four poster", "four-poster", "canopy bed"), (_b("red_bed"), _b("oak_fence"), _b("black_carpet")), "bedroom", "Bed with fence posts and trapdoor/carpet canopy"),
  FurnitureHack("wardrobe", "wardrobe", ("wardrobe", "closet"), (_b("oak_door"), _b("oak_fence")), "bedroom", "Double doors with fence posts inside as hanging space"),
  # Kitchen
  FurnitureHack("fridge", "fridge", ("fridge", "refrigerator"), (_b("dispenser"), _b("iron_block"), _b("iron_door")), "kitchen", "Dispenser + iron block + iron door with button"),
  FurnitureHack("stove", "stove", ("stove", "oven", "hob"), (_b("furnace"), _b("iron_trapdoor")), "kitchen", "Furnace with iron trapdoor on top as hob"),
  FurnitureHack("shelves", "wall shelves", ("shelf", "shelves", "bookshelf wall"), (_b("oak_slab"), _b("oak_stairs")), "any", "Slabs on wall with upside-down stairs as brackets"),
  # Bathroom
  FurnitureHack("toilet", "toilet", ("toilet", "wc"), (_b("quartz_slab"), _b("quartz_block"), _b("stone_pressure_plate")), "bathroom", "Quartz slab on block, pressure plate seat, button flush"),
  FurnitureHack("sink", "sink", ("sink", "basin"), (_b("hopper"), _b("quartz_slab"), _b("lever")), "bathroom", "Hopper in quartz counter with lever tap"),
  FurnitureHack("bath", "bathtub", ("bath", "bathtub", "tub"), (_b("quartz_stairs"), _b("dark_prismarine"), _b("lever")), "bathroom", "Quartz stairs tub with prismarine base"),
  FurnitureHack("mirror", "mirror", ("mirror"), (_b("packed_ice"), _b("quartz_block")), "bathroom", "Packed ice recessed in wall above sink"),
  # Living / entertainment
  FurnitureHack("fireplace", "fireplace", ("fireplace", "hearth"), (_b("cobblestone"), _b("netherrack"), _b("iron_bars")), "living room", "Cobblestone surround with netherrack fire behind iron bars"),
  FurnitureHack("tv", "television", ("tv", "television"), (_b("black_wool"), _b("painting"), _b("jukebox")), "living room", "Black wool with painting screen and jukebox speakers"),
  FurnitureHack("computer", "computer desk", ("computer", "desk", "office"), (_b("oak_stairs"), _b("painting"), _b("stone_pressure_plate")), "office", "Stair desk with painting monitor and pressure plate keyboard"),
  FurnitureHack("grand_piano", "grand piano", ("piano", "grand piano"), (_b("dark_oak_slab"), _b("spruce_fence"), _b("rail")), "living room", "Dark oak slabs, fence legs, rails as keys"),
  FurnitureHack("grandfather_clock", "grandfather clock", ("grandfather clock", "clock"), (_b("oak_planks"), _b("oak_trapdoor"), _b("item_frame")), "hallway", "Wood column with trapdoors and clock in item frame"),
  FurnitureHack("dj_deck", "dj decks", ("dj", "dj deck", "sound system"), (_b("note_block"), _b("stone_pressure_plate"), _b("redstone_lamp")), "party", "Note blocks, pressure plates, lever-activated lamp"),
  FurnitureHack("barbecue", "barbecue", ("barbecue", "bbq", "grill"), (_b("bricks"), _b("netherrack"), _b("iron_trapdoor")), "outdoor", "Brick base with netherrack fire and iron trapdoor grill"),
  FurnitureHack("window_box", "window box", ("window box", "flower box"), (_b("dirt"), _b("oak_trapdoor"), _b("poppy")), "any", "Dirt on window ledge with trapdoors and flowers"),
)


def detect_furniture(prompt: str) -> list[FurnitureHack]:
  lower = prompt.lower()
  matched: list[tuple[int, FurnitureHack]] = []
  seen: set[str] = set()
  for hack in FURNITURE_HACKS:
    for alias in sorted(hack.aliases, key=len, reverse=True):
      if alias in lower and hack.id not in seen:
        matched.append((len(alias), hack))
        seen.add(hack.id)
        break

  # Broad interior triggers → a few defaults
  if not matched and any(w in lower for w in ("furnished", "interior", "inside", "living room", "bedroom", "kitchen", "bathroom")):
    room_defaults = {
      "living room": ["chair", "sofa", "fireplace"],
      "bedroom": ["four_poster", "wardrobe"],
      "kitchen": ["fridge", "stove", "family_table"],
      "bathroom": ["toilet", "sink", "bath"],
      "office": ["computer", "shelves"],
    }
    for room, ids in room_defaults.items():
      if room in lower:
        return [h for h in FURNITURE_HACKS if h.id in ids]

  matched.sort(key=lambda x: x[0], reverse=True)
  return [h for _, h in matched]


def furniture_keywords(hack: FurnitureHack) -> list[str]:
  blocks = [b.removeprefix("minecraft:").replace("_", " ") for b in hack.blocks[:2]]
  return [hack.name, *blocks]
