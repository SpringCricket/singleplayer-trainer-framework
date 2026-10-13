"""Handler registry — where every feature in the framework gets wired in."""
from __future__ import annotations

from typing import TYPE_CHECKING

from feature_handlers.ammo_handler import AmmoHandler
from feature_handlers.health_handler import HealthHandler
from feature_handlers.speed_handler import SpeedHandler
from feature_handlers.teleport_handler import TeleportHandler

if TYPE_CHECKING:
    from trainer_core.engine import TrainerEngine


def build_default_handlers(engine: "TrainerEngine") -> list[object]:
    return [
        HealthHandler(engine),
        AmmoHandler(engine),
        SpeedHandler(engine),
        TeleportHandler(engine),
    ]


def handler_manifest() -> dict[str, str]:
    return {
        "godmode": "pins HP to max",
        "inf_ammo": "fills clip + reserve",
        "speedhack": "movement multiplier",
        "teleport": "save/warp XYZ (F5/F6)",
    }