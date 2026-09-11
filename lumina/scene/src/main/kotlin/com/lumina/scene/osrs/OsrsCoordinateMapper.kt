package com.lumina.scene.osrs

import kotlin.math.PI
import kotlin.math.atan2
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
     * OSRS convention: regionX = id >> 8, regionY = id & 0xFF; each region is 64×64 tiles.
     */
    fun regionOriginTiles(regionId: Int): Pair<Int, Int> {
        val regionX = (regionId shr 8) and 0xFF
        val regionY = regionId and 0xFF
        return regionX * 64 to regionY * 64
    }

    /**
     * Shared horizontal placement: world tile → Lumina XZ relative to scene origin.
     *
     * Derivation (must match [OsrsMapLoader] terrain/object placement after b15 Z-flip):
     *   worldTileX = regionBaseX + localTileX
     *   luminaX = (worldTileX − originBaseX) × TILE_SCALE
     *   luminaZ = −(worldTileY − originBaseY) × TILE_SCALE   // north (OSRS +Y) → Lumina −Z
     */
    fun worldTileToLuminaXZ(
        worldTileX: Float,
        worldTileY: Float,
        originBaseX: Int,
        originBaseY: Int
    ): Pair<Float, Float> {
        val luminaX = (worldTileX - originBaseX) * TILE_SCALE
        val luminaZ = -(worldTileY - originBaseY) * TILE_SCALE
        return luminaX to luminaZ
    }

    /** Region-local tile (0..63) → Lumina XZ via [worldTileToLuminaXZ]. */
    fun regionLocalTileToLuminaXZ(
        localTileX: Int,
        localTileY: Int,
        regionId: Int,
        originBaseX: Int,
        originBaseY: Int
    ): Pair<Float, Float> {
        val (regionBaseX, regionBaseY) = regionOriginTiles(regionId)
        return worldTileToLuminaXZ(
            regionBaseX + localTileX.toFloat(),
            regionBaseY + localTileY.toFloat(),
            originBaseX,
            originBaseY
        )
    }

    /**
     * Lumina placement offset for a region relative to the scene-local origin.
     * Equivalent to [regionLocalTileToLuminaXZ](0, 0, regionId, originBaseX, originBaseY).
     */
    fun regionWorldOffset(
        regionId: Int,
        originBaseX: Int,
        originBaseY: Int
    ): Pair<Float, Float> = regionLocalTileToLuminaXZ(0, 0, regionId, originBaseX, originBaseY)

    /** Vertical OSRS height (1/128 tile units, same as tile heights / cameraZ) → Lumina Y. */
    fun luminaYFromHeightUnits128(heightUnits: Int): Float =
        -heightUnits / 128f * TILE_SCALE

    /** Valid, unique region IDs from a client [Client.getMapRegions] array (drops 0 / negative). */
    fun normalizeRegionIds(mapRegions: IntArray): IntArray =
        mapRegions.filter { it > 0 }.distinct().toIntArray()

    fun jau14ToRadians(jau: Int): Double = (jau and (JAU14_UNITS - 1)) * JAU14_TO_RADIANS

    /** Local scene tile coords (0..104) from 1/128-tile local units. */
    fun localUnitsToSceneTiles(localUnits: Int): Float = localUnits / 128f

    /** World tile coords from scene SW base + local 1/128-tile units. */
    fun localSceneUnitsToWorldTiles(
        baseX: Int,
        baseY: Int,
        localUnitsX: Int,
        localUnitsY: Int
    ): Pair<Float, Float> {
        val worldTileX = baseX + localUnitsToSceneTiles(localUnitsX)
        val worldTileY = baseY + localUnitsToSceneTiles(localUnitsY)
        return worldTileX to worldTileY
    }

    /**
     * Camera position and forward in Lumina world units relative to [originBaseX]/[originBaseY].
     * Horizontal position uses the same [worldTileToLuminaXZ] transform as map geometry.
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
        val (worldTileX, worldTileY) = localSceneUnitsToWorldTiles(baseX, baseY, cameraX, cameraY)
        val (luminaX, luminaZ) = worldTileToLuminaXZ(worldTileX, worldTileY, originBaseX, originBaseY)
        val luminaY = luminaYFromHeightUnits128(cameraZ)

        val (fx, fy, fz) = osrsForwardVectorLumina(cameraPitch, cameraYaw)
        return LuminaCamera(luminaX, luminaY, luminaZ, fx, fy, fz)
    }

    /**
     * OSRS camera forward in Lumina world coords (unit vector).
     *
     * ## Derivation (Perspective.localToCanvasCpu / localToCanvasGpu)
     *
     * Scene-local axes: `x` = east, `y` = north, `z` = up. Relative to camera:
     * ```
     * x1 =  x·cos(yaw) + y·sin(yaw)
     * y1 =  y·cos(yaw) − x·sin(yaw)
     * y2 =  z·cos(pitch) − y1·sin(pitch)
     * z1 =  y1·cos(pitch) + z·sin(pitch)      // depth; visible when z1 ≥ 50
     * screenX = viewportW/2 + x1·scale/z1
     * screenY = viewportH/2 + y2·scale/z1
     * ```
     * Screen centre (`x1 = 0`, `y2 = 0`, `z1 > 0`). At `pitch = 0`: `z = 0`, `y1 = z1 > 0`, so
     * `x·cos + y·sin = 0` and `y > 0`. With `cos(yaw) > 0` this gives the horizontal unit vector
     * `(x, y) = (−sin(yaw), cos(yaw))` in OSRS east/north.
     *
     * **Camera yaw zero-direction (JAU14, [Client.getCameraYaw]):** index `0` → `yaw_rad = 0` →
     * `(x, y) = (0, 1)` → **north** (+Y). Increasing yaw advances **clockwise** on the compass
     * (east → south → west): `0x1000` → west, `0x2000` → south, `0x3000` → east.
     *
     * **Pitch sign:** `camAngleX` defaults to `128`; range ≈`128…512` JAU14 (`Client` / RSClient).
     * Larger pitch ⇒ larger `sin(pitch)` ⇒ more negative `y2` contribution ⇒ camera tilted **down**
     * (horizon moves up on screen). Mapped to Lumina: `forwardY = −sin(pitch) < 0`.
     *
     * **Entity orientation cross-check** ([net.runelite.api.coords.Angle], OSRS docs): NPC/player
     * facing uses JAU11 (`0…2047`, `0x4000` in JAU14 = `angle << 3`) where **0 = south** and
     * **1024 = north**. That is the *entity facing* convention, **not** [Client.getCameraYaw]:
     * camera yaw `0` already faces north (see `camAngleY = 0` default + minimap north-up).
     *
     * ## Lumina mapping (X = east, Y = up, Z = south; north = −Z)
     * ```
     * luminaForward = (−sin(yaw)·cos(pitch), −sin(pitch), −cos(yaw)·cos(pitch))
     * ```
     */
    fun osrsForwardVectorLumina(cameraPitch: Int, cameraYaw: Int): Triple<Float, Float, Float> {
        val pitchRad = jau14ToRadians(cameraPitch).toFloat()
        val yawRad = jau14ToRadians(cameraYaw).toFloat()
        val cp = cos(pitchRad)
        val sp = sin(pitchRad)
        val sy = sin(yawRad)
        val cy = cos(yawRad)
        val forwardX = -sy * cp
        val forwardY = -sp
        val forwardZ = -cy * cp
        return normalizeTriple(forwardX, forwardY, forwardZ)
    }

    /** Eight-way compass label from a horizontal Lumina forward (north = −Z). */
    fun cardinalFacingFromForward(forwardX: Float, forwardZ: Float): String {
        if (forwardX * forwardX + forwardZ * forwardZ < 1e-8f) return "?"
        val degrees = Math.toDegrees(atan2(forwardX.toDouble(), -forwardZ.toDouble()))
        val bearing = ((degrees + 360.0) % 360.0).toFloat()
        return when {
            bearing < 22.5f || bearing >= 337.5f -> "N"
            bearing < 67.5f -> "NE"
            bearing < 112.5f -> "E"
            bearing < 157.5f -> "SE"
            bearing < 202.5f -> "S"
            bearing < 247.5f -> "SW"
            bearing < 292.5f -> "W"
            else -> "NW"
        }
    }

    /** Lumina tile centre in world units for a region-local tile coordinate. */
    fun tileCenterLumina(
        localTileX: Int,
        localTileY: Int,
        regionId: Int,
        originBaseX: Int,
        originBaseY: Int
    ): Triple<Float, Float, Float> {
        val (x, z) = regionLocalTileToLuminaXZ(localTileX, localTileY, regionId, originBaseX, originBaseY)
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
