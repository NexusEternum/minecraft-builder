package com.lumina.game

import com.lumina.plugin.LiveGameSnapshot
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Assertions.assertNull
import org.junit.jupiter.api.Test

class LiveGameStateTest {
    @Test
    fun latestSnapshotNullBeforeClientStarts() {
        val state = LiveGameState()
        assertNull(state.latestSnapshot())
        assertFalse(state.isRunning())
    }

    @Test
    fun liveGameSnapshotSceneReadyRequiresRegionsAndBase() {
        val ready = LiveGameSnapshot(
            loggedIn = true,
            baseX = 3161,
            baseY = 3376,
            plane = 0,
            mapRegions = intArrayOf(12853),
            cameraX = 6656,
            cameraY = 6656,
            cameraZ = 0,
            cameraPitch = 0,
            cameraYaw = 0,
            playerLocalX = 6656,
            playerLocalY = 6656,
            playerPlane = 0
        )
        assert(ready.isSceneReady())
        assert(!ready.copy(baseX = 0, baseY = 0).isSceneReady())
        assert(!ready.copy(mapRegions = IntArray(0)).isSceneReady())
    }

    @Test
    fun liveGameSnapshotWorldTileHelpers() {
        val snapshot = LiveGameSnapshot(
            loggedIn = true,
            baseX = 3161,
            baseY = 3376,
            plane = 0,
            mapRegions = intArrayOf(12853),
            cameraX = 6656,
            cameraY = 6656,
            cameraZ = 0,
            cameraPitch = 0,
            cameraYaw = 0,
            playerLocalX = 6656,
            playerLocalY = 6656,
            playerPlane = 0
        )
        assertEquals(3213f, snapshot.cameraWorldTileX(), 0.001f)
        assertEquals(3428f, snapshot.cameraWorldTileY(), 0.001f)
    }

    @Test
    fun liveGameSnapshotEqualityUsesRegionContent() {
        val regions = intArrayOf(12850, 12906)
        val a = LiveGameSnapshot(
            loggedIn = true,
            baseX = 3200,
            baseY = 3200,
            plane = 0,
            mapRegions = regions,
            cameraX = 1280,
            cameraY = 2560,
            cameraZ = 640,
            cameraPitch = 512,
            cameraYaw = 1024,
            playerLocalX = 6400,
            playerLocalY = 3200,
            playerPlane = 0
        )
        val b = a.copy(mapRegions = regions.copyOf())
        assert(a == b)
    }
}
