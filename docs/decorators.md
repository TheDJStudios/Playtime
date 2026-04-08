# Decorators

`fabricpy` exposes these decorators at the top level:

- `@mc.on_use`
- `@mc.on_right_click`
- `@mc.on_hold`
- `@mc.on_place`
- `@mc.on_break`
- `@mc.on_tick`
- `@mc.inject(...)`

Block hook decorators:

- `@mc.on_use`: block right click
- `@mc.on_place`: block placement hook
- `@mc.on_break`: block break hook
- `@mc.on_tick`: per-tick block hook when the block has a generated block entity

Item hook decorators:

- `@mc.on_right_click`: item use hook
- `@mc.on_hold`: item held hook for selected main hand or offhand

Entity hook decorators:

- `@mc.on_tick`: normal entity tick hook when used on an `mc.Entity` subclass

Mixin decorator:

- `@mc.inject(method, at="HEAD", cancellable=False)`

Example:

```python
@mod.register
class Bell(mc.Block):
    block_id = "bell"

    @mc.on_use
    def on_use(self, ctx):
        ctx.player.send_message("dong")
```

Item hook example:

```python
@mod.register
class BeaconWand(mc.Item):
    item_id = "beacon_wand"

    @mc.on_right_click
    def on_right_click(self, ctx):
        ctx.player.send_action_bar("wand used")
```

Held item hook example:

```python
@mod.register
class Scanner(mc.Item):
    item_id = "scanner"

    @mc.on_hold
    def on_hold(self, ctx):
        if not ctx.world.is_client():
            ctx.player.send_action_bar("scanner active")
```

Entity tick example:

```python
@mod.register
class Sentinel(mc.Entity):
    entity_id = "sentinel"

    @mc.on_tick
    def on_tick(self, ctx):
        if ctx.entity.get_pos_y() < 0:
            ctx.entity.discard()
```
