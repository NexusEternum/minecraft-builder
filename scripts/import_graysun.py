"""Import Graysun .litematic schematics from Downloads into data/raw/."""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

DOWNLOADS = Path.home() / "Downloads"
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
CAPTIONS_PATH = Path(__file__).resolve().parents[1] / "data" / "captions.json"


def slug(text: str) -> str:
  text = re.sub(r"[^a-zA-Z0-9]+", "_", text.strip())
  text = re.sub(r"_+", "_", text).strip("_")
  return text.lower()[:48] or "build"


def humanize(text: str) -> str:
  text = re.sub(r"[_\-]+", " ", text)
  text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
  text = re.sub(r"\s+", " ", text).strip().lower()
  return text


def strip_zip(name: str) -> str:
  return name[:-4] if name.lower().endswith(".zip") else name


def pack_label(zip_name: str) -> str:
  base = strip_zip(zip_name)
  base = re.sub(r"\s*\(\d+\)$", "", base)
  return humanize(base)


def build_caption(pack: str, stem: str) -> str:
  pack_words = pack_label(pack)
  build_words = humanize(stem)
  if "tree" in pack_words or "tree" in build_words:
    kind = "tree"
  elif "village" in pack_words or "revamp" in pack_words:
    kind = "village building"
  else:
    kind = "house"
  return (
    f"a graysun {pack_words} {build_words} minecraft {kind}, "
    "detailed exterior and interior, survival build"
  )


def zip_paths() -> list[Path]:
  all_zips = sorted(DOWNLOADS.glob("*.zip"), key=lambda p: p.stat().st_mtime)
  skip: set[str] = set()
  names = {p.name for p in all_zips}
  for name in names:
    if re.search(r"\s\(\d+\)\.zip$", name):
      base = re.sub(r"\s\(\d+\)\.zip$", ".zip", name)
      if base in names:
        skip.add(name)
  return [p for p in all_zips if p.name not in skip]


def iter_litematic_members(zf: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
  return [
    info
    for info in zf.infolist()
    if not info.is_dir() and info.filename.lower().endswith(".litematic")
  ]


def main() -> None:
  RAW_DIR.mkdir(parents=True, exist_ok=True)
  captions: dict[str, str] = {}
  if CAPTIONS_PATH.exists():
    captions = json.loads(CAPTIONS_PATH.read_text(encoding="utf-8"))

  seen_stems: set[str] = set()
  imported = 0
  skipped_dup = 0
  errors: list[str] = []

  for zip_path in zip_paths():
    pack = zip_path.name
    pack_slug = slug(strip_zip(pack))
    try:
      with zipfile.ZipFile(zip_path) as zf:
        for info in iter_litematic_members(zf):
          stem = Path(info.filename).stem
          norm = slug(stem)
          if norm in seen_stems:
            skipped_dup += 1
            continue
          seen_stems.add(norm)

          out_name = f"graysun_{pack_slug}_{slug(stem)}.litematic"
          out_path = RAW_DIR / out_name
          with zf.open(info) as src, open(out_path, "wb") as dst:
            dst.write(src.read())

          cap = build_caption(pack, stem)
          captions[out_name] = cap
          captions[f"{out_path.stem}.npz"] = cap
          imported += 1
    except Exception as exc:
      errors.append(f"{pack}: {exc}")

  CAPTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
  CAPTIONS_PATH.write_text(json.dumps(captions, indent=2, sort_keys=True), encoding="utf-8")

  print(f"Imported: {imported} litematic -> {RAW_DIR}")
  print(f"Skipped duplicate stems: {skipped_dup}")
  print(f"Captions total: {len(captions)}")
  if errors:
    print(f"Errors ({len(errors)}):")
    for err in errors[:10]:
      print(f"  {err}")


if __name__ == "__main__":
  main()
