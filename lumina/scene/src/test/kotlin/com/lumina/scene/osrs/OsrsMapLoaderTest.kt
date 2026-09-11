package com.lumina.scene.osrs

import com.lumina.scene.graph.SceneGraph
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Test
import java.io.File

class OsrsMapLoaderTest {
    @Test
    fun loadRegionReturnsFalseForMissingCache() {
        val loader = OsrsMapLoader(SceneGraph(), XteaKeyService())
        val missingCache = File("/nonexistent/osrs/cache/path")
        assertFalse(loader.loadRegion(missingCache, 12850))
    }

    @Test
    fun loadRegionsReturnsFalseForEmptyAfterFilteringInvalidIds() {
        val loader = OsrsMapLoader(SceneGraph(), XteaKeyService())
        val missingCache = File("/nonexistent/osrs/cache/path")
        assertFalse(loader.loadRegions(missingCache, intArrayOf(0, -1), 3200, 3200))
    }

    @Test
    fun regionWorldOffsetMatchesKnownRegionId() {
        val (ox, oz) = OsrsCoordinateMapper.regionWorldOffset(12850, 3200, 3200)
        assertEquals(0f, ox)
        assertEquals(0f, oz)

        val (eastX, _) = OsrsCoordinateMapper.regionWorldOffset(13106, 3200, 3200)
        assertEquals(64f * OsrsMapLoader.TILE_SCALE, eastX)
    }
}
