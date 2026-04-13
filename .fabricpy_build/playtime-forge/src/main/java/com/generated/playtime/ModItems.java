package com.generated.playtime;

import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraftforge.event.BuildCreativeModeTabContentsEvent;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;
import com.generated.playtime.item.GrabPackCannon;
import com.generated.playtime.item.CoilItem;
import com.generated.playtime.item.BlueHand;
import com.generated.playtime.item.RedHand;
import com.generated.playtime.item.GreenHand;
import com.generated.playtime.item.FlareHand;
import com.generated.playtime.item.GrabPack;

public class ModItems {
    public static final DeferredRegister<Item> ITEMS =
        DeferredRegister.create(ForgeRegistries.ITEMS, Playtime.MOD_ID);

    public static final RegistryObject<Item> GRABPACK_CANNON = ITEMS.register("grabpack_cannon", GrabPackCannon::new);
    public static final RegistryObject<Item> COIL = ITEMS.register("coil", CoilItem::new);
    public static final RegistryObject<Item> BLUE_HAND = ITEMS.register("blue_hand", BlueHand::new);
    public static final RegistryObject<Item> RED_HAND = ITEMS.register("red_hand", RedHand::new);
    public static final RegistryObject<Item> GREEN_HAND = ITEMS.register("green_hand", GreenHand::new);
    public static final RegistryObject<Item> FLARE_HAND = ITEMS.register("flare_hand", FlareHand::new);
    public static final RegistryObject<Item> GRABPACK = ITEMS.register("grabpack", GrabPack::new);

    public static void addCreative(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey() == CreativeModeTabs.INGREDIENTS) {
            event.accept(GRABPACK_CANNON);
            event.accept(COIL);
            event.accept(BLUE_HAND);
            event.accept(RED_HAND);
            event.accept(GREEN_HAND);
            event.accept(FLARE_HAND);
            event.accept(GRABPACK);
        }
    }
}
