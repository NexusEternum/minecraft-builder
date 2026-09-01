"""Training loop for the voxel diffusion model."""

from __future__ import annotations

import json
from pathlib import Path

import click
import torch
import yaml
from rich.console import Console
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

from .data import BlockPalette, VoxelDataset, collate_batch, load_captions, train_val_split
from .models import DiffusionConfig, GaussianDiffusion

console = Console()


def load_config(path: Path) -> dict:
  with open(path, encoding="utf-8") as f:
    return yaml.safe_load(f)


def build_model(cfg: dict, palette_size: int) -> GaussianDiffusion:
  mcfg = cfg["model"]
  dcfg = cfg["diffusion"]
  config = DiffusionConfig(
    timesteps=dcfg["timesteps"],
    beta_schedule=dcfg["beta_schedule"],
    embed_dim=mcfg["embed_dim"],
    num_classes=max(palette_size, mcfg.get("num_classes", 256)),
    base_channels=mcfg["base_channels"],
    channel_mults=mcfg["channel_mults"],
    num_res_blocks=mcfg["num_res_blocks"],
    text_dim=mcfg["text_dim"],
    text_vocab_size=mcfg["text_vocab_size"],
    text_max_len=mcfg["text_max_len"],
  )
  return GaussianDiffusion(config)


@click.command()
@click.option("--config", default="configs/default.yaml")
@click.option("--resume", default=None, help="Checkpoint path to resume from")
def main(config: str, resume: str | None):
  """Train the Minecraft voxel diffusion model from scratch."""
  cfg = load_config(Path(config))
  device_name = cfg["train"]["device"]
  device = torch.device(device_name if torch.cuda.is_available() else "cpu")
  if device.type == "cuda":
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
  console.print(f"[cyan]Device: {device}[/cyan]")

  processed_dir = Path(cfg["data"]["processed_dir"])
  palette_path = processed_dir / "palette.json"
  if not palette_path.exists():
    console.print("[red]No processed data found. Run preprocess first:[/red]")
    console.print("  python -m minecraft_builder.scripts.preprocess")
    raise SystemExit(1)

  palette = BlockPalette.load(palette_path)
  captions = load_captions(Path(cfg["data"]["captions_file"]))

  dataset = VoxelDataset(processed_dir, palette, captions, cfg["data"]["resolution"])
  train_ds, val_ds = train_val_split(dataset, 1 - cfg["data"]["train_split"])

  train_loader = DataLoader(
    train_ds,
    batch_size=cfg["train"]["batch_size"],
    shuffle=True,
    collate_fn=collate_batch,
    num_workers=cfg["train"].get("num_workers", 0),
    pin_memory=device.type == "cuda",
  )
  val_loader = DataLoader(
    val_ds,
    batch_size=cfg["train"]["batch_size"],
    shuffle=False,
    collate_fn=collate_batch,
    num_workers=cfg["train"].get("num_workers", 0),
    pin_memory=device.type == "cuda",
  )

  model = build_model(cfg, palette.size).to(device)
  optimizer = torch.optim.AdamW(
    model.parameters(), lr=cfg["train"]["lr"], weight_decay=cfg["train"]["weight_decay"]
  )

  ckpt_dir = Path(cfg["train"]["checkpoint_dir"])
  ckpt_dir.mkdir(parents=True, exist_ok=True)
  writer = SummaryWriter(log_dir=str(ckpt_dir / "logs"))

  start_epoch = 0
  if resume:
    ckpt = torch.load(resume, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    optimizer.load_state_dict(ckpt["optimizer"])
    start_epoch = ckpt["epoch"] + 1
    console.print(f"[green]Resumed from epoch {start_epoch}[/green]")

  global_step = 0
  for epoch in range(start_epoch, cfg["train"]["epochs"]):
    model.train()
    train_loss = 0.0
    pbar = tqdm(train_loader, desc=f"Epoch {epoch + 1}/{cfg['train']['epochs']}")
    for batch in pbar:
      voxels = batch["voxels"].to(device)
      loss = model.training_loss(
        voxels, batch["captions"], non_air_weight=cfg["train"]["non_air_weight"]
      )
      optimizer.zero_grad()
      loss.backward()
      torch.nn.utils.clip_grad_norm_(model.parameters(), cfg["train"]["grad_clip"])
      optimizer.step()

      train_loss += loss.item()
      global_step += 1
      if global_step % cfg["train"]["log_every"] == 0:
        writer.add_scalar("train/loss", loss.item(), global_step)
      pbar.set_postfix(loss=f"{loss.item():.4f}")
      if not torch.isfinite(loss):
        console.print("[red]Non-finite loss detected — stopping training.[/red]")
        raise SystemExit(1)

    avg_train = train_loss / max(len(train_loader), 1)

    # Validation
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
      for batch in val_loader:
        voxels = batch["voxels"].to(device)
        loss = model.training_loss(voxels, batch["captions"])
        val_loss += loss.item()
    avg_val = val_loss / max(len(val_loader), 1)
    writer.add_scalar("val/loss", avg_val, epoch)

    console.print(f"Epoch {epoch + 1}: train={avg_train:.4f}  val={avg_val:.4f}")

    if (epoch + 1) % cfg["train"]["save_every"] == 0 or epoch == cfg["train"]["epochs"] - 1:
      ckpt_path = ckpt_dir / f"model_epoch_{epoch + 1:03d}.pt"
      torch.save(
        {
          "epoch": epoch,
          "model": model.state_dict(),
          "optimizer": optimizer.state_dict(),
          "config": cfg,
          "palette_size": palette.size,
        },
        ckpt_path,
      )
      console.print(f"[green]Saved {ckpt_path}[/green]")

  writer.close()
  console.print("[green]Training complete.[/green]")


if __name__ == "__main__":
  main()
