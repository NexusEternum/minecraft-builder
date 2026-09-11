package com.lumina.renderer.scene

import com.lumina.renderer.rt.AccelerationStructureManager
import com.lumina.renderer.vulkan.VulkanBuffer
import com.lumina.renderer.vulkan.VulkanContext
import com.lumina.renderer.vulkan.VulkanMemory
import com.lumina.scene.graph.MaterialComponent
import com.lumina.scene.graph.MeshComponent
import com.lumina.scene.graph.SceneGraph
import org.lwjgl.system.MemoryUtil
import org.lwjgl.vulkan.KHRAccelerationStructure.VK_BUFFER_USAGE_ACCELERATION_STRUCTURE_BUILD_INPUT_READ_ONLY_BIT_KHR
import org.lwjgl.vulkan.KHRBufferDeviceAddress.VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR
import org.lwjgl.vulkan.VK13.*
import org.slf4j.LoggerFactory
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SceneBufferManager @Inject constructor(
    private val ctx: VulkanContext,
    private val sceneGraph: SceneGraph,
    private val accelStructure: AccelerationStructureManager
) {
    private val log = LoggerFactory.getLogger(SceneBufferManager::class.java)

    var vertexBuffer: VulkanBuffer? = null; private set
    var indexBuffer: VulkanBuffer? = null; private set
    var materialBuffer: VulkanBuffer? = null; private set
    var instanceInfoBuffer: VulkanBuffer? = null; private set

    private var uploadedMeshCount = 0

    fun uploadSceneData() {
        val meshNodes = sceneGraph.nodesWithComponent(MeshComponent::class.java)
        if (meshNodes.isEmpty()) return

        var totalVertexFloats = 0
        var totalIndices = 0
        for (node in meshNodes) {
            val mesh = node.getComponent(MeshComponent::class.java) ?: continue
            totalVertexFloats += mesh.vertexData.size
            totalIndices += mesh.indexData.size
        }

        if (totalVertexFloats == 0) return

        destroyBuffers()

        val vertexSize = totalVertexFloats.toLong() * 4
        val indexSize = totalIndices.toLong() * 4
        val matSize = meshNodes.size.toLong() * 32 // 8 floats (2 vec4s) per material
        val instanceInfoSize = meshNodes.size.toLong() * 4 // one uint indexTriBase per mesh

        val vertBuf = VulkanMemory.createBuffer(ctx, vertexSize,
            VK_BUFFER_USAGE_STORAGE_BUFFER_BIT or VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR or
                    VK_BUFFER_USAGE_ACCELERATION_STRUCTURE_BUILD_INPUT_READ_ONLY_BIT_KHR,
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT or VK_MEMORY_PROPERTY_HOST_COHERENT_BIT)

        val idxBuf = VulkanMemory.createBuffer(ctx, indexSize,
            VK_BUFFER_USAGE_STORAGE_BUFFER_BIT or VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR or
                    VK_BUFFER_USAGE_ACCELERATION_STRUCTURE_BUILD_INPUT_READ_ONLY_BIT_KHR,
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT or VK_MEMORY_PROPERTY_HOST_COHERENT_BIT)

        val matBuf = VulkanMemory.createBuffer(ctx, matSize,
            VK_BUFFER_USAGE_STORAGE_BUFFER_BIT,
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT or VK_MEMORY_PROPERTY_HOST_COHERENT_BIT)

        val instanceInfoBuf = VulkanMemory.createBuffer(ctx, instanceInfoSize,
            VK_BUFFER_USAGE_STORAGE_BUFFER_BIT,
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT or VK_MEMORY_PROPERTY_HOST_COHERENT_BIT)

        val vertData = MemoryUtil.memAlloc(vertexSize.toInt())
        val idxData = MemoryUtil.memAlloc(indexSize.toInt())
        val matData = MemoryUtil.memAlloc(matSize.toInt())
        val instanceInfoData = MemoryUtil.memAlloc(instanceInfoSize.toInt())

        var vertexOffset = 0 // in vertices (not floats)
        var indexOffset = 0  // in indices
        var meshIdx = 0

        data class MeshInfo(val mesh: MeshComponent, val idxByteOffset: Int, val indexTriBase: Int)
        val meshInfos = mutableListOf<MeshInfo>()

        for (node in meshNodes) {
            val mesh = node.getComponent(MeshComponent::class.java) ?: continue
            val mat = node.getComponent(MaterialComponent::class.java) ?: MaterialComponent()

            for (f in mesh.vertexData) vertData.putFloat(f)
            // Global indices: offset by cumulative vertex count so they index into the combined buffer
            for (idx in mesh.indexData) idxData.putInt(idx + vertexOffset)

            matData.putFloat(mat.albedo[0]).putFloat(mat.albedo[1]).putFloat(mat.albedo[2]).putFloat(mat.roughness)
            matData.putFloat(mat.emissive[0]).putFloat(mat.emissive[1]).putFloat(mat.emissive[2]).putFloat(mat.metallic)

            val idxByteOffset = indexOffset * 4
            val indexTriBase = indexOffset / 3
            meshInfos.add(MeshInfo(mesh, idxByteOffset, indexTriBase))

            vertexOffset += mesh.vertexData.size / 8
            indexOffset += mesh.indexData.size
            meshIdx++
        }

        vertData.flip()
        idxData.flip()
        matData.flip()

        // Upload geometry and materials to GPU before building BLAS
        VulkanMemory.uploadBuffer(ctx, vertBuf, vertData)
        VulkanMemory.uploadBuffer(ctx, idxBuf, idxData)
        VulkanMemory.uploadBuffer(ctx, matBuf, matData)

        MemoryUtil.memFree(vertData)
        MemoryUtil.memFree(idxData)
        MemoryUtil.memFree(matData)

        // Build BLAS after data is on the GPU
        for (info in meshInfos) {
            accelStructure.buildBLAS(info.mesh, vertBuf.buffer, idxBuf.buffer, 0, info.idxByteOffset, info.indexTriBase, vertexOffset)
        }

        // Per-mesh indexTriBase for closest-hit shader (uses BLAS entry when geometry is deduplicated)
        for (info in meshInfos) {
            val indexTriBase = accelStructure.getIndexTriBase(info.mesh.blasId)
            instanceInfoData.putInt(indexTriBase)
        }
        instanceInfoData.flip()
        VulkanMemory.uploadBuffer(ctx, instanceInfoBuf, instanceInfoData)
        MemoryUtil.memFree(instanceInfoData)

        vertexBuffer = vertBuf
        indexBuffer = idxBuf
        materialBuffer = matBuf
        instanceInfoBuffer = instanceInfoBuf
        uploadedMeshCount = meshIdx

        log.info("Uploaded scene: {} meshes, {} vertices, {} indices", meshIdx, vertexOffset, indexOffset)
    }

    private fun destroyBuffers() {
        vertexBuffer?.let { VulkanMemory.destroyBuffer(ctx, it) }
        indexBuffer?.let { VulkanMemory.destroyBuffer(ctx, it) }
        materialBuffer?.let { VulkanMemory.destroyBuffer(ctx, it) }
        instanceInfoBuffer?.let { VulkanMemory.destroyBuffer(ctx, it) }
        vertexBuffer = null; indexBuffer = null; materialBuffer = null; instanceInfoBuffer = null
    }

    fun destroy() {
        destroyBuffers()
        log.info("Scene buffer manager destroyed")
    }
}
