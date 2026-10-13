"""ProcessHandle — thin wrapper over pymem for a single target process.

Only one handle per session. All reads/writes go through here so we can
log and (optionally) rate-limit. pymem opens with PROCESS_ALL_ACCESS by
default; on some protected games you'll need to run as admin.
"""
from __future__ import annotations

import struct
from dataclasses import dataclass

import pymem

from trainer_utils.logging_setup import get_logger

log = get_logger(__name__)


@dataclass
class ProcessHandle:
    pid: int
    base_address: int
    _pm: pymem.Pymem

    @classmethod
    def attach(cls, process_name: str) -> "ProcessHandle":
        pm = pymem.Pymem(process_name)
        base = pm.base_address
        log.info("attached to %s pid=%d base=0x%X", process_name, pm.process_id, base)
        return cls(pid=pm.process_id, base_address=base, _pm=pm)

    def read_bytes(self, address: int, size: int) -> bytes:
        return self._pm.read_bytes(address, size)

    def read_int32(self, address: int) -> int:
        return struct.unpack("<i", self.read_bytes(address, 4))[0]

    def read_float(self, address: int) -> float:
        return struct.unpack("<f", self.read_bytes(address, 4))[0]

    def write_bytes(self, address: int, data: bytes) -> None:
        self._pm.write_bytes(address, data, len(data))

    def write_int32(self, address: int, value: int) -> None:
        self.write_bytes(address, struct.pack("<i", value))

    def write_float(self, address: int, value: float) -> None:
        self.write_bytes(address, struct.pack("<f", value))

    def read_pointer(self, address: int) -> int:
        return struct.unpack("<Q", self.read_bytes(address, 8))[0]

    def close(self) -> None:
        try:
            self._pm.close_process()
        except Exception:
            log.debug("close_process raised (already closed?)", exc_info=True)