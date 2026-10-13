# Contributing to singleplayer-trainer-framework

Thanks for wanting to push spuds into the pot. This repo is a **singleplayer-only** trainer framework — memory scanning, pointer chains, feature handlers, hotkey dispatch. It is built for offline single-player games and personal reverse-engineering research.

## Ground rules

- **Singleplayer only.** PRs that add multiplayer / anti-cheat bypass for live services get closed without review.
- Keep features modular. Every new feature is a handler class, not a fork of the engine.
- No hardcoded addresses in source. Addresses live in `pointer_maps/*.json`, signatures live in `pointer_maps/signatures/*.toml`.
- Python 3.10+. Type hints required on public functions.

## Dev setup

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest -q
```

## Adding a feature handler

1. Create `feature_handlers/<name>_handler.py` subclassing `FeatureHandler`.
2. Register it in `feature_handlers/registry.py`.
3. Add a pointer map entry under `pointer_maps/<game_slug>.json`.
4. Add a test in `tests/`.

## Style

- `ruff` for lint, `mypy` for types, `pytest` for tests. All three must pass.
- Logging via `trainer_utils.logging_setup.get_logger(__name__)`.

## Reporting bugs

Use the issue template. Include: game name, game build/SKU, Windows version, Python version, and the full traceback from `logs/sptf.log`.