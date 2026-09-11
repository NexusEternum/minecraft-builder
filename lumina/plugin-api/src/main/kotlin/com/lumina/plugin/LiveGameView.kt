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
    val playerPlane: Int
) {
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
            playerPlane == other.playerPlane
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
