"""Signature — a named AOB pattern with a mask, loaded from TOML."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Signature:
    name: str
    pattern: bytes
    mask: bytes

    @classmethod
    def from_toml(cls, path: Path) -> list["Signature"]:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
        out: list[Signature] = []
        for entry in raw.get("signature", []):
            pat_str = entry["pattern"].replace(" ", "")
            mask = bytearray()
            pattern = bytearray()
            for i in range(0, len(pat_str), 2):
                tok = pat_str[i : i + 2]
                if tok == "??":
                    pattern.append(0)
                    mask.append(0x00)
                else:
                    pattern.append(int(tok, 16))
                    mask.append(0xFF)
            out.append(cls(name=entry["name"], pattern=bytes(pattern), mask=bytes(mask)))
        return out