package com.lumina.scene.osrs

import net.runelite.cache.models.JagexColor
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertFalse
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
    fun cameraOnKnownTileMatchesRegionLocalGeometryPlacement() {
        val originBaseX = 3152
        val originBaseY = 3488
        val regionId = 12850
        val localTileX = 40
        val localTileY = 25

        val (geoX, geoZ) = OsrsCoordinateMapper.regionLocalTileToLuminaXZ(
            localTileX,
            localTileY,
            regionId,
            originBaseX,
            originBaseY
        )

        val (regionBaseX, regionBaseY) = OsrsCoordinateMapper.regionOriginTiles(regionId)
        val worldTileX = regionBaseX + localTileX
        val worldTileY = regionBaseY + localTileY
        val cameraLocalX = (worldTileX - originBaseX) * 128
        val cameraLocalY = (worldTileY - originBaseY) * 128

        val cam = OsrsCoordinateMapper.cameraToLumina(
            cameraX = cameraLocalX,
            cameraY = cameraLocalY,
            cameraZ = 0,
            cameraPitch = 0,
            cameraYaw = 0,
            baseX = originBaseX,
            baseY = originBaseY,
            originBaseX = originBaseX,
            originBaseY = originBaseY
        )

        assertEquals(geoX, cam.x, 0.001f, "camera X must match geometry tile placement")
        assertEquals(geoZ, cam.z, 0.001f, "camera Z must match geometry tile placement (north = -Z)")
    }

    @Test
    fun worldTileTransformMatchesRegionOffsetPlusLocalTile() {
        val originBaseX = 3152
        val originBaseY = 3488
        val regionId = 12906
        val localTileX = 10
        val localTileY = 20

        val (fromLocal, fromWorld) = run {
            val a = OsrsCoordinateMapper.regionLocalTileToLuminaXZ(
                localTileX, localTileY, regionId, originBaseX, originBaseY
            )
            val (rbx, rby) = OsrsCoordinateMapper.regionOriginTiles(regionId)
            val b = OsrsCoordinateMapper.worldTileToLuminaXZ(
                (rbx + localTileX).toFloat(),
                (rby + localTileY).toFloat(),
                originBaseX,
                originBaseY
            )
            a to b
        }

        assertEquals(fromLocal.first, fromWorld.first, 0.001f)
        assertEquals(fromLocal.second, fromWorld.second, 0.001f)
    }

    @Test
    fun centerRegionTileAlignsWhenSceneBaseIsNotRegionAligned() {
        val originBaseX = 3152
        val originBaseY = 3456
        val centerRegionId = 12906
        val localTileX = 32
        val localTileY = 32

        val (luminaX, luminaZ) = OsrsCoordinateMapper.regionLocalTileToLuminaXZ(
            localTileX,
            localTileY,
            centerRegionId,
            originBaseX,
            originBaseY
        )

        val (regionBaseX, regionBaseY) = OsrsCoordinateMapper.regionOriginTiles(centerRegionId)
        val worldTileX = regionBaseX + localTileX
        val worldTileY = regionBaseY + localTileY

        val cam = OsrsCoordinateMapper.cameraToLumina(
            cameraX = (worldTileX - originBaseX) * 128,
            cameraY = (worldTileY - originBaseY) * 128,
            cameraZ = 0,
            cameraPitch = 0,
            cameraYaw = 0,
            baseX = originBaseX,
            baseY = originBaseY,
            originBaseX = originBaseX,
            originBaseY = originBaseY
        )

        assertEquals(luminaX, cam.x, 0.001f)
        assertEquals(luminaZ, cam.z, 0.001f)

        val (offsetX, offsetZ) = OsrsCoordinateMapper.regionWorldOffset(centerRegionId, originBaseX, originBaseY)
        val legacyX = localTileX * OsrsMapLoader.TILE_SCALE + offsetX
        val legacyZ = offsetZ - localTileY * OsrsMapLoader.TILE_SCALE
        assertEquals(luminaX, legacyX, 0.001f)
        assertEquals(luminaZ, legacyZ, 0.001f)
    }

    @Test
    fun yawZeroFacesNorth() {
        val (fx, fy, fz) = OsrsCoordinateMapper.osrsForwardVectorLumina(0, 0)
        assertEquals(0f, fx, 0.001f)
        assertEquals(0f, fy, 0.001f)
        assertEquals(-1f, fz, 0.001f)
        assertEquals("N", OsrsCoordinateMapper.cardinalFacingFromForward(fx, fz))
    }

    @Test
    fun yawOneQuarterTurnFacesWest() {
        val (fx, fy, fz) = OsrsCoordinateMapper.osrsForwardVectorLumina(0, 0x1000)
        assertEquals(-1f, fx, 0.01f)
        assertEquals(0f, fy, 0.01f)
        assertEquals(0f, fz, 0.01f)
        assertEquals("W", OsrsCoordinateMapper.cardinalFacingFromForward(fx, fz))
    }

    @Test
    fun yawHalfTurnFacesSouth() {
        val (fx, _, fz) = OsrsCoordinateMapper.osrsForwardVectorLumina(0, 0x2000)
        assertEquals(0f, fx, 0.01f)
        assertEquals(1f, fz, 0.01f)
        assertEquals("S", OsrsCoordinateMapper.cardinalFacingFromForward(fx, fz))
    }

    @Test
    fun yawThreeQuarterTurnFacesEast() {
        val (fx, _, fz) = OsrsCoordinateMapper.osrsForwardVectorLumina(0, 0x3000)
        assertEquals(1f, fx, 0.01f)
        assertEquals(0f, fz, 0.01f)
        assertEquals("E", OsrsCoordinateMapper.cardinalFacingFromForward(fx, fz))
    }

    @Test
    fun osrsPitchPositiveLooksDown() {
        val (_, fy, _) = OsrsCoordinateMapper.osrsForwardVectorLumina(0x400, 0)
        assertTrue(fy < 0f, "Expected downward OSRS pitch as negative Lumina forward.y, got $fy")
    }

    @Test
    fun tileCenterNorthDecreasesZ() {
        val regionId = 12850
        val originBaseX = 3200
        val originBaseY = 3200
        val (x0, _, z0) = OsrsCoordinateMapper.tileCenterLumina(10, 10, regionId, originBaseX, originBaseY)
        val (_, _, z1) = OsrsCoordinateMapper.tileCenterLumina(10, 11, regionId, originBaseX, originBaseY)
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

    @Test
    fun luminaYFromHeightUnits128NegatesOsrsUp() {
        assertEquals(-2.56f, OsrsCoordinateMapper.luminaYFromHeightUnits128(128), 0.001f)
        assertEquals(0f, OsrsCoordinateMapper.luminaYFromHeightUnits128(0), 0.001f)
    }

    /**
     * Varrock fountain end-to-end trace (region 12853, tile ≈ (3213, 3428)):
     *   scene-load origin ≈ (3161, 3376); region base (3200, 3392); local tile (13, 36)
     *   geometry lumina XZ = (133.12, -133.12)
     *   camera locals after scene scroll use CURRENT base, subtract LOAD origin only.
     */
    @Test
    fun varrockFountainLoaderMatchesCameraWithScrolledSceneBase() {
        val loadOriginBaseX = 3161
        val loadOriginBaseY = 3376
        val regionId = 12853
        val localTileX = 13
        val localTileY = 36
        val playerWorldTileX = 3213f
        val playerWorldTileY = 3428f

        val (geoX, geoZ) = OsrsCoordinateMapper.regionLocalTileToLuminaXZ(
            localTileX,
            localTileY,
            regionId,
            loadOriginBaseX,
            loadOriginBaseY
        )
        assertEquals(133.12f, geoX, 0.01f)
        assertEquals(-133.12f, geoZ, 0.01f)

        val currentBaseX = 3169
        val currentBaseY = 3384
        val cameraLocalX = ((playerWorldTileX - currentBaseX) * 128).toInt()
        val cameraLocalY = ((playerWorldTileY - currentBaseY) * 128).toInt()

        val cam = OsrsCoordinateMapper.cameraToLumina(
            cameraX = cameraLocalX,
            cameraY = cameraLocalY,
            cameraZ = 0,
            cameraPitch = 0,
            cameraYaw = 0,
            baseX = currentBaseX,
            baseY = currentBaseY,
            originBaseX = loadOriginBaseX,
            originBaseY = loadOriginBaseY
        )

        assertEquals(geoX, cam.x, 0.01f, "camera X must match terrain at Varrock fountain")
        assertEquals(geoZ, cam.z, 0.01f, "camera Z must match terrain at Varrock fountain")
    }

    @Test
    fun usingLoadTimeBaseWithScrolledLocalsOffsetsCameraBySceneScroll() {
        val loadOriginBaseX = 3161
        val loadOriginBaseY = 3376
        val loadBaseX = 3161
        val loadBaseY = 3376
        val currentBaseX = 3169
        val currentBaseY = 3384
        val playerWorldTileX = 3213f
        val playerWorldTileY = 3428f

        val cameraLocalX = ((playerWorldTileX - currentBaseX) * 128).toInt()
        val cameraLocalY = ((playerWorldTileY - currentBaseY) * 128).toInt()

        val correct = OsrsCoordinateMapper.cameraToLumina(
            cameraLocalX, cameraLocalY, 0, 0, 0,
            currentBaseX, currentBaseY, loadOriginBaseX, loadOriginBaseY
        )
        val wrong = OsrsCoordinateMapper.cameraToLumina(
            cameraLocalX, cameraLocalY, 0, 0, 0,
            loadBaseX, loadBaseY, loadOriginBaseX, loadOriginBaseY
        )

        assertEquals(8f * OsrsMapLoader.TILE_SCALE, correct.x - wrong.x, 0.01f)
        assertEquals(8f * OsrsMapLoader.TILE_SCALE, wrong.z - correct.z, 0.01f)
    }
}
