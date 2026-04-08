# Screens

`fabricpy` now supports simple client screens from Python.

Use screens when you need:

- a keybind-opened panel
- clickable buttons
- static labels
- lightweight client UI without dropping into manual Java screen code

## Screen API

Create a screen:

```python
panel = mod.screen("panel", "Runtime Panel", width=220, height=160)
```

Add labels:

```python
panel.label("Runtime systems online", 20, 40, 0x55FFFF)
```

Add buttons:

```python
send_button = panel.button.add("send_ping", "Send Ping", 20, 70, 120, 20)
```

Attach handlers:

```python
@panel.on_open
def on_panel_open(ctx):
    ctx.player.send_action_bar("Opened panel")
```

```python
@send_button.on_click
def on_send_ping(ctx):
    ctx.net.send_to_server("ping", "button packet")
    ctx.client.close_screen()
```

## Opening And Closing Screens

Available helpers:

- `ctx.client.open_screen(screen_id)`
- `ctx.client.close_screen()`

Typical keybind usage:

```python
open_bind = mod.keybind("open_panel", "Open Panel", "R")

@open_bind.on_press
def on_open_panel(ctx):
    ctx.client.open_screen("panel")
```

## Screen Handler Context

Screen open and button handlers can use:

- `ctx.client`
- `ctx.player`
- `ctx.world`
- `ctx.server`

That means screens can:

- send packets
- close themselves
- show client-side feedback
- react to the local player and world

## Current Scope

This screen system is intentionally simple:

- title
- width and height metadata
- labels
- buttons
- open handler

It is not yet a full inventory/menu/container system. For now it is the lightweight custom client UI layer.
