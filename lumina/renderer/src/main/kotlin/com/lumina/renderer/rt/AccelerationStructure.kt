package com.lumina.renderer.rt

import com.lumina.renderer.scene.SceneInstanceRecord
import com.lumina.renderer.vulkan.VulkanBuffer
import com.lumina.renderer.vulkan.VulkanContext
import com.lumina.renderer.vulkan.VulkanMemory
import com.lumina.scene.graph.MeshComponent
import org.lwjgl.system.MemoryStack
import org.lwjgl.system.MemoryUtil
import org.lwjgl.vulkan.*
import org.lwjgl.vulkan.KHRAccelerationStructure.*
import org.lwjgl.vulkan.KHRBufferDeviceAddress.VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR
import org.lwjgl.vulkan.KHRBufferDeviceAddress.vkGetBufferDeviceAddressKHR
import org.lwjgl.vulkan.KHRAccelerationStructure.VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_ACCELERATION_STRUCTURE_PROPERTIES_KHR
import org.lwjgl.vulkan.VK13.*
import org.slf4j.LoggerFactory
import java.nio.ByteBuffer
import javax.inject.Inject
import javax.inject.Singleton

data class BLASEntry(
    val handle: Int,
    val accelerationStructure: Long,
    val buffer: Long,
    val memory: Long,
    val deviceAddress: Long,
    val triangleCount: Int,
    val indexTriBase: Int = 0
)

@Singleton
class AccelerationStructureManager @Inject constructor(
    private val ctx: VulkanContext
) {
    private val log = LoggerFactory.getLogger(AccelerationStructureManager::class.java)
    private val blasCache = mutableMapOf<MeshComponent, BLASEntry>()
    private var nextBlasHandle = 1
    private var tlasAccelStruct: Long = 0
    private var tlasBuffer: Long = 0
    private var tlasMemory: Long = 0
    private var scratchAlignment: Long = 128

    fun queryScratchAlignment() {
        if (!ctx.rtSupported || ctx.physicalDevice == null) return
        MemoryStack.stackPush().use { stack ->
            val asProps = VkPhysicalDeviceAccelerationStructurePropertiesKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_ACCELERATION_STRUCTURE_PROPERTIES_KHR)
            val props2 = VkPhysicalDeviceProperties2.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_PROPERTIES_2)
                .pNext(asProps)
            vkGetPhysicalDeviceProperties2(ctx.physicalDevice!!, props2)
            scratchAlignment = asProps.minAccelerationStructureScratchOffsetAlignment().toLong()
            log.info("AS scratch alignment: {} bytes", scratchAlignment)
        }
    }

    private fun createAlignedScratchBuffer(size: Long): VulkanBuffer {
        val alignedSize = alignUp(size, scratchAlignment)
        return VulkanMemory.createBuffer(
            ctx, alignedSize,
            VK_BUFFER_USAGE_STORAGE_BUFFER_BIT or VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR,
            VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT
        )
    }

    private fun alignUp(value: Long, alignment: Long): Long {
        if (alignment <= 1) return value
        return (value + alignment - 1) and (alignment - 1).inv()
    }

    /**
     * Builds or returns cached BLAS for [mesh]. Dedup key is mesh reference identity — multiple
     * TLAS instances may share one BLAS with different transforms.
     */
    fun buildBLAS(
        mesh: MeshComponent,
        vertexBuffer: Long,
        indexBuffer: Long,
        vertexOffset: Int,
        indexOffset: Int,
        indexTriBase: Int = 0,
        totalVertexCount: Int = 0
    ): Int {
        if (!ctx.rtSupported) return -1
        if (!mesh.isRenderable()) {
            log.warn(
                "Skipping BLAS build for empty mesh ({} tris, {} verts, {} indices)",
                mesh.triangleCount,
                mesh.vertexCount,
                mesh.indexData.size
            )
            return -1
        }
        blasCache[mesh]?.let { return it.handle }

        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            val triangles = VkAccelerationStructureGeometryTrianglesDataKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_GEOMETRY_TRIANGLES_DATA_KHR)
                .vertexFormat(VK_FORMAT_R32G32B32_SFLOAT)
                .vertexStride(32)
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

            val buildInfo = VkAccelerationStructureBuildGeometryInfoKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_BUILD_GEOMETRY_INFO_KHR)
                .type(VK_ACCELERATION_STRUCTURE_TYPE_BOTTOM_LEVEL_KHR)
                .flags(
                    VK_BUILD_ACCELERATION_STRUCTURE_PREFER_FAST_TRACE_BIT_KHR or
                        VK_BUILD_ACCELERATION_STRUCTURE_ALLOW_COMPACTION_BIT_KHR
                )
                .geometryCount(1)
                .pGeometries(geometry)

            val sizeInfo = VkAccelerationStructureBuildSizesInfoKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_BUILD_SIZES_INFO_KHR)

            vkGetAccelerationStructureBuildSizesKHR(
                dev, VK_ACCELERATION_STRUCTURE_BUILD_TYPE_DEVICE_KHR,
                buildInfo, stack.ints(mesh.triangleCount), sizeInfo
            )

            val asBuffer = VulkanMemory.createBuffer(
                ctx, sizeInfo.accelerationStructureSize(),
                VK_BUFFER_USAGE_ACCELERATION_STRUCTURE_STORAGE_BIT_KHR or VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR,
                VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT
            )

            val asCreateInfo = VkAccelerationStructureCreateInfoKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_CREATE_INFO_KHR)
                .buffer(asBuffer.buffer)
                .size(sizeInfo.accelerationStructureSize())
                .type(VK_ACCELERATION_STRUCTURE_TYPE_BOTTOM_LEVEL_KHR)

            val pAS = stack.mallocLong(1)
            check(vkCreateAccelerationStructureKHR(dev, asCreateInfo, null, pAS) == VK_SUCCESS)
            val accelStruct = pAS.get(0)

            val scratch = createAlignedScratchBuffer(sizeInfo.buildScratchSize())

            buildInfo.dstAccelerationStructure(accelStruct)
            buildInfo.scratchData().deviceAddress(getBufferAddress(dev, scratch.buffer))

            val rangeInfo = VkAccelerationStructureBuildRangeInfoKHR.calloc(1, stack)
            rangeInfo.get(0).primitiveCount(mesh.triangleCount).primitiveOffset(0).firstVertex(0)

            val buildInfoBuf = VkAccelerationStructureBuildGeometryInfoKHR.calloc(1, stack)
            buildInfoBuf.put(0, buildInfo)

            val cmdBuf = beginSingleTimeCommands()
            vkCmdBuildAccelerationStructuresKHR(cmdBuf, buildInfoBuf, stack.pointers(rangeInfo))
            endSingleTimeCommands(cmdBuf)

            val addrInfo = VkAccelerationStructureDeviceAddressInfoKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_ACCELERATION_STRUCTURE_DEVICE_ADDRESS_INFO_KHR)
                .accelerationStructure(accelStruct)

            val deviceAddr = vkGetAccelerationStructureDeviceAddressKHR(dev, addrInfo)
            VulkanMemory.destroyBuffer(ctx, scratch)

            val handle = nextBlasHandle++
            val entry = BLASEntry(handle, accelStruct, asBuffer.buffer, asBuffer.memory, deviceAddr, mesh.triangleCount, indexTriBase)
            blasCache[mesh] = entry
            mesh.blasId = handle

            log.info(
                "Built BLAS handle={}: {} triangles, indexTriBase={} ({} unique BLAS total)",
                handle,
                mesh.triangleCount,
                indexTriBase,
                blasCache.size
            )
            return handle
        }
    }

    fun rebuildTLAS(instances: List<SceneInstanceRecord>) {
        if (!ctx.rtSupported) return
        val dev = ctx.device!!
        if (instances.isEmpty()) {
            log.warn("rebuildTLAS: no instance records (upload scene first?)")
            return
        }

        if (instances.size >= com.lumina.renderer.scene.SceneBufferManager.INSTANCE_WARN_THRESHOLD) {
            log.warn(
                "TLAS rebuilding {} instances (warn threshold {})",
                instances.size,
                com.lumina.renderer.scene.SceneBufferManager.INSTANCE_WARN_THRESHOLD
            )
        }

        // Resolve BLAS handles first — abort rather than build a partial TLAS that drops geometry.
        val resolved = ArrayList<Pair<SceneInstanceRecord, BLASEntry>>(instances.size)
        for (record in instances) {
            val blas = blasCache.values.firstOrNull { it.handle == record.blasId }
            if (blas == null) {
                log.error(
                    "TLAS rebuild aborted: instance[{}] {} — BLAS handle {} missing ({} of {} instances); " +
                        "keeping previous TLAS to avoid dropping objects",
                    record.instanceIndex,
                    record.nodeName,
                    record.blasId,
                    resolved.size,
                    instances.size
                )
                return
            }
            resolved.add(record to blas)
        }

        MemoryStack.stackPush().use { stack ->
            val instanceSize = 64L * resolved.size
            val instanceData = MemoryUtil.memAlloc(instanceSize.toInt())

            for ((i, pair) in resolved.withIndex()) {
                val (record, blas) = pair
                val offset = i * 64
                val xform = record.transform

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

                // instanceCustomIndex indexes material[] and instanceInfo[] SSBOs (24-bit, no wrap)
                val customIndex = record.instanceIndex
                if (customIndex >= com.lumina.renderer.scene.SceneBufferManager.MAX_TLAS_INSTANCES) {
                    log.error(
                        "TLAS rebuild aborted: instance index {} exceeds 24-bit customIndex limit for {}",
                        customIndex,
                        record.nodeName
                    )
                    MemoryUtil.memFree(instanceData)
                    return
                }
                val instanceMask = record.rayTraceMask and 0xFF
                instanceData.putInt(offset + 48, customIndex or (instanceMask shl 24))
                instanceData.putInt(offset + 52, 0)
                instanceData.putLong(offset + 56, blas.deviceAddress)

                log.info(
                    "tlas[{}] instIdx={} {} blas={} triBase={}",
                    i,
                    customIndex,
                    record.nodeName,
                    record.blasId,
                    record.indexTriBase
                )
            }

            val built = resolved.size
            if (built == 0) return

            val instBuf = VulkanMemory.createBuffer(
                ctx, 64L * built,
                VK_BUFFER_USAGE_ACCELERATION_STRUCTURE_BUILD_INPUT_READ_ONLY_BIT_KHR or
                    VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR,
                VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT or VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
            )
            VulkanMemory.uploadBuffer(ctx, instBuf, instanceData)
            MemoryUtil.memFree(instanceData)

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
                buildInfo, stack.ints(built), sizeInfo
            )

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

            val scratch = createAlignedScratchBuffer(sizeInfo.buildScratchSize())

            buildInfo.dstAccelerationStructure(tlasAccelStruct)
            buildInfo.scratchData().deviceAddress(getBufferAddress(dev, scratch.buffer))

            val rangeInfo = VkAccelerationStructureBuildRangeInfoKHR.calloc(1, stack)
            rangeInfo.get(0).primitiveCount(built)

            val tlasBuildInfoBuf = VkAccelerationStructureBuildGeometryInfoKHR.calloc(1, stack)
            tlasBuildInfoBuf.put(0, buildInfo)

            val cmdBuf = beginSingleTimeCommands()
            vkCmdBuildAccelerationStructuresKHR(cmdBuf, tlasBuildInfoBuf, stack.pointers(rangeInfo))
            endSingleTimeCommands(cmdBuf)

            VulkanMemory.destroyBuffer(ctx, scratch)
            VulkanMemory.destroyBuffer(ctx, instBuf)

            log.info("Rebuilt TLAS: {} instances, {} unique BLAS", built, blasCache.size)
        }
    }

    fun getTLASHandle(): Long = tlasAccelStruct
    fun getBLASCount(): Int = blasCache.size

    fun clearBlasCache() {
        if (!ctx.rtSupported || blasCache.isEmpty()) {
            blasCache.clear()
            nextBlasHandle = 1
            return
        }
        val dev = ctx.device!!
        for (entry in blasCache.values) {
            vkDestroyAccelerationStructureKHR(dev, entry.accelerationStructure, null)
            vkDestroyBuffer(dev, entry.buffer, null)
            vkFreeMemory(dev, entry.memory, null)
        }
        blasCache.clear()
        nextBlasHandle = 1
    }

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
