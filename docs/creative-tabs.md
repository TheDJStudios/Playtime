# Creative Tabs

`fabricpy` can generate custom creative tabs for Fabric and Forge.

Use `mod.creative_tab(...)` to create the tab, then add items into it through the tab builder.

## Main API

- `tab = mod.creative_tab(tab_id, title, icon_item)`
- `tab.item.add(item_id)`
- `tab.set_title(title)`
- `tab.set_icon(item_id)`

## Fields

- `tab_id`: registry path for the tab, for example `tools` or `playtime/tools`.
- `title`: player-facing tab name.
- `icon_item`: item id used as the tab icon.

## Adding entries

```python
tools_tab = mod.creative_tab(
    tab_id="tools",
    title="Playtime Tools",
    icon_item="playtime:hand_scanner",
)

tools_tab.item.add("playtime:hand_scanner")
tools_tab.item.add("playtime:security_chip")
tools_tab.item.add("minecraft:redstone")
```

`tab.item.add(...)` accepts:

- full item ids like `minecraft:redstone`
- your own item ids like `playtime:hand_scanner`
- bare ids like `hand_scanner`, which are treated as `<modid>:hand_scanner`

## Changing title and icon

```python
tools_tab.set_title("Playtime Equipment")
tools_tab.set_icon("playtime:advanced_scanner")
```

Multiple tabs example:

```python
tools_tab = mod.creative_tab("tools", "Tools", "playtime:hand_scanner")
tools_tab.item.add("playtime:hand_scanner")
tools_tab.item.add("playtime:grabpack_cannon")

blocks_tab = mod.creative_tab("blocks", "Blocks", "playtime:hand_scanner")
blocks_tab.item.add("playtime:hand_scanner")
```

## Generated language key

`fabricpy` writes the tab title into:

- `itemGroup.<modid>.<tab_id_with_slashes_replaced_by_dots>`

For example:

- `itemGroup.playtime.tools`
- `itemGroup.playtime.lab.scanners`

## Generated behavior

- Fabric: a custom `ItemGroup` is registered with the listed entries.
- Forge: a custom `CreativeModeTab` is registered with the listed entries.

## Notes

- The generated tab only contains the items you add explicitly.
- This does not replace vanilla tabs like Ingredients or Building Blocks.
- If you want an item in your custom tab and in a vanilla tab, keep the normal generated item registration and also add it to your tab.
- Repo assets and lang files can still override generated output if needed.
