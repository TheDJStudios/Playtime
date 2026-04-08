package com.generated.playtime;

import net.minecraft.item.Item;
import net.minecraft.item.ItemGroups;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;
import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;
import com.generated.playtime.item.GrabPackCannon;
import com.generated.playtime.item.GrabPackLeftBlue;
import com.generated.playtime.item.GrabPackRightRed;

/**
 * Registers all items for Playtime.
 */
public class ModItems {
    public static final GrabPackCannon GRABPACK_CANNON = register("grabpack_cannon", new GrabPackCannon());
    public static final GrabPackLeftBlue GRABPACK_LEFT_BLUE = register("grabpack_left_blue", new GrabPackLeftBlue());
    public static final GrabPackRightRed GRABPACK_RIGHT_RED = register("grabpack_right_red", new GrabPackRightRed());

    private static <T extends Item> T register(String id, T item) {
        return Registry.register(Registries.ITEM, new Identifier(Playtime.MOD_ID, id), item);
    }

    public static void register() {
        // Items registered via static fields above.
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.INGREDIENTS).register(entries -> entries.add(GRABPACK_CANNON));
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.INGREDIENTS).register(entries -> entries.add(GRABPACK_LEFT_BLUE));
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.INGREDIENTS).register(entries -> entries.add(GRABPACK_RIGHT_RED));
    }
}
