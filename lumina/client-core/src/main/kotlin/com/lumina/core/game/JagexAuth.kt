package com.lumina.core.game

import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.kotlin.registerKotlinModule
import okhttp3.FormBody
import okhttp3.OkHttpClient
import okhttp3.Request
import org.slf4j.LoggerFactory
import java.time.Instant
import javax.inject.Inject
import javax.inject.Singleton

data class JagexCredentials(
    val accessToken: String,
    val refreshToken: String,
    val idToken: String,
    val sessionId: String,
    val accountId: String,
    val displayName: String,
    val expiresAt: Instant
) {
    val isExpired: Boolean get() = Instant.now().isAfter(expiresAt)
}

@Singleton
class JagexAuthManager @Inject constructor(
    private val httpClient: OkHttpClient
) {
    private val log = LoggerFactory.getLogger(JagexAuthManager::class.java)
    private val mapper = ObjectMapper().registerKotlinModule()

    @Volatile
    var credentials: JagexCredentials? = null
        private set

    val isAuthenticated: Boolean get() = credentials != null && !credentials!!.isExpired

    /**
     * Receives credentials from the Jagex Launcher via environment variables / IPC.
     * The Jagex Launcher sets JX_* environment variables before launching the client.
     */
    fun authenticateFromLauncher(): Boolean {
        val accessToken = System.getenv("JX_ACCESS_TOKEN")
        val refreshToken = System.getenv("JX_REFRESH_TOKEN")
        val sessionId = System.getenv("JX_SESSION_ID")
        val characterId = System.getenv("JX_CHARACTER_ID")
        val displayName = System.getenv("JX_DISPLAY_NAME")

        if (accessToken.isNullOrBlank()) {
            log.warn("No Jagex Launcher credentials found in environment")
            return false
        }

        credentials = JagexCredentials(
            accessToken = accessToken,
            refreshToken = refreshToken ?: "",
            idToken = "",
            sessionId = sessionId ?: "",
            accountId = characterId ?: "",
            displayName = displayName ?: "Unknown",
            expiresAt = Instant.now().plusSeconds(3600)
        )

        log.info("Authenticated via Jagex Launcher as: {}", credentials?.displayName)
        return true
    }

    /**
     * Receives credentials passed as command-line arguments from the Jagex Launcher.
     * RuneLite receives them this way when configured as a third-party client.
     */
    fun authenticateFromArgs(args: Array<String>): Boolean {
        val argMap = mutableMapOf<String, String>()
        var i = 0
        while (i < args.size) {
            when {
                args[i].startsWith("--jx_") -> {
                    val key = args[i].removePrefix("--")
                    val value = if (i + 1 < args.size && !args[i + 1].startsWith("--")) {
                        i++
                        args[i]
                    } else ""
                    argMap[key] = value
                }
                args[i].contains("=") && args[i].startsWith("--jx_") -> {
                    val (key, value) = args[i].removePrefix("--").split("=", limit = 2)
                    argMap[key] = value
                }
            }
            i++
        }

        val accessToken = argMap["jx_access_token"]
        if (accessToken.isNullOrBlank()) return false

        credentials = JagexCredentials(
            accessToken = accessToken,
            refreshToken = argMap["jx_refresh_token"] ?: "",
            idToken = "",
            sessionId = argMap["jx_session_id"] ?: "",
            accountId = argMap["jx_character_id"] ?: "",
            displayName = argMap["jx_display_name"] ?: "Unknown",
            expiresAt = Instant.now().plusSeconds(3600)
        )

        log.info("Authenticated via launcher args as: {}", credentials?.displayName)
        return true
    }

    fun refreshAccessToken(): Boolean {
        val creds = credentials ?: return false
        if (creds.refreshToken.isBlank()) return false

        return try {
            val body = FormBody.Builder()
                .add("grant_type", "refresh_token")
                .add("refresh_token", creds.refreshToken)
                .build()

            val request = Request.Builder()
                .url("https://account.jagex.com/oauth2/token")
                .post(body)
                .build()

            httpClient.newCall(request).execute().use { response ->
                if (!response.isSuccessful) {
                    log.error("Token refresh failed: {}", response.code)
                    return false
                }

                val json = mapper.readTree(response.body?.string())
                credentials = creds.copy(
                    accessToken = json["access_token"].asText(),
                    expiresAt = Instant.now().plusSeconds(json["expires_in"].asLong())
                )
                log.info("Access token refreshed, expires at {}", credentials?.expiresAt)
                true
            }
        } catch (e: Exception) {
            log.error("Failed to refresh token", e)
            false
        }
    }

    fun getGameToken(): String? {
        if (credentials == null) return null
        if (credentials!!.isExpired) refreshAccessToken()
        return credentials?.accessToken
    }
}
