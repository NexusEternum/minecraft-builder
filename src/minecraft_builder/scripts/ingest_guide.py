"""Ingest the Minecraft Guide to Creative into a local RAG index."""

from __future__ import annotations

from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.table import Table

from ..rag import GuideIndex, load_directory, load_document

console = Console()


def load_config(path: Path) -> dict:
  with open(path, encoding="utf-8") as f:
    return yaml.safe_load(f)


@click.command()
@click.option("--source", required=True, help="Path to PDF/txt/md file or folder")
@click.option("--config", default="configs/default.yaml")
def main(source: str, config: str):
  """
  Index your copy of the Minecraft Guide to Creative for private RAG use.

  Examples:
    python -m minecraft_builder.scripts.ingest_guide --source data/guide/creative_guide.pdf
    python -m minecraft_builder.scripts.ingest_guide --source data/guide/
  """
  cfg = load_config(Path(config))
  rag_cfg = cfg.get("rag", {})
  source_path = Path(source)
  index_dir = Path(rag_cfg.get("index_dir", "data/rag"))
  chunk_size = rag_cfg.get("chunk_size", 500)
  overlap = rag_cfg.get("chunk_overlap", 80)

  if not source_path.exists():
    console.print(f"[red]Source not found:[/red] {source_path}")
    raise SystemExit(1)

  console.print(f"[cyan]Loading from[/cyan] {source_path}")
  if source_path.is_dir():
    chunks = load_directory(source_path, chunk_size=chunk_size, overlap=overlap)
  else:
    chunks = load_document(source_path, chunk_size=chunk_size, overlap=overlap)

  console.print(f"[cyan]Chunks created:[/cyan] {len(chunks)}")

  index = GuideIndex()
  index.build(chunks)
  index.save(index_dir)

  # Preview retrieval
  table = Table(title="Sample retrieval: 'cozy cottage with stone roof'")
  table.add_column("Score", style="cyan")
  table.add_column("Source")
  table.add_column("Preview")

  for result in index.search("cozy cottage with stone roof", top_k=3):
    preview = result.chunk.text[:120].replace("\n", " ") + "..."
    page = f" p.{result.chunk.page}" if result.chunk.page else ""
    table.add_row(f"{result.score:.3f}", f"{result.chunk.source}{page}", preview)

  console.print(table)
  console.print(f"[green]RAG index saved to {index_dir}[/green]")
  console.print("Use --use-rag when generating to enrich prompts from the guide.")


if __name__ == "__main__":
  main()
