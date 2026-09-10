package com.lumina.core.config

import com.google.inject.AbstractModule
import com.google.inject.Provides
import com.google.inject.name.Names
import com.lumina.plugin.ConfigManager
import com.lumina.plugin.EventBus
import com.lumina.core.game.JagexLauncherIPC
import com.lumina.renderer.LuminaRenderer
import com.lumina.renderer.denoise.SVGFDenoiser
import com.lumina.renderer.postfx.PostProcessStack
import com.lumina.renderer.rt.AccelerationStructureManager
import com.lumina.renderer.rt.RayTracingPipeline
import com.lumina.renderer.upscale.UpscaleManager
import com.lumina.renderer.vulkan.FrameManager
import com.lumina.renderer.vulkan.ShaderCompiler
import com.lumina.renderer.vulkan.VulkanContext
import com.lumina.scene.extract.OsrsSceneExtractor
import com.lumina.scene.graph.SceneGraph
import com.lumina.scene.model.ModelPackManager
import okhttp3.OkHttpClient
import java.io.File
import java.util.concurrent.TimeUnit
import javax.inject.Named
import javax.inject.Singleton

class LuminaModule(
    private val luminaDir: File,
    private val runeliteDir: File,
    private val args: Array<String>
) : AbstractModule() {

    override fun configure() {
        bind(File::class.java).annotatedWith(Names.named("luminaDir")).toInstance(luminaDir)
        bind(File::class.java).annotatedWith(Names.named("runeliteDir")).toInstance(runeliteDir)
        bind(File::class.java).annotatedWith(Names.named("configDir")).toInstance(File(luminaDir, "config"))
        bind(File::class.java).annotatedWith(Names.named("dataDir")).toInstance(File(luminaDir, "data"))

        bind(EventBus::class.java).asEagerSingleton()
        bind(SceneGraph::class.java).asEagerSingleton()
        bind(VulkanContext::class.java).asEagerSingleton()
        bind(AccelerationStructureManager::class.java).asEagerSingleton()
        bind(RayTracingPipeline::class.java).asEagerSingleton()
        bind(SVGFDenoiser::class.java).asEagerSingleton()
        bind(PostProcessStack::class.java).asEagerSingleton()
        bind(UpscaleManager::class.java).asEagerSingleton()
        bind(FrameManager::class.java).asEagerSingleton()
        bind(ShaderCompiler::class.java).asEagerSingleton()
        bind(LuminaRenderer::class.java).asEagerSingleton()
        bind(OsrsSceneExtractor::class.java).asEagerSingleton()
        bind(ModelPackManager::class.java).asEagerSingleton()
        bind(ConfigManager::class.java).asEagerSingleton()
        bind(JagexLauncherIPC::class.java).asEagerSingleton()
    }

    @Provides @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .connectTimeout(15, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .build()
    }
}
