# Mod API

`mc.Mod(...)` is the root of a FabricPy mod. Everything else hangs off it.

## Constructor

```python
mod = mc.Mod(
    mod_id="playtime",
    name="Playtime",
    version="1.0",
    description="Poppy Playtime demo mod",
    authors=["TheDJStudios"],
    minecraft_version="1.20.1",
    loader="both",
    package="com.generated.playtime",
    website="",
    license="MIT",
)
```

## Constructor Fields

- `mod_id`: lowercase identifier used for registries, assets, lang keys, and generated file names
- `name`: human-facing mod name
- `version`: version string used in generated metadata and jar names
- `description`: short loader/mod-list description
- `authors`: list of author strings
- `minecraft_version`: any version that has installed loader addons
- `loader`: a discovered loader name such as `fabric` or `forge`, plus `both` and `all`

The built-in addon set currently provides:

- `1.20.1`: Fabric, Forge
- `1.21.1`: Fabric, Forge

See [addons.md](./addons.md) for the extension path.
- `package`: optional Java package root; defaults to `com.generated.<mod_id>`
- `website`: optional URL
- `license`: optional license string

## Registration

Supported registration targets:

- `mc.Block`
- `mc.Item`
- `mc.Entity`
- `mc.Mixin`

Direct style:

```python
mod.register(MyBlock)
```

Decorator style:

```python
@mod.register
class MyItem(mc.Item):
    item_id = "my_item"
```

If a class is not registered, it will not be counted during compile and it will not be generated into the loader project.

## Major APIs

- `mod.event(...)`
- `mod.command(...)`
- `mod.add_recipe(...)`
- `mod.shaped_recipe(...)`
- `mod.shapeless_recipe(...)`
- `mod.add_advancement(...)`
- `mod.add_advancement_json(...)`
- `mod.item_advancement(...)`
- `mod.add_sound(...)`
- `mod.creative_tab(...)`
- `mod.keybind(...)`
- `mod.dependency(...)`
- `mod.add_dimension_type(...)`
- `mod.add_dimension(...)`
- `mod.add_structure(...)`
- `mod.compile(...)`

## Minimal Starter Mod

```python
import fabricpy as mc

mod = mc.Mod(
    mod_id="examplemod",
    name="Example Mod",
    minecraft_version="1.20.1",
    loader="both",
)


@mod.register
class ExampleItem(mc.Item):
    item_id = "example_item"
    texture = "tools/example_item"


@mod.register
class ExampleBlock(mc.Block):
    block_id = "example_block"
    texture = "machines/example_block"


@mod.event("player_join")
def on_join(ctx):
    ctx.player.send_message("Example Mod loaded")


if __name__ == "__main__":
    mod.compile()
```

## Recipes

Raw JSON:

```python
mod.add_recipe("parts/gear", {
    "type": "minecraft:crafting_shaped",
    "pattern": [" I ", "IRI", " I "],
    "key": {
        "I": {"item": "minecraft:iron_ingot"},
        "R": {"item": "minecraft:redstone"}
    },
    "result": {"item": "mymod:gear", "count": 1}
})
```

Convenience helper:

```python
mod.shapeless_recipe(
    "scanner_core",
    result="playtime:hand_scanner",
    ingredients=[
        {"item": "minecraft:iron_ingot"},
        {"item": "minecraft:redstone"},
    ],
)
```

## Advancements

```python
mod.item_advancement(
    advancement_id="story/get_scanner",
    title="Field Kit",
    description="Obtain a hand scanner.",
    icon_item="playtime:hand_scanner",
    parent="minecraft:story/root",
)
```

## Creative Tabs

```python
playtime_tab = mod.creative_tab(
    tab_id="playtime_tab",
    title="Playtime",
    icon_item="playtime:grabpack_cannon",
)

playtime_tab.item.add("playtime:hand_scanner")
playtime_tab.item.add("playtime:scanner_relay")
playtime_tab.item.add("playtime:grabpack_cannon")
```

## Keybinds

```python
scanner_ping = mod.keybind(
    keybind_id="scanner_ping",
    title="Scanner Ping",
    key="R",
    category_title="Playtime Controls",
)

@scanner_ping.on_press
def on_scanner_ping(ctx):
    ctx.player.send_action_bar("Scanner pulse primed")
```

## Dependencies

```python
mod.dependency(
    coordinate="com.simibubi.create:create-fabric-1.20.1:0.5.1",
    loader="fabric",
    scope="modImplementation",
    repo="https://maven.tterrag.com/",
    mod_id="create",
    required=True,
)
```

See [dependencies.md](./dependencies.md) and [interop.md](./interop.md) for the advanced side of this system.

## Dimensions and Structures

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
    "effects": "minecraft:overworld",
})
```

```python
mod.add_structure("rooms/test_room", "structures/test_room.nbt")
```

## Compile

```python
if __name__ == "__main__":
    mod.compile()
```

Optional output directory:

```python
mod.compile(output_dir="./out")
```

## Practical Notes

- if you define a class but do not register it, the compiler ignores it
- if a block needs persistent state, use `uses_block_data = True`
- if a block needs GeckoLib animation, use `geo_model`, `geo_texture`, and `geo_animations`
- if you need dependency API exploration, declare dependencies or use a feature that causes them to be added, then inspect `.fabricpy_meta/python_stubs/dep/...`
