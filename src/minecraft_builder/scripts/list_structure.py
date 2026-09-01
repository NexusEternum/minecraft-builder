"""List depth and structure techniques from the guide."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

from ..rag.architecture import ARCHITECTURAL_FEATURES
from ..rag.depth import DEPTH_TECHNIQUES
from ..rag.framework import BUILD_STEPS
from ..rag.linking import LINKING_TECHNIQUES, SCENE_TRIGGERS
from ..rag.structure import STRUCTURE_SHAPES

console = Console()


@click.command()
def main():
  depth = Table(title="Adding Depth")
  depth.add_column("Technique", style="cyan")
  depth.add_column("Blocks")
  depth.add_column("Tip", style="dim")
  for t in DEPTH_TECHNIQUES:
    blocks = ", ".join(b.removeprefix("minecraft:").replace("_", " ") for b in t.blocks[:3])
    depth.add_row(t.name, blocks, t.tip)
  console.print(depth)

  shapes = Table(title="Structure Shapes")
  shapes.add_column("Shape", style="cyan")
  shapes.add_column("Keywords")
  shapes.add_column("Circle guide", style="dim")
  for s in STRUCTURE_SHAPES.values():
    kws = ", ".join(s.keywords)
    circles = " → ".join(str(c) for c in s.circle_sizes) if s.circle_sizes else "—"
    shapes.add_row(s.name, kws, circles)
  console.print(shapes)

  framework = Table(title="Build Framework (7 steps)")
  framework.add_column("Step", style="cyan")
  framework.add_column("Name")
  framework.add_column("Instruction", style="dim")
  for s in BUILD_STEPS:
    framework.add_row(str(s.step), s.name, s.instruction)
  console.print(framework)

  arch = Table(title="Architectural Structures")
  arch.add_column("Feature", style="cyan")
  arch.add_column("Blocks")
  arch.add_column("Tip", style="dim")
  for f in ARCHITECTURAL_FEATURES:
    blocks = ", ".join(b.removeprefix("minecraft:").replace("_", " ") for b in f.blocks)
    arch.add_row(f.name, blocks, f.tip)
  console.print(arch)

  linking = Table(title="Linking Builds (multi-building scenes)")
  linking.add_column("Technique", style="cyan")
  linking.add_column("Keywords")
  linking.add_column("Tip", style="dim")
  for t in LINKING_TECHNIQUES:
    kws = ", ".join(t.keywords)
    linking.add_row(t.name, kws, t.tip)
  console.print(linking)
  console.print(f"[dim]Scene triggers: {', '.join(SCENE_TRIGGERS[:8])}...[/dim]")


if __name__ == "__main__":
  main()
