package com.lumina.scene.osrs

import net.runelite.cache.SpriteManager
import net.runelite.cache.TextureManager
import net.runelite.cache.definitions.SpriteDefinition
import net.runelite.cache.definitions.TextureDefinition
import net.runelite.cache.definitions.providers.SpriteProvider
import net.runelite.cache.fs.Store
import org.slf4j.LoggerFactory

/**
 * Per-texture average colors decoded from OSRS cache sprites.
 *
 * [net.runelite.cache.definitions.TextureDefinition] in cache 1.12.38 exposes [TextureDefinition.getFileIds]
 * (sprite archive ids) and [TextureDefinition.missingColor] but no precomputed averageRgb / field1777 —
 * those live in the live client, not the cache loader. Colors are computed from sprite pixels.
 */
class OsrsTextureColorCache private constructor(
    private val textureIdToLinearRgb: Map<Int, FloatArray>
) {
    fun linearRgb(textureId: Int): FloatArray? = textureIdToLinearRgb[textureId]

    fun linearRgbOrFallback(textureId: Int): FloatArray =
        textureIdToLinearRgb[textureId] ?: OsrsColorDecoder.texturedFallbackLinear()

    companion object {
        private val log = LoggerFactory.getLogger(OsrsTextureColorCache::class.java)

        fun build(store: Store): OsrsTextureColorCache {
            val textureManager = TextureManager(store)
            textureManager.load()
            val spriteManager = SpriteManager(store)
            spriteManager.load()

            val colors = HashMap<Int, FloatArray>()
            for (texture in textureManager.textures) {
                val textureId = texture.id
                val average = averageTextureColor(texture, spriteManager) ?: continue
                colors[textureId] = average
            }
            log.info("Built {} per-texture average colors from OSRS cache", colors.size)
            return OsrsTextureColorCache(colors)
        }

        /**
         * Mean sRGB of all non-transparent, non-magenta pixels across the texture's sprite frames.
         * Returns linear RGB floats for the path tracer.
         */
        fun averageTextureColor(texture: TextureDefinition, sprites: SpriteProvider): FloatArray? {
            val fileIds = texture.fileIds ?: return null
            if (fileIds.isEmpty()) return null

            var rSum = 0L
            var gSum = 0L
            var bSum = 0L
            var count = 0L
            for (spriteId in fileIds) {
                val sprite = sprites.provide(spriteId, 0) ?: continue
                val contribution = accumulateSpriteRgb(sprite, rSum, gSum, bSum, count)
                rSum = contribution[0]
                gSum = contribution[1]
                bSum = contribution[2]
                count = contribution[3]
            }
            if (count == 0L) return null
            val rgb = ((rSum / count).toInt() shl 16) or
                ((gSum / count).toInt() shl 8) or
                (bSum / count).toInt()
            return OsrsColorDecoder.packedRgbToLinearFloats(rgb)
        }

        /** @return long[4] = rSum, gSum, bSum, count */
        fun accumulateSpriteRgb(
            sprite: SpriteDefinition,
            rSum: Long = 0,
            gSum: Long = 0,
            bSum: Long = 0,
            count: Long = 0
        ): LongArray {
            sprite.normalize()
            val pixels = sprite.pixels
            if (pixels != null && pixels.isNotEmpty()) {
                return accumulateFromArgbPixels(pixels, rSum, gSum, bSum, count)
            }

            val indices = sprite.pixelIdx
            val palette = sprite.palette
            if (indices == null || palette == null || indices.isEmpty()) {
                return longArrayOf(rSum, gSum, bSum, count)
            }

            var rs = rSum
            var gs = gSum
            var bs = bSum
            var c = count
            for (idx in indices) {
                val palIdx = idx.toInt() and 0xFF
                if (palIdx == 0) continue
                val argb = palette[palIdx]
                val alpha = (argb ushr 24) and 0xFF
                if (alpha == 0) continue
                val rgb = argb and 0xFFFFFF
                if (OsrsColorDecoder.isMagentaTextureMarker(rgb)) continue
                rs += (rgb shr 16) and 0xFF
                gs += (rgb shr 8) and 0xFF
                bs += rgb and 0xFF
                c++
            }
            return longArrayOf(rs, gs, bs, c)
        }

        private fun accumulateFromArgbPixels(
            pixels: IntArray,
            rSum: Long,
            gSum: Long,
            bSum: Long,
            count: Long
        ): LongArray {
            var rs = rSum
            var gs = gSum
            var bs = bSum
            var c = count
            for (argb in pixels) {
                val alpha = (argb ushr 24) and 0xFF
                if (alpha == 0) continue
                val rgb = argb and 0xFFFFFF
                if (OsrsColorDecoder.isMagentaTextureMarker(rgb)) continue
                rs += (rgb shr 16) and 0xFF
                gs += (rgb shr 8) and 0xFF
                bs += rgb and 0xFF
                c++
            }
            return longArrayOf(rs, gs, bs, c)
        }
    }
}
