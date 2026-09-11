package com.lumina.renderer.upscale

import com.lumina.renderer.vulkan.*
import org.lwjgl.system.MemoryStack
import org.lwjgl.vulkan.VK13.*
import org.lwjgl.vulkan.VkCommandBuffer
import org.slf4j.LoggerFactory
import javax.inject.Inject
import javax.inject.Singleton

enum class UpscaleMode { NONE, FSR2, DLSS }

enum class UpscaleQuality(val renderScale: Float) {
    ULTRA_PERFORMANCE(0.33f),
    PERFORMANCE(0.5f),
    BALANCED(0.67f),
    QUALITY(0.77f),
    NATIVE(1.0f)
}

@Singleton
class UpscaleManager @Inject constructor(
    private val ctx: VulkanContext,
    private val shaderCompiler: ShaderCompiler,
    private val renderTargets: RenderTargets
) {
    private val log = LoggerFactory.getLogger(UpscaleManager::class.java)

    var mode: UpscaleMode = UpscaleMode.FSR2
    var quality: UpscaleQuality = UpscaleQuality.QUALITY
    var sharpness: Float = 0.5f
    var dlssAvailable: Boolean = false; private set

    val renderWidth: Int get() = (ctx.width * quality.renderScale).toInt().coerceAtLeast(1)
    val renderHeight: Int get() = (ctx.height * quality.renderScale).toInt().coerceAtLeast(1)

    private var fsr2Pipeline: ComputePipelineBundle? = null
    private var frameIndex: Long = 0

    private var jitterX: Float = 0f
    private var jitterY: Float = 0f

    fun init() {
        dlssAvailable = checkDLSSSupport()
        if (mode == UpscaleMode.DLSS && !dlssAvailable) {
            log.warn("DLSS not available, falling back to FSR 2.0")
            mode = UpscaleMode.FSR2
        }

        if (mode == UpscaleMode.FSR2) {
            createFSR2Pipeline()
        }

        log.info("Upscaling: {} {} (render: {}x{} -> {}x{})",
            mode, quality, renderWidth, renderHeight, ctx.width, ctx.height)
    }

    private fun checkDLSSSupport(): Boolean = false

    private fun createFSR2Pipeline() {
        val bindings = listOf(
            ComputePipelineFactory.BindingDesc(0, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // inputColor
            ComputePipelineFactory.BindingDesc(1, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // inputDepth
            ComputePipelineFactory.BindingDesc(2, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // motionVectors
            ComputePipelineFactory.BindingDesc(3, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // historyColor
            ComputePipelineFactory.BindingDesc(4, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE), // outputColor
        )
        fsr2Pipeline = ComputePipelineFactory.create(
            ctx, shaderCompiler, "/shaders/upscale/fsr2.comp", bindings,
            pushConstantSize = 36 // inputSize(8)+outputSize(8)+jitter(8)+sharpness(4)+dt(4)+frameIdx(4)
        )
    }

    fun updateDescriptors() {
        val fsr2 = fsr2Pipeline ?: return
        val rt = renderTargets

        ComputePipelineFactory.updateImageBinding(ctx, fsr2.descriptorSet, 0, rt.denoiseOutput!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, fsr2.descriptorSet, 1, rt.rtNormalDepth!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, fsr2.descriptorSet, 2, rt.rtMotionVectors!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, fsr2.descriptorSet, 3, rt.upscaleHistory!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
        ComputePipelineFactory.updateImageBinding(ctx, fsr2.descriptorSet, 4, rt.upscaleOutput!!.view, VK_DESCRIPTOR_TYPE_STORAGE_IMAGE)
    }

    fun updateJitter() {
        val haltonBase2 = halton(frameIndex.toInt() + 1, 2)
        val haltonBase3 = halton(frameIndex.toInt() + 1, 3)
        jitterX = (haltonBase2 - 0.5f) / renderWidth
        jitterY = (haltonBase3 - 0.5f) / renderHeight
    }

    fun getJitterX(): Float = jitterX
    fun getJitterY(): Float = jitterY

    fun recordCommands(cmdBuf: VkCommandBuffer, deltaTime: Float) {
        if (mode == UpscaleMode.NONE) return
        val fsr2 = fsr2Pipeline ?: return

        val outputW = ctx.width
        val outputH = ctx.height
        val groupsX = (outputW + 15) / 16
        val groupsY = (outputH + 15) / 16

        vkCmdBindPipeline(cmdBuf, VK_PIPELINE_BIND_POINT_COMPUTE, fsr2.pipeline)
        MemoryStack.stackPush().use { stack ->
            vkCmdBindDescriptorSets(cmdBuf, VK_PIPELINE_BIND_POINT_COMPUTE,
                fsr2.pipelineLayout, 0, stack.longs(fsr2.descriptorSet), null)

            val pushData = stack.calloc(36)
            pushData.putInt(renderWidth)
            pushData.putInt(renderHeight)
            pushData.putInt(outputW)
            pushData.putInt(outputH)
            pushData.putFloat(jitterX)
            pushData.putFloat(jitterY)
            pushData.putFloat(sharpness)
            pushData.putFloat(deltaTime)
            pushData.putInt(frameIndex.toInt())
            pushData.flip()
            vkCmdPushConstants(cmdBuf, fsr2.pipelineLayout, VK_SHADER_STAGE_COMPUTE_BIT, 0, pushData)
        }
        vkCmdDispatch(cmdBuf, groupsX, groupsY, 1)
        frameIndex++
    }

    private fun halton(index: Int, base: Int): Float {
        var result = 0.0f
        var f = 1.0f / base
        var i = index
        while (i > 0) {
            result += f * (i % base)
            i /= base
            f /= base
        }
        return result
    }

    fun destroy() {
        fsr2Pipeline?.let { ComputePipelineFactory.destroy(ctx, it) }
        fsr2Pipeline = null
        log.info("Upscale manager destroyed")
    }
}
