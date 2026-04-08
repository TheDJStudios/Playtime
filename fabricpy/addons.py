from __future__ import annotations

from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Callable


@dataclass(frozen=True)
class Addon:
    kind: str
    target: str
    minecraft_version: str
    name: str
    module: ModuleType
    path: Path
    priority: int = 0

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.kind, self.target, self.minecraft_version)

    @property
    def build_label(self) -> str:
        return self.target

    def generate_project(self, mod, project_dir: Path):
        generator: Callable | None = getattr(self.module, "generate_project", None)
        if generator is None:
            raise ValueError(f"Addon {self.name!r} does not define generate_project(mod, project_dir)")
        return generator(mod, project_dir)

    def build_project(self, project_dir: Path, minecraft_version: str, clean: bool = False, output_dir: Path | None = None):
        builder: Callable | None = getattr(self.module, "build_project", None)
        if builder is not None:
            return builder(project_dir, minecraft_version, clean=clean, output_dir=output_dir)
        from fabricpy.compiler.gradle_runner import run_build

        return run_build(project_dir, minecraft_version, self.build_label, clean=clean, output_dir=output_dir)


def _addons_root() -> Path:
    return Path(__file__).resolve().parent / "addons"


def _load_module(module_path: Path) -> ModuleType:
    module_name = "fabricpy_dynamic_" + "_".join(module_path.parts[-6:]).replace(".", "_").replace("-", "_")
    spec = spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load addon module from {module_path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _addon_from_module(module: ModuleType, module_path: Path) -> Addon | None:
    kind = str(getattr(module, "ADDON_KIND", "")).strip().lower()
    target = str(getattr(module, "ADDON_TARGET", getattr(module, "LOADER", ""))).strip().lower()
    minecraft_version = str(getattr(module, "MINECRAFT_VERSION", "")).strip()
    name = str(getattr(module, "ADDON_NAME", module_path.parent.name)).strip() or module_path.parent.name
    priority = int(getattr(module, "ADDON_PRIORITY", 0))

    if not kind or not target or not minecraft_version:
        return None

    return Addon(
        kind=kind,
        target=target,
        minecraft_version=minecraft_version,
        name=name,
        module=module,
        path=module_path.parent,
        priority=priority,
    )


def discover_addons() -> list[Addon]:
    root = _addons_root()
    if not root.exists():
        return []

    found: list[Addon] = []
    for module_path in root.rglob("addon.py"):
        try:
            module = _load_module(module_path)
            addon = _addon_from_module(module, module_path)
            if addon is not None:
                found.append(addon)
        except Exception:
            continue

    found.sort(key=lambda addon: (addon.kind, addon.target, addon.minecraft_version, addon.priority, addon.name))
    return found


def list_addons(kind: str = "", minecraft_version: str = "") -> list[dict]:
    kind = (kind or "").strip().lower()
    minecraft_version = (minecraft_version or "").strip()

    addons = []
    for addon in discover_addons():
        if kind and addon.kind != kind:
            continue
        if minecraft_version and addon.minecraft_version != minecraft_version:
            continue
        addons.append({
            "kind": addon.kind,
            "target": addon.target,
            "minecraft_version": addon.minecraft_version,
            "name": addon.name,
            "priority": addon.priority,
            "path": str(addon.path),
        })
    return addons


def resolve_addon(kind: str, target: str, minecraft_version: str) -> Addon | None:
    kind = kind.strip().lower()
    target = target.strip().lower()
    minecraft_version = minecraft_version.strip()

    matches = [
        addon
        for addon in discover_addons()
        if addon.kind == kind and addon.target == target and addon.minecraft_version == minecraft_version
    ]
    if not matches:
        return None

    matches.sort(key=lambda addon: (addon.priority, addon.name))
    return matches[-1]


def supported_targets(kind: str, minecraft_version: str) -> list[str]:
    kind = kind.strip().lower()
    minecraft_version = minecraft_version.strip()
    targets = {
        addon.target
        for addon in discover_addons()
        if addon.kind == kind and addon.minecraft_version == minecraft_version
    }
    return sorted(targets)
