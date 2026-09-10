package com.lumina.renderer.vulkan

import org.lwjgl.system.MemoryStack
import org.lwjgl.vulkan.*
import org.lwjgl.vulkan.KHRSwapchain.*
import org.lwjgl.vulkan.VK13.*
import org.slf4j.LoggerFactory
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class FrameManager @Inject constructor(
    private val ctx: VulkanContext
) {
    private val log = LoggerFactory.getLogger(FrameManager::class.java)

    companion object {
        const val MAX_FRAMES_IN_FLIGHT = 2
    }

    lateinit var commandBuffers: List<VkCommandBuffer>; private set
    private var imageAvailableSemaphores = LongArray(MAX_FRAMES_IN_FLIGHT)
    private var renderFinishedSemaphores = LongArray(MAX_FRAMES_IN_FLIGHT)
    private var inFlightFences = LongArray(MAX_FRAMES_IN_FLIGHT)
    private var currentFrame = 0

    fun init() {
        val dev = ctx.device!!
        createCommandBuffers()
        createSyncObjects()
        log.info("Frame manager initialized ({} frames in flight)", MAX_FRAMES_IN_FLIGHT)
    }

    private fun createCommandBuffers() {
        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            val allocInfo = VkCommandBufferAllocateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO)
                .commandPool(ctx.commandPool)
                .level(VK_COMMAND_BUFFER_LEVEL_PRIMARY)
                .commandBufferCount(MAX_FRAMES_IN_FLIGHT)

            val pBuffers = stack.mallocPointer(MAX_FRAMES_IN_FLIGHT)
            check(vkAllocateCommandBuffers(dev, allocInfo, pBuffers) == VK_SUCCESS)

            commandBuffers = (0 until MAX_FRAMES_IN_FLIGHT).map {
                VkCommandBuffer(pBuffers.get(it), dev)
            }
        }
    }

    private fun createSyncObjects() {
        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            val semInfo = VkSemaphoreCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO)
            val fenceInfo = VkFenceCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_FENCE_CREATE_INFO)
                .flags(VK_FENCE_CREATE_SIGNALED_BIT)

            val pSem = stack.mallocLong(1)
            val pFence = stack.mallocLong(1)

            for (i in 0 until MAX_FRAMES_IN_FLIGHT) {
                check(vkCreateSemaphore(dev, semInfo, null, pSem) == VK_SUCCESS)
                imageAvailableSemaphores[i] = pSem.get(0)

                check(vkCreateSemaphore(dev, semInfo, null, pSem) == VK_SUCCESS)
                renderFinishedSemaphores[i] = pSem.get(0)

                check(vkCreateFence(dev, fenceInfo, null, pFence) == VK_SUCCESS)
                inFlightFences[i] = pFence.get(0)
            }
        }
    }

    fun beginFrame(): FrameContext? {
        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            vkWaitForFences(dev, inFlightFences[currentFrame], true, Long.MAX_VALUE)

            val pImageIndex = stack.mallocInt(1)
            val result = vkAcquireNextImageKHR(
                dev, ctx.swapchain, Long.MAX_VALUE,
                imageAvailableSemaphores[currentFrame], 0L, pImageIndex
            )

            if (result == VK_SUBOPTIMAL_KHR || result == VK_ERROR_OUT_OF_DATE_KHR) {
                return null // swapchain out of date
            }

            vkResetFences(dev, inFlightFences[currentFrame])

            val cmdBuf = commandBuffers[currentFrame]
            vkResetCommandBuffer(cmdBuf, 0)

            val beginInfo = VkCommandBufferBeginInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO)
                .flags(VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT)

            check(vkBeginCommandBuffer(cmdBuf, beginInfo) == VK_SUCCESS)

            return FrameContext(
                commandBuffer = cmdBuf,
                imageIndex = pImageIndex.get(0),
                frameIndex = currentFrame
            )
        }
    }

    fun endFrame(frameCtx: FrameContext) {
        val dev = ctx.device!!
        val cmdBuf = frameCtx.commandBuffer

        check(vkEndCommandBuffer(cmdBuf) == VK_SUCCESS)

        MemoryStack.stackPush().use { stack ->
            val submitInfo = VkSubmitInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_SUBMIT_INFO)
                .waitSemaphoreCount(1)
                .pWaitSemaphores(stack.longs(imageAvailableSemaphores[currentFrame]))
                .pWaitDstStageMask(stack.ints(VK_PIPELINE_STAGE_ALL_COMMANDS_BIT))
                .pCommandBuffers(stack.pointers(cmdBuf))
                .pSignalSemaphores(stack.longs(renderFinishedSemaphores[currentFrame]))

            check(vkQueueSubmit(ctx.graphicsQueue!!, submitInfo, inFlightFences[currentFrame]) == VK_SUCCESS)

            val presentInfo = VkPresentInfoKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_PRESENT_INFO_KHR)
                .pWaitSemaphores(stack.longs(renderFinishedSemaphores[currentFrame]))
                .swapchainCount(1)
                .pSwapchains(stack.longs(ctx.swapchain))
                .pImageIndices(stack.ints(frameCtx.imageIndex))

            vkQueuePresentKHR(ctx.presentQueue!!, presentInfo)
        }

        currentFrame = (currentFrame + 1) % MAX_FRAMES_IN_FLIGHT
    }

    fun destroy() {
        val dev = ctx.device ?: return
        vkDeviceWaitIdle(dev)
        for (i in 0 until MAX_FRAMES_IN_FLIGHT) {
            vkDestroySemaphore(dev, imageAvailableSemaphores[i], null)
            vkDestroySemaphore(dev, renderFinishedSemaphores[i], null)
            vkDestroyFence(dev, inFlightFences[i], null)
        }
        log.info("Frame manager destroyed")
    }
}

data class FrameContext(
    val commandBuffer: VkCommandBuffer,
    val imageIndex: Int,
    val frameIndex: Int
)
