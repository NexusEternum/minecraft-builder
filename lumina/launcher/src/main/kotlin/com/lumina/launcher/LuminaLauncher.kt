package com.lumina.launcher

import com.lumina.core.LuminaClient
import org.slf4j.LoggerFactory

private val log = LoggerFactory.getLogger("LuminaLauncher")

fun main(args: Array<String>) {
    log.info("=== Lumina OSRS Client ===")
    log.info("Version: 0.1.0-SNAPSHOT")
    log.info("Java: {} ({})", System.getProperty("java.version"), System.getProperty("java.vm.name"))
    log.info("OS: {} {} ({})", System.getProperty("os.name"), System.getProperty("os.version"), System.getProperty("os.arch"))
    log.info("Args: {}", if (args.isEmpty()) "none" else args.joinToString(" "))

    try {
        val client = LuminaClient(args)
        client.start()
    } catch (e: Exception) {
        log.error("Fatal error", e)
        System.exit(1)
    }
}
