# Building

`fabricpy` generates a real loader project under `.fabricpy_build/`, then runs Gradle to produce jars in `dist/`.

That means there are always two layers to keep in mind:

- your Python mod source
- the generated loader projects and their normal Java/Gradle build rules

Loader support now comes from addons under `fabricpy/addons/...`.

## Requirements

- Python `3.10+`
- Java `17` for Minecraft `1.20.1`
- Java `21` for Minecraft `1.21.1`
- Gradle available for the first wrapper bootstrap, or an existing wrapper jar that can be reused

## JDK Selection

`fabricpy` now tries to pick a matching JDK automatically.

Version rules:

- Minecraft `1.20.1` prefers Java `17`
- Minecraft `1.21.1` prefers Java `21`

Discovery order:

- `JAVA_HOME`
- `JDK*_HOME` environment variables
- common Windows JDK install locations
- `PATH`

Important note:

- you can install Java 17 and Java 21 side by side
- `fabricpy` will try to choose the correct one for the selected Minecraft version
- this is better than manually swapping JDKs on and off `PATH`

## Gradle Selection

Gradle wrapper selection is automatic per loader/version combination:

- Fabric `1.20.1`: Gradle `8.8`
- Fabric `1.21.1`: Gradle `8.8`
- Forge `1.20.1`: Gradle `8.8`
- Forge `1.21.1`: Gradle `9.3.0`

## Basic Compile Flow

Minimal pattern:

```python
import fabricpy as mc

mod = mc.Mod(
    mod_id="examplemod",
    name="Example Mod",
    minecraft_version="1.20.1",
    loader="both",
)

if __name__ == "__main__":
    mod.compile()
```

Run it from PowerShell:

```powershell
python .\my_mod.py
```

## What `mod.compile()` Actually Does

1. validates the Python mod definition
2. resolves target loaders from `loader` and `minecraft_version`
3. resolves the best loader addon for each requested loader
4. generates loader projects in `.fabricpy_build/<modid>-<loader>`
5. copies repo `assets/` and `data/` into generated resources
6. runs the addon build step in each generated project
7. copies built jars into `dist/`
8. emits interop metadata and dependency stub output under `.fabricpy_meta/`

## Generated Output

Per-loader generated projects:

- `.fabricpy_build/<modid>-fabric/`
- `.fabricpy_build/<modid>-forge/`

Built jars:

- `dist/<modid>-<version>.jar`
- `dist/<modid>-forge-<version>.jar`

Interop/compiler metadata:

- `.fabricpy_build/<modid>-<loader>/.fabricpy_meta/interop_project.json`
- `.fabricpy_build/<modid>-<loader>/.fabricpy_meta/symbol_index.stub.json`
- `.fabricpy_build/<modid>-<loader>/.fabricpy_meta/symbol_index.json`
- `.fabricpy_build/<modid>-<loader>/.fabricpy_meta/python_stubs/dep/...`

## Addon-backed Loader Support

Built-in loader support is now provided through addon folders inside `fabricpy/addons/...`.

See [addons.md](./addons.md) for:

- the addon file layout
- the required `addon.py` fields
- loader override priority
- how to add custom loader/version support

## Repo Asset and Data Layout

Textures, models, blockstates, lang, and sounds should live under:

- `assets/<modid>/textures/...`
- `assets/<modid>/models/...`
- `assets/<modid>/blockstates/...`
- `assets/<modid>/lang/...`
- `assets/<modid>/sounds.json`
- `assets/<modid>/sounds/...`

Recipes, advancements, dimensions, and structures should live under:

- `data/<modid>/recipes/...`
- `data/<modid>/advancements/...`
- `data/<modid>/dimension_type/...`
- `data/<modid>/dimension/...`
- `data/<modid>/structures/...`

## Troubleshooting

### Wrong Java version

- Java 17 installed for `1.20.1`
- Java 21 installed for `1.21.1`
- `JAVA_HOME` is not forcing the wrong JDK globally

### Wrong model or texture in-game

Most common cause:

- a manual file under `assets/<modid>/models/...` or `assets/<modid>/blockstates/...` is overriding the generated JSON

### Missing block particles

Cause:

- manual block model JSON is missing a `particle` texture entry

### Item texture missing

Cause:

- manual model uses `<modid>:food/foo` instead of `<modid>:item/foo`

### Dependency interop output missing

- the build may have had no scan-worthy dependency jars
- non-geo builds with no explicit dependencies will often have an empty dependency symbol index, which is expected
