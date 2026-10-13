"""Pointer map loader — reads JSON maps keyed by game slug."""
from __future__ import annotations

from pathlib import Path

from trainer_models.pointer_map import PointerMap

MAP_DIR = Path(__file__).parent


def load_map_for_slug(slug: str) -> PointerMap:
    path = MAP_DIR / f"{slug}.json"
    if not path.exists():
        raise FileNotFoundError(f"no pointer map for slug '{slug}' at {path}")
    return PointerMap.from_file(path)