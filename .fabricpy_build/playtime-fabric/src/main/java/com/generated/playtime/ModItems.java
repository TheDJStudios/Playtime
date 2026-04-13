package com.generated.playtime;

import net.minecraft.item.Item;
import net.minecraft.item.ItemGroups;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;
import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;
import com.generated.playtime.item.GrabPackCannon;
import com.generated.playtime.item.CoilItem;
import com.generated.playtime.item.BlueHand;
import com.generated.playtime.item.RedHand;
import com.generated.playtime.item.GreenHand;
import com.generated.playtime.item.FlareHand;
import com.generated.playtime.item.GrabPack;

/**
 * Registers all items for Playtime.
 */
public class ModItems {
    public static final GrabPackCannon GRABPACK_CANNON = register("grabpack_cannon", new GrabPackCannon());
    public static final CoilItem COIL = register("coil", new CoilItem());
    public static final BlueHand BLUE_HAND = register("blue_hand", new BlueHand());
    public static final RedHand RED_HAND = register("red_hand", new RedHand());
    public static final GreenHand GREEN_HAND = register("green_hand", new GreenHand());
    public static final FlareHand FLARE_HAND = register("flare_hand", new FlareHand());
    public static final GrabPack GRABPACK = register("grabpack", new GrabPack());

    private static <T extends Item> T register(String id, T item) {
        return Registry.register(Registries.ITEM, new Identifier(Playtime.MOD_ID, id), item);
    }

    public static void register() {
        // Items registered via static fields above.
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.INGREDIENTS).register(entries -> entries.add(GRABPACK_CANNON));
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.INGREDIENTS).register(entries -> entries.add(COIL));
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.INGREDIENTS).register(entries -> entries.add(BLUE_HAND));
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.INGREDIENTS).register(entries -> entries.add(RED_HAND));
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.INGREDIENTS).register(entries -> entries.add(GREEN_HAND));
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.INGREDIENTS).register(entries -> entries.add(FLARE_HAND));
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.INGREDIENTS).register(entries -> entries.add(GRABPACK));
    }
}
