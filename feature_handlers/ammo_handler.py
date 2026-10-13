"""Infinite ammo handler — writes clip + reserve to a fixed value.

Note: some engines re-read reserve from a different struct on reload;
if ammo still drops, add `weapon.reserve_alt` to the pointer map.
"""
from __future__ import annotations

from feature_handlers.base import FeatureHandler
from trainer_utils.logging_setup import get_logger

log = get_logger(__name__)


class AmmoHandler(FeatureHandler):
    name = "inf_ammo"
    default_hotkey = "f2"
    FILL = 999

    def enable(self) -> None:
        self._clip = self.engine.resolve("weapon.clip")
        self._reserve = self.engine.resolve("weapon.reserve")
        log.info("inf ammo on")

    def disable(self) -> None:
        log.info("inf ammo off")

    def tick(self) -> None:
        proc = self.engine.process
        if proc.read_int32(self._clip) < self.FILL:
            proc.write_int32(self._clip, self.FILL)
        if proc.read_int32(self._reserve) < self.FILL:
            proc.write_int32(self._reserve, self.FILL)