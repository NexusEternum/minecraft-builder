"""List natural features from the Natural Features chapter."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

from ..rag.natural_features import NATURAL_FEATURES

console = Console()


@click.command()
def main():
  table = Table(title="Natural Features — Build Guide")
  table.add_column("Feature", style="cyan")
  table.add_column("Good for")
  table.add_column("Tip", style="dim")

  for f in NATURAL_FEATURES:
    builds = ", ".join(f.suitable_builds[:3])
    table.add_row(f.name, builds, f.tip)

  console.print(table)


if __name__ == "__main__":
  main()
