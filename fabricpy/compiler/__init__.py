"""
Main compiler entry point.

Called by Mod.compile(). Generates Fabric and/or Forge project trees,
then invokes Gradle to produce .jar files.
"""

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fabricpy.mod import Mod


def compile_mod(mod: "Mod", output_dir: str = "./dist", clean: bool = False):
    """
    Compile a Mod into .jar files.

    Steps:
      1. Validate the mod definition
      2. Generate loader project(s)
      4. Run Gradle build(s)
      5. Copy output .jar(s) to output_dir
    """
    from fabricpy.compiler.jar_scanner import build_symbol_index_for_project
    from fabricpy.addons import resolve_addon

    _validate(mod)

    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    gen_root = Path(".fabricpy_build").resolve()
    gen_root.mkdir(exist_ok=True)

    loaders = _resolve_loaders(mod.loader, mod.minecraft_version)

    print(f"[fabricpy] Compiling {mod.name!r} v{mod.version} -> {loaders}")
    print(f"  Blocks:   {len(mod._blocks)}")
    print(f"  Items:    {len(mod._items)}")
    print(f"  Entities: {len(mod._entities)}")
    print(f"  Events:   {len(mod._events)}")
    print(f"  Commands: {len(mod._commands)}")
    print(f"  Mixins:   {len(mod._mixins)}")
    print(f"  Recipes:  {len(mod._recipes)}")
    print(f"  Advancements: {len(mod._advancements)}")
    print(f"  Sounds:   {len(mod._sounds)}")
    print(f"  Creative Tabs: {len(mod._creative_tabs)}")
    print(f"  Keybinds: {len(mod._keybinds)}")
    print(f"  Packets:  {len(mod._packets)}")
    print(f"  Screens:  {len(mod._screens)}")
    print(f"  Dependencies: {len(mod._dependencies)}")
    print(f"  Dimension Types: {len(mod._dimension_types)}")
    print(f"  Dimensions:      {len(mod._dimensions)}")
    print(f"  Structures:      {len(mod._structures)}")
    print()

    results = {}

    for loader in loaders:
        addon = resolve_addon("loader", loader, mod.minecraft_version)
        if addon is None:
            raise ValueError(
                f"No loader addon found for loader={loader!r} minecraft_version={mod.minecraft_version!r}."
            )

        project_dir = gen_root / f"{mod.mod_id}-{loader}"
        addon.generate_project(mod, project_dir)
        success = addon.build_project(project_dir, mod.minecraft_version, clean=clean, output_dir=out)
        results[loader] = success
        if success:
            try:
                build_symbol_index_for_project(project_dir)
                print(f"[fabricpy] Interop index written: {project_dir / '.fabricpy_meta' / 'symbol_index.json'}")
            except Exception as exc:
                print(f"[fabricpy] Warning: interop index generation failed for {loader}: {exc}")

    print()
    print("=" * 50)
    print(f"[fabricpy] Compilation complete for {mod.name}")
    for loader, ok in results.items():
        status = "SUCCESS" if ok else "FAILED (source generated, check errors above)"
        print(f"  {loader.upper():8} {status}")
    if any(results.values()):
        print(f"  Output: {out}")
    print("=" * 50)


def _resolve_loaders(loader: str, minecraft_version: str) -> list[str]:
    from fabricpy.addons import supported_targets

    loader = loader.lower().strip()

    supported = supported_targets("loader", minecraft_version)
    if not supported:
        raise ValueError(
            f"No loader addons found for minecraft_version={minecraft_version!r}."
        )

    alias_map = {
        "both": [name for name in ("fabric", "forge") if name in supported],
        "all": list(supported),
    }

    if loader in alias_map:
        return alias_map[loader]

    requested = [part.strip() for part in loader.replace("+", ",").split(",") if part.strip()]
    if not requested:
        raise ValueError("loader is required")

    invalid = [name for name in requested if name not in supported]
    if invalid:
        raise ValueError(
            f"Invalid loader(s) for Minecraft {minecraft_version}: {invalid!r}. "
            f"Supported loaders: {supported!r}."
        )

    seen = []
    for name in requested:
        if name not in seen:
            seen.append(name)
    return seen


def _validate(mod: "Mod"):
    """Basic sanity checks before compiling."""
    errors = []

    if not mod.mod_id:
        errors.append("mod_id is required")
    if not mod.name:
        errors.append("name is required")
    for block in mod._blocks:
        if not block.block_id:
            errors.append(f"{block.__name__} is missing block_id")
    for item in mod._items:
        if not item.item_id:
            errors.append(f"{item.__name__} is missing item_id")
    for entity in mod._entities:
        if not entity.entity_id:
            errors.append(f"{entity.__name__} is missing entity_id")
    for mx in mod._mixins:
        if not mx.target_class:
            errors.append(f"{mx.__name__} is missing target_class")
    for structure in mod._structures:
        if not Path(structure["path"]).exists():
            errors.append(f"structure source file does not exist: {structure['path']}")

    if errors:
        raise ValueError(
            "Mod definition has errors:\n" + "\n".join(f"  - {e}" for e in errors)
        )
