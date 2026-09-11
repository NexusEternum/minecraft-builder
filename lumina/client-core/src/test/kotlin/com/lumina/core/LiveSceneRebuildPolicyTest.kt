package com.lumina.core

import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

class LiveSceneRebuildPolicyTest {
    @Test
    fun noRebuildWhenPlaneUnchanged() {
        val step = LiveSceneRebuildPolicy.advancePlaneDebounce(
            LiveSceneRebuildPolicy.PlaneDebounceState(loadedMaxVisiblePlane = 0),
            snapshotPlane = 0
        )
        assertFalse(step.readyToRebuild)
        assertEquals(0, step.state.loadedMaxVisiblePlane)
        assertEquals(null, step.state.pendingMaxVisiblePlane)
    }

    @Test
    fun planeUpRequiresStablePollsBeforeRebuild() {
        var state = LiveSceneRebuildPolicy.PlaneDebounceState(loadedMaxVisiblePlane = 0)

        val first = LiveSceneRebuildPolicy.advancePlaneDebounce(state, snapshotPlane = 1)
        assertFalse(first.readyToRebuild)
        assertEquals(1, first.state.pendingMaxVisiblePlane)
        assertEquals(1, first.state.pendingPlaneStablePolls)

        val second = LiveSceneRebuildPolicy.advancePlaneDebounce(first.state, snapshotPlane = 1)
        assertTrue(second.readyToRebuild)
        assertEquals(1, second.state.loadedMaxVisiblePlane)
        assertEquals(null, second.state.pendingMaxVisiblePlane)
    }

    @Test
    fun planeDownRequiresStablePollsBeforeRebuild() {
        var state = LiveSceneRebuildPolicy.PlaneDebounceState(loadedMaxVisiblePlane = 2)

        val first = LiveSceneRebuildPolicy.advancePlaneDebounce(state, snapshotPlane = 0)
        assertFalse(first.readyToRebuild)
        assertEquals(0, first.state.pendingMaxVisiblePlane)

        val second = LiveSceneRebuildPolicy.advancePlaneDebounce(first.state, snapshotPlane = 0)
        assertTrue(second.readyToRebuild)
        assertEquals(0, second.state.loadedMaxVisiblePlane)
    }

    @Test
    fun planeDebounceResetsWhenSnapshotFlickers() {
        val first = LiveSceneRebuildPolicy.advancePlaneDebounce(
            LiveSceneRebuildPolicy.PlaneDebounceState(loadedMaxVisiblePlane = 0),
            snapshotPlane = 1
        )
        val flicker = LiveSceneRebuildPolicy.advancePlaneDebounce(first.state, snapshotPlane = 0)
        assertFalse(flicker.readyToRebuild)
        assertEquals(null, flicker.state.pendingMaxVisiblePlane)
        assertEquals(0, flicker.state.pendingPlaneStablePolls)
    }
}
