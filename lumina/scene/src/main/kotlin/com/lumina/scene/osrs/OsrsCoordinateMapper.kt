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
 * Scene-local origin: geometry and camera are expressed relative to [originBaseX]/[originBaseY]
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

    fun jau14ToRadians(jau: Int): Double = (jau and (JAU14_UNITS - 1)) * JAU14_TO_RADIANS

    /**
     * Local scene tile coords (0..104) from 1/128-tile local units.
     */
    fun localUnitsToSceneTiles(localUnits: Int): Float = localUnits / 128f

    /**
     * Camera position in Lumina world units relative to [originBaseX]/[originBaseY].
     *
     * Formulas (scene-local origin at load-time base):
     * - luminaX = (cameraX / 128) * TILE_SCALE
     * - luminaZ = (cameraY / 128) * TILE_SCALE
     * - luminaY = -(cameraZ / 128) * TILE_SCALE
     */
    fun cameraToLumina(
        cameraX: Int,
        cameraY: Int,
        cameraZ: Int,
        cameraPitch: Int,
        cameraYaw: Int,
        originBaseX: Int,
        originBaseY: Int
    ): LuminaCamera {
        val sceneTileX = localUnitsToSceneTiles(cameraX)
        val sceneTileY = localUnitsToSceneTiles(cameraY)
        val luminaX = sceneTileX * TILE_SCALE
        val luminaZ = sceneTileY * TILE_SCALE
        val luminaY = -localUnitsToSceneTiles(cameraZ) * TILE_SCALE

        val (pitch, yaw) = cameraAnglesToLumina(cameraPitch, cameraYaw)
        return LuminaCamera(luminaX, luminaY, luminaZ, pitch, yaw)
    }

    /**
     * Converts JAU14 pitch/yaw into Lumina [CameraController] radians.
     *
     * Derivation mirrors RuneLite [Perspective.localToCanvasGpu] rotation: OSRS local X=east,
     * Y=north, Z=up; Lumina X=east, Z=north, Y=up. At OSRS yaw=0 the camera faces north (+Z).
     * Lumina [CameraController] at yaw=0 faces +Z, so yaw maps directly from JAU14 with axis flips
     * on pitch (OSRS positive pitch looks down; Lumina negative pitch looks down).
     */
    fun cameraAnglesToLumina(cameraPitch: Int, cameraYaw: Int): Pair<Float, Float> {
        val pitchRad = jau14ToRadians(cameraPitch).toFloat()
        val yawRad = jau14ToRadians(cameraYaw).toFloat()

        val pitchSin = sin(pitchRad)
        val pitchCos = cos(pitchRad)
        val yawSin = sin(yawRad)
        val yawCos = cos(yawRad)

        // Forward direction in Lumina world (unit) from Jagex yaw-then-pitch rotation.
        val dirX = yawSin * pitchCos
        val dirY = -pitchSin
        val dirZ = yawCos * pitchCos

        val luminaYaw = atan2(dirX, dirZ)
        val horizontal = sqrt(dirX * dirX + dirZ * dirZ)
        val luminaPitch = atan2(dirY, horizontal)
        return luminaPitch to luminaYaw
    }

    fun mapRegionsKey(mapRegions: IntArray): String =
        mapRegions.copyOf().sorted().joinToString(",")
}
