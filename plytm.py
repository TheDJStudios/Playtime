import fabricpy as mc

mod = mc.Mod(
    mod_id="playtime",
    name="Playtime",
    version="1.1",
    description="Poppy playtime",
    authors=["TheDJStudios"],
    minecraft_version="1.20.1",
    loader="both",
)

@mod.register
class HandScanner(mc.Block):
    block_id = "hand_scanner"
    display_name = "Hand Scanner"
    emissive_texture = "playtime/blue_left_em"
    emissive_level = 191
    variable_rotation = True
    rotation_mode = "wall"
    item_model = {
        "parent": "playtime:block/hand_scanner"
    }
    hardness = 4.0
    resistance = 4.0
    luminance = 3
    slipperiness = 0.6
    material = "stone"
    sound_group = "stone"
    requires_tool = True
    drops_self = True
    has_block_entity = False
    opaque = False
    collidable = True

@mod.register
class HandScannerRedRight(mc.Block):
    block_id = "hand_scanner_red_right"
    display_name = "Hand Scanner (Red)"
    emissive_texture = "playtime/red_right_em"
    emissive_level = 191
    variable_rotation = True
    rotation_mode = "wall"
    item_model = {
        "parent": "playtime:block/hand_scanner_red_right"
    }
    hardness = 4.0
    resistance = 4.0
    luminance = 3
    slipperiness = 0.6
    material = "stone"
    sound_group = "stone"
    requires_tool = True
    drops_self = True
    has_block_entity = False
    opaque = False
    collidable = True

@mod.register
class GrabPackCannon(mc.Item):
    item_id = "grabpack_cannon"
    display_name = "Grabpack cannon"
    max_stack_size = 1
    max_damage = 0
    rarity = "epic"
    model = {
        "parent": "playtime:item/tool/grabpack"
    }
@mod.register
class GrabPackLeftBlue(mc.Item):
    item_id = "grabpack_left_blue"
    display_name = "Grabpack Left (Blue)"
    max_stack_size = 1
    max_damage = 0
    rarity = "epic"
    model = {
        "parent": "playtime:item/tool/grabpack_left_blue"
    }
@mod.register
class GrabPackRightRed(mc.Item):
    item_id = "grabpack_right_red"
    display_name = "Grabpack right (red)"
    max_stack_size = 1
    max_damage = 0
    rarity = "epic"
    model = {
        "parent": "playtime:item/tool/grabpack_right_red"
    }
            
@mod.register
class HoppyPlush(mc.Block):
    block_id = "critter_plush_hoppy"
    display_name = "Critter plush (Hoppy)"
    variable_rotation = True
    rotation_mode = "wall"
    item_model = {
        "parent": "playtime:block/deco/critter_plush",
        "textures": {
            "1": "playtime:block/deco/hoppy_plush"
        }
    }
    model = {
        "parent": "playtime:block/deco/critter_plush",
        "textures": {
            "1": "playtime:block/deco/hoppy_plush"
        }
    }
    hardness = 0.3
    resistance = 0.1
    luminance = 0
    slipperiness = 0.6
    material = "wool"
    sound_group = "wool"
    requires_tool = False
    drops_self = True
    has_block_entity = False
    opaque = False
    collidable = False

@mod.register
class CatNapPlush(mc.Block):
    block_id = "critter_plush_catnap"
    display_name = "Critter plush (CatNap)"
    variable_rotation = True
    rotation_mode = "wall"
    item_model = {
        "parent": "playtime:block/deco/critter_plush",
        "textures": {
            "1": "playtime:block/deco/catnap_plush"
        }
    }
    model = {
        "parent": "playtime:block/deco/critter_plush",
        "textures": {
            "1": "playtime:block/deco/catnap_plush"
        }
    }
    hardness = 0.3
    resistance = 0.1
    luminance = 0
    slipperiness = 0.6
    material = "wool"
    sound_group = "wool"
    requires_tool = False
    drops_self = True
    has_block_entity = False
    opaque = False
    collidable = False

@mod.register
class DogDayPlush(mc.Block):
    block_id = "critter_plush_dogday"
    display_name = "Critter plush (Dogday)"
    variable_rotation = True
    rotation_mode = "wall"
    item_model = {
        "parent": "playtime:block/deco/critter_plush",
        "textures": {
            "1": "playtime:block/deco/dogday_plush"
        }
    }
    model = {
        "parent": "playtime:block/deco/critter_plush",
        "textures": {
            "1": "playtime:block/deco/dogday_plush"
        }
    }
    hardness = 0.3
    resistance = 0.1
    luminance = 0
    slipperiness = 0.6
    material = "wool"
    sound_group = "wool"
    requires_tool = False
    drops_self = True
    has_block_entity = False
    opaque = False
    collidable = False

mod.shaped_recipe(
    "critter_plush_catnap_recipe",
    result="playtime:critter_plush_catnap",
    pattern=[
        "A A",
        "CAC",
        "A A",
    ],
    key={
        "A": {"item": "minecraft:purple_wool"},
        "C": {"item": "minecraft:string"}
    },
    count=1,
)

mod.shaped_recipe(
    "critter_plush_dogday_recipe",
    result="playtime:critter_plush_dogday",
    pattern=[
        "A A",
        "CAC",
        "A A",
    ],
    key={
        "A": {"item": "minecraft:orange_wool"},
        "C": {"item": "minecraft:string"}
    },
    count=1,
)

mod.shaped_recipe(
    "critter_plush_hoppy_recipe",
    result="playtime:critter_plush_hoppy",
    pattern=[
        "A A",
        "CAC",
        "A A",
    ],
    key={
        "A": {"item": "minecraft:green_wool"},
        "C": {"item": "minecraft:string"}
    },
    count=1,
)

playtime_tab = mod.creative_tab(
    tab_id="playtime_tab",
    title="Playtime",
    icon_item="playtime:grabpack_cannon"
)
playtime_tab.item.add("playtime:hand_scanner")
playtime_tab.item.add("playtime:hand_scanner_red_right")
playtime_tab.item.add("playtime:grabpack_cannon")
playtime_tab.item.add("playtime:grabpack_left_blue")
playtime_tab.item.add("playtime:grabpack_right_red")

plushie_tab = mod.creative_tab(
    tab_id="playtime_plushies_tab",
    title="Plushies",
    icon_item="playtime:critter_plush_dogday"
)
plushie_tab.item.add("playtime:critter_plush_hoppy")
plushie_tab.item.add("playtime:critter_plush_catnap")
plushie_tab.item.add("playtime:critter_plush_dogday")

mod.add_advancement(
    advancement_id="playtime/playtime",
    title="Whats the time?",
    description="Join a world with the playtime mod installed",
    icon_item="playtime:hand_scanner",
    background="minecraft:textures/gui/advancements/backgrounds/stone.png",
    frame="task"
)
mod.item_advancement(
    advancement_id="playtime/grabpack",
    title="Grabby",
    description="Obtain a Grabpack",
    icon_item="playtime:grabpack_left_blue",
    background="minecraft:textures/gui/advancements/backgrounds/stone.png",
    frame="task",
    parent="playtime:playtime/playtime",
    trigger_item="playtime:grabpack_cannon"
)
mod.item_advancement(
    advancement_id="playtime/hand_scanner",
    title="Identification",
    description="Obtain or use a Hand Scanner",
    icon_item="playtime:hand_scanner",
    background="minecraft:textures/gui/advancements/backgrounds/stone.png",
    frame="task",
    parent="playtime:playtime/playtime",
    trigger_item="playtime:hand_scanner"
)

@mod.event("player_join")
def on_join(ctx):
    if not ctx.player.has_advancement("playtime:playtime/playtime"):
        ctx.player.grant_advancement("playtime:playtime/playtime")




if __name__ == "__main__":
    mod.compile()
