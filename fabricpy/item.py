"""
Item base class. Subclass this to create a custom item.

Class attributes:
    item_id             str     Registry ID, e.g. "sonic_screwdriver"  (required)
    display_name        str     In-game display name                    (default: title-cased item_id)
    max_stack_size      int     Max stack size (1–64)                   (default: 64)
    max_damage          int     Durability (0 = unbreakable)            (default: 0)
    rarity              str     "common","uncommon","rare","epic"        (default: "common")
    fireproof           bool    Survives lava/fire                      (default: False)
    bundle_inventory    bool    Use vanilla bundle-style item storage   (default: False)
    inventory_slots     int     Managed internal slot count             (default: 0)
    inventory_slot_capacity int Max items per managed slot             (default: 64)
    inventory_total_capacity int Optional total managed item cap        (default: 0 = slots * slot capacity)
    inventory_visible_in_tooltip bool Show managed slots in tooltip     (default: True)
    inventory_tooltip_show_empty bool Show empty managed slots          (default: False)
    inventory_tooltip_slot_limit int Max slots shown in tooltip         (default: 8)
    inventory_insert_from_offhand bool Insert from opposite hand on use (default: True)
    inventory_extract_from_use bool Extract stored stack on use         (default: True)
    inventory_extract_requires_sneak bool Sneak required for extract    (default: True)
    inventory_extract_order str  "first" or "last" extraction order     (default: "last")
    inventory_whitelist  list    Allowed item ids for all slots         (default: [])
    inventory_blacklist  list    Blocked item ids for all slots         (default: [])
    inventory_slot_whitelists dict Per-slot allowed item ids            (default: {})
    inventory_slot_blacklists dict Per-slot blocked item ids            (default: {})
    inventory_slot_labels dict  Per-slot tooltip labels                 (default: {})
    food_hunger         int     Hunger restored if food (0 = not food)  (default: 0)
    food_saturation     float   Saturation if food                      (default: 0.0)
    food_always_edible  bool    Edible even when not hungry             (default: False)
    is_tool             bool    Treat as a tool item                    (default: False)
    tool_type           str     "sword","pickaxe","axe","shovel","hoe"  (default: "")
    tool_material       str     "wood","stone","iron","gold","diamond","netherite" (default: "iron")

Hook decorators:
    @mc.on_right_click  — player right-clicks with the item
    @mc.on_tick         — item tick (advanced, requires block entity or entity)
"""


class ItemMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        hooks = {}
        for attr_name, val in namespace.items():
            if callable(val) and hasattr(val, "_fabricpy_hook"):
                hooks[val._fabricpy_hook] = val
        cls._hooks = hooks
        return cls


class Item(metaclass=ItemMeta):
    # ---- Registry ----
    item_id: str = ""
    display_name: str = ""
    namespace: str = ""

    # ---- Stack / Durability ----
    max_stack_size: int = 64
    max_damage: int = 0
    rarity: str = "common"

    # ---- Survival ----
    fireproof: bool = False
    bundle_inventory: bool = False
    inventory_slots: int = 0
    inventory_slot_capacity: int = 64
    inventory_total_capacity: int = 0
    inventory_visible_in_tooltip: bool = True
    inventory_tooltip_show_empty: bool = False
    inventory_tooltip_slot_limit: int = 8
    inventory_insert_from_offhand: bool = True
    inventory_extract_from_use: bool = True
    inventory_extract_requires_sneak: bool = True
    inventory_extract_order: str = "last"
    inventory_whitelist: list = []
    inventory_blacklist: list = []
    inventory_slot_whitelists: dict = {}
    inventory_slot_blacklists: dict = {}
    inventory_slot_labels: dict = {}

    # ---- Food ----
    food_hunger: int = 0
    food_saturation: float = 0.0
    food_always_edible: bool = False

    # ---- Tool ----
    is_tool: bool = False
    tool_type: str = ""
    tool_material: str = "iron"

    # ---- Assets ----
    texture: str = ""                   # Shortcut for generated item layer0
    emissive_texture: str = ""          # Optional overlay texture for emissive parts
    emissive_level: int = 0             # 1-255 authoring value, currently advisory for item overlays
    textures: dict = {}                 # Full item model texture map override
    model: dict | None = None           # Full item model JSON override

    # ---- Internal ----
    _hooks: dict = {}

    @classmethod
    def get_hooks(cls) -> dict:
        return cls._hooks

    @classmethod
    def get_class_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_display_name(cls) -> str:
        if cls.display_name:
            return cls.display_name
        return cls.item_id.replace("_", " ").title()

    @classmethod
    def get_full_id(cls) -> str:
        ns = cls.namespace or "modid"
        return f"{ns}:{cls.item_id}"
