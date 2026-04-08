package com.generated.playtime.event;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.item.ItemStack;
import net.minecraft.registry.Registries;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.SoundCategory;
import net.minecraft.sound.SoundEvents;
import net.minecraft.text.Text;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;

/**
 * Event registrations for Playtime.
 */
public class ModEvents {
    private static final Map<UUID, String> LAST_OFFHAND_ITEM = new HashMap<>();
    private static final Map<UUID, Integer> LAST_OFFHAND_COUNT = new HashMap<>();

    public static void register() {
        ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> {
            ServerPlayerEntity player = handler.getPlayer();
            ServerWorld world = player.getServerWorld();
            BlockPos soundPos = player.getBlockPos();
            if (!((((ServerPlayerEntity)player).getServer().getAdvancementLoader().get(new Identifier("playtime:playtime/playtime")) != null && ((ServerPlayerEntity)player).getAdvancementTracker().getProgress(((ServerPlayerEntity)player).getServer().getAdvancementLoader().get(new Identifier("playtime:playtime/playtime"))).isDone()))) {
        player.getServer().getCommandManager().executeWithPrefix(player.getCommandSource().withSilent(), "advancement grant " + player.getName().getString() + " only " + "playtime:playtime/playtime");
    }
        });
    }
}
