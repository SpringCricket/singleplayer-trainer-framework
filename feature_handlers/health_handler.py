"""Health / godmode handler — pins player HP to a max value each tick."""
from __future__ import annotations

from feature_handlers.base import FeatureHandler
from trainer_utils.logging_setup import get_logger

log = get_logger(__name__)


class HealthHandler(FeatureHandler):
    name = "godmode"
    default_hotkey = "f1"

    def enable(self) -> None:
        self._addr = self.engine.resolve("player.health")
        self._max = self.engine.resolve("player.health_max")
        log.info("godmode on @ 0x%X", self._addr)

    def disable(self) -> None:
        log.info("godmode off")

    def tick(self) -> None:
        cap = self.engine.process.read_int32(self._max)
        self.engine.process.write_int32(self._addr, cap)