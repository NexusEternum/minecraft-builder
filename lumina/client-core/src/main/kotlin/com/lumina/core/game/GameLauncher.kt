package com.lumina.core.game

import org.slf4j.LoggerFactory

/**
 * Reflection indirection so client-core does not compile against net.runelite:client.
 * The :game module is pulled in at runtime by :launcher (runtimeOnly).
 */
object GameLauncher {
    private val log = LoggerFactory.getLogger(GameLauncher::class.java)

    fun launchIfRequested(args: Array<String>): Boolean {
        if ("--game" !in args) return false

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
}
