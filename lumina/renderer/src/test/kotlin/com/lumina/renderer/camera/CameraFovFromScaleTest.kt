package com.lumina.renderer.camera

import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test
import kotlin.math.atan

class CameraFovFromScaleTest {
    @Test
    fun verticalFovMatchesPerspectiveFormula() {
        val canvasHeight = 503
        val scale = 512
        val expected = Math.toDegrees(2.0 * atan(canvasHeight.toDouble() / (2.0 * scale.toDouble()))).toFloat()
        assertEquals(expected, CameraFovFromScale.verticalFovDegrees(canvasHeight, scale), 0.01f)
    }

    @Test
    fun zoomedInHasSmallerFovThanZoomedOut() {
        val canvasHeight = 503
        val zoomedIn = CameraFovFromScale.verticalFovDegrees(canvasHeight, scale = 800)
        val zoomedOut = CameraFovFromScale.verticalFovDegrees(canvasHeight, scale = 300)
        assertTrue(zoomedIn < zoomedOut)
    }

    @Test
    fun fovClampedToSaneRange() {
        assertEquals(CameraFovFromScale.MAX_FOV_DEGREES, CameraFovFromScale.verticalFovDegrees(2000, 100))
        assertEquals(CameraFovFromScale.MIN_FOV_DEGREES, CameraFovFromScale.verticalFovDegrees(100, 2000))
    }

    @Test
    fun invalidInputsReturnDefault() {
        assertEquals(CameraFovFromScale.DEFAULT_FOV_DEGREES, CameraFovFromScale.verticalFovDegrees(0, 512))
        assertEquals(CameraFovFromScale.DEFAULT_FOV_DEGREES, CameraFovFromScale.verticalFovDegrees(503, 0))
    }
}
