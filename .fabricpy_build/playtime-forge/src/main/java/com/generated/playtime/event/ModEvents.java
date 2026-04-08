package com.generated.playtime.event;

import com.generated.playtime.Playtime;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.ForgeRegistries;

@Mod.EventBusSubscriber(modid = Playtime.MOD_ID, bus = Mod.EventBusSubscriber.Bus.FORGE)
public class ModEvents {
    private static final Map<UUID, String> LAST_OFFHAND_ITEM = new HashMap<>();
    private static final Map<UUID, Integer> LAST_OFFHAND_COUNT = new HashMap<>();

    public static void onCommonSetup(FMLCommonSetupEvent event) {
        // Common setup
    }

    @SubscribeEvent
    public static void onPlayerJoin(PlayerEvent.PlayerLoggedInEvent event) {

        Player player = event.getEntity();
        var server = player.getServer();
        var level = player.level();
        var soundPos = player.blockPosition();
    if (!((((ServerPlayer)player).getServer().getAdvancements().getAdvancement(new ResourceLocation("playtime:playtime/playtime")) != null && ((ServerPlayer)player).getAdvancements().getOrStartProgress(((ServerPlayer)player).getServer().getAdvancements().getAdvancement(new ResourceLocation("playtime:playtime/playtime"))).isDone()))) {
        player.getServer().getCommands().performPrefixedCommand(player.createCommandSourceStack().withSuppressedOutput(), "advancement grant " + player.getGameProfile().getName() + " only " + "playtime:playtime/playtime");
    }
    }
}
