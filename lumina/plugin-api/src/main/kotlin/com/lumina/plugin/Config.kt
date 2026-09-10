package com.lumina.plugin

import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.google.gson.reflect.TypeToken
import org.slf4j.LoggerFactory
import java.io.File
import java.util.concurrent.ConcurrentHashMap
import javax.inject.Inject
import javax.inject.Named
import javax.inject.Singleton

@Target(AnnotationTarget.PROPERTY, AnnotationTarget.FIELD)
@Retention(AnnotationRetention.RUNTIME)
annotation class ConfigItem(
    val keyName: String,
    val name: String,
    val description: String = "",
    val section: String = ""
)

@Target(AnnotationTarget.PROPERTY, AnnotationTarget.FIELD)
@Retention(AnnotationRetention.RUNTIME)
annotation class Range(val min: Int = Int.MIN_VALUE, val max: Int = Int.MAX_VALUE)

@Singleton
class ConfigManager @Inject constructor(@Named("configDir") private val configDir: File) {
    private val log = LoggerFactory.getLogger(ConfigManager::class.java)
    private val gson: Gson = GsonBuilder().setPrettyPrinting().create()
    private val configs = ConcurrentHashMap<String, MutableMap<String, Any?>>()

    init {
        configDir.mkdirs()
    }

    fun <T> getConfig(group: String, key: String, defaultValue: T): T {
        val groupConfig = configs.getOrPut(group) { loadConfig(group) }
        @Suppress("UNCHECKED_CAST")
        return (groupConfig[key] as? T) ?: defaultValue
    }

    fun setConfig(group: String, key: String, value: Any?) {
        val groupConfig = configs.getOrPut(group) { loadConfig(group) }
        groupConfig[key] = value
        saveConfig(group, groupConfig)
    }

    private fun loadConfig(group: String): MutableMap<String, Any?> {
        val file = File(configDir, "$group.json")
        if (!file.exists()) return mutableMapOf()
        return try {
            val type = object : TypeToken<MutableMap<String, Any?>>() {}.type
            gson.fromJson(file.readText(), type) ?: mutableMapOf()
        } catch (e: Exception) {
            log.error("Failed to load config: {}", group, e)
            mutableMapOf()
        }
    }

    private fun saveConfig(group: String, data: Map<String, Any?>) {
        try {
            File(configDir, "$group.json").writeText(gson.toJson(data))
        } catch (e: Exception) {
            log.error("Failed to save config: {}", group, e)
        }
    }
}
