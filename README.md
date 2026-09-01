# Minecraft Builder AI

Train a **custom** text-to-Minecraft model from scratch. No pretrained schematic generators — you own the full pipeline: data ingestion, 3D diffusion model, training, and Litematica export.

```
Prompt → [RAG: Creative Guide] → Text Encoder → 3D Diffusion U-Net → Voxel Grid → .litematic
```

## How it works

1. **Data** — Load `.litematic`, `.schem`, or `.schematic` files (or bootstrap with synthetic procedural builds)
2. **Preprocess** — Normalize structures to 32³ voxel grids with a block palette
3. **Model** — 3D U-Net with DDPM diffusion, trained from scratch with a character-level text encoder
4. **Generate** — Sample a voxel grid conditioned on your prompt, export to `.litematic`

## Quick start

```bash
# Install
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e .

# 1. Preprocess (generates 200 synthetic builds to bootstrap training)
python -m minecraft_builder.scripts.preprocess --synthetic 200

# 2. Train (requires GPU for reasonable speed; CPU works for smoke tests)
python -m minecraft_builder.train

# 3. Generate
python -m minecraft_builder.generate --prompt "a stone tower with battlements" --checkpoint checkpoints/model_epoch_010.pt

# Optional: enrich prompts from your copy of the Minecraft Guide to Creative
python -m minecraft_builder.scripts.ingest_guide --source data/guide/creative_guide.pdf
python -m minecraft_builder.generate --prompt "a cozy cottage" --checkpoint checkpoints/model_epoch_010.pt --use-rag
```

## RAG with the Minecraft Guide to Creative (private use)

You can index your own copy of the book to enrich prompts before generation. The guide is **not** used to place blocks — it adds style and material hints to the prompt your model sees.

1. Put your PDF or text export in `data/guide/` (this folder is gitignored)
2. Build the local index:

```bash
python -m minecraft_builder.scripts.ingest_guide --source data/guide/creative_guide.pdf
```

3. Generate with RAG:

```bash
python -m minecraft_builder.generate --prompt "a cozy cottage" --checkpoint checkpoints/model_epoch_050.pt --use-rag
```

**How it works:**
- Book is chunked and indexed locally with TF-IDF (no cloud, no API)
- Your prompt retrieves relevant passages
- **Theme palettes** from the book (rustic, fantasy, steampunk, etc.) inject the right blocks
- Keywords are appended to the prompt for your diffusion model

### Book theme palettes (built in)

| Theme | Blocks |
|---|---|
| **rustic** | cobblestone, dark oak planks/log, andesite, glass |
| **historical** | sandstone, orange terracotta, diorite, andesite, granite |
| **fantasy** | purpur, prismarine, moss block |
| **industrial** | stone bricks, polished andesite, quartz, gravel |
| **steampunk** | stone bricks, oak log, glowstone, quartz, dark oak |
| **infernal** | nether bricks, netherrack, obsidian, glowstone |
| **classical** | quartz, diorite, chiseled stone bricks, light blue glass |
| **monochromatic** | black concrete → coal → gray → stone bricks → quartz scale |

```bash
# List all themes
python -m minecraft_builder.scripts.list_themes

# List block hacks (stairs roofs, trapdoor shutters, cobweb smoke, etc.)
python -m minecraft_builder.scripts.list_hacks

# List biome → build pairings (plains → farmhouse, forest → cottage, etc.)
python -m minecraft_builder.scripts.list_biomes

# Force a theme (works without indexing the PDF)
python -m minecraft_builder.generate --prompt "a small watchtower" --theme steampunk --checkpoint checkpoints/model_epoch_050.pt

# Auto-detect theme from prompt + RAG
python -m minecraft_builder.generate --prompt "a rustic cottage" --use-rag --checkpoint checkpoints/model_epoch_050.pt
```

## Adding your own builds

1. Drop `.litematic` / `.schem` files into `data/raw/`
2. Add captions in `data/captions.json`:

```json
{
  "my_house.litematic": "a cozy medieval house with oak walls and stone roof",
  "castle.schem": "a large stone castle with four towers"
}
```

3. Re-run preprocess, then train.

## Project structure

```
configs/default.yaml          # All hyperparameters
src/minecraft_builder/
  data/                       # Ingestion, palette, dataset, synthetic data
  models/                     # 3D U-Net, diffusion, text encoder (from scratch)
  rag/                        # Private book RAG (ingest, retrieve, enrich)
  export/                     # Voxel grid → .litematic
  scripts/preprocess.py       # Data preprocessing CLI
  scripts/ingest_guide.py     # Index the creative guide for RAG
  train.py                    # Training loop
  generate.py                 # Inference CLI
```

## Model architecture

| Component | Description |
|---|---|
| **Block embedding** | Each voxel class → 32-dim vector |
| **Text encoder** | Small Transformer (3 layers), trained jointly |
| **Denoiser** | 3D U-Net with time + text conditioning |
| **Diffusion** | DDPM, 200 timesteps, cosine beta schedule |
| **Guidance** | Classifier-free guidance at inference |

## Hardware

| Setup | Notes |
|---|---|
| **GPU (8GB+)** | Recommended. Batch size 8, ~32³ resolution |
| **CPU** | Works for testing; training will be very slow |
| **More data** | Quality scales with dataset size and diversity |

## Training tips

- Start with synthetic data to verify the pipeline, then add real builds
- Aim for **500+ diverse structures** before expecting good results
- Caption quality matters — describe materials, size, and style
- Monitor `checkpoints/logs/` in TensorBoard
- Increase `non_air_weight` if the model predicts too much air

## Limitations (v0.1)

- Fixed 32³ resolution (structures are center-cropped/padded)
- Block palette capped at 256 classes
- Early training produces noisy results — expect 50+ epochs for coherence
- Text encoder is simple; larger datasets benefit from more `text_dim` / layers
- **Scenes** (structure + terrain) are planned but not implemented yet — structure-only for now

## Roadmap: Scene generation (advanced)

The book's "Using the Land" chapter pairs builds with biomes. A future **scene model** would output:

1. **Structure region** — the building (current 32³ model)
2. **Terrain region** — grass, water, trees, paths matched to biome
3. **Combined `.litematic`** — multiple regions in one file

For now, mentioning a biome in your prompt enriches it with suitable build types
(e.g. `"haunted house in a roofed forest"` → dark forest, spooky build, decrepit temple).
Use `--prompt "... scene with terrain"` to see the planned scene mode notice.

## References

Inspired by research on voxel generation for Minecraft structures:
- [3D-Craft / VoxelCNN](https://openaccess.thecvf.com/content_ICCV_2019/papers/Chen_Order-Aware_Generative_Modeling_Using_the_3D-Craft_Dataset_ICCV_2019_paper.pdf)
- [Scaffold Diffusion](https://arxiv.org/html/2509.00062)
- [Dream-Cubed](https://arxiv.org/abs/2604.22847)
