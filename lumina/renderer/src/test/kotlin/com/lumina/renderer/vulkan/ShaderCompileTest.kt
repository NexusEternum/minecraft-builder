package com.lumina.renderer.vulkan

import org.junit.jupiter.api.Assertions.assertNotEquals
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test
import org.lwjgl.util.shaderc.Shaderc.*
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import kotlin.io.path.extension
import kotlin.io.path.isRegularFile
import kotlin.io.path.readText

class ShaderCompileTest {

    private val extensionToKind = mapOf(
        "rgen" to shaderc_raygen_shader,
        "rmiss" to shaderc_miss_shader,
        "rchit" to shaderc_closesthit_shader,
        "comp" to shaderc_compute_shader,
        "vert" to shaderc_vertex_shader,
        "frag" to shaderc_fragment_shader,
    )

    private fun findShaderRoot(): Path {
        val candidates = listOf(
            Paths.get("src/main/resources/shaders"),
            Paths.get("renderer/src/main/resources/shaders"),
        )
        for (candidate in candidates) {
            if (Files.isDirectory(candidate)) {
                return candidate
            }
        }
        throw AssertionError(
            "Shader directory not found. Tried: " +
                candidates.joinToString { it.toAbsolutePath().normalize().toString() }
        )
    }

    private fun collectShaders(root: Path): List<Path> =
        Files.walk(root)
            .filter { it.isRegularFile() && it.extension in extensionToKind }
            .sorted()
            .toList()

    @Test
    fun allShadersCompile() {
        val root = findShaderRoot()
        val shaders = collectShaders(root)
        assertTrue(
            shaders.size >= 5,
            "Expected at least 5 shaders under $root, found ${shaders.size}"
        )

        val compiler = shaderc_compiler_initialize()
        assertNotEquals(0L, compiler, "Failed to initialize shaderc compiler")

        val options = shaderc_compile_options_initialize()
        try {
            shaderc_compile_options_set_target_env(
                options, shaderc_target_env_vulkan, shaderc_env_version_vulkan_1_3
            )
            shaderc_compile_options_set_target_spirv(options, shaderc_spirv_version_1_6)
            shaderc_compile_options_set_optimization_level(options, shaderc_optimization_level_performance)

            val failures = mutableListOf<String>()
            for (shaderPath in shaders) {
                val source = shaderPath.readText()
                val kind = extensionToKind.getValue(shaderPath.extension)
                val filename = root.relativize(shaderPath).toString().replace('\\', '/')

                val result = shaderc_compile_into_spv(
                    compiler, source, kind, filename, "main", options
                )
                try {
                    if (shaderc_result_get_compilation_status(result) != shaderc_compilation_status_success) {
                        val errorMsg = shaderc_result_get_error_message(result)
                        failures.add("$filename: $errorMsg")
                    }
                } finally {
                    shaderc_result_release(result)
                }
            }

            if (failures.isNotEmpty()) {
                throw AssertionError("Shader compilation failed:\n${failures.joinToString("\n")}")
            }
        } finally {
            shaderc_compile_options_release(options)
            shaderc_compiler_release(compiler)
        }
    }
}
