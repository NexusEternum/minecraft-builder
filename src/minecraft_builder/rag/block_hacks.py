"""
Block hacks from the Minecraft Guide to Creative (Block Hacks chapter).

Techniques for using blocks in unexpected ways. Enriches prompts with
technique keywords when relevant build features are mentioned.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BlockHack:
  id: str
  name: str
  blocks: tuple[str, ...]
  triggers: tuple[str, ...]
  tip: str


def _b(name: str) -> str:
  if name.startswith("minecraft:"):
    return name
  return f"minecraft:{name}"


BLOCK_HACKS: tuple[BlockHack, ...] = (
  BlockHack(
    id="stairs_roof",
    name="stair roof",
    blocks=(_b("oak_stairs"), _b("dark_oak_stairs"), _b("stone_brick_stairs")),
    triggers=("roof", "rooftop", "shingle", "tiling", "lodge", "cabin", "cottage"),
    tip="Use stairs for staggered roof tiling — works in wood and stone",
  ),
  BlockHack(
    id="cobblestone_wall_supports",
    name="cobblestone wall supports",
    blocks=(_b("cobblestone_wall"),),
    triggers=("balcony", "lookout", "tower", "raised", "perimeter", "boundary", "support", "platform"),
    tip="Cobblestone walls work as pillars for balconies and lookouts",
  ),
  BlockHack(
    id="fence_railings",
    name="fence railings",
    blocks=(_b("oak_fence"), _b("spruce_fence"), _b("dark_oak_fence")),
    triggers=("balcony", "stairs", "staircase", "railing", "ledge", "walkway", "deck"),
    tip="Line stairs, balconies, and roofs with fences to prevent falls",
  ),
  BlockHack(
    id="cobweb_smoke",
    name="cobweb chimney smoke",
    blocks=(_b("cobweb"),),
    triggers=("chimney", "fireplace", "fire", "smoke", "cozy", "hearth"),
    tip="Place cobwebs above chimneys to simulate billowing smoke",
  ),
  BlockHack(
    id="trapdoor_shutters",
    name="trapdoor shutters",
    blocks=(_b("oak_trapdoor"), _b("spruce_trapdoor"), _b("dark_oak_trapdoor")),
    triggers=("window", "shutter", "rustic", "cottage", "farmhouse", "exterior"),
    tip="Trapdoors beside windows make openable rustic shutters",
  ),
  BlockHack(
    id="medieval_torch",
    name="medieval wall torch",
    blocks=(_b("torch"), _b("item_frame"), _b("stone_slab")),
    triggers=("torch", "light", "lighting", "medieval", "wall mount", "lantern", "exterior"),
    tip="Torch + item frame + stone slab = medieval wall-mounted torch",
  ),
  BlockHack(
    id="indoor_shrub",
    name="indoor shrub",
    blocks=(_b("oak_fence"), _b("oak_leaves")),
    triggers=("interior", "inside", "decor", "decoration", "plant", "shrub", "furniture"),
    tip="Fence pole with a leaf block on top makes a quaint indoor shrub",
  ),
)


def detect_hacks(prompt: str) -> list[BlockHack]:
  """Return block hacks relevant to the prompt."""
  lower = prompt.lower()
  matched: list[BlockHack] = []
  seen: set[str] = set()

  for hack in BLOCK_HACKS:
    if any(trigger in lower for trigger in hack.triggers):
      if hack.id not in seen:
        matched.append(hack)
        seen.add(hack.id)

  return matched


def hack_keywords(hack: BlockHack) -> list[str]:
  """Human-readable keywords to append to a prompt."""
  names = [b.removeprefix("minecraft:").replace("_", " ") for b in hack.blocks[:3]]
  return [hack.name] + names
