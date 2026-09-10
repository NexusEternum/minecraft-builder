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
import com.lumina.renderer.overlay.OverlayRenderer
import com.lumina.renderer.scene.DemoScene
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
    private lateinit var overlay: OverlayRenderer
    private lateinit var demoScene: DemoScene
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
        overlay = injector.getInstance(OverlayRenderer::class.java)
        demoScene = injector.getInstance(DemoScene::class.java)

        val ipc = injector.getInstance(JagexLauncherIPC::class.java)
        ipc.initialize(args)

        val gameJarLoader = injector.getInstance(GameJarLoader::class.java)
        try {
            gameJarLoader.loadGameJars(runeliteDir)
            log.info("Game client version: {}", gameJarLoader.getClientVersion())
        } catch (e: Exception) {
            log.warn("Game JARs not found (running in demo mode): {}", e.message)
        }

        renderer.init("Lumina - Old School RuneScape", 1920, 1080)
        setupCallbacks()

        // Generate and upload demo scene so the path tracer has geometry
        demoScene.generate()
        sceneBufferManager.uploadSceneData()
        log.info("Demo scene loaded and uploaded to GPU")

        // Position camera to view the scene
        camera.setPosition(0f, 8f, 20f)
        camera.setRotation(-0.3f, 3.14f)

        val developerMode = "--developer-mode" in args || "--demo" in args
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

        printControls()

        running = true
        mainLoop()
    }

    private fun printControls() {
        log.info("=== Controls ===")
        log.info("WASD       - Move camera")
        log.info("Mouse      - Look around (click to capture, ESC to release)")
        log.info("Space/Shift- Up/Down")
        log.info("F1         - Toggle FPS display")
        log.info("F2         - Toggle debug info")
        log.info("F3         - Print settings")
        log.info("F5         - Toggle bloom")
        log.info("F6         - Toggle volumetric fog")
        log.info("F7         - Cycle tone mapping (AgX/ACES/Reinhard/None)")
        log.info("F8         - Cycle upscale quality")
        log.info("+/-        - Adjust exposure")
        log.info("ESC        - Toggle mouse capture")
        log.info("================")
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

        glfwSetKeyCallback(window, GLFWKeyCallbackI { win, key, _, action, _ ->
            if (!overlay.handleKey(key, action)) {
                if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS) {
                    camera.toggleMouseCapture(win)
                }
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

            overlay.update(renderer.lastFrameTimeMs, renderer.frameCount)

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
