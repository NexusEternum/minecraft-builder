package com.lumina.scene.osrs

import net.runelite.cache.models.JagexColor

/**
 * OSRS color decode aligned with [net.runelite.cache.models.JagexColor].
 *
 * Jagex packed HSL (16-bit): 6-bit hue / 3-bit saturation / 7-bit luminance.
 * [JagexColor.HSLtoRGB] applies hue/sat offsets (+0.0078125, +0.0625) and brightness gamma.
 */
object OsrsColorDecoder {
    /** Default model/terrain brightness used by the RS2 renderer (JagexColor.BRIGHTNESS_MAX). */
    const val DEFAULT_BRIGHTNESS: Double = JagexColor.BRIGHTNESS_MAX

    /** Decode a Jagex packed HSL short to linear RGB floats in [0, 1]. */
    fun hslToRgb(hsl: Int, brightness: Double = DEFAULT_BRIGHTNESS): FloatArray {
        if (hsl == -1 || hsl == 12345678) return floatArrayOf(0f, 0f, 0f)
        val rgb = JagexColor.HSLtoRGB(hsl.toShort(), brightness)
        return OsrsMapLoader.packedRgbToFloats(rgb)
    }

    /** Underlay definitions store 24-bit RGB in [net.runelite.cache.definitions.UnderlayDefinition.color]. */
    fun underlayRgb(color: Int): FloatArray = OsrsMapLoader.packedRgbToFloats(color)

    /** Overlay primary/secondary colors are 24-bit RGB when present. */
    fun overlayRgb(rgb: Int): FloatArray? {
        if (rgb == 0 || rgb == -1) return null
        return OsrsMapLoader.packedRgbToFloats(rgb)
    }
}
