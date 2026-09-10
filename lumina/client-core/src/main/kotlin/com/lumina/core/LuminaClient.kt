package com.lumina.core

import com.google.inject.Guice
import com.google.inject.Injector
import com.lumina.core.config.LuminaModule
import com.lumina.core.game.GameJarLoader
import com.lumina.core.game.JagexAuthManager
import com.lumina.core.game.JagexLauncherIPC
import com.lumina.plugin.*
import com.lumina.renderer.LuminaRenderer
import com.lumina.renderer.camera.CameraController
import com.lumina.renderer.scene.SceneBufferManager
import com.lumina.scene.graph.SceneGraph
import org.lwjgl.glfw.GLFW.*
import org.lwjgl.glfw.GLFWCursorPosCallbackI
import org.lwjgl.glfw.GLFWFramebufferSizeCallbackI
import org.lwjgl.glfw.GLFWKeyCallbackI
import org.slf4j.LoggerFactory
import java.io.File

class LuminaClient(private val args: Array<String>) {
    private val log = LoggerFactory.getLogger(LuminaClient::class.java)
    private lateinit var injector: Injector
    private lateinit var renderer: LuminaRenderer
    private lateinit var pluginManager: PluginManager
    private lateinit var eventBus: EventBus
    private lateinit var authManager: JagexAuthManager
    private lateinit var camera: CameraController
    private lateinit var sceneBufferManager: SceneBufferManager
    @Volatile private var running = false
    private var resizeRequested = false
    private var newWidth = 0
    private var newHeight = 0

    fun start() {
        log.info("Lumina OSRS Client starting...")

        val luminaDir = File(System.getProperty("user.home"), ".lumina")
        luminaDir.mkdirs()
        val runeliteDir = File(System.getProperty("user.home"), ".runelite")

        injector = Guice.createInjector(LuminaModule(luminaDir, runeliteDir, args))

        eventBus = injector.getInstance(EventBus::class.java)
        authManager = injector.getInstance(JagexAuthManager::class.java)
        renderer = injector.getInstance(LuminaRenderer::class.java)
        camera = injector.getInstance(CameraController::class.java)
        sceneBufferManager = injector.getInstance(SceneBufferManager::class.java)
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

        renderer.init("Lumina - Old School RuneScape", 1920, 1080)
        setupCallbacks()

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

    private fun setupCallbacks() {
        val window = renderer.vkContext.window

        glfwSetFramebufferSizeCallback(window, GLFWFramebufferSizeCallbackI { _, w, h ->
            if (w > 0 && h > 0) {
                resizeRequested = true
                newWidth = w; newHeight = h
            }
        })

        glfwSetCursorPosCallback(window, GLFWCursorPosCallbackI { _, x, y ->
            camera.handleMouseMove(x, y)
        })

        glfwSetKeyCallback(window, GLFWKeyCallbackI { _, key, _, action, _ ->
            if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS) {
                camera.toggleMouseCapture(window)
            }
            if (key == GLFW_KEY_F11 && action == GLFW_PRESS) {
                // could toggle fullscreen in the future
            }
        })
    }

    private fun mainLoop() {
        val window = renderer.vkContext.window
        log.info("Entering main loop")

        while (running && !glfwWindowShouldClose(window)) {
            glfwPollEvents()

            if (resizeRequested) {
                resizeRequested = false
                renderer.resize(newWidth, newHeight)
            }

            val deltaTime = (renderer.lastFrameTimeMs / 1000.0).toFloat().coerceIn(0.0001f, 0.1f)
            camera.update(window, deltaTime,
                renderer.upscale.getJitterX(), renderer.upscale.getJitterY())

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
        sceneBufferManager.destroy()
        renderer.destroy()
        log.info("Lumina client stopped")
    }
}
