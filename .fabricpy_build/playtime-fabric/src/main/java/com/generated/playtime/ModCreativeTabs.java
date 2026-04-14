package com.generated.playtime;

import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.minecraft.util.Identifier;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemStack;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.text.Text;

public class ModCreativeTabs {
    public static final ItemGroup PLAYTIME_TAB = Registry.register(
        Registries.ITEM_GROUP,
        new Identifier(Playtime.MOD_ID, "playtime_tab"),
        FabricItemGroup.builder()
            .displayName(Text.translatable("itemGroup.playtime.playtime_tab"))
            .icon(() -> new ItemStack(ModItems.GRABPACK))
            .entries((displayContext, entries) -> {
                entries.add(ModItems.GRABPACK);
                entries.add(ModItems.BLUE_HAND);
                entries.add(ModItems.RED_HAND);
                entries.add(ModItems.GRABPACK_CANNON);
                entries.add(ModItems.COIL);
                entries.add(Registries.ITEM.get(new Identifier("playtime", "hand_scanner_red_right")));
                entries.add(Registries.ITEM.get(new Identifier("playtime", "hand_scanner")));
            })
            .build()
    );
    public static final ItemGroup PLAYTIME_PLUSHIES_TAB = Registry.register(
        Registries.ITEM_GROUP,
        new Identifier(Playtime.MOD_ID, "playtime_plushies_tab"),
        FabricItemGroup.builder()
            .displayName(Text.translatable("itemGroup.playtime.playtime_plushies_tab"))
            .icon(() -> new ItemStack(Registries.ITEM.get(new Identifier("playtime", "critter_plush_dogday"))))
            .entries((displayContext, entries) -> {
                entries.add(Registries.ITEM.get(new Identifier("playtime", "critter_plush_hoppy")));
                entries.add(Registries.ITEM.get(new Identifier("playtime", "critter_plush_catnap")));
                entries.add(Registries.ITEM.get(new Identifier("playtime", "critter_plush_dogday")));
            })
            .build()
    );
    public static final ItemGroup PLAYTIME_HANDS_TAB = Registry.register(
        Registries.ITEM_GROUP,
        new Identifier(Playtime.MOD_ID, "playtime_hands_tab"),
        FabricItemGroup.builder()
            .displayName(Text.translatable("itemGroup.playtime.playtime_hands_tab"))
            .icon(() -> new ItemStack(ModItems.BLUE_HAND))
            .entries((displayContext, entries) -> {
                entries.add(ModItems.BLUE_HAND);
                entries.add(ModItems.RED_HAND);
                entries.add(ModItems.GREEN_HAND);
                entries.add(ModItems.FLARE_HAND);
                entries.add(ModItems.PURPLE_HAND);
            })
            .build()
    );

    public static void register() {
        // Creative tabs are registered via static fields above.
    }
}
