package com.lumina.game

import com.lumina.plugin.LiveGameSnapshot
import com.lumina.plugin.LiveGameView
import net.runelite.api.Client
import net.runelite.api.GameState
import net.runelite.client.RuneLite
import org.slf4j.LoggerFactory
import java.util.concurrent.atomic.AtomicReference

/**
 * Polls the embedded RuneLite [Client] for live scene/camera state used by --play mirror mode.
 *
 * Camera semantics (RuneLite API 1.12.x):
 * - [Client.getCameraX]/[getCameraY]: local scene position in 1/128 tile units
 *   (same space as [net.runelite.api.coords.LocalPoint]; see LocalPoint javadoc).
 * - [Client.getCameraZ]: vertical height in the same 1/128 tile units as tile heights.
 * - [Client.getCameraPitch]/[getCameraYaw]: JAU14 angles (0x4000 units per revolution;
 *   see Client javadoc and Perspective.UNIT14).
 * - [Client.getBaseX]/[getBaseY]: SW corner of the loaded scene in world tile coordinates.
 * - [Client.getMapRegions]: region IDs currently loaded (typically up to nine).
 */
class LiveGameState : LiveGameView {
    private val log = LoggerFactory.getLogger(LiveGameState::class.java)
    private val snapshotRef = AtomicReference<LiveGameSnapshot?>(null)
    @Volatile private var clientThreadRunning = false
    @Volatile private var pollThreadRunning = false

    /**
     * Called by [GameLauncher] before the client thread starts so [isRunning] is true during startup.
     */
    fun markClientStarting() {
        clientThreadRunning = true
    }

    /**
     * Blocks the calling thread running [RuneLite.main]. Intended to run on a dedicated
     * background thread started by [GameLauncher].
     */
    fun startEmbeddedClient(args: List<String>) {
        val pollThread = Thread({ pollLoop() }, "live-game-poll")
        pollThread.isDaemon = true
        pollThread.start()

        try {
            RuneLiteBootstrap().launch(args)
        } catch (e: Exception) {
            log.error("RuneLite launch failed", e)
        }

        // RuneLite.main() returns after startup; the Swing/game client keeps running on other threads.
        while (obtainClient() != null) {
            Thread.sleep(500)
        }

        pollThreadRunning = false
        pollThread.join(2000)
        clientThreadRunning = false
        log.info("Embedded RuneLite client session ended")
    }

    override fun latestSnapshot(): LiveGameSnapshot? = snapshotRef.get()

    override fun isRunning(): Boolean = clientThreadRunning

    private fun pollLoop() {
        pollThreadRunning = true
        var waitLogged = false
        while (pollThreadRunning && clientThreadRunning) {
            try {
                val client = obtainClient()
                if (client == null) {
                    if (!waitLogged) {
                        log.debug("LiveGameState: waiting for RuneLite injector...")
                        waitLogged = true
                    }
                } else {
                    waitLogged = false
                    snapshotRef.set(readSnapshot(client))
                }
            } catch (e: Exception) {
                log.debug("LiveGameState poll error: {}", e.message)
            }
            Thread.sleep(POLL_INTERVAL_MS)
        }
    }

    private fun obtainClient(): Client? {
        val injector = RuneLite.getInjector() ?: return null
        return injector.getInstance(Client::class.java)
    }

    private fun readSnapshot(client: Client): LiveGameSnapshot {
        val gameState = client.gameState
        val loggedIn = gameState == GameState.LOGGED_IN
        if (!loggedIn) {
            return LiveGameSnapshot(
                loggedIn = false,
                baseX = 0,
                baseY = 0,
                plane = 0,
                mapRegions = IntArray(0),
                cameraX = safeCameraX(client),
                cameraY = safeCameraY(client),
                cameraZ = safeCameraZ(client),
                cameraPitch = safeCameraPitch(client),
                cameraYaw = safeCameraYaw(client)
            )
        }

        @Suppress("DEPRECATION")
        val mapRegions = client.mapRegions ?: IntArray(0)
        @Suppress("DEPRECATION")
        return LiveGameSnapshot(
            loggedIn = true,
            baseX = client.baseX,
            baseY = client.baseY,
            plane = client.plane,
            mapRegions = mapRegions.copyOf(),
            cameraX = client.cameraX,
            cameraY = client.cameraY,
            cameraZ = client.cameraZ,
            cameraPitch = client.cameraPitch,
            cameraYaw = client.cameraYaw
        )
    }

    private fun safeCameraX(client: Client): Int =
        runCatching { client.cameraX }.getOrDefault(0)

    private fun safeCameraY(client: Client): Int =
        runCatching { client.cameraY }.getOrDefault(0)

    private fun safeCameraZ(client: Client): Int =
        runCatching { client.cameraZ }.getOrDefault(0)

    private fun safeCameraPitch(client: Client): Int =
        runCatching { client.cameraPitch }.getOrDefault(0)

    private fun safeCameraYaw(client: Client): Int =
        runCatching { client.cameraYaw }.getOrDefault(0)

    companion object {
        /** ~30 Hz camera polling. */
        const val POLL_INTERVAL_MS = 33L
    }
}
