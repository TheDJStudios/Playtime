import itertools
import json
from pathlib import Path


def _deepcopy_json(value):
    return json.loads(json.dumps(value))


def normalize_item_model_id(mod_id: str, ref: str, default_id: str) -> str:
    clean = (ref or "").strip()
    if not clean:
        return f"{mod_id}:item/{default_id}"
    if ":" in clean:
        return clean
    if clean.startswith("item/"):
        return f"{mod_id}:{clean}"
    return f"{mod_id}:item/{clean}"


def _item_model_file_from_id(project_root: Path, default_mod_id: str, model_id: str) -> Path | None:
    if ":" in model_id:
        namespace, path = model_id.split(":", 1)
    else:
        namespace, path = default_mod_id, model_id
    if not path.startswith("item/"):
        return None
    rel = path[len("item/"):]
    return project_root / "assets" / namespace / "models" / "item" / f"{rel}.json"


def _load_item_model_data(project_root: Path, default_mod_id: str, model_id: str) -> dict | None:
    model_file = _item_model_file_from_id(project_root, default_mod_id, model_id)
    if model_file and model_file.exists():
        try:
            return json.loads(model_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
    return None


def resolve_item_model_data(project_root: Path, mod, item) -> dict | None:
    default_model_id = normalize_item_model_id(mod.mod_id, "", item.item_id)
    if isinstance(item.model, dict):
        data = _deepcopy_json(item.model)
    else:
        data = _load_item_model_data(project_root, mod.mod_id, default_model_id)
    if not isinstance(data, dict):
        return None

    seen: set[str] = set()
    while isinstance(data, dict) and "elements" not in data:
        parent = data.get("parent")
        if not isinstance(parent, str) or parent.startswith("minecraft:"):
            break
        parent_id = normalize_item_model_id(mod.mod_id, parent, item.item_id)
        if parent_id in seen:
            break
        seen.add(parent_id)
        parent_data = _load_item_model_data(project_root, mod.mod_id, parent_id)
        if not isinstance(parent_data, dict):
            break
        merged = _deepcopy_json(parent_data)
        parent_textures = merged.get("textures")
        child_textures = data.get("textures")
        if isinstance(parent_textures, dict) and isinstance(child_textures, dict):
            parent_textures.update(_deepcopy_json(child_textures))
        elif isinstance(child_textures, dict):
            merged["textures"] = _deepcopy_json(child_textures)
        for key, value in data.items():
            if key in {"parent", "textures"}:
                continue
            merged[key] = _deepcopy_json(value)
        data = merged
    return data if isinstance(data, dict) else None


def _normalize_strings(raw) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        values = [raw]
    elif isinstance(raw, (list, tuple, set)):
        values = list(raw)
    else:
        values = [raw]
    out: list[str] = []
    for value in values:
        text = str(value).strip()
        if text and text not in out:
            out.append(text)
    return out


def _normalize_slot_name_map(raw, slots: int) -> dict[int, str]:
    out: dict[int, str] = {}
    if not isinstance(raw, dict):
        return out
    for key, value in raw.items():
        try:
            slot = int(key)
        except (TypeError, ValueError):
            continue
        if 0 <= slot < slots and value:
            out[slot] = str(value)
    return out


def _normalize_slot_items_map(raw, slots: int) -> dict[int, list[str]]:
    out: dict[int, list[str]] = {}
    if not isinstance(raw, dict):
        return out
    for key, value in raw.items():
        try:
            slot = int(key)
        except (TypeError, ValueError):
            continue
        if 0 <= slot < slots:
            out[slot] = _normalize_strings(value)
    return out


def _item_lookup(mod) -> dict[str, object]:
    out = {}
    for item in mod._items:
        out[item.get_full_id()] = item
        out[f"{mod.mod_id}:{item.item_id}"] = item
        out[item.item_id] = item
    return out


def _named_element(model_data: dict, name: str) -> dict | None:
    elements = model_data.get("elements")
    if not isinstance(elements, list):
        return None
    for element in elements:
        if isinstance(element, dict) and element.get("name") == name:
            return element
    return None


def _element_center(element: dict) -> tuple[float, float, float] | None:
    from_pos = element.get("from")
    to_pos = element.get("to")
    if not (isinstance(from_pos, list) and isinstance(to_pos, list) and len(from_pos) == 3 and len(to_pos) == 3):
        return None
    return (
        (float(from_pos[0]) + float(to_pos[0])) / 2.0,
        (float(from_pos[1]) + float(to_pos[1])) / 2.0,
        (float(from_pos[2]) + float(to_pos[2])) / 2.0,
    )


def _remove_named_elements(model_data: dict, names: set[str]) -> dict:
    out = _deepcopy_json(model_data)
    elements = out.get("elements")
    if isinstance(elements, list):
        out["elements"] = [
            element for element in elements
            if not (isinstance(element, dict) and element.get("name") in names)
        ]
    return out


def _translate_triplet(value, dx: float, dy: float, dz: float):
    if isinstance(value, list) and len(value) == 3:
        value[0] = float(value[0]) + dx
        value[1] = float(value[1]) + dy
        value[2] = float(value[2]) + dz


def _translate_element(element: dict, dx: float, dy: float, dz: float) -> dict:
    out = _deepcopy_json(element)
    _translate_triplet(out.get("from"), dx, dy, dz)
    _translate_triplet(out.get("to"), dx, dy, dz)
    rotation = out.get("rotation")
    if isinstance(rotation, dict):
        _translate_triplet(rotation.get("origin"), dx, dy, dz)
    _translate_triplet(out.get("origin"), dx, dy, dz)
    return out


def _remap_texture_refs(value, ref_map: dict[str, str]):
    if isinstance(value, dict):
        return {key: _remap_texture_refs(val, ref_map) for key, val in value.items()}
    if isinstance(value, list):
        return [_remap_texture_refs(entry, ref_map) for entry in value]
    if isinstance(value, str) and value.startswith("#"):
        return ref_map.get(value, value)
    return value


def _prefixed_child_textures(child_model: dict, prefix: str) -> tuple[dict, list[dict]]:
    textures = child_model.get("textures")
    texture_map = textures if isinstance(textures, dict) else {}
    ref_map = {f"#{key}": f"#{prefix}{key}" for key in texture_map.keys()}
    new_textures = {f"{prefix}{key}": value for key, value in texture_map.items()}
    elements = child_model.get("elements")
    out_elements = []
    if isinstance(elements, list):
        for element in elements:
            if isinstance(element, dict):
                out_elements.append(_remap_texture_refs(_deepcopy_json(element), ref_map))
    return new_textures, out_elements


def _texture_size(model_data: dict) -> list[int] | None:
    value = model_data.get("texture_size")
    if isinstance(value, list) and len(value) == 2:
        try:
            return [int(value[0]), int(value[1])]
        except (TypeError, ValueError):
            return None
    return None


def _merge_attachment_model(base_model: dict, attachments: list[dict], hidden_names: set[str]) -> dict:
    result = _remove_named_elements(base_model, hidden_names)
    base_textures = result.get("textures")
    if not isinstance(base_textures, dict):
        base_textures = {}
        result["textures"] = base_textures
    result_elements = result.get("elements")
    if not isinstance(result_elements, list):
        result_elements = []
        result["elements"] = result_elements
    max_texture = _texture_size(base_model) or [16, 16]

    for index, attachment in enumerate(attachments):
        child_model = _remove_named_elements(attachment["model"], {attachment["child_point"]})
        child_textures, child_elements = _prefixed_child_textures(child_model, f"att{index}_")
        base_textures.update(child_textures)
        dx = attachment["host_center"][0] - attachment["child_center"][0]
        dy = attachment["host_center"][1] - attachment["child_center"][1]
        dz = attachment["host_center"][2] - attachment["child_center"][2]
        for element in child_elements:
            result_elements.append(_translate_element(element, dx, dy, dz))
        child_texture = _texture_size(child_model)
        if child_texture:
            max_texture[0] = max(max_texture[0], child_texture[0])
            max_texture[1] = max(max_texture[1], child_texture[1])

    result["texture_size"] = max_texture
    result.pop("groups", None)
    return result


def build_item_attachment_variants(project_root: Path, mod, item) -> dict | None:
    slots = max(0, int(getattr(item, "inventory_slots", 0) or 0))
    if slots <= 0:
        return None

    host_points = _normalize_slot_name_map(getattr(item, "inventory_attachment_points", {}), slots)
    if not host_points:
        return None

    explicit_items = _normalize_slot_items_map(getattr(item, "inventory_attachment_items", {}), slots)
    slot_whitelists = _normalize_slot_items_map(getattr(item, "inventory_slot_whitelists", {}), slots)
    global_whitelist = _normalize_strings(getattr(item, "inventory_whitelist", []))

    base_model = resolve_item_model_data(project_root, mod, item)
    if not isinstance(base_model, dict):
        return None

    host_centers: dict[int, tuple[float, float, float]] = {}
    hidden_names = set(host_points.values())
    for slot, point_name in host_points.items():
        point_element = _named_element(base_model, point_name)
        point_center = _element_center(point_element) if isinstance(point_element, dict) else None
        if point_center is None:
            continue
        host_centers[slot] = point_center
    if not host_centers:
        return None

    lookup = _item_lookup(mod)
    slot_options: list[tuple[int, list[tuple[str, dict | None]]]] = []
    for slot in sorted(host_centers.keys()):
        candidates = explicit_items.get(slot) or slot_whitelists.get(slot) or global_whitelist
        options: list[tuple[str, dict | None]] = [("", None)]
        for item_id in candidates:
            normalized_item_id = item_id if ":" in item_id else f"{mod.mod_id}:{item_id}"
            child_item = lookup.get(item_id) or lookup.get(normalized_item_id)
            if child_item is None:
                continue
            child_point = str(getattr(child_item, "attachment_connection_point", "") or "").strip()
            if not child_point:
                continue
            child_model = resolve_item_model_data(project_root, mod, child_item)
            if not isinstance(child_model, dict):
                continue
            child_point_element = _named_element(child_model, child_point)
            child_center = _element_center(child_point_element) if isinstance(child_point_element, dict) else None
            if child_center is None:
                continue
            hidden_names.add(child_point)
            options.append((normalized_item_id, {
                "item_id": normalized_item_id,
                "model": child_model,
                "child_point": child_point,
                "child_center": child_center,
                "host_point": host_points[slot],
                "host_center": host_centers[slot],
            }))
        slot_options.append((slot, options))

    combo_count = 1
    for _, options in slot_options:
        combo_count *= max(1, len(options))
    if combo_count > 128:
        return None

    variants = []
    custom_model_data = 1
    for combo in itertools.product(*(options for _, options in slot_options)):
        attachments = [bundle for _, bundle in combo if bundle is not None]
        if not attachments:
            continue
        slot_state = {
            slot: item_id
            for (slot, _), (item_id, bundle) in zip(slot_options, combo)
            if bundle is not None and item_id
        }
        merged_model = _merge_attachment_model(base_model, attachments, hidden_names)
        variants.append({
            "custom_model_data": custom_model_data,
            "model_name": f"{item.item_id}__attached_{custom_model_data}",
            "slot_state": slot_state,
            "model": merged_model,
        })
        custom_model_data += 1

    return {
        "attachment_slots": sorted(host_centers.keys()),
        "base_model_name": f"{item.item_id}__base",
        "base_model": _remove_named_elements(base_model, hidden_names),
        "variants": variants,
    }
