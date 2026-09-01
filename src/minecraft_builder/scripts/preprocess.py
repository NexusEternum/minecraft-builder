"""Preprocess raw schematics into training-ready .npz files."""

from __future__ import annotations

import json
from pathlib import Path

import click
import numpy as np
import yaml
from rich.console import Console
from tqdm import tqdm

from ..data import BlockPalette, generate_synthetic_dataset, load_voxels, voxels_to_palette_indices

console = Console()


def load_config(path: Path) -> dict:
  with open(path, encoding="utf-8") as f:
    return yaml.safe_load(f)


@click.command()
@click.option("--config", default="configs/default.yaml", help="Path to config file")
@click.option("--synthetic", default=200, help="Number of synthetic samples to generate (0 to skip)")
@click.option("--raw-dir", default=None, help="Override raw data directory")
@click.option("--book-builds/--no-book-builds", default=True, help="Generate procedural book builds")
def main(config: str, synthetic: int, raw_dir: str | None, book_builds: bool):
  """Preprocess schematic files and optionally generate synthetic training data."""
  cfg = load_config(Path(config))
  resolution = cfg["data"]["resolution"]
  max_palette = cfg["data"]["max_palette_size"]
  processed_dir = Path(cfg["data"]["processed_dir"])
  raw = Path(raw_dir or cfg["data"]["raw_dir"])
  captions_path = Path(cfg["data"]["captions_file"])

  processed_dir.mkdir(parents=True, exist_ok=True)
  raw.mkdir(parents=True, exist_ok=True)

  palette = BlockPalette(max_size=max_palette)
  captions: dict[str, str] = {}

  # Synthetic bootstrap data
  if synthetic > 0:
    console.print(f"[cyan]Generating {synthetic} synthetic builds...[/cyan]")
    synth_dir = processed_dir / "synthetic"
    synth_captions = generate_synthetic_dataset(synth_dir, count=synthetic, resolution=resolution)
    captions.update(synth_captions)

    for npy_file in tqdm(sorted(synth_dir.glob("*.npy")), desc="Encoding synthetic"):
      voxels = np.load(npy_file, allow_pickle=True)
      indices = voxels_to_palette_indices(voxels, palette)
      out = processed_dir / npy_file.name.replace(".npy", ".npz")
      np.savez_compressed(out, voxels=indices)

  # Procedural book builds (no Minecraft required)
  if book_builds:
    from ..book_builds import BOOK_BUILDS
    from ..book_builds.generators import generate_book_build
    from ..book_builds.registry import build_caption

    console.print(f"[cyan]Generating {len(BOOK_BUILDS)} book build(s)...[/cyan]")
    for bid, spec in BOOK_BUILDS.items():
      try:
        indices, _ = generate_book_build(bid, palette)
        out = processed_dir / f"book_{bid}.npz"
        np.savez_compressed(out, voxels=indices)
        captions[f"book_{bid}.npz"] = build_caption(spec)
        captions[f"{bid}.litematic"] = build_caption(spec)
      except NotImplementedError as exc:
        console.print(f"[yellow]Skipped {bid}: {exc}[/yellow]")

  # Raw schematic files
  from ..data.ingest import SUPPORTED_EXTENSIONS

  raw_files = []
  for ext in SUPPORTED_EXTENSIONS:
    raw_files.extend(raw.glob(f"*{ext}"))

  if raw_files:
    console.print(f"[cyan]Processing {len(raw_files)} raw schematics...[/cyan]")
    existing_captions = {}
    if captions_path.exists():
      existing_captions = json.loads(captions_path.read_text(encoding="utf-8"))

    for path in tqdm(raw_files, desc="Processing raw"):
      try:
        voxels = load_voxels(path, resolution)
        indices = voxels_to_palette_indices(voxels, palette)
        out = processed_dir / f"{path.stem}.npz"
        np.savez_compressed(out, voxels=indices)
        cap = existing_captions.get(path.name) or existing_captions.get(path.stem)
        if cap:
          captions[out.name] = cap
      except Exception as exc:
        console.print(f"[yellow]Skipped {path.name}: {exc}[/yellow]")

  palette.save(processed_dir / "palette.json")
  captions_path.parent.mkdir(parents=True, exist_ok=True)
  captions_path.write_text(json.dumps(captions, indent=2), encoding="utf-8")

  console.print(f"[green]Done![/green] Processed data in {processed_dir}")
  console.print(f"Palette: {palette.size} block classes")
  console.print(f"Captions: {len(captions)} entries -> {captions_path}")


if __name__ == "__main__":
  main()
