package com.lumina.scene.osrs

import com.lumina.scene.graph.MaterialComponent
import com.lumina.scene.graph.MeshComponent
import com.lumina.scene.graph.SceneGraph
import com.lumina.scene.graph.Transform
import net.runelite.cache.models.JagexColor
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Assertions.assertSame
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test
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
    fun upperPlaneTileFilterRequiresOverlayUnderlayOrLocation() {
        assertTrue(OsrsMapLoader.shouldRenderUpperPlaneTile(overlayId = 1, underlayId = 0, hasLocation = false))
        assertTrue(OsrsMapLoader.shouldRenderUpperPlaneTile(overlayId = 0, underlayId = 2, hasLocation = false))
        assertTrue(OsrsMapLoader.shouldRenderUpperPlaneTile(overlayId = 0, underlayId = 0, hasLocation = true))
        assertFalse(OsrsMapLoader.shouldRenderUpperPlaneTile(overlayId = 0, underlayId = 0, hasLocation = false))
    }

    @Test
    fun objectHeightUsesPlaneSpecificSampleFormula() {
        val heightUnits = 384
        val planeY = OsrsCoordinateMapper.luminaYFromHeightUnits128(heightUnits)
        assertEquals(-384 / 128f * OsrsMapLoader.TILE_SCALE, planeY, 0.001f)
    }
}

class OsrsColorDecoderTest {
    @Test
    fun hslDecodeMatchesJagexColorForKnownValues() {
        val cases = intArrayOf(0, 960, 3500, 15200)
        for (hsl in cases) {
            val expected = JagexColor.HSLtoRGB(hsl.toShort(), JagexColor.BRIGHTNESS_MAX)
            val decoded = OsrsColorDecoder.hslToRgb(hsl)
            assertEquals(
                ((expected shr 16) and 0xFF) / 255f,
                decoded[0],
                0.001f,
                "R mismatch for hsl=$hsl"
            )
            assertEquals(
                ((expected shr 8) and 0xFF) / 255f,
                decoded[1],
                0.001f,
                "G mismatch for hsl=$hsl"
            )
            assertEquals(
                (expected and 0xFF) / 255f,
                decoded[2],
                0.001f,
                "B mismatch for hsl=$hsl"
            )
        }
    }

    @Test
    fun greenHueIsGreenerThanOldApproximation() {
        // Hue ~22/63 (green-yellow grass) should have G > R unlike naive HSL with /63 hue scale error
        val hsl = JagexColor.packHSL(22, 3, 60).toInt()
        val rgb = OsrsColorDecoder.hslToRgb(hsl)
        assertTrue(rgb[1] > rgb[0], "Grass-like HSL should be green-dominant: ${rgb.contentToString()}")
    }
}
