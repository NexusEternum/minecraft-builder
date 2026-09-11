package com.lumina.game.jagex

/**
 * Parsed contents of RuneLite's `~/.runelite/credentials.properties`.
 *
 * Keys match those written by the RuneLite client when launched via the Jagex Launcher
 * with `--insecure-write-credentials` (see runelite/runelite wiki "Using Jagex Accounts").
 */
data class JagexCredentials(
    val characterId: String = "",
    val sessionId: String = "",
    val refreshToken: String = "",
    val displayName: String = "",
    val accessToken: String = "",
) {
    val hasSessionCredentials: Boolean
        get() = sessionId.isNotBlank() && characterId.isNotBlank()

    val hasAccessTokenCredentials: Boolean
        get() = accessToken.isNotBlank()

    fun isEmpty(): Boolean =
        characterId.isBlank() &&
            sessionId.isBlank() &&
            refreshToken.isBlank() &&
            displayName.isBlank() &&
            accessToken.isBlank()

    fun toPropertiesMap(): Map<String, String> = buildMap {
        put(PROPERTY_CHARACTER_ID, characterId)
        put(PROPERTY_SESSION_ID, sessionId)
        put(PROPERTY_REFRESH_TOKEN, refreshToken)
        put(PROPERTY_DISPLAY_NAME, displayName)
        put(PROPERTY_ACCESS_TOKEN, accessToken)
    }

    companion object {
        const val PROPERTY_CHARACTER_ID = "JX_CHARACTER_ID"
        const val PROPERTY_SESSION_ID = "JX_SESSION_ID"
        const val PROPERTY_REFRESH_TOKEN = "JX_REFRESH_TOKEN"
        const val PROPERTY_DISPLAY_NAME = "JX_DISPLAY_NAME"
        const val PROPERTY_ACCESS_TOKEN = "JX_ACCESS_TOKEN"

        val PROPERTY_KEYS = listOf(
            PROPERTY_CHARACTER_ID,
            PROPERTY_SESSION_ID,
            PROPERTY_REFRESH_TOKEN,
            PROPERTY_DISPLAY_NAME,
            PROPERTY_ACCESS_TOKEN,
        )

        fun fromProperties(properties: Map<String, String>): JagexCredentials =
            JagexCredentials(
                characterId = properties[PROPERTY_CHARACTER_ID]?.trim() ?: "",
                sessionId = properties[PROPERTY_SESSION_ID]?.trim() ?: "",
                refreshToken = properties[PROPERTY_REFRESH_TOKEN]?.trim() ?: "",
                displayName = properties[PROPERTY_DISPLAY_NAME]?.trim() ?: "",
                accessToken = properties[PROPERTY_ACCESS_TOKEN]?.trim() ?: "",
            )
    }
}
