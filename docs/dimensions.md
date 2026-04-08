# Dimensions

`fabricpy` supports custom dimension definitions as generated datapack files.

Python methods:

- `mod.add_dimension_type(type_id, data)`
- `mod.add_dimension(dimension_id, dimension_type, generator=None, data=None)`

Generated output:

- `data/<modid>/dimension_type/<type_id>.json`
- `data/<modid>/dimension/<dimension_id>.json`

Dimension type example:

```python
mod.add_dimension_type("pocket", {
    "ultrawarm": False,
    "natural": False,
    "coordinate_scale": 1.0,
    "has_skylight": False,
    "has_ceiling": True,
    "ambient_light": 0.0,
    "fixed_time": 18000,
    "bed_works": True,
    "respawn_anchor_works": False,
    "min_y": 0,
    "height": 256,
    "logical_height": 256,
    "infiniburn": "#minecraft:infiniburn_overworld",
    "effects": "minecraft:overworld"
})
```

Dimension example:

```python
mod.add_dimension(
    "pocket",
    dimension_type="mymod:pocket",
    generator={
        "type": "minecraft:noise",
        "settings": "minecraft:overworld",
        "biome_source": {
            "type": "minecraft:fixed",
            "biome": "minecraft:plains"
        }
    }
)
```

Teleport example:

```python
@mod.event("player_join")
def on_join(ctx):
    ctx.player.teleport_dimension("mymod:pocket", 0, 80, 0)
```

Advanced mode:

- pass `data={...}` to `mod.add_dimension(...)` if you want to provide the full dimension JSON yourself

Runtime note:

- this API creates dimension definitions as datapack content
- that is the clean cross-loader path in this repo
- true hot creation and unloading of arbitrary dimensions during gameplay is not exposed as a stable high-level API here
- for runtime changes, use `ctx.server.run_command(...)` and `ctx.server.reload_data()` if you are working with datapack-backed content
