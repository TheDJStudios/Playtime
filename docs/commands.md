# Commands

Register commands with `@mod.command(...)`.

Arguments:

- `name`: command name without the leading slash
- `permission_level`: default `0`
- `aliases`: optional list of alternate names

Example:

```python
@mod.command("ping", permission_level=0, aliases=["p"])
def ping(ctx):
    ctx.source.send_message("pong")
```

Teleport command example:

```python
@mod.command("lobby", permission_level=0)
def lobby(ctx):
    ctx.source.run_command("tp @s 0 80 0")
```

Available command context helpers:

- `ctx.source`
- `ctx.source.send_message(text)`
- `ctx.source.get_player()`
- `ctx.source.get_pos()`

Notes:

- aliases redirect to the main command
- commands are emitted through Brigadier for the supported loaders
