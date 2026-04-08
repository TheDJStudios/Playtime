# Events

Global events are registered with:

```python
@mod.event("event_name")
def handler(ctx):
    ...
```

These are different from block hooks, item hooks, and keybind handlers.

## Supported Event Names

- `player_join`
- `player_leave`
- `player_death`
- `player_respawn`
- `player_change_dimension`
- `player_chat`
- `player_offhand_change`
- `block_break`
- `player_tick`
- `player_use_item`
- `player_use_block`
- `player_attack_entity`
- `player_interact_entity`
- `entity_death`
- `server_start`
- `server_stop`
- `server_tick`

## Common Event Shapes

Player lifecycle:

- `player_join`
- `player_leave`
- `player_death`
- `player_respawn`
- `player_change_dimension`

Chat:

- `player_chat`

Offhand changes:

- `player_offhand_change`

Interactions:

- `player_use_item`
- `player_use_block`
- `player_attack_entity`
- `player_interact_entity`

World/server:

- `block_break`
- `player_tick`
- `server_start`
- `server_stop`
- `server_tick`

## Examples

```python
@mod.event("player_join")
def on_join(ctx):
    ctx.player.send_message("Welcome")
```

```python
@mod.event("player_chat")
def on_chat(ctx):
    if "scanner" in ctx.message:
        ctx.player.send_message("Scanner keyword detected")
```

```python
@mod.event("player_offhand_change")
def on_offhand(ctx):
    if ctx.stack.is_of("playtime:grabpack_left_blue"):
        ctx.player.send_action_bar("Blue left hand online")
```

```python
@mod.event("player_use_item")
def on_use_item(ctx):
    if ctx.stack.is_of("playtime:grabpack_cannon"):
        ctx.player.add_cooldown("playtime:grabpack_cannon", 8)
        ctx.player.send_action_bar("GrabPack hand launched")
```
