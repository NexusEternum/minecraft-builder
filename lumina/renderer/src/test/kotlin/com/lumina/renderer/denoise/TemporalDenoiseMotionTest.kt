package com.lumina.renderer.denoise

import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

class TemporalDenoiseMotionTest {
    @Test
    fun cameraMovedFactorDetectsPositionAndForwardDelta() {
        assertEquals(
            1f,
            TemporalDenoiseMotion.cameraMovedFactor(
                1f, 0f, 0f, 0f, 0f, -1f,
                0f, 0f, 0f, 0f, 0f, -1f,
                hasPrevious = true
            )
        )
        assertEquals(
            0f,
            TemporalDenoiseMotion.cameraMovedFactor(
                0f, 10f, 0f, 0f, -0.5f, -0.8660254f,
                0f, 10f, 0f, 0f, -0.5f, -0.8660254f,
                hasPrevious = true
            )
        )
    }

    @Test
    fun effectiveHistoryCapLimitsBlendUnderMotion() {
        assertEquals(16, TemporalDenoiseMotion.effectiveHistoryCap(64, cameraMovedFactor = 1f))
        assertEquals(64, TemporalDenoiseMotion.effectiveHistoryCap(64, cameraMovedFactor = 0f))
        assertEquals(3, TemporalDenoiseMotion.effectiveHistoryCap(3, cameraMovedFactor = 1f))
    }

    @Test
    fun tightAabbUsedOnlyWhenCameraMoved() {
        assertTrue(TemporalDenoiseMotion.useTightAabb(cameraMovedFactor = 1f))
        assertFalse(TemporalDenoiseMotion.useTightAabb(cameraMovedFactor = 0f))
    }
}
