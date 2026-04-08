# Items

Items have three important tiers:

- ordinary generated items
- custom-model items
- items that carry appearance/runtime state on the stack

## Minimal Item

```python
@mod.register
class Gear(mc.Item):
    item_id = "gear"
    display_name = "Gear"
    texture = "parts/gear"
```

## Core Fields

- `item_id`
- `display_name`
- `max_stack_size`
- `max_damage`
- `rarity`
- `fireproof`
- `food_hunger`
- `food_saturation`
- `food_always_edible`
- `is_tool`
- `tool_type`
- `tool_material`
- `texture`
- `emissive_texture`
- `emissive_level`
- `textures`
- `model`

## Texture Resolution

This Python:

```python
texture = "food/pickle"
```

means:

- source PNG: `assets/<modid>/textures/item/food/pickle.png`
- generated model texture id: `<modid>:item/food/pickle`

Common mistake:

- writing `<modid>:food/pickle` in a manual item model

Correct value:

- `<modid>:item/food/pickle`

## Food Item Example

```python
@mod.register
class Pickle(mc.Item):
    item_id = "pickle"
    display_name = "Pickle"
    texture = "food/pickle"
    food_hunger = 4
    food_saturation = 6
    food_always_edible = True
```

## Custom Model Item Example

```python
@mod.register
class GrabPackCannon(mc.Item):
    item_id = "grabpack_cannon"
    display_name = "GrabPack Cannon"
    max_stack_size = 1
    rarity = "epic"
    model = {
        "parent": "playtime:item/tool/grabpack"
    }
```

## Right-Click Hook

Items support:

- `@mc.on_right_click`
- `@mc.on_hold`

```python
@mod.register
class TeleportAnchor(mc.Item):
    item_id = "teleport_anchor"
    texture = "tools/teleport_anchor"

    @mc.on_right_click
    def on_right_click(self, ctx):
        if not ctx.world.is_client():
            ctx.player.teleport(0, 80, 0)
            ctx.player.send_action_bar("Teleported")
```

## Held Hook

Use `@mc.on_hold` when the logic should run while the item is actively held.

This means:

- selected main hand slot
- offhand

Example:

```python
@mod.register
class SonicProbe(mc.Item):
    item_id = "sonic_probe"
    texture = "tools/sonic_probe"

    @mc.on_hold
    def on_hold(self, ctx):
        if not ctx.world.is_client():
            ctx.player.add_effect("minecraft:night_vision", 1, 0)
```

This hook is not a general inventory scan. It does not fire just because the item exists somewhere in the inventory.

## Stack Appearance Data

Stacks can store appearance keys:

- `ctx.stack.texture_change(texture_id)`
- `ctx.stack.model_change(model_id)`
- `ctx.stack.get_texture()`
- `ctx.stack.get_model()`

These helpers are useful for stateful items and future render systems, but they are not yet a guaranteed universal live item-render mutation path on their own.
