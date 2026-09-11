package com.lumina.renderer.denoise

import kotlin.math.sqrt

/**
 * Kotlin-side mirror of camera-motion history capping in svgf_temporal.comp.
 */
object TemporalDenoiseMotion {
    const val POSITION_EPSILON = 0.05f
    const val FORWARD_EPSILON = 0.001f
    const val MOTION_HISTORY_CAP = 8

    fun cameraMovedFactor(
        posX: Float, posY: Float, posZ: Float,
        forwardX: Float, forwardY: Float, forwardZ: Float,
        lastPosX: Float, lastPosY: Float, lastPosZ: Float,
        lastForwardX: Float, lastForwardY: Float, lastForwardZ: Float,
        hasPrevious: Boolean
    ): Float {
        if (!hasPrevious) return 1f
        val posDelta = sqrt(
            (posX - lastPosX) * (posX - lastPosX) +
                (posY - lastPosY) * (posY - lastPosY) +
                (posZ - lastPosZ) * (posZ - lastPosZ)
        )
        val fwdDelta = sqrt(
            (forwardX - lastForwardX) * (forwardX - lastForwardX) +
                (forwardY - lastForwardY) * (forwardY - lastForwardY) +
                (forwardZ - lastForwardZ) * (forwardZ - lastForwardZ)
        )
        return if (posDelta > POSITION_EPSILON || fwdDelta > FORWARD_EPSILON) 1f else 0f
    }

    fun effectiveHistoryCap(historyLen: Int, cameraMovedFactor: Float): Int =
        if (cameraMovedFactor > 0f) minOf(historyLen, MOTION_HISTORY_CAP) else historyLen

    fun useTightAabb(cameraMovedFactor: Float): Boolean = cameraMovedFactor > 0f
}
