package com.lumina.renderer.camera

import com.lumina.renderer.rt.RayTracingPipeline
import org.lwjgl.glfw.GLFW.*
import org.slf4j.LoggerFactory
import javax.inject.Inject
import javax.inject.Singleton
import kotlin.math.cos
import kotlin.math.sin

@Singleton
class CameraController @Inject constructor(
    private val rtPipeline: RayTracingPipeline
) {
    private val log = LoggerFactory.getLogger(CameraController::class.java)

    var x: Float = 0f
    var y: Float = 120f
    var z: Float = 0f
    var pitch: Float = -0.3f
    var yaw: Float = 0f
    var fov: Float = 70f
    var nearPlane: Float = 0.1f
    var farPlane: Float = 2000f

    var moveSpeed: Float = 50f
    var lookSpeed: Float = 0.003f

    private var lastMouseX: Double = 0.0
    private var lastMouseY: Double = 0.0
    private var firstMouse: Boolean = true
    private var mouseCaptured: Boolean = false

    private var frameIndex = 0L

    fun update(window: Long, deltaTime: Float, jitterX: Float = 0f, jitterY: Float = 0f) {
        handleKeyboard(window, deltaTime)
        rtPipeline.updateCamera(x, y, z, pitch, yaw, fov, nearPlane, farPlane, jitterX, jitterY)
        if (frameIndex < 3) {
            log.info("Camera frame {}: pos=({}, {}, {}), pitch={}, yaw={}, fov={}",
                frameIndex, x, y, z, pitch, yaw, fov)
        }
        frameIndex++
    }

    private fun handleKeyboard(window: Long, dt: Float) {
        val speed = moveSpeed * dt
        val fwdX = -sin(yaw.toDouble()).toFloat()
        val fwdZ = -cos(yaw.toDouble()).toFloat()
        val rightX = cos(yaw.toDouble()).toFloat()
        val rightZ = -sin(yaw.toDouble()).toFloat()

        if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS) { x += fwdX * speed; z += fwdZ * speed }
        if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS) { x -= fwdX * speed; z -= fwdZ * speed }
        if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS) { x -= rightX * speed; z -= rightZ * speed }
        if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS) { x += rightX * speed; z += rightZ * speed }
        if (glfwGetKey(window, GLFW_KEY_SPACE) == GLFW_PRESS) { y += speed }
        if (glfwGetKey(window, GLFW_KEY_LEFT_SHIFT) == GLFW_PRESS) { y -= speed }
    }

    fun handleMouseMove(xpos: Double, ypos: Double) {
        if (!mouseCaptured) return
        if (firstMouse) {
            lastMouseX = xpos; lastMouseY = ypos; firstMouse = false; return
        }
        val dx = (xpos - lastMouseX) * lookSpeed
        val dy = (ypos - lastMouseY) * lookSpeed
        lastMouseX = xpos; lastMouseY = ypos

        yaw += dx.toFloat()
        pitch = (pitch - dy.toFloat()).coerceIn(-1.5f, 1.5f)
    }

    fun toggleMouseCapture(window: Long) {
        mouseCaptured = !mouseCaptured
        firstMouse = true
        glfwSetInputMode(window, GLFW_CURSOR,
            if (mouseCaptured) GLFW_CURSOR_DISABLED else GLFW_CURSOR_NORMAL)
    }

    fun setPosition(px: Float, py: Float, pz: Float) { x = px; y = py; z = pz }
    fun setRotation(p: Float, y: Float) { pitch = p; yaw = y }
}
