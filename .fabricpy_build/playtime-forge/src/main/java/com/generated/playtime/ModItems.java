package com.generated.playtime;

import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraftforge.event.BuildCreativeModeTabContentsEvent;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;
import com.generated.playtime.item.GrabPackCannon;
import com.generated.playtime.item.GrabPackLeftBlue;
import com.generated.playtime.item.GrabPackRightRed;

public class ModItems {
    public static final DeferredRegister<Item> ITEMS =
        DeferredRegister.create(ForgeRegistries.ITEMS, Playtime.MOD_ID);

    public static final RegistryObject<Item> GRABPACK_CANNON = ITEMS.register("grabpack_cannon", GrabPackCannon::new);
    public static final RegistryObject<Item> GRABPACK_LEFT_BLUE = ITEMS.register("grabpack_left_blue", GrabPackLeftBlue::new);
    public static final RegistryObject<Item> GRABPACK_RIGHT_RED = ITEMS.register("grabpack_right_red", GrabPackRightRed::new);

    public static void addCreative(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey() == CreativeModeTabs.INGREDIENTS) {
            event.accept(GRABPACK_CANNON);
            event.accept(GRABPACK_LEFT_BLUE);
            event.accept(GRABPACK_RIGHT_RED);
        }
    }
}
