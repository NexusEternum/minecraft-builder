"""Diagnose where NaN appears during CUDA forward pass."""
import torch
import yaml
from pathlib import Path

from minecraft_builder.data import BlockPalette, VoxelDataset, collate_batch, load_captions, train_val_split
from minecraft_builder.models import DiffusionConfig, GaussianDiffusion


def check(name, tensor):
    has_nan = torch.isnan(tensor).any().item()
    has_inf = torch.isinf(tensor).any().item()
    mx = tensor.abs().max().item()
    tag = ""
    if has_nan:
        tag = " *** NaN ***"
    elif has_inf:
        tag = " *** Inf ***"
    print(f"  {name:30s}  nan={has_nan}  inf={has_inf}  absmax={mx:.6g}  shape={list(tensor.shape)}{tag}")
    return has_nan or has_inf


def main():
    cfg = yaml.safe_load(open("configs/runpod_h100.yaml"))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    palette = BlockPalette.load(Path("data/processed/palette.json"))
    captions = load_captions(Path("data/captions.json"))
    ds = VoxelDataset(Path("data/processed"), palette, captions, 32)
    train_ds, _ = train_val_split(ds, 0.15)

    print(f"Dataset: {len(ds)} samples, palette: {palette.size} classes")
    print(f"Train split: {len(train_ds)} samples")

    bs = min(cfg["train"]["batch_size"], len(train_ds))
    batch = collate_batch([train_ds[i] for i in range(bs)])
    voxels = batch["voxels"].to(device)

    print(f"\n--- Data check ---")
    print(f"  voxels: min={voxels.min().item()} max={voxels.max().item()} dtype={voxels.dtype}")
    air_pct = (voxels == 0).float().mean().item() * 100
    print(f"  air percentage: {air_pct:.1f}%")

    mcfg, dcfg = cfg["model"], cfg["diffusion"]
    num_classes = max(palette.size, mcfg.get("num_classes", 256))
    print(f"  num_classes for model: {num_classes}")
    if voxels.max().item() >= num_classes:
        print(f"  *** PROBLEM: max voxel index {voxels.max().item()} >= num_classes {num_classes} ***")

    model = GaussianDiffusion(DiffusionConfig(
        timesteps=dcfg["timesteps"], beta_schedule=dcfg["beta_schedule"],
        embed_dim=mcfg["embed_dim"], num_classes=num_classes,
        base_channels=mcfg["base_channels"], channel_mults=mcfg["channel_mults"],
        num_res_blocks=mcfg["num_res_blocks"], text_dim=mcfg["text_dim"],
        text_vocab_size=mcfg["text_vocab_size"], text_max_len=mcfg["text_max_len"],
    )).to(device)
    model.train()

    print(f"\n--- Diffusion schedule ---")
    check("betas", model.betas)
    check("alphas_cumprod", model.alphas_cumprod)
    check("sqrt_alphas_cumprod", model.sqrt_alphas_cumprod)
    check("sqrt_1-alphas_cumprod", model.sqrt_one_minus_alphas_cumprod)

    print(f"\n--- Embedding ---")
    check("block_embed.weight", model.block_embed.weight)
    voxels_clamped = voxels.clamp(0, num_classes - 1)
    x0 = model.embed_voxels(voxels_clamped)
    check("x0 (embedded voxels)", x0)

    print(f"\n--- Noise schedule ---")
    b = voxels.shape[0]
    t = torch.randint(0, dcfg["timesteps"], (b,), device=device)
    print(f"  timesteps sampled: {t.tolist()[:8]}...")
    xt, noise = model.q_sample(x0, t)
    check("xt (noised)", xt)
    check("noise", noise)

    print(f"\n--- Text encoder ---")
    text_emb = model.encode_text(batch["captions"], device)
    check("text_emb", text_emb)
    null_emb = model.encode_text([""] * b, device)
    check("null_emb", null_emb)

    print(f"\n--- UNet forward ---")
    t_emb = model.unet.time_embed(t)
    check("time_embedding", t_emb)

    h = model.unet.input_conv(xt)
    check("after input_conv", h)

    skips = []
    for i, stage in enumerate(model.unet.down_stages):
        for j, block in enumerate(stage.res):
            norm_out = block.norm1(h)
            check(f"down[{i}].res[{j}].norm1", norm_out)
            conv_out = block.conv1(torch.nn.functional.silu(norm_out))
            check(f"down[{i}].res[{j}].conv1", conv_out)
            cond = block.time_proj(t_emb)[:, :, None, None, None] + block.text_proj(text_emb)[:, :, None, None, None]
            check(f"down[{i}].res[{j}].cond", cond)
            h_inner = conv_out + cond
            norm2_out = block.norm2(h_inner)
            check(f"down[{i}].res[{j}].norm2", norm2_out)
            conv2_out = block.conv2(torch.nn.functional.silu(norm2_out))
            check(f"down[{i}].res[{j}].conv2", conv2_out)
            h = h + conv2_out
            if check(f"down[{i}].res[{j}].output", h):
                print("  *** Stopping at first NaN ***")
                return
        skips.append(h)
        h = stage.down(h)
        if check(f"down[{i}].downsample", h):
            print("  *** Stopping at first NaN ***")
            return

    for i, block in enumerate(model.unet.mid):
        norm_out = block.norm1(h)
        check(f"mid[{i}].norm1", norm_out)
        h_mid = block.conv1(torch.nn.functional.silu(norm_out))
        cond = block.time_proj(t_emb)[:, :, None, None, None] + block.text_proj(text_emb)[:, :, None, None, None]
        h_mid = h_mid + cond
        norm2_out = block.norm2(h_mid)
        check(f"mid[{i}].norm2", norm2_out)
        h_mid = block.conv2(torch.nn.functional.silu(norm2_out))
        h = h + h_mid
        if check(f"mid[{i}].output", h):
            print("  *** Stopping at first NaN ***")
            return

    for i, (stage, skip) in enumerate(zip(model.unet.up_stages, reversed(skips))):
        h = stage.up(h)
        if h.shape[2:] != skip.shape[2:]:
            h = torch.nn.functional.interpolate(h, size=skip.shape[2:], mode="trilinear", align_corners=False)
        h = stage.merge(torch.cat([h, skip], dim=1))
        for j, block in enumerate(stage.res):
            norm_out = block.norm1(h)
            check(f"up[{i}].res[{j}].norm1", norm_out)
            conv_out = block.conv1(torch.nn.functional.silu(norm_out))
            cond = block.time_proj(t_emb)[:, :, None, None, None] + block.text_proj(text_emb)[:, :, None, None, None]
            h_inner = conv_out + cond
            norm2_out = block.norm2(h_inner)
            conv2_out = block.conv2(torch.nn.functional.silu(norm2_out))
            h = h + conv2_out
            if check(f"up[{i}].res[{j}].output", h):
                print("  *** Stopping at first NaN ***")
                return

    out = model.unet.output(h)
    check("unet_output (pred_noise)", out)

    print(f"\n--- Loss ---")
    diff = (out - noise).pow(2)
    check("(pred - noise)^2", diff)
    weight = torch.where(
        voxels_clamped.unsqueeze(1) != 0,
        torch.full((), 5.0, device=device, dtype=x0.dtype),
        torch.ones((), device=device, dtype=x0.dtype),
    )
    check("weight", weight)
    loss = (weight * diff).mean()
    print(f"\n  FINAL LOSS: {loss.item()}")


if __name__ == "__main__":
    main()
