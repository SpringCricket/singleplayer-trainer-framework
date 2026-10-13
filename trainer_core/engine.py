"""TrainerEngine — owns handlers, pointer maps, and the main loop.

Handlers are registered by name. Each handler exposes:
    enable() / disable() / tick() / hotkeys() -> dict[str, Callable]
The engine ticks all enabled handlers at `profile.tick_hz`.
"""
from __future__ import annotations

import time
from collections.abc import Callable

from trainer_config.schema import Profile
from trainer_core.process import ProcessHandle
from trainer_models.pointer_map import PointerMap
from trainer_services.scan_service import ScanService
from trainer_utils.logging_setup import get_logger

log = get_logger(__name__)


class TrainerEngine:
    def __init__(self, process: ProcessHandle, scan: ScanService, profile: Profile) -> None:
        self.process = process
        self.scan = scan
        self.profile = profile
        self.pointer_maps: dict[str, PointerMap] = {}
        self.handlers: dict[str, object] = {}
        self._running = False

    def load_pointer_maps(self, game_slug: str) -> None:
        from pointer_maps import load_map_for_slug

        pm = load_map_for_slug(game_slug)
        self.pointer_maps[game_slug] = pm
        log.info("loaded %d pointer entries for %s", len(pm.entries), game_slug)

    def register_default_handlers(self) -> None:
        from feature_handlers.registry import build_default_handlers

        for handler in build_default_handlers(self):
            self.register(handler)

    def register(self, handler: object) -> None:
        name = getattr(handler, "name", handler.__class__.__name__)
        self.handlers[name] = handler
        log.debug("registered handler: %s", name)

    def resolve(self, symbol: str) -> int:
        """Resolve a symbol name to an absolute address via loaded pointer maps."""
        for pm in self.pointer_maps.values():
            addr = pm.resolve(symbol, self.process)
            if addr:
                return addr
        raise KeyError(f"symbol not found in any pointer map: {symbol}")

    def serve_forever(self) -> None:
        self._running = True
        interval = 1.0 / max(1, self.profile.tick_hz)
        while self._running:
            t0 = time.perf_counter()
            for name, handler in self.handlers.items():
                if getattr(handler, "enabled", False):
                    try:
                        handler.tick()  # type: ignore[attr-defined]
                    except Exception:
                        log.exception("handler %s tick failed", name)
            elapsed = time.perf_counter() - t0
            time.sleep(max(0.0, interval - elapsed))

    def toggle(self, handler_name: str) -> None:
        h = self.handlers.get(handler_name)
        if h is None:
            log.warning("no such handler: %s", handler_name)
            return
        enabled = getattr(h, "enabled", False)
        setattr(h, "enabled", not enabled)
        log.info("handler %s -> %s", handler_name, "ON" if not enabled else "OFF")

    def shutdown(self) -> None:
        self._running = False
        for h in self.handlers.values():
            try:
                if getattr(h, "enabled", False):
                    h.disable()  # type: ignore[attr-defined]
            except Exception:
                log.exception("handler disable failed")
        self.process.close()