"""List biome → build pairings from Using the Land."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

from ..rag.biomes import BIOMES

console = Console()


@click.command()
def main():
  table = Table(title="Using the Land — Biome Build Guide")
  table.add_column("Biome", style="cyan")
  table.add_column("Good for")
  table.add_column("Characteristics", style="dim")

  for biome in BIOMES.values():
    builds = ", ".join(biome.suitable_builds)
    table.add_row(biome.name, builds, biome.characteristics)

  console.print(table)
  console.print(
    "\n[dim]Scene generation (structure + terrain) is a planned advanced feature.[/dim]"
  )
  console.print("[dim]For now, biomes enrich prompts with suitable build types.[/dim]")


if __name__ == "__main__":
  main()
