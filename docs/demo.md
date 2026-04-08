# Demo Mod

`demo.py` is the canonical FabricPy demo mod in this repo.

It is the file that should answer:

- what a small but real FabricPy mod looks like
- what the advanced region looks like without jumping into a project-specific mod
- how the newer compiler/runtime/interoperability layers show up in normal author code

## What `demo.py` Demonstrates

Core content:

- a normal block
- a normal item
- a geo animated entity
- a creative tab
- an advancement
- a command
- a keybind

Advanced runtime:

- a stateful animated block with `uses_block_data = True`
- a translucent animated entity with generated renderer controls
- generated block-entity ticking through `@mc.on_tick`
- generated entity ticking through `@mc.on_tick`
- event-driven logic with `player_use_item`
- animation switching from Python

Advanced compiler/interoperability:

- automatic GeckoLib dependency injection because the animated block uses geo assets
- dependency jar scanning after build
- generated dependency stubs under `.fabricpy_meta/python_stubs/dep/...`
- an explicit `dep.geckolib...RawAnimation.begin()` interop example in a keybind handler

## Main Objects

### `DemoBlock`

This is the simple baseline block.

It demonstrates:

- a normal registered block
- normal texture/model setup
- normal block item model path

### `DemoRelay`

This is the advanced block in the demo.

It demonstrates:

- `has_block_entity = True`
- `uses_block_data = True`
- `geo_model`
- `geo_texture`
- `geo_animations`
- `default_animation`
- `@mc.on_use`
- `@mc.on_tick`
- persistent state through `ctx.block_entity`

### `Pickle`

This is the baseline item.

It demonstrates:

- a straightforward generated item texture path
- food settings
- event usage through `player_use_item`

### `TimeWisp`

This is the advanced entity in the demo.

It demonstrates:

- `mc.Entity`
- generated GeckoLib entity model/rendering
- `geo_model`
- `geo_texture`
- `geo_animations`
- `default_animation`
- translucent rendering
- renderer scale, offset, tint, and alpha controls
- code-driven animation switching in `@mc.on_tick`

## Demo Assets

The animated relay uses:

- `assets/demo/geo/machines/demo_relay.geo.json`
- `assets/demo/animations/machines/demo_relay.animation.json`
- `assets/demo/textures/block/block.png`

The animated entity uses:

- `assets/demo/geo/mobs/time_wisp.bbmodel`
- `assets/demo/animations/mobs/time_wisp.animation.json`
- `assets/demo/textures/entity/mobs/time_wisp.png`

That combination is intentionally simple. The point is to prove the path, not to ship a complicated art asset.

## What to Inspect After Building

Build it with:

```powershell
python .\demo.py
```

Then inspect:

- `.fabricpy_build/demo-fabric/.fabricpy_meta/symbol_index.json`
- `.fabricpy_build/demo-fabric/.fabricpy_meta/python_stubs/dep/geckolib/...`
- `.fabricpy_build/demo-forge/.fabricpy_meta/symbol_index.json`
- `.fabricpy_build/demo-forge/.fabricpy_meta/python_stubs/dep/geckolib/...`

Those outputs show the current dependency interop layer in a clean demo context instead of inside the Playtime mod.
