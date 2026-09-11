package com.lumina.game

import com.lumina.game.jagex.JagexSessionService
import net.runelite.client.RuneLite
import org.slf4j.LoggerFactory

/**
 * Boots Jagex's OSRS client via the published RuneLite client artifact.
 *
 * RuneLite's [ClientLoader] downloads the vanilla gamepack from Jagex and applies
 * injection at runtime; it needs network access and writes to ~/.runelite.
 */
class RuneLiteBootstrap {
    private val log = LoggerFactory.getLogger(RuneLiteBootstrap::class.java)
    private val jagexSessionService = JagexSessionService()

    fun launch(args: List<String>) {
        log.info("Launching embedded RuneLite client (net.runelite:client)")
        jagexSessionService.prepareForRuneliteLaunch()
        logRuneliteDataDir()

        val runeliteArgs = buildRuneliteArgs(args)
        log.info("RuneLite args: {}", if (runeliteArgs.isEmpty()) "none" else runeliteArgs.joinToString(" "))

        RuneLite.main(runeliteArgs.toTypedArray())
    }

    private fun logRuneliteDataDir() {
        val home = System.getProperty("user.home")
        log.info("RuneLite data directory: {}/.runelite (created on first run)", home)
        log.info("Internet access required to download vanilla gamepack via ClientLoader")
    }

    private fun buildRuneliteArgs(args: List<String>): List<String> {
        val filtered = args.filterNot { arg ->
            arg == "--game" ||
                arg == "--play" ||
                arg == "--demo" ||
                arg == "--developer-mode" ||
                arg == "--help" ||
                arg == "-h" ||
                arg == "--osrs" ||
                arg.startsWith("--lumina.")
        }.toMutableList()

        // Drop the region id that follows --osrs (already removed --osrs itself).
        val osrsIndex = args.indexOf("--osrs")
        if (osrsIndex >= 0) {
            val next = args.getOrNull(osrsIndex + 1)
            if (next != null && next.toIntOrNull() != null) {
                filtered.remove(next)
            }
        }

        if (!filtered.contains("--noupdate")) {
            filtered.add("--noupdate")
        }

        return filtered
    }
}
