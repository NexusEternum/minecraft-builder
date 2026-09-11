package com.lumina.core

import com.google.inject.Guice
import com.google.inject.Injector
import com.lumina.core.config.LuminaModule
import com.lumina.core.game.GameJarLoader
import com.lumina.core.game.GameLauncher
import com.lumina.core.game.JagexAuthManager
import com.lumina.core.game.JagexLauncherIPC
import com.lumina.plugin.*
import com.lumina.renderer.LuminaRenderer
import com.lumina.renderer.camera.CameraController
import com.lumina.renderer.camera.CameraFovFromScale
import com.lumina.renderer.overlay.BUILD_STAMP
import com.lumina.renderer.overlay.OverlayRenderer
import com.lumina.renderer.postfx.PostProcessStack
import com.lumina.renderer.scene.DemoScene
import com.lumina.renderer.scene.SceneBufferManager
import com.lumina.scene.graph.MaterialComponent
import com.lumina.scene.graph.MeshComponent
import com.lumina.scene.graph.SceneGraph
import com.lumina.scene.graph.Transform
import org.lwjgl.glfw.GLFW.*
import org.lwjgl.glfw.GLFWCursorPosCallbackI
import org.lwjgl.glfw.GLFWFramebufferSizeCallbackI
import org.lwjgl.glfw.GLFWKeyCallbackI
import com.lumina.scene.osrs.OsrsCoordinateMapper
import com.lumina.scene.osrs.OsrsMapLoader
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
    private lateinit var sceneGraph: SceneGraph
    @Volatile private var running = false
    private var resizeRequested = false
    private var newWidth = 0
    private var newHeight = 0

    private var playMode = false
    private var liveGameView: LiveGameView? = null
    private var cameraSyncEnabled = true
    /** Frozen scene-load origin in world tiles; geometry and camera both subtract this, never the current base. */
    private var sceneLoadOriginBaseX = 0
    private var sceneLoadOriginBaseY = 0
    private var lastCameraDiagLogMs = 0L
    private var loadedRegionsKey: String? = null
    private var pendingRegionsKey: String? = null
    private var pendingRegionsStablePolls = 0
    private var loadedMaxVisiblePlane = 0
    private var pendingMaxVisiblePlane: Int? = null
    private var pendingPlaneStablePolls = 0
    private var playerMarkerNodeId: Int? = null
    private var lastPlayerMarkerX = Float.NaN
    private var lastPlayerMarkerY = Float.NaN
    private var lastPlayerMarkerZ = Float.NaN

    fun start() {
        if ("--game" in args && "--play" !in args) {
            if (GameLauncher.launchIfRequested(args)) {
                return
            }
        }

        if ("--play" in args) {
            startPlayMode()
            return
        }

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

        val osrsRegionId = parseOsrsRegionId()
        if (osrsRegionId >= 0) {
            configureOsrsWorldRendering()
        }

        // Generate and upload scene so the path tracer has geometry
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
            camera.setPosition(
                osrsMapLoader.lastRegionCenterWorldX,
                osrsMapLoader.lastRegionCenterWorldY,
                osrsMapLoader.lastRegionCenterWorldZ
            )
            camera.setRotation(-0.35f, 0f)
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

    private fun startPlayMode() {
        playMode = true
        log.info("Lumina --play live mirror mode starting (build {})", BUILD_STAMP)

        liveGameView = GameLauncher.startPlaySession(args)
        val loginSnapshot = waitForLogin(liveGameView!!)

        val luminaDir = File(System.getProperty("user.home"), ".lumina")
        luminaDir.mkdirs()
        val runeliteDir = File(System.getProperty("user.home"), ".runelite")

        injector = Guice.createInjector(LuminaModule(luminaDir, runeliteDir, args))

        eventBus = injector.getInstance(EventBus::class.java)
        renderer = injector.getInstance(LuminaRenderer::class.java)
        camera = injector.getInstance(CameraController::class.java)
        sceneBufferManager = injector.getInstance(SceneBufferManager::class.java)
        overlay = injector.getInstance(OverlayRenderer::class.java)
        osrsMapLoader = injector.getInstance(OsrsMapLoader::class.java)
        sceneGraph = injector.getInstance(SceneGraph::class.java)

        camera.manualControlEnabled = false
        camera.useYawPitchControl()

        renderer.init("Lumina LIVE - OSRS [build $BUILD_STAMP]", 1920, 1080)
        setupCallbacks()
        configureOsrsWorldRendering()

        val loadSnapshot = waitForStableSceneSnapshot(liveGameView!!, loginSnapshot)
        if (loadSnapshot !== loginSnapshot) {
            log.info(
                "--play: scene load snapshot base=({}, {}) vs login=({}, {})",
                loadSnapshot.baseX,
                loadSnapshot.baseY,
                loginSnapshot.baseX,
                loginSnapshot.baseY
            )
        }
        if (!reloadLiveScene(loadSnapshot)) {
            log.error("--play: failed to load live scene regions; exiting")
            System.exit(1)
        }

        // Use the same atomic snapshot as scene load so base/camera/regions are never mixed.
        syncCameraFromSnapshot(loadSnapshot)

        printControls()
        log.info("--play: mirror window open; camera sync enabled (F8 toggles free camera)")

        running = true
        mainLoop()
    }

    /**
     * Wait until the embedded client reports a coherent scene: non-empty regions and a stable base
     * for [STABLE_SCENE_POLLS] consecutive polls. Avoids loading with base=(0,0) while WorldView
     * is still coming up (which places geometry relative to the wrong origin).
     */
    private fun waitForStableSceneSnapshot(
        liveView: LiveGameView,
        fallback: LiveGameSnapshot
    ): LiveGameSnapshot {
        var lastBaseX = Int.MIN_VALUE
        var lastBaseY = Int.MIN_VALUE
        var stablePolls = 0
        var lastSnapshot = fallback
        var waitLogged = false

        while (stablePolls < STABLE_SCENE_POLLS) {
            val snapshot = liveView.latestSnapshot()
            if (snapshot?.loggedIn == true && snapshot.isSceneReady()) {
                if (snapshot.baseX == lastBaseX && snapshot.baseY == lastBaseY) {
                    stablePolls++
                } else {
                    stablePolls = 1
                }
                lastBaseX = snapshot.baseX
                lastBaseY = snapshot.baseY
                lastSnapshot = snapshot
            } else {
                stablePolls = 0
                lastBaseX = Int.MIN_VALUE
                lastBaseY = Int.MIN_VALUE
                if (!waitLogged) {
                    log.info("--play: waiting for stable scene snapshot (regions + base)...")
                    waitLogged = true
                }
            }
            Thread.sleep(LIVE_POLL_INTERVAL_MS)
        }

        log.info(
            "--play: stable scene snapshot base=({}, {}), {} regions, camera local=({}, {})",
            lastSnapshot.baseX,
            lastSnapshot.baseY,
            lastSnapshot.mapRegions.size,
            lastSnapshot.cameraX,
            lastSnapshot.cameraY
        )
        return lastSnapshot
    }

    private fun configureOsrsWorldRendering() {
        val postProcess = injector.getInstance(PostProcessStack::class.java)
        postProcess.applyOsrsWorldDefaults()
        log.info("OSRS world rendering: fogDensity={}, godRayIntensity={}",
            postProcess.fogDensity, postProcess.godRayIntensity)
    }

    private fun waitForLogin(liveView: LiveGameView): LiveGameSnapshot {
        var lastLogMs = 0L
        var clientEverRan = false
        while (true) {
            if (liveView.isRunning()) {
                clientEverRan = true
            }

            val snapshot = liveView.latestSnapshot()
            if (snapshot?.loggedIn == true) {
                log.info(
                    "--play: logged in at base=({}, {}), {} regions loaded",
                    snapshot.baseX,
                    snapshot.baseY,
                    snapshot.mapRegions.size
                )
                return snapshot
            }

            if (clientEverRan && !liveView.isRunning()) {
                throw IllegalStateException("Embedded RuneLite client exited before login")
            }

            val now = System.currentTimeMillis()
            if (now - lastLogMs >= 3000L) {
                log.info("--play: waiting for login...")
                lastLogMs = now
            }
            Thread.sleep(100)
        }
    }

    private fun reloadLiveScene(snapshot: LiveGameSnapshot): Boolean {
        if (snapshot.mapRegions.isEmpty()) {
            log.warn("--play: no map regions reported by client")
            return false
        }

        val cacheDir = resolveCacheDir()
        val playerWorldTileX = snapshot.playerWorldTileX().toInt()
        val playerWorldTileY = snapshot.playerWorldTileY().toInt()
        val maxVisiblePlane = snapshot.playerPlane.coerceIn(0, 3)
        log.info(
            "--play: loading {} regions from {} with origin ({}, {}), player tile=({}, {}), maxVisiblePlane={}",
            snapshot.mapRegions.size,
            cacheDir.absolutePath,
            snapshot.baseX,
            snapshot.baseY,
            playerWorldTileX,
            playerWorldTileY,
            maxVisiblePlane
        )

        val loadStartNs = System.nanoTime()
        val loaded = osrsMapLoader.loadRegions(
            cacheDir,
            snapshot.mapRegions,
            snapshot.baseX,
            snapshot.baseY,
            playerWorldTileX,
            playerWorldTileY,
            maxVisiblePlane
        )
        if (!loaded) return false
        val loadMs = (System.nanoTime() - loadStartNs) / 1_000_000

        setupPlayerMarker()

        sceneLoadOriginBaseX = snapshot.baseX
        sceneLoadOriginBaseY = snapshot.baseY
        log.info(
            "--play: scene-load origin frozen at ({}, {}); current snapshot base=({}, {})",
            sceneLoadOriginBaseX,
            sceneLoadOriginBaseY,
            snapshot.baseX,
            snapshot.baseY
        )
        loadedRegionsKey = OsrsCoordinateMapper.mapRegionsKey(snapshot.mapRegions)
        loadedMaxVisiblePlane = maxVisiblePlane
        pendingRegionsKey = null
        pendingRegionsStablePolls = 0
        pendingMaxVisiblePlane = null
        pendingPlaneStablePolls = 0

        val uploadStartNs = System.nanoTime()
        sceneBufferManager.uploadSceneData()
        val uploadMs = (System.nanoTime() - uploadStartNs) / 1_000_000
        log.info(
            "--play: scene rebuild timings — map load {} ms, GPU upload {} ms (total {} ms)",
            loadMs,
            uploadMs,
            loadMs + uploadMs
        )
        return true
    }

    private fun syncCameraFromSnapshot(snapshot: LiveGameSnapshot) {
        val luminaCamera = OsrsCoordinateMapper.cameraToLumina(
            snapshot.cameraX,
            snapshot.cameraY,
            snapshot.cameraZ,
            snapshot.cameraPitch,
            snapshot.cameraYaw,
            snapshot.baseX,
            snapshot.baseY,
            sceneLoadOriginBaseX,
            sceneLoadOriginBaseY
        )
        camera.setPosition(luminaCamera.x, luminaCamera.y, luminaCamera.z)
        camera.setFromForwardVector(luminaCamera.forwardX, luminaCamera.forwardY, luminaCamera.forwardZ)
        camera.fov = CameraFovFromScale.verticalFovDegrees(snapshot.canvasHeight, snapshot.cameraScale)

        overlay.cameraWorldTileX = snapshot.cameraWorldTileX()
        overlay.cameraWorldTileY = snapshot.cameraWorldTileY()

        val now = System.currentTimeMillis()
        if (now - lastCameraDiagLogMs >= 1000L) {
            lastCameraDiagLogMs = now
            val facing = OsrsCoordinateMapper.cardinalFacingFromForward(
                luminaCamera.forwardX,
                luminaCamera.forwardZ
            )
            log.info(
                "--play: camera world tile=({}, {}), yaw=0x{} ({}), facing={}, lumina pos=({}, {}, {})",
                snapshot.cameraWorldTileX(),
                snapshot.cameraWorldTileY(),
                Integer.toHexString(snapshot.cameraYaw),
                snapshot.cameraYaw,
                facing,
                luminaCamera.x,
                luminaCamera.y,
                luminaCamera.z
            )
        }
    }

    private fun handleLiveMirrorUpdate() {
        val liveView = liveGameView ?: return
        if (!liveView.isRunning()) {
            log.warn("--play: embedded client exited; closing mirror window")
            running = false
            return
        }

        val snapshot = liveView.latestSnapshot() ?: return
        if (!snapshot.loggedIn) return

        maybeRebuildLiveScene(snapshot)
        updatePlayerMarker(snapshot)

        if (cameraSyncEnabled) {
            syncCameraFromSnapshot(snapshot)
        }
    }

    private fun maybeRebuildLiveScene(snapshot: LiveGameSnapshot) {
        val regionsKey = OsrsCoordinateMapper.mapRegionsKey(snapshot.mapRegions)
        val maxVisiblePlane = snapshot.playerPlane.coerceIn(0, 3)
        val regionsChanged = regionsKey != loadedRegionsKey
        val planeChanged = maxVisiblePlane != loadedMaxVisiblePlane

        if (!regionsChanged && !planeChanged) {
            pendingRegionsKey = null
            pendingRegionsStablePolls = 0
            pendingMaxVisiblePlane = null
            pendingPlaneStablePolls = 0
            return
        }

        val pendingKey = when {
            regionsChanged -> regionsKey
            else -> pendingRegionsKey ?: loadedRegionsKey
        }
        val pendingPlane = when {
            planeChanged -> maxVisiblePlane
            else -> pendingMaxVisiblePlane ?: loadedMaxVisiblePlane
        }

        if (pendingKey != pendingRegionsKey || pendingPlane != pendingMaxVisiblePlane) {
            pendingRegionsKey = pendingKey
            pendingMaxVisiblePlane = pendingPlane
            pendingRegionsStablePolls = 1
            pendingPlaneStablePolls = 1
            return
        }

        pendingRegionsStablePolls++
        pendingPlaneStablePolls++
        if (pendingRegionsStablePolls < REGION_CHANGE_STABLE_POLLS) return
        if (pendingPlaneStablePolls < PLANE_CHANGE_STABLE_POLLS) return

        log.info(
            "--play: scene visibility changed (regions {} -> {}, plane {} -> {}), rebuilding scene",
            loadedRegionsKey,
            regionsKey,
            loadedMaxVisiblePlane,
            maxVisiblePlane
        )
        if (reloadLiveScene(snapshot)) {
            syncCameraFromSnapshot(snapshot)
        }
    }

    private fun setupPlayerMarker() {
        playerMarkerNodeId = null
        lastPlayerMarkerX = Float.NaN
        lastPlayerMarkerY = Float.NaN
        lastPlayerMarkerZ = Float.NaN

        val node = sceneGraph.createNode("player_marker")
        playerMarkerNodeId = node.id
        node.addComponent(
            Transform(
                scaleX = PLAYER_MARKER_SIZE,
                scaleY = PLAYER_MARKER_SIZE,
                scaleZ = PLAYER_MARKER_SIZE
            )
        )
        node.addComponent(createPlayerMarkerMesh())
        node.addComponent(
            MaterialComponent(
                albedo = floatArrayOf(1f, 0.9f, 0.2f),
                roughness = 0.2f,
                metallic = 0f,
                emissive = floatArrayOf(4f, 3f, 1f)
            )
        )
    }

    private fun updatePlayerMarker(snapshot: LiveGameSnapshot) {
        val nodeId = playerMarkerNodeId ?: return
        val node = sceneGraph.getNode(nodeId) ?: return
        val transform = node.getComponent(Transform::class.java) ?: return

        val (worldTileX, worldTileY) = OsrsCoordinateMapper.localSceneUnitsToWorldTiles(
            snapshot.baseX,
            snapshot.baseY,
            snapshot.playerLocalX,
            snapshot.playerLocalY
        )
        val (luminaX, luminaZ) = OsrsCoordinateMapper.worldTileToLuminaXZ(
            worldTileX,
            worldTileY,
            sceneLoadOriginBaseX,
            sceneLoadOriginBaseY
        )
        val luminaY = OsrsCoordinateMapper.luminaYFromHeightUnits128(snapshot.playerPlane * PLANE_HEIGHT_UNITS) +
            PLAYER_MARKER_SIZE * 0.5f

        val dx = luminaX - lastPlayerMarkerX
        val dy = luminaY - lastPlayerMarkerY
        val dz = luminaZ - lastPlayerMarkerZ
        val movedSq = dx * dx + dy * dy + dz * dz
        val threshold = 0.5f * OsrsMapLoader.TILE_SCALE
        if (!movedSq.isNaN() && movedSq < threshold * threshold &&
            transform.x == luminaX && transform.y == luminaY && transform.z == luminaZ
        ) {
            return
        }

        transform.x = luminaX
        transform.y = luminaY
        transform.z = luminaZ
        lastPlayerMarkerX = luminaX
        lastPlayerMarkerY = luminaY
        lastPlayerMarkerZ = luminaZ
        sceneGraph.markDirty()
    }

    private fun createPlayerMarkerMesh(): MeshComponent {
        val h = 0.5f
        val verts = floatArrayOf(
            -h, -h, -h, 0f, 1f, 0f, 0f, 0f,
            h, -h, -h, 0f, 1f, 0f, 0f, 0f,
            h, h, -h, 0f, 1f, 0f, 0f, 0f,
            -h, h, -h, 0f, 1f, 0f, 0f, 0f,
            -h, -h, h, 0f, 1f, 0f, 0f, 0f,
            h, -h, h, 0f, 1f, 0f, 0f, 0f,
            h, h, h, 0f, 1f, 0f, 0f, 0f,
            -h, h, h, 0f, 1f, 0f, 0f, 0f
        )
        val indices = intArrayOf(
            0, 1, 2, 0, 2, 3,
            4, 6, 5, 4, 7, 6,
            0, 4, 5, 0, 5, 1,
            2, 6, 7, 2, 7, 3,
            0, 3, 7, 0, 7, 4,
            1, 5, 6, 1, 6, 2
        )
        return MeshComponent(verts, indices, 8, 12)
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
        /** Debounce region rebuild until the new set is stable for this many live polls. */
        private const val REGION_CHANGE_STABLE_POLLS = 2
        /** Debounce plane visibility rebuild until the new plane is stable for this many live polls. */
        private const val PLANE_CHANGE_STABLE_POLLS = 2
        /** Scene base must match for this many consecutive polls before mirror load. */
        private const val STABLE_SCENE_POLLS = 2
        /** Matches [com.lumina.game.LiveGameState.POLL_INTERVAL_MS]. */
        private const val LIVE_POLL_INTERVAL_MS = 33L
        private const val PLAYER_MARKER_SIZE = 0.8f
        /** OSRS nominal vertical spacing between planes in 1/128 tile height units. */
        private const val PLANE_HEIGHT_UNITS = 256
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
        log.info("F8         - Cycle upscale quality (or toggle camera sync in --play)")
        log.info("F9         - Toggle raw path-traced output (skip denoiser/postfx)")
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
            if (playMode && key == GLFW_KEY_F8 && action == GLFW_PRESS) {
                cameraSyncEnabled = !cameraSyncEnabled
                camera.manualControlEnabled = !cameraSyncEnabled
                if (cameraSyncEnabled) {
                    liveGameView?.latestSnapshot()?.let { syncCameraFromSnapshot(it) }
                } else {
                    camera.useYawPitchControl()
                }
                log.info("--play: camera sync {} (manual control {})",
                    if (cameraSyncEnabled) "enabled" else "disabled",
                    if (camera.manualControlEnabled) "enabled" else "disabled")
                return@GLFWKeyCallbackI
            }
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
                if (playMode) {
                    handleLiveMirrorUpdate()
                }
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
        if (playMode) {
            System.exit(0)
        }
    }
}
