package com.lumina.scene.osrs

import net.runelite.cache.definitions.OverlayDefinition

/**
 * OSRS tile-overlay water is identified by [OverlayDefinition.getTexture] referencing
 * animated water sprites (flo.dat opcode 2). Classic ids from cache / rs-codes:
 * 1 = still water, 2 = stone wall (mislabeled in some docs), 15/17/24/25 = flowing water variants.
 */
object OsrsWaterOverlay {
    /** Texture ids used by water overlays in flo.dat (not an exhaustive modern-cache list). */
    val WATER_TEXTURE_IDS: Set<Int> = setOf(1, 2, 15, 17, 24, 25)

    /** Path-traced water albedo — deep blue-teal in linear space. */
    val ALBEDO_LINEAR = floatArrayOf(0.02f, 0.08f, 0.12f)

    const val ROUGHNESS = 0.05f
    const val METALLIC = 0.0f

    fun isWaterOverlay(overlay: OverlayDefinition): Boolean =
        overlay.texture in WATER_TEXTURE_IDS
}
