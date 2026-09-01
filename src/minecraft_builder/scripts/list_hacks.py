"""List block hacks from the Minecraft Guide to Creative."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

from ..rag.block_hacks import BLOCK_HACKS

console = Console()


@click.command()
def main():
  """Show all block hacks and their trigger words."""
  table = Table(title="Minecraft Guide to Creative — Block Hacks")
  table.add_column("Technique", style="cyan")
  table.add_column("Blocks")
  table.add_column("Triggers when prompt mentions", style="dim")

  for hack in BLOCK_HACKS:
    blocks = ", ".join(b.removeprefix("minecraft:").replace("_", " ") for b in hack.blocks)
    triggers = ", ".join(hack.triggers[:5])
    table.add_row(hack.name, blocks, triggers)

  console.print(table)
  console.print("\n[dim]These auto-enrich prompts when trigger words are detected.[/dim]")


if __name__ == "__main__":
  main()
