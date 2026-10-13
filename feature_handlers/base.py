"""FeatureHandler — the contract every trainer feature implements."""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from trainer_core.engine import TrainerEngine


class FeatureHandler(ABC):
    name: str = "unnamed"
    default_hotkey: str | None = None

    def __init__(self, engine: "TrainerEngine") -> None:
        self.engine = engine
        self.enabled = False

    @abstractmethod
    def enable(self) -> None: ...

    @abstractmethod
    def disable(self) -> None: ...

    def tick(self) -> None:
        """Called every engine tick while enabled. Override for continuous writes."""
        return None

    def hotkeys(self) -> dict[str, Callable[[], None]]:
        """Return {hotkey_string: callable}. Called once at registration."""
        if self.default_hotkey is None:
            return {}
        return {self.default_hotkey: lambda: self.engine.toggle(self.name)}