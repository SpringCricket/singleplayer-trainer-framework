"""TrainerSession — the top-level lifecycle object.

Owns: process attach, engine construction, handler registration, hotkey
dispatcher start/stop, and clean detach. One session per process.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from rich.console import Console

from trainer_config.schema import Profile
from trainer_core.engine import TrainerEngine
from trainer_core.process import ProcessHandle
from trainer_services.hotkey_service import HotkeyService
from trainer_services.scan_service import ScanService
from trainer_utils.logging_setup import get_logger

log = get_logger(__name__)
console = Console()


@dataclass
class TrainerSession:
    game_slug: str
    profile: Profile
    enable_hotkeys: bool = True
    _engine: TrainerEngine | None = field(default=None, repr=False)
    _hotkeys: HotkeyService | None = field(default=None, repr=False)

    def attach(self) -> None:
        proc = ProcessHandle.attach(self.profile.process_name)
        console.print(f"[green]attached[/green] pid={proc.pid} base=0x{proc.base_address:X}")
        scan = ScanService(proc)
        self._engine = TrainerEngine(process=proc, scan=scan, profile=self.profile)
        self._engine.load_pointer_maps(self.game_slug)
        self._engine.register_default_handlers()

    def run(self) -> None:
        if self._engine is None:
            raise RuntimeError("session not attached")
        if self.enable_hotkeys:
            self._hotkeys = HotkeyService(engine=self._engine)
            self._hotkeys.start()
        console.print("[bold cyan]trainer live[/bold cyan] — Ctrl+C to detach")
        self._engine.serve_forever()

    def detach(self) -> None:
        if self._hotkeys is not None:
            self._hotkeys.stop()
        if self._engine is not None:
            self._engine.shutdown()
        log.info("session detached")