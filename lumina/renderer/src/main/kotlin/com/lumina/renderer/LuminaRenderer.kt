package com.lumina.renderer

import com.lumina.renderer.denoise.SVGFDenoiser
import com.lumina.renderer.postfx.PostProcessStack
import com.lumina.renderer.rt.AccelerationStructureManager
import com.lumina.renderer.rt.RayTracingPipeline
import com.lumina.renderer.upscale.UpscaleManager
import com.lumina.renderer.upscale.UpscaleMode
import com.lumina.renderer.vulkan.FrameManager
import com.lumina.renderer.vulkan.RenderTargets
import com.lumina.renderer.vulkan.VulkanContext
import com.lumina.scene.graph.SceneGraph
import org.lwjgl.system.MemoryStack
import org.lwjgl.vulkan.KHRSwapchain.VK_IMAGE_LAYOUT_PRESENT_SRC_KHR
import org.lwjgl.vulkan.VK13.*
import org.lwjgl.vulkan.VkImageCopy
import org.lwjgl.vulkan.VkImageMemoryBarrier
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
    val frameManager: FrameManager,
    val renderTargets: RenderTargets
) {
    private val log = LoggerFactory.getLogger(LuminaRenderer::class.java)

    var frameCount: Long = 0; private set
    var lastFrameTimeMs: Double = 0.0; private set
    private var lastFrameNanos: Long = 0
    private var descriptorsDirty = true

    fun init(title: String = "Lumina - OSRS", width: Int = 1280, height: Int = 720) {
        vkContext.init(title, width, height)
        frameManager.init()
        upscale.init()

        renderTargets.init(upscale.renderWidth, upscale.renderHeight, width, height)

        rtPipeline.init()
        denoiser.init(upscale.renderWidth, upscale.renderHeight)
        postProcess.init(upscale.renderWidth, upscale.renderHeight)

        descriptorsDirty = true
        lastFrameNanos = System.nanoTime()
        log.info("Lumina renderer initialized ({}x{}, render={}x{}, RT: {})",
            width, height, upscale.renderWidth, upscale.renderHeight, vkContext.rtSupported)
    }

    private fun updateAllDescriptors() {
        if (!descriptorsDirty) return
        descriptorsDirty = false

        rtPipeline.updateDescriptors(renderTargets, rtPipeline.getCameraBuffer())

        denoiser.updateDescriptors()

        val denoiseOut = renderTargets.denoiseOutput ?: return
        val normalDepth = renderTargets.rtNormalDepth ?: return
        val tonemapOut = renderTargets.tonemapOutput ?: return

        if (upscale.mode == UpscaleMode.NONE) {
            postProcess.updateDescriptors(denoiseOut, normalDepth, tonemapOut)
        } else {
            postProcess.updateDescriptors(renderTargets.upscaleOutput ?: denoiseOut, normalDepth, tonemapOut)
        }

        upscale.updateDescriptors()
    }

    fun renderFrame() {
        val now = System.nanoTime()
        lastFrameTimeMs = (now - lastFrameNanos) / 1_000_000.0
        lastFrameNanos = now
        val deltaTime = (lastFrameTimeMs / 1000.0).toFloat()

        if (sceneGraph.dirty) {
            accelStructure.rebuildTLAS()
            sceneGraph.clearDirty()
            descriptorsDirty = true
        }

        updateAllDescriptors()

        upscale.updateJitter()

        val frameCtx = frameManager.beginFrame() ?: return
        val cmdBuf = frameCtx.commandBuffer

        // Transition all render targets to GENERAL on first use
        renderTargets.transitionAllToGeneral(cmdBuf)

        // 1. Path trace via hardware RT
        rtPipeline.recordCommands(cmdBuf, upscale.renderWidth, upscale.renderHeight)

        // Barrier: RT writes -> compute reads
        insertRTToComputeBarrier(cmdBuf)

        // 2. Denoise (SVGF temporal + A-Trous)
        denoiser.recordCommands(cmdBuf)

        RenderTargets.insertComputeBarrier(cmdBuf)

        // 3. Upscale (FSR 2.0)
        if (upscale.mode != UpscaleMode.NONE) {
            upscale.recordCommands(cmdBuf, deltaTime)
            RenderTargets.insertComputeBarrier(cmdBuf)
        }

        // 4. Post-processing (bloom, volumetric fog, tone mapping)
        postProcess.recordCommands(cmdBuf, vkContext.width, vkContext.height)

        // 5. Copy tonemapped result to swapchain image
        copyToSwapchain(cmdBuf, frameCtx.imageIndex)

        frameManager.endFrame(frameCtx)
        frameCount++
    }

    private fun insertRTToComputeBarrier(cmdBuf: org.lwjgl.vulkan.VkCommandBuffer) {
        MemoryStack.stackPush().use { stack ->
            val memBarrier = org.lwjgl.vulkan.VkMemoryBarrier.calloc(1, stack)
            memBarrier.get(0)
                .sType(VK_STRUCTURE_TYPE_MEMORY_BARRIER)
                .srcAccessMask(VK_ACCESS_SHADER_WRITE_BIT)
                .dstAccessMask(VK_ACCESS_SHADER_READ_BIT)
            vkCmdPipelineBarrier(cmdBuf,
                RT_SHADER_STAGE, VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT,
                0, memBarrier, null, null)
        }
    }

    private fun copyToSwapchain(cmdBuf: org.lwjgl.vulkan.VkCommandBuffer, imageIndex: Int) {
        val tonemapImg = renderTargets.tonemapOutput ?: return
        val swapchainImage = vkContext.swapchainImages.getOrNull(imageIndex) ?: return

        MemoryStack.stackPush().use { stack ->
            // Transition tonemap output: GENERAL -> TRANSFER_SRC
            val srcBarrier = VkImageMemoryBarrier.calloc(1, stack)
            srcBarrier.get(0)
                .sType(VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER)
                .oldLayout(VK_IMAGE_LAYOUT_GENERAL)
                .newLayout(VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL)
                .srcAccessMask(VK_ACCESS_SHADER_WRITE_BIT)
                .dstAccessMask(VK_ACCESS_TRANSFER_READ_BIT)
                .srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .image(tonemapImg.image)
            srcBarrier.get(0).subresourceRange()
                .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                .baseMipLevel(0).levelCount(1).baseArrayLayer(0).layerCount(1)

            // Transition swapchain image: UNDEFINED -> TRANSFER_DST
            val dstBarrier = VkImageMemoryBarrier.calloc(1, stack)
            dstBarrier.get(0)
                .sType(VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER)
                .oldLayout(VK_IMAGE_LAYOUT_UNDEFINED)
                .newLayout(VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL)
                .srcAccessMask(0)
                .dstAccessMask(VK_ACCESS_TRANSFER_WRITE_BIT)
                .srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .image(swapchainImage)
            dstBarrier.get(0).subresourceRange()
                .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                .baseMipLevel(0).levelCount(1).baseArrayLayer(0).layerCount(1)

            val combined = VkImageMemoryBarrier.calloc(2, stack)
            combined.put(0, srcBarrier.get(0))
            combined.put(1, dstBarrier.get(0))
            vkCmdPipelineBarrier(cmdBuf,
                VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT, VK_PIPELINE_STAGE_TRANSFER_BIT,
                0, null, null, combined)

            // Copy (using vkCmdCopyImage since both are same dimensions)
            val copyRegion = VkImageCopy.calloc(1, stack)
            copyRegion.get(0).let { region ->
                region.srcSubresource()
                    .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                    .mipLevel(0).baseArrayLayer(0).layerCount(1)
                region.dstSubresource()
                    .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                    .mipLevel(0).baseArrayLayer(0).layerCount(1)
                region.extent().width(vkContext.width).height(vkContext.height).depth(1)
            }

            vkCmdCopyImage(cmdBuf,
                tonemapImg.image, VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,
                swapchainImage, VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
                copyRegion)

            // Transition swapchain image: TRANSFER_DST -> PRESENT_SRC
            val presentBarrier = VkImageMemoryBarrier.calloc(1, stack)
            presentBarrier.get(0)
                .sType(VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER)
                .oldLayout(VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL)
                .newLayout(VK_IMAGE_LAYOUT_PRESENT_SRC_KHR)
                .srcAccessMask(VK_ACCESS_TRANSFER_WRITE_BIT)
                .dstAccessMask(0)
                .srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .image(swapchainImage)
            presentBarrier.get(0).subresourceRange()
                .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                .baseMipLevel(0).levelCount(1).baseArrayLayer(0).layerCount(1)

            vkCmdPipelineBarrier(cmdBuf,
                VK_PIPELINE_STAGE_TRANSFER_BIT, VK_PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT,
                0, null, null, presentBarrier)

            // Transition tonemap output back to GENERAL
            val backBarrier = VkImageMemoryBarrier.calloc(1, stack)
            backBarrier.get(0)
                .sType(VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER)
                .oldLayout(VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL)
                .newLayout(VK_IMAGE_LAYOUT_GENERAL)
                .srcAccessMask(VK_ACCESS_TRANSFER_READ_BIT)
                .dstAccessMask(VK_ACCESS_SHADER_WRITE_BIT)
                .srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .image(tonemapImg.image)
            backBarrier.get(0).subresourceRange()
                .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                .baseMipLevel(0).levelCount(1).baseArrayLayer(0).layerCount(1)

            vkCmdPipelineBarrier(cmdBuf,
                VK_PIPELINE_STAGE_TRANSFER_BIT, VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT,
                0, null, null, backBarrier)
        }
    }

    fun resize(width: Int, height: Int) {
        vkContext.device?.let { vkDeviceWaitIdle(it) }

        renderTargets.destroy()
        frameManager.destroy()
        vkContext.destroy()
        vkContext.init("Lumina - OSRS", width, height)
        frameManager.init()
        renderTargets.init(upscale.renderWidth, upscale.renderHeight, width, height)
        denoiser.resize(upscale.renderWidth, upscale.renderHeight)
        postProcess.resize(upscale.renderWidth, upscale.renderHeight)
        descriptorsDirty = true
    }

    val fps: Int get() = if (lastFrameTimeMs > 0) (1000.0 / lastFrameTimeMs).toInt() else 0

    fun destroy() {
        vkContext.device?.let { vkDeviceWaitIdle(it) }
        upscale.destroy()
        postProcess.destroy()
        denoiser.destroy()
        rtPipeline.destroy()
        accelStructure.destroy()
        renderTargets.destroy()
        frameManager.destroy()
        vkContext.destroy()
        log.info("Lumina renderer destroyed after {} frames", frameCount)
    }

    companion object {
        private const val RT_SHADER_STAGE = 0x00200000 // VK_PIPELINE_STAGE_RAY_TRACING_SHADER_BIT_KHR
    }
}
