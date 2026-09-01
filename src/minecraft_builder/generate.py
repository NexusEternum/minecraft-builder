"""Generate a Minecraft build from a text prompt."""

from __future__ import annotations

from pathlib import Path

import click
import torch
import yaml
from rich.console import Console

from .data import BlockPalette
from .export import export_litematic
from .models import DiffusionConfig, GaussianDiffusion
from .train import build_model

console = Console()


def load_config(path: Path) -> dict:
  with open(path, encoding="utf-8") as f:
    return yaml.safe_load(f)


@click.command()
@click.option("--prompt", required=True, help="Text description of the build")
@click.option("--checkpoint", required=True, help="Path to trained model checkpoint")
@click.option("--config", default="configs/default.yaml")
@click.option("--output", default=None, help="Output .litematic path")
@click.option("--guidance", default=None, type=float, help="Classifier-free guidance scale")
@click.option("--use-rag/--no-rag", default=None, help="Enrich prompt from the creative guide index")
@click.option("--theme", default=None, help="Force a book theme: rustic, historical, fantasy, industrial, steampunk, infernal, classical, monochromatic")
@click.option("--furnish/--no-furnish", default=False, help="Furnish interior rooms after generation (procedural module)")
@click.option("--room-type", default="living room", help="Room type for furnishing: living room, bedroom, kitchen, bathroom, workshop")
def main(
  prompt: str,
  checkpoint: str,
  config: str,
  output: str | None,
  guidance: float | None,
  use_rag: bool | None,
  theme: str | None,
  furnish: bool,
  room_type: str,
):
  """Generate a .litematic file from a text prompt using your trained model."""
  cfg = load_config(Path(config))
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

  ckpt = torch.load(checkpoint, map_location=device, weights_only=False)
  palette_path = Path(cfg["data"]["processed_dir"]) / "palette.json"
  palette = BlockPalette.load(palette_path)

  model = build_model(cfg, ckpt.get("palette_size", palette.size)).to(device)
  model.load_state_dict(ckpt["model"])
  model.eval()

  guidance_scale = guidance if guidance is not None else cfg["generate"]["guidance_scale"]
  resolution = cfg["data"]["resolution"]
  should_use_rag = use_rag if use_rag is not None else cfg["generate"].get("use_rag", False)

  from .rag import enrich_prompt, load_index

  rag_cfg = cfg.get("rag", {})
  index = None
  if should_use_rag:
    index_dir = Path(rag_cfg.get("index_dir", "data/rag"))
    try:
      index = load_index(index_dir)
    except FileNotFoundError:
      console.print("[yellow]RAG index not found — using theme palettes only.[/yellow]")
      console.print("  Run: python -m minecraft_builder.scripts.ingest_guide --source data/guide/")

  generation_prompt, hits, matched_themes = enrich_prompt(
    prompt,
    index=index,
    max_len=cfg["model"]["text_max_len"],
    top_k=rag_cfg.get("top_k", 4),
    theme=theme,
  )

  from .rag.scenes import parse_scene_prompt, scene_available

  scene = parse_scene_prompt(prompt)
  if scene.include_terrain and not scene_available():
    if scene.is_multi_building:
      console.print(
        "[yellow]Multi-building scene mode is planned — generating primary structure only.[/yellow]"
      )
      console.print(
        f"[dim]Scene would include ~{scene.building_count} buildings with: "
        f"{', '.join(scene.linking_keywords[:4]) or 'roads, parks, paths'}[/dim]"
      )
    else:
      console.print(
        "[yellow]Scene mode (structure + terrain) is planned — generating structure only.[/yellow]"
      )
  if scene.biome:
    console.print(f"[dim]Biome context: {scene.biome.name} — {scene.biome.characteristics}[/dim]")
  if scene.natural_features:
    names = ", ".join(f.name for f in scene.natural_features)
    console.print(f"[dim]Natural features: {names}[/dim]")

  if generation_prompt != prompt:
    console.print(f'[cyan]Enriched prompt:[/cyan] "{generation_prompt}"')
  if matched_themes:
    names = ", ".join(t.name for t in matched_themes)
    console.print(f"[dim]Themes: {names}[/dim]")
  if index and hits:
    console.print(f"[dim]Retrieved {len(hits)} passage(s) from the guide[/dim]")

  from .book_builds import match_build

  book_build = match_build(prompt)
  if book_build:
    console.print(f"[dim]Book build matched: {book_build.name}[/dim]")
    if generation_prompt == prompt:
      generation_prompt = book_build.caption

  console.print(f'[cyan]Generating:[/cyan] "{generation_prompt}"')
  console.print(f"[cyan]Guidance scale:[/cyan] {guidance_scale}")

  with torch.no_grad():
    voxels = model.sample(
      [generation_prompt], resolution, guidance_scale=guidance_scale, device=device
    )

  indices = voxels[0].cpu().numpy()

  if furnish:
    from .interior import InteriorFurnisher, RoomType

    furnisher = InteriorFurnisher(palette)
    try:
      rt = RoomType(room_type)
    except ValueError:
      rt = RoomType.GENERIC
    results = furnisher.furnish(indices, room_type=rt)
    if results:
      indices = furnisher.apply(indices, results)
      console.print(f"[green]Furnished {len(results)} room(s) as {rt.value}[/green]")
    else:
      console.print("[yellow]No interior rooms detected — try a hollow-shell exterior build[/yellow]")

  out_dir = Path(cfg["generate"]["output_dir"])
  out_dir.mkdir(parents=True, exist_ok=True)

  safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in prompt[:40])
  out_path = Path(output) if output else out_dir / f"{safe_name}.litematic"

  export_litematic(
    indices,
    palette,
    out_path,
    name=prompt[:64],
    description=f'Generated from prompt: "{prompt}"',
  )
  console.print(f"[green]Saved {out_path}[/green]")
  console.print("Import into Minecraft with the Litematica mod.")


if __name__ == "__main__":
  main()
