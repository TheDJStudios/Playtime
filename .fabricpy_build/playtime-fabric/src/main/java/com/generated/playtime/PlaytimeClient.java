package com.generated.playtime;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.blockrenderlayer.v1.BlockRenderLayerMap;
import net.minecraft.client.render.RenderLayer;


public class PlaytimeClient implements ClientModInitializer {

    @Override
    public void onInitializeClient() {
        BlockRenderLayerMap.INSTANCE.putBlock(ModBlocks.HAND_SCANNER, RenderLayer.getSolid());
        BlockRenderLayerMap.INSTANCE.putBlock(ModBlocks.HAND_SCANNER_RED_RIGHT, RenderLayer.getSolid());
        BlockRenderLayerMap.INSTANCE.putBlock(ModBlocks.CRITTER_PLUSH_HOPPY, RenderLayer.getSolid());



    }
}
