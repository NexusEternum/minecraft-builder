package com.lumina.renderer.vulkan

import org.lwjgl.system.MemoryStack
import org.lwjgl.vulkan.VK13.*
import org.lwjgl.vulkan.VkImageMemoryBarrier
import org.lwjgl.vulkan.VkCommandBuffer
import org.slf4j.LoggerFactory
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class RenderTargets @Inject constructor(
    private val ctx: VulkanContext
) {
    private val log = LoggerFactory.getLogger(RenderTargets::class.java)

    var rtOutputColor: VulkanImage? = null; private set
    var rtNormalDepth: VulkanImage? = null; private set
    var rtMotionVectors: VulkanImage? = null; private set

    var denoiseOutput: VulkanImage? = null; private set
    var denoiseHistory: VulkanImage? = null; private set
    var denoiseMoments: VulkanImage? = null; private set

    var bloomScratchA: VulkanImage? = null; private set
    var bloomScratchB: VulkanImage? = null; private set

    var postfxOutput: VulkanImage? = null; private set

    var upscaleOutput: VulkanImage? = null; private set
    var upscaleHistory: VulkanImage? = null; private set

    var tonemapOutput: VulkanImage? = null; private set

    var renderWidth: Int = 0; private set
    var renderHeight: Int = 0; private set
    var displayWidth: Int = 0; private set
    var displayHeight: Int = 0; private set
    private var initialTransitionDone = false

    fun init(renderW: Int, renderH: Int, displayW: Int, displayH: Int) {
        renderWidth = renderW
        renderHeight = renderH
        displayWidth = displayW
        displayHeight = displayH

        val storageUsage = VK_IMAGE_USAGE_STORAGE_BIT or VK_IMAGE_USAGE_SAMPLED_BIT or VK_IMAGE_USAGE_TRANSFER_SRC_BIT
        val deviceLocal = VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT

        rtOutputColor = VulkanMemory.createImage(ctx, renderW, renderH, VK_FORMAT_R32G32B32A32_SFLOAT, storageUsage, deviceLocal)
        rtNormalDepth = VulkanMemory.createImage(ctx, renderW, renderH, VK_FORMAT_R32G32B32A32_SFLOAT, storageUsage, deviceLocal)
        rtMotionVectors = VulkanMemory.createImage(ctx, renderW, renderH, VK_FORMAT_R16G16_SFLOAT, storageUsage, deviceLocal)

        denoiseOutput = VulkanMemory.createImage(ctx, renderW, renderH, VK_FORMAT_R32G32B32A32_SFLOAT, storageUsage, deviceLocal)
        denoiseHistory = VulkanMemory.createImage(ctx, renderW, renderH, VK_FORMAT_R32G32B32A32_SFLOAT, storageUsage, deviceLocal)
        denoiseMoments = VulkanMemory.createImage(ctx, renderW, renderH, VK_FORMAT_R32G32_SFLOAT, storageUsage, deviceLocal)

        bloomScratchA = VulkanMemory.createImage(ctx, renderW, renderH, VK_FORMAT_R32G32B32A32_SFLOAT, storageUsage, deviceLocal)
        bloomScratchB = VulkanMemory.createImage(ctx, renderW, renderH, VK_FORMAT_R32G32B32A32_SFLOAT, storageUsage, deviceLocal)
        postfxOutput = VulkanMemory.createImage(ctx, renderW, renderH, VK_FORMAT_R16G16B16A16_SFLOAT, storageUsage, deviceLocal)

        upscaleOutput = VulkanMemory.createImage(ctx, displayW, displayH, VK_FORMAT_R32G32B32A32_SFLOAT, storageUsage, deviceLocal)
        upscaleHistory = VulkanMemory.createImage(ctx, displayW, displayH, VK_FORMAT_R32G32B32A32_SFLOAT, storageUsage, deviceLocal)

        tonemapOutput = VulkanMemory.createImage(ctx, renderW, renderH, VK_FORMAT_R8G8B8A8_UNORM,
            storageUsage or VK_IMAGE_USAGE_TRANSFER_SRC_BIT, deviceLocal)

        log.info("Render targets created: render={}x{}, display={}x{}", renderW, renderH, displayW, displayH)
    }

    fun transitionAllToGeneral(cmdBuf: VkCommandBuffer) {
        if (initialTransitionDone) return
        initialTransitionDone = true
        val allImages = listOfNotNull(
            rtOutputColor, rtNormalDepth, rtMotionVectors,
            denoiseOutput, denoiseHistory, denoiseMoments,
            bloomScratchA, bloomScratchB, postfxOutput,
            upscaleOutput, upscaleHistory, tonemapOutput
        )
        transitionImages(cmdBuf, allImages, VK_IMAGE_LAYOUT_UNDEFINED, VK_IMAGE_LAYOUT_GENERAL,
            VK_ACCESS_NONE, VK_ACCESS_SHADER_WRITE_BIT or VK_ACCESS_SHADER_READ_BIT,
            VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT,
            VK_PIPELINE_STAGE_RAY_TRACING_SHADER_BIT_KHR or VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT)
    }

    fun resize(renderW: Int, renderH: Int, displayW: Int, displayH: Int) {
        destroy()
        init(renderW, renderH, displayW, displayH)
    }

    fun destroy() {
        val images = listOfNotNull(
            rtOutputColor, rtNormalDepth, rtMotionVectors,
            denoiseOutput, denoiseHistory, denoiseMoments,
            bloomScratchA, bloomScratchB, postfxOutput,
            upscaleOutput, upscaleHistory, tonemapOutput
        )
        images.forEach { VulkanMemory.destroyImage(ctx, it) }
        rtOutputColor = null; rtNormalDepth = null; rtMotionVectors = null
        denoiseOutput = null; denoiseHistory = null; denoiseMoments = null
        bloomScratchA = null; bloomScratchB = null; postfxOutput = null
        upscaleOutput = null; upscaleHistory = null; tonemapOutput = null
        initialTransitionDone = false
        log.debug("Render targets destroyed")
    }

    companion object {
        private const val VK_PIPELINE_STAGE_RAY_TRACING_SHADER_BIT_KHR = 0x00200000

        fun transitionImages(
            cmdBuf: VkCommandBuffer, images: List<VulkanImage>,
            oldLayout: Int, newLayout: Int,
            srcAccess: Int, dstAccess: Int,
            srcStage: Int, dstStage: Int
        ) {
            if (images.isEmpty()) return
            MemoryStack.stackPush().use { stack ->
                val barriers = VkImageMemoryBarrier.calloc(images.size, stack)
                for ((i, img) in images.withIndex()) {
                    barriers.get(i)
                        .sType(VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER)
                        .oldLayout(oldLayout)
                        .newLayout(newLayout)
                        .srcAccessMask(srcAccess)
                        .dstAccessMask(dstAccess)
                        .srcQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                        .dstQueueFamilyIndex(VK_QUEUE_FAMILY_IGNORED)
                        .image(img.image)
                    barriers.get(i).subresourceRange()
                        .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                        .baseMipLevel(0).levelCount(1)
                        .baseArrayLayer(0).layerCount(1)
                }
                vkCmdPipelineBarrier(cmdBuf, srcStage, dstStage, 0, null, null, barriers)
            }
        }

        fun insertComputeBarrier(cmdBuf: VkCommandBuffer) {
            MemoryStack.stackPush().use { stack ->
                val memBarrier = org.lwjgl.vulkan.VkMemoryBarrier.calloc(1, stack)
                memBarrier.get(0)
                    .sType(VK_STRUCTURE_TYPE_MEMORY_BARRIER)
                    .srcAccessMask(VK_ACCESS_SHADER_WRITE_BIT)
                    .dstAccessMask(VK_ACCESS_SHADER_READ_BIT)
                vkCmdPipelineBarrier(cmdBuf,
                    VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT, VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT,
                    0, memBarrier, null, null)
            }
        }
    }
}
