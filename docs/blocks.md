# Blocks

Blocks now span three levels of complexity:

- simple registry/data blocks
- stateful blocks with persistent data
- animated blocks with generated block entities and GeckoLib renderers

## Minimal Block

```python
@mod.register
class SteelBlock(mc.Block):
    block_id = "steel_block"
    display_name = "Steel Block"
    hardness = 2.0
    resistance = 6.0
    texture = "storage/steel_block"
```

## Core Fields

Registry and display:

- `block_id`
- `display_name`
- `namespace`

Physical behavior:

- `hardness`
- `resistance`
- `luminance`
- `slipperiness`
- `material`
- `sound_group`
- `requires_tool`
- `drops_self`
- `opaque`
- `collidable`

State/runtime:

- `has_block_entity`
- `uses_block_data`
- `variable_rotation`
- `rotation_mode`
- `model_collision`

Asset/model fields:

- `texture`
- `textures`
- `model`
- `blockstate`
- `item_model`
- `emissive_texture`
- `emissive_level`
- `emissive_textures`
- `emissive_model`
- `wall_model`
- `floor_model`
- `geo_model`
- `geo_texture`
- `geo_animations`
- `default_animation`

## Hooks

- `@mc.on_use`
- `@mc.on_place`
- `@mc.on_break`
- `@mc.on_tick`

## Persistent Block Data

If a block needs state like mode, owner, color, usage count, or power state, use:

```python
uses_block_data = True
```

Example:

```python
@mod.register
class ScannerRelay(mc.Block):
    block_id = "scanner_relay"
    uses_block_data = True
    has_block_entity = True
    opaque = False

    @mc.on_use
    def on_use(self, ctx):
        count = ctx.block_entity.get_int("uses")
        ctx.block_entity.set_int("uses", count + 1)
        ctx.block_entity.set_bool("powered", True)
        ctx.block_entity.sync()
```

## Rotation

Use:

```python
variable_rotation = True
rotation_mode = "wall"
```

or:

```python
variable_rotation = True
rotation_mode = "floor"
```

Meaning:

- authored model is assumed to face north
- `wall` means upright wall-style handling
- `floor` means floor-placement handling before directional rotation

## Model Collision

Use:

```python
model_collision = True
```

when you want the generated collision/outline shape to follow the model cuboids instead of a full cube.

## Emissive Overlays

Blocks support a separate emissive texture:

```python
emissive_texture = "machines/reactor_lamp_em"
emissive_level = 191
```

Authoring pattern:

- base texture contains the full visible surface
- emissive texture keeps only the glowing pixels
- non-glowing pixels should be transparent

## Animated Blocks

Animated blocks use GeckoLib-backed generation.

```python
@mod.register
class ScannerRelay(mc.Block):
    block_id = "scanner_relay"
    has_block_entity = True
    uses_block_data = True
    opaque = False
    geo_model = "terminals/scanner_relay"
    geo_texture = "playtime/red_right"
    geo_animations = "terminals/scanner_relay"
    default_animation = "controller.idle"

    @mc.on_use
    def on_use(self, ctx):
        ctx.block_entity.play_animation_once("controller.scan")
```

Expected assets:

- `assets/<modid>/geo/...`
- `assets/<modid>/textures/block/...`
- `assets/<modid>/animations/...`
