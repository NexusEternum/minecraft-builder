"""
Structure shapes from the Minecraft Guide to Creative.

Foundation shapes and circle templates for planning builds.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StructureShape:
  id: str
  name: str
  aliases: tuple[str, ...]
  keywords: tuple[str, ...]
  circle_sizes: tuple[int, ...]  # for round shapes
  tip: str


STRUCTURE_SHAPES: dict[str, StructureShape] = {
  "quadrilateral": StructureShape(
    id="quadrilateral",
    name="rectangular",
    aliases=("rectangular", "rectangle", "square", "box", "room", "house", "building"),
    keywords=("rectangular base", "four-sided", "flat walls"),
    circle_sizes=(),
    tip="Easiest shape — rectangular bases, rooms, and flat walls",
  ),
  "triangle": StructureShape(
    id="triangle",
    name="triangular",
    aliases=("a-frame", "a frame", "gabled", "gable", "pitched roof", "triangular"),
    keywords=("a-frame roof", "gabled roof", "triangular"),
    circle_sizes=(),
    tip="Triangles for roofs and A-frame builds; diagonal walls are harder inside",
  ),
  "circle": StructureShape(
    id="circle",
    name="circular",
    aliases=("circle", "circular", "round", "tower", "octagonal", "cylinder"),
    keywords=("circular base", "round tower", "octagonal"),
    circle_sizes=(5, 7, 9, 11),
    tip="Use 5x5, 7x7, 9x9, or 11x11 circle templates from the book",
  ),
  "pyramid": StructureShape(
    id="pyramid",
    name="pyramid",
    aliases=("pyramid", "ziggurat", "stepped"),
    keywords=("pyramid", "stepped base", "square pyramid"),
    circle_sizes=(),
    tip="Start with a large square base and step inward as you build up",
  ),
  "triangular_prism": StructureShape(
    id="triangular_prism",
    name="triangular prism",
    aliases=("tent", "attic", "prism", "long roof", "warehouse roof"),
    keywords=("triangular prism", "tent shape", "attic"),
    circle_sizes=(),
    tip="Like a pyramid but elongated — good for attics and tents",
  ),
  "sphere": StructureShape(
    id="sphere",
    name="sphere",
    aliases=("sphere", "spherical", "dome", "orb", "globe", "futuristic"),
    keywords=("sphere", "dome", "round structure"),
    circle_sizes=(5, 7, 9, 11, 11, 11, 9, 7, 5),
    tip="Stack circles 5→7→9→11→11 then back down for a sphere",
  ),
}


def detect_shape(prompt: str) -> StructureShape | None:
  lower = prompt.lower()
  matches: list[tuple[int, StructureShape]] = []
  for shape in STRUCTURE_SHAPES.values():
    for alias in shape.aliases:
      if alias in lower:
        matches.append((len(alias), shape))
        break
  if not matches:
    return None
  matches.sort(key=lambda x: x[0], reverse=True)
  return matches[0][1]


def shape_keywords(shape: StructureShape) -> list[str]:
  kws = [shape.name, *list(shape.keywords[:2])]
  if shape.circle_sizes:
    sizes = " ".join(f"{s}x{s}" for s in shape.circle_sizes[:4])
    kws.append(f"circle guide {sizes}")
  return kws
