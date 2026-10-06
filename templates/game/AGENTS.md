# {{GAME_NAME}} — Agent Guide

A Xylo Studios game. Unity {{UNITY_EDITOR}} ({{TEMPLATE}} URP). This folder is its **own git repo**
(usually private) inside the studio root at `../../`. Studio-wide rules, the toolchain and shared tools are
in `../../AGENTS.md`; read that first. This file holds only what's specific to this game.

## Pitch
_One or two sentences: what the player does and why it's fun. Keep updated._

## Status
_Current milestone, what's playable, what's next._

## Project layout
```
Assets/
  Art/        imported game-ready art (.png, .glb); sources live in Source/ or ../../art
  Audio/      game-ready .ogg / .wav (export with ../../tools/audio/game_audio.py)
  Prefabs/
  Scenes/
  Scripts/    C# — PascalCase namespace from the game name, one public type per file
  Settings/   URP and input settings
Packages/     manifest.json (shared studio packages referenced via file:../../../packages/…)
Source/       working files (.blend, .kra, .mmp) — tracked with Git LFS
```

## How to verify changes
- Scripts compile: `unity recompile --project-path . --strict` with the Editor open; `unity run . --timeout 600`
  opens it headless in batch mode (compile + import) when no Editor is running.
- Tests: `unity test . --mode EditMode --timeout 900` (and `--mode PlayMode` once play-mode tests exist).
- Build: `unity build . --target StandaloneWindows64 --output-path ../../builds/{{GAME_SLUG}}/{{GAME_SLUG}}.exe`.
- Live editor: `unity status` lists open Editors; `unity list` / `unity command` drive one (needs the Pipeline package).
- These flags come from Unity CLI 1.0 beta; confirm with `unity <cmd> --help` if one fails.

## Game-specific rules
_Add rules here as they come up (art style constraints, performance budgets, platform targets, etc.)._
