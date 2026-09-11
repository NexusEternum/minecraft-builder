package com.lumina.renderer.scene

import com.lumina.renderer.rt.AccelerationStructureManager
import com.lumina.renderer.vulkan.VulkanBuffer
import com.lumina.renderer.vulkan.VulkanContext
import com.lumina.renderer.vulkan.VulkanMemory
import com.lumina.scene.graph.MaterialComponent
import com.lumina.scene.graph.MeshComponent
import com.lumina.scene.graph.SceneGraph
import com.lumina.scene.graph.SceneNode
import com.lumina.scene.graph.Transform
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

    /** TLAS instance records built during the last upload; indexed by [SceneInstanceRecord.instanceIndex]. */
    var instanceRecords: List<SceneInstanceRecord> = emptyList()
        private set

    /**
     * Returns [instanceRecords] for TLAS rebuild after validating they still match the scene graph.
     * A count mismatch means a partial/stale list — caller must not rebuild TLAS from it.
     */
    fun instancesForTlasRebuild(): List<SceneInstanceRecord>? {
        val meshNodes = sceneGraph.nodesWithComponent(MeshComponent::class.java)
        val records = instanceRecords
        if (records.isEmpty()) {
            if (meshNodes.isNotEmpty()) {
                log.error(
                    "TLAS rebuild blocked: {} mesh nodes but instanceRecords empty (upload incomplete?)",
                    meshNodes.size
                )
            }
            return null
        }
        if (records.size != meshNodes.size) {
            log.error(
                "TLAS rebuild blocked: instanceRecords={} vs meshNodes={} — lists must match after upload",
                records.size,
                meshNodes.size
            )
            return null
        }
        return records
    }

    fun uploadSceneData() {
        val uploadStartNs = System.nanoTime()
        val meshNodes = sceneGraph.nodesWithComponent(MeshComponent::class.java)
        if (meshNodes.isEmpty()) {
            log.warn("uploadSceneData: scene has no mesh nodes")
            return
        }

        destroyBuffers()
        // TODO: content-key BLAS cache (modelId+orientation) across scene reloads requires persisting
        // GPU vertex/index buffers for unchanged meshes; clearBlasCache() forces full BLAS rebuild today.
        val blasClearStartNs = System.nanoTime()
        accelStructure.clearBlasCache()
        val blasClearMs = (System.nanoTime() - blasClearStartNs) / 1_000_000

        if (meshNodes.size >= INSTANCE_WARN_THRESHOLD) {
            log.warn(
                "Scene has {} mesh nodes (warn threshold {}); verify instancing dedup is working",
                meshNodes.size,
                INSTANCE_WARN_THRESHOLD
            )
        }
        if (meshNodes.size > MAX_TLAS_INSTANCES) {
            log.error(
                "Scene mesh node count {} exceeds MAX_TLAS_INSTANCES {}; truncating TLAS instances",
                meshNodes.size,
                MAX_TLAS_INSTANCES
            )
        }

        val instanceNodes = meshNodes.take(MAX_TLAS_INSTANCES)
        val skippedInstances = meshNodes.size - instanceNodes.size
        if (skippedInstances > 0) {
            log.warn("Skipped {} scene nodes due to TLAS instance cap", skippedInstances)
        }

        data class UniqueMeshSlot(
            val mesh: MeshComponent,
            val indexTriBase: Int,
            val idxByteOffset: Int,
            val vertexOffset: Int
        )

        val uniqueMeshes = LinkedHashMap<MeshComponent, UniqueMeshSlot>()
        var totalVertexFloats = 0
        var totalIndices = 0
        var vertexOffset = 0
        var indexOffset = 0

        for (node in instanceNodes) {
            val mesh = node.getComponent(MeshComponent::class.java) ?: continue
            if (uniqueMeshes.containsKey(mesh)) continue

            uniqueMeshes[mesh] = UniqueMeshSlot(
                mesh = mesh,
                indexTriBase = indexOffset / 3,
                idxByteOffset = indexOffset * 4,
                vertexOffset = vertexOffset
            )
            totalVertexFloats += mesh.vertexData.size
            totalIndices += mesh.indexData.size
            vertexOffset += mesh.vertexData.size / FLOATS_PER_VERTEX
            indexOffset += mesh.indexData.size
        }

        if (totalVertexFloats == 0) return

        val instanceCount = instanceNodes.size
        val vertexSize = totalVertexFloats.toLong() * 4
        val indexSize = totalIndices.toLong() * 4
        val matSize = instanceCount.toLong() * 32
        val instanceInfoSize = instanceCount.toLong() * 4

        val vertBuf = VulkanMemory.createBuffer(
            ctx, vertexSize,
            VK_BUFFER_USAGE_STORAGE_BUFFER_BIT or VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR or
                VK_BUFFER_USAGE_ACCELERATION_STRUCTURE_BUILD_INPUT_READ_ONLY_BIT_KHR,
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT or VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
        )
        val idxBuf = VulkanMemory.createBuffer(
            ctx, indexSize,
            VK_BUFFER_USAGE_STORAGE_BUFFER_BIT or VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR or
                VK_BUFFER_USAGE_ACCELERATION_STRUCTURE_BUILD_INPUT_READ_ONLY_BIT_KHR,
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT or VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
        )
        val matBuf = VulkanMemory.createBuffer(
            ctx, matSize,
            VK_BUFFER_USAGE_STORAGE_BUFFER_BIT,
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT or VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
        )
        val instanceInfoBuf = VulkanMemory.createBuffer(
            ctx, instanceInfoSize,
            VK_BUFFER_USAGE_STORAGE_BUFFER_BIT,
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT or VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
        )

        val vertData = MemoryUtil.memAlloc(vertexSize.toInt())
        val idxData = MemoryUtil.memAlloc(indexSize.toInt())
        val matData = MemoryUtil.memAlloc(matSize.toInt())
        val instanceInfoData = MemoryUtil.memAlloc(instanceInfoSize.toInt())

        var uploadVertexOffset = 0
        for ((_, slot) in uniqueMeshes) {
            val mesh = slot.mesh
            for (f in mesh.vertexData) vertData.putFloat(f)
            for (idx in mesh.indexData) idxData.putInt(idx + uploadVertexOffset)
            uploadVertexOffset += mesh.vertexData.size / FLOATS_PER_VERTEX
        }

        data class PendingInstance(
            val node: SceneNode,
            val slot: UniqueMeshSlot,
            val transform: Transform,
            val instanceIndex: Int
        )
        val pendingInstances = ArrayList<PendingInstance>(instanceCount)
        var instanceIdx = 0
        for (node in instanceNodes) {
            val mesh = node.getComponent(MeshComponent::class.java) ?: continue
            val mat = node.getComponent(MaterialComponent::class.java) ?: MaterialComponent()
            val transform = node.getComponent(Transform::class.java) ?: Transform()
            val slot = uniqueMeshes[mesh]
            if (slot == null) {
                log.warn("Instance {} node={} references mesh not in unique table; skipping", instanceIdx, node.name)
                continue
            }

            matData.putFloat(mat.albedo[0]).putFloat(mat.albedo[1]).putFloat(mat.albedo[2]).putFloat(mat.roughness)
            matData.putFloat(mat.emissive[0]).putFloat(mat.emissive[1]).putFloat(mat.emissive[2]).putFloat(mat.metallic)
            instanceInfoData.putInt(slot.indexTriBase)
            pendingInstances.add(PendingInstance(node, slot, transform, instanceIdx))
            instanceIdx++
        }

        vertData.flip()
        idxData.flip()
        matData.flip()
        instanceInfoData.flip()

        VulkanMemory.uploadBuffer(ctx, vertBuf, vertData)
        VulkanMemory.uploadBuffer(ctx, idxBuf, idxData)
        VulkanMemory.uploadBuffer(ctx, matBuf, matData)
        VulkanMemory.uploadBuffer(ctx, instanceInfoBuf, instanceInfoData)

        val records = ArrayList<SceneInstanceRecord>(pendingInstances.size)
        val blasBuildStartNs = System.nanoTime()
        for (pending in pendingInstances) {
            val blasId = accelStructure.buildBLAS(
                pending.slot.mesh,
                vertBuf.buffer,
                idxBuf.buffer,
                0,
                pending.slot.idxByteOffset,
                pending.slot.indexTriBase,
                uploadVertexOffset
            )
            if (blasId < 0) {
                log.warn("BLAS build failed for instance {} node={}", pending.instanceIndex, pending.node.name)
                continue
            }
            records.add(
                SceneInstanceRecord(
                    instanceIndex = pending.instanceIndex,
                    blasId = blasId,
                    indexTriBase = pending.slot.indexTriBase,
                    transform = pending.transform,
                    nodeName = pending.node.name
                )
            )
            log.info(
                "instance[{}] {} meshSlot triBase={} uniqueMeshes={} blas={}",
                pending.instanceIndex,
                pending.node.name,
                pending.slot.indexTriBase,
                uniqueMeshes.size,
                blasId
            )
        }

        val blasBuildMs = (System.nanoTime() - blasBuildStartNs) / 1_000_000

        MemoryUtil.memFree(vertData)
        MemoryUtil.memFree(idxData)
        MemoryUtil.memFree(matData)
        MemoryUtil.memFree(instanceInfoData)

        vertexBuffer = vertBuf
        indexBuffer = idxBuf
        materialBuffer = matBuf
        instanceInfoBuffer = instanceInfoBuf
        instanceRecords = records
        sceneGraph.markDirty(immediateTlasRebuild = true)

        val uploadMs = (System.nanoTime() - uploadStartNs) / 1_000_000
        if (records.size != instanceCount) {
            log.error(
                "Upload instance mismatch: {} mesh nodes, {} TLAS records ({} BLAS failures) — " +
                    "some objects will not render until re-upload",
                instanceCount,
                records.size,
                instanceCount - records.size
            )
        }

        log.info(
            "Uploaded scene: {} TLAS instances, {} unique meshes, {} vertices, {} indices " +
                "(upload {} ms, BLAS clear {} ms, BLAS build {} ms)",
            records.size,
            uniqueMeshes.size,
            uploadVertexOffset,
            totalIndices,
            uploadMs,
            blasClearMs,
            blasBuildMs
        )
    }

    private fun destroyBuffers() {
        vertexBuffer?.let { VulkanMemory.destroyBuffer(ctx, it) }
        indexBuffer?.let { VulkanMemory.destroyBuffer(ctx, it) }
        materialBuffer?.let { VulkanMemory.destroyBuffer(ctx, it) }
        instanceInfoBuffer?.let { VulkanMemory.destroyBuffer(ctx, it) }
        vertexBuffer = null
        indexBuffer = null
        materialBuffer = null
        instanceInfoBuffer = null
        instanceRecords = emptyList()
    }

    fun destroy() {
        destroyBuffers()
        log.info("Scene buffer manager destroyed")
    }

    companion object {
        private const val FLOATS_PER_VERTEX = 8
        /** Vulkan instanceCustomIndex is 24-bit; never wrap — skip and log beyond this. */
        const val MAX_TLAS_INSTANCES = 0xFFFFFF
        const val INSTANCE_WARN_THRESHOLD = 8000
    }
}
