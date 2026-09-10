package com.lumina.core

import com.google.inject.Guice
import com.google.inject.Injector
import com.lumina.core.config.LuminaModule
import com.lumina.core.game.GameJarLoader
import com.lumina.core.game.JagexAuthManager
import com.lumina.core.game.JagexLauncherIPC
import com.lumina.plugin.*
import com.lumina.renderer.LuminaRenderer
import com.lumina.scene.graph.SceneGraph
import org.lwjgl.glfw.GLFW.glfwPollEvents
import org.lwjgl.glfw.GLFW.glfwWindowShouldClose
import org.slf4j.LoggerFactory
import java.io.File

class LuminaClient(private val args: Array<String>) {
    private val log = LoggerFactory.getLogger(LuminaClient::class.java)
    private lateinit var injector: Injector
    private lateinit var renderer: LuminaRenderer
    private lateinit var pluginManager: PluginManager
    private lateinit var eventBus: EventBus
    private lateinit var authManager: JagexAuthManager
    @Volatile private var running = false

    fun start() {
        log.info("Lumina OSRS Client starting...")

        val luminaDir = File(System.getProperty("user.home"), ".lumina")
        luminaDir.mkdirs()
        val runeliteDir = File(System.getProperty("user.home"), ".runelite")

        injector = Guice.createInjector(LuminaModule(luminaDir, runeliteDir, args))

        eventBus = injector.getInstance(EventBus::class.java)
        authManager = injector.getInstance(JagexAuthManager::class.java)
        renderer = injector.getInstance(LuminaRenderer::class.java)
        val sceneGraph = injector.getInstance(SceneGraph::class.java)

        val ipc = injector.getInstance(JagexLauncherIPC::class.java)
        ipc.initialize(args)

        val gameJarLoader = injector.getInstance(GameJarLoader::class.java)
        try {
            gameJarLoader.loadGameJars(runeliteDir)
            log.info("Game client version: {}", gameJarLoader.getClientVersion())
        } catch (e: Exception) {
            log.error("Failed to load game JARs: {}", e.message)
        }

        renderer.init("Lumina - Old School RuneScape", 1280, 720)

        val developerMode = "--developer-mode" in args
        pluginManager = PluginManager(injector, developerMode)

        val pluginDir = File(luminaDir, "plugins")
        pluginDir.mkdirs()
        pluginManager.loadPluginsFromDirectory(pluginDir)

        if (developerMode) {
            val sideloadDir = File(luminaDir, "sideloaded-plugins")
            sideloadDir.mkdirs()
            pluginManager.loadPluginsFromDirectory(sideloadDir)
        }

        pluginManager.startAll()
        eventBus.post(GameStateChanged(GameState.STARTING, GameState.LOGIN_SCREEN))

        running = true
        mainLoop()
    }

    private fun mainLoop() {
        val window = renderer.vkContext.window
        log.info("Entering main loop")

        while (running && !glfwWindowShouldClose(window)) {
            glfwPollEvents()

            eventBus.post(BeforeRender())
            renderer.renderFrame()
            eventBus.post(AfterRender())

            if (renderer.frameCount % 300 == 0L) {
                eventBus.post(FrameRendered(renderer.lastFrameTimeMs, renderer.fps))
            }
        }

        shutdown()
    }

    private fun shutdown() {
        running = false
        log.info("Shutting down...")
        eventBus.post(ClientShutdown())
        pluginManager.stopAll()
        renderer.destroy()
        log.info("Lumina client stopped")
    }
}
