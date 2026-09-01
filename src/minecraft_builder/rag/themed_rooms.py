"""
Themed interior rooms from Utility Blocks (Minecraft Guide to Creative).

Each room type maps to functional blocks that match its aesthetic.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ThemedRoom:
  id: str
  name: str
  aliases: tuple[str, ...]
  wall_blocks: tuple[str, ...]
  utility_blocks: tuple[str, ...]
  tip: str


def _b(name: str) -> str:
  if name.startswith("minecraft:"):
    return name
  return f"minecraft:{name}"


THEMED_ROOMS: dict[str, ThemedRoom] = {
  "rustic_workshop": ThemedRoom(
    id="rustic_workshop",
    name="rustic workshop",
    aliases=("workshop", "smithy", "forge", "blacksmith", "rustic interior", "craft room"),
    wall_blocks=(_b("dark_oak_planks"), _b("cobblestone"), _b("stone_bricks")),
    utility_blocks=(
      _b("chest"),
      _b("anvil"),
      _b("furnace"),
      _b("crafting_table"),
      _b("torch"),
    ),
    tip="Raw furnace and anvil with wood crafting table and chest in wood/stone room",
  ),
  "mystic_lair": ThemedRoom(
    id="mystic_lair",
    name="mystic lair",
    aliases=("mystic", "lair", "enchanting room", "wizard", "magic room", "underground lair", "hideout"),
    wall_blocks=(_b("nether_bricks"), _b("stone_bricks"), _b("bookshelf")),
    utility_blocks=(
      _b("bookshelf"),
      _b("enchanting_table"),
      _b("brewing_stand"),
      _b("ender_chest"),
      _b("cauldron"),
    ),
    tip="Bookshelves ring an enchantment table with brewing stand, ender chest, cauldron",
  ),
  "modern_den": ThemedRoom(
    id="modern_den",
    name="modern den",
    aliases=("modern interior", "modern den", "minimalist", "apartment", "living room", "loft"),
    wall_blocks=(_b("white_concrete"), _b("light_gray_concrete"), _b("birch_planks")),
    utility_blocks=(
      _b("jukebox"),
      _b("shulker_box"),
      _b("white_bed"),
      _b("armor_stand"),
    ),
    tip="Jukebox, dyed shulker boxes, bed, and armor stands in a minimalist space",
  ),
}


def detect_room(prompt: str) -> ThemedRoom | None:
  lower = prompt.lower()
  matches: list[tuple[int, ThemedRoom]] = []
  for room in THEMED_ROOMS.values():
    for alias in room.aliases:
      if alias in lower:
        matches.append((len(alias), room))
        break
  if not matches:
    return None
  matches.sort(key=lambda x: x[0], reverse=True)
  return matches[0][1]


def room_keywords(room: ThemedRoom) -> list[str]:
  kws = [room.name]
  for block in room.utility_blocks[:4]:
    kws.append(block.removeprefix("minecraft:").replace("_", " "))
  return kws
