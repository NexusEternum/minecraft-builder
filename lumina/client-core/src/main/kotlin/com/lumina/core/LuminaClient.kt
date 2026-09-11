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
import com.lumina.scene.osrs.OsrsMapLoader
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
    private lateinit var osrsMapLoader: OsrsMapLoader
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
        osrsMapLoader = injector.getInstance(OsrsMapLoader::class.java)

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

        // Generate and upload scene so the path tracer has geometry
        val osrsRegionId = parseOsrsRegionId()
        val osrsLoaded = if (osrsRegionId >= 0) {
            val cacheDir = resolveCacheDir()
            log.info("Loading OSRS region {} from cache: {}", osrsRegionId, cacheDir.absolutePath)
            osrsMapLoader.loadRegion(cacheDir, osrsRegionId)
        } else {
            false
        }

        if (osrsLoaded) {
            sceneBufferManager.uploadSceneData()
            log.info("OSRS terrain loaded and uploaded to GPU")
            camera.setPosition(81f, 30f, 81f)
            camera.setRotation(-0.5f, 0f)
        } else {
            if (osrsRegionId >= 0) {
                log.warn("OSRS terrain load failed; falling back to demo scene")
            }
            demoScene.generate()
            sceneBufferManager.uploadSceneData()
            log.info("Demo scene loaded and uploaded to GPU")
            camera.setPosition(0f, 8f, 20f)
            camera.setRotation(-0.3f, 0f)
        }

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

    private fun parseOsrsRegionId(): Int {
        val index = args.indexOf("--osrs")
        if (index < 0) return -1
        val next = args.getOrNull(index + 1)?.toIntOrNull()
        return next ?: DEFAULT_OSRS_REGION_ID
    }

    private fun resolveCacheDir(): File {
        System.getProperty("lumina.cache")?.let { path ->
            val dir = File(path)
            log.info("Using OSRS cache from lumina.cache system property: {}", dir.absolutePath)
            return dir
        }

        val home = File(System.getProperty("user.home"))
        val jagexCache = File(home, "jagexcache/oldschool/LIVE")
        if (jagexCache.isDirectory) {
            log.info("Using OSRS cache from Jagex launcher path: {}", jagexCache.absolutePath)
            return jagexCache
        }

        val runeliteCache = File(home, ".runelite/jagexcache/oldschool/LIVE")
        log.info("Using OSRS cache from RuneLite path: {}", runeliteCache.absolutePath)
        return runeliteCache
    }

    companion object {
        private const val DEFAULT_OSRS_REGION_ID = 12850
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
        log.info("F11        - Toggle debug mode (flat albedo, no shadows)")
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
            }

            try {
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
            } catch (e: Exception) {
                log.error("Render error: {}", e.message)
                if (renderer.frameCount < 5) {
                    log.error("Fatal render error on early frame", e)
                    break
                }
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
