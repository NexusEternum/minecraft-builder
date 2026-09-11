package com.lumina.core.game

import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.kotlin.registerKotlinModule
import org.slf4j.LoggerFactory
import java.io.File
import java.io.RandomAccessFile
import java.net.ServerSocket
import java.nio.channels.FileChannel
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Handles IPC with the Jagex Launcher for credential exchange.
 *
 * The Jagex Launcher can pass credentials to third-party clients via:
 * 1. Environment variables (JX_ACCESS_TOKEN, JX_REFRESH_TOKEN, etc.)
 * 2. CLI arguments (--jx_access_token, --jx_session_id, etc.)
 * 3. Shared memory / named pipe (platform-specific)
 * 4. Local loopback socket handshake
 *
 * This class implements all four mechanisms and tries them in order.
 */
@Singleton
class JagexLauncherIPC @Inject constructor(
    private val authManager: JagexAuthManager
) {
    private val log = LoggerFactory.getLogger(JagexLauncherIPC::class.java)
    private val mapper = ObjectMapper().registerKotlinModule()

    @Volatile var launcherDetected = false; private set
    @Volatile var launcherVersion: String? = null; private set

    /**
     * Attempt all IPC mechanisms to receive credentials from the Jagex Launcher.
     */
    fun initialize(args: Array<String>): Boolean {
        // Method 1: CLI arguments (highest priority -- this is how RuneLite receives them)
        if (authManager.authenticateFromArgs(args)) {
            launcherDetected = true
            extractLauncherVersion(args)
            log.info("Authenticated via CLI arguments (launcher v{})", launcherVersion ?: "unknown")
            return true
        }

        // Method 2: Environment variables
        if (authManager.authenticateFromLauncher()) {
            launcherDetected = true
            launcherVersion = System.getenv("JX_LAUNCHER_VERSION")
            log.info("Authenticated via environment variables (launcher v{})", launcherVersion ?: "unknown")
            return true
        }

        // Method 3: Shared credential file (Windows)
        if (trySharedCredentialFile()) {
            launcherDetected = true
            log.info("Authenticated via shared credential file")
            return true
        }

        // Method 4: Local socket handshake
        if (tryLocalSocketHandshake(args)) {
            launcherDetected = true
            log.info("Authenticated via local socket handshake")
            return true
        }

        log.info("No Jagex Launcher detected -- legacy login mode")
        return false
    }

    private fun extractLauncherVersion(args: Array<String>) {
        for (i in args.indices) {
            if (args[i] == "--jx_launcher_version" && i + 1 < args.size) {
                launcherVersion = args[i + 1]
                return
            }
            if (args[i].startsWith("--jx_launcher_version=")) {
                launcherVersion = args[i].substringAfter("=")
                return
            }
        }
    }

    /**
     * The Jagex Launcher on Windows writes a temporary credential file
     * that the client can read and then delete.
     */
    private fun trySharedCredentialFile(): Boolean {
        val credPaths = listOf(
            File(System.getProperty("java.io.tmpdir"), "jagex_credentials.json"),
            File(System.getProperty("user.home"), ".jagex/credentials.json"),
            File(System.getenv("LOCALAPPDATA") ?: "", "Jagex/credentials.json")
        )

        for (credFile in credPaths) {
            if (!credFile.exists()) continue
            try {
                RandomAccessFile(credFile, "r").use { raf ->
                    val channel = raf.channel
                    val lock = channel.tryLock(0, Long.MAX_VALUE, true) ?: return@use

                    try {
                        val content = credFile.readText()
                        val json = mapper.readTree(content)

                        val accessToken = json["access_token"]?.asText() ?: return@use
                        authManager.authenticateFromArgs(arrayOf(
                            "--jx_access_token", accessToken,
                            "--jx_refresh_token", json["refresh_token"]?.asText() ?: "",
                            "--jx_session_id", json["session_id"]?.asText() ?: "",
                            "--jx_character_id", json["character_id"]?.asText() ?: "",
                            "--jx_display_name", json["display_name"]?.asText() ?: "Player"
                        ))

                        launcherVersion = json["launcher_version"]?.asText()
                        log.info("Read credentials from {}", credFile.absolutePath)

                        // Delete after reading for security
                        credFile.delete()
                        return true
                    } finally {
                        lock.release()
                    }
                }
            } catch (e: Exception) {
                log.debug("Failed to read credential file {}: {}", credFile, e.message)
            }
        }
        return false
    }

    /**
     * Listen on a local port for the launcher to push credentials via HTTP POST.
     * The launcher discovers the port via a lock file.
     */
    private fun tryLocalSocketHandshake(args: Array<String>): Boolean {
        // Check if a port was specified in args
        var port = -1
        for (i in args.indices) {
            if (args[i] == "--jx_ipc_port" && i + 1 < args.size) {
                port = args[i + 1].toIntOrNull() ?: -1
            }
        }
        if (port < 0) return false

        return try {
            ServerSocket(port).use { server ->
                server.soTimeout = 5000 // 5 second timeout
                val socket = server.accept()
                socket.soTimeout = 3000

                val input = socket.getInputStream().bufferedReader().readText()
                val json = mapper.readTree(input)

                val accessToken = json["access_token"]?.asText() ?: return false
                authManager.authenticateFromArgs(arrayOf(
                    "--jx_access_token", accessToken,
                    "--jx_refresh_token", json["refresh_token"]?.asText() ?: "",
                    "--jx_session_id", json["session_id"]?.asText() ?: "",
                    "--jx_character_id", json["character_id"]?.asText() ?: "",
                    "--jx_display_name", json["display_name"]?.asText() ?: "Player"
                ))

                socket.getOutputStream().write("OK\n".toByteArray())
                socket.close()
                true
            }
        } catch (e: Exception) {
            log.debug("Local socket handshake failed: {}", e.message)
            false
        }
    }

    /**
     * Register Lumina as a third-party client with the Jagex Launcher.
     * Creates the necessary registry entries / config files.
     */
    fun registerWithLauncher(installDir: File) {
        val os = System.getProperty("os.name").lowercase()
        if ("windows" in os) {
            registerWindows(installDir)
        } else if ("linux" in os) {
            registerLinux(installDir)
        }
    }

    private fun registerWindows(installDir: File) {
        // Write a .json manifest that the Jagex Launcher can discover
        val manifest = mapOf(
            "name" to "Lumina",
            "display_name" to "Lumina OSRS Client",
            "executable" to File(installDir, "lumina.bat").absolutePath,
            "arguments" to listOf("--jx_access_token", "\${access_token}",
                "--jx_refresh_token", "\${refresh_token}",
                "--jx_session_id", "\${session_id}",
                "--jx_character_id", "\${character_id}",
                "--jx_display_name", "\${display_name}"),
            "game" to "osrs",
            "version" to "0.1.0"
        )

        val configDir = File(System.getenv("LOCALAPPDATA") ?: System.getProperty("user.home"),
            "Jagex/third-party-clients")
        configDir.mkdirs()

        val manifestFile = File(configDir, "lumina.json")
        manifestFile.writeText(mapper.writerWithDefaultPrettyPrinter().writeValueAsString(manifest))
        log.info("Registered with Jagex Launcher at {}", manifestFile.absolutePath)
    }

    private fun registerLinux(installDir: File) {
        val configDir = File(System.getProperty("user.home"), ".config/jagex/third-party-clients")
        configDir.mkdirs()

        val manifest = mapOf(
            "name" to "Lumina",
            "executable" to File(installDir, "lumina.sh").absolutePath,
            "game" to "osrs",
            "version" to "0.1.0"
        )

        val manifestFile = File(configDir, "lumina.json")
        manifestFile.writeText(mapper.writerWithDefaultPrettyPrinter().writeValueAsString(manifest))
        log.info("Registered with Jagex Launcher at {}", manifestFile.absolutePath)
    }
}
