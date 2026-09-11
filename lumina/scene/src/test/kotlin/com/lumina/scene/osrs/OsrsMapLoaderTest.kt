package com.lumina.scene.osrs

import com.lumina.scene.graph.SceneGraph
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
}
