package com.lumina.scene.osrs

import com.lumina.scene.graph.MaterialComponent
import com.lumina.scene.graph.MeshComponent
import com.lumina.scene.graph.SceneGraph
import com.lumina.scene.graph.Transform
import net.runelite.cache.OverlayManager
import net.runelite.cache.UnderlayManager
import net.runelite.cache.definitions.OverlayDefinition
import net.runelite.cache.definitions.UnderlayDefinition
import net.runelite.cache.fs.Store
import net.runelite.cache.region.Region
import net.runelite.cache.region.RegionLoader
import net.runelite.cache.util.XteaKeyManager
import org.slf4j.LoggerFactory
import java.io.File
import javax.inject.Inject
import javax.inject.Singleton
import kotlin.math.sqrt

@Singleton
class OsrsMapLoader @Inject constructor(
    private val sceneGraph: SceneGraph
) {
    private val log = LoggerFactory.getLogger(OsrsMapLoader::class.java)

    fun loadRegion(cacheDir: File, regionId: Int): Boolean {
        if (!cacheDir.isDirectory) {
            log.warn("OSRS cache directory not found: {}", cacheDir.absolutePath)
            return false
        }

        return try {
            Store(cacheDir).use { store ->
                store.load()

                val underlayManager = UnderlayManager(store)
                underlayManager.load()

                val overlayManager = OverlayManager(store)
                overlayManager.load()

                val regionLoader = RegionLoader(store, XteaKeyManager())
                val mapDef = try {
                    regionLoader.loadMapDef(regionId)
                } catch (e: Exception) {
                    log.warn("Map definition not found for region {}: {}", regionId, e.message)
                    return false
                }

                val region = Region(regionId)
                region.loadTerrain(mapDef)

                buildTerrainScene(region, underlayManager, overlayManager, regionId)
                true
            }
        } catch (e: Exception) {
            log.warn("Failed to load OSRS region {} from {}: {}", regionId, cacheDir.absolutePath, e.message)
            log.debug("Region load failure details", e)
            false
        }
    }

    private fun buildTerrainScene(
        region: Region,
        underlayManager: UnderlayManager,
        overlayManager: OverlayManager,
        regionId: Int
    ) {
        sceneGraph.clear()

        val plane = 0
        var tileCount = 0
        var triangleCount = 0
        var meshCount = 0

        for (chunkX in 0 until CHUNKS_PER_AXIS) {
            for (chunkY in 0 until CHUNKS_PER_AXIS) {
                val startX = chunkX * CHUNK_SIZE
                val startY = chunkY * CHUNK_SIZE

                val avgColor = averageChunkColor(
                    region, plane, startX, startY,
                    underlayManager, overlayManager
                )

                val mesh = buildChunkMesh(region, plane, startX, startY)
                if (mesh.triangleCount == 0) continue

                val node = sceneGraph.createNode("terrain_${regionId}_${chunkX}_${chunkY}")
                node.addComponent(Transform())
                node.addComponent(mesh)
                node.addComponent(
                    MaterialComponent(
                        albedo = avgColor,
                        roughness = 0.9f,
                        metallic = 0.0f
                    )
                )

                tileCount += CHUNK_SIZE * CHUNK_SIZE
                triangleCount += mesh.triangleCount
                meshCount++
            }
        }

        log.info(
            "Loaded OSRS region {}: {} tiles, {} meshes, {} triangles",
            regionId, tileCount, meshCount, triangleCount
        )
    }

    private fun averageChunkColor(
        region: Region,
        plane: Int,
        startX: Int,
        startY: Int,
        underlayManager: UnderlayManager,
        overlayManager: OverlayManager
    ): FloatArray {
        var rSum = 0f
        var gSum = 0f
        var bSum = 0f
        var count = 0

        for (tx in startX until startX + CHUNK_SIZE) {
            for (ty in startY until startY + CHUNK_SIZE) {
                val color = tileColor(region, plane, tx, ty, underlayManager, overlayManager)
                rSum += color[0]
                gSum += color[1]
                bSum += color[2]
                count++
            }
        }

        if (count == 0) return floatArrayOf(0.4f, 0.5f, 0.3f)
        return floatArrayOf(rSum / count, gSum / count, bSum / count)
    }

    private fun tileColor(
        region: Region,
        plane: Int,
        x: Int,
        y: Int,
        underlayManager: UnderlayManager,
        overlayManager: OverlayManager
    ): FloatArray {
        val overlayId = region.getOverlayId(plane, x, y)
        if (overlayId > 0) {
            val overlay = overlayManager.provide(overlayId)
            if (overlay != null) {
                val rgb = overlayRgb(overlay)
                if (rgb != null) return rgb
            }
        }

        val underlayId = region.getUnderlayId(plane, x, y)
        if (underlayId > 0) {
            val underlay = underlayManager.provide(underlayId)
            if (underlay != null) {
                return packedRgbToFloats(underlay.getColor())
            }
        }

        return floatArrayOf(0.35f, 0.45f, 0.25f)
    }

    private fun overlayRgb(overlay: OverlayDefinition): FloatArray? {
        if (overlay.getTexture() >= 0) return null
        if (overlay.getRgbColor() != 0) return packedRgbToFloats(overlay.getRgbColor())
        if (overlay.getSecondaryRgbColor() != 0) return packedRgbToFloats(overlay.getSecondaryRgbColor())
        return null
    }

    private fun buildChunkMesh(region: Region, plane: Int, startX: Int, startY: Int): MeshComponent {
        val gridSize = CHUNK_SIZE + 1
        val vertexCount = gridSize * gridSize
        val triangleCount = CHUNK_SIZE * CHUNK_SIZE * 2

        val verts = FloatArray(vertexCount * FLOATS_PER_VERTEX)
        val indices = IntArray(triangleCount * 3)

        for (localY in 0 until gridSize) {
            for (localX in 0 until gridSize) {
                val tileX = startX + localX
                val tileY = startY + localY
                val vi = localY * gridSize + localX
                val off = vi * FLOATS_PER_VERTEX

                val height = region.getTileHeight(plane, tileX, tileY)
                verts[off] = tileX * TILE_SCALE
                verts[off + 1] = -height / 128f * TILE_SCALE
                verts[off + 2] = tileY * TILE_SCALE

                val normal = computeNormal(region, plane, tileX, tileY)
                verts[off + 3] = normal[0]
                verts[off + 4] = normal[1]
                verts[off + 5] = normal[2]
                verts[off + 6] = localX.toFloat() / CHUNK_SIZE
                verts[off + 7] = localY.toFloat() / CHUNK_SIZE
            }
        }

        var ii = 0
        for (localY in 0 until CHUNK_SIZE) {
            for (localX in 0 until CHUNK_SIZE) {
                val v00 = localY * gridSize + localX
                val v10 = v00 + 1
                val v01 = v00 + gridSize
                val v11 = v01 + 1

                indices[ii++] = v00
                indices[ii++] = v10
                indices[ii++] = v11
                indices[ii++] = v00
                indices[ii++] = v11
                indices[ii++] = v01
            }
        }

        return MeshComponent(verts, indices, vertexCount, triangleCount)
    }

    private fun computeNormal(region: Region, plane: Int, x: Int, y: Int): FloatArray {
        val hL = sampleHeight(region, plane, x - 1, y)
        val hR = sampleHeight(region, plane, x + 1, y)
        val hD = sampleHeight(region, plane, x, y - 1)
        val hU = sampleHeight(region, plane, x, y + 1)

        val dx = (hR - hL) / (2f * 128f)
        val dz = (hU - hD) / (2f * 128f)
        val dy = 1f

        val len = sqrt(dx * dx + dy * dy + dz * dz)
        if (len <= 0f) return floatArrayOf(0f, 1f, 0f)
        return floatArrayOf(-dx / len, dy / len, -dz / len)
    }

    private fun sampleHeight(region: Region, plane: Int, x: Int, y: Int): Int {
        val clampedX = x.coerceIn(0, REGION_SIZE)
        val clampedY = y.coerceIn(0, REGION_SIZE)
        return region.getTileHeight(plane, clampedX, clampedY)
    }

    companion object {
        const val TILE_SCALE = 2.56f
        private const val REGION_SIZE = 64
        private const val CHUNK_SIZE = 8
        private const val CHUNKS_PER_AXIS = REGION_SIZE / CHUNK_SIZE
        private const val FLOATS_PER_VERTEX = 8

        fun packedRgbToFloats(rgb: Int): FloatArray {
            val r = ((rgb shr 16) and 0xFF) / 255f
            val g = ((rgb shr 8) and 0xFF) / 255f
            val b = (rgb and 0xFF) / 255f
            return floatArrayOf(r, g, b)
        }
    }
}
