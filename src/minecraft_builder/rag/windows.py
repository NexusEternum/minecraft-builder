"""
Window aesthetics from Aesthetic Decor (Minecraft Guide to Creative).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WindowStyle:
  id: str
  name: str
  aliases: tuple[str, ...]
  blocks: tuple[str, ...]
  tip: str


def _b(name: str) -> str:
  if name.startswith("minecraft:"):
    return name
  return f"minecraft:{name}"


WINDOW_STYLES: tuple[WindowStyle, ...] = (
  WindowStyle(
    id="shaped",
    name="shaped windows",
    aliases=("shaped window", "circular window", "round window", "diamond window", "non-rectangular"),
    blocks=(_b("glass_pane"), _b("sandstone")),
    tip="Windows don't have to be rectangular — use circles and diamonds",
  ),
  WindowStyle(
    id="ornate",
    name="ornate windows",
    aliases=("ornate window", "gothic window", "arched window", "cathedral window", "castle window"),
    blocks=(_b("glass_pane"), _b("stone_brick_stairs"), _b("chiseled_stone_bricks")),
    tip="Intricate arched patterns for castles, temples, and extravagant builds",
  ),
  WindowStyle(
    id="glass_panes",
    name="inset glass panes",
    aliases=("glass pane", "recessed window", "thin window"),
    blocks=(_b("glass_pane"),),
    tip="Panes sit inset in the wall; blocks sit flush with the outer edge",
  ),
  WindowStyle(
    id="pictorial",
    name="pictorial windows",
    aliases=("pictorial", "pixel art window", "stained glass art", "flower window", "mosaic window"),
    blocks=(_b("stained_glass"), _b("yellow_stained_glass"), _b("white_stained_glass")),
    tip="Stained glass blocks arranged as pixel art in the wall",
  ),
  WindowStyle(
    id="glass_building",
    name="glass building",
    aliases=("glass building", "glass tower", "glass facade", "skyscraper", "modern glass"),
    blocks=(_b("glass"), _b("light_gray_stained_glass"), _b("quartz_block")),
    tip="Glass majority exterior for modern spacious bright buildings",
  ),
  WindowStyle(
    id="coloured_glass",
    name="coloured glass bands",
    aliases=("coloured glass", "colored glass", "tinted glass", "glass bands", "stained facade"),
    blocks=(_b("stained_glass_pane"), _b("orange_stained_glass"), _b("blue_stained_glass")),
    tip="Coloured glass panes and blocks to add colour to walls and facades",
  ),
)


def detect_window_style(prompt: str) -> list[WindowStyle]:
  lower = prompt.lower()
  matched: list[WindowStyle] = []
  seen: set[str] = set()

  # Generic window mention → panes + one style if specific
  has_window = "window" in lower or "glass" in lower

  for style in WINDOW_STYLES:
    for alias in sorted(style.aliases, key=len, reverse=True):
      if alias in lower and style.id not in seen:
        matched.append(style)
        seen.add(style.id)
        break

  if not matched and has_window:
    matched.append(WINDOW_STYLES[2])  # default to inset panes

  return matched


def window_keywords(style: WindowStyle) -> list[str]:
  blocks = [b.removeprefix("minecraft:").replace("_", " ") for b in style.blocks[:2]]
  return [style.name, *blocks]
