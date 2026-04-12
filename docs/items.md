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
- `bundle_inventory`
- `inventory_slots`
- `inventory_slot_capacity`
- `inventory_total_capacity`
- `inventory_visible_in_tooltip`
- `inventory_tooltip_show_empty`
- `inventory_tooltip_slot_limit`
- `inventory_insert_from_offhand`
- `inventory_extract_from_use`
- `inventory_extract_requires_sneak`
- `inventory_extract_order`
- `inventory_whitelist`
- `inventory_blacklist`
- `inventory_slot_whitelists`
- `inventory_slot_blacklists`
- `inventory_slot_labels`
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

## Bundle-Style Item Inventory

Set `bundle_inventory = True` to make an item behave like a vanilla bundle.

```python
@mod.register
class ToolSatchel(mc.Item):
    item_id = "tool_satchel"
    display_name = "Tool Satchel"
    texture = "bags/tool_satchel"
    bundle_inventory = True
```

What this does:

- the generated item class extends Minecraft's `BundleItem`
- the item stores other item stacks inside itself
- the item uses the normal bundle-style inventory interactions and tooltip behavior
- `max_stack_size` is forced to `1` while this is enabled

What this does not do:

- it does not generate a chest-style menu screen
- it is not a general custom container API yet

## Managed Slot Item Inventory

Set `inventory_slots` above `0` to use FabricPy's managed item inventory instead of vanilla bundle behavior.

```python
@mod.register
class ToolSatchel(mc.Item):
    item_id = "tool_satchel"
    display_name = "Tool Satchel"
    texture = "bags/tool_satchel"

    inventory_slots = 6
    inventory_slot_capacity = 16
    inventory_total_capacity = 48
    inventory_visible_in_tooltip = True
    inventory_tooltip_show_empty = True
    inventory_tooltip_slot_limit = 6
    inventory_insert_from_offhand = True
    inventory_extract_from_use = True
    inventory_extract_requires_sneak = True
    inventory_extract_order = "last"

    inventory_whitelist = [
        "minecraft:apple",
        "minecraft:coal",
        "minecraft:stick",
    ]
    inventory_slot_whitelists = {
        1: ["minecraft:coal"],
        2: ["minecraft:stick"],
    }
    inventory_slot_labels = {
        0: "Input",
        1: "Fuel",
        2: "Core",
    }
```

What this does:

- stores items in numbered internal slots on the stack itself
- shows slot contents in the tooltip
- supports per-item and per-slot allow/block filters
- inserts from the opposite hand on use
- extracts from the configured slot order on use
- forces `max_stack_size` to `1`

Important behavior:

- if `inventory_slots > 0`, this managed inventory path takes precedence over `bundle_inventory`
- slot dictionaries are zero-based
- extraction normally happens while sneaking by default
- this is still not a chest-style menu screen; it is a stack-carried inventory with built-in use behavior

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
