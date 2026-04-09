package com.generated.playtime;

import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraftforge.event.BuildCreativeModeTabContentsEvent;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;
import com.generated.playtime.block.HandScanner;
import com.generated.playtime.block.HandScannerRedRight;
import com.generated.playtime.block.HoppyPlush;
import com.generated.playtime.block.CatNapPlush;
import com.generated.playtime.block.DogDayPlush;

public class ModBlocks {
    public static final DeferredRegister<Block> BLOCKS =
        DeferredRegister.create(ForgeRegistries.BLOCKS, Playtime.MOD_ID);
    public static final DeferredRegister<Item> ITEMS =
        DeferredRegister.create(ForgeRegistries.ITEMS, Playtime.MOD_ID);

    public static final RegistryObject<Block> HAND_SCANNER = BLOCKS.register("hand_scanner", HandScanner::new);
    public static final RegistryObject<Block> HAND_SCANNER_RED_RIGHT = BLOCKS.register("hand_scanner_red_right", HandScannerRedRight::new);
    public static final RegistryObject<Block> CRITTER_PLUSH_HOPPY = BLOCKS.register("critter_plush_hoppy", HoppyPlush::new);
    public static final RegistryObject<Block> CRITTER_PLUSH_CATNAP = BLOCKS.register("critter_plush_catnap", CatNapPlush::new);
    public static final RegistryObject<Block> CRITTER_PLUSH_DOGDAY = BLOCKS.register("critter_plush_dogday", DogDayPlush::new);
    public static final RegistryObject<Item> HAND_SCANNER_ITEM = ITEMS.register("hand_scanner", () -> new BlockItem(HAND_SCANNER.get(), new Item.Properties()));
    public static final RegistryObject<Item> HAND_SCANNER_RED_RIGHT_ITEM = ITEMS.register("hand_scanner_red_right", () -> new BlockItem(HAND_SCANNER_RED_RIGHT.get(), new Item.Properties()));
    public static final RegistryObject<Item> CRITTER_PLUSH_HOPPY_ITEM = ITEMS.register("critter_plush_hoppy", () -> new BlockItem(CRITTER_PLUSH_HOPPY.get(), new Item.Properties()));
    public static final RegistryObject<Item> CRITTER_PLUSH_CATNAP_ITEM = ITEMS.register("critter_plush_catnap", () -> new BlockItem(CRITTER_PLUSH_CATNAP.get(), new Item.Properties()));
    public static final RegistryObject<Item> CRITTER_PLUSH_DOGDAY_ITEM = ITEMS.register("critter_plush_dogday", () -> new BlockItem(CRITTER_PLUSH_DOGDAY.get(), new Item.Properties()));

    public static void addCreative(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey() == CreativeModeTabs.BUILDING_BLOCKS) {
            event.accept(HAND_SCANNER_ITEM);
            event.accept(HAND_SCANNER_RED_RIGHT_ITEM);
            event.accept(CRITTER_PLUSH_HOPPY_ITEM);
            event.accept(CRITTER_PLUSH_CATNAP_ITEM);
            event.accept(CRITTER_PLUSH_DOGDAY_ITEM);
        }
    }
}
