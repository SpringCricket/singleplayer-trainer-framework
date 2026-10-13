"""Command-line entry point for sptf.

Usage:
    sptf --game eldenring --profile default
    sptf --list-profiles
    sptf --game skyrim --no-hotkeys
"""
from __future__ import annotations

import argparse
import sys

from rich.console import Console

from trainer_bootstrap.session import TrainerSession
from trainer_config.loader import list_profiles, load_profile
from trainer_utils.logging_setup import get_logger, init_logging

log = get_logger(__name__)
console = Console()


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sptf",
        description="Singleplayer trainer framework — attach, scan, toggle features.",
    )
    p.add_argument("--game", required=False, help="Game slug (matches pointer_maps/<slug>.json)")
    p.add_argument("--profile", default="default", help="Profile name under trainer_config/profiles/")
    p.add_argument("--list-profiles", action="store_true", help="List available profiles and exit")
    p.add_argument("--no-hotkeys", action="store_true", help="Disable global hotkey listener")
    p.add_argument("--verbose", action="store_true", help="Debug logging")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    init_logging(verbose=args.verbose)

    if args.list_profiles:
        for name in list_profiles():
            console.print(f"  • {name}")
        return 0

    if not args.game:
        console.print("[red]--game is required unless --list-profiles is set[/red]")
        return 2

    try:
        profile = load_profile(args.profile)
    except FileNotFoundError as exc:
        console.print(f"[red]profile not found:[/red] {exc}")
        return 2

    session = TrainerSession(game_slug=args.game, profile=profile, enable_hotkeys=not args.no_hotkeys)
    try:
        session.attach()
        session.run()
    except KeyboardInterrupt:
        console.print("\n[dim]detaching...[/dim]")
    finally:
        session.detach()
    return 0


if __name__ == "__main__":
    sys.exit(main())