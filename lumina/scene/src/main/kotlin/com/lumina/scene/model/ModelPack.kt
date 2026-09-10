package com.lumina.scene.model

import com.google.gson.Gson
import com.google.gson.annotations.SerializedName
import org.slf4j.LoggerFactory
import java.io.File
import java.util.concurrent.ConcurrentHashMap
import java.util.zip.ZipFile
import javax.inject.Singleton

data class ModelPackManifest(
    val name: String,
    val version: String = "1.0",
    val author: String = "",
    val description: String = "",
    val models: Map<String, ModelEntry> = emptyMap(),
    val textures: Map<String, String> = emptyMap()
)

data class ModelEntry(
    val mesh: String,
    val materials: Map<String, String> = emptyMap(),
    val lod: List<String> = emptyList(),
    @SerializedName("scale") val scale: Float = 1f
)

data class LoadedModel(
    val vertexData: FloatArray,
    val indexData: IntArray,
    val vertexCount: Int,
    val triangleCount: Int,
    val materialPaths: Map<String, String>
) {
    override fun equals(other: Any?) = this === other
    override fun hashCode() = System.identityHashCode(this)
}

@Singleton
class ModelPackManager {
    private val log = LoggerFactory.getLogger(ModelPackManager::class.java)
    private val gson = Gson()
    private val packs = ConcurrentHashMap<String, ModelPackManifest>()
    private val modelOverrides = ConcurrentHashMap<String, LoadedModel>()

    fun loadPack(file: File): ModelPackManifest? {
        if (!file.exists()) return null
        return try {
            ZipFile(file).use { zip ->
                val manifestEntry = zip.getEntry("manifest.json")
                    ?: throw IllegalArgumentException("No manifest.json in pack")
                val manifest = zip.getInputStream(manifestEntry).bufferedReader().use {
                    gson.fromJson(it, ModelPackManifest::class.java)
                }
                packs[manifest.name] = manifest
                log.info("Loaded model pack: {} v{} ({} models, {} textures)",
                    manifest.name, manifest.version,
                    manifest.models.size, manifest.textures.size)
                manifest
            }
        } catch (e: Exception) {
            log.error("Failed to load model pack: {}", file.name, e)
            null
        }
    }

    fun hasOverride(osrsKey: String): Boolean = modelOverrides.containsKey(osrsKey)

    fun getOverride(osrsKey: String): LoadedModel? = modelOverrides[osrsKey]

    fun getLoadedPacks(): List<ModelPackManifest> = packs.values.toList()

    fun unloadPack(name: String) {
        packs.remove(name)
        log.info("Unloaded model pack: {}", name)
    }
}
