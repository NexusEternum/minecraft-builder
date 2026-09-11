package com.lumina.renderer.postfx

import com.lumina.renderer.vulkan.*
import org.lwjgl.system.MemoryStack
import org.lwjgl.vulkan.VK13.*
import org.lwjgl.vulkan.VkCommandBuffer
import org.slf4j.LoggerFactory
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class PostProcessStack @Inject constructor(
    private val ctx: VulkanContext,
    private val shaderCompiler: ShaderCompiler,
    private val renderTargets: RenderTargets
) {
    private val log = LoggerFactory.getLogger(PostProcessStack::class.java)

    var bloomEnabled: Boolean = true
    var bloomIntensity: Float = 0.5f
    var bloomThreshold: Float = 1.0f

    var volumetricFogEnabled: Boolean = true
    var fogDensity: Float = 0.004f
    var fogColor: FloatArray = floatArrayOf(0.7f, 0.75f, 0.85f)
    var fogHeight: Float = 50.0f

    var godRaysEnabled: Boolean = true
    var godRayIntensity: Float = 0.4f
    var scatteringCoeff: Float = 0.1f
    var volumetricSteps: Int = 64

    var sunDirection: FloatArray = floatArrayOf(0.3f, 0.8f, 0.5f)
    var sunColor: FloatArray = floatArrayOf(1.0f, 0.95f, 0.85f)

    var toneMappingMode: ToneMapMode = ToneMapMode.AGX
    var exposure: Float = 1.0f
    var gamma: Float = 2.2f

    var timeOfDay: Float = 0.5f

    enum class ToneMapMode(val modeIndex: Int) { AGX(0), ACES(1), REINHARD(2), NONE(3) }

    private var bloomPipeline: ComputePipelineBundle? = null
    private var volumetricPipeline: ComputePipelineBundle? = null
    private var tonemapPipeline: ComputePipelineBundle? = null

    private var width: Int = 0
    private var height: Int = 0

    fun init(w: Int, h: Int) {
        width = w; height = h
        createBloomPipeline()
        createVolumetricPipeline()
        createTonemapPipeline()
        log.info("Post-process stack initialized ({}x{}, bloom={}, volumetric={}, tonemap={})",
            w, h, bloomEnabled, volumetricFogEnabled, toneMappingMode)
    }

    private fun createBloomPipeline() {
        val bindings = listOf(
            ComputePipelineFactory.BindingDesc(0, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // sceneColor
            ComputePipelineFactory.BindingDesc(1, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // bloomTexA
            ComputePipelineFactory.BindingDesc(2, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // bloomTexB
        )
        bloomPipeline = ComputePipelineFactory.create(
            ctx, shaderCompiler, "/shaders/postfx/bloom_simple.comp", bindings,
            pushConstantSize = 12 // mode(4) + threshold(4) + intensity(4)
        )
    }

    private fun createVolumetricPipeline() {
        val bindings = listOf(
            ComputePipelineFactory.BindingDesc(0, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // sceneColor
            ComputePipelineFactory.BindingDesc(1, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // depthBuffer
            ComputePipelineFactory.BindingDesc(2, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // output
            ComputePipelineFactory.BindingDesc(3, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // bloomTexA
        )
        volumetricPipeline = ComputePipelineFactory.create(
            ctx, shaderCompiler, "/shaders/postfx/volumetric.comp", bindings,
            pushConstantSize = 64 // sunDir(12)+fogDens(4)+fogColor(12)+fogH(4)+sunCol(12)+godRay(4)+numSteps(4)+scatter(4)+time(4)+bloomIntensity(4)
        )
    }

    private fun createTonemapPipeline() {
        val bindings = listOf(
            ComputePipelineFactory.BindingDesc(0, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // input
            ComputePipelineFactory.BindingDesc(1, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // output
        )
        tonemapPipeline = ComputePipelineFactory.create(
            ctx, shaderCompiler, "/shaders/postfx/tonemap.comp", bindings,
            pushConstantSize = 12 // mode(4) + exposure(4) + gamma(4)
        )
    }

    fun updateTonemapDescriptors(inputImage: VulkanImage, outputImage: VulkanImage) {
        val tonemap = tonemapPipeline ?: return
        ComputePipelineFactory.updateImageBinding(ctx, tonemap.descriptorSet, 0, inputImage.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, tonemap.descriptorSet, 1, outputImage.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
    }

    fun recordTonemapOnly(cmdBuf: VkCommandBuffer, displayW: Int, displayH: Int) {
        recordTonemap(cmdBuf, width, height)
    }

    fun updateDescriptors(inputImage: VulkanImage, depthImage: VulkanImage, outputImage: VulkanImage) {
        val bloom = bloomPipeline ?: return
        val vol = volumetricPipeline ?: return
        val tonemap = tonemapPipeline ?: return
        val rt = renderTargets

        ComputePipelineFactory.updateImageBinding(ctx, bloom.descriptorSet, 0, inputImage.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, bloom.descriptorSet, 1, rt.bloomTexA!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, bloom.descriptorSet, 2, rt.bloomTexB!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)

        ComputePipelineFactory.updateImageBinding(ctx, vol.descriptorSet, 0, inputImage.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, vol.descriptorSet, 1, depthImage.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, vol.descriptorSet, 2, rt.postfxOutput!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, vol.descriptorSet, 3, rt.bloomTexA!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)

        ComputePipelineFactory.updateImageBinding(ctx, tonemap.descriptorSet, 0, rt.postfxOutput!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, tonemap.descriptorSet, 1, outputImage.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
    }

    fun recordCommands(cmdBuf: VkCommandBuffer, displayWidth: Int, displayHeight: Int) {
        val groupsX = (width + 15) / 16
        val groupsY = (height + 15) / 16

        if (bloomEnabled) {
            recordBloom(cmdBuf, groupsX, groupsY)
            RenderTargets.insertComputeBarrier(cmdBuf)
        }

        if (volumetricFogEnabled) {
            recordVolumetric(cmdBuf)
            RenderTargets.insertComputeBarrier(cmdBuf)
        }

        recordTonemap(cmdBuf, displayWidth, displayHeight)
    }

    private fun recordBloom(cmdBuf: VkCommandBuffer, groupsX: Int, groupsY: Int) {
        val bloom = bloomPipeline ?: return
        vkCmdBindPipeline(cmdBuf, VK_PIPELINE_BIND_POINT_COMPUTE, bloom.pipeline)

        MemoryStack.stackPush().use { stack ->
            vkCmdBindDescriptorSets(cmdBuf, VK_PIPELINE_BIND_POINT_COMPUTE,
                bloom.pipelineLayout, 0, stack.longs(bloom.descriptorSet), null)

            for (mode in 0..2) {
                val pushData = stack.calloc(12)
                pushData.putInt(mode)
                pushData.putFloat(bloomThreshold)
                pushData.putFloat(bloomIntensity)
                pushData.flip()
                vkCmdPushConstants(cmdBuf, bloom.pipelineLayout, VK_SHADER_STAGE_COMPUTE_BIT, 0, pushData)
                vkCmdDispatch(cmdBuf, groupsX, groupsY, 1)
                if (mode < 2) RenderTargets.insertComputeBarrier(cmdBuf)
            }
        }
    }

    private fun recordVolumetric(cmdBuf: VkCommandBuffer) {
        val vol = volumetricPipeline ?: return
        val groupsX = (width + 7) / 8
        val groupsY = (height + 7) / 8

        vkCmdBindPipeline(cmdBuf, VK_PIPELINE_BIND_POINT_COMPUTE, vol.pipeline)
        MemoryStack.stackPush().use { stack ->
            vkCmdBindDescriptorSets(cmdBuf, VK_PIPELINE_BIND_POINT_COMPUTE,
                vol.pipelineLayout, 0, stack.longs(vol.descriptorSet), null)

            val pushData = stack.calloc(64)
            pushData.putFloat(sunDirection[0])
            pushData.putFloat(sunDirection[1])
            pushData.putFloat(sunDirection[2])
            pushData.putFloat(fogDensity)
            pushData.putFloat(fogColor[0])
            pushData.putFloat(fogColor[1])
            pushData.putFloat(fogColor[2])
            pushData.putFloat(fogHeight)
            pushData.putFloat(sunColor[0])
            pushData.putFloat(sunColor[1])
            pushData.putFloat(sunColor[2])
            pushData.putFloat(godRayIntensity)
            pushData.putInt(volumetricSteps)
            pushData.putFloat(scatteringCoeff)
            pushData.putFloat(timeOfDay)
            pushData.putFloat(if (bloomEnabled) bloomIntensity else 0f)
            pushData.flip()
            vkCmdPushConstants(cmdBuf, vol.pipelineLayout, VK_SHADER_STAGE_COMPUTE_BIT, 0, pushData)
        }
        vkCmdDispatch(cmdBuf, groupsX, groupsY, 1)
    }

    private fun recordTonemap(cmdBuf: VkCommandBuffer, displayW: Int, displayH: Int) {
        val tonemap = tonemapPipeline ?: return
        val groupsX = (displayW + 15) / 16
        val groupsY = (displayH + 15) / 16

        vkCmdBindPipeline(cmdBuf, VK_PIPELINE_BIND_POINT_COMPUTE, tonemap.pipeline)
        MemoryStack.stackPush().use { stack ->
            vkCmdBindDescriptorSets(cmdBuf, VK_PIPELINE_BIND_POINT_COMPUTE,
                tonemap.pipelineLayout, 0, stack.longs(tonemap.descriptorSet), null)

            val pushData = stack.calloc(12)
            pushData.putInt(toneMappingMode.modeIndex)
            pushData.putFloat(exposure)
            pushData.putFloat(gamma)
            pushData.flip()
            vkCmdPushConstants(cmdBuf, tonemap.pipelineLayout, VK_SHADER_STAGE_COMPUTE_BIT, 0, pushData)
        }
        vkCmdDispatch(cmdBuf, groupsX, groupsY, 1)
    }

    fun resize(w: Int, h: Int) {
        width = w; height = h
    }

    fun destroy() {
        bloomPipeline?.let { ComputePipelineFactory.destroy(ctx, it) }
        volumetricPipeline?.let { ComputePipelineFactory.destroy(ctx, it) }
        tonemapPipeline?.let { ComputePipelineFactory.destroy(ctx, it) }
        bloomPipeline = null; volumetricPipeline = null; tonemapPipeline = null
        log.info("Post-process stack destroyed")
    }
}
