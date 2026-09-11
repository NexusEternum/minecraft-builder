package com.lumina.renderer.denoise

import com.lumina.renderer.vulkan.*
import org.lwjgl.system.MemoryStack
import org.lwjgl.vulkan.VK13.*
import org.lwjgl.vulkan.VkCommandBuffer
import org.slf4j.LoggerFactory
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SVGFDenoiser @Inject constructor(
    private val ctx: VulkanContext,
    private val shaderCompiler: ShaderCompiler,
    private val renderTargets: RenderTargets
) {
    private val log = LoggerFactory.getLogger(SVGFDenoiser::class.java)

    private var temporalPipeline: ComputePipelineBundle? = null
    private var atrousPipeline: ComputePipelineBundle? = null
    // A-Trous ping-pong: denoiseOutput → bloomScratchA → bloomScratchB → bloomScratchA.
    // denoiseOutput is never overwritten so copyDenoiseHistory still gets the temporal pass result.
    private var atrousDescriptorSetA: Long = 0
    private var atrousDescriptorSetB: Long = 0
    private var atrousDescriptorSetC: Long = 0

    var atrousIterations: Int = 3
    var temporalAlpha: Float = 0.1f
    var momentAlpha: Float = 0.3f
    var sigmaLuminance: Float = 4.0f
    var sigmaNormal: Float = 128.0f
    var sigmaDepth: Float = 1.0f

    private var width: Int = 0
    private var height: Int = 0
    private var frameCount: Long = 0

    fun init(w: Int, h: Int) {
        width = w; height = h
        createTemporalPipeline()
        createAtrousPipeline()
        log.info("SVGF denoiser initialized ({}x{}, {} A-Trous passes)", w, h, atrousIterations)
    }

    private fun createTemporalPipeline() {
        val bindings = listOf(
            ComputePipelineFactory.BindingDesc(0, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // currentColor
            ComputePipelineFactory.BindingDesc(1, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // historyColor
            ComputePipelineFactory.BindingDesc(2, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // normalDepth
            ComputePipelineFactory.BindingDesc(3, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // motionVectors
            ComputePipelineFactory.BindingDesc(4, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // outputColor
            ComputePipelineFactory.BindingDesc(5, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // moments
        )
        temporalPipeline = ComputePipelineFactory.create(
            ctx, shaderCompiler, "/shaders/denoise/svgf_temporal.comp", bindings,
            pushConstantSize = 12 // alpha(4) + momentAlpha(4) + frameCount(4)
        )
    }

    private fun createAtrousPipeline() {
        val bindings = listOf(
            ComputePipelineFactory.BindingDesc(0, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // input
            ComputePipelineFactory.BindingDesc(1, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // normalDepth
            ComputePipelineFactory.BindingDesc(2, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // moments (variance)
            ComputePipelineFactory.BindingDesc(3, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // output
        )
        atrousPipeline = ComputePipelineFactory.create(
            ctx, shaderCompiler, "/shaders/denoise/svgf_atrous.comp", bindings,
            pushConstantSize = 20, // stepSize(4) + sigmaLum(4) + sigmaNorm(4) + sigmaDepth(4) + iteration(4)
            maxDescriptorSets = 3
        )
        val atrous = atrousPipeline!!
        atrousDescriptorSetA = atrous.descriptorSet
        atrousDescriptorSetB = ComputePipelineFactory.allocateDescriptorSet(ctx, atrous)
        atrousDescriptorSetC = ComputePipelineFactory.allocateDescriptorSet(ctx, atrous)
    }

    fun updateDescriptors() {
        val temporal = temporalPipeline ?: return
        val rt = renderTargets

        ComputePipelineFactory.updateImageBinding(ctx, temporal.descriptorSet, 0, rt.rtOutputColor!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, temporal.descriptorSet, 1, rt.denoiseHistory!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, temporal.descriptorSet, 2, rt.rtNormalDepth!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, temporal.descriptorSet, 3, rt.rtMotionVectors!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, temporal.descriptorSet, 4, rt.denoiseOutput!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, temporal.descriptorSet, 5, rt.denoiseMoments!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)

        if (atrousDescriptorSetA == 0L) return
        val normalDepth = rt.rtNormalDepth!!.view
        val moments = rt.denoiseMoments!!.view
        val denoiseOut = rt.denoiseOutput!!.view
        val scratchA = rt.bloomScratchA!!.view
        val scratchB = rt.bloomScratchB!!.view

        // Set A: temporal output → bloomScratchA
        ComputePipelineFactory.updateImageBinding(ctx, atrousDescriptorSetA, 0, denoiseOut, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, atrousDescriptorSetA, 1, normalDepth, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, atrousDescriptorSetA, 2, moments, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, atrousDescriptorSetA, 3, scratchA, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)

        // Set B: bloomScratchA → bloomScratchB
        ComputePipelineFactory.updateImageBinding(ctx, atrousDescriptorSetB, 0, scratchA, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, atrousDescriptorSetB, 1, normalDepth, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, atrousDescriptorSetB, 2, moments, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, atrousDescriptorSetB, 3, scratchB, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)

        // Set C: bloomScratchB → bloomScratchA (final denoised scene for post-process)
        ComputePipelineFactory.updateImageBinding(ctx, atrousDescriptorSetC, 0, scratchB, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, atrousDescriptorSetC, 1, normalDepth, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, atrousDescriptorSetC, 2, moments, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, atrousDescriptorSetC, 3, scratchA, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
    }

    fun recordCommands(cmdBuf: VkCommandBuffer) {
        val temporal = temporalPipeline ?: return
        val atrous = atrousPipeline ?: return

        val groupsX = (width + 15) / 16
        val groupsY = (height + 15) / 16

        // Pass 1: Temporal accumulation
        vkCmdBindPipeline(cmdBuf, VK_PIPELINE_BIND_POINT_COMPUTE, temporal.pipeline)
        MemoryStack.stackPush().use { stack ->
            vkCmdBindDescriptorSets(cmdBuf, VK_PIPELINE_BIND_POINT_COMPUTE,
                temporal.pipelineLayout, 0, stack.longs(temporal.descriptorSet), null)

            val pushData = stack.calloc(12)
            pushData.putFloat(temporalAlpha)
            pushData.putFloat(momentAlpha)
            pushData.putInt(frameCount.toInt())
            pushData.flip()
            vkCmdPushConstants(cmdBuf, temporal.pipelineLayout, VK_SHADER_STAGE_COMPUTE_BIT, 0, pushData)
        }
        vkCmdDispatch(cmdBuf, groupsX, groupsY, 1)

        RenderTargets.insertComputeBarrier(cmdBuf)

        // Passes 2..N: A-Trous wavelet filter (ping-pong across three descriptor sets)
        vkCmdBindPipeline(cmdBuf, VK_PIPELINE_BIND_POINT_COMPUTE, atrous.pipeline)
        val atrousSets = longArrayOf(atrousDescriptorSetA, atrousDescriptorSetB, atrousDescriptorSetC)

        for (i in 0 until atrousIterations) {
            val stepSize = 1 shl i
            MemoryStack.stackPush().use { stack ->
                vkCmdBindDescriptorSets(cmdBuf, VK_PIPELINE_BIND_POINT_COMPUTE,
                    atrous.pipelineLayout, 0, stack.longs(atrousSets[i % atrousSets.size]), null)

                val pushData = stack.calloc(20)
                pushData.putInt(stepSize)
                pushData.putFloat(sigmaLuminance)
                pushData.putFloat(sigmaNormal)
                pushData.putFloat(sigmaDepth)
                pushData.putInt(i)
                pushData.flip()
                vkCmdPushConstants(cmdBuf, atrous.pipelineLayout, VK_SHADER_STAGE_COMPUTE_BIT, 0, pushData)
            }
            vkCmdDispatch(cmdBuf, groupsX, groupsY, 1)

            if (i < atrousIterations - 1) {
                RenderTargets.insertComputeBarrier(cmdBuf)
            }
        }

        frameCount++
    }

    fun resize(w: Int, h: Int) {
        width = w; height = h
        frameCount = 0
    }

    fun destroy() {
        temporalPipeline?.let { ComputePipelineFactory.destroy(ctx, it) }
        atrousPipeline?.let { ComputePipelineFactory.destroy(ctx, it) }
        temporalPipeline = null
        atrousPipeline = null
        atrousDescriptorSetA = 0
        atrousDescriptorSetB = 0
        atrousDescriptorSetC = 0
        log.info("SVGF denoiser destroyed")
    }
}
