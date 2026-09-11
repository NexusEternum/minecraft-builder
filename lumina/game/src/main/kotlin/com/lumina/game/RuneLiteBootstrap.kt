package com.lumina.game

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

    fun launch(args: List<String>) {
        log.info("Launching embedded RuneLite client (net.runelite:client)")
        logJagexLauncherEnv()
        logRuneliteDataDir()

        val runeliteArgs = buildRuneliteArgs(args)
        log.info("RuneLite args: {}", if (runeliteArgs.isEmpty()) "none" else runeliteArgs.joinToString(" "))

        RuneLite.main(runeliteArgs.toTypedArray())
    }

    private fun logJagexLauncherEnv() {
        val vars = listOf(
            "JX_SESSION_ID",
            "JX_CHARACTER_ID",
            "JX_DISPLAY_NAME",
            "JX_REFRESH_TOKEN",
        )
        for (name in vars) {
            val value = System.getenv(name)
            if (value != null) {
                log.info("Jagex launcher env {} present (masked: {})", name, mask(value))
            } else {
                log.info("Jagex launcher env {} not set", name)
            }
        }
    }

    private fun logRuneliteDataDir() {
        val home = System.getProperty("user.home")
        log.info("RuneLite data directory: {}/.runelite (created on first run)", home)
        log.info("Internet access required to download vanilla gamepack via ClientLoader")
    }

    private fun buildRuneliteArgs(args: List<String>): List<String> {
        val filtered = args.filterNot { arg ->
            arg == "--game" ||
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

    private fun mask(value: String): String {
        if (value.length <= 4) return "****"
        return value.take(2) + "****" + value.takeLast(2)
    }
}
