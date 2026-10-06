# Xylo Studios — Agent Guide

This repo is the **studio root** for Xylo Studios: an indie studio that makes many games, plus the art,
music and shared tooling behind them. Agents working here should treat it as a production studio, not a
single project. The goal is that every game we ship makes the next one faster to build.

`CLAUDE.md` imports this file. Keep shared instructions here; put only Claude-specific notes in `CLAUDE.md`.

## Layout

```
C:\GameDev\                 studio root (this repo, PUBLIC: github.com/lukenneth/xylo-studios)
├── AGENTS.md / CLAUDE.md   agent instructions (this file)
├── docs/                   studio docs: toolchain, conventions, pipelines
├── tools/                  shared scripts (Python first; run from repo root)
│   ├── doctor.py           verifies every CLI in the toolchain works
│   ├── new_game.py         scaffolds games/<name> as a Unity project + its own git repo
│   ├── blender/            headless Blender scripts (export, batch processing)
│   ├── audio/              sox/ffmpeg wrappers (normalize, convert to game formats)
│   └── art/                image pipeline helpers (ImageMagick/Inkscape/Krita)
├── packages/               shared Unity UPM packages (com.xylo.*), reusable across games
├── templates/game/         files copied into every new game repo (AGENTS.md, .gitignore, .gitattributes)
├── games/      (ignored)   one folder per game, EACH ITS OWN GIT REPO (usually private)
├── art/        (ignored)   studio-owned source art (.kra, .blend, .psd, .svg …)
├── audio/      (ignored)   studio-owned music/ and sfx/ sources (.mmp, .wav, .aup4 …)
└── builds/     (ignored)   build output; never committed anywhere
```

## Public / private boundary — read before committing

This repo is **public**. Before staging anything, ask: *is this reusable know-how, or is it the studio's product?*

| Commit here (public) | Never commit here |
|---|---|
| Tools, scripts, editor utilities | Game source for unreleased/commercial games (lives in `games/<name>/` repos) |
| Shared packages meant for reuse | Studio-owned art, music, SFX, models, fonts we licensed |
| Templates, docs, conventions | `.env`, API keys, tokens, signing keys, keystores, `.p12/.pfx` |
| Small test fixtures you generated yourself | Unity license files (`*.ulf`, `*.alf`), Steamworks credentials |
| | Personal info: emails, real names in configs, machine-specific absolute paths |

- `.gitignore` already blocks `games/`, `art/`, `audio/`, `builds/` and common secret files. **Do not weaken it**
  to commit something; if a studio asset should be public, discuss it with the user first.
- Third-party assets (Asset Store, purchased packs, fonts) are never redistributed here, even inside packages.
- Run `git diff --cached --stat` and scan the list before every commit. When in doubt, leave it out and ask.
- Commits use the GitHub noreply email configured in this repo; don't override `user.email`.

## Toolchain (Windows 11, all verified headless)

Every tool below is on PATH in new shells (PowerShell, cmd and Git Bash). Run `python tools/doctor.py` to
re-verify. Full recipes are in `docs/toolchain.md`.

| Need | Command | Notes |
|---|---|---|
| Engine | `unity` (Unity CLI) | Editor 6000.3.25f1 (Unity 6.3 LTS). `unity status`, `unity projects create`, `unity test`, `unity build`, `unity recompile` |
| 3D | `blender --background --python script.py -- args` | Blender 5.2. Always `--background`; use `--factory-startup` for reproducibility |
| glTF | `gltf-transform inspect\|optimize\|…` | Inspect/optimize `.glb` exports |
| Raster art | `magick` (ImageMagick 7), `krita --export`, `gimp-console` | GIMP 3 needs `--batch-interpreter=python-fu-eval … --quit` |
| Vector art | `inkscape in.svg --export-type=png --export-filename=out.png` | |
| Audio | `sox`, `ffmpeg`, `ffprobe` | Game format = `.ogg` (music) / `.wav` (short SFX) |
| Music | `lmms render song.mmp -o out.wav` | LMMS 1.2; Surge XT is available as a synth plugin |
| Code | `python` 3.13, `uv`, `node` 24, `dotnet`, `git`, `git lfs`, `gh`, `rg`, `jq`, `7z` | |

GUI-only (ask the user; don't try to drive them headlessly): Audacity, Pixelorama, Material Maker, Surge XT.

## Working rules

- **Verify, don't assume.** After changing a tool or script, run it on a real input and check the output file
  exists and is sane. For Unity code, use `unity recompile` (running Editor) or `unity test` before claiming done.
- **Prefer shared tooling.** If you solve something a second game will need, put it in `tools/` or `packages/`
  instead of copy-pasting into a game. Document new tools in `docs/toolchain.md` and the table above.
- **Scripts are Python** (stdlib first; add deps via `uv` with inline script metadata) so they run the same from
  PowerShell and Git Bash. Use `pathlib`, never hard-code `C:\Users\<name>`; resolve paths relative to the repo.
- **Don't launch GUI apps** unless the user asks. Every pipeline step should have a headless path.
- **Long-running commands** (Unity imports/builds, Blender renders) run in the background with a timeout.
- Windows has long paths enabled and `git core.longpaths=true`; still keep project paths short (`C:\GameDev\games\<name>`).

## Games

- Create with `python tools/new_game.py <name>` (kebab-case). It makes `games/<name>/` a Unity project using the
  studio editor version, copies `templates/game/`, and runs `git init` so the game has its own repo + Git LFS.
- Each game has its own `AGENTS.md`; read it when working inside that game. Game-specific rules live there.
- Shared packages are referenced from games via `"com.xylo.<name>": "file:../../../packages/com.xylo.<name>"`
  in `Packages/manifest.json` (or a git URL once published).

## Conventions

- Folders/files: `kebab-case` for repo folders, `PascalCase` for Unity C# types and their files.
- C#: one public type per file, namespaces `Xylo.<Package>` / `<GameName>`, no `Find()`/`GetComponent()` in `Update()`.
- Assets in games: `Art/`, `Audio/`, `Prefabs/`, `Scenes/`, `Scripts/`, `Settings/` under `Assets/`.
- Source files (`.blend`, `.kra`, `.mmp`) live in studio `art/` / `audio/` or the game's `Source/` folder (LFS);
  only exported game-ready files (`.glb`/`.fbx`, `.png`, `.ogg`/`.wav`) go into Unity `Assets/`.
- Commit messages: imperative, scoped — `tools: add glb batch exporter`, `docs: document gimp batch mode`.
