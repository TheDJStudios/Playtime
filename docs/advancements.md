# Advancements

`fabricpy` can generate advancement JSON from Python.

Generated output:

- `data/<modid>/advancements/<advancement_id>.json`

Titles and descriptions passed as plain strings are also written into:

- `assets/<modid>/lang/en_us.json`

and the generated advancement JSON uses translate keys automatically.

## Main API

- `mod.add_advancement(advancement_id, title, description, icon_item, parent=None, criteria=None, rewards=None, background="", frame="task", show_toast=True, announce_to_chat=True, hidden=False)`
- `mod.add_advancement_json(advancement_id, data)`
- `mod.item_advancement(advancement_id, title, description, icon_item, trigger_item=None, parent=None, rewards=None, background="", frame="task", show_toast=True, announce_to_chat=True, hidden=False)`

## Fields

- `advancement_id`: path under `data/<modid>/advancements/`. Slashes are allowed, for example `story/get_scanner`.
- `title`: player-facing title text.
- `description`: player-facing description text.
- `icon_item`: item id used for the advancement icon, for example `minecraft:diamond` or `mymod:scanner`.
- `parent`: optional parent advancement id such as `minecraft:story/root` or `mymod:story/root`.
- `criteria`: raw advancement criteria dict. If omitted, `fabricpy` uses a manual impossible trigger.
- `rewards`: optional raw rewards dict.
- `background`: optional advancement background texture, usually for root advancements.
- `frame`: `task`, `goal`, or `challenge`.
- `show_toast`: whether to show the toast popup.
- `announce_to_chat`: whether completion is announced in chat.
- `hidden`: whether the advancement stays hidden until unlocked.

## Simple example

```python
mod.add_advancement(
    advancement_id="story/root",
    title="Playtime",
    description="Begin investigating the factory.",
    icon_item="playtime:hand_scanner",
    background="minecraft:textures/gui/advancements/backgrounds/stone.png",
    frame="task",
)
```

Goal and challenge examples:

```python
mod.add_advancement(
    advancement_id="story/power_on",
    title="System Online",
    description="Restore power to the facility.",
    icon_item="minecraft:redstone",
    parent="playtime:story/root",
    frame="goal",
)

mod.add_advancement(
    advancement_id="story/master_operator",
    title="Master Operator",
    description="Unlock every scanner door.",
    icon_item="playtime:hand_scanner",
    parent="playtime:story/power_on",
    frame="challenge",
)
```

## Item-based advancement

Use `mod.item_advancement(...)` when the trigger should be "player has this item in inventory".

```python
mod.item_advancement(
    advancement_id="story/get_scanner",
    title="Field Kit",
    description="Obtain a hand scanner.",
    icon_item="playtime:hand_scanner",
    trigger_item="playtime:hand_scanner",
    parent="playtime:story/root",
)
```

If `trigger_item` is omitted, `icon_item` is used as the inventory trigger item.

## Raw JSON example

Use `mod.add_advancement_json(...)` when you want full control.

```python
mod.add_advancement_json(
    "story/power_on",
    {
        "parent": "playtime:story/root",
        "display": {
            "icon": {"item": "minecraft:redstone"},
            "title": {"translate": "advancement.playtime.story.power_on.title"},
            "description": {"translate": "advancement.playtime.story.power_on.description"},
            "frame": "goal",
            "show_toast": True,
            "announce_to_chat": True,
            "hidden": False,
        },
        "criteria": {
            "powered": {
                "trigger": "minecraft:impossible"
            }
        }
    }
)
```

## Path rules

- `playtime:story/root` is a full advancement id.
- `story/root` is a path under your mod namespace when used as the generated file name.
- `parent` should usually be a full namespaced id if it refers to another mod or to vanilla.

## Notes

- `fabricpy` generates the JSON; repo files under `data/<modid>/advancements/...` still override generated files if you place your own.
- `mod.add_advancement(...)` does not currently create custom triggers by itself. For complex criteria, pass raw JSON through `criteria=` or use `add_advancement_json(...)`.

## Player-side helpers

Generated advancements can also be checked and controlled from `ctx.player`:

- `ctx.player.has_advancement("mymod:story/root")`
- `ctx.player.grant_advancement("mymod:story/root")`
- `ctx.player.revoke_advancement("mymod:story/root")`

Example:

```python
@mod.event("player_join")
def ensure_root(ctx):
    if not ctx.player.has_advancement("playtime:story/root"):
        ctx.player.grant_advancement("playtime:story/root")
```

These helpers expect full advancement ids in `namespace:path` form.
