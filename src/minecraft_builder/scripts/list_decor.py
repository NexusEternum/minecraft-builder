"""List functional decor and lighting from the guide."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

from ..rag.decor import DECOR_FEATURES, LIGHT_SOURCES, MOB_SAFE_LIGHT_LEVEL, mob_safe_sources
from ..rag.themed_rooms import THEMED_ROOMS
from ..rag.interiors import INTERIOR_DECOR, WALL_FLOOR_TECHNIQUES

console = Console()


@click.command()
def main():
  lights = Table(title="Light Levels (reference)")
  lights.add_column("Block", style="cyan")
  lights.add_column("Level")
  for block, level in sorted(LIGHT_SOURCES.items(), key=lambda x: -x[1]):
    safe = " ✓" if level >= MOB_SAFE_LIGHT_LEVEL else ""
    lights.add_row(block.replace("_", " "), f"{level}{safe}")
  console.print(lights)
  console.print(f"[dim]✓ = mob-safe (level {MOB_SAFE_LIGHT_LEVEL}+)[/dim]\n")

  rooms = Table(title="Themed Rooms & Utility Blocks")
  rooms.add_column("Room", style="cyan")
  rooms.add_column("Utility blocks")
  rooms.add_column("Tip", style="dim")
  for room in THEMED_ROOMS.values():
    utils = ", ".join(b.removeprefix("minecraft:").replace("_", " ") for b in room.utility_blocks)
    rooms.add_row(room.name, utils, room.tip)
  console.print(rooms)

  windows = Table(title="Window Styles")
  windows.add_column("Style", style="cyan")
  windows.add_column("Blocks")
  windows.add_column("Tip", style="dim")
  for w in WINDOW_STYLES:
    blocks = ", ".join(b.removeprefix("minecraft:").replace("_", " ") for b in w.blocks)
    windows.add_row(w.name, blocks, w.tip)
  console.print(windows)

  walls = Table(title="Walls & Floors")
  walls.add_column("Technique", style="cyan")
  walls.add_column("Blocks")
  walls.add_column("Best in", style="dim")
  for t in WALL_FLOOR_TECHNIQUES:
    blocks = ", ".join(b.removeprefix("minecraft:").replace("_", " ") for b in t.blocks[:3])
    rooms = ", ".join(t.room_types) or "any"
    walls.add_row(t.name, blocks, rooms)
  console.print(walls)

  gallery = Table(title="Interior Decor (Paintings & Item Frames)")
  gallery.add_column("Feature", style="cyan")
  gallery.add_column("Blocks")
  gallery.add_column("Tip", style="dim")
  for d in INTERIOR_DECOR:
    blocks = ", ".join(b.removeprefix("minecraft:").replace("_", " ") for b in d.blocks)
    gallery.add_row(d.name, blocks, d.tip)
  console.print(gallery)

  from ..rag.furniture import FURNITURE_HACKS

  furn = Table(title="Furniture Hacks")
  furn.add_column("Item", style="cyan")
  furn.add_column("Blocks")
  furn.add_column("Room", style="dim")
  for h in FURNITURE_HACKS:
    blocks = ", ".join(b.removeprefix("minecraft:").replace("_", " ") for b in h.blocks[:3])
    furn.add_row(h.name, blocks, h.room)
  console.print(furn)

  decor = Table(title="Light Fixtures")
  decor.add_column("Feature", style="cyan")
  decor.add_column("Blocks")
  decor.add_column("Tip", style="dim")
  for f in DECOR_FEATURES:
    blocks = ", ".join(b.removeprefix("minecraft:").replace("_", " ") for b in f.blocks)
    decor.add_row(f.name, blocks, f.tip)
  console.print(decor)


if __name__ == "__main__":
  main()
