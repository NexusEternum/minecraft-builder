package com.lumina.core

/**
 * Pure debounce logic for live mirror scene rebuilds when the player's visible plane changes.
 * Extracted from [LuminaClient.maybeRebuildLiveScene] for unit testing.
 */
object LiveSceneRebuildPolicy {
    data class PlaneDebounceState(
        val loadedMaxVisiblePlane: Int,
        val pendingMaxVisiblePlane: Int? = null,
        val pendingPlaneStablePolls: Int = 0
    )

    data class PlaneDebounceStep(
        val state: PlaneDebounceState,
        /** True when [requiredStablePolls] consecutive polls agree on the new plane. */
        val readyToRebuild: Boolean
    )

    /**
     * @param snapshotPlane current player plane from live snapshot (already clamped 0..3)
     * @param requiredStablePolls polls the new plane must remain stable (default 2 ≈ 66 ms at 30 Hz)
     */
    fun advancePlaneDebounce(
        state: PlaneDebounceState,
        snapshotPlane: Int,
        requiredStablePolls: Int = 2
    ): PlaneDebounceStep {
        if (snapshotPlane == state.loadedMaxVisiblePlane) {
            return PlaneDebounceStep(
                PlaneDebounceState(state.loadedMaxVisiblePlane),
                readyToRebuild = false
            )
        }

        if (state.pendingMaxVisiblePlane != snapshotPlane) {
            return PlaneDebounceStep(
                PlaneDebounceState(
                    loadedMaxVisiblePlane = state.loadedMaxVisiblePlane,
                    pendingMaxVisiblePlane = snapshotPlane,
                    pendingPlaneStablePolls = 1
                ),
                readyToRebuild = false
            )
        }

        val polls = state.pendingPlaneStablePolls + 1
        if (polls < requiredStablePolls) {
            return PlaneDebounceStep(
                PlaneDebounceState(
                    loadedMaxVisiblePlane = state.loadedMaxVisiblePlane,
                    pendingMaxVisiblePlane = snapshotPlane,
                    pendingPlaneStablePolls = polls
                ),
                readyToRebuild = false
            )
        }

        return PlaneDebounceStep(
            PlaneDebounceState(loadedMaxVisiblePlane = snapshotPlane),
            readyToRebuild = true
        )
    }
}
