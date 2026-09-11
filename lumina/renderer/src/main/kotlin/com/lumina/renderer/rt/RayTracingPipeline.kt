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

    var spp: Int = 8
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
            val bindings = VkDescriptorSetLayoutBinding.calloc(9, stack)

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
                .stageFlags(VK_SHADER_STAGE_RAYGEN_BIT_KHR or VK_SHADER_STAGE_MISS_BIT_KHR or VK_SHADER_STAGE_CLOSEST_HIT_BIT_KHR)

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

            // Binding 8: Per-instance indexTriBase SSBO
            bindings.get(8).binding(8)
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
            poolSizes.get(3).type(VK_DESCRIPTOR_TYPE_STORAGE_BUFFER).descriptorCount(4)

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

            // Raygen handle (group 0) at SBT offset 0
            mapped.position(0)
            for (i in 0 until handleSize) mapped.put(handleData.get(i))

            // Miss handles (groups 2,3) at SBT offset raygenSize
            mapped.position(raygenSize.toInt())
            for (i in 0 until handleSize) mapped.put(handleData.get(handleSize * 2 + i))

            mapped.position((raygenSize + alignedHandleSize).toInt())
            for (i in 0 until handleSize) mapped.put(handleData.get(handleSize * 3 + i))

            // Hit handle (group 1) at SBT offset raygenSize + missSize
            mapped.position((raygenSize + missSize).toInt())
            for (i in 0 until handleSize) mapped.put(handleData.get(handleSize + i))

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
                          materialBuffer: VulkanBuffer? = null, instanceInfoBuffer: VulkanBuffer? = null) {
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

            // Bindings 5-8: SSBOs
            val bufferBindings = listOf(
                5 to vertexBuffer,
                6 to indexBuffer,
                7 to materialBuffer,
                8 to instanceInfoBuffer
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
    private var frameCount: Long = 0
    private val prevViewProj = FloatArray(16) { if (it % 5 == 0) 1f else 0f }

    fun updateCamera(
        posX: Float, posY: Float, posZ: Float,
        pitch: Float, yaw: Float, fov: Float,
        nearPlane: Float, farPlane: Float,
        jitterX: Float = 0f, jitterY: Float = 0f
    ) {
        val bufSize = 224L // 3 mat4(192) + vec3(12) + float(4) + 3 uint(12) + float(4) = 224
        if (cameraBuffer == null) {
            cameraBuffer = VulkanMemory.createBuffer(ctx, bufSize,
                VK_BUFFER_USAGE_UNIFORM_BUFFER_BIT,
                VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT or VK_MEMORY_PROPERTY_HOST_COHERENT_BIT)
        }

        val aspect = ctx.width.toFloat() / ctx.height.toFloat().coerceAtLeast(1f)
        val fovRad = Math.toRadians(fov.toDouble()).toFloat()

        val viewInv = computeViewInverse(posX, posY, posZ, pitch, yaw)
        val projInv = computeProjInverse(fovRad, aspect, nearPlane, farPlane)

        val view = invertMat4(viewInv)
        val proj = invertMat4(projInv)
        val viewProj = multiplyMat4(proj, view)

        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            val pData = stack.mallocPointer(1)
            vkMapMemory(dev, cameraBuffer!!.memory, 0, bufSize, 0, pData)
            val mapped = pData.getByteBuffer(0, bufSize.toInt())

            for (f in viewInv) mapped.putFloat(f)
            for (f in projInv) mapped.putFloat(f)
            for (f in prevViewProj) mapped.putFloat(f)
            mapped.putFloat(posX).putFloat(posY).putFloat(posZ)
            mapped.putFloat(fov)
            mapped.putInt(frameCount.toInt())
            mapped.putInt(spp)
            mapped.putInt(maxBounces)
            mapped.putFloat(0.5f) // time (default noon)

            vkUnmapMemory(dev, cameraBuffer!!.memory)
        }

        System.arraycopy(viewProj, 0, prevViewProj, 0, 16)
        frameCount++
    }

    private fun computeViewInverse(px: Float, py: Float, pz: Float, pitch: Float, yaw: Float): FloatArray {
        val cp = kotlin.math.cos(pitch); val sp = kotlin.math.sin(pitch)
        val cy = kotlin.math.cos(yaw);   val sy = kotlin.math.sin(yaw)

        // Column-major: R_yaw * R_pitch, then translate by position
        return floatArrayOf(
            cy,      sp * sy,   -cp * sy, 0f,
            0f,      cp,         sp,      0f,
            sy,     -sp * cy,    cp * cy, 0f,
            px,      py,         pz,      1f
        )
    }

    private fun computeProjInverse(fovRad: Float, aspect: Float, near: Float, far: Float): FloatArray {
        val tanHalfFov = kotlin.math.tan(fovRad * 0.5f)
        val a = 1f / (aspect * tanHalfFov)
        val b = 1f / tanHalfFov
        val c = -(far + near) / (far - near)
        val d = -(2f * far * near) / (far - near)
        // Inverse of perspective projection (column-major)
        return floatArrayOf(
            1f / a, 0f,     0f,     0f,
            0f,     1f / b, 0f,     0f,
            0f,     0f,     0f,     1f / d,
            0f,     0f,     -1f,    c / d
        )
    }

    private fun invertMat4(m: FloatArray): FloatArray {
        // For view inverse: input IS the inverse, so invert it to get the forward matrix
        val inv = FloatArray(16)
        val m00=m[0]; val m01=m[4]; val m02=m[8];  val m03=m[12]
        val m10=m[1]; val m11=m[5]; val m12=m[9];  val m13=m[13]
        val m20=m[2]; val m21=m[6]; val m22=m[10]; val m23=m[14]
        val m30=m[3]; val m31=m[7]; val m32=m[11]; val m33=m[15]

        val a2323 = m22*m33 - m23*m32; val a1323 = m21*m33 - m23*m31
        val a1223 = m21*m32 - m22*m31; val a0323 = m20*m33 - m23*m30
        val a0223 = m20*m32 - m22*m30; val a0123 = m20*m31 - m21*m30
        val a2313 = m12*m33 - m13*m32; val a1313 = m11*m33 - m13*m31
        val a1213 = m11*m32 - m12*m31; val a2312 = m12*m23 - m13*m22
        val a1312 = m11*m23 - m13*m21; val a1212 = m11*m22 - m12*m21
        val a0313 = m10*m33 - m13*m30; val a0213 = m10*m32 - m12*m30
        val a0312 = m10*m23 - m13*m20; val a0212 = m10*m22 - m12*m20
        val a0113 = m10*m31 - m11*m30; val a0112 = m10*m21 - m11*m20

        var det = m00*(m11*a2323 - m12*a1323 + m13*a1223) -
                  m01*(m10*a2323 - m12*a0323 + m13*a0223) +
                  m02*(m10*a1323 - m11*a0323 + m13*a0123) -
                  m03*(m10*a1223 - m11*a0223 + m12*a0123)
        if (kotlin.math.abs(det) < 1e-10f) return FloatArray(16) { if (it % 5 == 0) 1f else 0f }
        det = 1f / det

        inv[0] = det *  (m11*a2323 - m12*a1323 + m13*a1223)
        inv[1] = det * -(m10*a2323 - m12*a0323 + m13*a0223)
        inv[2] = det *  (m10*a1323 - m11*a0323 + m13*a0123)
        inv[3] = det * -(m10*a1223 - m11*a0223 + m12*a0123)
        inv[4] = det * -(m01*a2323 - m02*a1323 + m03*a1223)
        inv[5] = det *  (m00*a2323 - m02*a0323 + m03*a0223)
        inv[6] = det * -(m00*a1323 - m01*a0323 + m03*a0123)
        inv[7] = det *  (m00*a1223 - m01*a0223 + m02*a0123)
        inv[8] = det *  (m01*a2313 - m02*a1313 + m03*a1213)
        inv[9] = det * -(m00*a2313 - m02*a0313 + m03*a0213)
        inv[10]= det *  (m00*a1313 - m01*a0313 + m03*a0113)
        inv[11]= det * -(m00*a1213 - m01*a0213 + m02*a0113)
        inv[12]= det * -(m01*a2312 - m02*a1312 + m03*a1212)
        inv[13]= det *  (m00*a2312 - m02*a0312 + m03*a0212)
        inv[14]= det * -(m00*a1312 - m01*a0312 + m03*a0112)
        inv[15]= det *  (m00*a1212 - m01*a0212 + m02*a0112)
        return inv
    }

    private fun multiplyMat4(a: FloatArray, b: FloatArray): FloatArray {
        val r = FloatArray(16)
        for (col in 0..3) for (row in 0..3) {
            r[col * 4 + row] = a[row] * b[col * 4] + a[4 + row] * b[col * 4 + 1] +
                               a[8 + row] * b[col * 4 + 2] + a[12 + row] * b[col * 4 + 3]
        }
        return r
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
        log.info("RT pipeline destroyed")
    }
}
