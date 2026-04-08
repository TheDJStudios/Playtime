# Entities

Create an entity by subclassing `mc.Entity` and registering it with the mod.

```python
@mod.register
class PocketSentinel(mc.Entity):
    entity_id = "pocket_sentinel"
    display_name = "Pocket Sentinel"
    width = 0.8
    height = 2.1
    tracking_range = 10
    update_rate = 3
    spawn_group = "misc"
    fireproof = False
    summonable = True
    max_health = 30.0
    movement_speed = 0.3
    attack_damage = 4.0
    follow_range = 24.0
    knockback_resistance = 0.2

    @mc.on_tick
    def on_tick(self, ctx):
        if ctx.entity.get_pos_y() < 0:
            ctx.entity.discard()
```

Animated entity example:

```python
@mod.register
class TimeWisp(mc.Entity):
    entity_id = "time_wisp"
    display_name = "Time Wisp"
    width = 0.8
    height = 0.8
    render_layer = "translucent"
    shadow_radius = 0.15

    geo_model = "mobs/time_wisp"
    geo_texture = "mobs/time_wisp"
    geo_animations = "mobs/time_wisp"
    default_animation = "controller.float"
    render_scale_x = 0.85
    render_scale_y = 0.85
    render_scale_z = 0.85
    render_offset_y = 0.1
    render_tint_r = 0.85
    render_tint_g = 0.95
    render_tint_b = 1.0
    render_tint_a = 0.9

    @mc.on_tick
    def on_tick(self, ctx):
        if ctx.entity.get_pos_y() < 64:
            ctx.entity.play_animation("controller.rise")
            ctx.entity.texture_change("mymod:textures/entity/mobs/time_wisp_alert.png")
```

Registry fields:

- `entity_id`: required registry id
- `display_name`: optional in-game name
- `namespace`: set automatically from `mod_id`

Size and networking fields:

- `width`: entity hitbox width
- `height`: entity hitbox height
- `tracking_range`: how far away clients keep tracking the entity
- `update_rate`: network update interval
- `spawn_group`: one of `misc`, `creature`, `monster`, `ambient`, `water_creature`, `water_ambient`, `underground_water_creature`, `axolotls`
- `fireproof`: register the entity as fire-immune when the loader supports it
- `summonable`: Python-side metadata for intent; the current generators do not yet change registration based on this flag
- `render_layer`: `solid`, `cutout`, `cutout_mipped`, or `translucent`
- `shadow_radius`: client shadow size used by generated geo entity renderers
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

Animation fields:

- `geo_model`
- `geo_texture`
- `geo_animations`
- `default_animation`

When those geo fields are present, FabricPy generates a GeckoLib entity renderer automatically.

Renderer controls:

- scale fields resize the rendered geo model without changing the server hitbox
- offset fields move the rendered model relative to the entity origin
- tint fields multiply the final rendered color and alpha

That means you can do things like:

- shrink or enlarge an entity model while keeping the same collision box
- float a hologram slightly above its logical position
- fade an entity with `render_tint_a`
- color-shift an entity without authoring another texture

Attribute fields:

- `max_health`
- `movement_speed`
- `attack_damage`
- `follow_range`
- `knockback_resistance`

Current generated Java shape:

- Fabric generates a `PathAwareEntity`
- Forge generates a `PathfinderMob`
- a basic attribute builder is generated from the fields above
- no default AI goals are generated yet
- when `geo_model` is present, a generated GeckoLib renderer and GeckoLib model class are also emitted

Hooks:

- `@mc.on_tick`

`@mc.on_tick` on an entity maps to the Java entity `tick()` method. In that hook:

- `ctx.entity` is the current entity
- `ctx.world` is the owning world/level
- `ctx.pos` is the current block position

Useful context helpers:

- `ctx.entity.get_pos_x()`
- `ctx.entity.get_pos_y()`
- `ctx.entity.get_pos_z()`
- `ctx.entity.teleport(x, y, z)`
- `ctx.entity.discard()`
- `ctx.entity.set_on_fire(seconds)`
- `ctx.entity.damage(amount)`
- `ctx.entity.get_animation()`
- `ctx.entity.play_animation(name)`
- `ctx.entity.play_animation_once(name)`
- `ctx.entity.stop_animation()`
- `ctx.entity.get_texture()`
- `ctx.entity.texture_change(resource_id)`
- `ctx.entity.get_model()`
- `ctx.entity.model_change(resource_id)`
- `ctx.world.spawn_entity(entity_id, x, y, z)`

Spawn example:

```python
@mod.event("player_join")
def on_join(ctx):
    if not ctx.world.is_client():
        ctx.world.spawn_entity("mymod:pocket_sentinel", 0, 80, 0)
```

Command summon example:

```python
@mod.command("spawn_time_wisp")
def spawn_time_wisp(ctx):
    ctx.source.run_command("summon mymod:time_wisp ~ ~1 ~")
```

Geo asset layout for the `TimeWisp` example above:

- `assets/mymod/geo/mobs/time_wisp.geo.json` or `assets/mymod/geo/mobs/time_wisp.bbmodel`
- `assets/mymod/textures/entity/mobs/time_wisp.png`
- `assets/mymod/animations/mobs/time_wisp.animation.json`

`.bbmodel` support:

- if a `.bbmodel` file exists under `assets/<modid>/geo/...`, FabricPy compiles it into the `.geo.json` GeckoLib expects during mod generation
- `geo_model = "mobs/time_wisp"` works with either source file
- `geo_model = "mobs/time_wisp.bbmodel"` also works
- this path currently imports the model geometry and bone hierarchy
- keep textures as normal PNG assets and animations as normal `.animation.json` files

Notes:

- `ctx.world.spawn_entity(...)` uses Minecraft's summon command under the hood
- plain non-geo entities still use the normal generated entity class path
- geo entities now get generated client renderers, runtime animation hooks, render-layer selection, scale/offset/tint control, and runtime model/texture switching
- fully arbitrary handwritten non-Gecko renderer authoring is still not a first-class Python API
