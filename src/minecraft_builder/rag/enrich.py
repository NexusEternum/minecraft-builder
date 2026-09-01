"""Turn guide themes and retrieved passages into a short enriched prompt."""

from __future__ import annotations

import re
from pathlib import Path

from .store import GuideIndex, SearchResult
from .architecture import architecture_keywords, detect_architecture
from .banners import banner_keywords, detect_banners
from .biomes import biome_keywords, detect_biome
from .block_hacks import detect_hacks, hack_keywords
from .build_tips import detect_tips
from .color_theory import blocks_for_scheme, detect_color_scheme, wheel_blocks_for_hue
from .decor import decor_keywords, detect_decor
from .depth import depth_keywords, detect_depth_techniques
from .framework import framework_keywords
from .furniture import detect_furniture, furniture_keywords
from .interiors import detect_interior_decor, detect_wall_floor, interior_keywords
from .linking import linking_keywords
from .outdoors import (
  detect_custom_trees,
  detect_landscape,
  detect_outdoor_structures,
  outdoor_keywords,
)
from .redstone_lighting import detect_lighting_system, lighting_keywords
from .redstone_transport import detect_transport_system, transport_keywords
from .structure import detect_shape, shape_keywords
from .themed_rooms import detect_room, room_keywords
from .windows import detect_window_style, window_keywords

BUILD_TERMS = {
  "oak", "spruce", "birch", "jungle", "acacia", "dark oak", "mangrove", "cherry",
  "stone", "cobblestone", "stone bricks", "deepslate", "andesite", "diorite", "granite",
  "brick", "terracotta", "concrete", "glass", "wool", "planks", "log", "wood",
  "roof", "foundation", "wall", "tower", "cottage", "house", "castle", "barn",
  "medieval", "modern", "rustic", "cozy", "fantasy", "japanese", "viking",
  "window", "door", "chimney", "porch", "balcony", "stair", "pillar", "arch",
  "lantern", "torch", "banner", "fence", "trapdoor", "slab", "stairs",
  "symmetry", "depth", "detail", "palette", "accent", "frame", "trim",
  "steampunk", "industrial", "infernal", "classical", "historical", "monochromatic",
}

BLOCK_PATTERN = re.compile(
  r"\b(oak|spruce|birch|stone|cobblestone|brick|glass|plank|log|terracotta|concrete|wool|deepslate|quartz|prismarine|purpur|nether|obsidian|glowstone)\w*\b",
  re.IGNORECASE,
)


def enrich_prompt(
  prompt: str,
  index: GuideIndex | None = None,
  max_len: int = 128,
  top_k: int = 4,
  theme: str | None = None,
) -> tuple[str, list[SearchResult], list[Theme]]:
  """
  Enrich a prompt using book theme palettes and optional RAG retrieval.
  Returns (enriched_prompt, search_results, matched_themes).
  """
  results: list[SearchResult] = []
  themes = _resolve_themes(prompt, theme)

  keywords: list[str] = []
  seen: set[str] = set()
  prompt_lower = prompt.lower()

  # 1. Inject block palette from matched book themes
  for t in themes:
    _add_keywords(keywords, seen, prompt_lower, [t.name])
    for block in theme_block_names(t)[:4]:
      _add_keywords(keywords, seen, prompt_lower, [block])

  # 1b. Color theory from the aesthetics chapter
  scheme = detect_color_scheme(prompt)
  if scheme:
    _add_keywords(keywords, seen, prompt_lower, [scheme])
    for block in blocks_for_scheme(scheme):
      _add_keywords(keywords, seen, prompt_lower, [block])

  # 1c. Block hacks from the block hacks chapter
  for hack in detect_hacks(prompt):
    for kw in hack_keywords(hack)[:3]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1d. Biome → suitable build types ("Using the Land")
  biome = detect_biome(prompt)
  if biome:
    for kw in biome_keywords(biome)[:4]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1e. Natural features (rivers, temples, waterfalls, etc.)
  for feature in detect_features(prompt):
    for kw in feature_keywords(feature)[:3]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1f. Beginner build tips (depth, location fit, etc.)
  for tip in detect_tips(prompt):
    for kw in tip.keywords[:2]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1g. Adding depth techniques (stairs, slabs, double walls, bay windows)
  for tech in detect_depth_techniques(prompt):
    for kw in depth_keywords(tech)[:3]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1h. Structure shapes (rectangular, circle, pyramid, sphere)
  shape = detect_shape(prompt)
  if shape:
    for kw in shape_keywords(shape)[:3]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1i. Build framework (7-step construction process)
  for kw in framework_keywords(prompt)[:4]:
    _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1j. Architectural structures (arch, balcony, colonnade, etc.)
  for feature in detect_architecture(prompt):
    for kw in architecture_keywords(feature)[:3]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1k. Linking builds — multi-building scenes (roads, parks, fire escapes)
  for kw in linking_keywords(prompt)[:5]:
    _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1l. Functional decor and lighting
  for feature in detect_decor(prompt):
    for kw in decor_keywords(feature)[:3]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1m. Themed interior rooms (workshop, mystic lair, modern den)
  room = detect_room(prompt)
  if room:
    for kw in room_keywords(room)[:5]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1n. Window aesthetics (shaped, ornate, pictorial, glass buildings)
  for style in detect_window_style(prompt):
    for kw in window_keywords(style)[:2]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1o. Walls, floors, and interior decor
  for tech in detect_wall_floor(prompt):
    for kw in interior_keywords(tech)[:3]:
      _add_keywords(keywords, seen, prompt_lower, [kw])
  for decor in detect_interior_decor(prompt):
    for kw in interior_keywords(decor)[:3]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1p. Banners and flag displays (low priority — only when mentioned)
  for display in detect_banners(prompt):
    for kw in banner_keywords(display)[:2]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1q. Furniture hacks (interior detail — prompt hints only)
  for hack in detect_furniture(prompt)[:3]:
    for kw in furniture_keywords(hack)[:2]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1r. Outdoor spaces and landscaping (scenes)
  for item in (*detect_landscape(prompt), *detect_custom_trees(prompt), *detect_outdoor_structures(prompt)):
    for kw in outdoor_keywords(item)[:2]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1s. Redstone lighting (prompt hints only — circuits not generated)
  for system in detect_lighting_system(prompt):
    for kw in lighting_keywords(system)[:2]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # 1t. Redstone transport (prompt hints only — minecart logic not generated)
  for system in detect_transport_system(prompt):
    for kw in transport_keywords(system)[:2]:
      _add_keywords(keywords, seen, prompt_lower, [kw])

  # Detect hue words (e.g. "blue build") and pull wheel blocks
  for hue in ("red", "orange", "yellow", "green", "blue", "purple", "pink", "cyan", "teal"):
    if hue in prompt_lower:
      for block in wheel_blocks_for_hue(hue)[:2]:
        _add_keywords(keywords, seen, prompt_lower, [block])

  # 2. Retrieve passages from indexed guide text
  if index is not None:
    results = index.search(_theme_aware_query(prompt, themes), top_k=top_k)
    rag_keywords = _extract_keywords(prompt, results)
    for kw in rag_keywords:
      _add_keywords(keywords, seen, prompt_lower, [kw])

    # Detect themes mentioned in retrieved text but not in the prompt
    if not themes:
      retrieved_text = " ".join(r.chunk.text for r in results).lower()
      for t in THEMES.values():
        if any(alias in retrieved_text for alias in t.aliases):
          themes.append(t)
          for block in theme_block_names(t)[:3]:
            _add_keywords(keywords, seen, prompt_lower, [block])

  if not keywords:
    if results:
      snippet = _shorten(results[0].chunk.text, max_words=10)
      return _join_prompt(prompt, snippet, max_len), results, themes
    return prompt, results, themes

  keyword_str = ", ".join(keywords[:8])
  return _join_prompt(prompt, keyword_str, max_len), results, themes


def load_index(index_dir: Path) -> GuideIndex:
  return GuideIndex.load(index_dir)


def _resolve_themes(prompt: str, explicit_theme: str | None) -> list[Theme]:
  if explicit_theme:
    key = explicit_theme.lower().replace(" ", "_")
    if key in THEMES:
      return [THEMES[key]]
    # Fuzzy match on aliases
    for theme in THEMES.values():
      if explicit_theme.lower() in theme.aliases or explicit_theme.lower() == theme.name:
        return [theme]
  return detect_themes(prompt)


def _theme_aware_query(prompt: str, themes: list[Theme]) -> str:
  if not themes:
    return prompt
  theme_names = " ".join(t.name for t in themes)
  return f"{prompt} {theme_names} palette blocks materials"


def _add_keywords(keywords: list[str], seen: set[str], prompt_lower: str, candidates: list[str]) -> None:
  for word in candidates:
    w = word.lower()
    if w not in prompt_lower and w not in seen:
      keywords.append(word)
      seen.add(w)


def _extract_keywords(prompt: str, results: list[SearchResult]) -> list[str]:
  found: list[str] = []
  seen: set[str] = set()
  combined = " ".join(r.chunk.text for r in results).lower()
  prompt_lower = prompt.lower()

  for term in BUILD_TERMS:
    if term in combined and term not in prompt_lower and term not in seen:
      found.append(term)
      seen.add(term)

  for match in BLOCK_PATTERN.finditer(combined):
    word = match.group(0).lower()
    if word not in prompt_lower and word not in seen:
      found.append(word)
      seen.add(word)

  return found


def _shorten(text: str, max_words: int) -> str:
  words = text.split()
  return " ".join(words[:max_words]).rstrip(".,;:")


def _join_prompt(prompt: str, addition: str, max_len: int) -> str:
  if not addition:
    return prompt[:max_len]
  combined = f"{prompt}, {addition}"
  if len(combined) <= max_len:
    return combined
  budget = max_len - len(prompt) - 2
  if budget <= 0:
    return prompt[:max_len]
  return f"{prompt}, {addition[:budget].rstrip(' ,')}"
