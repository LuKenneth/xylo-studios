#!/usr/bin/env python3
"""Verify the Xylo Studios toolchain: every CLI resolves on PATH and answers a version/help probe.

Usage:
    python tools/doctor.py            # human-readable table
    python tools/doctor.py --json     # machine-readable, for agents/CI

Exit code is 1 if any *required* tool is missing or fails its probe.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys

# (name, probe args or None for a PATH-only check, required, purpose)
TOOLS: list[tuple[str, list[str] | None, bool, str]] = [
    ("git", ["--version"], True, "version control"),
    ("git-lfs", ["version"], True, "large files in game repos"),
    ("gh", ["--version"], True, "GitHub repos/PRs"),
    ("python", ["--version"], True, "studio scripts"),
    ("uv", ["--version"], False, "python deps / tool runner"),
    ("node", ["--version"], False, "JS tooling"),
    ("dotnet", ["--version"], False, "C# tooling outside Unity"),
    ("unity", ["--version"], True, "Unity CLI (editors, projects, builds, tests)"),
    ("blender", ["--version"], True, "3D modelling / export"),
    ("gltf-transform", ["--version"], False, "glTF inspect/optimize"),
    ("magick", ["-version"], True, "image processing"),
    ("inkscape", ["--version"], False, "vector -> raster export"),
    ("krita", None, False, "paint file export (presence only: --version starts the GUI)"),
    ("gimp-console", ["--version"], False, "GIMP batch processing"),
    ("sox", ["--version"], True, "audio processing"),
    ("ffmpeg", ["-version"], True, "audio/video conversion"),
    ("ffprobe", ["-version"], False, "media inspection"),
    ("lmms", ["--version"], False, "music render"),
    ("rg", ["--version"], False, "code search"),
    ("jq", ["--version"], False, "JSON processing"),
    ("7z", ["i"], False, "archives"),
]


def probe(name: str, args: list[str] | None) -> dict:
    path = shutil.which(name)
    if not path:
        return {"tool": name, "ok": False, "path": None, "version": None, "error": "not on PATH"}
    if args is None:
        return {"tool": name, "ok": True, "path": path, "version": "(on PATH)", "error": None}
    try:
        proc = subprocess.run(
            [path, *args], capture_output=True, text=True, timeout=60,
            encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"tool": name, "ok": False, "path": path, "version": None, "error": str(exc)}
    out = (proc.stdout or proc.stderr).strip()
    first = next((line.strip() for line in out.splitlines() if line.strip()), "")
    # krita/7z/lmms print banners or return non-zero for info flags; treat any output as alive.
    ok = proc.returncode == 0 or bool(first)
    return {"tool": name, "ok": ok, "path": path, "version": first[:80], "error": None if ok else f"exit {proc.returncode}"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", action="store_true", help="emit JSON")
    opts = parser.parse_args()

    results = []
    for name, args, required, purpose in TOOLS:
        r = probe(name, args)
        r.update(required=required, purpose=purpose)
        results.append(r)

    failed_required = [r for r in results if r["required"] and not r["ok"]]
    if opts.json:
        print(json.dumps({"ok": not failed_required, "tools": results}, indent=2))
    else:
        for r in results:
            mark = "PASS" if r["ok"] else ("FAIL" if r["required"] else "warn")
            detail = r["version"] if r["ok"] else r["error"]
            print(f"{mark:4}  {r['tool']:15} {detail}")
        print()
        print("All required tools OK." if not failed_required else
              f"Missing/broken required tools: {', '.join(r['tool'] for r in failed_required)}")
    return 1 if failed_required else 0


if __name__ == "__main__":
    sys.exit(main())
