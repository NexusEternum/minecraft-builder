package com.lumina.scene.osrs

import com.lumina.scene.graph.MeshComponent
import com.lumina.scene.graph.SceneGraph
import net.runelite.cache.OverlayManager
import net.runelite.cache.UnderlayManager
import net.runelite.cache.definitions.MapDefinition
import net.runelite.cache.fs.Store
import net.runelite.cache.region.Region
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test
import java.io.File

class OsrsChunkMeshTest {
    @Test
    fun allWaterChunkProducesWaterMeshWithoutTerrainNode() {
        val region = Region(12850)
        val tiles = Array(4) { Array(64) { Array(64) { MapDefinition.Tile() } } }
        for (x in 0 until 8) {
            for (z in 0 until 8) {
                val tile = tiles[0][x][z]
                tile.height = 0
                tile.overlayId = 7 // stored id for WATER_FLAT (definition 6)
            }
        }
        val map = MapDefinition()
        map.setTiles(tiles)
        region.loadTerrain(map)

        val store = Store(File.createTempFile("lumina-cache", "").parentFile!!)
        val overlayManager = OverlayManager(store)
        val underlayManager = UnderlayManager(store)
        val textureColors = emptyTextureCache()
        val loader = OsrsMapLoader(SceneGraph(), XteaKeyService())

        val chunkMeshes = loader.buildChunkMeshesForTest(
            region = region,
            plane = 0,
            startX = 0,
            startY = 0,
            underlayManager = underlayManager,
            overlayManager = overlayManager,
            textureColors = textureColors,
            regionId = 12850,
            originBaseX = 0,
            originBaseY = 0
        )

        assertEquals(0, chunkMeshes.terrain.triangleCount, "all-water chunk must not build terrain tris")
        assertTrue(chunkMeshes.water.triangleCount > 0, "all-water chunk must build water tris")
        assertFalse(chunkMeshes.terrain.isRenderable())
        assertTrue(chunkMeshes.water.isRenderable())

        val graph = SceneGraph()
        val (terrainPlaced, waterPlaced) = loader.placeChunkMeshNodes(
            graph,
            regionId = 12850,
            plane = 0,
            chunkX = 0,
            chunkY = 0,
            terrainMesh = chunkMeshes.terrain,
            waterMesh = chunkMeshes.water
        )

        assertFalse(terrainPlaced, "empty terrain mesh must not create a scene node")
        assertTrue(waterPlaced, "water mesh must create a scene node")

        val meshNodes = graph.nodesWithComponent(MeshComponent::class.java)
        assertEquals(1, meshNodes.size)
        assertTrue(meshNodes[0].name.startsWith("water_"))
        assertTrue(meshNodes[0].getComponent(MeshComponent::class.java)!!.isRenderable())
    }

    private fun emptyTextureCache(): OsrsTextureColorCache {
        val ctor = OsrsTextureColorCache::class.java.getDeclaredConstructor(Map::class.java)
        ctor.isAccessible = true
        return ctor.newInstance(emptyMap<Int, FloatArray>()) as OsrsTextureColorCache
    }
}
