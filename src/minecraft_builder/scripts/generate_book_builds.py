"""Generate .litematic files from book build specs — no Minecraft required."""

from __future__ import annotations

from pathlib import Path

import click
import numpy as np
import yaml
from rich.console import Console

from ..book_builds import BOOK_BUILDS
from ..book_builds.generators import generate_book_build
from ..data.palette import BlockPalette
from ..export import export_litematic

console = Console()


@click.command()
@click.option("--build", default=None, help="Specific build id (default: all)")
@click.option("--output-dir", default="data/book_builds")
@click.option("--furnish", is_flag=True, help="Add interior furniture")
def main(build: str | None, output_dir: str, furnish: bool):
  """
  Procedurally generate book builds as .litematic training files.
  You do NOT need to rebuild them in Minecraft.
  """
  out = Path(output_dir)
  out.mkdir(parents=True, exist_ok=True)

  build_ids = [build] if build else list(BOOK_BUILDS.keys())
  palette = BlockPalette()

  for bid in build_ids:
    try:
      indices, spec = generate_book_build(bid, palette)
    except NotImplementedError as exc:
      console.print(f"[yellow]Skipped {bid}: {exc}[/yellow]")
      continue

    if furnish:
      from ..interior import InteriorFurnisher, RoomType

      furnisher = InteriorFurnisher(palette)
      # Furnish workshop (ground) and living (upper) if rooms detected
      for rt in (RoomType.WORKSHOP, RoomType.BEDROOM, RoomType.LIVING):
        results = furnisher.furnish(indices, room_type=rt, max_rooms=1)
        if results:
          indices = furnisher.apply(indices, results)

    path = out / f"{bid}.litematic"
    export_litematic(indices, palette, path, name=spec.name, description=spec.caption)
    console.print(f"[green]Generated {path}[/green]")
    console.print(f"  Caption: {spec.caption}")

  palette.save(out / "palette.json")
  console.print(f"\n[cyan]Next steps:[/cyan]")
  console.print(f"  1. Copy captions: python -m minecraft_builder.scripts.export_book_captions")
  console.print(f"  2. Preprocess:    python -m minecraft_builder.scripts.preprocess --synthetic 500")
  console.print(f"  3. Train:         python -m minecraft_builder.train")


if __name__ == "__main__":
  main()
