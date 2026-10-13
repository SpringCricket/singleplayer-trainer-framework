"""Logging — file + stderr, single init per process."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

_LOGGER_INIT = False


def init_logging(verbose: bool = False) -> None:
    global _LOGGER_INIT
    if _LOGGER_INIT:
        return
    logs = Path("logs")
    logs.mkdir(exist_ok=True)
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(logs / "sptf.log", encoding="utf-8"),
            logging.StreamHandler(sys.stderr),
        ],
    )
    _LOGGER_INIT = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)