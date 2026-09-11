package com.lumina.core.game

import org.slf4j.LoggerFactory
import java.io.File
import java.net.URL
import java.net.URLClassLoader
import javax.inject.Inject
import javax.inject.Named
import javax.inject.Singleton

@Singleton
class GameJarLoader @Inject constructor(
    @Named("dataDir") private val dataDir: File
) {
    private val log = LoggerFactory.getLogger(GameJarLoader::class.java)
    private var gameClassLoader: ClassLoader? = null
    private val gameJars = mutableListOf<File>()

    val isLoaded: Boolean get() = gameClassLoader != null

    fun loadGameJars(runeliteDir: File): ClassLoader {
        val repoDir = File(runeliteDir, "repository2")
        if (!repoDir.isDirectory) {
            throw IllegalStateException(
                "RuneLite repository not found at ${repoDir.absolutePath}. " +
                "Please install RuneLite first."
            )
        }

        val jars = repoDir.listFiles { f -> f.extension == "jar" }
            ?: throw IllegalStateException("No JARs found in ${repoDir.absolutePath}")

        gameJars.addAll(jars)
        val urls = jars.map { it.toURI().toURL() }.toTypedArray()
        gameClassLoader = URLClassLoader(urls, javaClass.classLoader)

        log.info("Loaded {} game JARs from {}", jars.size, repoDir.absolutePath)
        jars.filter { it.name.startsWith("client-") || it.name.startsWith("injected-client-") }
            .forEach { log.info("  Game client: {}", it.name) }

        return gameClassLoader!!
    }

    fun findClientClass(): Class<*>? {
        val cl = gameClassLoader ?: return null
        return try {
            cl.loadClass("net.runelite.client.RuneLite")
        } catch (e: ClassNotFoundException) {
            log.warn("RuneLite main class not found, trying raw OSRS client")
            try {
                cl.loadClass("client")
            } catch (e2: ClassNotFoundException) {
                log.error("No game client class found")
                null
            }
        }
    }

    fun getGameClassLoader(): ClassLoader = gameClassLoader
        ?: throw IllegalStateException("Game JARs not loaded")

    fun getClientVersion(): String? {
        return gameJars.firstOrNull { it.name.startsWith("client-") }
            ?.name?.removePrefix("client-")?.removeSuffix(".jar")
    }
}
