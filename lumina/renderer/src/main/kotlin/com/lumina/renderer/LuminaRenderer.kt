package com.lumina.renderer

import com.lumina.renderer.denoise.SVGFDenoiser
import com.lumina.renderer.postfx.PostProcessStack
import com.lumina.renderer.rt.AccelerationStructureManager
import com.lumina.renderer.rt.RayTracingPipeline
import com.lumina.renderer.upscale.UpscaleManager
import com.lumina.renderer.scene.SceneBufferManager
import com.lumina.renderer.vulkan.FrameManager
import com.lumina.renderer.vulkan.RenderTargets
import com.lumina.renderer.vulkan.ShaderCompiler
import com.lumina.renderer.vulkan.VulkanContext
import com.lumina.scene.graph.SceneGraph
import org.lwjgl.system.MemoryStack
import org.lwjgl.vulkan.KHRSwapchain.VK_IMAGE_LAYOUT_PRESENT_SRC_KHR
import org.lwjgl.vulkan.VK13.*
import org.lwjgl.vulkan.VkImageBlit
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
    val renderTargets: RenderTargets,
    val shaderCompiler: ShaderCompiler,
    val sceneBufferManager: SceneBufferManager
) {
    private val log = LoggerFactory.getLogger(LuminaRenderer::class.java)

    var frameCount: Long = 0; private set
    var lastFrameTimeMs: Double = 0.0; private set
    private var lastFrameNanos: Long = 0
    private var descriptorsDirty = true

    fun init(title: String = "Lumina - OSRS", width: Int = 1280, height: Int = 720) {
        vkContext.init(title, width, height)
        shaderCompiler.init()
        frameManager.init()
        upscale.init()

        renderTargets.init(upscale.renderWidth, upscale.renderHeight, width, height)

        accelStructure.queryScratchAlignment()
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

        rtPipeline.updateDescriptors(
            renderTargets, rtPipeline.getCameraBuffer(),
            sceneBufferManager.vertexBuffer,
            sceneBufferManager.indexBuffer,
            sceneBufferManager.materialBuffer,
            sceneBufferManager.instanceInfoBuffer
        )

        val rtOutput = renderTargets.rtOutputColor ?: return
        val tonemapOut = renderTargets.tonemapOutput ?: return

        if (vkContext.rtSupported) {
            denoiser.updateDescriptors()
            val bloomScratchA = renderTargets.bloomScratchA ?: return
            val rtNormalDepth = renderTargets.rtNormalDepth ?: return
            postProcess.updateDescriptors(bloomScratchA, rtNormalDepth, tonemapOut)
        } else {
            postProcess.updateTonemapDescriptors(rtOutput, tonemapOut)
        }
    }

    fun renderFrame() {
        val now = System.nanoTime()
        lastFrameTimeMs = (now - lastFrameNanos) / 1_000_000.0
        lastFrameNanos = now

        if (sceneGraph.dirty) {
            accelStructure.rebuildTLAS()
            sceneGraph.clearDirty()
            descriptorsDirty = true
        }

        updateAllDescriptors()

        val frameCtx = frameManager.beginFrame() ?: return
        val cmdBuf = frameCtx.commandBuffer

        renderTargets.transitionAllToGeneral(cmdBuf)

        if (vkContext.rtSupported) {
            rtPipeline.recordCommands(cmdBuf, renderTargets.renderWidth, renderTargets.renderHeight)
            insertRTToComputeBarrier(cmdBuf)

            denoiser.recordCommands(cmdBuf)
            RenderTargets.insertComputeBarrier(cmdBuf)
            copyDenoiseHistory(cmdBuf)

            postProcess.recordCommands(cmdBuf, renderTargets.renderWidth, renderTargets.renderHeight)
        } else {
            postProcess.recordTonemapOnly(cmdBuf, vkContext.width, vkContext.height)
        }

        copyToSwapchain(cmdBuf, frameCtx.imageIndex)

        frameManager.endFrame(frameCtx)
        frameCount++

        if (frameCount <= 3 || frameCount % 300 == 0L) {
            log.info("Frame {} rendered (RT: {}, render: {}x{}, display: {}x{})",
                frameCount, vkContext.rtSupported,
                renderTargets.renderWidth, renderTargets.renderHeight,
                vkContext.width, vkContext.height)
        }
    }

    private fun copyDenoiseHistory(cmdBuf: org.lwjgl.vulkan.VkCommandBuffer) {
        val output = renderTargets.denoiseOutput ?: return
        val history = renderTargets.denoiseHistory ?: return

        MemoryStack.stackPush().use { stack ->
            val preBarrier = org.lwjgl.vulkan.VkMemoryBarrier.calloc(1, stack)
            preBarrier.get(0)
                .sType(VK_STRUCTURE_TYPE_MEMORY_BARRIER)
                .srcAccessMask(VK_ACCESS_SHADER_WRITE_BIT)
                .dstAccessMask(VK_ACCESS_TRANSFER_READ_BIT)
            vkCmdPipelineBarrier(cmdBuf,
                VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT, VK_PIPELINE_STAGE_TRANSFER_BIT,
                0, preBarrier, null, null)

            val copyRegion = VkImageCopy.calloc(1, stack)
            copyRegion.get(0).srcSubresource()
                .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                .mipLevel(0).baseArrayLayer(0).layerCount(1)
            copyRegion.get(0).srcOffset().set(0, 0, 0)
            copyRegion.get(0).dstSubresource()
                .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                .mipLevel(0).baseArrayLayer(0).layerCount(1)
            copyRegion.get(0).dstOffset().set(0, 0, 0)
            copyRegion.get(0).extent()
                .width(output.width)
                .height(output.height)
                .depth(1)

            vkCmdCopyImage(cmdBuf,
                output.image, VK_IMAGE_LAYOUT_GENERAL,
                history.image, VK_IMAGE_LAYOUT_GENERAL,
                copyRegion)

            val postBarrier = org.lwjgl.vulkan.VkMemoryBarrier.calloc(1, stack)
            postBarrier.get(0)
                .sType(VK_STRUCTURE_TYPE_MEMORY_BARRIER)
                .srcAccessMask(VK_ACCESS_TRANSFER_WRITE_BIT)
                .dstAccessMask(VK_ACCESS_SHADER_READ_BIT)
            vkCmdPipelineBarrier(cmdBuf,
                VK_PIPELINE_STAGE_TRANSFER_BIT, VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT,
                0, postBarrier, null, null)
        }
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
            val barriers = VkImageMemoryBarrier.calloc(2, stack)

            // Transition tonemap output: GENERAL -> TRANSFER_SRC
            barriers.get(0)
                .sType(VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER)
                .oldLayout(VK_IMAGE_LAYOUT_GENERAL)
                .newLayout(VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL)
                .srcAccessMask(VK_ACCESS_SHADER_WRITE_BIT)
                .dstAccessMask(VK_ACCESS_TRANSFER_READ_BIT)
                .srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .image(tonemapImg.image)
            barriers.get(0).subresourceRange()
                .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                .baseMipLevel(0).levelCount(1).baseArrayLayer(0).layerCount(1)

            // Transition swapchain image: UNDEFINED -> TRANSFER_DST
            barriers.get(1)
                .sType(VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER)
                .oldLayout(VK_IMAGE_LAYOUT_UNDEFINED)
                .newLayout(VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL)
                .srcAccessMask(0)
                .dstAccessMask(VK_ACCESS_TRANSFER_WRITE_BIT)
                .srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .image(swapchainImage)
            barriers.get(1).subresourceRange()
                .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                .baseMipLevel(0).levelCount(1).baseArrayLayer(0).layerCount(1)

            vkCmdPipelineBarrier(cmdBuf,
                VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT, VK_PIPELINE_STAGE_TRANSFER_BIT,
                0, null, null, barriers)

            // Blit (handles format conversion + scaling: render res -> display res)
            val blitRegion = VkImageBlit.calloc(1, stack)
            blitRegion.get(0).let { region ->
                region.srcSubresource()
                    .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                    .mipLevel(0).baseArrayLayer(0).layerCount(1)
                region.srcOffsets(0).x(0).y(0).z(0)
                region.srcOffsets(1).x(tonemapImg.width).y(tonemapImg.height).z(1)
                region.dstSubresource()
                    .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                    .mipLevel(0).baseArrayLayer(0).layerCount(1)
                region.dstOffsets(0).x(0).y(0).z(0)
                region.dstOffsets(1).x(vkContext.width).y(vkContext.height).z(1)
            }

            vkCmdBlitImage(cmdBuf,
                tonemapImg.image, VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL,
                swapchainImage, VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
                blitRegion, VK_FILTER_NEAREST)

            // Transition swapchain: TRANSFER_DST -> PRESENT_SRC
            // Transition tonemap: TRANSFER_SRC -> GENERAL
            val postBarriers = VkImageMemoryBarrier.calloc(2, stack)
            postBarriers.get(0)
                .sType(VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER)
                .oldLayout(VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL)
                .newLayout(VK_IMAGE_LAYOUT_PRESENT_SRC_KHR)
                .srcAccessMask(VK_ACCESS_TRANSFER_WRITE_BIT)
                .dstAccessMask(0)
                .srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .image(swapchainImage)
            postBarriers.get(0).subresourceRange()
                .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                .baseMipLevel(0).levelCount(1).baseArrayLayer(0).layerCount(1)

            postBarriers.get(1)
                .sType(VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER)
                .oldLayout(VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL)
                .newLayout(VK_IMAGE_LAYOUT_GENERAL)
                .srcAccessMask(VK_ACCESS_TRANSFER_READ_BIT)
                .dstAccessMask(VK_ACCESS_SHADER_WRITE_BIT)
                .srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                .image(tonemapImg.image)
            postBarriers.get(1).subresourceRange()
                .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                .baseMipLevel(0).levelCount(1).baseArrayLayer(0).layerCount(1)

            vkCmdPipelineBarrier(cmdBuf,
                VK_PIPELINE_STAGE_TRANSFER_BIT,
                VK_PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT or VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT,
                0, null, null, postBarriers)
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
        shaderCompiler.destroy()
        renderTargets.destroy()
        frameManager.destroy()
        vkContext.destroy()
        log.info("Lumina renderer destroyed after {} frames", frameCount)
    }

    companion object {
        private const val RT_SHADER_STAGE = 0x00200000 // VK_PIPELINE_STAGE_RAY_TRACING_SHADER_BIT_KHR
    }
}
