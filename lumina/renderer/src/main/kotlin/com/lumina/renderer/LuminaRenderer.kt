package com.lumina.renderer

import com.lumina.renderer.denoise.SVGFDenoiser
import com.lumina.renderer.postfx.PostProcessStack
import com.lumina.renderer.rt.AccelerationStructureManager
import com.lumina.renderer.rt.RayTracingPipeline
import com.lumina.renderer.upscale.UpscaleManager
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
    val upscale: UpscaleManager
) {
    private val log = LoggerFactory.getLogger(LuminaRenderer::class.java)

    var frameCount: Long = 0; private set
    var lastFrameTimeMs: Double = 0.0; private set
    private var lastFrameNanos: Long = 0

    fun init(title: String = "Lumina - OSRS", width: Int = 1280, height: Int = 720) {
        vkContext.init(title, width, height)
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

        // 1. Path trace / rasterize
        rtPipeline.recordCommands(upscale.renderWidth, upscale.renderHeight, (frameCount % 2).toInt())

        // 2. Denoise
        denoiser.denoise(0, 0, 0, 0)

        // 3. Post-processing (volumetrics, bloom, tone mapping)
        postProcess.execute(0, 0, 0)

        // 4. Upscale to display resolution
        upscale.upscale(0, 0, 0, 0, lastFrameTimeMs.toFloat() / 1000f, 0f, 0f)

        // 5. Present
        frameCount++
    }

    fun resize(width: Int, height: Int) {
        vkContext.destroy()
        vkContext.init("Lumina - OSRS", width, height)
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
        vkContext.destroy()
        log.info("Lumina renderer destroyed after {} frames", frameCount)
    }
}
