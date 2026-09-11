package com.lumina.scene.osrs

import kotlin.math.PI
import kotlin.math.atan2
import kotlin.math.cos
import kotlin.math.sin
import kotlin.math.sqrt

/**
 * Converts RuneLite client camera/scene coordinates into Lumina world units.
 *
 * Semantics (RuneLite API / Perspective):
 * - [cameraX]/[cameraY]: local scene position in 1/128 tile units (same as [net.runelite.api.coords.LocalPoint]).
 * - [cameraZ]: vertical height in the same 1/128 tile units as [Region.getTileHeight].
 * - [cameraPitch]/[cameraYaw]: JAU14 angles — 0x4000 units per full circle; see Perspective.UNIT14 (~pi/8192 rad/unit).
 * - Scene axes: local X = east, local Y = north; Lumina maps X=east, Z=north, Y=up with negated OSRS height.
 *
 * Scene-local origin: geometry is expressed relative to [originBaseX]/[originBaseY]
 * (client [Client.getBaseX]/[getBaseY] at load time) to keep float coordinates small for RT precision.
 */
object OsrsCoordinateMapper {
    /** JAU14 units per full revolution (14-bit Jagex angle). */
    const val JAU14_UNITS = 0x4000

    /** Radians per JAU14 unit (Perspective.UNIT14). */
    const val JAU14_TO_RADIANS = PI * 2.0 / JAU14_UNITS

    /** Lumina world units per OSRS tile (matches [OsrsMapLoader.TILE_SCALE]). */
    const val TILE_SCALE = OsrsMapLoader.TILE_SCALE

    data class LuminaCamera(
        val x: Float,
        val y: Float,
        val z: Float,
        val pitch: Float,
        val yaw: Float
    )

    /**
     * Region SW corner in world tile coords from a packed region id.
     * OSRS convention: regionX = id >> 8, regionY = id & 0xFF; each region is 64x64 tiles.
     */
    fun regionOriginTiles(regionId: Int): Pair<Int, Int> {
        val regionX = (regionId shr 8) and 0xFF
        val regionY = regionId and 0xFF
        return regionX * 64 to regionY * 64
    }

    /**
     * Lumina placement offset for a region relative to the scene-local origin.
     * Used when composing multi-region scenes.
     */
    fun regionWorldOffset(
        regionId: Int,
        originBaseX: Int,
        originBaseY: Int
    ): Pair<Float, Float> {
        val (regionBaseX, regionBaseY) = regionOriginTiles(regionId)
        val offsetX = (regionBaseX - originBaseX) * TILE_SCALE
        val offsetZ = (regionBaseY - originBaseY) * TILE_SCALE
        return offsetX to offsetZ
    }

    /** Valid, unique region IDs from a client [Client.getMapRegions] array (drops 0 / negative). */
    fun normalizeRegionIds(mapRegions: IntArray): IntArray =
        mapRegions.filter { it > 0 }.distinct().toIntArray()

    fun jau14ToRadians(jau: Int): Double = (jau and (JAU14_UNITS - 1)) * JAU14_TO_RADIANS

    /**
     * Local scene tile coords (0..104) from 1/128-tile local units.
     */
    fun localUnitsToSceneTiles(localUnits: Int): Float = localUnits / 128f

    /**
     * Camera position in Lumina world units relative to [originBaseX]/[originBaseY].
     *
     * [baseX]/[baseY] are the client's current scene SW corner (tiles); [cameraX]/[cameraY] are local
     * to that corner. World tile = base + local, then subtract the frozen scene origin used at load.
     */
    fun cameraToLumina(
        cameraX: Int,
        cameraY: Int,
        cameraZ: Int,
        cameraPitch: Int,
        cameraYaw: Int,
        baseX: Int,
        baseY: Int,
        originBaseX: Int,
        originBaseY: Int
    ): LuminaCamera {
        val sceneTileX = localUnitsToSceneTiles(cameraX)
        val sceneTileY = localUnitsToSceneTiles(cameraY)
        val luminaX = (baseX + sceneTileX - originBaseX) * TILE_SCALE
        val luminaZ = (baseY + sceneTileY - originBaseY) * TILE_SCALE
        val luminaY = -localUnitsToSceneTiles(cameraZ) * TILE_SCALE

        val (pitch, yaw) = cameraAnglesToLumina(cameraPitch, cameraYaw)
        return LuminaCamera(luminaX, luminaY, luminaZ, pitch, yaw)
    }

    /**
     * Converts JAU14 pitch/yaw into Lumina [CameraController] / [RayTracingPipeline.computeViewInverse] radians.
     *
     * ## OSRS basis (RuneLite Perspective.localToCanvasGpu)
     * Scene axes: X=east, Y=north, Z=up. Yaw then pitch; at yaw=0,pitch=0 the camera faces **north** (+Y).
     * Mapped into Lumina (X=east, Z=north, Y=up) the look direction is:
     *   f_osrs = (sin(y)cos(p), -sin(p), cos(y)cos(p))
     *
     * ## Lumina basis (CameraController + computeViewInverse)
     * Yaw about +Y, pitch about +X; rotation order R_yaw * R_pitch. View direction (camera looks down -Z_cam):
     *   f_lum = (cos(p)sin(y_l), -sin(p), -cos(p)cos(y_l))
     *
     * ## Matching (same pitch sign; yaw reflected across north)
     * f_lum = f_osrs when pitch_l = pitch_osrs and yaw_l = π - yaw_osrs.
     *
     * Decomposing f_osrs with atan2(dirX, dirZ) assumes yaw_l=0 faces +Z, but Lumina yaw_l=0 faces -Z;
     * that 180° yaw-plane mismatch couples with pitch and produces rotation about a tilted axis when yaw changes.
     */
    fun cameraAnglesToLumina(cameraPitch: Int, cameraYaw: Int): Pair<Float, Float> {
        val pitchRad = jau14ToRadians(cameraPitch).toFloat()
        val yawRad = jau14ToRadians(cameraYaw).toFloat()
        val luminaPitch = pitchRad
        val luminaYaw = normalizeAnglePi((PI - yawRad).toFloat())
        return luminaPitch to luminaYaw
    }

    /** OSRS camera forward unit vector in Lumina world coords (for tests / debugging). */
    fun osrsLookDirectionLumina(cameraPitch: Int, cameraYaw: Int): Triple<Float, Float, Float> {
        val pitchRad = jau14ToRadians(cameraPitch).toFloat()
        val yawRad = jau14ToRadians(cameraYaw).toFloat()
        val dirX = sin(yawRad) * cos(pitchRad)
        val dirY = -sin(pitchRad)
        val dirZ = cos(yawRad) * cos(pitchRad)
        return Triple(dirX, dirY, dirZ)
    }

    /** Lumina [RayTracingPipeline] view direction from pitch/yaw (unit vector). */
    fun luminaLookDirection(pitch: Float, yaw: Float): Triple<Float, Float, Float> {
        val cp = cos(pitch)
        val sp = sin(pitch)
        val sy = sin(yaw)
        val cy = cos(yaw)
        return Triple(cp * sy, -sp, -cp * cy)
    }

    private fun normalizeAnglePi(angle: Float): Float {
        var a = angle
        while (a > PI) a -= (2 * PI).toFloat()
        while (a < -PI) a += (2 * PI).toFloat()
        return a
    }

    fun mapRegionsKey(mapRegions: IntArray): String =
        normalizeRegionIds(mapRegions).sorted().joinToString(",")
}
