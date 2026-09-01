"""List book photos waiting to be processed into training builds."""

from __future__ import annotations

import json
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from ..book_builds import BOOK_BUILDS
from ..book_builds.bite_sized_registry import BITE_SIZED_BUILDS

console = Console()

PHOTO_DIR = Path("data/book_photos/bite_sized_builds")
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


@click.command()
def main():
  manifest_path = PHOTO_DIR / "manifest.json"
  manifest = {"processed": [], "pending": []}
  if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

  photos = sorted(
    p for p in PHOTO_DIR.iterdir()
    if p.suffix.lower() in IMAGE_EXTS
  ) if PHOTO_DIR.exists() else []

  table = Table(title="Bite-Sized Builds Status")
  table.add_column("Build ID")
  table.add_column("Name")
  table.add_column("Generator")
  table.add_column("Status")

  for bid, spec in BITE_SIZED_BUILDS.items():
    has_gen = bid in BOOK_BUILDS
    table.add_row(bid, spec.name, "yes" if has_gen else "no", "[green]ready[/green]")

  for p in photos:
    stem = p.stem
    if not any(stem.startswith(bid.replace("bite_", "")) for bid in BITE_SIZED_BUILDS):
      table.add_row("—", stem, "—", "[yellow]photo waiting[/yellow]")

  console.print(table)
  console.print(f"\nGuide to Creative builds: {len(BOOK_BUILDS) - len(BITE_SIZED_BUILDS)}")
  console.print(f"Bite-sized builds:       {len(BITE_SIZED_BUILDS)}")
  console.print(f"Photos in drop folder:   {len(photos)}")
  console.print(f"Processed (manifest):    {len(manifest.get('processed', []))}")

  if photos:
    console.print("\n[cyan]Photos found:[/cyan]")
    for p in photos:
      console.print(f"  {p.name}")


if __name__ == "__main__":
  main()
