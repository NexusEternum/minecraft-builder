"""Export book build captions for training data/captions.json."""

from __future__ import annotations

import json
from pathlib import Path

import click
from rich.console import Console

from ..book_builds import BOOK_BUILDS
from ..book_builds.registry import build_caption

console = Console()


@click.command()
@click.option("--output", default="data/captions.json")
def main(output: str):
  """Print captions for all registered book builds — add to your training captions."""
  path = Path(output)
  existing: dict[str, str] = {}
  if path.exists():
    existing = json.loads(path.read_text(encoding="utf-8"))

  for build in BOOK_BUILDS.values():
    key = f"{build.id}.litematic"
    cap = build_caption(build)
    existing[key] = cap
    console.print(f"[cyan]{build.name}[/cyan]")
    console.print(f"  Caption: {cap}")
    console.print(f"  Palette: {', '.join(b.removeprefix('minecraft:') for b in build.palette)}")
    console.print(f"  Zones: {', '.join(z.name for z in build.zones)}")
    console.print()

  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
  console.print(f"[green]Updated {path} with {len(BOOK_BUILDS)} book build captions[/green]")
  console.print("Recreate builds as .litematic and place in data/book_builds/ for training.")


if __name__ == "__main__":
  main()
