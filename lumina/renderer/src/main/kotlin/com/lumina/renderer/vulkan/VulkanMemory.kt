package com.lumina.renderer.vulkan

import org.lwjgl.system.MemoryStack
import org.lwjgl.vulkan.*
import org.lwjgl.vulkan.VK13.*
import org.slf4j.LoggerFactory
import java.nio.ByteBuffer

class VulkanBuffer(
    val buffer: Long,
    val memory: Long,
    val size: Long
)

class VulkanImage(
    val image: Long,
    val memory: Long,
    val view: Long,
    val format: Int,
    val width: Int,
    val height: Int
)

object VulkanMemory {
    private val log = LoggerFactory.getLogger(VulkanMemory::class.java)

    fun createBuffer(
        ctx: VulkanContext, size: Long, usage: Int, memoryProperties: Int
    ): VulkanBuffer {
        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            val bufferInfo = VkBufferCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO)
                .size(size)
                .usage(usage)
                .sharingMode(VK_SHARING_MODE_EXCLUSIVE)

            val pBuffer = stack.mallocLong(1)
            check(vkCreateBuffer(dev, bufferInfo, null, pBuffer) == VK_SUCCESS)
            val buffer = pBuffer.get(0)

            val memReqs = VkMemoryRequirements.calloc(stack)
            vkGetBufferMemoryRequirements(dev, buffer, memReqs)

            val allocInfo = VkMemoryAllocateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO)
                .allocationSize(memReqs.size())
                .memoryTypeIndex(findMemoryType(ctx, memReqs.memoryTypeBits(), memoryProperties))

            val pMemory = stack.mallocLong(1)
            check(vkAllocateMemory(dev, allocInfo, null, pMemory) == VK_SUCCESS)
            val memory = pMemory.get(0)

            vkBindBufferMemory(dev, buffer, memory, 0)
            return VulkanBuffer(buffer, memory, size)
        }
    }

    fun createImage(
        ctx: VulkanContext, width: Int, height: Int, format: Int,
        usage: Int, memoryProperties: Int
    ): VulkanImage {
        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            val imageInfo = VkImageCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_IMAGE_CREATE_INFO)
                .imageType(VK_IMAGE_TYPE_2D)
                .format(format)
                .mipLevels(1).arrayLayers(1)
                .samples(VK_SAMPLE_COUNT_1_BIT)
                .tiling(VK_IMAGE_TILING_OPTIMAL)
                .usage(usage)
                .sharingMode(VK_SHARING_MODE_EXCLUSIVE)
                .initialLayout(VK_IMAGE_LAYOUT_UNDEFINED)
            imageInfo.extent().width(width).height(height).depth(1)

            val pImage = stack.mallocLong(1)
            check(vkCreateImage(dev, imageInfo, null, pImage) == VK_SUCCESS)
            val image = pImage.get(0)

            val memReqs = VkMemoryRequirements.calloc(stack)
            vkGetImageMemoryRequirements(dev, image, memReqs)

            val allocInfo = VkMemoryAllocateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO)
                .allocationSize(memReqs.size())
                .memoryTypeIndex(findMemoryType(ctx, memReqs.memoryTypeBits(), memoryProperties))

            val pMemory = stack.mallocLong(1)
            check(vkAllocateMemory(dev, allocInfo, null, pMemory) == VK_SUCCESS)
            val memory = pMemory.get(0)

            vkBindImageMemory(dev, image, memory, 0)

            val viewInfo = VkImageViewCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO)
                .image(image).viewType(VK_IMAGE_VIEW_TYPE_2D).format(format)
            viewInfo.subresourceRange()
                .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                .baseMipLevel(0).levelCount(1)
                .baseArrayLayer(0).layerCount(1)

            val pView = stack.mallocLong(1)
            check(vkCreateImageView(dev, viewInfo, null, pView) == VK_SUCCESS)

            return VulkanImage(image, memory, pView.get(0), format, width, height)
        }
    }

    fun uploadBuffer(ctx: VulkanContext, buffer: VulkanBuffer, data: ByteBuffer) {
        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            val pData = stack.mallocPointer(1)
            vkMapMemory(dev, buffer.memory, 0, buffer.size, 0, pData)
            val mapped = pData.getByteBuffer(0, data.remaining())
            mapped.put(data)
            vkUnmapMemory(dev, buffer.memory)
        }
    }

    fun destroyBuffer(ctx: VulkanContext, buffer: VulkanBuffer) {
        val dev = ctx.device!!
        vkDestroyBuffer(dev, buffer.buffer, null)
        vkFreeMemory(dev, buffer.memory, null)
    }

    fun destroyImage(ctx: VulkanContext, image: VulkanImage) {
        val dev = ctx.device!!
        vkDestroyImageView(dev, image.view, null)
        vkDestroyImage(dev, image.image, null)
        vkFreeMemory(dev, image.memory, null)
    }

    private fun findMemoryType(ctx: VulkanContext, typeFilter: Int, properties: Int): Int {
        val physDev = ctx.physicalDevice!!
        MemoryStack.stackPush().use { stack ->
            val memProps = VkPhysicalDeviceMemoryProperties.calloc(stack)
            vkGetPhysicalDeviceMemoryProperties(physDev, memProps)
            for (i in 0 until memProps.memoryTypeCount()) {
                if (typeFilter and (1 shl i) != 0 &&
                    memProps.memoryTypes(i).propertyFlags() and properties == properties
                ) return i
            }
        }
        throw RuntimeException("Failed to find suitable memory type")
    }
}
