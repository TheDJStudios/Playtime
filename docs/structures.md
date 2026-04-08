# Structures And NBT

NBT structure templates can be copied into the generated datapack and placed from Python at runtime.

Python method:

- `mod.add_structure(structure_id, nbt_path)`

Generated output:

- `data/<modid>/structures/<structure_id>.nbt`

Example:

```python
mod.add_structure("rooms/test_room", "assets_src/test_room.nbt")
```

Place on command example:

```python
@mod.command("spawn_room")
def spawn_room(ctx):
    ctx.source.run_command("execute in mymod:pocket run place template mymod:rooms/test_room 0 64 0")
```

That creates:

- `data/<modid>/structures/rooms/test_room.nbt`

Runtime placement helpers:

- `ctx.world.place_structure(dimension_id, structure_id, x, y, z)`
- `ctx.world.place_nbt(dimension_id, structure_id, x, y, z)`

Example:

```python
@mod.event("player_join")
def on_join(ctx):
    ctx.world.place_structure("mymod:pocket", "mymod:rooms/test_room", 0, 64, 0)
```

Notes:

- structure ids should be full ids like `"mymod:rooms/test_room"`
- the helper uses Minecraft's `place template` command under the hood
- you can also keep structure files directly in repo data at `data/<modid>/structures/...`
