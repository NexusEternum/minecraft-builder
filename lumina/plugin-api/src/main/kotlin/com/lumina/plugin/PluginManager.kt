package com.lumina.plugin

import com.google.inject.Guice
import com.google.inject.Injector
import com.google.inject.Module
import org.slf4j.LoggerFactory
import java.io.File
import java.net.URLClassLoader
import java.util.ServiceLoader
import java.util.concurrent.CopyOnWriteArrayList
import java.util.jar.JarFile

class PluginManager(
    private val parentInjector: Injector,
    private val developerMode: Boolean = false
) {
    private val log = LoggerFactory.getLogger(PluginManager::class.java)
    private val _plugins = CopyOnWriteArrayList<Plugin>()
    val plugins: List<Plugin> get() = _plugins.toList()
    private val eventBus: EventBus = parentInjector.getInstance(EventBus::class.java)

    fun loadPluginsFromClasspath(): List<Plugin> {
        val loaded = mutableListOf<Plugin>()
        val classes = scanClasspathForPlugins()
        for (clazz in classes) {
            try {
                val descriptor = clazz.getAnnotation(PluginDescriptor::class.java) ?: continue
                if (descriptor.developerPlugin && !developerMode) continue
                val plugin = instantiatePlugin(clazz)
                _plugins.add(plugin)
                loaded.add(plugin)
                log.info("Loaded plugin: {} ({})", descriptor.name, clazz.name)
            } catch (e: Exception) {
                log.error("Failed to load plugin: {}", clazz.name, e)
            }
        }
        return loaded
    }

    fun loadPluginsFromDirectory(directory: File): List<Plugin> {
        if (!directory.isDirectory) return emptyList()
        val loaded = mutableListOf<Plugin>()
        val jars = directory.listFiles { f -> f.extension == "jar" } ?: return emptyList()
        for (jar in jars) {
            try {
                log.info("Side-loading plugin JAR: {}", jar.name)
                val classLoader = URLClassLoader(arrayOf(jar.toURI().toURL()), javaClass.classLoader)
                val classes = scanJarForPlugins(jar, classLoader)
                for (clazz in classes) {
                    val descriptor = clazz.getAnnotation(PluginDescriptor::class.java) ?: continue
                    val plugin = instantiatePlugin(clazz, classLoader)
                    _plugins.add(plugin)
                    loaded.add(plugin)
                    log.info("Loaded sideloaded plugin: {} ({})", descriptor.name, clazz.name)
                }
            } catch (e: Exception) {
                log.error("Failed to load plugin JAR: {}", jar.name, e)
            }
        }
        return loaded
    }

    fun startPlugin(plugin: Plugin) {
        try {
            plugin.startUp()
            eventBus.register(plugin)
            log.info("Started plugin: {}", plugin.name)
        } catch (e: Exception) {
            log.error("Failed to start plugin: {}", plugin.name, e)
        }
    }

    fun stopPlugin(plugin: Plugin) {
        try {
            eventBus.unregister(plugin)
            plugin.shutDown()
            log.info("Stopped plugin: {}", plugin.name)
        } catch (e: Exception) {
            log.error("Failed to stop plugin: {}", plugin.name, e)
        }
    }

    fun startAll() = _plugins.forEach { startPlugin(it) }
    fun stopAll() = _plugins.reversed().forEach { stopPlugin(it) }

    @Suppress("UNCHECKED_CAST")
    private fun scanClasspathForPlugins(): List<Class<out Plugin>> {
        // Scan using ServiceLoader pattern - plugins register via META-INF/services
        val result = mutableListOf<Class<out Plugin>>()
        try {
            val loader = ServiceLoader.load(Plugin::class.java)
            for (plugin in loader) {
                result.add(plugin::class.java as Class<out Plugin>)
            }
        } catch (e: Exception) {
            log.debug("ServiceLoader scan: {}", e.message)
        }
        return result
    }

    @Suppress("UNCHECKED_CAST")
    private fun scanJarForPlugins(jar: File, classLoader: ClassLoader): List<Class<out Plugin>> {
        val result = mutableListOf<Class<out Plugin>>()
        JarFile(jar).use { jf ->
            for (entry in jf.entries()) {
                if (!entry.name.endsWith(".class")) continue
                val className = entry.name.removeSuffix(".class").replace('/', '.')
                try {
                    val clazz = classLoader.loadClass(className)
                    if (Plugin::class.java.isAssignableFrom(clazz) && clazz != Plugin::class.java) {
                        result.add(clazz as Class<out Plugin>)
                    }
                } catch (e: Throwable) {
                    // skip classes that can't load
                }
            }
        }
        return result
    }

    private fun instantiatePlugin(clazz: Class<out Plugin>, classLoader: ClassLoader? = null): Plugin {
        val childInjector = parentInjector.createChildInjector(Module { binder ->
            classLoader?.let { binder.bind(ClassLoader::class.java).toInstance(it) }
        })
        val plugin = childInjector.getInstance(clazz)
        plugin.injector = childInjector
        return plugin
    }
}
