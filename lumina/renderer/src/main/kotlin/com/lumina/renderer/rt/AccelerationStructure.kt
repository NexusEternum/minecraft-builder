package com.lumina.renderer.rt

import com.lumina.renderer.vulkan.VulkanContext
import com.lumina.renderer.vulkan.VulkanMemory
import com.lumina.scene.graph.MeshComponent
import com.lumina.scene.graph.SceneGraph
import com.lumina.scene.graph.Transform
import org.lwjgl.system.MemoryStack
import org.lwjgl.system.MemoryUtil
import org.lwjgl.vulkan.*
import org.lwjgl.vulkan.KHRAccelerationStructure.*
import org.lwjgl.vulkan.KHRBufferDeviceAddress.VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR
import org.lwjgl.vulkan.KHRBufferDeviceAddress.vkGetBufferDeviceAddressKHR
import org.lwjgl.vulkan.VK13.*
import org.slf4j.LoggerFactory
import java.nio.ByteBuffer
import javax.inject.Inject
import javax.inject.Singleton

data class BLASEntry(
    val handle: Long,
    val accelerationStructure: Long,
    val buffer: Long,
    val memory: Long,
    val deviceAddress: Long,
    val triangleCount: Int,
    val indexTriBase: Int = 0
)

@Singleton
class AccelerationStructureManager @Inject constructor(
    private val ctx: VulkanContext,
    private val sceneGraph: SceneGraph
) {
    private val log = LoggerFactory.getLogger(AccelerationStructureManager::class.java)
    private val blasCache = mutableMapOf<Int, BLASEntry>()
    private var tlasHandle: Long = 0
    private var tlasAccelStruct: Long = 0
    private var tlasBuffer: Long = 0
    private var tlasMemory: Long = 0
    private var instanceBuffer: Long = 0
    private var instanceMemory: Long = 0
    private var scratchBuffer: Long = 0
    private var scratchMemory: Long = 0

    fun buildBLAS(mesh: MeshComponent, vertexBuffer: Long, indexBuffer: Long, vertexOffset: Int, indexOffset: Int, indexTriBase: Int = 0, totalVertexCount: Int = 0): Int {
        if (!ctx.rtSupported) return -1
        val hash = System.identityHashCode(mesh)
        if (blasCache.containsKey(hash)) return hash

        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            // Geometry description
            val triangles = VkAccelerationStructureGeometryTrianglesDataKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_GEOMETRY_TRIANGLES_DATA_KHR)
                .vertexFormat(VK_FORMAT_R32G32B32_SFLOAT)
                .vertexStride(32) // 8 floats * 4 bytes
                .maxVertex(if (totalVertexCount > 0) totalVertexCount - 1 else mesh.vertexCount - 1)
                .indexType(VK_INDEX_TYPE_UINT32)

            triangles.vertexData().deviceAddress(getBufferAddress(dev, vertexBuffer) + vertexOffset.toLong())
            triangles.indexData().deviceAddress(getBufferAddress(dev, indexBuffer) + indexOffset.toLong())

            val geometry = VkAccelerationStructureGeometryKHR.calloc(1, stack)
            geometry.get(0)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_GEOMETRY_KHR)
                .geometryType(VK_GEOMETRY_TYPE_TRIANGLES_KHR)
                .flags(VK_GEOMETRY_OPAQUE_BIT_KHR)
            geometry.get(0).geometry().triangles(triangles)

            // Query build sizes
            val buildInfo = VkAccelerationStructureBuildGeometryInfoKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_BUILD_GEOMETRY_INFO_KHR)
                .type(VK_ACCELERATION_STRUCTURE_TYPE_BOTTOM_LEVEL_KHR)
                .flags(VK_BUILD_ACCELERATION_STRUCTURE_PREFER_FAST_TRACE_BIT_KHR or
                       VK_BUILD_ACCELERATION_STRUCTURE_ALLOW_COMPACTION_BIT_KHR)
                .geometryCount(1)
                .pGeometries(geometry)

            val sizeInfo = VkAccelerationStructureBuildSizesInfoKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_BUILD_SIZES_INFO_KHR)

            vkGetAccelerationStructureBuildSizesKHR(
                dev, VK_ACCELERATION_STRUCTURE_BUILD_TYPE_DEVICE_KHR,
                buildInfo, stack.ints(mesh.triangleCount), sizeInfo
            )

            // Create acceleration structure buffer
            val asBuffer = VulkanMemory.createBuffer(
                ctx, sizeInfo.accelerationStructureSize(),
                VK_BUFFER_USAGE_ACCELERATION_STRUCTURE_STORAGE_BIT_KHR or VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR,
                VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT
            )

            // Create the acceleration structure
            val asCreateInfo = VkAccelerationStructureCreateInfoKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_CREATE_INFO_KHR)
                .buffer(asBuffer.buffer)
                .size(sizeInfo.accelerationStructureSize())
                .type(VK_ACCELERATION_STRUCTURE_TYPE_BOTTOM_LEVEL_KHR)

            val pAS = stack.mallocLong(1)
            check(vkCreateAccelerationStructureKHR(dev, asCreateInfo, null, pAS) == VK_SUCCESS)
            val accelStruct = pAS.get(0)

            // Create scratch buffer
            val scratch = VulkanMemory.createBuffer(
                ctx, sizeInfo.buildScratchSize(),
                VK_BUFFER_USAGE_STORAGE_BUFFER_BIT or VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR,
                VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT
            )

            // Build
            buildInfo.dstAccelerationStructure(accelStruct)
            buildInfo.scratchData().deviceAddress(getBufferAddress(dev, scratch.buffer))

            val rangeInfo = VkAccelerationStructureBuildRangeInfoKHR.calloc(1, stack)
            rangeInfo.get(0).primitiveCount(mesh.triangleCount).primitiveOffset(0).firstVertex(0)

            val buildInfoBuf = VkAccelerationStructureBuildGeometryInfoKHR.calloc(1, stack)
            buildInfoBuf.put(0, buildInfo)

            val cmdBuf = beginSingleTimeCommands()
            vkCmdBuildAccelerationStructuresKHR(cmdBuf, buildInfoBuf, stack.pointers(rangeInfo))
            endSingleTimeCommands(cmdBuf)

            // Get device address
            val addrInfo = VkAccelerationStructureDeviceAddressInfoKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_DEVICE_ADDRESS_INFO_KHR)
                .accelerationStructure(accelStruct)

            val deviceAddr = vkGetAccelerationStructureDeviceAddressKHR(dev, addrInfo)

            // Cleanup scratch
            VulkanMemory.destroyBuffer(ctx, scratch)

            val entry = BLASEntry(hash.toLong(), accelStruct, asBuffer.buffer, asBuffer.memory, deviceAddr, mesh.triangleCount, indexTriBase)
            blasCache[hash] = entry
            mesh.blasId = hash

            log.debug("Built BLAS: {} triangles, {} bytes", mesh.triangleCount, sizeInfo.accelerationStructureSize())
            return hash
        }
    }

    fun rebuildTLAS() {
        if (!ctx.rtSupported) return
        val dev = ctx.device!!

        val meshNodes = sceneGraph.nodesWithComponent(MeshComponent::class.java)
        val instances = mutableListOf<Pair<BLASEntry, Transform>>()

        for (node in meshNodes) {
            val mesh = node.getComponent(MeshComponent::class.java) ?: continue
            val transform = node.getComponent(Transform::class.java) ?: Transform()
            val blas = blasCache[mesh.blasId] ?: continue
            instances.add(blas to transform)
        }

        if (instances.isEmpty()) return

        MemoryStack.stackPush().use { stack ->
            // Create instance buffer
            val instanceSize = 64L * instances.size // VkAccelerationStructureInstanceKHR = 64 bytes
            val instanceData = MemoryUtil.memAlloc(instanceSize.toInt())

            for ((i, pair) in instances.withIndex()) {
                val (blas, xform) = pair
                val offset = i * 64

                // 3x4 row-major transform matrix
                instanceData.putFloat(offset + 0, xform.scaleX)
                instanceData.putFloat(offset + 4, 0f)
                instanceData.putFloat(offset + 8, 0f)
                instanceData.putFloat(offset + 12, xform.x)
                instanceData.putFloat(offset + 16, 0f)
                instanceData.putFloat(offset + 20, xform.scaleY)
                instanceData.putFloat(offset + 24, 0f)
                instanceData.putFloat(offset + 28, xform.y)
                instanceData.putFloat(offset + 32, 0f)
                instanceData.putFloat(offset + 36, 0f)
                instanceData.putFloat(offset + 40, xform.scaleZ)
                instanceData.putFloat(offset + 44, xform.z)

                // instanceCustomIndex:24 (lower 12 = material index, upper 12 = index tri base), mask:8
                val customIndex = (i and 0xFFF) or ((blas.indexTriBase and 0xFFF) shl 12)
                instanceData.putInt(offset + 48, customIndex or (0xFF shl 24))
                // instanceShaderBindingTableRecordOffset:24, flags:8
                instanceData.putInt(offset + 52, 0)
                // accelerationStructureReference
                instanceData.putLong(offset + 56, blas.deviceAddress)
            }
            instanceData.flip()

            val instBuf = VulkanMemory.createBuffer(
                ctx, instanceSize,
                VK_BUFFER_USAGE_ACCELERATION_STRUCTURE_BUILD_INPUT_READ_ONLY_BIT_KHR or
                VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR,
                VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT or VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
            )
            VulkanMemory.uploadBuffer(ctx, instBuf, instanceData)
            MemoryUtil.memFree(instanceData)

            // TLAS geometry
            val instancesData = VkAccelerationStructureGeometryInstancesDataKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_GEOMETRY_INSTANCES_DATA_KHR)
                .arrayOfPointers(false)
            instancesData.data().deviceAddress(getBufferAddress(dev, instBuf.buffer))

            val geometry = VkAccelerationStructureGeometryKHR.calloc(1, stack)
            geometry.get(0)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_GEOMETRY_KHR)
                .geometryType(VK_GEOMETRY_TYPE_INSTANCES_KHR)
            geometry.get(0).geometry().instances(instancesData)

            val buildInfo = VkAccelerationStructureBuildGeometryInfoKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_BUILD_GEOMETRY_INFO_KHR)
                .type(VK_ACCELERATION_STRUCTURE_TYPE_TOP_LEVEL_KHR)
                .flags(VK_BUILD_ACCELERATION_STRUCTURE_PREFER_FAST_TRACE_BIT_KHR)
                .geometryCount(1)
                .pGeometries(geometry)

            val sizeInfo = VkAccelerationStructureBuildSizesInfoKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_BUILD_SIZES_INFO_KHR)

            vkGetAccelerationStructureBuildSizesKHR(
                dev, VK_ACCELERATION_STRUCTURE_BUILD_TYPE_DEVICE_KHR,
                buildInfo, stack.ints(instances.size), sizeInfo
            )

            // Destroy old TLAS
            if (tlasAccelStruct != 0L) {
                vkDestroyAccelerationStructureKHR(dev, tlasAccelStruct, null)
                vkDestroyBuffer(dev, tlasBuffer, null)
                vkFreeMemory(dev, tlasMemory, null)
            }

            val tlasBuf = VulkanMemory.createBuffer(
                ctx, sizeInfo.accelerationStructureSize(),
                VK_BUFFER_USAGE_ACCELERATION_STRUCTURE_STORAGE_BIT_KHR or VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR,
                VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT
            )

            val asCreateInfo = VkAccelerationStructureCreateInfoKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_CREATE_INFO_KHR)
                .buffer(tlasBuf.buffer)
                .size(sizeInfo.accelerationStructureSize())
                .type(VK_ACCELERATION_STRUCTURE_TYPE_TOP_LEVEL_KHR)

            val pAS = stack.mallocLong(1)
            check(vkCreateAccelerationStructureKHR(dev, asCreateInfo, null, pAS) == VK_SUCCESS)
            tlasAccelStruct = pAS.get(0)
            tlasBuffer = tlasBuf.buffer
            tlasMemory = tlasBuf.memory

            val scratch = VulkanMemory.createBuffer(
                ctx, sizeInfo.buildScratchSize(),
                VK_BUFFER_USAGE_STORAGE_BUFFER_BIT or VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR,
                VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT
            )

            buildInfo.dstAccelerationStructure(tlasAccelStruct)
            buildInfo.scratchData().deviceAddress(getBufferAddress(dev, scratch.buffer))

            val rangeInfo = VkAccelerationStructureBuildRangeInfoKHR.calloc(1, stack)
            rangeInfo.get(0).primitiveCount(instances.size)

            val tlasBuildInfoBuf = VkAccelerationStructureBuildGeometryInfoKHR.calloc(1, stack)
            tlasBuildInfoBuf.put(0, buildInfo)

            val cmdBuf = beginSingleTimeCommands()
            vkCmdBuildAccelerationStructuresKHR(cmdBuf, tlasBuildInfoBuf, stack.pointers(rangeInfo))
            endSingleTimeCommands(cmdBuf)

            VulkanMemory.destroyBuffer(ctx, scratch)
            VulkanMemory.destroyBuffer(ctx, instBuf)

            log.debug("Rebuilt TLAS: {} instances", instances.size)
        }
    }

    fun getTLASHandle(): Long = tlasAccelStruct
    fun getBLASCount(): Int = blasCache.size

    private fun getBufferAddress(dev: VkDevice, buffer: Long): Long {
        MemoryStack.stackPush().use { stack ->
            val addrInfo = VkBufferDeviceAddressInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_BUFFER_DEVICE_ADDRESS_INFO)
                .buffer(buffer)
            return vkGetBufferDeviceAddressKHR(dev, addrInfo)
        }
    }

    private fun beginSingleTimeCommands(): VkCommandBuffer {
        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            val allocInfo = VkCommandBufferAllocateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO)
                .commandPool(ctx.commandPool)
                .level(VK_COMMAND_BUFFER_LEVEL_PRIMARY)
                .commandBufferCount(1)

            val pBuf = stack.mallocPointer(1)
            vkAllocateCommandBuffers(dev, allocInfo, pBuf)
            val cmdBuf = VkCommandBuffer(pBuf.get(0), dev)

            val beginInfo = VkCommandBufferBeginInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO)
                .flags(VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT)

            vkBeginCommandBuffer(cmdBuf, beginInfo)
            return cmdBuf
        }
    }

    private fun endSingleTimeCommands(cmdBuf: VkCommandBuffer) {
        val dev = ctx.device!!
        vkEndCommandBuffer(cmdBuf)

        MemoryStack.stackPush().use { stack ->
            val submitInfo = VkSubmitInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_SUBMIT_INFO)
                .pCommandBuffers(stack.pointers(cmdBuf))

            vkQueueSubmit(ctx.graphicsQueue!!, submitInfo, 0L)
            vkQueueWaitIdle(ctx.graphicsQueue!!)
            vkFreeCommandBuffers(dev, ctx.commandPool, cmdBuf)
        }
    }

    fun destroy() {
        val dev = ctx.device ?: return
        if (tlasAccelStruct != 0L) {
            vkDestroyAccelerationStructureKHR(dev, tlasAccelStruct, null)
            vkDestroyBuffer(dev, tlasBuffer, null)
            vkFreeMemory(dev, tlasMemory, null)
        }
        for (entry in blasCache.values) {
            vkDestroyAccelerationStructureKHR(dev, entry.accelerationStructure, null)
            vkDestroyBuffer(dev, entry.buffer, null)
            vkFreeMemory(dev, entry.memory, null)
        }
        blasCache.clear()
        log.info("Acceleration structures destroyed")
    }
}
