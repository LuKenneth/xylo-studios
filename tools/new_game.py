#!/usr/bin/env python3
"""Scaffold a new game: games/<name>/ as a Unity project with its own git repo (+ Git LFS).

Usage (from the studio root):
    python tools/new_game.py my-game                 # URP 2D, with the Unity Pipeline package (agent control)
    python tools/new_game.py my-game --template 3d   # URP 3D
    python tools/new_game.py my-game --no-pipeline   # skip the Pipeline package
    python tools/new_game.py my-game --dry-run       # print the plan, change nothing

The editor version and template ids come from studio.json. The game repo is created locally only; publish
it yourself with `gh repo create <owner>/<name> --private --source games/<name> --push` when ready.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "templates" / "game"


def run(cmd: list[str], cwd: Path | None = None, dry: bool = False) -> None:
    print("$", " ".join(cmd))
    if dry:
        return
    exe = shutil.which(cmd[0])
    if not exe:
        raise SystemExit(f"{cmd[0]} not found on PATH; run python tools/doctor.py")
    proc = subprocess.run([exe, *cmd[1:]], cwd=cwd)
    if proc.returncode != 0:
        raise SystemExit(f"command failed ({proc.returncode}): {' '.join(cmd)}")


def main() -> int:
    studio = json.loads((ROOT / "studio.json").read_text(encoding="utf-8"))
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("name", help="kebab-case game folder name, e.g. space-goat")
    p.add_argument("--template", choices=sorted(studio["unityTemplates"]), default="2d")
    p.add_argument("--no-pipeline", action="store_true", help="don't add the Unity Pipeline package")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.name):
        raise SystemExit("name must be kebab-case (lowercase letters, digits, single hyphens)")
    games_dir = ROOT / studio["gamesDir"]
    game = games_dir / args.name
    if game.exists():
        raise SystemExit(f"{game} already exists")

    cmd = [
        "unity", "projects", "create", args.name,
        "--path", str(games_dir),
        "--editor-version", studio["unityEditor"],
        "--template", studio["unityTemplates"][args.template],
        "--no-cloud", "--non-interactive", "--no-banner",
    ]
    if not args.no_pipeline:
        cmd.append("--with-pipeline")
    run(cmd, dry=args.dry_run)

    title = " ".join(w.capitalize() for w in args.name.split("-"))
    for src in sorted(TEMPLATE_DIR.iterdir()):
        dst = game / src.name
        print(f"copy {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
        if args.dry_run:
            continue
        text = src.read_text(encoding="utf-8")
        text = text.replace("{{GAME_NAME}}", title).replace("{{GAME_SLUG}}", args.name)
        text = text.replace("{{UNITY_EDITOR}}", studio["unityEditor"]).replace("{{TEMPLATE}}", args.template.upper())
        dst.write_text(text, encoding="utf-8", newline="\n")

    run(["git", "init", "-b", "main"], cwd=game, dry=args.dry_run)
    run(["git", "lfs", "install", "--local"], cwd=game, dry=args.dry_run)

    print(f"\nCreated {game.relative_to(ROOT)} ({args.template.upper()}, Unity {studio['unityEditor']}).")
    print("Next: review files, `git add -A && git commit -m \"Initial project\"` inside the game folder,")
    print(f"then `gh repo create <owner>/{args.name} --private --source {game.relative_to(ROOT).as_posix()} --push`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
