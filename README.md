# Xylo Studios

Studio root for Xylo Studios: shared tooling, templates, docs and reusable Unity packages behind our games,
art and music. Built to be worked on by humans and coding agents together.

The games themselves and studio-owned art/audio live in their own repositories (or stay local); this repo
holds the reusable parts that help us make each game faster than the last.

## What's here

| Path | Contents |
|---|---|
| [`AGENTS.md`](AGENTS.md) | How agents (and people) should work in the studio: layout, rules, toolchain |
| [`docs/`](docs/) | [Toolchain & recipes](docs/toolchain.md) |
| [`tools/`](tools/) | Python CLIs: toolchain doctor, game scaffolding, Blender/art/audio pipelines |
| [`templates/game/`](templates/game/) | Files every new game repo starts with |
| [`packages/`](packages/) | Shared Unity packages (`com.xylo.*`) |
| `games/`, `art/`, `audio/`, `builds/` | Local/private; ignored by this repo |

## Quick start

Requires Windows 10/11 with the tools listed in [docs/toolchain.md](docs/toolchain.md).

```sh
python tools/doctor.py                  # verify the toolchain
python tools/new_game.py my-game        # scaffold games/my-game (Unity 6.3 LTS, own git repo)
```

## License

Code and docs in this repository are [MIT licensed](LICENSE). Games, art, music and other creative assets
from Xylo Studios are **not** included here and are not covered by this license.
