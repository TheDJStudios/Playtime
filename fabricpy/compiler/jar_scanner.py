"""
Dependency jar scanning and lightweight Python stub generation.

This is a first-pass interop scanner:
- resolves dependency jars from the local Gradle cache
- indexes package/class names from class files
- emits a symbol index JSON
- emits lightweight Python stub packages for autocomplete and discovery
"""

from __future__ import annotations

import json
import re
import subprocess
import zipfile
from pathlib import Path


CORE_GROUP_PREFIXES = (
    "com.mojang",
    "net.fabricmc",
    "net.minecraftforge",
    "org.spongepowered",
)


def _parse_coordinate(value: str) -> tuple[str, str, str] | None:
    parts = (value or "").strip().split(":")
    if len(parts) < 3:
        return None
    return parts[0], parts[1], parts[2]


def _load_project_meta(project_dir: Path) -> dict | None:
    meta_path = project_dir / ".fabricpy_meta" / "interop_project.json"
    if not meta_path.exists():
        return None
    return json.loads(meta_path.read_text(encoding="utf-8"))


def _extract_gradle_coordinates(project_meta: dict) -> list[dict]:
    entries: list[dict] = []
    seen: set[str] = set()

    for dep in project_meta.get("dependencies", []):
        coord = dep.get("coordinate", "")
        if coord and coord not in seen:
            entries.append({
                "coordinate": coord,
                "repo": dep.get("repo", ""),
                "mod_id": dep.get("mod_id", ""),
                "explicit": True,
            })
            seen.add(coord)

    for line in project_meta.get("dependency_lines", []):
        for match in re.findall(r"['\"]([A-Za-z0-9_.\-]+:[A-Za-z0-9_.\-]+:[^'\"]+)['\"]", line or ""):
            if match not in seen:
                entries.append({
                    "coordinate": match,
                    "repo": "",
                    "mod_id": "",
                    "explicit": False,
                })
                seen.add(match)

    return entries


def _should_scan_dependency(entry: dict) -> bool:
    parsed = _parse_coordinate(entry.get("coordinate", ""))
    if not parsed:
        return False
    group, artifact, _version = parsed
    if entry.get("explicit") or entry.get("mod_id"):
        return True
    if "geckolib" in artifact.lower():
        return True
    if group.startswith(CORE_GROUP_PREFIXES):
        return False
    return True


def _dependency_alias(entry: dict) -> str:
    if entry.get("mod_id"):
        return _sanitize_python_name(entry["mod_id"])
    parsed = _parse_coordinate(entry.get("coordinate", ""))
    if not parsed:
        return "unknown"
    _group, artifact, _version = parsed
    if "geckolib" in artifact.lower():
        return "geckolib"
    return _sanitize_python_name(artifact)


def _sanitize_python_name(value: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9_]+", "_", value or "").strip("_")
    if not clean:
        return "unknown"
    if clean[0].isdigit():
        clean = f"pkg_{clean}"
    return clean


def _resolve_gradle_cached_jars(coordinate: str) -> list[Path]:
    parsed = _parse_coordinate(coordinate)
    if not parsed:
        return []
    group, artifact, version = parsed
    cache_root = Path.home() / ".gradle" / "caches" / "modules-2" / "files-2.1"
    base = cache_root / group / artifact / version
    if not base.exists():
        return []
    jars = []
    for jar in base.rglob("*.jar"):
        name = jar.name.lower()
        if name.endswith("-sources.jar") or name.endswith("-javadoc.jar"):
            continue
        jars.append(jar)
    return sorted(jars)


def _scan_jar_classes(jar_path: Path) -> tuple[dict[str, set[str]], list[str]]:
    packages: dict[str, set[str]] = {}
    full_class_names: list[str] = []
    with zipfile.ZipFile(jar_path) as zf:
        for name in zf.namelist():
            if not name.endswith(".class"):
                continue
            if name.startswith("META-INF/") or name in {"module-info.class", "package-info.class"}:
                continue
            clean = name[:-6]
            parts = clean.split("/")
            if not parts:
                continue
            class_name = parts[-1]
            if "$" in class_name:
                nested_name = class_name.split("$", 1)[1]
                # Skip anonymous/synthetic nested classes but keep named inners.
                if nested_name.isdigit():
                    continue
            package_name = ".".join(parts[:-1])
            packages.setdefault(package_name, set()).add(class_name.replace("$", "_"))
            binary_class_name = f"{package_name}.{class_name}" if package_name else class_name
            full_class_names.append(binary_class_name)
    return packages, sorted(full_class_names)


def _chunked(values: list[str], size: int) -> list[list[str]]:
    return [values[index:index + size] for index in range(0, len(values), size)]


def _run_javap(jar_path: Path, class_names: list[str]) -> str:
    if not class_names:
        return ""
    result = subprocess.run(
        ["javap", "-classpath", str(jar_path), "-public", *class_names],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        return ""
    return result.stdout


def _split_top_level_commas(value: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for char in value:
        if char == "<":
            depth += 1
        elif char == ">":
            depth = max(0, depth - 1)
        elif char == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return parts


def _parse_method_signature(line: str, current_class: str) -> dict | None:
    text = line.strip().rstrip(";")
    if "(" not in text or ")" not in text:
        return None

    before_args, after_open = text.split("(", 1)
    args_text = after_open.rsplit(")", 1)[0].strip()
    tokens = before_args.split()
    if not tokens:
        return None
    name_token = tokens[-1]
    simple_class = current_class.split(".")[-1]
    is_constructor = name_token == current_class or name_token.endswith(f".{simple_class}")
    is_static = " static " in f" {text} "
    return_type = current_class if is_constructor else (tokens[-2] if len(tokens) >= 2 else "void")
    arg_types = _split_top_level_commas(args_text) if args_text else []
    arg_count = 0 if not args_text else len(_split_top_level_commas(args_text))

    return {
        "name": "__init__" if is_constructor else name_token.split(".")[-1],
        "arg_count": arg_count,
        "arg_types": arg_types,
        "return_type": return_type,
        "static": is_static,
        "constructor": is_constructor,
        "raw": text,
    }


def _parse_field_signature(line: str) -> dict | None:
    text = line.strip().rstrip(";")
    if "(" in text or ")" in text:
        return None
    tokens = text.split()
    if len(tokens) < 2:
        return None
    return {
        "name": tokens[-1],
        "type": tokens[-2],
        "static": " static " in f" {text} ",
        "raw": text,
    }


def _parse_javap_output(output: str) -> dict[str, dict]:
    class_map: dict[str, dict] = {}
    current_class: str | None = None

    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("Compiled from "):
            continue
        if line == "}":
            current_class = None
            continue

        class_match = re.match(r"^(public|protected|private)?\s*(abstract\s+|final\s+)?(class|interface|enum)\s+([A-Za-z0-9_.$]+)", line)
        if class_match:
            current_class = class_match.group(4).replace("$", ".")
            class_map.setdefault(current_class, {
                "kind": class_match.group(3),
                "methods": [],
                "fields": [],
            })
            continue

        if not current_class:
            continue

        method_info = _parse_method_signature(line, current_class)
        if method_info:
            class_map[current_class]["methods"].append(method_info)
            continue

        field_info = _parse_field_signature(line)
        if field_info:
            class_map[current_class]["fields"].append(field_info)

    return class_map


def _ensure_stub_pkg(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    init_file = path / "__init__.pyi"
    if not init_file.exists():
        init_file.write_text("# generated by fabricpy jar scanner\n", encoding="utf-8")


def _java_type_to_stub(value: str) -> str:
    clean = (value or "").strip()
    clean = clean.replace("...", "[]")
    if not clean:
        return "object"

    if clean.endswith("[]"):
        return "list[object]"

    mapping = {
        "byte": "int",
        "short": "int",
        "int": "int",
        "long": "int",
        "float": "float",
        "double": "float",
        "boolean": "bool",
        "char": "str",
        "java.lang.String": "str",
        "String": "str",
        "void": "None",
    }
    if clean in mapping:
        return mapping[clean]
    return "object"


def _render_stub_class(class_name: str, detail: dict | None) -> str:
    lines = [f"class {class_name}:"]
    body: list[str] = []

    if detail:
        for field in detail.get("fields", []):
            body.append(f"    {field['name']}: {_java_type_to_stub(field.get('type', 'object'))}")

        for method in detail.get("methods", []):
            args = []
            if not method.get("static") and not method.get("constructor"):
                args.append("self")
            elif method.get("constructor"):
                args.append("self")
            for index, arg_type in enumerate(method.get("arg_types", [])):
                args.append(f"arg{index}: {_java_type_to_stub(arg_type)}")
            signature = ", ".join(args)
            return_type = _java_type_to_stub(method.get("return_type", "object"))
            if method.get("static") and not method.get("constructor"):
                body.append("    @staticmethod")
                body.append(f"    def {method['name']}({signature}) -> {return_type}: ...")
            else:
                body.append(f"    def {method['name']}({signature}) -> {return_type}: ...")

    if not body:
        body.append("    ...")

    lines.extend(body)
    return "\n".join(lines)


def _write_stub_tree(stub_root: Path, alias: str, packages: dict[str, set[str]], class_details: dict[str, dict]):
    base = stub_root / "dep" / alias
    _ensure_stub_pkg(stub_root / "dep")
    _ensure_stub_pkg(base)

    for package_name, classes in sorted(packages.items()):
        current = base
        if package_name:
            for part in package_name.split("."):
                current = current / part
                _ensure_stub_pkg(current)
        init_path = current / "__init__.pyi"
        header = "# generated by fabricpy jar scanner\n\n"
        rendered_classes = []
        for cls in sorted(classes):
            full_name = f"{package_name}.{cls}" if package_name else cls
            rendered_classes.append(_render_stub_class(cls, class_details.get(full_name)))
        body = "\n\n".join(rendered_classes)
        init_path.write_text(header + body + ("\n" if body else ""), encoding="utf-8")


def build_symbol_index_for_project(project_dir: Path):
    project_meta = _load_project_meta(project_dir)
    if not project_meta:
        return

    scan_entries = [entry for entry in _extract_gradle_coordinates(project_meta) if _should_scan_dependency(entry)]
    meta_dir = project_dir / ".fabricpy_meta"
    stubs_dir = meta_dir / "python_stubs"
    stubs_dir.mkdir(parents=True, exist_ok=True)

    resolved = []
    unresolved = []
    package_index = []

    for entry in scan_entries:
        coordinate = entry["coordinate"]
        alias = _dependency_alias(entry)
        jar_paths = _resolve_gradle_cached_jars(coordinate)
        if not jar_paths:
            unresolved.append({
                "coordinate": coordinate,
                "alias": alias,
                "repo": entry.get("repo", ""),
            })
            continue

        merged_packages: dict[str, set[str]] = {}
        merged_class_details: dict[str, dict] = {}
        for jar_path in jar_paths:
            jar_packages, full_class_names = _scan_jar_classes(jar_path)
            for package_name, classes in jar_packages.items():
                merged_packages.setdefault(package_name, set()).update(classes)
            for chunk in _chunked(full_class_names, 40):
                javap_output = _run_javap(jar_path, chunk)
                if not javap_output:
                    continue
                merged_class_details.update(_parse_javap_output(javap_output))
            resolved.append({
                "coordinate": coordinate,
                "alias": alias,
                "jar": str(jar_path.resolve()),
            })

        _write_stub_tree(stubs_dir, alias, merged_packages, merged_class_details)
        package_index.append({
            "coordinate": coordinate,
            "alias": alias,
            "package_count": len(merged_packages),
            "class_count": sum(len(classes) for classes in merged_packages.values()),
            "packages": {pkg: sorted(classes) for pkg, classes in sorted(merged_packages.items())},
            "class_details": merged_class_details,
        })

    symbol_index = {
        "format": 1,
        "kind": "fabricpy_symbol_index",
        "status": "partial",
        "loader": project_meta.get("loader", ""),
        "minecraft_version": project_meta.get("minecraft_version", ""),
        "resolved_jars": resolved,
        "unresolved_dependencies": unresolved,
        "dependencies": package_index,
        "stub_root": str(stubs_dir.resolve()),
    }

    (meta_dir / "symbol_index.json").write_text(json.dumps(symbol_index, indent=2), encoding="utf-8")
