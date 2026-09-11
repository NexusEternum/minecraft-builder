package com.lumina.scene.osrs

import net.runelite.cache.definitions.SpriteDefinition
import org.junit.jupiter.api.Assertions.assertArrayEquals
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test

class OsrsTextureColorServiceTest {
    @Test
    fun averageSpritePixelsSkipsTransparentAndMagenta() {
        val sprite = SpriteDefinition()
        sprite.setWidth(3)
        sprite.setHeight(1)
        sprite.setMaxWidth(3)
        sprite.setMaxHeight(1)
        sprite.setPalette(
            intArrayOf(
                0x00000000,
                0xFFFF0000.toInt(),
                OsrsColorDecoder.MAGENTA_TEXTURE_MARKER,
                0xFF0000FF.toInt()
            )
        )
        sprite.setPixelIdx(byteArrayOf(0, 1, 3))

        val totals = OsrsTextureColorCache.accumulateSpriteRgb(sprite)
        assertEquals(2L, totals[3], "only red and blue pixels count")
        assertEquals(255L, totals[0], "red channel sum")
        assertEquals(255L, totals[2], "blue channel sum")

        val avgPacked = ((totals[0] / totals[3]).toInt() shl 16) or (totals[2] / totals[3]).toInt()
        val linear = OsrsColorDecoder.packedRgbToLinearFloats(avgPacked)
        val expectedR = OsrsColorDecoder.srgbToLinear(127.5f / 255f)
        val expectedB = OsrsColorDecoder.srgbToLinear(127.5f / 255f)
        assertEquals(expectedR, linear[0], 0.02f)
        assertEquals(0f, linear[1], 0.02f)
        assertEquals(expectedB, linear[2], 0.02f)
    }

    @Test
    fun textureIdMissUsesFallback() {
        val cache = OsrsTextureColorCache.build(emptyMap())
        val fallback = OsrsColorDecoder.texturedFallbackLinear()
        assertArrayEquals(fallback, cache.linearRgbOrFallback(9999), 0.001f)
        assertEquals(null, cache.linearRgb(9999))
    }

    private fun OsrsTextureColorCache.Companion.build(map: Map<Int, FloatArray>): OsrsTextureColorCache {
        val ctor = OsrsTextureColorCache::class.java.getDeclaredConstructor(Map::class.java)
        ctor.isAccessible = true
        return ctor.newInstance(map) as OsrsTextureColorCache
    }
}
