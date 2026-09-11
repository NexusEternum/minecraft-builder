package com.lumina.game.jagex

import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Assumptions.assumeTrue
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.io.TempDir
import java.nio.charset.StandardCharsets
import java.nio.file.Files
import java.nio.file.Path

class JagexSessionServiceTest {
    private val service = JagexSessionService()

    @TempDir
    lateinit var tempDir: Path

    @Test
    fun `parses credentials properties with all JX keys`() {
        val file = tempDir.resolve("credentials.properties")
        Files.writeString(
            file,
            """
            JX_CHARACTER_ID=char-123
            JX_SESSION_ID=session-456
            JX_REFRESH_TOKEN=refresh-789
            JX_DISPLAY_NAME=TestPlayer
            JX_ACCESS_TOKEN=access-abc
            """.trimIndent(),
            StandardCharsets.UTF_8,
        )

        val credentials = service.load(file)
        requireNotNull(credentials)
        assertEquals("char-123", credentials.characterId)
        assertEquals("session-456", credentials.sessionId)
        assertEquals("refresh-789", credentials.refreshToken)
        assertEquals("TestPlayer", credentials.displayName)
        assertEquals("access-abc", credentials.accessToken)
        assertTrue(credentials.hasSessionCredentials)
        assertTrue(credentials.hasAccessTokenCredentials)
    }

    @Test
    fun `round-trips credentials through save and load`() {
        val file = tempDir.resolve("credentials.properties")
        val original = JagexCredentials(
            characterId = "id-1",
            sessionId = "sess-1",
            refreshToken = "",
            displayName = "Player One",
            accessToken = "",
        )

        service.save(file, original)
        val loaded = service.load(file)
        requireNotNull(loaded)
        assertEquals(original, loaded)
    }

    @Test
    fun `toEnvVars prefers session credentials when both sets are present`() {
        val credentials = JagexCredentials(
            characterId = "char",
            sessionId = "sess",
            refreshToken = "refresh",
            displayName = "Name",
            accessToken = "access",
        )

        val env = JagexSessionService.toEnvVars(credentials)
        assertEquals("char", env[JagexCredentials.PROPERTY_CHARACTER_ID])
        assertEquals("sess", env[JagexCredentials.PROPERTY_SESSION_ID])
        assertEquals("Name", env[JagexCredentials.PROPERTY_DISPLAY_NAME])
        assertFalse(env.containsKey(JagexCredentials.PROPERTY_ACCESS_TOKEN))
        assertFalse(env.containsKey(JagexCredentials.PROPERTY_REFRESH_TOKEN))
    }

    @Test
    fun `env injection round-trip sets System getenv`() {
        val testKey = "JX_TEST_VAR"
        val testValue = "lumina-test-value"
        assumeTrue(
            System.getenv(testKey) == null,
            "JX_TEST_VAR already set in the environment; skipping injection test",
        )

        val injected = ProcessEnvironmentInjector.inject(mapOf(testKey to testValue))
        assumeTrue(injected, "Environment injection blocked by JVM module restrictions")

        assertEquals(testValue, System.getenv(testKey))
    }

    @Test
    fun `mask never reveals more than four characters`() {
        assertEquals("****", JagexSessionService.mask("ab"))
        assertEquals("abcd...", JagexSessionService.mask("abcdefghij"))
    }
}
