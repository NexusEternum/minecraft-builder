package com.lumina.scene.osrs

import com.google.gson.Gson
import com.google.gson.JsonArray
import com.google.gson.reflect.TypeToken
import net.runelite.cache.util.XteaKeyManager
import org.slf4j.LoggerFactory
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.net.URI
import java.net.http.HttpClient
import java.net.http.HttpRequest
import java.net.http.HttpResponse
import java.time.Duration
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class XteaKeyService @Inject constructor() {
    private val log = LoggerFactory.getLogger(XteaKeyService::class.java)
    private val gson = Gson()
    private val httpClient = HttpClient.newBuilder()
        .connectTimeout(Duration.ofSeconds(15))
        .build()

    fun buildKeyManager(): XteaKeyManager {
        val manager = XteaKeyManager()
        val keysFile = resolveKeysFile()
        if (keysFile != null) {
            FileInputStream(keysFile).use { manager.loadKeys(it) }
        }
        return manager
    }

    private fun resolveKeysFile(): File? {
        val localFile = File(System.getProperty("user.home"), ".lumina/xtea-keys.json")
        if (localFile.isFile) {
            log.info("Using local XTEA keys from {}", localFile.absolutePath)
            return localFile
        }

        val downloaded = downloadAndSaveKeys(localFile)
        return downloaded
    }

    private fun downloadAndSaveKeys(target: File): File? {
        return try {
            val cachesRequest = HttpRequest.newBuilder()
                .uri(URI.create(CACHES_URL))
                .GET()
                .timeout(Duration.ofSeconds(30))
                .build()
            val cachesResponse = httpClient.send(cachesRequest, HttpResponse.BodyHandlers.ofString())
            if (cachesResponse.statusCode() != 200) {
                log.warn("Failed to download OpenRS2 cache list: HTTP {}", cachesResponse.statusCode())
                return null
            }

            val cachesBody = cachesResponse.body()
            val cacheId = selectNewestOsrsLiveCacheId(cachesBody)
            if (cacheId < 0) {
                log.warn("No oldschool/live cache entry with published XTEA keys found in OpenRS2 archive")
                return null
            }

            val keysUrl = "https://archive.openrs2.org/caches/runescape/$cacheId/keys.json"
            val publishedKeyCount = keyCountForOsrsLiveCache(cachesBody, cacheId)
            log.info(
                "Downloading XTEA keys from OpenRS2 cache {} ({} published keys)",
                cacheId,
                publishedKeyCount,
            )
            val keysRequest = HttpRequest.newBuilder()
                .uri(URI.create(keysUrl))
                .GET()
                .timeout(Duration.ofSeconds(60))
                .build()
            val keysResponse = httpClient.send(keysRequest, HttpResponse.BodyHandlers.ofString())
            if (keysResponse.statusCode() != 200) {
                log.warn("Failed to download XTEA keys for cache {}: HTTP {}", cacheId, keysResponse.statusCode())
                return null
            }

            val runeliteFormat = convertOpenRs2Keys(keysResponse.body())
            if (runeliteFormat.isEmpty()) {
                log.warn("OpenRS2 cache {} returned no XTEA keys", cacheId)
                return null
            }

            target.parentFile?.mkdirs()
            FileOutputStream(target).use { out ->
                out.write(gson.toJson(runeliteFormat).toByteArray(Charsets.UTF_8))
            }
            log.info("Saved {} XTEA keys to {}", runeliteFormat.size, target.absolutePath)
            target
        } catch (e: Exception) {
            log.warn("Failed to download XTEA keys: {}", e.message)
            log.debug("XTEA download failure details", e)
            null
        }
    }

    internal fun selectNewestOsrsLiveCacheId(cachesJson: String): Int {
        val type = object : TypeToken<List<Map<String, Any?>>>() {}.type
        val caches: List<Map<String, Any?>> = gson.fromJson(cachesJson, type)
        val newest = caches
            .filter { it["game"] == "oldschool" && it["environment"] == "live" }
            .filter { cacheKeyCount(it) > 0 }
            .maxByOrNull { it["timestamp"]?.toString().orEmpty() }
        return when (val id = newest?.get("id")) {
            is Number -> id.toInt()
            is String -> id.toIntOrNull() ?: -1
            else -> -1
        }
    }

    internal fun cacheKeyCount(cache: Map<String, Any?>): Int {
        val validKeys = cache["valid_keys"]
        if (validKeys != null) {
            return numericToInt(validKeys)
        }
        return numericToInt(cache["keys"])
    }

    private fun keyCountForOsrsLiveCache(cachesJson: String, cacheId: Int): Int {
        val type = object : TypeToken<List<Map<String, Any?>>>() {}.type
        val caches: List<Map<String, Any?>> = gson.fromJson(cachesJson, type)
        val cache = caches.firstOrNull {
            it["game"] == "oldschool" && it["environment"] == "live" && cacheIdFromEntry(it) == cacheId
        }
        return cache?.let { cacheKeyCount(it) } ?: 0
    }

    private fun cacheIdFromEntry(cache: Map<String, Any?>): Int? {
        return when (val id = cache["id"]) {
            is Number -> id.toInt()
            is String -> id.toIntOrNull()
            else -> null
        }
    }

    private fun numericToInt(value: Any?): Int {
        return when (value) {
            is Number -> value.toInt()
            is String -> value.toIntOrNull() ?: 0
            else -> 0
        }
    }

    internal fun convertOpenRs2Keys(keysJson: String): List<Map<String, Any>> {
        val array = gson.fromJson(keysJson, JsonArray::class.java) ?: return emptyList()
        val converted = LinkedHashMap<Int, IntArray>()

        for (element in array) {
            if (!element.isJsonObject) continue
            val entry = element.asJsonObject
            val mapsquare = entry.get("mapsquare")?.asInt ?: continue
            val keyArray = entry.getAsJsonArray("key") ?: continue
            if (keyArray.size() != 4) continue

            val keys = IntArray(4) { keyArray[it].asInt }
            converted[mapsquare] = keys
        }

        return converted.map { (region, keys) ->
            mapOf("region" to region, "keys" to keys.toList())
        }
    }

    companion object {
        private const val CACHES_URL = "https://archive.openrs2.org/caches.json"
    }
}
