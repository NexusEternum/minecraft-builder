package com.lumina.core.game

import com.lumina.plugin.LiveGameView
import org.slf4j.LoggerFactory

/**
 * Reflection indirection so client-core does not compile against net.runelite:client.
 * The :game module is pulled in at runtime by :launcher (runtimeOnly).
 */
object GameLauncher {
    private val log = LoggerFactory.getLogger(GameLauncher::class.java)

    fun launchIfRequested(args: Array<String>): Boolean {
        if ("--game" !in args || "--play" in args) return false

        log.info("Delegating to embedded RuneLite client via :game module")
        try {
            val bootstrapClass = Class.forName("com.lumina.game.RuneLiteBootstrap")
            val bootstrap = bootstrapClass.getDeclaredConstructor().newInstance()
            val launch = bootstrapClass.getMethod("launch", List::class.java)
            launch.invoke(bootstrap, args.toList())
        } catch (e: ClassNotFoundException) {
            throw IllegalStateException(
                "Game module not on classpath. Build with :launcher (runtimeOnly :game) or add :game to the classpath.",
                e
            )
        }
        return true
    }

    /**
     * Boots embedded RuneLite on a background thread and returns a [LiveGameView]
     * implemented by [com.lumina.game.LiveGameState] in the :game module.
     */
    fun startPlaySession(args: Array<String>): LiveGameView {
        log.info("Starting embedded RuneLite client for --play mirror mode")
        try {
            val liveGameStateClass = Class.forName("com.lumina.game.LiveGameState")
            val liveGameState = liveGameStateClass.getDeclaredConstructor().newInstance()
            val markStarting = liveGameStateClass.getMethod("markClientStarting")
            val startEmbedded = liveGameStateClass.getMethod("startEmbeddedClient", List::class.java)

            markStarting.invoke(liveGameState)

            Thread({
                try {
                    startEmbedded.invoke(liveGameState, args.toList())
                } catch (e: Exception) {
                    log.error("Embedded RuneLite client failed", e)
                }
            }, "runelite-client").apply {
                isDaemon = false
                start()
            }

            return liveGameState as LiveGameView
        } catch (e: ClassNotFoundException) {
            throw IllegalStateException(
                "Game module not on classpath. Build with :launcher (runtimeOnly :game) or add :game to the classpath.",
                e
            )
        }
    }
}
