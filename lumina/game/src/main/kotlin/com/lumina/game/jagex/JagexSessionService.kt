package com.lumina.game.jagex

import org.slf4j.LoggerFactory
import java.io.IOException
import java.net.URI
import java.net.URLEncoder
import java.net.http.HttpClient
import java.net.http.HttpRequest
import java.net.http.HttpResponse
import java.nio.charset.StandardCharsets
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.nio.file.StandardCopyOption
import java.nio.file.attribute.PosixFilePermission
import java.time.Duration
import java.util.Properties
import kotlin.io.path.exists

/**
 * Loads Jagex launcher credentials from RuneLite's `credentials.properties`, optionally
 * refreshes OAuth access tokens, and injects `JX_*` environment variables for in-process
 * RuneLite boot.
 *
 * RuneLite writes this file when launched through the Jagex Launcher with
 * `--insecure-write-credentials` ([runelite/runelite] wiki). The open-source RuneLite
 * launcher passes stored values to the client as environment variables; Lumina mirrors that
 * behaviour via [ProcessEnvironmentInjector] because it calls [net.runelite.client.RuneLite.main]
 * in-process.
 */
class JagexSessionService(
    private val httpClient: HttpClient = HttpClient.newBuilder()
        .followRedirects(HttpClient.Redirect.NORMAL)
        .connectTimeout(Duration.ofSeconds(15))
        .build(),
) {
    private val log = LoggerFactory.getLogger(JagexSessionService::class.java)

    fun credentialsPath(): Path {
        val override = System.getProperty(CREDENTIALS_PROPERTY)?.trim()
        if (!override.isNullOrEmpty()) {
            return Paths.get(override)
        }
        return Paths.get(System.getProperty("user.home"), ".runelite", CREDENTIALS_FILE_NAME)
    }

    /**
     * Loads credentials, refreshes when possible, writes updates back to disk, and injects
     * env vars unless the process already has Jagex launcher credentials.
     *
     * @return true when credentials were loaded and applied (or already present in the environment)
     */
    fun prepareForRuneliteLaunch(): Boolean {
        if (ProcessEnvironmentInjector.jagexEnvAlreadyPresent()) {
            log.info("Jagex launcher environment variables already present; skipping credentials file and injection")
            logEnvPresence()
            return true
        }

        val path = credentialsPath()
        if (!path.exists()) {
            log.info(
                "No Jagex credentials file at {}. One-time setup: launch RuneLite through the " +
                    "Jagex Launcher with \"Remember me\" enabled (add --insecure-write-credentials " +
                    "in RuneLite Configure → Client arguments if developing). Lumina will then reuse " +
                    "the saved session from {}.",
                path,
                path,
            )
            return false
        }

        val loaded = load(path)
        if (loaded == null || loaded.isEmpty()) {
            log.warn(
                "Jagex credentials file exists at {} but contains no usable values. " +
                    "Re-export via the Jagex Launcher flow described in the RuneLite wiki.",
                path,
            )
            return false
        }

        log.info("Loaded Jagex credentials from {}", path)
        logCredentialPresence(loaded)

        val refreshed = refreshIfNeeded(loaded)
        if (refreshed != loaded) {
            try {
                save(path, refreshed)
                log.info("Wrote refreshed Jagex credentials back to {}", path)
            } catch (e: IOException) {
                log.warn("Could not persist refreshed credentials to {}: {}", path, e.message)
            }
        }

        val envVars = toEnvVars(refreshed)
        if (envVars.isEmpty()) {
            log.warn(
                "Jagex credentials file at {} has no values to inject; RuneLite will show the login screen",
                path,
            )
            return false
        }

        val injected = ProcessEnvironmentInjector.inject(envVars)
        if (injected) {
            log.info("Injected Jagex launcher environment variables for in-process RuneLite boot")
            logEnvPresence()
        }
        return injected
    }

    fun load(path: Path): JagexCredentials? {
        return try {
            val properties = Properties()
            Files.newBufferedReader(path, StandardCharsets.UTF_8).use { reader ->
                properties.load(reader)
            }
            val map = JagexCredentials.PROPERTY_KEYS.associateWith { key ->
                properties.getProperty(key, "")
            }
            JagexCredentials.fromProperties(map)
        } catch (e: IOException) {
            log.warn("Failed to read Jagex credentials from {}: {}", path, e.message)
            null
        }
    }

    fun save(path: Path, credentials: JagexCredentials) {
        val properties = Properties()
        credentials.toPropertiesMap().forEach { (key, value) ->
            properties.setProperty(key, value)
        }

        val parent = path.parent
        if (parent != null) {
            Files.createDirectories(parent)
        }

        val temp = Files.createTempFile(parent ?: path.parent ?: Paths.get("."), "credentials", ".tmp")
        try {
            Files.newBufferedWriter(temp, StandardCharsets.UTF_8).use { writer ->
                properties.store(writer, "Lumina Jagex credentials (compatible with RuneLite launcher)")
            }
            trySetOwnerOnlyPermissions(temp)
            Files.move(temp, path, StandardCopyOption.REPLACE_EXISTING, StandardCopyOption.ATOMIC_MOVE)
        } finally {
            Files.deleteIfExists(temp)
        }
        trySetOwnerOnlyPermissions(path)
    }

    /**
     * OAuth refresh for the access-token credential path.
     *
     * Matches the Jagex desktop launcher client (`com_jagex_auth_desktop_launcher`) token
     * endpoint used by community launchers such as jagex-launcher-linux
     * (`POST https://account.jagex.com/oauth2/token`, `grant_type=refresh_token`).
     *
     * Session-id credentials (`JX_SESSION_ID` / `JX_CHARACTER_ID`) are passed through;
     * when a refresh token is present we validate the game session and log if it may be stale.
     */
    fun refreshIfNeeded(credentials: JagexCredentials): JagexCredentials {
        if (credentials.hasAccessTokenCredentials && credentials.refreshToken.isNotBlank()) {
            return refreshAccessToken(credentials)
        }

        if (credentials.hasSessionCredentials) {
            if (credentials.refreshToken.isNotBlank()) {
                log.debug("JX_REFRESH_TOKEN present with session credentials; session refresh is not implemented, passing through stored session")
            }
            if (!validateGameSession(credentials.sessionId)) {
                log.warn(
                    "Stored JX_SESSION_ID may be expired or invalid. Re-launch RuneLite through the " +
                        "Jagex Launcher to refresh credentials.properties, or use \"End sessions\" on " +
                        "runescape.com and export again.",
                )
            }
        }

        return credentials
    }

    private fun refreshAccessToken(credentials: JagexCredentials): JagexCredentials {
        val body = buildFormBody(
            "grant_type" to "refresh_token",
            "client_id" to JAGEX_LAUNCHER_CLIENT_ID,
            "refresh_token" to credentials.refreshToken,
        )

        val request = HttpRequest.newBuilder()
            .uri(URI.create("$ACCOUNT_ORIGIN/oauth2/token"))
            .header("Accept", "application/json")
            .header("Content-Type", "application/x-www-form-urlencoded")
            .timeout(Duration.ofSeconds(30))
            .POST(HttpRequest.BodyPublishers.ofString(body))
            .build()

        return try {
            val response = httpClient.send(request, HttpResponse.BodyHandlers.ofString())
            if (response.statusCode() !in 200..299) {
                log.warn(
                    "Jagex token refresh failed (HTTP {}). Stored access token may be stale; " +
                        "re-launch through the Jagex Launcher to renew credentials.properties",
                    response.statusCode(),
                )
                return credentials
            }

            val json = parseJsonObject(response.body())
            val accessToken = json["access_token"]?.trim()
            if (accessToken.isNullOrEmpty()) {
                log.warn("Jagex token refresh returned no access_token; using stored credentials")
                return credentials
            }

            val refreshToken = json["refresh_token"]?.trim()?.takeIf { it.isNotEmpty() }
                ?: credentials.refreshToken

            log.info("Refreshed Jagex access token (masked: {})", mask(accessToken))
            credentials.copy(
                accessToken = accessToken,
                refreshToken = refreshToken,
            )
        } catch (e: Exception) {
            log.warn(
                "Jagex token refresh request failed: {}. Using stored credentials; they may be stale.",
                e.message,
            )
            credentials
        }
    }

    private fun validateGameSession(sessionId: String): Boolean {
        val request = HttpRequest.newBuilder()
            .uri(URI.create("$AUTH_ORIGIN/game-session/v1/accounts"))
            .header("Accept", "application/json")
            .header("Authorization", "Bearer $sessionId")
            .timeout(Duration.ofSeconds(15))
            .GET()
            .build()

        return try {
            val response = httpClient.send(request, HttpResponse.BodyHandlers.discarding())
            when (response.statusCode()) {
                200 -> true
                401 -> false
                else -> {
                    log.debug("Game session validation returned HTTP {}; assuming session is still usable", response.statusCode())
                    true
                }
            }
        } catch (e: Exception) {
            log.debug("Could not validate game session: {}", e.message)
            true
        }
    }

    private fun logCredentialPresence(credentials: JagexCredentials) {
        for ((name, value) in credentials.toPropertiesMap()) {
            if (value.isBlank()) {
                log.info("Credential {} not set in file", name)
            } else {
                log.info("Credential {} present (masked: {})", name, mask(value))
            }
        }
    }

    private fun logEnvPresence() {
        for (name in JagexCredentials.PROPERTY_KEYS) {
            val value = System.getenv(name)
            if (value.isNullOrBlank()) {
                log.info("Jagex launcher env {} not set", name)
            } else {
                log.info("Jagex launcher env {} present (masked: {})", name, mask(value))
            }
        }
    }

    companion object {
        const val CREDENTIALS_PROPERTY = "lumina.jagex.credentials"
        const val CREDENTIALS_FILE_NAME = "credentials.properties"

        private const val ACCOUNT_ORIGIN = "https://account.jagex.com"
        private const val AUTH_ORIGIN = "https://auth.jagex.com"
        private const val JAGEX_LAUNCHER_CLIENT_ID = "com_jagex_auth_desktop_launcher"

        fun mask(value: String): String {
            if (value.length <= 4) return "****"
            return value.take(4) + "..."
        }

        fun toEnvVars(credentials: JagexCredentials): Map<String, String> {
            val all = credentials.toPropertiesMap().filterValues { it.isNotBlank() }
            if (credentials.hasSessionCredentials && credentials.hasAccessTokenCredentials) {
                // Jagex/RuneLite treat session and access-token credential sets as mutually exclusive.
                LoggerFactory.getLogger(JagexSessionService::class.java).warn(
                    "credentials.properties contains both session and access-token fields; " +
                        "preferring session credentials (JX_SESSION_ID / JX_CHARACTER_ID)",
                )
                return all.filterKeys {
                    it == JagexCredentials.PROPERTY_CHARACTER_ID ||
                        it == JagexCredentials.PROPERTY_SESSION_ID ||
                        it == JagexCredentials.PROPERTY_DISPLAY_NAME
                }
            }
            return all
        }

        private fun buildFormBody(vararg pairs: Pair<String, String>): String =
            pairs.joinToString("&") { (key, value) ->
                "${encode(key)}=${encode(value)}"
            }

        private fun encode(value: String): String =
            URLEncoder.encode(value, StandardCharsets.UTF_8)

        private fun parseJsonObject(body: String): Map<String, String> {
            val result = mutableMapOf<String, String>()
            val trimmed = body.trim()
            if (!trimmed.startsWith("{") || !trimmed.endsWith("}")) {
                return result
            }
            val inner = trimmed.removePrefix("{").removeSuffix("}").trim()
            if (inner.isEmpty()) {
                return result
            }
            // Minimal JSON string extractor — sufficient for Jagex token responses.
            val pattern = Regex("\"([^\"]+)\"\\s*:\\s*\"((?:\\\\.|[^\"\\\\])*)\"")
            for (match in pattern.findAll(inner)) {
                val key = match.groupValues[1]
                val raw = match.groupValues[2]
                result[key] = raw
                    .replace("\\\\", "\\")
                    .replace("\\\"", "\"")
                    .replace("\\n", "\n")
                    .replace("\\r", "\r")
                    .replace("\\t", "\t")
            }
            return result
        }

        private fun trySetOwnerOnlyPermissions(path: Path) {
            try {
                val perms = setOf(
                    PosixFilePermission.OWNER_READ,
                    PosixFilePermission.OWNER_WRITE,
                )
                Files.setPosixFilePermissions(path, perms)
            } catch (_: UnsupportedOperationException) {
                // Windows or unsupported FS
            } catch (_: IOException) {
                // Best effort
            }
        }
    }
}
