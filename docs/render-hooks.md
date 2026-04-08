# Render Hooks

`fabricpy` now has a real generated render layer for animated GeckoLib-backed blocks and entities.

This is not a free-form manual Java renderer callback API yet, but it is enough to control the most important rendering behavior from Python.

## Current Render Controls

On `mc.Block`:

- `render_layer`
- `opaque`
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
- `geo_model`
- `geo_texture`
- `geo_animations`

On `mc.Entity`:

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
- `geo_model`
- `geo_texture`
- `geo_animations`

## Render Layer Options

Supported values:

- `solid`
- `cutout`
- `cutout_mipped`
- `translucent`

Examples:

```python
render_layer = "solid"
```

```python
opaque = False
render_layer = "translucent"
```

Use `translucent` for:

- glass tubes
- holograms
- semi-transparent sci-fi props
- Doctor Who style transparent animated pieces

Use `cutout` for:

- masked grilles
- hard-edged alpha textures
- panel details with transparent holes

## Generated Renderer Behavior

When a block or entity uses geo fields, FabricPy now generates:

- a GeckoLib model class
- a GeckoLib renderer class
- renderer registration
- render-layer selection from `render_layer`
- renderer-space translation from `render_offset_*`
- renderer-space scaling from `render_scale_*`
- final model tint and alpha from `render_tint_*`

That means transparency behavior is no longer stuck at a single default path.

Example:

```python
render_layer = "translucent"
render_scale_x = 0.9
render_scale_y = 0.9
render_scale_z = 0.9
render_offset_y = 0.15
render_tint_r = 0.85
render_tint_g = 0.95
render_tint_b = 1.0
render_tint_a = 0.9
```

This is useful for:

- holograms
- floating spirits
- glass or phased machinery
- subtle per-variant color grading without extra textures

## Runtime Visual Changes

Animated block entities and animated entities can now switch:

- animation
- texture
- model

from Python code.

Helpers:

- `ctx.block_entity.texture_change(resource_id)`
- `ctx.block_entity.model_change(resource_id)`
- `ctx.block_entity.play_animation(name)`
- `ctx.entity.texture_change(resource_id)`
- `ctx.entity.model_change(resource_id)`
- `ctx.entity.play_animation(name)`

## Current Boundary

What is done:

- generated block geo renderers
- generated entity geo renderers
- explicit render-layer control
- generated scale, offset, tint, and alpha control
- runtime model/texture/animation switching

What is not done yet:

- arbitrary handwritten render callbacks from Python
- custom non-Gecko renderer authoring as a first-class API
- beam/cable rendering helpers
