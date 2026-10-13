"""Profile schema — validated with pydantic v2."""
from __future__ import annotations

from pydantic import BaseModel, Field


class Profile(BaseModel):
    name: str
    process_name: str = Field(..., description="e.g. 'EldenRing.exe'")
    tick_hz: int = Field(30, ge=1, le=240)
    pointer_map: str | None = Field(None, description="Override slug for pointer map file")
    enabled_by_default: list[str] = Field(default_factory=list)
    notes: str | None = None