package com.lumina.scene.osrs

import com.lumina.scene.graph.MaterialComponent
import com.lumina.scene.graph.MeshComponent
import com.lumina.scene.graph.SceneGraph
import com.lumina.scene.graph.Transform
import net.runelite.cache.definitions.OverlayDefinition
import net.runelite.cache.definitions.SpriteDefinition
import org.junit.jupiter.api.Assertions.assertArrayEquals
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

class OsrsWaterOverlayTest {
    @Test
    fun classicWaterTextureIdsAreRecognized() {
        for (textureId in intArrayOf(1, 2, 15, 17, 24, 25)) {
            val overlay = OverlayDefinition()
            overlay.texture = textureId
            assertTrue(OsrsWaterOverlay.isWaterOverlayByTexture(overlay), "texture $textureId should be water")
        }
    }

    @Test
    fun rlhdWaterOverlayIdsAreRecognized() {
        // 117HD tile_overrides.json: WATER_FLAT->6, WATER->151, Varrock fountain pools use flat water overlays.
        for (overlayId in intArrayOf(6, 151, 161, 380)) {
            assertTrue(OsrsWaterOverlay.isWaterOverlayId(overlayId), "overlay $overlayId should be water")
        }
        val stoneOverlay = OverlayDefinition()
        stoneOverlay.texture = 46
        val classification = OsrsWaterOverlay.classifyWaterTile(storedOverlayId = 999, overlay = stoneOverlay)
        assertFalse(classification.isWater)
        assertFalse(classification.byOverlayId)
        assertFalse(classification.byTextureId)
    }

    @Test
    fun overlayIdDetectionDoesNotRequireOverlayDefinition() {
        // Stored overlay 7 = definition 6 (WATER_FLAT).
        val classification = OsrsWaterOverlay.classifyWaterTile(storedOverlayId = 7, overlay = null)
        assertTrue(classification.isWater)
        assertTrue(classification.byOverlayId)
        assertFalse(classification.byTextureId)
    }

    @Test
    fun storedOverlayIdSpaceMatchesColorPath() {
        // Region.getOverlayId returns definition id + 1; WATER_OVERLAY_IDS is definition space.
        val flatWater = OsrsWaterOverlay.classifyWaterTile(storedOverlayId = 7, overlay = null)
        assertTrue(flatWater.isWater, "stored 7 (def 6, WATER_FLAT) must be water")
        assertTrue(flatWater.byOverlayId)

        val dirt = OsrsWaterOverlay.classifyWaterTile(storedOverlayId = 6, overlay = null)
        assertFalse(dirt.isWater, "stored 6 (def 5, dirt) must not be water")
        assertFalse(dirt.byOverlayId)
    }

    @Test
    fun textureIdIsSecondarySignalWhenOverlayIdUnknown() {
        val overlay = OverlayDefinition()
        overlay.texture = 1
        val classification = OsrsWaterOverlay.classifyWaterTile(storedOverlayId = 999, overlay = overlay)
        assertTrue(classification.isWater)
        assertFalse(classification.byOverlayId)
        assertTrue(classification.byTextureId)
    }

    @Test
    fun nonWaterTexturesAreExcluded() {
        val overlay = OverlayDefinition()
        overlay.texture = 46 // Varrock fountain ground stone per rs-codes
        assertFalse(OsrsWaterOverlay.isWaterOverlayByTexture(overlay))
        overlay.texture = -1
        assertFalse(OsrsWaterOverlay.isWaterOverlayByTexture(overlay))
    }

    @Test
    fun waterMaterialUsesUniformAlbedoNotVertexColorMode() {
        val material = MaterialComponent(
            albedo = OsrsWaterOverlay.ALBEDO_LINEAR.copyOf(),
            roughness = OsrsWaterOverlay.ROUGHNESS,
            metallic = OsrsWaterOverlay.METALLIC
        )
        assertFalse(material.metallic > 1.5f, "water must not use terrain vertex-color mode")
        assertArrayEquals(floatArrayOf(0.04f, 0.12f, 0.16f), material.albedo, 0.001f)
        assertEquals(0.05f, material.roughness, 0.001f)
    }

    @Test
    fun fullyTransparentWaterSpriteYieldsNoAverageColor() {
        val sprite = SpriteDefinition()
        sprite.setWidth(4)
        sprite.setHeight(1)
        sprite.setMaxWidth(4)
        sprite.setMaxHeight(1)
        sprite.setPalette(intArrayOf(0x00000000, 0xFF0066CC.toInt()))
        sprite.setPixelIdx(byteArrayOf(0, 0, 0, 0))

        val totals = OsrsTextureColorCache.accumulateSpriteRgb(sprite)
        assertEquals(0L, totals[3], "transparent water sprite pixels must not contribute")

        val cache = textureCache(emptyMap())
        val fallback = OsrsColorDecoder.texturedFallbackLinear()
        assertArrayEquals(fallback, cache.linearRgbOrFallback(1), 0.001f)
    }

    @Test
    fun waterChunkMeshUsesSeparateNodeNaming() {
        val graph = SceneGraph()
        val waterMesh = MeshComponent(floatArrayOf(0f), intArrayOf(0), 1, 1)
        val node = graph.createNode("water_12853_p0_0_0")
        node.addComponent(Transform())
        node.addComponent(waterMesh)
        node.addComponent(
            MaterialComponent(
                albedo = OsrsWaterOverlay.ALBEDO_LINEAR.copyOf(),
                roughness = OsrsWaterOverlay.ROUGHNESS,
                metallic = OsrsWaterOverlay.METALLIC
            )
        )
        assertTrue(node.name.startsWith("water_"))
        assertFalse(node.getComponent(MaterialComponent::class.java)!!.metallic > 1.5f)
    }

    private fun textureCache(map: Map<Int, FloatArray>): OsrsTextureColorCache {
        val ctor = OsrsTextureColorCache::class.java.getDeclaredConstructor(Map::class.java)
        ctor.isAccessible = true
        return ctor.newInstance(map) as OsrsTextureColorCache
    }
}
