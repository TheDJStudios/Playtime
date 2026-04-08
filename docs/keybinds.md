# Keybinds

`fabricpy` supports client-side keybind definitions for Fabric and Forge.

Define a keybind from Python, then attach an `on_press` handler to it.

## Main API

- `bind = mod.keybind(keybind_id, title, key, category="", category_title="")`
- `@bind.on_press`

## Fields

- `keybind_id`: unique id for the bind, for example `open_scanner`
- `title`: player-facing keybind name shown in controls
- `key`: default key, for example `"R"`, `"SPACE"`, `"F6"`, or a GLFW key code integer
- `category`: optional category id, defaults to your `mod_id`
- `category_title`: optional category title shown in controls, defaults to `mod.name`

## Minimal example

```python
scanner_bind = mod.keybind(
    keybind_id="open_scanner",
    title="Open Scanner",
    key="R",
)


@scanner_bind.on_press
def on_open_scanner(ctx):
    ctx.player.send_message("Scanner key pressed")
```

## Multiple keybinds example

```python
scanner_bind = mod.keybind("open_scanner", "Open Scanner", "R", category_title="Playtime Controls")
flashlight_bind = mod.keybind("toggle_flashlight", "Toggle Flashlight", "F")


@scanner_bind.on_press
def on_open_scanner(ctx):
    ctx.player.send_action_bar("Scanner opened")


@flashlight_bind.on_press
def on_flashlight(ctx):
    ctx.player.send_action_bar("Flashlight toggled")
```

## Custom category example

```python
map_bind = mod.keybind(
    keybind_id="open_map",
    title="Open Facility Map",
    key="M",
    category="playtime.controls",
    category_title="Playtime Controls",
)
```

## Notes

- keybind handlers are client-side
- `ctx.player` and `ctx.world` are available when the client player exists
- `ctx.keybind` is the generated keybind object
- `ctx.client` is the Minecraft client object
- keybinds are registered automatically during client setup
- category and key names are written into generated lang entries

## Runtime note

Because keybinds are client-side, anything that needs authoritative server behavior should usually:

- show client feedback directly, or
- send a command/message path you control, or
- be used in singleplayer/integrated-server scenarios

Avoid assuming `ctx.server` exists in multiplayer client sessions.
