"""Movement speed multiplier — scales player velocity each tick."""
from __future__ import annotations

from feature_handlers.base import FeatureHandler
from trainer_utils.logging_setup import get_logger

log = get_logger(__name__)


class SpeedHandler(FeatureHandler):
    name = "speedhack"
    default_hotkey = "f3"

    def __init__(self, engine) -> None:  # type: ignore[no-untyped-def]
        super().__init__(engine)
        self.multiplier = 2.0

    def enable(self) -> None:
        self._vx = self.engine.resolve("player.vel_x")
        self._vy = self.engine.resolve("player.vel_y")
        log.info("speedhack on x%.2f", self.multiplier)

    def disable(self) -> None:
        log.info("speedhack off")

    def tick(self) -> None:
        proc = self.engine.process
        proc.write_float(self._vx, proc.read_float(self._vx) * self.multiplier)
        proc.write_float(self._vy, proc.read_float(self._vy) * self.multiplier)