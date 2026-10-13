"""Global hotkey dispatcher — binds handler hotkeys to the keyboard module."""
from __future__ import annotations

from typing import TYPE_CHECKING

import keyboard

from trainer_utils.logging_setup import get_logger

if TYPE_CHECKING:
    from trainer_core.engine import TrainerEngine

log = get_logger(__name__)


class HotkeyService:
    def __init__(self, engine: "TrainerEngine") -> None:
        self.engine = engine
        self._handles: list[object] = []

    def start(self) -> None:
        for name, handler in self.engine.handlers.items():
            for combo, cb in handler.hotkeys().items():  # type: ignore[attr-defined]
                h = keyboard.add_hotkey(combo, cb, suppress=False)
                self._handles.append(h)
                log.debug("bound %s -> %s", combo, name)
        log.info("hotkey service started (%d bindings)", len(self._handles))

    def stop(self) -> None:
        for h in self._handles:
            try:
                keyboard.remove_hotkey(h)
            except Exception:
                log.debug("remove_hotkey failed", exc_info=True)
        self._handles.clear()