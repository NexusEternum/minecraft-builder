"""List block palettes from the Minecraft Guide to Creative."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

from ..rag.themes import THEMES, theme_block_names

console = Console()


@click.command()
def main():
  """Show all book themes and their block palettes."""
  table = Table(title="Minecraft Guide to Creative — Theme Palettes")
  table.add_column("Theme", style="cyan")
  table.add_column("Blocks")
  table.add_column("Trigger words", style="dim")

  for theme in THEMES.values():
    blocks = ", ".join(theme_block_names(theme))
    aliases = ", ".join(theme.aliases[:4])
    table.add_row(theme.name, blocks, aliases)

  console.print(table)
  console.print(
    "\nUse with: python -m minecraft_builder.generate --prompt \"a tower\" --theme steampunk --checkpoint ..."
  )


if __name__ == "__main__":
  main()
