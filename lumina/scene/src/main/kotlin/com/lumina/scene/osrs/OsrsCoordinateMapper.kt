package com.lumina.scene.osrs

import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin
import kotlin.math.sqrt

/**
 * Converts RuneLite client camera/scene coordinates into Lumina world units.
 *
 * Lumina world is **right-handed**: X = east, Y = up, Z = south (north = −Z).
 *
 * Scene-local origin: geometry is expressed relative to [originBaseX]/[originBaseY]
 * (client [Client.getBaseX]/[getBaseY] at load time) to keep float coordinates small for RT precision.
 *
 * OSRS scene axes (Perspective): X = east, Y = north, Z = up.
 * OSRS camera yaw/pitch are JAU14 (0x4000 per revolution, Perspective.UNIT14).
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
        val forwardX: Float,
        val forwardY: Float,
        val forwardZ: Float
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
     * Z offset is negated so north (OSRS +Y) maps to Lumina −Z.
     */
    fun regionWorldOffset(
        regionId: Int,
        originBaseX: Int,
        originBaseY: Int
    ): Pair<Float, Float> {
        val (regionBaseX, regionBaseY) = regionOriginTiles(regionId)
        val offsetX = (regionBaseX - originBaseX) * TILE_SCALE
        val offsetZ = -(regionBaseY - originBaseY) * TILE_SCALE
        return offsetX to offsetZ
    }

    /** Valid, unique region IDs from a client [Client.getMapRegions] array (drops 0 / negative). */
    fun normalizeRegionIds(mapRegions: IntArray): IntArray =
        mapRegions.filter { it > 0 }.distinct().toIntArray()

    fun jau14ToRadians(jau: Int): Double = (jau and (JAU14_UNITS - 1)) * JAU14_TO_RADIANS

    /** Local scene tile coords (0..104) from 1/128-tile local units. */
    fun localUnitsToSceneTiles(localUnits: Int): Float = localUnits / 128f

    /**
     * Camera position and forward in Lumina world units relative to [originBaseX]/[originBaseY].
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
        val luminaZ = -(baseY + sceneTileY - originBaseY) * TILE_SCALE
        val luminaY = -localUnitsToSceneTiles(cameraZ) * TILE_SCALE

        val (fx, fy, fz) = osrsForwardVectorLumina(cameraPitch, cameraYaw)
        return LuminaCamera(luminaX, luminaY, luminaZ, fx, fy, fz)
    }

    /**
     * OSRS camera forward in Lumina world coords (unit vector).
     *
     * Derived from Perspective.localToCanvasGpu yaw-then-pitch (X=east, Y=north, Z=up):
     *   osrsForward = (sin(y)cos(p), cos(y)cos(p), −sin(p))
     * Mapped into right-handed Lumina (X=east, Y=up, Z=south):
     *   luminaForward = (osrsEast, osrsUp, −osrsNorth)
     *
     * Pinned cases:
     *   yaw=0, pitch=0 → (0, 0, −1) north
     *   yaw=0x1000 (90°), pitch=0 → (1, 0, 0) east
     *   pitch>0 → forward.y < 0 (looking down)
     */
    fun osrsForwardVectorLumina(cameraPitch: Int, cameraYaw: Int): Triple<Float, Float, Float> {
        val pitchRad = jau14ToRadians(cameraPitch).toFloat()
        val yawRad = jau14ToRadians(cameraYaw).toFloat()
        val cp = cos(pitchRad)
        val sp = sin(pitchRad)
        val sy = sin(yawRad)
        val cy = cos(yawRad)
        val forwardX = sy * cp
        val forwardY = -sp
        val forwardZ = -cy * cp
        return normalizeTriple(forwardX, forwardY, forwardZ)
    }

    /** Lumina tile centre in world units for a region-local tile coordinate. */
    fun tileCenterLumina(localTileX: Int, localTileY: Int, worldOffsetX: Float, worldOffsetZ: Float): Triple<Float, Float, Float> {
        val x = localTileX * TILE_SCALE + worldOffsetX
        val z = worldOffsetZ - localTileY * TILE_SCALE
        return Triple(x, 0f, z)
    }

    /**
     * Build a column-major view-inverse matrix from camera position and forward (same layout as
     * [com.lumina.renderer.rt.RayTracingPipeline.computeViewInverse]).
     */
    fun viewInverseFromForward(
        px: Float,
        py: Float,
        pz: Float,
        forwardX: Float,
        forwardY: Float,
        forwardZ: Float
    ): FloatArray {
        val (fx, fy, fz) = normalizeTriple(forwardX, forwardY, forwardZ)
        // Camera looks down −Z_cam; viewInverse third column is camera-back = −forward.
        val bx = -fx
        val by = -fy
        val bz = -fz
        // right = normalize(up × back), up = (0,1,0) → (back.z, 0, −back.x)
        var rx = bz
        var ry = 0f
        var rz = -bx
        val rLen = sqrt(rx * rx + ry * ry + rz * rz)
        if (rLen > 1e-6f) {
            rx /= rLen
            ry /= rLen
            rz /= rLen
        } else {
            rx = 1f
            ry = 0f
            rz = 0f
        }
        // up = back × right
        val ux = by * rz - bz * ry
        val uy = bz * rx - bx * rz
        val uz = bx * ry - by * rx
        return floatArrayOf(
            rx, ry, rz, 0f,
            ux, uy, uz, 0f,
            bx, by, bz, 0f,
            px, py, pz, 1f
        )
    }

    fun mapRegionsKey(mapRegions: IntArray): String =
        normalizeRegionIds(mapRegions).sorted().joinToString(",")

    private fun normalizeTriple(x: Float, y: Float, z: Float): Triple<Float, Float, Float> {
        val len = sqrt(x * x + y * y + z * z)
        if (len <= 1e-6f) return Triple(0f, 0f, -1f)
        return Triple(x / len, y / len, z / len)
    }
}
