package com.generated.playtime;

import net.minecraft.block.Block;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroups;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;
import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;
import com.generated.playtime.block.HandScanner;
import com.generated.playtime.block.HandScannerRedRight;
import com.generated.playtime.block.HoppyPlush;
import com.generated.playtime.block.CatNapPlush;
import com.generated.playtime.block.DogDayPlush;

/**
 * Registers all blocks for Playtime.
 */
public class ModBlocks {
    public static final HandScanner HAND_SCANNER = register("hand_scanner", new HandScanner());
    public static final HandScannerRedRight HAND_SCANNER_RED_RIGHT = register("hand_scanner_red_right", new HandScannerRedRight());
    public static final HoppyPlush CRITTER_PLUSH_HOPPY = register("critter_plush_hoppy", new HoppyPlush());
    public static final CatNapPlush CRITTER_PLUSH_CATNAP = register("critter_plush_catnap", new CatNapPlush());
    public static final DogDayPlush CRITTER_PLUSH_DOGDAY = register("critter_plush_dogday", new DogDayPlush());

    private static <T extends Block> T register(String id, T block) {
        Registry.register(Registries.BLOCK, new Identifier(Playtime.MOD_ID, id), block);
        return block;
    }

    public static void register() {
        // Blocks are registered via static initializer above.
        // Register block items:
        Registry.register(Registries.ITEM, new Identifier(Playtime.MOD_ID, "hand_scanner"), new BlockItem(HAND_SCANNER, new Item.Settings()));
        Registry.register(Registries.ITEM, new Identifier(Playtime.MOD_ID, "hand_scanner_red_right"), new BlockItem(HAND_SCANNER_RED_RIGHT, new Item.Settings()));
        Registry.register(Registries.ITEM, new Identifier(Playtime.MOD_ID, "critter_plush_hoppy"), new BlockItem(CRITTER_PLUSH_HOPPY, new Item.Settings()));
        Registry.register(Registries.ITEM, new Identifier(Playtime.MOD_ID, "critter_plush_catnap"), new BlockItem(CRITTER_PLUSH_CATNAP, new Item.Settings()));
        Registry.register(Registries.ITEM, new Identifier(Playtime.MOD_ID, "critter_plush_dogday"), new BlockItem(CRITTER_PLUSH_DOGDAY, new Item.Settings()));
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.BUILDING_BLOCKS).register(entries -> entries.add(HAND_SCANNER));
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.BUILDING_BLOCKS).register(entries -> entries.add(HAND_SCANNER_RED_RIGHT));
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.BUILDING_BLOCKS).register(entries -> entries.add(CRITTER_PLUSH_HOPPY));
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.BUILDING_BLOCKS).register(entries -> entries.add(CRITTER_PLUSH_CATNAP));
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.BUILDING_BLOCKS).register(entries -> entries.add(CRITTER_PLUSH_DOGDAY));
    }
}
