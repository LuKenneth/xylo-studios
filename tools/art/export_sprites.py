#!/usr/bin/env python3
"""Export source art (.svg, .kra, .png, .psd) to game-ready PNG sprites at one or more scales.

Usage:
    python tools/art/export_sprites.py art/icons/*.svg --out out/sprites --sizes 64 128
    python tools/art/export_sprites.py art/chars/hero.kra --out out/sprites            # native size

.svg -> Inkscape (crisp vector rasterization at each size)
.kra -> Krita export, then ImageMagick resize
other -> ImageMagick
Sizes are the target width in pixels (height keeps aspect ratio). Output: <stem>.png or <stem>@<size>.png
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd: list[str]) -> None:
    exe = shutil.which(cmd[0])
    if not exe:
        raise SystemExit(f"{cmd[0]} not found on PATH; run python tools/doctor.py")
    proc = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stderr}")


def export_one(src: Path, out_dir: Path, sizes: list[int]) -> list[Path]:
    outputs: list[Path] = []
    targets = [(size, out_dir / f"{src.stem}@{size}.png") for size in sizes] or [(None, out_dir / f"{src.stem}.png")]
    if src.suffix.lower() == ".svg":
        for size, dst in targets:
            cmd = ["inkscape", str(src), "--export-type=png", f"--export-filename={dst}"]
            if size:
                cmd.append(f"--export-width={size}")
            run(cmd)
            outputs.append(dst)
        return outputs

    with tempfile.TemporaryDirectory() as tmp:
        base = src
        if src.suffix.lower() == ".kra":
            base = Path(tmp) / f"{src.stem}.png"
            run(["krita", "--export", "--export-filename", str(base), str(src)])
        for size, dst in targets:
            cmd = ["magick", f"{base}[0]"]  # [0] = first layer/frame for .psd/.gif
            if size:
                cmd += ["-filter", "Lanczos", "-resize", f"{size}x"]
            run([*cmd, str(dst)])
            outputs.append(dst)
    return outputs


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("inputs", nargs="+", type=Path)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--sizes", nargs="*", type=int, default=[], help="target widths in px")
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for src in args.inputs:
        if not src.is_file():
            raise SystemExit(f"input not found: {src}")
        for dst in export_one(src, args.out, args.sizes):
            if not dst.exists() or dst.stat().st_size == 0:
                raise SystemExit(f"export failed: {dst}")
            print(f"{src} -> {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
