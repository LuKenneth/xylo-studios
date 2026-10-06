#!/usr/bin/env python3
"""Convert source audio into game-ready files with consistent loudness.

Usage:
    python tools/audio/game_audio.py sfx   in.wav [more.wav ...] --out out/dir
    python tools/audio/game_audio.py music in.wav [...]           --out out/dir

sfx   -> 44.1 kHz 16-bit mono .wav, peak-normalized to -1 dBFS, leading/trailing silence trimmed
music -> 44.1 kHz stereo .ogg (Vorbis q6), loudness-normalized to -16 LUFS (ffmpeg loudnorm)
Requires sox and ffmpeg on PATH (see tools/doctor.py).
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stderr}")


def sfx(src: Path, out_dir: Path) -> Path:
    dst = out_dir / f"{src.stem}.wav"
    run([
        "sox", str(src), "-r", "44100", "-b", "16", "-c", "1", str(dst),
        "silence", "1", "0.01", "0.1%", "reverse", "silence", "1", "0.01", "0.1%", "reverse",
        "gain", "-n", "-1",
    ])
    return dst


def music(src: Path, out_dir: Path) -> Path:
    dst = out_dir / f"{src.stem}.ogg"
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "2",
        "-c:a", "libvorbis", "-q:a", "6", str(dst),
    ])
    return dst


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("kind", choices=["sfx", "music"])
    p.add_argument("inputs", nargs="+", type=Path)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()

    for tool in ("sox", "ffmpeg"):
        if not shutil.which(tool):
            raise SystemExit(f"{tool} not found on PATH; run python tools/doctor.py")
    args.out.mkdir(parents=True, exist_ok=True)
    convert = sfx if args.kind == "sfx" else music
    for src in args.inputs:
        if not src.is_file():
            raise SystemExit(f"input not found: {src}")
        dst = convert(src, args.out)
        print(f"{src} -> {dst} ({dst.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
