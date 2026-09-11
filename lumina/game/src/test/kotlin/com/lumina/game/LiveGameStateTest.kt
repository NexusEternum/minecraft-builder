package com.lumina.game

import com.lumina.plugin.LiveGameSnapshot
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
            cameraYaw = 1024
        )
        val b = a.copy(mapRegions = regions.copyOf())
        assert(a == b)
    }
}
