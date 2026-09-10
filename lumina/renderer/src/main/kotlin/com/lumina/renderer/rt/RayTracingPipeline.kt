package com.lumina.renderer.rt

import com.lumina.renderer.vulkan.*
import org.lwjgl.system.MemoryStack
import org.lwjgl.system.MemoryUtil
import org.lwjgl.vulkan.*
import org.lwjgl.vulkan.KHRAccelerationStructure
import org.lwjgl.vulkan.KHRAccelerationStructure.VK_DESCRIPTOR_TYPE_ACCELERATION_STRUCTURE_KHR
import org.lwjgl.vulkan.KHRBufferDeviceAddress.VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR
import org.lwjgl.vulkan.KHRRayTracingPipeline.*
import org.lwjgl.vulkan.VK13.*
import org.slf4j.LoggerFactory
import java.nio.ByteBuffer
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class RayTracingPipeline @Inject constructor(
    private val ctx: VulkanContext,
    private val shaderCompiler: ShaderCompiler,
    private val accelStructure: AccelerationStructureManager
) {
    private val log = LoggerFactory.getLogger(RayTracingPipeline::class.java)

    var pipeline: Long = 0; private set
    var pipelineLayout: Long = 0; private set
    var descriptorSetLayout: Long = 0; private set
    var descriptorPool: Long = 0; private set
    var descriptorSet: Long = 0; private set

    private var sbtBuffer: Long = 0
    private var sbtMemory: Long = 0
    private var raygenRegion = VkStridedDeviceAddressRegionKHR.create()
    private var missRegion = VkStridedDeviceAddressRegionKHR.create()
    private var hitRegion = VkStridedDeviceAddressRegionKHR.create()
    private var callableRegion = VkStridedDeviceAddressRegionKHR.create()

    var spp: Int = 1
    var maxBounces: Int = 4

    fun init() {
        if (!ctx.rtSupported) {
            log.warn("RT pipeline not available -- hardware ray tracing not supported")
            return
        }
        createDescriptorSetLayout()
        createDescriptorPool()
        createPipeline()
        createShaderBindingTable()
        log.info("RT pipeline initialized (SPP: {}, bounces: {})", spp, maxBounces)
    }

    private fun createDescriptorSetLayout() {
        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            val bindings = VkDescriptorSetLayoutBinding.calloc(8, stack)

            // Binding 0: TLAS
            bindings.get(0)
                .binding(0)
                .descriptorType(VK_DESCRIPTOR_TYPE_ACCELERATION_STRUCTURE_KHR)
                .descriptorCount(1)
                .stageFlags(VK_SHADER_STAGE_RAYGEN_BIT_KHR or VK_SHADER_STAGE_CLOSEST_HIT_BIT_KHR)

            // Binding 1: Output image
            bindings.get(1).binding(1)
                .descriptorType(VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
                .descriptorCount(1)
                .stageFlags(VK_SHADER_STAGE_RAYGEN_BIT_KHR)

            // Binding 2: Normal/depth image
            bindings.get(2).binding(2)
                .descriptorType(VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
                .descriptorCount(1)
                .stageFlags(VK_SHADER_STAGE_RAYGEN_BIT_KHR)

            // Binding 3: Motion vector image
            bindings.get(3).binding(3)
                .descriptorType(VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
                .descriptorCount(1)
                .stageFlags(VK_SHADER_STAGE_RAYGEN_BIT_KHR)

            // Binding 4: Camera UBO
            bindings.get(4).binding(4)
                .descriptorType(VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER)
                .descriptorCount(1)
                .stageFlags(VK_SHADER_STAGE_RAYGEN_BIT_KHR or VK_SHADER_STAGE_MISS_BIT_KHR)

            // Binding 5: Vertex buffer SSBO
            bindings.get(5).binding(5)
                .descriptorType(VK_DESCRIPTOR_TYPE_STORAGE_BUFFER)
                .descriptorCount(1)
                .stageFlags(VK_SHADER_STAGE_CLOSEST_HIT_BIT_KHR)

            // Binding 6: Index buffer SSBO
            bindings.get(6).binding(6)
                .descriptorType(VK_DESCRIPTOR_TYPE_STORAGE_BUFFER)
                .descriptorCount(1)
                .stageFlags(VK_SHADER_STAGE_CLOSEST_HIT_BIT_KHR)

            // Binding 7: Material buffer SSBO
            bindings.get(7).binding(7)
                .descriptorType(VK_DESCRIPTOR_TYPE_STORAGE_BUFFER)
                .descriptorCount(1)
                .stageFlags(VK_SHADER_STAGE_CLOSEST_HIT_BIT_KHR)

            val layoutInfo = VkDescriptorSetLayoutCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO)
                .pBindings(bindings)

            val pLayout = stack.mallocLong(1)
            check(vkCreateDescriptorSetLayout(dev, layoutInfo, null, pLayout) == VK_SUCCESS)
            descriptorSetLayout = pLayout.get(0)

            // Pipeline layout
            val pipelineLayoutInfo = VkPipelineLayoutCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO)
                .pSetLayouts(stack.longs(descriptorSetLayout))

            val pPipelineLayout = stack.mallocLong(1)
            check(vkCreatePipelineLayout(dev, pipelineLayoutInfo, null, pPipelineLayout) == VK_SUCCESS)
            pipelineLayout = pPipelineLayout.get(0)
        }
    }

    private fun createDescriptorPool() {
        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            val poolSizes = VkDescriptorPoolSize.calloc(4, stack)
            poolSizes.get(0).type(VK_DESCRIPTOR_TYPE_ACCELERATION_STRUCTURE_KHR).descriptorCount(1)
            poolSizes.get(1).type(VK_DESCRIPTOR_TYPE_STORAGE_IMAGE).descriptorCount(3)
            poolSizes.get(2).type(VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER).descriptorCount(1)
            poolSizes.get(3).type(VK_DESCRIPTOR_TYPE_STORAGE_BUFFER).descriptorCount(3)

            val poolInfo = VkDescriptorPoolCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO)
                .maxSets(1)
                .pPoolSizes(poolSizes)

            val pPool = stack.mallocLong(1)
            check(vkCreateDescriptorPool(dev, poolInfo, null, pPool) == VK_SUCCESS)
            descriptorPool = pPool.get(0)

            // Allocate descriptor set
            val allocInfo = VkDescriptorSetAllocateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO)
                .descriptorPool(descriptorPool)
                .pSetLayouts(stack.longs(descriptorSetLayout))

            val pSet = stack.mallocLong(1)
            check(vkAllocateDescriptorSets(dev, allocInfo, pSet) == VK_SUCCESS)
            descriptorSet = pSet.get(0)
        }
    }

    private fun createPipeline() {
        val dev = ctx.device!!

        val raygenShader = shaderCompiler.compileFromResource("/shaders/rt/raygen.rgen", ShaderStage.RAYGEN)
        val chitShader = shaderCompiler.compileFromResource("/shaders/rt/closesthit.rchit", ShaderStage.CLOSEST_HIT)
        val missShader = shaderCompiler.compileFromResource("/shaders/rt/miss.rmiss", ShaderStage.MISS)
        val shadowMissShader = shaderCompiler.compileFromResource("/shaders/rt/shadow.rmiss", ShaderStage.MISS)

        MemoryStack.stackPush().use { stack ->
            val stages = VkPipelineShaderStageCreateInfo.calloc(4, stack)
            stages.get(0).sType(VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO)
                .stage(VK_SHADER_STAGE_RAYGEN_BIT_KHR)
                .module(raygenShader.module)
                .pName(stack.UTF8("main"))
            stages.get(1).sType(VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO)
                .stage(VK_SHADER_STAGE_CLOSEST_HIT_BIT_KHR)
                .module(chitShader.module)
                .pName(stack.UTF8("main"))
            stages.get(2).sType(VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO)
                .stage(VK_SHADER_STAGE_MISS_BIT_KHR)
                .module(missShader.module)
                .pName(stack.UTF8("main"))
            stages.get(3).sType(VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO)
                .stage(VK_SHADER_STAGE_MISS_BIT_KHR)
                .module(shadowMissShader.module)
                .pName(stack.UTF8("main"))

            // Shader groups
            val groups = VkRayTracingShaderGroupCreateInfoKHR.calloc(4, stack)

            // Group 0: Ray generation
            groups.get(0).sType(VK_STRUCTURE_TYPE_RAY_TRACING_SHADER_GROUP_CREATE_INFO_KHR)
                .type(VK_RAY_TRACING_SHADER_GROUP_TYPE_GENERAL_KHR)
                .generalShader(0).closestHitShader(VK_SHADER_UNUSED_KHR)
                .anyHitShader(VK_SHADER_UNUSED_KHR).intersectionShader(VK_SHADER_UNUSED_KHR)

            // Group 1: Closest hit
            groups.get(1).sType(VK_STRUCTURE_TYPE_RAY_TRACING_SHADER_GROUP_CREATE_INFO_KHR)
                .type(VK_RAY_TRACING_SHADER_GROUP_TYPE_TRIANGLES_HIT_GROUP_KHR)
                .generalShader(VK_SHADER_UNUSED_KHR).closestHitShader(1)
                .anyHitShader(VK_SHADER_UNUSED_KHR).intersectionShader(VK_SHADER_UNUSED_KHR)

            // Group 2: Miss
            groups.get(2).sType(VK_STRUCTURE_TYPE_RAY_TRACING_SHADER_GROUP_CREATE_INFO_KHR)
                .type(VK_RAY_TRACING_SHADER_GROUP_TYPE_GENERAL_KHR)
                .generalShader(2).closestHitShader(VK_SHADER_UNUSED_KHR)
                .anyHitShader(VK_SHADER_UNUSED_KHR).intersectionShader(VK_SHADER_UNUSED_KHR)

            // Group 3: Shadow miss
            groups.get(3).sType(VK_STRUCTURE_TYPE_RAY_TRACING_SHADER_GROUP_CREATE_INFO_KHR)
                .type(VK_RAY_TRACING_SHADER_GROUP_TYPE_GENERAL_KHR)
                .generalShader(3).closestHitShader(VK_SHADER_UNUSED_KHR)
                .anyHitShader(VK_SHADER_UNUSED_KHR).intersectionShader(VK_SHADER_UNUSED_KHR)

            val createInfo = VkRayTracingPipelineCreateInfoKHR.calloc(1, stack)
            createInfo.get(0)
                .sType(VK_STRUCTURE_TYPE_RAY_TRACING_PIPELINE_CREATE_INFO_KHR)
                .pStages(stages)
                .pGroups(groups)
                .maxPipelineRayRecursionDepth(2)
                .layout(pipelineLayout)

            val pPipeline = stack.mallocLong(1)
            check(vkCreateRayTracingPipelinesKHR(dev, 0L, 0L, createInfo, null, pPipeline) == VK_SUCCESS)
            pipeline = pPipeline.get(0)

            log.info("RT pipeline created (4 shader groups, max recursion: 2)")
        }
    }

    private fun createShaderBindingTable() {
        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            val rtProps = VkPhysicalDeviceRayTracingPipelinePropertiesKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_RAY_TRACING_PIPELINE_PROPERTIES_KHR)

            val deviceProps = VkPhysicalDeviceProperties2.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_PROPERTIES_2)
                .pNext(rtProps)

            vkGetPhysicalDeviceProperties2(ctx.physicalDevice!!, deviceProps)

            val handleSize = rtProps.shaderGroupHandleSize()
            val handleAlignment = rtProps.shaderGroupHandleAlignment()
            val baseAlignment = rtProps.shaderGroupBaseAlignment()

            val alignedHandleSize = alignUp(handleSize, handleAlignment)

            val raygenSize = alignUp(alignedHandleSize, baseAlignment).toLong()
            val missSize = alignUp(alignedHandleSize * 2, baseAlignment).toLong()
            val hitSize = alignUp(alignedHandleSize, baseAlignment).toLong()

            val sbtSize = raygenSize + missSize + hitSize

            // Get shader group handles
            val handleData = MemoryUtil.memAlloc(handleSize * 4)
            vkGetRayTracingShaderGroupHandlesKHR(dev, pipeline, 0, 4, handleData)

            // Create SBT buffer
            val buf = VulkanMemory.createBuffer(
                ctx, sbtSize,
                VK_BUFFER_USAGE_SHADER_BINDING_TABLE_BIT_KHR or VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR,
                VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT or VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
            )
            sbtBuffer = buf.buffer
            sbtMemory = buf.memory

            // Map and write handles
            val pData = stack.mallocPointer(1)
            vkMapMemory(dev, buf.memory, 0, sbtSize, 0, pData)
            val mapped = pData.getByteBuffer(0, sbtSize.toInt())

            // Raygen handle at offset 0
            handleData.position(0).limit(handleSize)
            mapped.position(0)
            mapped.put(handleData.slice().limit(handleSize) as ByteBuffer)

            // Miss handles
            handleData.position(handleSize * 2).limit(handleSize * 3)
            mapped.position(raygenSize.toInt())
            mapped.put(handleData.slice().limit(handleSize) as ByteBuffer)

            handleData.position(handleSize * 3).limit(handleSize * 4)
            mapped.position((raygenSize + alignedHandleSize).toInt())
            mapped.put(handleData.slice().limit(handleSize) as ByteBuffer)

            // Hit handle
            handleData.position(handleSize).limit(handleSize * 2)
            mapped.position((raygenSize + missSize).toInt())
            mapped.put(handleData.slice().limit(handleSize) as ByteBuffer)

            vkUnmapMemory(dev, buf.memory)
            MemoryUtil.memFree(handleData)

            // Set up regions
            val addrInfo = VkBufferDeviceAddressInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_BUFFER_DEVICE_ADDRESS_INFO)
                .buffer(sbtBuffer)
            val sbtAddr = vkGetBufferDeviceAddress(dev, addrInfo)

            raygenRegion.deviceAddress(sbtAddr).stride(raygenSize).size(raygenSize)
            missRegion.deviceAddress(sbtAddr + raygenSize).stride(alignedHandleSize.toLong()).size(missSize)
            hitRegion.deviceAddress(sbtAddr + raygenSize + missSize).stride(alignedHandleSize.toLong()).size(hitSize)
            callableRegion.deviceAddress(0).stride(0).size(0)

            log.info("SBT created: raygen={}, miss={}, hit={} bytes", raygenSize, missSize, hitSize)
        }
    }

    fun recordCommands(cmdBuf: VkCommandBuffer, width: Int, height: Int) {
        if (!ctx.rtSupported || pipeline == 0L) return

        vkCmdBindPipeline(cmdBuf, VK_PIPELINE_BIND_POINT_RAY_TRACING_KHR, pipeline)

        MemoryStack.stackPush().use { stack ->
            vkCmdBindDescriptorSets(
                cmdBuf, VK_PIPELINE_BIND_POINT_RAY_TRACING_KHR, pipelineLayout,
                0, stack.longs(descriptorSet), null
            )
        }

        vkCmdTraceRaysKHR(
            cmdBuf,
            raygenRegion, missRegion, hitRegion, callableRegion,
            width, height, 1
        )
    }

    fun updateDescriptors(renderTargets: RenderTargets, cameraUbo: VulkanBuffer? = null,
                          vertexBuffer: VulkanBuffer? = null, indexBuffer: VulkanBuffer? = null,
                          materialBuffer: VulkanBuffer? = null) {
        if (!ctx.rtSupported || descriptorSet == 0L) return
        val dev = ctx.device!!
        val rt = renderTargets

        MemoryStack.stackPush().use { stack ->
            val writes = mutableListOf<() -> Unit>()

            // Binding 0: TLAS
            if (accelStructure.getTLASHandle() != 0L) {
                val asWrite = VkWriteDescriptorSetAccelerationStructureKHR.calloc(stack)
                    .sType(KHRAccelerationStructure.VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET_ACCELERATION_STRUCTURE_KHR)
                    .pAccelerationStructures(stack.longs(accelStructure.getTLASHandle()))

                val write = VkWriteDescriptorSet.calloc(1, stack)
                write.get(0)
                    .sType(VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET)
                    .dstSet(descriptorSet)
                    .dstBinding(0)
                    .descriptorCount(1)
                    .descriptorType(VK_DESCRIPTOR_TYPE_ACCELERATION_STRUCTURE_KHR)
                    .pNext(asWrite)

                vkUpdateDescriptorSets(dev, write, null)
            }

            // Bindings 1-3: Storage images
            val imageBindings = listOf(
                1 to rt.rtOutputColor,
                2 to rt.rtNormalDepth,
                3 to rt.rtMotionVectors
            )
            for ((binding, image) in imageBindings) {
                if (image != null) {
                    ComputePipelineFactory.updateImageBinding(ctx, descriptorSet, binding, image.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
                }
            }

            // Binding 4: Camera UBO
            if (cameraUbo != null) {
                val bufInfo = VkDescriptorBufferInfo.calloc(1, stack)
                bufInfo.get(0).buffer(cameraUbo.buffer).offset(0).range(cameraUbo.size)

                val write = VkWriteDescriptorSet.calloc(1, stack)
                write.get(0)
                    .sType(VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET)
                    .dstSet(descriptorSet)
                    .dstBinding(4)
                    .descriptorCount(1)
                    .descriptorType(VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER)
                    .pBufferInfo(bufInfo)

                vkUpdateDescriptorSets(dev, write, null)
            }

            // Bindings 5-7: SSBOs
            val bufferBindings = listOf(
                5 to vertexBuffer,
                6 to indexBuffer,
                7 to materialBuffer
            )
            for ((binding, buffer) in bufferBindings) {
                if (buffer != null) {
                    val bufInfo = VkDescriptorBufferInfo.calloc(1, stack)
                    bufInfo.get(0).buffer(buffer.buffer).offset(0).range(buffer.size)

                    val write = VkWriteDescriptorSet.calloc(1, stack)
                    write.get(0)
                        .sType(VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET)
                        .dstSet(descriptorSet)
                        .dstBinding(binding)
                        .descriptorCount(1)
                        .descriptorType(VK_DESCRIPTOR_TYPE_STORAGE_BUFFER)
                        .pBufferInfo(bufInfo)

                    vkUpdateDescriptorSets(dev, write, null)
                }
            }
        }
    }

    private var cameraBuffer: VulkanBuffer? = null

    fun updateCamera(
        posX: Float, posY: Float, posZ: Float,
        pitch: Float, yaw: Float, fov: Float,
        nearPlane: Float, farPlane: Float,
        jitterX: Float = 0f, jitterY: Float = 0f
    ) {
        if (cameraBuffer == null) {
            cameraBuffer = VulkanMemory.createBuffer(ctx, 64,
                VK_BUFFER_USAGE_UNIFORM_BUFFER_BIT,
                VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT or VK_MEMORY_PROPERTY_HOST_COHERENT_BIT)
        }

        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            val pData = stack.mallocPointer(1)
            vkMapMemory(dev, cameraBuffer!!.memory, 0, 64, 0, pData)
            val mapped = pData.getByteBuffer(0, 64)
            mapped.putFloat(posX).putFloat(posY).putFloat(posZ).putFloat(fov)
            mapped.putFloat(pitch).putFloat(yaw).putFloat(nearPlane).putFloat(farPlane)
            mapped.putFloat(jitterX).putFloat(jitterY)
            mapped.putFloat(0f).putFloat(0f) // padding
            mapped.putInt(spp).putInt(maxBounces)
            mapped.putInt(0).putInt(0) // reserved
            vkUnmapMemory(dev, cameraBuffer!!.memory)
        }
    }

    fun getCameraBuffer(): VulkanBuffer? = cameraBuffer

    private fun alignUp(value: Int, alignment: Int): Int {
        return (value + alignment - 1) and (alignment - 1).inv()
    }

    fun destroy() {
        val dev = ctx.device ?: return
        if (pipeline != 0L) vkDestroyPipeline(dev, pipeline, null)
        if (pipelineLayout != 0L) vkDestroyPipelineLayout(dev, pipelineLayout, null)
        if (descriptorSetLayout != 0L) vkDestroyDescriptorSetLayout(dev, descriptorSetLayout, null)
        if (descriptorPool != 0L) vkDestroyDescriptorPool(dev, descriptorPool, null)
        if (sbtBuffer != 0L) { vkDestroyBuffer(dev, sbtBuffer, null); vkFreeMemory(dev, sbtMemory, null) }
        cameraBuffer?.let { VulkanMemory.destroyBuffer(ctx, it) }
        cameraBuffer = null
        shaderCompiler.destroy()
        log.info("RT pipeline destroyed")
    }
}
