package com.lumina.renderer

import com.lumina.renderer.denoise.SVGFDenoiser
import com.lumina.renderer.postfx.PostProcessStack
import com.lumina.renderer.rt.AccelerationStructureManager
import com.lumina.renderer.rt.RayTracingPipeline
import com.lumina.renderer.upscale.UpscaleManager
import com.lumina.renderer.vulkan.FrameManager
import com.lumina.renderer.vulkan.VulkanContext
import com.lumina.scene.graph.SceneGraph
import org.slf4j.LoggerFactory
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class LuminaRenderer @Inject constructor(
    val vkContext: VulkanContext,
    val sceneGraph: SceneGraph,
    val accelStructure: AccelerationStructureManager,
    val rtPipeline: RayTracingPipeline,
    val denoiser: SVGFDenoiser,
    val postProcess: PostProcessStack,
    val upscale: UpscaleManager,
    val frameManager: FrameManager
) {
    private val log = LoggerFactory.getLogger(LuminaRenderer::class.java)

    var frameCount: Long = 0; private set
    var lastFrameTimeMs: Double = 0.0; private set
    private var lastFrameNanos: Long = 0

    fun init(title: String = "Lumina - OSRS", width: Int = 1280, height: Int = 720) {
        vkContext.init(title, width, height)
        frameManager.init()
        upscale.init()
        rtPipeline.init()
        denoiser.init(upscale.renderWidth, upscale.renderHeight)
        postProcess.init(upscale.renderWidth, upscale.renderHeight)
        lastFrameNanos = System.nanoTime()
        log.info("Lumina renderer initialized ({}x{}, RT: {})", width, height, vkContext.rtSupported)
    }

    fun renderFrame() {
        val now = System.nanoTime()
        lastFrameTimeMs = (now - lastFrameNanos) / 1_000_000.0
        lastFrameNanos = now

        if (sceneGraph.dirty) {
            accelStructure.rebuildTLAS()
            sceneGraph.clearDirty()
        }

        val frameCtx = frameManager.beginFrame() ?: return
        val cmdBuf = frameCtx.commandBuffer

        // 1. Path trace via hardware RT
        rtPipeline.recordCommands(cmdBuf, upscale.renderWidth, upscale.renderHeight)

        // 2. Denoise (dispatched on same command buffer in future)
        // 3. Post-processing
        // 4. Upscale

        frameManager.endFrame(frameCtx)
        frameCount++
    }

    fun resize(width: Int, height: Int) {
        frameManager.destroy()
        vkContext.destroy()
        vkContext.init("Lumina - OSRS", width, height)
        frameManager.init()
        denoiser.resize(upscale.renderWidth, upscale.renderHeight)
        postProcess.resize(upscale.renderWidth, upscale.renderHeight)
    }

    val fps: Int get() = if (lastFrameTimeMs > 0) (1000.0 / lastFrameTimeMs).toInt() else 0

    fun destroy() {
        upscale.destroy()
        postProcess.destroy()
        denoiser.destroy()
        rtPipeline.destroy()
        accelStructure.destroy()
        frameManager.destroy()
        vkContext.destroy()
        log.info("Lumina renderer destroyed after {} frames", frameCount)
    }
}
