package com.lumina.scene.osrs

import com.lumina.scene.extract.OsrsSceneExtractor
import com.lumina.scene.graph.MaterialComponent
import com.lumina.scene.graph.MeshComponent
import com.lumina.scene.graph.SceneGraph
import com.lumina.scene.graph.Transform
import net.runelite.cache.IndexType
import net.runelite.cache.ObjectManager
import net.runelite.cache.OverlayManager
import net.runelite.cache.UnderlayManager
import net.runelite.cache.definitions.ModelDefinition
import net.runelite.cache.definitions.OverlayDefinition
import net.runelite.cache.definitions.UnderlayDefinition
import net.runelite.cache.definitions.loaders.ModelLoader
import net.runelite.cache.fs.Store
import net.runelite.cache.region.Region
import net.runelite.cache.region.RegionLoader
import org.slf4j.LoggerFactory
import java.io.File
import javax.inject.Inject
import javax.inject.Singleton
import kotlin.math.sqrt

@Singleton
class OsrsMapLoader @Inject constructor(
    private val sceneGraph: SceneGraph,
    private val xteaKeyService: XteaKeyService
) {
    private val log = LoggerFactory.getLogger(OsrsMapLoader::class.java)

    var lastRegionCenterWorldX: Float = 81f
        private set
    var lastRegionCenterWorldY: Float = 30f
        private set
    var lastRegionCenterWorldZ: Float = 81f
        private set

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

                val objectManager = ObjectManager(store)
                objectManager.load()

                val xteaKeyManager = xteaKeyService.buildKeyManager()
                val regionLoader = RegionLoader(store, xteaKeyManager)

                val mapDef = try {
                    regionLoader.loadMapDef(regionId)
                } catch (e: Exception) {
                    log.warn("Map definition not found for region {}: {}", regionId, e.message)
                    return false
                }
                if (mapDef == null) {
                    log.warn("Map definition not found for region {}", regionId)
                    return false
                }

                val region = Region(regionId)
                region.loadTerrain(mapDef)

                val locDef = try {
                    regionLoader.loadLocDef(regionId)
                } catch (e: Exception) {
                    log.debug("Location definition unavailable for region {}: {}", regionId, e.message)
                    null
                }
                if (locDef != null) {
                    region.loadLocations(locDef)
                } else {
                    log.warn("No object locations for region {} (missing XTEA keys or loc archive)", regionId)
                }

                buildScene(region, underlayManager, overlayManager, objectManager, store, regionId)
                true
            }
        } catch (e: Exception) {
            log.warn("Failed to load OSRS region {} from {}: {}", regionId, cacheDir.absolutePath, e.message)
            log.debug("Region load failure details", e)
            false
        }
    }

    private fun buildScene(
        region: Region,
        underlayManager: UnderlayManager,
        overlayManager: OverlayManager,
        objectManager: ObjectManager,
        store: Store,
        regionId: Int
    ) {
        sceneGraph.clear()

        val plane = 0
        var tileCount = 0
        var terrainTriangleCount = 0
        var terrainMeshCount = 0

        for (chunkX in 0 until CHUNKS_PER_AXIS) {
            for (chunkY in 0 until CHUNKS_PER_AXIS) {
                val startX = chunkX * CHUNK_SIZE
                val startY = chunkY * CHUNK_SIZE

                val mesh = buildChunkMesh(
                    region, plane, startX, startY,
                    underlayManager, overlayManager
                )
                if (mesh.triangleCount == 0) continue

                val node = sceneGraph.createNode("terrain_${regionId}_${chunkX}_${chunkY}")
                node.addComponent(Transform())
                node.addComponent(mesh)
                node.addComponent(
                    MaterialComponent(
                        albedo = floatArrayOf(1f, 1f, 1f),
                        roughness = 0.9f,
                        metallic = 2.0f
                    )
                )

                tileCount += CHUNK_SIZE * CHUNK_SIZE
                terrainTriangleCount += mesh.triangleCount
                terrainMeshCount++
            }
        }

        val centerTileX = REGION_SIZE / 2
        val centerTileY = REGION_SIZE / 2
        val centerHeight = -sampleHeight(region, plane, centerTileX, centerTileY) / 128f * TILE_SCALE
        lastRegionCenterWorldX = centerTileX * TILE_SCALE
        lastRegionCenterWorldY = centerHeight + 25f
        lastRegionCenterWorldZ = centerTileY * TILE_SCALE

        val objectStats = loadObjects(region, objectManager, store, regionId, plane)

        log.info(
            "Loaded OSRS region {}: {} tiles, {} terrain meshes, {} terrain triangles, " +
                "{} objects placed (skipped-no-model={}, skipped-type={}, deduped={})",
            regionId,
            tileCount,
            terrainMeshCount,
            terrainTriangleCount,
            objectStats.placed,
            objectStats.skippedNoModel,
            objectStats.skippedType,
            objectStats.dedupedMeshes
        )
    }

    private data class ObjectLoadStats(
        val placed: Int = 0,
        val skippedNoModel: Int = 0,
        val skippedType: Int = 0,
        val dedupedMeshes: Int = 0
    )

    private fun loadObjects(
        region: Region,
        objectManager: ObjectManager,
        store: Store,
        regionId: Int,
        plane: Int
    ): ObjectLoadStats {
        val locations = region.locations ?: return ObjectLoadStats()
        val baseX = region.baseX
        val baseY = region.baseY

        val modelLoader = ModelLoader()
        val modelDefCache = HashMap<Int, ModelDefinition>()
        val meshCache = HashMap<Pair<Int, Int>, MeshComponent>()

        var placed = 0
        var skippedNoModel = 0
        var skippedType = 0
        var dedupedMeshes = 0
        var capWarned = false

        for (location in locations) {
            if (placed >= MAX_OBJECT_NODES) {
                if (!capWarned) {
                    log.warn("Object node cap ({}) reached for region {}", MAX_OBJECT_NODES, regionId)
                    capWarned = true
                }
                break
            }

            if (!isSupportedLocationType(location.type)) {
                skippedType++
                continue
            }

            val position = location.position ?: continue
            if (!rendersOnPlane(position.z, plane)) continue

            try {
                val objectDef = objectManager.getObject(location.id)
                if (objectDef == null) {
                    skippedNoModel++
                    continue
                }

                val modelId = resolveModelId(objectDef.objectModels, objectDef.objectTypes, location.type)
                if (modelId < 0) {
                    skippedNoModel++
                    continue
                }

                val orientation = location.orientation and 3
                val cacheKey = modelId to orientation
                var mesh = meshCache[cacheKey]
                if (mesh == null) {
                    val modelDef = loadModelDefinition(store, modelLoader, modelDefCache, modelId)
                    if (modelDef == null) {
                        skippedNoModel++
                        continue
                    }
                    mesh = modelDefinitionToMesh(modelDef, orientation)
                    if (mesh.triangleCount == 0) {
                        skippedNoModel++
                        continue
                    }
                    meshCache[cacheKey] = mesh
                } else {
                    dedupedMeshes++
                }

                val localTileX = position.x - baseX
                val localTileY = position.y - baseY
                if (localTileX !in 0 until REGION_SIZE || localTileY !in 0 until REGION_SIZE) {
                    continue
                }

                val worldX = localTileX * TILE_SCALE
                val worldZ = localTileY * TILE_SCALE
                val terrainY = -sampleHeight(region, plane, localTileX, localTileY) / 128f * TILE_SCALE
                val offsetScale = MODEL_SCALE
                val worldY = terrainY +
                    (-objectDef.offsetHeight * offsetScale) +
                    (-objectDef.offsetY * offsetScale)

                val node = sceneGraph.createNode("obj_${location.id}_${localTileX}_${localTileY}")
                node.addComponent(
                    Transform(
                        x = worldX + objectDef.offsetX * offsetScale,
                        y = worldY,
                        z = worldZ
                    )
                )
                node.addComponent(mesh)
                node.addComponent(
                    MaterialComponent(
                        albedo = floatArrayOf(1f, 1f, 1f),
                        roughness = 0.85f,
                        metallic = 2.0f
                    )
                )
                placed++
            } catch (e: Exception) {
                log.debug(
                    "Failed to place object {} type {} at {}: {}",
                    location.id,
                    location.type,
                    location.position,
                    e.message
                )
                skippedNoModel++
            }
        }

        return ObjectLoadStats(placed, skippedNoModel, skippedType, dedupedMeshes)
    }

    private fun loadModelDefinition(
        store: Store,
        modelLoader: ModelLoader,
        cache: MutableMap<Int, ModelDefinition>,
        modelId: Int
    ): ModelDefinition? {
        cache[modelId]?.let { return it }

        val index = store.getIndex(IndexType.MODELS) ?: return null
        val archive = index.getArchive(modelId) ?: return null
        val storage = store.storage
        val compressed = storage.loadArchive(archive)
        val data = archive.decompress(compressed)
        val modelDef = modelLoader.load(modelId, data) ?: return null
        cache[modelId] = modelDef
        return modelDef
    }

    private fun modelDefinitionToMesh(model: ModelDefinition, orientation: Int): MeshComponent {
        val vertexCount = model.vertexCount
        val faceCount = model.faceCount
        if (vertexCount <= 0 || faceCount <= 0) {
            return MeshComponent(FloatArray(0), IntArray(0), 0, 0)
        }

        val srcX = model.vertexX
        val srcY = model.vertexY
        val srcZ = model.vertexZ
        val idx1 = model.faceIndices1
        val idx2 = model.faceIndices2
        val idx3 = model.faceIndices3
        val faceColors = model.faceColors
        val faceTransparencies = model.faceTransparencies

        val rotatedX = IntArray(vertexCount)
        val rotatedY = IntArray(vertexCount)
        val rotatedZ = IntArray(vertexCount)
        for (i in 0 until vertexCount) {
            val x = srcX[i]
            val y = srcY[i]
            val z = srcZ[i]
            when (orientation and 3) {
                0 -> {
                    rotatedX[i] = x
                    rotatedY[i] = y
                    rotatedZ[i] = z
                }
                1 -> {
                    rotatedX[i] = z
                    rotatedY[i] = y
                    rotatedZ[i] = -x
                }
                2 -> {
                    rotatedX[i] = -x
                    rotatedY[i] = y
                    rotatedZ[i] = -z
                }
                else -> {
                    rotatedX[i] = -z
                    rotatedY[i] = y
                    rotatedZ[i] = x
                }
            }
        }

        var visibleFaces = 0
        for (face in 0 until faceCount) {
            if (faceTransparencies != null && (faceTransparencies[face].toInt() and 0xFF) > 250) {
                continue
            }
            visibleFaces++
        }

        if (visibleFaces == 0) {
            return MeshComponent(FloatArray(0), IntArray(0), 0, 0)
        }

        val outVertexCount = visibleFaces * 3
        val verts = FloatArray(outVertexCount * FLOATS_PER_VERTEX)
        val indices = IntArray(visibleFaces * 3)

        var vi = 0
        var ii = 0
        for (face in 0 until faceCount) {
            if (faceTransparencies != null && (faceTransparencies[face].toInt() and 0xFF) > 250) {
                continue
            }

            val i1 = idx1[face]
            val i2 = idx2[face]
            val i3 = idx3[face]

            val ax = rotatedX[i1] * MODEL_SCALE
            val ay = -rotatedY[i1] * MODEL_SCALE
            val az = rotatedZ[i1] * MODEL_SCALE
            val bx = rotatedX[i2] * MODEL_SCALE
            val by = -rotatedY[i2] * MODEL_SCALE
            val bz = rotatedZ[i2] * MODEL_SCALE
            val cx = rotatedX[i3] * MODEL_SCALE
            val cy = -rotatedY[i3] * MODEL_SCALE
            val cz = rotatedZ[i3] * MODEL_SCALE

            val e1x = bx - ax
            val e1y = by - ay
            val e1z = bz - az
            val e2x = cx - ax
            val e2y = cy - ay
            val e2z = cz - az
            var nx = e1y * e2z - e1z * e2y
            var ny = e1z * e2x - e1x * e2z
            var nz = e1x * e2y - e1y * e2x
            val len = sqrt(nx * nx + ny * ny + nz * nz)
            if (len > 0f) {
                nx /= len
                ny /= len
                nz /= len
            } else {
                nx = 0f
                ny = 1f
                nz = 0f
            }

            val hsl = if (faceColors != null && face < faceColors.size) faceColors[face].toInt() else 0
            val rgb = OsrsSceneExtractor.hslToRgb(hsl)
            val packedColor = packTileColorToUv(rgb)

            val cornerX = floatArrayOf(ax, bx, cx)
            val cornerY = floatArrayOf(ay, by, cy)
            val cornerZ = floatArrayOf(az, bz, cz)
            val baseVertex = vi

            for (corner in 0 until 3) {
                val off = vi * FLOATS_PER_VERTEX
                verts[off] = cornerX[corner]
                verts[off + 1] = cornerY[corner]
                verts[off + 2] = cornerZ[corner]
                verts[off + 3] = nx
                verts[off + 4] = ny
                verts[off + 5] = nz
                verts[off + 6] = packedColor
                verts[off + 7] = 0f
                vi++
            }

            indices[ii++] = baseVertex
            indices[ii++] = baseVertex + 1
            indices[ii++] = baseVertex + 2
        }

        return MeshComponent(verts, indices, outVertexCount, visibleFaces)
    }

    private fun resolveModelId(objectModels: IntArray?, objectTypes: IntArray?, locationType: Int): Int {
        if (objectModels == null || objectModels.isEmpty()) return -1
        if (objectTypes != null) {
            for (i in objectTypes.indices) {
                if (objectTypes[i] == locationType && i < objectModels.size) {
                    return objectModels[i]
                }
            }
        }
        return objectModels[0]
    }

    private fun isSupportedLocationType(type: Int): Boolean {
        return type in 0..3 || type in 10..11 || type == 22
    }

    private fun rendersOnPlane(locationPlane: Int, viewPlane: Int): Boolean {
        return locationPlane == viewPlane
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

        return blendedUnderlayColor(region, plane, x, y, underlayManager)
    }

    private fun blendedUnderlayColor(
        region: Region,
        plane: Int,
        x: Int,
        y: Int,
        underlayManager: UnderlayManager
    ): FloatArray {
        var rSum = 0f
        var gSum = 0f
        var bSum = 0f
        var count = 0

        for (dy in -2..2) {
            for (dx in -2..2) {
                val sx = (x + dx).coerceIn(0, REGION_SIZE - 1)
                val sy = (y + dy).coerceIn(0, REGION_SIZE - 1)
                val underlayId = region.getUnderlayId(plane, sx, sy)
                if (underlayId <= 0) continue
                val underlay = underlayManager.provide(underlayId) ?: continue
                val rgb = packedRgbToFloats(underlay.color)
                rSum += rgb[0]
                gSum += rgb[1]
                bSum += rgb[2]
                count++
            }
        }

        if (count > 0) {
            return floatArrayOf(rSum / count, gSum / count, bSum / count)
        }
        return floatArrayOf(0.35f, 0.45f, 0.25f)
    }

    private fun overlayRgb(overlay: OverlayDefinition): FloatArray? {
        if (overlay.texture >= 0) return null
        if (overlay.rgbColor != 0) return packedRgbToFloats(overlay.rgbColor)
        if (overlay.secondaryRgbColor != 0) return packedRgbToFloats(overlay.secondaryRgbColor)
        return null
    }

    private fun buildChunkMesh(
        region: Region,
        plane: Int,
        startX: Int,
        startY: Int,
        underlayManager: UnderlayManager,
        overlayManager: OverlayManager
    ): MeshComponent {
        val tilesPerChunk = CHUNK_SIZE * CHUNK_SIZE
        val vertexCount = tilesPerChunk * 4
        val triangleCount = tilesPerChunk * 2

        val verts = FloatArray(vertexCount * FLOATS_PER_VERTEX)
        val indices = IntArray(triangleCount * 3)

        var vi = 0
        var ii = 0
        for (localY in 0 until CHUNK_SIZE) {
            for (localX in 0 until CHUNK_SIZE) {
                val tileX = startX + localX
                val tileY = startY + localY
                val packedColor = packTileColorToUv(
                    tileColor(region, plane, tileX, tileY, underlayManager, overlayManager)
                )
                val baseVertex = vi

                for (corner in TILE_CORNERS) {
                    val cx = tileX + corner[0]
                    val cy = tileY + corner[1]
                    val off = vi * FLOATS_PER_VERTEX

                    val height = sampleHeight(region, plane, cx, cy)
                    verts[off] = cx * TILE_SCALE
                    verts[off + 1] = -height / 128f * TILE_SCALE
                    verts[off + 2] = cy * TILE_SCALE

                    val normal = computeNormal(region, plane, cx, cy)
                    verts[off + 3] = normal[0]
                    verts[off + 4] = normal[1]
                    verts[off + 5] = normal[2]
                    verts[off + 6] = packedColor
                    verts[off + 7] = 0f

                    vi++
                }

                indices[ii++] = baseVertex
                indices[ii++] = baseVertex + 1
                indices[ii++] = baseVertex + 2
                indices[ii++] = baseVertex
                indices[ii++] = baseVertex + 2
                indices[ii++] = baseVertex + 3
            }
        }

        return MeshComponent(verts, indices, vertexCount, triangleCount)
    }

    private fun packTileColorToUv(color: FloatArray): Float {
        val r = (color[0] * 255f).toInt().coerceIn(0, 255)
        val g = (color[1] * 255f).toInt().coerceIn(0, 255)
        val b = (color[2] * 255f).toInt().coerceIn(0, 255)
        return Float.fromBits((r shl 16) or (g shl 8) or b)
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
        val clampedX = x.coerceIn(0, REGION_SIZE - 1)
        val clampedY = y.coerceIn(0, REGION_SIZE - 1)
        return region.getTileHeight(plane, clampedX, clampedY)
    }

    companion object {
        const val TILE_SCALE = 2.56f
        private const val MODEL_SCALE = TILE_SCALE / 128f
        private const val REGION_SIZE = 64
        private const val CHUNK_SIZE = 8
        private const val CHUNKS_PER_AXIS = REGION_SIZE / CHUNK_SIZE
        private const val FLOATS_PER_VERTEX = 8
        private const val MAX_OBJECT_NODES = 1500
        private val TILE_CORNERS = arrayOf(
            intArrayOf(0, 0),
            intArrayOf(1, 0),
            intArrayOf(1, 1),
            intArrayOf(0, 1)
        )

        fun packedRgbToFloats(rgb: Int): FloatArray {
            val r = ((rgb shr 16) and 0xFF) / 255f
            val g = ((rgb shr 8) and 0xFF) / 255f
            val b = (rgb and 0xFF) / 255f
            return floatArrayOf(r, g, b)
        }
    }
}
