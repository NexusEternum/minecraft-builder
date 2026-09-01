#!/usr/bin/env bash
# One-shot setup + train on a RunPod GPU pod (PyTorch template).
# Usage: bash scripts/runpod_train.sh
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> Python: $(python --version)"
python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'none')"

echo "==> Installing package"
pip install -e . --pre -q

echo "==> Preprocessing (200 synthetic + 34 book builds)"
python -m minecraft_builder.scripts.preprocess --synthetic 200

echo "==> Training on H100 config"
python -m minecraft_builder.train --config configs/runpod_h100.yaml

echo "==> Done. Checkpoints in checkpoints/"
