package com.lumina.launcher

import com.lumina.core.LuminaClient
import org.slf4j.LoggerFactory

private val log = LoggerFactory.getLogger("LuminaLauncher")

fun main(args: Array<String>) {
    log.info("╔══════════════════════════════════════╗")
    log.info("║     Lumina OSRS Client v0.1.0        ║")
    log.info("║  Hardware-Accelerated Path Tracing   ║")
    log.info("╚══════════════════════════════════════╝")
    log.info("Java: {} ({})", System.getProperty("java.version"), System.getProperty("java.vm.name"))
    log.info("OS: {} {} ({})", System.getProperty("os.name"), System.getProperty("os.version"), System.getProperty("os.arch"))
    log.info("Memory: {} MB max", Runtime.getRuntime().maxMemory() / 1024 / 1024)
    log.info("Args: {}", if (args.isEmpty()) "none" else args.joinToString(" "))

    if ("--game" in args) {
        log.info("Running embedded RuneLite game client (login screen via Jagex gamepack)")
    }
    if ("--play" in args) {
        log.info("Running --play live mirror (embedded game + path-traced window)")
    }
    if ("--demo" in args) {
        log.info("Running in DEMO mode (no OSRS connection required)")
    }
    if ("--help" in args || "-h" in args) {
        printHelp()
        return
    }

    try {
        val client = LuminaClient(args)
        client.start()
    } catch (e: Exception) {
        log.error("Fatal error", e)
        System.exit(1)
    }
}

private fun printHelp() {
    println("""
        Lumina OSRS Client - Hardware-Accelerated Path Tracing
        
        Usage: java -jar lumina-all.jar [options]
        
        Options:
          --game              Boot the real OSRS client via embedded RuneLite (login screen)
          --play              Boot game + path-traced LIVE mirror window (camera synced)
          --demo              Run with demo scene (no OSRS connection needed)
          --developer-mode    Enable developer mode and sideloaded plugins
          --jx_session_id ID  Jagex session ID (from Jagex Launcher)
          --jx_character_id C Jagex character ID
          --jx_display_name N Display name
          --help, -h          Show this help
        
        Controls (in-app):
          WASD            Move camera
          Mouse           Look around (click window, ESC to release)
          Space/Shift     Fly up/down
          F1              Toggle FPS display
          F2              Toggle debug info
          F3              Print all settings
          F5              Toggle bloom
          F6              Toggle volumetric fog
          F7              Cycle tone mapping (AgX → ACES → Reinhard → None)
          F8              Cycle upscale quality
          +/-             Adjust exposure
          
        Build fat JAR:
          ./gradlew :launcher:fatJar
          
        Run demo:
          ./gradlew :launcher:runDemo
    """.trimIndent())
}
