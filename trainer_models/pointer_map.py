"""PointerMap — reads a JSON map of {symbol: [base_offset, off1, off2...]}.

A pointer map is the difference between "this trainer only works on one
build" and "this trainer works across patches". Each entry names a
symbol, a module-relative base, and a chain of offsets to dereference.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from trainer_core.process import ProcessHandle
from trainer_utils.logging_setup import get_logger

log = get_logger(__name__)


@dataclass(frozen=True)
class PointerEntry:
    symbol: str
    module: str
    base_offset: int
    offsets: tuple[int, ...]


class PointerMap:
    def __init__(self, slug: str, entries: list[PointerEntry]) -> None:
        self.slug = slug
        self.entries = entries
        self._by_symbol = {e.symbol: e for e in entries}

    @classmethod
    def from_file(cls, path: Path) -> "PointerMap":
        raw = json.loads(path.read_text(encoding="utf-8"))
        slug = raw.get("slug", path.stem)
        entries = [
            PointerEntry(
                symbol=e["symbol"],
                module=e.get("module", "Game.exe"),
                base_offset=int(e["base_offset"], 0),
                offsets=tuple(int(o, 0) for o in e.get("offsets", [])),
            )
            for e in raw["entries"]
        ]
        return cls(slug=slug, entries=entries)

    def resolve(self, symbol: str, proc: ProcessHandle) -> int | None:
        entry = self._by_symbol.get(symbol)
        if entry is None:
            return None
        from trainer_core.memory import module_bounds

        bounds = module_bounds(proc, entry.module)
        addr = bounds.base + entry.base_offset
        for off in entry.offsets:
            addr = proc.read_pointer(addr) + off
        return addr