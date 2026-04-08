# Recipes

Recipes can be defined directly from Python or placed in repo data files.

Python methods:

- `mod.add_recipe(recipe_id, data)`
- `mod.shaped_recipe(recipe_id, result, pattern, key, count=1)`
- `mod.shapeless_recipe(recipe_id, result, ingredients, count=1)`

Raw JSON:

```python
mod.add_recipe("pickle", {
    "type": "minecraft:crafting_shapeless",
    "ingredients": [
        {"item": "minecraft:slime_ball"}
    ],
    "result": {
        "item": "mymod:pickle",
        "count": 1
    }
})
```

Shaped helper:

```python
mod.shaped_recipe(
    "pickle_block",
    result="mymod:pickle_block",
    pattern=[
        "PPP",
        "PPP",
        "PPP",
    ],
    key={
        "P": {"item": "mymod:pickle"}
    },
    count=1,
)
```

Shapeless helper:

```python
mod.shapeless_recipe(
    "pickle",
    result="mymod:pickle",
    ingredients=[
        {"item": "minecraft:slime_ball"}
    ],
    count=1,
)
```

Smelting-style raw recipe example:

```python
mod.add_recipe("steel_ingot_from_smelting", {
    "type": "minecraft:smelting",
    "ingredient": {"item": "mymod:raw_steel"},
    "result": "mymod:steel_ingot",
    "experience": 0.7,
    "cookingtime": 200
})
```

Stonecutter example:

```python
mod.add_recipe("steel_tiles_from_cutting", {
    "type": "minecraft:stonecutting",
    "ingredient": {"item": "mymod:steel_block"},
    "result": "mymod:steel_tiles",
    "count": 4
})
```

Repo data files:

- `data/<modid>/recipes/...`

Compile behavior:

- Python-defined recipes are generated first
- repo files are copied after generation
- repo files override generated recipes when paths collide
