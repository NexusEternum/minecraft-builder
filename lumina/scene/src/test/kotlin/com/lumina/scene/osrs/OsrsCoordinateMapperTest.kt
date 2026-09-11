package com.lumina.scene.osrs

import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test
import kotlin.math.PI
import kotlin.math.abs

class OsrsCoordinateMapperTest {
    @Test
    fun jau14ToRadiansFullCircle() {
        assertEquals(0.0, OsrsCoordinateMapper.jau14ToRadians(0), 1e-9)
        assertEquals(PI / 2, OsrsCoordinateMapper.jau14ToRadians(0x1000), 1e-6)
        assertEquals(PI, OsrsCoordinateMapper.jau14ToRadians(0x2000), 1e-6)
        assertEquals(PI * 1.5, OsrsCoordinateMapper.jau14ToRadians(0x3000), 1e-6)
        // Mask wraps at 14 bits
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
        // Scene tile (10, 20) at height 640 local units -> Lumina (25.6, -12.8, 51.2)
        val cam = OsrsCoordinateMapper.cameraToLumina(
            cameraX = 10 * 128,
            cameraY = 20 * 128,
            cameraZ = 640,
            cameraPitch = 0,
            cameraYaw = 0,
            originBaseX = 3200,
            originBaseY = 3200
        )
        assertEquals(10f * OsrsMapLoader.TILE_SCALE, cam.x, 0.001f)
        assertEquals(20f * OsrsMapLoader.TILE_SCALE, cam.z, 0.001f)
        assertEquals(-5f * OsrsMapLoader.TILE_SCALE, cam.y, 0.001f)
    }

    @Test
    fun cameraYawZeroFacesNorthPositiveZ() {
        val (_, yaw) = OsrsCoordinateMapper.cameraAnglesToLumina(0, 0)
        assertEquals(0f, yaw, 0.001f)
    }

    @Test
    fun cameraYawQuarterTurnFacesEastPositiveX() {
        val (_, yaw) = OsrsCoordinateMapper.cameraAnglesToLumina(0, 0x1000)
        assertEquals((PI / 2).toFloat(), yaw, 0.01f)
    }

    @Test
    fun cameraPitchPositiveLooksDownNegativePitch() {
        val (pitch, _) = OsrsCoordinateMapper.cameraAnglesToLumina(0x400, 0)
        assertTrue(pitch < 0f, "Expected downward pitch, got $pitch")
    }

    @Test
    fun regionWorldOffsetUsesSceneLocalOrigin() {
        // Region 12850 -> base tiles (50*64, 50*64) = (3200, 3200)
        val (ox, oz) = OsrsCoordinateMapper.regionWorldOffset(12850, 3200, 3200)
        assertEquals(0f, ox, 0.001f)
        assertEquals(0f, oz, 0.001f)

        // Neighbour one region east: region 13106 -> (3264, 3200)
        val (eastX, eastZ) = OsrsCoordinateMapper.regionWorldOffset(13106, 3200, 3200)
        assertEquals(64f * OsrsMapLoader.TILE_SCALE, eastX, 0.001f)
        assertEquals(0f, eastZ, 0.001f)
    }

    @Test
    fun regionOriginTilesFromPackedId() {
        assertEquals(3200 to 3200, OsrsCoordinateMapper.regionOriginTiles(12850))
        assertEquals(3264 to 3200, OsrsCoordinateMapper.regionOriginTiles(13106))
    }

    @Test
    fun mapRegionsKeyIsOrderIndependent() {
        val a = intArrayOf(12850, 12906, 12851)
        val b = intArrayOf(12906, 12851, 12850)
        assertEquals(OsrsCoordinateMapper.mapRegionsKey(a), OsrsCoordinateMapper.mapRegionsKey(b))
    }
}
