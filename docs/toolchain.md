# Toolchain

Every command here was verified headless on the studio machine (Windows 11, RTX 4060 laptop). Run
`python tools/doctor.py` to re-check after installs or updates.

## Installed tools

| Tool | Version | How it's on PATH |
|---|---|---|
| Unity Editor | 6000.3.25f1 (Unity 6.3 LTS) + Windows IL2CPP | via Unity Hub / `unity` CLI |
| Unity CLI (`unity`) | 1.0 beta | `%LOCALAPPDATA%\Unity\bin` (see note below) |
| Unity Hub | 3.22 (MSIX) | Start menu |
| Visual Studio 2022 Community | + "Game development with Unity" workload | script editor for Unity |
| Blender | 5.2 | install dir on PATH |
| Krita / Inkscape / GIMP 3 | 5.3 / 1.4 / 3.2 | `.cmd` + POSIX shims in `~/.local/bin` (their dirs bundle `python.exe`/`ffmpeg.exe`, so they are *not* put on PATH directly) |
| ImageMagick (`magick`) | 7.1 | installer PATH |
| LMMS | 1.2 | install dir on PATH |
| SoX, FFmpeg | 14.4 / 7.1 | winget |
| gltf-transform | npm global | `npm i -g @gltf-transform/cli` |
| Python / uv / Node | 3.13 / 0.12 / 24 LTS | winget |
| gh, git, git-lfs, rg, jq, 7z | | winget / Git for Windows |
| GUI only | Audacity, Pixelorama, Material Maker, Surge XT | Start menu |

## Recipes

### Unity
```sh
unity editors                                   # installed editors (default: 6000.3.25f1)
unity status                                    # running Editors an agent can talk to
python tools/new_game.py my-game                # new project in games/ (wraps `unity projects create`)
unity test games/my-game --mode EditMode --timeout 900
unity build games/my-game --target StandaloneWindows64 --output-path builds/my-game/my-game.exe
unity recompile --project-path games/my-game --strict   # with the Editor open
unity commands --json                           # full machine-readable command manifest
```
The Hub runs as an MSIX app, so when it self-updates the CLI the new copy lands in its sandbox
(`%LOCALAPPDATA%\Packages\UnityTechnologies.UnityHub_*\LocalCache\Local\Unity\bin`). If `unity --version`
lags behind the Hub, copy `unity.exe` from there to `%LOCALAPPDATA%\Unity\bin`.

### Blender
```sh
# export a .blend to .glb
blender --background art/props/crate.blend --python tools/blender/export_glb.py -- out/crate.glb
# one-off python
blender --background --factory-startup --python-expr "import bpy; print(bpy.app.version_string)"
gltf-transform inspect out/crate.glb
gltf-transform optimize out/crate.glb out/crate.min.glb --compress meshopt
```

### 2D art
```sh
python tools/art/export_sprites.py art/icons/*.svg --out out/sprites --sizes 64 128
inkscape icon.svg --export-type=png --export-filename=icon.png --export-width=256
krita --export --export-filename out.png painting.kra
magick in.png -resize 50% -strip out.png
magick sheet/*.png +append spritesheet.png           # horizontal sprite strip
```
GIMP 3 batch mode needs an explicit interpreter and `--quit`, otherwise it hangs:
```sh
gimp-console -i --batch-interpreter=python-fu-eval \
  -b "from gi.repository import Gimp, Gio; img = Gimp.file_load(Gimp.RunMode.NONINTERACTIVE, Gio.File.new_for_path('in.png')); Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, img, Gio.File.new_for_path('out.png'), None)" \
  --quit
```

### Audio & music
```sh
python tools/audio/game_audio.py sfx audio/sfx/raw/*.wav --out out/sfx       # mono wav, trimmed, -1 dBFS
python tools/audio/game_audio.py music audio/music/theme.wav --out out/music # ogg, -16 LUFS
lmms render audio/music/theme.mmp -o audio/music/theme.wav                   # render an LMMS project
sox -n -r 44100 blip.wav synth 0.1 square 880 fade 0 0.1 0.05                # quick placeholder SFX
ffprobe -hide_banner out/music/theme.ogg
```

## Agent integrations
- **Claude Code**: Unity's official plugin `unity@unity-agent-plugin` (installed via `unity setup claude`).
- **Other agents**: `unity skill install <client>` (cursor, codex, vscode, …) and `unity mcp configure <client>`.
- All scripts in `tools/` are plain Python CLIs with `--help`, deterministic output paths and non-zero exit
  codes on failure, so agents can chain and verify them.
