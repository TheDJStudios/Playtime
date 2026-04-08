# Networking

`fabricpy` now has a first-class packet system for simple client/server messaging.

Use it when you need:

- a keybind to tell the server something happened
- a screen button to send a request to the server
- the server to push a message back to one player or all players

## Packet API

Create a packet with:

```python
ping_packet = mod.packet("ping")
```

Then attach handlers:

```python
@ping_packet.on_server
def on_ping_server(ctx):
    ctx.player.send_message("Server got: " + ctx.message)
```

```python
@ping_packet.on_client
def on_ping_client(ctx):
    ctx.player.send_action_bar("Client got: " + ctx.message)
```

## Packet Context

Packet handlers expose:

- `ctx.message`
- `ctx.player` when a player exists on that side
- `ctx.world`
- `ctx.server`

## Sending Packets

Available helpers:

- `ctx.net.send_to_server(packet_id, message)`
- `ctx.net.send_to_player(player, packet_id, message)`
- `ctx.net.broadcast(packet_id, message)`

Example:

```python
@mod.event("player_join")
def on_join(ctx):
    ctx.net.send_to_player(ctx.player, "welcome", "hello")
```

```python
welcome_packet = mod.packet("welcome")

@welcome_packet.on_client
def on_welcome(ctx):
    ctx.player.send_action_bar(ctx.message)
```

## Keybind Example

```python
open_bind = mod.keybind("ping_server", "Ping Server", "R")

@open_bind.on_press
def on_ping(ctx):
    ctx.net.send_to_server("ping", "pressed R")
```

## Screen Button Example

```python
panel = mod.screen("panel", "Panel")
send_button = panel.button.add("send_ping", "Send Ping", 20, 40, 100, 20)

@send_button.on_click
def on_send_ping(ctx):
    ctx.net.send_to_server("ping", "clicked button")
    ctx.client.close_screen()
```

## Current Scope

Current packet payloads are string-message based:

- `packet_id`
- `message`

That keeps the Python API small and easy to read. More complex typed payloads can still be added later without breaking this surface.
