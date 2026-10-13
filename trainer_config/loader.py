"""Profile loader — YAML files under trainer_config/profiles/."""
from __future__ import annotations

from pathlib import Path

import yaml

from trainer_config.schema import Profile

PROFILE_DIR = Path(__file__).parent / "profiles"


def list_profiles() -> list[str]:
    return sorted(p.stem for p in PROFILE_DIR.glob("*.yaml"))


def load_profile(name: str) -> Profile:
    path = PROFILE_DIR / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Profile(**raw)