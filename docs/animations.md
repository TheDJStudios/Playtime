# Programmed Animations

`fabricpy` now supports programmed GeckoLib-backed animation for both blocks and entities.

Use this when you need:

- element movement
- stretching or scaling
- bone rotation
- switching between named animations from Python
- transparent or translucent animated props
- runtime texture/model swaps for animated actors

This is the correct route for real animated model parts. Static block JSON alone cannot do that.

## Python Fields For Animated Blocks

Animated blocks use these `mc.Block` fields:

- `geo_model`
- `geo_texture`
- `geo_animations`
- `default_animation`
- `render_layer`

`render_layer` can be:

- `solid`
- `cutout`
- `cutout_mipped`
- `translucent`

Use `translucent` for things like glass consoles, holograms, time-rotor parts, and other semi-transparent Doctor Who style props.

## Python Fields For Animated Entities

Animated entities use these `mc.Entity` fields:

- `geo_model`
- `geo_texture`
- `geo_animations`
- `default_animation`
- `render_layer`
- `shadow_radius`
- `render_scale_x`
- `render_scale_y`
- `render_scale_z`
- `render_offset_x`
- `render_offset_y`
- `render_offset_z`
- `render_tint_r`
- `render_tint_g`
- `render_tint_b`
- `render_tint_a`

## Minimal Animated Block Example

```python
@mod.register
class AnimatedPanel(mc.Block):
    block_id = "animated_panel"
    display_name = "Animated Panel"
    has_block_entity = True
    opaque = False
    render_layer = "translucent"

    geo_model = "machines/animated_panel"
    geo_texture = "machines/animated_panel"
    geo_animations = "machines/animated_panel"
    default_animation = "idle"

    @mc.on_use
    def on_use(self, ctx):
        ctx.block_entity.play_animation("open")
```

## Minimal Animated Entity Example

```python
@mod.register
class TimeWisp(mc.Entity):
    entity_id = "time_wisp"
    display_name = "Time Wisp"
    render_layer = "translucent"
    shadow_radius = 0.15
    render_scale_x = 0.85
    render_scale_y = 0.85
    render_scale_z = 0.85
    render_offset_y = 0.1
    render_tint_r = 0.85
    render_tint_g = 0.95
    render_tint_b = 1.0
    render_tint_a = 0.9

    geo_model = "mobs/time_wisp"
    geo_texture = "mobs/time_wisp"
    geo_animations = "mobs/time_wisp"
    default_animation = "controller.float"

    @mc.on_tick
    def on_tick(self, ctx):
        if ctx.entity.get_pos_y() < 64:
            ctx.entity.play_animation("controller.rise")
```

## Resource Layout

For this Python setup:

```python
geo_model = "machines/animated_panel"
geo_texture = "machines/animated_panel"
geo_animations = "machines/animated_panel"
```

the expected block files are:

- `assets/<modid>/geo/machines/animated_panel.geo.json` or `assets/<modid>/geo/machines/animated_panel.bbmodel`
- `assets/<modid>/textures/block/machines/animated_panel.png`
- `assets/<modid>/animations/machines/animated_panel.animation.json`

Animated entities use:

- `assets/<modid>/geo/<path>.geo.json` or `assets/<modid>/geo/<path>.bbmodel`
- `assets/<modid>/textures/entity/<path>.png`
- `assets/<modid>/animations/<path>.animation.json`

When you use `.bbmodel`, FabricPy converts it to a generated `.geo.json` during compile. That lets you keep the Blockbench project file as the source of truth instead of exporting the model by hand every time.

For translucent or spectral entities, prefer:

```python
render_layer = "translucent"
render_tint_a = 0.9
```

For crisp masked parts, prefer:

```python
render_layer = "cutout"
```

## Animation Control

### Block Entity Animation Control

Available on `ctx.block_entity` for animated blocks:

- `ctx.block_entity.get_animation()`
- `ctx.block_entity.play_animation(name)`
- `ctx.block_entity.play_animation_once(name)`
- `ctx.block_entity.stop_animation()`

Examples:

```python
@mc.on_use
def on_use(self, ctx):
    ctx.block_entity.play_animation("open")
```

```python
@mc.on_use
def on_use(self, ctx):
    ctx.block_entity.play_animation_once("press")
```

```python
@mc.on_break
def on_break(self, ctx):
    ctx.block_entity.stop_animation()
```

### Entity Animation Control

Available on `ctx.entity` for animated entities:

- `ctx.entity.get_animation()`
- `ctx.entity.play_animation(name)`
- `ctx.entity.play_animation_once(name)`
- `ctx.entity.stop_animation()`
- `ctx.entity.get_texture()`
- `ctx.entity.texture_change(texture_id)`
- `ctx.entity.get_model()`
- `ctx.entity.model_change(model_id)`

Example:

```python
@mc.on_tick
def on_tick(self, ctx):
    if ctx.entity.get_pos_y() < 64:
        ctx.entity.play_animation("controller.alert")
        ctx.entity.texture_change("mymod:textures/entity/mobs/time_wisp_alert.png")
```

## Runtime Model And Texture Swaps

Animated blocks and animated entities can now switch model and texture paths from code.

Block side:

- `ctx.block_entity.texture_change(resource_id)`
- `ctx.block_entity.model_change(resource_id)`

Entity side:

- `ctx.entity.texture_change(resource_id)`
- `ctx.entity.model_change(resource_id)`

The values are resource ids pointing at the generated/runtime assets, for example:

- `mymod:textures/block/terminals/console_glow.png`
- `mymod:geo/terminals/console_open.geo.json`
- `mymod:textures/entity/mobs/time_wisp_alert.png`

This is useful for:

- swapping a scanner from idle to alert visuals
- changing a console shell when a state changes
- changing an entity to a damaged or phased visual state

The animation file path is still fixed per class right now. The runtime swaps are for model and texture, not the animation JSON file itself.

## Stateful Example

```python
@mod.register
class ReactorDoor(mc.Block):
    block_id = "reactor_door"
    display_name = "Reactor Door"
    has_block_entity = True
    uses_block_data = True
    opaque = False

    geo_model = "doors/reactor_door"
    geo_texture = "doors/reactor_door"
    geo_animations = "doors/reactor_door"
    default_animation = "idle_closed"

    @mc.on_use
    def on_use(self, ctx):
        is_open = ctx.block_entity.get_bool("open")
        if is_open:
            ctx.block_entity.set_bool("open", False)
            ctx.block_entity.play_animation("close")
        else:
            ctx.block_entity.set_bool("open", True)
            ctx.block_entity.play_animation("open")
        ctx.block_entity.sync()
```

## Transparent Props

For transparent animated props, set:

```python
opaque = False
render_layer = "translucent"
```

That tells the generated renderer to use a translucent render path instead of the default solid path.

Use `cutout` instead when:

- the texture uses hard alpha edges
- you want crisp masked transparency
- the prop is not semi-transparent glass

Examples:

- `translucent`: time rotor tubes, holograms, glowing glass cylinders
- `cutout`: grilles, punched panels, masked emissive overlays

## Notes

- animated blocks automatically get a backing block entity and client renderer
- animated entities automatically get a GeckoLib entity renderer when geo fields are present
- generated entity renderers now honor render-layer, scale, offset, tint, and alpha settings
- `has_block_entity = True` is still recommended for readability
- the motion itself is authored in Blockbench/GeckoLib animation JSON
- Python controls when animations start, stop, switch, and now also swap model/texture resources
- generated projects add GeckoLib automatically when animated blocks are present
- generated projects also add GeckoLib automatically for animated entities
- item-side GeckoLib animation is still not first-class yet
