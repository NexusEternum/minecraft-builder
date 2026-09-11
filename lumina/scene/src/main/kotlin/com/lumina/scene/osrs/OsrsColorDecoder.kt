package com.lumina.scene.osrs

import net.runelite.cache.models.JagexColor
import kotlin.math.pow

/**
 * OSRS color decode aligned with [net.runelite.cache.models.JagexColor].
 *
 * Jagex packed HSL (16-bit): 6-bit hue / 3-bit saturation / 7-bit luminance.
 * [JagexColor.HSLtoRGB] applies hue/sat offsets (+0.0078125, +0.0625) and brightness gamma.
 *
 * Brightness: vanilla OSRS defaults to the middle client setting ([JagexColor.BRIGHTNESS_LOW], exponent 0.8).
 * [JagexColor.BRIGHTNESS_MAX] (0.6) is the brightest UI option and washes colors toward white.
 *
 * Linearization: HSLtoRGB output is display/sRGB-like (gamma already baked via [JagexColor.adjustForBrightness]).
 * The path tracer treats vertex colors as linear albedo, so channels are converted sRGB→linear before packing.
 */
object OsrsColorDecoder {
    /** Vanilla default brightness (middle client setting). Not [JagexColor.BRIGHTNESS_MAX] (brightest). */
    const val DEFAULT_BRIGHTNESS: Double = JagexColor.BRIGHTNESS_LOW

    /** Jagex marks textured/transparent slots with pure magenta in 24-bit RGB tables. */
    const val MAGENTA_TEXTURE_MARKER: Int = 0xFF00FF

    private val TEXTURED_FALLBACK_LINEAR = floatArrayOf(0.10f, 0.14f, 0.06f)

    fun isMagentaTextureMarker(rgb: Int): Boolean = (rgb and 0xFFFFFF) == MAGENTA_TEXTURE_MARKER

    /** Fallback linear albedo for textured overlays, underlays, and model faces. */
    fun texturedFallbackLinear(): FloatArray = TEXTURED_FALLBACK_LINEAR.copyOf()

    /** Decode a Jagex packed HSL short to linear RGB floats in [0, 1]. */
    fun hslToRgb(hsl: Int, brightness: Double = DEFAULT_BRIGHTNESS): FloatArray {
        if (hsl == -1 || hsl == 12345678) return floatArrayOf(0f, 0f, 0f)
        val rgb = JagexColor.HSLtoRGB(hsl.toShort(), brightness)
        if (isMagentaTextureMarker(rgb)) return texturedFallbackLinear()
        return packedRgbToLinearFloats(rgb)
    }

    /** Underlay definitions store 24-bit RGB in [net.runelite.cache.definitions.UnderlayDefinition.color]. */
    fun underlayRgb(color: Int): FloatArray {
        if (isMagentaTextureMarker(color)) return texturedFallbackLinear()
        return packedRgbToLinearFloats(color)
    }

    /** Overlay primary/secondary colors are 24-bit RGB when present. */
    fun overlayRgb(rgb: Int): FloatArray? {
        if (rgb == 0 || rgb == -1) return null
        if (isMagentaTextureMarker(rgb)) return null
        return packedRgbToLinearFloats(rgb)
    }

    /** Convert Jagex 24-bit RGB (display/sRGB-like) to linear [0, 1] floats for the path tracer. */
    fun packedRgbToLinearFloats(rgb: Int): FloatArray {
        val r = ((rgb shr 16) and 0xFF) / 255f
        val g = ((rgb shr 8) and 0xFF) / 255f
        val b = (rgb and 0xFF) / 255f
        return floatArrayOf(srgbToLinear(r), srgbToLinear(g), srgbToLinear(b))
    }

    /** sRGB channel → linear (IEC 61966-2-1). */
    fun srgbToLinear(channel: Float): Float =
        if (channel <= 0.04045f) channel / 12.92f
        else ((channel + 0.055f) / 1.055f).pow(2.4f)
}
