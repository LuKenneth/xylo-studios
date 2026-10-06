@AGENTS.md

## Claude Code specifics

- The official **Unity plugin** (`unity@unity-agent-plugin`) is installed at user scope; it provides Unity skills
  and lets you drive a running Editor through the `unity` CLI (`unity status`, `unity command`, `unity recompile`).
  For live Editor control a project needs the Pipeline package (`unity projects create … --with-pipeline`).
- Run `python tools/doctor.py` at the start of a session that will touch the toolchain.
- Shell: both Bash (Git Bash) and PowerShell work; tools resolve the same in both. Prefer forward slashes and
  repo-relative paths in commands you put in docs or scripts.
- Use the Bash tool's background mode for Unity imports/builds and Blender renders; they can take minutes.
- Before any `git commit` in this repo, show the user the staged file list if it includes anything outside
  `tools/`, `docs/`, `templates/`, `packages/` or the root config files.
