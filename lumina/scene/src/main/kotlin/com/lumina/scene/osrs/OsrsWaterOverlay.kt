package com.lumina.scene.osrs

import net.runelite.cache.definitions.OverlayDefinition

/**
 * OSRS tile-overlay water detection.
 *
 * Primary signal: tile **overlay id** (117HD [tile_overrides.json] waterType entries).
 * Secondary signal: overlay **texture id** (animated water sprites in flo.dat).
 */
object OsrsWaterOverlay {
    /**
     * Overlay ids assigned a non-NONE waterType in 117HD RLHD tile_overrides.json.
     * Extracted from entries with waterType != NONE (overlay id 0 excluded — means no overlay).
     *
     * @see [117HD tile_overrides.json](https://github.com/117HD/RLHD/blob/master/src/main/resources/rs117/hd/scene/tile_overrides.json)
     */
    val WATER_OVERLAY_IDS: Set<Int> = setOf(
        6, 7, 13, 29, 37, 41, 42, 59, 66, 67, 72, 73, 85, 86, 89, 95, 104, 124, 128, 130,
        133, 136, 151, 156, 158, 161, 181, 196, 201, 245, 246, 292, 302, 304, 331, 364, 380,
        381, 454, 456, 636
    )

    /** Texture ids used by water overlays in flo.dat (secondary / legacy signal). */
    val WATER_TEXTURE_IDS: Set<Int> = setOf(1, 2, 15, 17, 24, 25)

    /** Path-traced water albedo — brighter green-teal in linear space. */
    val ALBEDO_LINEAR = floatArrayOf(0.04f, 0.12f, 0.16f)

    const val ROUGHNESS = 0.05f
    const val METALLIC = 0.0f

    data class WaterTileClassification(
        val isWater: Boolean,
        val byOverlayId: Boolean,
        val byTextureId: Boolean
    )

    /** True when [overlayDefinitionId] is a 117HD water overlay (flo definition id, not map-stored +1). */
    fun isWaterOverlayId(overlayDefinitionId: Int): Boolean = overlayDefinitionId in WATER_OVERLAY_IDS

    fun isWaterOverlayByTexture(overlay: OverlayDefinition): Boolean =
        overlay.texture in WATER_TEXTURE_IDS

    /**
     * Classify a tile overlay as water by overlay id (primary) and/or texture id (secondary).
     *
     * @param storedOverlayId Raw value from [net.runelite.cache.region.Region.getOverlayId] (definition id + 1;
     *   0 means no overlay). The overlay-id check converts to definition space via [storedOverlayId] - 1 to
     *   match [WATER_OVERLAY_IDS]. Texture ids on [overlay] are not offset.
     */
    fun classifyWaterTile(storedOverlayId: Int, overlay: OverlayDefinition?): WaterTileClassification {
        if (storedOverlayId <= 0) {
            return WaterTileClassification(isWater = false, byOverlayId = false, byTextureId = false)
        }
        val byOverlayId = isWaterOverlayId(storedOverlayId - 1)
        val byTextureId = overlay != null && isWaterOverlayByTexture(overlay)
        return WaterTileClassification(
            isWater = byOverlayId || byTextureId,
            byOverlayId = byOverlayId,
            byTextureId = byTextureId
        )
    }

    /** @deprecated Use [classifyWaterTile] or [isWaterOverlayByTexture] for explicit signal choice. */
    fun isWaterOverlay(overlay: OverlayDefinition): Boolean =
        isWaterOverlayByTexture(overlay)
}
