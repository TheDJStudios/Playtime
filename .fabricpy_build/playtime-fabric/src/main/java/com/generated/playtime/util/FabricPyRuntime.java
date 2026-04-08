package com.generated.playtime.util;

import net.minecraft.block.BlockState;
import net.minecraft.entity.Entity;
import net.minecraft.particle.DefaultParticleType;
import net.minecraft.registry.Registries;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.util.Identifier;
import net.minecraft.util.hit.BlockHitResult;
import net.minecraft.util.hit.HitResult;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Vec3d;
import net.minecraft.world.RaycastContext;
import net.minecraft.world.World;

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

    public static Vec3d normalize3(double x, double y, double z) {
        double len = length3(x, y, z);
        if (len <= 0.000001d) {
            return new Vec3d(0, 0, 0);
        }
        return new Vec3d(x / len, y / len, z / len);
    }

    public static Vec3d add3(double x1, double y1, double z1, double x2, double y2, double z2) {
        return new Vec3d(x1 + x2, y1 + y2, z1 + z2);
    }

    public static BlockHitResult raycastBlock(World world, Vec3d start, Vec3d end) {
        return world.raycast(new RaycastContext(start, end, RaycastContext.ShapeType.OUTLINE, RaycastContext.FluidHandling.NONE, (Entity)null));
    }

    public static String raycastBlockId(World world, Vec3d start, Vec3d end) {
        BlockHitResult hit = raycastBlock(world, start, end);
        if (hit.getType() != HitResult.Type.BLOCK) {
            return "";
        }
        BlockState state = world.getBlockState(hit.getBlockPos());
        return Registries.BLOCK.getId(state.getBlock()).toString();
    }

    public static int raycastBlockPosX(World world, Vec3d start, Vec3d end) {
        BlockHitResult hit = raycastBlock(world, start, end);
        return hit.getType() == HitResult.Type.BLOCK ? hit.getBlockPos().getX() : 0;
    }

    public static int raycastBlockPosY(World world, Vec3d start, Vec3d end) {
        BlockHitResult hit = raycastBlock(world, start, end);
        return hit.getType() == HitResult.Type.BLOCK ? hit.getBlockPos().getY() : 0;
    }

    public static int raycastBlockPosZ(World world, Vec3d start, Vec3d end) {
        BlockHitResult hit = raycastBlock(world, start, end);
        return hit.getType() == HitResult.Type.BLOCK ? hit.getBlockPos().getZ() : 0;
    }

    public static void spawnParticle(World world, String particleId, double x, double y, double z, double dx, double dy, double dz, double speed, int count) {
        var particleType = Registries.PARTICLE_TYPE.get(new Identifier(particleId));
        if (!(particleType instanceof DefaultParticleType defaultParticle)) {
            return;
        }
        if (world instanceof ServerWorld serverWorld) {
            serverWorld.spawnParticles(defaultParticle, x, y, z, count, dx, dy, dz, speed);
            return;
        }
        for (int i = 0; i < Math.max(1, count); i++) {
            world.addParticle(defaultParticle, x, y, z, dx, dy, dz);
        }
    }
}
