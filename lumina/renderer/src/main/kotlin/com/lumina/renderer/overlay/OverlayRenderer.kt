package com.lumina.renderer.overlay

import com.lumina.renderer.LuminaRenderer
import com.lumina.renderer.postfx.PostProcessStack
import com.lumina.renderer.rt.RayTracingPipeline
import com.lumina.renderer.upscale.UpscaleManager
import com.lumina.renderer.upscale.UpscaleMode
import com.lumina.renderer.vulkan.VulkanContext
import org.lwjgl.glfw.GLFW.*
import org.slf4j.LoggerFactory
import javax.inject.Inject
import javax.inject.Singleton

/** Bumped on renderer-affecting commits so screenshots prove which build is running. */
const val BUILD_STAMP = "b29-water2"

@Singleton
class OverlayRenderer @Inject constructor(
    private val ctx: VulkanContext,
    private val renderer: LuminaRenderer,
    private val postProcess: PostProcessStack,
    private val upscale: UpscaleManager,
    private val rtPipeline: RayTracingPipeline
) {
    private val log = LoggerFactory.getLogger(OverlayRenderer::class.java)

    var showFps: Boolean = true
    var showDebugInfo: Boolean = false
    var showSettings: Boolean = false
    var debugMode: Boolean = false

    /** Latest camera world tile from --play mirror sync; NaN when unavailable. */
    var cameraWorldTileX: Float = Float.NaN
    var cameraWorldTileY: Float = Float.NaN

    private var fpsHistory = FloatArray(120)
    private var fpsIndex = 0
    private var frameTimeAccum = 0.0
    private var frameCounter = 0
    private var smoothFps = 0

    fun update(frameTimeMs: Double, frameCount: Long) {
        frameTimeAccum += frameTimeMs
        frameCounter++

        if (frameCounter >= 10) {
            smoothFps = if (frameTimeAccum > 0) (10000.0 / frameTimeAccum).toInt() else 0
            frameTimeAccum = 0.0
            frameCounter = 0
        }

        fpsHistory[fpsIndex] = (1000.0 / frameTimeMs.coerceAtLeast(0.01)).toFloat()
        fpsIndex = (fpsIndex + 1) % fpsHistory.size

        if (showFps && frameCount % 60 == 0L) {
            val avgFps = fpsHistory.filter { it > 0 }.let { if (it.isNotEmpty()) it.average() else 0.0 }
            val minFps = fpsHistory.filter { it > 0 }.minOrNull() ?: 0f
            glfwSetWindowTitle(ctx.window, buildTitle(avgFps, minFps))
        }
    }

    private fun buildTitle(avgFps: Double, minFps: Float): String {
        val sb = StringBuilder("Lumina - OSRS [build $BUILD_STAMP]")
        if (showFps) {
            sb.append(" | FPS: $smoothFps (avg: ${avgFps.toInt()}, min: ${minFps.toInt()})")
            sb.append(" | ${ctx.width}x${ctx.height}")
            if (upscale.mode != UpscaleMode.NONE) {
                sb.append(" -> ${upscale.renderWidth}x${upscale.renderHeight} (${upscale.quality})")
            }
        }
        if (!cameraWorldTileX.isNaN() && !cameraWorldTileY.isNaN()) {
            sb.append(" | tile (${cameraWorldTileX.toInt()}, ${cameraWorldTileY.toInt()})")
        }
        if (showDebugInfo) {
            sb.append(" | ${ctx.getDeviceName()}")
            sb.append(" | RT: ${ctx.rtSupported}")
            sb.append(" | Tonemap: ${postProcess.toneMappingMode}")
        }
        if (renderer.rawOutputMode) {
            sb.append(" | RAW")
        }
        return sb.toString()
    }

    fun handleKey(key: Int, action: Int): Boolean {
        if (action != GLFW_PRESS) return false

        return when (key) {
            GLFW_KEY_F1 -> { showFps = !showFps; true }
            GLFW_KEY_F2 -> { showDebugInfo = !showDebugInfo; true }
            GLFW_KEY_F3 -> { showSettings = !showSettings; logSettings(); true }
            GLFW_KEY_F5 -> {
                postProcess.bloomEnabled = !postProcess.bloomEnabled
                log.info("Bloom: {}", postProcess.bloomEnabled); true
            }
            GLFW_KEY_F6 -> {
                postProcess.volumetricFogEnabled = !postProcess.volumetricFogEnabled
                log.info("Volumetric fog: {}", postProcess.volumetricFogEnabled); true
            }
            GLFW_KEY_F7 -> {
                postProcess.toneMappingMode = PostProcessStack.ToneMapMode.entries.let { modes ->
                    modes[(modes.indexOf(postProcess.toneMappingMode) + 1) % modes.size]
                }
                log.info("Tone mapping: {}", postProcess.toneMappingMode); true
            }
            GLFW_KEY_F8 -> {
                upscale.quality = com.lumina.renderer.upscale.UpscaleQuality.entries.let { q ->
                    q[(q.indexOf(upscale.quality) + 1) % q.size]
                }
                log.info("Upscale quality: {} ({}x{} -> {}x{})",
                    upscale.quality, upscale.renderWidth, upscale.renderHeight, ctx.width, ctx.height); true
            }
            GLFW_KEY_F9 -> {
                renderer.setRawOutputMode(!renderer.rawOutputMode)
                log.info("Raw output mode: {}", renderer.rawOutputMode); true
            }
            GLFW_KEY_EQUAL -> {
                postProcess.exposure = (postProcess.exposure * 1.1f).coerceAtMost(10f)
                log.info("Exposure: {}", postProcess.exposure); true
            }
            GLFW_KEY_MINUS -> {
                postProcess.exposure = (postProcess.exposure * 0.9f).coerceAtLeast(0.1f)
                log.info("Exposure: {}", postProcess.exposure); true
            }
            GLFW_KEY_F11 -> {
                debugMode = !debugMode
                rtPipeline.maxBounces = if (debugMode) 0 else 4
                log.info("Debug mode: {} (maxBounces={})", debugMode, rtPipeline.maxBounces); true
            }
            else -> false
        }
    }

    private fun logSettings() {
        log.info("=== Lumina Settings ===")
        log.info("Resolution: {}x{} (render: {}x{})", ctx.width, ctx.height, upscale.renderWidth, upscale.renderHeight)
        log.info("Upscale: {} {} (sharpness: {})", upscale.mode, upscale.quality, upscale.sharpness)
        log.info("Bloom: {} (threshold: {}, intensity: {})", postProcess.bloomEnabled, postProcess.bloomThreshold, postProcess.bloomIntensity)
        log.info("Volumetric fog: {} (density: {})", postProcess.volumetricFogEnabled, postProcess.fogDensity)
        log.info("God rays: {} (intensity: {})", postProcess.godRaysEnabled, postProcess.godRayIntensity)
        log.info("Tone mapping: {} (exposure: {}, gamma: {})", postProcess.toneMappingMode, postProcess.exposure, postProcess.gamma)
        log.info("RT: {} | Device: {}", ctx.rtSupported, ctx.getDeviceName())
        log.info("======================")
    }
}
