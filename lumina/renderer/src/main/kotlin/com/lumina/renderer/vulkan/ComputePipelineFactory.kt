package com.lumina.renderer.vulkan

import org.lwjgl.system.MemoryStack
import org.lwjgl.vulkan.*
import org.lwjgl.vulkan.VK13.*
import org.slf4j.LoggerFactory

data class ComputePipelineBundle(
    val pipeline: Long,
    val pipelineLayout: Long,
    val descriptorSetLayout: Long,
    val descriptorPool: Long,
    val descriptorSet: Long
)

object ComputePipelineFactory {
    private val log = LoggerFactory.getLogger(ComputePipelineFactory::class.java)

    data class BindingDesc(
        val binding: Int,
        val descriptorType: Int,
        val stageFlags: Int = VK_SHADER_STAGE_COMPUTE_BIT,
        val count: Int = 1
    )

    fun create(
        ctx: VulkanContext,
        shaderCompiler: ShaderCompiler,
        shaderPath: String,
        bindings: List<BindingDesc>,
        pushConstantSize: Int = 0,
        maxDescriptorSets: Int = 1
    ): ComputePipelineBundle {
        val dev = ctx.device!!

        val shader = shaderCompiler.compileFromResource(shaderPath, ShaderStage.COMPUTE)

        val descriptorSetLayout: Long
        val pipelineLayout: Long
        val descriptorPool: Long
        val descriptorSet: Long
        val pipeline: Long

        MemoryStack.stackPush().use { stack ->
            val layoutBindings = VkDescriptorSetLayoutBinding.calloc(bindings.size, stack)
            for ((i, b) in bindings.withIndex()) {
                layoutBindings.get(i)
                    .binding(b.binding)
                    .descriptorType(b.descriptorType)
                    .descriptorCount(b.count)
                    .stageFlags(b.stageFlags)
            }

            val layoutInfo = VkDescriptorSetLayoutCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO)
                .pBindings(layoutBindings)

            val pLayout = stack.mallocLong(1)
            check(vkCreateDescriptorSetLayout(dev, layoutInfo, null, pLayout) == VK_SUCCESS)
            descriptorSetLayout = pLayout.get(0)

            val pipelineLayoutInfo = VkPipelineLayoutCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO)
                .pSetLayouts(stack.longs(descriptorSetLayout))

            if (pushConstantSize > 0) {
                val pushRange = VkPushConstantRange.calloc(1, stack)
                pushRange.get(0)
                    .stageFlags(VK_SHADER_STAGE_COMPUTE_BIT)
                    .offset(0)
                    .size(pushConstantSize)
                pipelineLayoutInfo.pPushConstantRanges(pushRange)
            }

            val pPipelineLayout = stack.mallocLong(1)
            check(vkCreatePipelineLayout(dev, pipelineLayoutInfo, null, pPipelineLayout) == VK_SUCCESS)
            pipelineLayout = pPipelineLayout.get(0)

            // Descriptor pool
            val typeCounts = bindings.groupBy { it.descriptorType }
                .map { (type, list) -> type to list.sumOf { it.count } }
            val poolSizes = VkDescriptorPoolSize.calloc(typeCounts.size, stack)
            for ((i, pair) in typeCounts.withIndex()) {
                poolSizes.get(i).type(pair.first).descriptorCount(pair.second * maxDescriptorSets)
            }

            val poolInfo = VkDescriptorPoolCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO)
                .maxSets(maxDescriptorSets)
                .pPoolSizes(poolSizes)

            val pPool = stack.mallocLong(1)
            check(vkCreateDescriptorPool(dev, poolInfo, null, pPool) == VK_SUCCESS)
            descriptorPool = pPool.get(0)

            val allocInfo = VkDescriptorSetAllocateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO)
                .descriptorPool(descriptorPool)
                .pSetLayouts(stack.longs(descriptorSetLayout))

            val pSet = stack.mallocLong(1)
            check(vkAllocateDescriptorSets(dev, allocInfo, pSet) == VK_SUCCESS)
            descriptorSet = pSet.get(0)

            // Compute pipeline
            val stageInfo = VkPipelineShaderStageCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO)
                .stage(VK_SHADER_STAGE_COMPUTE_BIT)
                .module(shader.module)
                .pName(stack.UTF8("main"))

            val computeInfo = VkComputePipelineCreateInfo.calloc(1, stack)
            computeInfo.get(0)
                .sType(VK_STRUCTURE_TYPE_COMPUTE_PIPELINE_CREATE_INFO)
                .stage(stageInfo)
                .layout(pipelineLayout)

            val pPipeline = stack.mallocLong(1)
            check(vkCreateComputePipelines(dev, 0L, computeInfo, null, pPipeline) == VK_SUCCESS)
            pipeline = pPipeline.get(0)
        }

        log.debug("Created compute pipeline for {}", shaderPath)
        return ComputePipelineBundle(pipeline, pipelineLayout, descriptorSetLayout, descriptorPool, descriptorSet)
    }

    fun allocateDescriptorSet(ctx: VulkanContext, bundle: ComputePipelineBundle): Long {
        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            val allocInfo = VkDescriptorSetAllocateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO)
                .descriptorPool(bundle.descriptorPool)
                .pSetLayouts(stack.longs(bundle.descriptorSetLayout))

            val pSet = stack.mallocLong(1)
            check(vkAllocateDescriptorSets(dev, allocInfo, pSet) == VK_SUCCESS)
            return pSet.get(0)
        }
    }

    fun updateImageBinding(ctx: VulkanContext, descriptorSet: Long, binding: Int, imageView: Long, type: Int) {
        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            val imageInfo = VkDescriptorImageInfo.calloc(1, stack)
            imageInfo.get(0)
                .imageView(imageView)
                .imageLayout(VK_IMAGE_LAYOUT_GENERAL)

            val write = VkWriteDescriptorSet.calloc(1, stack)
            write.get(0)
                .sType(VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET)
                .dstSet(descriptorSet)
                .dstBinding(binding)
                .descriptorCount(1)
                .descriptorType(type)
                .pImageInfo(imageInfo)

            vkUpdateDescriptorSets(dev, write, null)
        }
    }

    fun destroy(ctx: VulkanContext, bundle: ComputePipelineBundle) {
        val dev = ctx.device ?: return
        if (bundle.pipeline != 0L) vkDestroyPipeline(dev, bundle.pipeline, null)
        if (bundle.pipelineLayout != 0L) vkDestroyPipelineLayout(dev, bundle.pipelineLayout, null)
        if (bundle.descriptorPool != 0L) vkDestroyDescriptorPool(dev, bundle.descriptorPool, null)
        if (bundle.descriptorSetLayout != 0L) vkDestroyDescriptorSetLayout(dev, bundle.descriptorSetLayout, null)
    }
}
