"""Procedural generators for Bite-Sized Builds combination challenges."""

from __future__ import annotations

import numpy as np

from ..data.palette import AIR
from .bite_sized_generators import generate_bite_sized
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


_COMBINATION_GENERATORS: dict[str, object] = {
  "bite_combo_submarine_airlock": _generate_combo_submarine_airlock,
  "bite_combo_maze_creeper": _generate_combo_maze_creeper,
  "bite_combo_fountain_aviary": _generate_combo_fountain_aviary,
  "bite_combo_train_collector": _generate_combo_train_collector,
  "bite_combo_bunker_destroyer": _generate_combo_bunker_destroyer,
  "bite_combo_vault_alarm": _generate_combo_vault_alarm,
}
