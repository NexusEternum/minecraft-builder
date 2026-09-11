package com.lumina.plugin

/**
 * Read-only snapshot of the embedded RuneLite client's live scene/camera state.
 * Populated by the :game module; consumed by client-core for --play mirror mode.
 */
data class LiveGameSnapshot(
    val loggedIn: Boolean,
    val baseX: Int,
    val baseY: Int,
    val plane: Int,
    /** Loaded map region IDs (typically up to nine surrounding regions). */
    val mapRegions: IntArray,
    /** Camera position in local scene coords; 1/128 tile units (see RuneLite LocalPoint). */
    val cameraX: Int,
    val cameraY: Int,
    /** Camera height in the same 1/128 tile vertical units as tile heights. */
    val cameraZ: Int,
    /** Pitch in JAU14 (0x4000 units per full revolution). */
    val cameraPitch: Int,
    /** Yaw in JAU14 (0x4000 units per full revolution). */
    val cameraYaw: Int,
    /** Local player position in scene coords; 1/128 tile units (LocalPoint). */
    val playerLocalX: Int,
    val playerLocalY: Int,
    /** Local player render plane (0..3). */
    val playerPlane: Int,
    /** RuneLite camera zoom ([net.runelite.api.Client.getScale]); focal length in pixels at canvas height. */
    val cameraScale: Int = 512,
    /** Embedded game canvas height in pixels ([net.runelite.api.Client.getCanvasHeight]). */
    val canvasHeight: Int = 503
) {
    /** Camera world tile X from this snapshot's [baseX] + [cameraX]/128. */
    fun cameraWorldTileX(): Float = baseX + cameraX / 128f

    /** Camera world tile Y from this snapshot's [baseY] + [cameraY]/128. */
    fun cameraWorldTileY(): Float = baseY + cameraY / 128f

    /** Player world tile X from this snapshot's [baseX] + [playerLocalX]/128. */
    fun playerWorldTileX(): Float = baseX + playerLocalX / 128f

    /** Player world tile Y from this snapshot's [baseY] + [playerLocalY]/128. */
    fun playerWorldTileY(): Float = baseY + playerLocalY / 128f

    /** True when scene base and regions are populated enough for mirror load. */
    fun isSceneReady(): Boolean =
        loggedIn && mapRegions.isNotEmpty() && (baseX != 0 || baseY != 0)

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is LiveGameSnapshot) return false
        return loggedIn == other.loggedIn &&
            baseX == other.baseX &&
            baseY == other.baseY &&
            plane == other.plane &&
            mapRegions.contentEquals(other.mapRegions) &&
            cameraX == other.cameraX &&
            cameraY == other.cameraY &&
            cameraZ == other.cameraZ &&
            cameraPitch == other.cameraPitch &&
            cameraYaw == other.cameraYaw &&
            playerLocalX == other.playerLocalX &&
            playerLocalY == other.playerLocalY &&
            playerPlane == other.playerPlane &&
            cameraScale == other.cameraScale &&
            canvasHeight == other.canvasHeight
    }

    override fun hashCode(): Int {
        var result = loggedIn.hashCode()
        result = 31 * result + baseX
        result = 31 * result + baseY
        result = 31 * result + plane
        result = 31 * result + mapRegions.contentHashCode()
        result = 31 * result + cameraX
        result = 31 * result + cameraY
        result = 31 * result + cameraZ
        result = 31 * result + cameraPitch
        result = 31 * result + cameraYaw
        result = 31 * result + playerLocalX
        result = 31 * result + playerLocalY
        result = 31 * result + playerPlane
        result = 31 * result + cameraScale
        result = 31 * result + canvasHeight
        return result
    }
}

/**
 * Poll-based view into the embedded RuneLite client, implemented reflectively by :game.
 */
interface LiveGameView {
    /** Latest snapshot, or null before the client injector is ready. */
    fun latestSnapshot(): LiveGameSnapshot?

    /** Whether the embedded client thread is still running. */
    fun isRunning(): Boolean
}
