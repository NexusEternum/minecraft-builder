package com.lumina.renderer.vulkan

import org.lwjgl.system.MemoryStack
import org.lwjgl.util.shaderc.Shaderc.*
import org.lwjgl.vulkan.*
import org.lwjgl.vulkan.VK13.*
import org.slf4j.LoggerFactory
import java.nio.ByteBuffer
import javax.inject.Inject
import javax.inject.Singleton

enum class ShaderStage(val shadercKind: Int, val vkStage: Int) {
    VERTEX(shaderc_vertex_shader, VK_SHADER_STAGE_VERTEX_BIT),
    FRAGMENT(shaderc_fragment_shader, VK_SHADER_STAGE_FRAGMENT_BIT),
    COMPUTE(shaderc_compute_shader, VK_SHADER_STAGE_COMPUTE_BIT),
    RAYGEN(shaderc_raygen_shader, 0x00000100),          // VK_SHADER_STAGE_RAYGEN_BIT_KHR
    CLOSEST_HIT(shaderc_closesthit_shader, 0x00000200), // VK_SHADER_STAGE_CLOSEST_HIT_BIT_KHR
    ANY_HIT(shaderc_anyhit_shader, 0x00000400),         // VK_SHADER_STAGE_ANY_HIT_BIT_KHR
    MISS(shaderc_miss_shader, 0x00000800),               // VK_SHADER_STAGE_MISS_BIT_KHR
}

data class CompiledShader(
    val spirvCode: ByteBuffer,
    val module: Long,
    val stage: ShaderStage
)

@Singleton
class ShaderCompiler @Inject constructor(
    private val ctx: VulkanContext
) {
    private val log = LoggerFactory.getLogger(ShaderCompiler::class.java)
    private var compiler: Long = 0
    private val shaderCache = mutableMapOf<String, CompiledShader>()

    fun init() {
        compiler = shaderc_compiler_initialize()
        check(compiler != 0L) { "Failed to initialize shaderc compiler" }
        log.info("SPIR-V shader compiler initialized")
    }

    fun compileGLSL(
        source: String,
        stage: ShaderStage,
        filename: String,
        entryPoint: String = "main"
    ): CompiledShader {
        shaderCache[filename]?.let { return it }

        val options = shaderc_compile_options_initialize()
        shaderc_compile_options_set_target_env(options, shaderc_target_env_vulkan, shaderc_env_version_vulkan_1_3)
        shaderc_compile_options_set_target_spirv(options, shaderc_spirv_version_1_6)
        shaderc_compile_options_set_optimization_level(options, shaderc_optimization_level_performance)

        val result = shaderc_compile_into_spv(
            compiler, source, stage.shadercKind, filename, entryPoint, options
        )

        val status = shaderc_result_get_compilation_status(result)
        if (status != shaderc_compilation_status_success) {
            val errorMsg = shaderc_result_get_error_message(result)
            shaderc_result_release(result)
            shaderc_compile_options_release(options)
            throw RuntimeException("Shader compilation failed ($filename): $errorMsg")
        }

        val warnings = shaderc_result_get_num_warnings(result)
        if (warnings > 0) {
            log.warn("Shader {} compiled with {} warnings", filename, warnings)
        }

        val spirv = shaderc_result_get_bytes(result)!!
        val module = createShaderModule(spirv)

        val compiled = CompiledShader(spirv, module, stage)
        shaderCache[filename] = compiled

        shaderc_compile_options_release(options)
        log.debug("Compiled shader: {} ({} bytes SPIR-V)", filename, spirv.remaining())

        return compiled
    }

    fun compileFromResource(
        resourcePath: String,
        stage: ShaderStage,
        entryPoint: String = "main"
    ): CompiledShader {
        val source = javaClass.getResourceAsStream(resourcePath)?.bufferedReader()?.readText()
            ?: throw IllegalArgumentException("Shader resource not found: $resourcePath")
        return compileGLSL(source, stage, resourcePath, entryPoint)
    }

    private fun createShaderModule(spirv: ByteBuffer): Long {
        val dev = ctx.device!!
        MemoryStack.stackPush().use { stack ->
            val createInfo = VkShaderModuleCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO)
                .pCode(spirv)

            val pModule = stack.mallocLong(1)
            check(vkCreateShaderModule(dev, createInfo, null, pModule) == VK_SUCCESS)
            return pModule.get(0)
        }
    }

    fun createPipelineShaderStage(
        shader: CompiledShader,
        entryPoint: String = "main",
        stack: MemoryStack
    ): VkPipelineShaderStageCreateInfo {
        return VkPipelineShaderStageCreateInfo.calloc(stack)
            .sType(VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO)
            .stage(shader.stage.vkStage)
            .module(shader.module)
            .pName(stack.UTF8(entryPoint))
    }

    fun destroy() {
        val dev = ctx.device
        if (dev != null) {
            for (shader in shaderCache.values) {
                vkDestroyShaderModule(dev, shader.module, null)
            }
        }
        shaderCache.clear()
        if (compiler != 0L) {
            shaderc_compiler_release(compiler)
        }
        log.info("Shader compiler destroyed ({} cached shaders released)", shaderCache.size)
    }
}
