#!/usr/bin/env bash
# One-shot setup + train on a RunPod GPU pod (PyTorch template).
# Usage: bash scripts/runpod_train.sh [--resume CHECKPOINT]
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> Python: $(python --version)"
python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'none')"

echo "==> Installing package (includes sentence-transformers)"
pip install -e . --pre -q

echo "==> Downloading pretrained text encoder (first run only)"
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

echo "==> Preprocessing (book builds + raw schematics @ 32³, no synthetic)"
python -m minecraft_builder.scripts.preprocess --config configs/runpod_h100.yaml --synthetic 0 --book-builds

RESUME_ARG=""
if [ "${1:-}" = "--resume" ] && [ -n "${2:-}" ]; then
  RESUME_ARG="--resume $2"
fi

echo "==> Training on H100 config (pretrained text encoder, frozen)"
python -m minecraft_builder.train --config configs/runpod_h100.yaml $RESUME_ARG

echo "==> Done. Checkpoints in checkpoints/"
