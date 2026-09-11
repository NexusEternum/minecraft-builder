package com.lumina.scene.osrs

import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test

class XteaKeyServiceTest {
    private val service = XteaKeyService()

    @Test
    fun selectNewestOsrsLiveCacheIdSkipsNewestWhenItHasNoKeys() {
        val cachesJson = """
            [
              {
                "id": 100,
                "game": "oldschool",
                "environment": "live",
                "timestamp": "2026-09-08T10:30:08Z",
                "valid_keys": 0,
                "keys": 0
              },
              {
                "id": 200,
                "game": "oldschool",
                "environment": "live",
                "timestamp": "2026-03-18T11:45:07Z",
                "valid_keys": 2678,
                "keys": 2868
              },
              {
                "id": 300,
                "game": "oldschool",
                "environment": "beta",
                "timestamp": "2026-09-09T10:30:08Z",
                "valid_keys": 2200,
                "keys": 2270
              }
            ]
        """.trimIndent()

        assertEquals(200, service.selectNewestOsrsLiveCacheId(cachesJson))
    }

    @Test
    fun selectNewestOsrsLiveCacheIdFallsBackToKeysWhenValidKeysAbsent() {
        val cachesJson = """
            [
              {
                "id": 400,
                "game": "oldschool",
                "environment": "live",
                "timestamp": "2026-01-01T00:00:00Z",
                "keys": 42
              }
            ]
        """.trimIndent()

        assertEquals(400, service.selectNewestOsrsLiveCacheId(cachesJson))
    }

    @Test
    fun selectNewestOsrsLiveCacheIdReturnsNegativeWhenNoCachesHaveKeys() {
        val cachesJson = """
            [
              {
                "id": 500,
                "game": "oldschool",
                "environment": "live",
                "timestamp": "2026-09-08T10:30:08Z",
                "valid_keys": 0,
                "keys": 10
              }
            ]
        """.trimIndent()

        assertEquals(-1, service.selectNewestOsrsLiveCacheId(cachesJson))
    }

    @Test
    fun cacheKeyCountPrefersValidKeysOverKeys() {
        val cache = mapOf(
            "valid_keys" to 0,
            "keys" to 10,
        )

        assertEquals(0, service.cacheKeyCount(cache))
    }
}
