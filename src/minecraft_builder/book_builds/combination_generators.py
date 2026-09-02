"""Procedural generators for Bite-Sized Builds combination challenges."""

from __future__ import annotations

import numpy as np

from ..data.palette import AIR
from .bite_sized_generators import _b, _set, generate_bite_sized
from .compose import overlay_voxels, stamp_voxels


def generate_combination(combo_id: str) -> np.ndarray:
  fn = _COMBINATION_GENERATORS.get(combo_id)
  if fn is None:
    raise KeyError(f"Unknown combination build: {combo_id}")
  return fn()


def _generate_combo_submarine_airlock() -> np.ndarray:
  """Book combo: deep-sea submarine with underside underwater airlock."""
  sub = generate_bite_sized("bite_deep_sea_submarine")
  lock = generate_bite_sized("bite_underwater_airlock")
  # Airlock mounts under the hull belly (book page 91)
  return stamp_voxels(sub, lock, 0, 0, 0)


def _generate_combo_maze_creeper() -> np.ndarray:
  """Challenge 1: Halloween maze with creeper centerpiece."""
  maze = generate_bite_sized("bite_halloween_maze")
  creeper = generate_bite_sized("bite_creeper")
  return overlay_voxels(maze, creeper)


def _generate_combo_fountain_aviary() -> np.ndarray:
  """Challenge 2: Dolphin fountain merged into aviary pyramid courtyard."""
  aviary = generate_bite_sized("bite_aviary_pyramid")
  fountain = generate_bite_sized("bite_dolphin_fountain")
  # Fountain basin sits in the aviary interior (book merge illustration)
  return stamp_voxels(aviary, fountain, -2, 0, 1)


def _generate_combo_train_collector() -> np.ndarray:
  """Challenge 3: Train station with cart collector on the rail line."""
  station = generate_bite_sized("bite_train_station")
  collector = generate_bite_sized("bite_cart_collector")
  return stamp_voxels(station, collector, 0, 0, 8)


def _generate_combo_bunker_destroyer() -> np.ndarray:
  """Challenge 4: Hidden bunker with built-in item destroyer alcove."""
  bunker = generate_bite_sized("bite_hidden_bunker")
  destroyer = generate_bite_sized("bite_item_destroyer")
  return stamp_voxels(bunker, destroyer, 10, 0, 2)


def _generate_combo_vault_alarm() -> np.ndarray:
  """Challenge 5: Combination lock vault with alarm system at the entrance."""
  vault = generate_bite_sized("bite_combination_lock")
  alarm = generate_bite_sized("bite_alarm_system")
  return stamp_voxels(vault, alarm, 4, 0, -4)


def _pirate_watchtower_patch() -> np.ndarray:
  """Small cliff-top lookout tower for skull cove combo (book page 90)."""
  OLOG = _b("oak_log")
  OFENCE = _b("oak_fence")
  OPLANK = _b("oak_planks")
  VINE = _b("vine")
  GLASS = _b("glass_pane")
  LANTERN = _b("lantern")
  AIR_B = AIR

  res = 32
  v = np.full((res, res, res), AIR_B, dtype=object)
  ox, oz, oy = 0, 0, 0
  tw, td, th = 5, 5, 12

  for x in range(ox, ox + tw):
    for z in range(oz, oz + td):
      _set(v, x, oy, z, OPLANK)

  for y in range(oy + 1, oy + th):
    for x in range(ox, ox + tw):
      for z in range(oz, oz + td):
        corner = x in (ox, ox + tw - 1) and z in (oz, oz + td - 1)
        edge = x in (ox, ox + tw - 1) or z in (oz, oz + td - 1)
        if corner:
          _set(v, x, y, z, OLOG)
        elif edge:
          _set(v, x, y, z, OFENCE if y % 2 == 0 else OPLANK)
        else:
          _set(v, x, y, z, AIR_B)

  cabin_y = oy + 8
  for x in range(ox + 1, ox + tw - 1):
    for z in range(oz + 1, oz + td - 1):
      _set(v, x, cabin_y, z, OPLANK)
  for x in range(ox, ox + tw):
    for z in range(oz, oz + td):
      _set(v, x, cabin_y + 3, z, OPLANK)
  for x in (ox + 1, ox + tw - 2):
    for y in range(cabin_y + 1, cabin_y + 3):
      _set(v, x, y, oz, GLASS)

  for y in range(oy + 2, oy + th - 2, 3):
    for x in (ox, ox + tw - 1):
      for z in (oz + 1, oz + td - 2):
        _set(v, x, y, z, OFENCE)
        _set(v, x, y + 1, z, VINE)

  _set(v, ox + 2, cabin_y + 2, oz + 2, LANTERN)
  return v


def _generate_combo_greenhouse_wishing_well() -> np.ndarray:
  """Challenge 1 (page 90): greenhouse garden with wishing well."""
  greenhouse = generate_bite_sized("bite_greenhouse")
  well = generate_bite_sized("bite_wishing_well")
  return stamp_voxels(greenhouse, well, -5, 4, 11)


def _generate_combo_watchtower_skull_cove() -> np.ndarray:
  """Challenge 2 (page 90): pirate watchtower above skull cove."""
  cove = generate_bite_sized("bite_skull_cove")
  tower = _pirate_watchtower_patch()
  return stamp_voxels(cove, tower, 18, 12, 10)


def _generate_combo_bus_racetrack() -> np.ndarray:
  """Challenge 3 (page 90): monster-truck bus on horse racecourse."""
  track = generate_bite_sized("bite_horse_racecourse")
  bus = generate_bite_sized("bite_monster_truck_bus")
  return stamp_voxels(track, bus, 3, 0, 4)


def _generate_combo_steamboat_island() -> np.ndarray:
  """Challenge 4 (page 90): steamboat sailing toward secret island base."""
  boat = generate_bite_sized("bite_steamboat")
  island = generate_bite_sized("bite_secret_island_base")
  merged = stamp_voxels(boat, island, 6, -3, 10)
  return merged


def _generate_combo_pagoda_hot_spring() -> np.ndarray:
  """Challenge 5 (page 90): pagoda beside hot-spring bath."""
  spring = generate_bite_sized("bite_hot_spring")
  pagoda = generate_bite_sized("bite_pagoda")
  return stamp_voxels(spring, pagoda, -5, -2, -3)


def _generate_combo_beanstalk_shoe() -> np.ndarray:
  """Challenge 1 (page 92): beanstalk growing from a giant shoe house."""
  shoe = generate_bite_sized("bite_house_in_a_shoe")
  beanstalk = generate_bite_sized("bite_giant_beanstalk")
  return stamp_voxels(shoe, beanstalk, 2, 0, 4)


def _generate_combo_frog_lagoon() -> np.ndarray:
  """Challenge 2 (page 92): royal frog fountain in mermaid lagoon."""
  lagoon = generate_bite_sized("bite_mermaid_lagoon")
  frog = generate_bite_sized("bite_royal_frog")
  return stamp_voxels(lagoon, frog, 6, 0, 2)


def _generate_combo_atlantis_mushroom() -> np.ndarray:
  """Challenge 3 (page 93): glowing mushroom cap atop atlantis tower."""
  tower = generate_bite_sized("bite_atlantis_abode")
  mushroom = generate_bite_sized("bite_glowing_mushroom")
  return stamp_voxels(tower, mushroom, -1, 8, -1)


def _generate_combo_emerald_library() -> np.ndarray:
  """Challenge 4 (page 93): emerald apartments beside spellbook shop."""
  tower = generate_bite_sized("bite_emerald_apartments")
  shop = generate_bite_sized("bite_spellbook_shop")
  return stamp_voxels(tower, shop, -8, 0, 4)


def _generate_combo_palace_carriage() -> np.ndarray:
  """Challenge 5 (page 93): pumpkin carriage at fairy tale palace gate."""
  palace = generate_bite_sized("bite_fairy_tale_palace")
  carriage = generate_bite_sized("bite_pumpkin_carriage")
  return stamp_voxels(palace, carriage, 2, 0, -10)


_COMBINATION_GENERATORS: dict[str, object] = {
  "bite_combo_submarine_airlock": _generate_combo_submarine_airlock,
  "bite_combo_maze_creeper": _generate_combo_maze_creeper,
  "bite_combo_fountain_aviary": _generate_combo_fountain_aviary,
  "bite_combo_train_collector": _generate_combo_train_collector,
  "bite_combo_bunker_destroyer": _generate_combo_bunker_destroyer,
  "bite_combo_vault_alarm": _generate_combo_vault_alarm,
  "bite_combo_greenhouse_wishing_well": _generate_combo_greenhouse_wishing_well,
  "bite_combo_watchtower_skull_cove": _generate_combo_watchtower_skull_cove,
  "bite_combo_bus_racetrack": _generate_combo_bus_racetrack,
  "bite_combo_steamboat_island": _generate_combo_steamboat_island,
  "bite_combo_pagoda_hot_spring": _generate_combo_pagoda_hot_spring,
  "bite_combo_beanstalk_shoe": _generate_combo_beanstalk_shoe,
  "bite_combo_frog_lagoon": _generate_combo_frog_lagoon,
  "bite_combo_atlantis_mushroom": _generate_combo_atlantis_mushroom,
  "bite_combo_emerald_library": _generate_combo_emerald_library,
  "bite_combo_palace_carriage": _generate_combo_palace_carriage,
}
