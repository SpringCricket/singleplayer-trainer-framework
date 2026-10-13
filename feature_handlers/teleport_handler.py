"""Teleport handler — writes a saved XYZ to the player position.

Hotkey layout: F5 saves current pos, F6 warps to saved pos.
"""
from __future__ import annotations

from feature_handlers.base import FeatureHandler
from trainer_utils.logging_setup import get_logger

log = get_logger(__name__)


class TeleportHandler(FeatureHandler):
    name = "teleport"
    default_hotkey = None  # bound explicitly in hotkeys()

    def __init__(self, engine) -> None:  # type: ignore[no-untyped-def]
        super().__init__(engine)
        self._saved: tuple[float, float, float] | None = None

    def enable(self) -> None:
        self._x = self.engine.resolve("player.pos_x")
        self._y = self.engine.resolve("player.pos_y")
        self._z = self.engine.resolve("player.pos_z")
        log.info("teleport ready (F5 save / F6 warp)")

    def disable(self) -> None:
        log.info("teleport off")

    def save(self) -> None:
        p = self.engine.process
        self._saved = (p.read_float(self._x), p.read_float(self._y), p.read_float(self._z))
        log.info("saved pos %s", self._saved)

    def warp(self) -> None:
        if self._saved is None:
            log.warning("no saved position")
            return
        p = self.engine.process
        p.write_float(self._x, self._saved[0])
        p.write_float(self._y, self._saved[1])
        p.write_float(self._z, self._saved[2])

    def hotkeys(self):  # type: ignore[no-untyped-def]
        return {"f5": self.save, "f6": self.warp}