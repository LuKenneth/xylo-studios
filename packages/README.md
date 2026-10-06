# packages/

Shared Unity packages (UPM) reused across Xylo Studios games, named `com.xylo.<area>` (e.g. `com.xylo.core`,
`com.xylo.audio`). Only put code and self-made assets here: this folder is public.

Each package follows the standard Unity layout:

```
com.xylo.<area>/
  package.json            name, version (semver), unity "6000.3", displayName, description
  README.md
  Runtime/Xylo.<Area>.asmdef  + runtime C#
  Editor/Xylo.<Area>.Editor.asmdef  + editor-only C#
  Tests/Runtime, Tests/Editor
```

Reference from a game's `Packages/manifest.json`:

```json
"com.xylo.core": "file:../../../packages/com.xylo.core"
```

Promote code here when a second game needs it; don't pre-build abstractions for one game.
