"""Low-level memory helpers — AOB scanning, module bounds, region enumeration."""
from __future__ import annotations

from dataclasses import dataclass

from trainer_core.process import ProcessHandle
from trainer_utils.logging_setup import get_logger

log = get_logger(__name__)


@dataclass(frozen=True)
class ModuleBounds:
    name: str
    base: int
    size: int

    @property
    def end(self) -> int:
        return self.base + self.size


def module_bounds(proc: ProcessHandle, module_name: str) -> ModuleBounds:
    mod = proc._pm.read_module(module_name)  # type: ignore[attr-defined]
    return ModuleBounds(name=mod.name, base=mod.lpBaseOfDll, size=mod.SizeOfImage)


def aob_scan(proc: ProcessHandle, pattern: bytes, mask: bytes, bounds: ModuleBounds) -> int | None:
    """Scan a module for a byte pattern. mask uses 0xFF for exact, 0x00 for wildcard.

    Returns the absolute address of the first match, or None.
    """
    chunk = 0x10000
    overlap = len(pattern) - 1
    addr = bounds.base
    tail = b""
    while addr < bounds.end:
        size = min(chunk, bounds.end - addr)
        try:
            block = tail + proc.read_bytes(addr - len(tail), size + len(tail))
        except Exception:
            addr += size
            tail = b""
            continue
        for i in range(len(block) - len(pattern) + 1):
            ok = True
            for j, m in enumerate(mask):
                if m == 0xFF and block[i + j] != pattern[j]:
                    ok = False
                    break
            if ok:
                return addr - len(tail) + i
        tail = block[-(overlap):] if overlap else b""
        addr += size
    return None