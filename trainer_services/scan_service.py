"""ScanService — wraps memory scanning with a small in-memory cache.

Used by handlers that need to resolve a symbol at enable-time and cache
the result. Pointer maps that change mid-session can be invalidated
via `invalidate()`.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from trainer_core.process import ProcessHandle
from trainer_utils.logging_setup import get_logger

log = get_logger(__name__)


@dataclass
class ScanService:
    process: ProcessHandle
    _cache: dict[str, int] = field(default_factory=dict)

    def cached(self, key: str) -> int | None:
        return self._cache.get(key)

    def remember(self, key: str, address: int) -> None:
        self._cache[key] = address

    def invalidate(self) -> None:
        self._cache.clear()