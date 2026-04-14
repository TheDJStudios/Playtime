package com.generated.playtime;

import net.minecraft.network.chat.Component;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

public class ModCreativeTabs {
    public static final DeferredRegister<CreativeModeTab> TABS =
        DeferredRegister.create(Registries.CREATIVE_MODE_TAB, Playtime.MOD_ID);

    public static final RegistryObject<CreativeModeTab> PLAYTIME_TAB = TABS.register("playtime_tab", () ->
        CreativeModeTab.builder()
            .title(Component.translatable("itemGroup.playtime.playtime_tab"))
            .icon(() -> new ItemStack(ModItems.GRABPACK.get()))
            .displayItems((parameters, output) -> {
                output.accept(ModItems.GRABPACK.get());
                output.accept(ModItems.BLUE_HAND.get());
                output.accept(ModItems.RED_HAND.get());
                output.accept(ModItems.GRABPACK_CANNON.get());
                output.accept(ModItems.COIL.get());
                output.accept(ForgeRegistries.ITEMS.getValue(new net.minecraft.resources.ResourceLocation("playtime", "hand_scanner_red_right")));
                output.accept(ForgeRegistries.ITEMS.getValue(new net.minecraft.resources.ResourceLocation("playtime", "hand_scanner")));
            })
            .build()
    );
    public static final RegistryObject<CreativeModeTab> PLAYTIME_PLUSHIES_TAB = TABS.register("playtime_plushies_tab", () ->
        CreativeModeTab.builder()
            .title(Component.translatable("itemGroup.playtime.playtime_plushies_tab"))
            .icon(() -> new ItemStack(ForgeRegistries.ITEMS.getValue(new net.minecraft.resources.ResourceLocation("playtime", "critter_plush_dogday"))))
            .displayItems((parameters, output) -> {
                output.accept(ForgeRegistries.ITEMS.getValue(new net.minecraft.resources.ResourceLocation("playtime", "critter_plush_hoppy")));
                output.accept(ForgeRegistries.ITEMS.getValue(new net.minecraft.resources.ResourceLocation("playtime", "critter_plush_catnap")));
                output.accept(ForgeRegistries.ITEMS.getValue(new net.minecraft.resources.ResourceLocation("playtime", "critter_plush_dogday")));
            })
            .build()
    );
    public static final RegistryObject<CreativeModeTab> PLAYTIME_HANDS_TAB = TABS.register("playtime_hands_tab", () ->
        CreativeModeTab.builder()
            .title(Component.translatable("itemGroup.playtime.playtime_hands_tab"))
            .icon(() -> new ItemStack(ModItems.BLUE_HAND.get()))
            .displayItems((parameters, output) -> {
                output.accept(ModItems.BLUE_HAND.get());
                output.accept(ModItems.RED_HAND.get());
                output.accept(ModItems.GREEN_HAND.get());
                output.accept(ModItems.FLARE_HAND.get());
                output.accept(ModItems.PURPLE_HAND.get());
            })
            .build()
    );
}
