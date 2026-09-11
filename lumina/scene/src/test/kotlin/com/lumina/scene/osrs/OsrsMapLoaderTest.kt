package com.lumina.scene.osrs

import com.lumina.scene.graph.MaterialComponent
import com.lumina.scene.graph.MeshComponent
import com.lumina.scene.graph.SceneGraph
import com.lumina.scene.graph.Transform
import net.runelite.cache.models.JagexColor
import org.junit.jupiter.api.Assertions.assertArrayEquals
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Assertions.assertSame
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test
import kotlin.math.abs
import java.io.File

class OsrsMapLoaderTest {
    @Test
    fun loadRegionReturnsFalseForMissingCache() {
        val loader = OsrsMapLoader(SceneGraph(), XteaKeyService())
        val missingCache = File("/nonexistent/osrs/cache/path")
        assertFalse(loader.loadRegion(missingCache, 12850))
    }

    @Test
    fun loadRegionsReturnsFalseForEmptyAfterFilteringInvalidIds() {
        val loader = OsrsMapLoader(SceneGraph(), XteaKeyService())
        val missingCache = File("/nonexistent/osrs/cache/path")
        assertFalse(loader.loadRegions(missingCache, intArrayOf(0, -1), 3200, 3200))
    }

    @Test
    fun regionWorldOffsetMatchesKnownRegionId() {
        val (ox, oz) = OsrsCoordinateMapper.regionWorldOffset(12850, 3200, 3200)
        assertEquals(0f, ox, 0.001f)
        assertEquals(0f, oz, 0.001f)

        val (eastX, eastZ) = OsrsCoordinateMapper.regionWorldOffset(13106, 3200, 3200)
        assertEquals(64f * OsrsMapLoader.TILE_SCALE, eastX, 0.001f)
        assertEquals(0f, eastZ, 0.001f)
    }

    @Test
    fun sharedMeshInstancesDedupByReference() {
        val graph = SceneGraph()
        val sharedVerts = floatArrayOf(0f, 0f, 0f, 0f, 1f, 0f, 0f, 0f)
        val sharedIndices = intArrayOf(0, 1, 2)
        val sharedMesh = MeshComponent(sharedVerts, sharedIndices, 3, 1)

        val nodeA = graph.createNode("obj_a")
        nodeA.addComponent(Transform(x = 1f, y = 0f, z = 2f))
        nodeA.addComponent(sharedMesh)

        val nodeB = graph.createNode("obj_b")
        nodeB.addComponent(Transform(x = 5f, y = 0f, z = 8f))
        nodeB.addComponent(sharedMesh)

        val meshNodes = graph.nodesWithComponent(MeshComponent::class.java)
        assertEquals(2, meshNodes.size)
        assertSame(
            meshNodes[0].getComponent(MeshComponent::class.java),
            meshNodes[1].getComponent(MeshComponent::class.java)
        )

        val transforms = meshNodes.map { it.getComponent(Transform::class.java)!! }
        assertEquals(1f, transforms[0].x)
        assertEquals(5f, transforms[1].x)
        assertEquals(2f, transforms[0].z)
        assertEquals(8f, transforms[1].z)
    }

    @Test
    fun loadUpperPlanesDefaultsFalse() {
        val loader = OsrsMapLoader(SceneGraph(), XteaKeyService())
        assertFalse(loader.loadUpperPlanes)
        assertEquals(0, loader.maxVisiblePlane)
    }

    @Test
    fun upperPlaneTileFilterRequiresOverlayOrLocationNotUnderlayAlone() {
        assertTrue(OsrsMapLoader.shouldRenderUpperPlaneTile(overlayId = 1, hasLocation = false))
        assertFalse(OsrsMapLoader.shouldRenderUpperPlaneTile(overlayId = 0, hasLocation = false))
        assertTrue(OsrsMapLoader.shouldRenderUpperPlaneTile(overlayId = 0, hasLocation = true))
        // b16 regression: underlay-only must not render upper terrain sheets
        assertFalse(
            OsrsMapLoader.shouldRenderUpperPlaneTile(overlayId = 0, underlayId = 2, hasLocation = false)
        )
    }

    @Test
    fun visiblePlanesForPlayerIncludesBelowAndCurrentExcludesAbove() {
        assertArrayEquals(intArrayOf(0), OsrsCoordinateMapper.visiblePlanesForPlayer(0))
        assertArrayEquals(intArrayOf(0, 1), OsrsCoordinateMapper.visiblePlanesForPlayer(1))
        assertArrayEquals(intArrayOf(0, 1, 2), OsrsCoordinateMapper.visiblePlanesForPlayer(2))
        assertArrayEquals(intArrayOf(0, 1, 2, 3), OsrsCoordinateMapper.visiblePlanesForPlayer(3))
        assertArrayEquals(intArrayOf(0, 1, 2, 3), OsrsCoordinateMapper.visiblePlanesForPlayer(99))
    }

    @Test
    fun objectHeightUsesPlaneSpecificSampleFormula() {
        val heightUnits = 384
        val planeY = OsrsCoordinateMapper.luminaYFromHeightUnits128(heightUnits)
        assertEquals(-384 / 128f * OsrsMapLoader.TILE_SCALE, planeY, 0.001f)
    }

    /**
     * Varrock fountain tile (region 12853, local 13/36): terrain and objects must share lumina XZ.
     * Region.loadLocations() stores world tiles; passing them into regionLocalTileToLuminaXZ as
     * region-local (b16 regression) double-adds the region base (~3200 tiles → horizon cluster).
     */
    @Test
    fun objectAtWorldTileMatchesTerrainPlacementAtVarrockFountain() {
        val originBaseX = 3161
        val originBaseY = 3376
        val regionId = 12853
        val localTileX = 13
        val localTileY = 36
        val (regionBaseX, regionBaseY) = OsrsCoordinateMapper.regionOriginTiles(regionId)
        val worldTileX = regionBaseX + localTileX
        val worldTileY = regionBaseY + localTileY

        assertEquals(3213, worldTileX)
        assertEquals(3428, worldTileY)

        val (terrainX, terrainZ) = OsrsCoordinateMapper.regionLocalTileToLuminaXZ(
            localTileX,
            localTileY,
            regionId,
            originBaseX,
            originBaseY
        )
        assertEquals(133.12f, terrainX, 0.01f)
        assertEquals(-133.12f, terrainZ, 0.01f)

        val (objectX, objectZ) = OsrsCoordinateMapper.worldTileToLuminaXZ(
            worldTileX.toFloat(),
            worldTileY.toFloat(),
            originBaseX,
            originBaseY
        )
        assertEquals(terrainX, objectX, 0.001f, "object X must match terrain at same tile")
        assertEquals(terrainZ, objectZ, 0.001f, "object Z must match terrain at same tile")

        val (buggyX, buggyZ) = OsrsCoordinateMapper.regionLocalTileToLuminaXZ(
            worldTileX,
            worldTileY,
            regionId,
            originBaseX,
            originBaseY
        )
        assertFalse(
            abs(terrainX - buggyX) < 1f,
            "world tile coords mistaken for region-local must not match terrain (regression guard)"
        )
        assertEquals(8325.12f, buggyX, 0.01f)
        assertEquals(-8816.64f, buggyZ, 0.01f)
    }
}

class OsrsColorDecoderTest {
    @Test
    fun defaultBrightnessIsVanillaMiddleSetting() {
        assertEquals(JagexColor.BRIGHTNESS_LOW, OsrsColorDecoder.DEFAULT_BRIGHTNESS, 0.0001)
    }

    @Test
    fun hslDecodeAppliesLinearizationFromVanillaBrightness() {
        val cases = intArrayOf(0, 960, 3500, 15200)
        for (hsl in cases) {
            val srgb = JagexColor.HSLtoRGB(hsl.toShort(), JagexColor.BRIGHTNESS_LOW)
            val expectedR = OsrsColorDecoder.srgbToLinear(((srgb shr 16) and 0xFF) / 255f)
            val expectedG = OsrsColorDecoder.srgbToLinear(((srgb shr 8) and 0xFF) / 255f)
            val expectedB = OsrsColorDecoder.srgbToLinear((srgb and 0xFF) / 255f)
            val decoded = OsrsColorDecoder.hslToRgb(hsl)
            assertEquals(expectedR, decoded[0], 0.001f, "R mismatch for hsl=$hsl")
            assertEquals(expectedG, decoded[1], 0.001f, "G mismatch for hsl=$hsl")
            assertEquals(expectedB, decoded[2], 0.001f, "B mismatch for hsl=$hsl")
        }
    }

    @Test
    fun greenHueIsGreenDominantNotNearWhite() {
        val hsl = JagexColor.packHSL(25, 5, 60).toInt()
        val rgb = OsrsColorDecoder.hslToRgb(hsl)
        assertTrue(rgb[1] > rgb[0], "Grass-like HSL should be green-dominant: ${rgb.contentToString()}")
        assertTrue(rgb[1] > rgb[2], "Grass-like HSL should have strongest green channel")
        assertTrue(rgb[0] < 0.2f && rgb[2] < 0.3f, "Grass green should not wash to near-white: ${rgb.contentToString()}")
    }

    @Test
    fun magentaMarkerSubstitutedForOverlaysUnderlaysAndHsl() {
        assertTrue(OsrsColorDecoder.isMagentaTextureMarker(0xFF00FF))
        val fallback = OsrsColorDecoder.texturedFallbackLinear()
        assertArrayEquals(fallback, OsrsColorDecoder.underlayRgb(0xFF00FF), 0.001f)
        assertEquals(null, OsrsColorDecoder.overlayRgb(0xFF00FF))
        assertArrayEquals(fallback, OsrsColorDecoder.texturedFallbackLinear(), 0.001f)
    }

    @Test
    fun objectPlaneVisibilityRespectsMaxVisiblePlane() {
        assertTrue(OsrsMapLoader.isObjectPlaneVisible(0, maxVisiblePlane = 0))
        assertFalse(OsrsMapLoader.isObjectPlaneVisible(1, maxVisiblePlane = 0))
        assertTrue(OsrsMapLoader.isObjectPlaneVisible(1, maxVisiblePlane = 1))
        assertTrue(OsrsMapLoader.isObjectPlaneVisible(2, maxVisiblePlane = 3))
        assertFalse(OsrsMapLoader.isObjectPlaneVisible(3, maxVisiblePlane = 2))
    }
}
