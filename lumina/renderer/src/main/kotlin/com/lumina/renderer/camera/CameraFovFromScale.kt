package com.lumina.renderer.camera

import kotlin.math.atan

/**
 * Maps RuneLite [net.runelite.api.Client.getScale] zoom to a vertical FOV matching the game projection.
 *
 * Perspective projects with `screenY = canvasHeight/2 + y * scale / z`, so the half-angle satisfies
 * `tan(fov/2) = canvasHeight / (2 * scale)`.
 */
object CameraFovFromScale {
    const val MIN_FOV_DEGREES = 20f
    const val MAX_FOV_DEGREES = 90f
    const val DEFAULT_FOV_DEGREES = 70f

    fun verticalFovDegrees(canvasHeight: Int, scale: Int): Float {
        if (canvasHeight <= 0 || scale <= 0) return DEFAULT_FOV_DEGREES
        val halfAngle = atan(canvasHeight.toDouble() / (2.0 * scale.toDouble()))
        val degrees = Math.toDegrees(2.0 * halfAngle).toFloat()
        return degrees.coerceIn(MIN_FOV_DEGREES, MAX_FOV_DEGREES)
    }
}
