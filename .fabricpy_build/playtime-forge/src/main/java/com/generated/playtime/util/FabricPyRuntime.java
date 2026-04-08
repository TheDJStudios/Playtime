package com.generated.playtime.util;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.SimpleParticleType;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.registries.ForgeRegistries;

public class FabricPyRuntime {
    public static double clamp(double value, double min, double max) {
        return Math.max(min, Math.min(max, value));
    }

    public static double lerp(double start, double end, double delta) {
        return start + ((end - start) * delta);
    }

    public static double distance3(double x1, double y1, double z1, double x2, double y2, double z2) {
        return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2) + Math.pow(z2 - z1, 2));
    }

    public static double length3(double x, double y, double z) {
        return Math.sqrt((x * x) + (y * y) + (z * z));
    }

    public static Vec3 normalize3(double x, double y, double z) {
        double len = length3(x, y, z);
        if (len <= 0.000001d) {
            return new Vec3(0, 0, 0);
        }
        return new Vec3(x / len, y / len, z / len);
    }

    public static Vec3 add3(double x1, double y1, double z1, double x2, double y2, double z2) {
        return new Vec3(x1 + x2, y1 + y2, z1 + z2);
    }

    public static BlockHitResult raycastBlock(Level level, Vec3 start, Vec3 end) {
        return level.clip(new ClipContext(start, end, ClipContext.Block.OUTLINE, ClipContext.Fluid.NONE, null));
    }

    public static String raycastBlockId(Level level, Vec3 start, Vec3 end) {
        BlockHitResult hit = raycastBlock(level, start, end);
        if (hit.getType() != HitResult.Type.BLOCK) {
            return "";
        }
        BlockState state = level.getBlockState(hit.getBlockPos());
        return ForgeRegistries.BLOCKS.getKey(state.getBlock()).toString();
    }

    public static int raycastBlockPosX(Level level, Vec3 start, Vec3 end) {
        BlockHitResult hit = raycastBlock(level, start, end);
        return hit.getType() == HitResult.Type.BLOCK ? hit.getBlockPos().getX() : 0;
    }

    public static int raycastBlockPosY(Level level, Vec3 start, Vec3 end) {
        BlockHitResult hit = raycastBlock(level, start, end);
        return hit.getType() == HitResult.Type.BLOCK ? hit.getBlockPos().getY() : 0;
    }

    public static int raycastBlockPosZ(Level level, Vec3 start, Vec3 end) {
        BlockHitResult hit = raycastBlock(level, start, end);
        return hit.getType() == HitResult.Type.BLOCK ? hit.getBlockPos().getZ() : 0;
    }

    public static void spawnParticle(Level level, String particleId, double x, double y, double z, double dx, double dy, double dz, double speed, int count) {
        var particleType = ForgeRegistries.PARTICLE_TYPES.getValue(new net.minecraft.resources.ResourceLocation(particleId));
        if (!(particleType instanceof SimpleParticleType simple)) {
            return;
        }
        if (level instanceof net.minecraft.server.level.ServerLevel serverLevel) {
            serverLevel.sendParticles(simple, x, y, z, count, dx, dy, dz, speed);
            return;
        }
        for (int i = 0; i < Math.max(1, count); i++) {
            level.addParticle(simple, x, y, z, dx, dy, dz);
        }
    }
}
