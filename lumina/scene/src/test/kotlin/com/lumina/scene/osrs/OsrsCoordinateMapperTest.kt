package com.lumina.scene.osrs

import net.runelite.cache.models.JagexColor
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test
import kotlin.math.PI
import kotlin.math.abs
import kotlin.math.sqrt

class OsrsCoordinateMapperTest {
    @Test
    fun jau14ToRadiansFullCircle() {
        assertEquals(0.0, OsrsCoordinateMapper.jau14ToRadians(0), 1e-9)
        assertEquals(PI / 2, OsrsCoordinateMapper.jau14ToRadians(0x1000), 1e-6)
        assertEquals(PI, OsrsCoordinateMapper.jau14ToRadians(0x2000), 1e-6)
        assertEquals(PI * 1.5, OsrsCoordinateMapper.jau14ToRadians(0x3000), 1e-6)
        assertEquals(0.0, OsrsCoordinateMapper.jau14ToRadians(0x4000), 1e-9)
    }

    @Test
    fun localUnitsToSceneTiles() {
        assertEquals(0f, OsrsCoordinateMapper.localUnitsToSceneTiles(0))
        assertEquals(1f, OsrsCoordinateMapper.localUnitsToSceneTiles(128))
        assertEquals(52.5f, OsrsCoordinateMapper.localUnitsToSceneTiles(6720))
    }

    @Test
    fun cameraPositionMapsLocalSceneUnitsToLuminaWorld() {
        val cam = OsrsCoordinateMapper.cameraToLumina(
            cameraX = 10 * 128,
            cameraY = 20 * 128,
            cameraZ = 640,
            cameraPitch = 0,
            cameraYaw = 0,
            baseX = 3200,
            baseY = 3200,
            originBaseX = 3200,
            originBaseY = 3200
        )
        assertEquals(10f * OsrsMapLoader.TILE_SCALE, cam.x, 0.001f)
        assertEquals(-20f * OsrsMapLoader.TILE_SCALE, cam.z, 0.001f)
        assertEquals(-5f * OsrsMapLoader.TILE_SCALE, cam.y, 0.001f)
    }

    @Test
    fun cameraPositionAccountsForSceneBaseShift() {
        val atOrigin = OsrsCoordinateMapper.cameraToLumina(
            40 * 128, 20 * 128, 0, 0, 0,
            baseX = 3200, baseY = 3200, originBaseX = 3200, originBaseY = 3200
        )
        val afterScroll = OsrsCoordinateMapper.cameraToLumina(
            32 * 128, 20 * 128, 0, 0, 0,
            baseX = 3208, baseY = 3200, originBaseX = 3200, originBaseY = 3200
        )
        assertEquals(atOrigin.x, afterScroll.x, 0.001f)
        assertEquals(atOrigin.z, afterScroll.z, 0.001f)
    }

    @Test
    fun osrsYawZeroForwardIsNorthMinusZ() {
        val (fx, fy, fz) = OsrsCoordinateMapper.osrsForwardVectorLumina(0, 0)
        assertEquals(0f, fx, 0.001f)
        assertEquals(0f, fy, 0.001f)
        assertEquals(-1f, fz, 0.001f)
    }

    @Test
    fun osrsYawQuarterTurnForwardIsEastPlusX() {
        val (fx, fy, fz) = OsrsCoordinateMapper.osrsForwardVectorLumina(0, 0x1000)
        assertEquals(1f, fx, 0.01f)
        assertEquals(0f, fy, 0.01f)
        assertEquals(0f, fz, 0.01f)
    }

    @Test
    fun osrsPitchPositiveLooksDown() {
        val (_, fy, _) = OsrsCoordinateMapper.osrsForwardVectorLumina(0x400, 0)
        assertTrue(fy < 0f, "Expected downward OSRS pitch as negative Lumina forward.y, got $fy")
    }

    @Test
    fun tileCenterNorthDecreasesZ() {
        val (x0, _, z0) = OsrsCoordinateMapper.tileCenterLumina(10, 10, 0f, 0f)
        val (_, _, z1) = OsrsCoordinateMapper.tileCenterLumina(10, 11, 0f, 0f)
        assertEquals(10f * OsrsMapLoader.TILE_SCALE, x0, 0.001f)
        assertTrue(z1 < z0, "Moving north (tileY+1) must decrease Lumina Z")
        assertEquals(OsrsMapLoader.TILE_SCALE, z0 - z1, 0.001f)
    }

    @Test
    fun regionWorldOffsetUsesSceneLocalOriginWithSouthPositiveZ() {
        val (ox, oz) = OsrsCoordinateMapper.regionWorldOffset(12850, 3200, 3200)
        assertEquals(0f, ox, 0.001f)
        assertEquals(0f, oz, 0.001f)

        val (eastX, eastZ) = OsrsCoordinateMapper.regionWorldOffset(13106, 3200, 3200)
        assertEquals(64f * OsrsMapLoader.TILE_SCALE, eastX, 0.001f)
        assertEquals(0f, eastZ, 0.001f)
    }

    @Test
    fun viewInverseFromForwardNorthMatchesRayGenBasis() {
        val view = OsrsCoordinateMapper.viewInverseFromForward(0f, 10f, 0f, 0f, 0f, -1f)
        // Third column = camera-back = −forward = (0,0,1); camera forward = −Z = north
        assertEquals(0f, view[8], 0.01f)
        assertEquals(0f, view[9], 0.01f)
        assertEquals(1f, view[10], 0.01f)
        // First column = right = east
        assertEquals(1f, view[0], 0.01f)
        assertEquals(0f, view[1], 0.01f)
        assertEquals(0f, view[2], 0.01f)
    }

    @Test
    fun regionOriginTilesFromPackedId() {
        assertEquals(3200 to 3200, OsrsCoordinateMapper.regionOriginTiles(12850))
        assertEquals(3264 to 3200, OsrsCoordinateMapper.regionOriginTiles(13106))
    }

    @Test
    fun normalizeRegionIdsDropsZerosAndDuplicates() {
        val normalized = OsrsCoordinateMapper.normalizeRegionIds(intArrayOf(0, 12850, 0, 12850, 12906))
        assertTrue(normalized.contentEquals(intArrayOf(12850, 12906)))
    }

    @Test
    fun mapRegionsKeyIsOrderIndependentAndIgnoresZeros() {
        val a = intArrayOf(12850, 0, 12906, 12851)
        val b = intArrayOf(12906, 12851, 12850)
        assertEquals(OsrsCoordinateMapper.mapRegionsKey(a), OsrsCoordinateMapper.mapRegionsKey(b))
    }
}
