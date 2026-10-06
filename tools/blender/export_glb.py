"""Export a .blend file to a game-ready .glb (runs inside Blender).

Usage (from the studio root):
    blender --background path/to/model.blend --python tools/blender/export_glb.py -- out/model.glb [--selected]

Applies modifiers, exports +Y-up glTF binary with materials/textures embedded. Unity imports .glb via the
glTFast package; use .fbx instead only if a game's AGENTS.md says so.
"""
import argparse
import sys
from pathlib import Path

import bpy


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser(prog="export_glb.py")
    p.add_argument("output", type=Path, help="destination .glb path")
    p.add_argument("--selected", action="store_true", help="export only selected objects")
    return p.parse_args(argv)


def main() -> None:
    args = parse_args()
    out = args.output.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=str(out),
        export_format="GLB",
        use_selection=args.selected,
        export_apply=True,
        export_yup=True,
    )
    if not out.exists() or out.stat().st_size == 0:
        raise SystemExit(f"export failed: {out} was not written")
    print(f"exported {out} ({out.stat().st_size} bytes)")


main()
