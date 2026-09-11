package com.lumina.scene.osrs

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

    /** Scene-local origin in world tile coords used by the last multi-region load. */
    var sceneOriginBaseX: Int = 0
        private set
    var sceneOriginBaseY: Int = 0
        private set

    fun loadRegion(cacheDir: File, regionId: Int): Boolean {
        sceneOriginBaseX = 0
        sceneOriginBaseY = 0
        return loadRegions(cacheDir, intArrayOf(regionId), 0, 0)
    }

    /**
     * Loads multiple OSRS regions into one scene using a scene-local origin.
     * All geometry is positioned relative to ([originBaseX], [originBaseY]) in world tile coords.
     */
    fun loadRegions(
        cacheDir: File,
        regionIds: IntArray,
        originBaseX: Int,
        originBaseY: Int
    ): Boolean {
        if (regionIds.isEmpty()) {
            log.warn("No region IDs supplied for multi-region load")
            return false
        }
        if (!cacheDir.isDirectory) {
            log.warn("OSRS cache directory not found: {}", cacheDir.absolutePath)
            return false
        }

        sceneOriginBaseX = originBaseX
        sceneOriginBaseY = originBaseY

        val validRegionIds = OsrsCoordinateMapper.normalizeRegionIds(regionIds)
        if (validRegionIds.isEmpty()) {
            log.warn("No valid region IDs in {}", regionIds.contentToString())
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

                sceneGraph.clear()
                var loadedCount = 0
                var totalTiles = 0
                var totalTerrainMeshes = 0
                var totalTerrainTriangles = 0
                var totalObjects = 0
                var sceneObjectsPlaced = 0

                for (regionId in validRegionIds) {
                    val mapDef = try {
                        regionLoader.loadMapDef(regionId)
                    } catch (e: Exception) {
                        log.warn("Map definition not found for region {}: {}", regionId, e.message)
                        continue
                    }
                    if (mapDef == null) {
                        log.warn("Map definition not found for region {}", regionId)
                        continue
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

                    val stats = buildScene(
                        region,
                        underlayManager,
                        overlayManager,
                        objectManager,
                        store,
                        regionId,
                        originBaseX,
                        originBaseY,
                        append = loadedCount > 0,
                        sceneObjectsPlaced = sceneObjectsPlaced
                    )
                    loadedCount++
                    totalTiles += stats.tileCount
                    totalTerrainMeshes += stats.terrainMeshCount
                    totalTerrainTriangles += stats.terrainTriangleCount
                    totalObjects += stats.objectPlaced
                    sceneObjectsPlaced += stats.objectPlaced
                }

                if (loadedCount == 0) {
                    log.warn("Failed to load any regions from {}", cacheDir.absolutePath)
                    return false
                }

                lastRegionCenterWorldX = REGION_SIZE / 2f * TILE_SCALE
                lastRegionCenterWorldY = 30f
                lastRegionCenterWorldZ = REGION_SIZE / 2f * TILE_SCALE

                log.info(
                    "Loaded {} OSRS regions at origin ({}, {}): {} tiles, {} terrain meshes, {} terrain triangles, {} objects",
                    loadedCount,
                    originBaseX,
                    originBaseY,
                    totalTiles,
                    totalTerrainMeshes,
                    totalTerrainTriangles,
                    totalObjects
                )
                true
            }
        } catch (e: Exception) {
            log.warn("Failed to load OSRS regions from {}: {}", cacheDir.absolutePath, e.message)
            log.debug("Multi-region load failure details", e)
            false
        }
    }

    private data class SceneBuildStats(
        val tileCount: Int = 0,
        val terrainMeshCount: Int = 0,
        val terrainTriangleCount: Int = 0,
        val objectPlaced: Int = 0
    )

    private fun buildScene(
        region: Region,
        underlayManager: UnderlayManager,
        overlayManager: OverlayManager,
        objectManager: ObjectManager,
        store: Store,
        regionId: Int,
        originBaseX: Int,
        originBaseY: Int,
        append: Boolean,
        sceneObjectsPlaced: Int = 0
    ): SceneBuildStats {
        if (!append) {
            sceneGraph.clear()
        }

        if (!bridgeHandlingLogged) {
            log.info("Bridge tile plane shifting (tile setting 0x2) not implemented — plane 0 only for bridged tiles")
            bridgeHandlingLogged = true
        }

        val locationTilesByPlane = buildLocationTileMasks(region)
        var tileCount = 0
        var terrainTriangleCount = 0
        var terrainMeshCount = 0

        for (plane in 0 until PLANE_COUNT) {
            for (chunkX in 0 until CHUNKS_PER_AXIS) {
                for (chunkY in 0 until CHUNKS_PER_AXIS) {
                    val startX = chunkX * CHUNK_SIZE
                    val startY = chunkY * CHUNK_SIZE

                    val mesh = buildChunkMesh(
                        region,
                        plane,
                        startX,
                        startY,
                        underlayManager,
                        overlayManager,
                        regionId,
                        originBaseX,
                        originBaseY,
                        locationTilesByPlane[plane]
                    )
                    if (mesh.triangleCount == 0) continue

                    val node = sceneGraph.createNode("terrain_${regionId}_p${plane}_${chunkX}_${chunkY}")
                    node.addComponent(Transform())
                    node.addComponent(mesh)
                    node.addComponent(
                        MaterialComponent(
                            albedo = floatArrayOf(1f, 1f, 1f),
                            roughness = 0.9f,
                            metallic = 2.0f
                        )
                    )

                    tileCount += mesh.triangleCount / 2
                    terrainTriangleCount += mesh.triangleCount
                    terrainMeshCount++
                }
            }
        }

        if (!append) {
            val centerTileX = REGION_SIZE / 2
            val centerTileY = REGION_SIZE / 2
            val centerHeight = OsrsCoordinateMapper.luminaYFromHeightUnits128(
                sampleHeight(region, 0, centerTileX, centerTileY)
            )
            val (centerX, centerZ) = OsrsCoordinateMapper.regionLocalTileToLuminaXZ(
                centerTileX,
                centerTileY,
                regionId,
                originBaseX,
                originBaseY
            )
            lastRegionCenterWorldX = centerX
            lastRegionCenterWorldY = centerHeight + 25f
            lastRegionCenterWorldZ = centerZ
        }

        val objectStats = loadObjects(
            region,
            objectManager,
            store,
            regionId,
            originBaseX,
            originBaseY,
            sceneObjectsPlaced
        )

        log.info(
            "Loaded OSRS region {} at origin ({}, {}): {} tiles, {} terrain meshes, {} terrain triangles, " +
                "{} objects placed (skipped-no-model={}, skipped-type={}, deduped={})",
            regionId,
            originBaseX,
            originBaseY,
            tileCount,
            terrainMeshCount,
            terrainTriangleCount,
            objectStats.placed,
            objectStats.skippedNoModel,
            objectStats.skippedType,
            objectStats.dedupedMeshes
        )

        return SceneBuildStats(tileCount, terrainMeshCount, terrainTriangleCount, objectStats.placed)
    }

    private data class ObjectLoadStats(
        val placed: Int = 0,
        val skippedNoModel: Int = 0,
        val skippedType: Int = 0,
        val dedupedMeshes: Int = 0
    )

    private var bridgeHandlingLogged = false

    private fun buildLocationTileMasks(region: Region): Array<Set<Long>> {
        val masks = Array(PLANE_COUNT) { mutableSetOf<Long>() }
        val locations = region.locations ?: return masks.map { it.toSet() }.toTypedArray()
        val baseX = region.baseX
        val baseY = region.baseY
        for (location in locations) {
            val position = location.position ?: continue
            val plane = position.z
            if (plane !in 0 until PLANE_COUNT) continue
            val localTileX = position.x - baseX
            val localTileY = position.y - baseY
            if (localTileX !in 0 until REGION_SIZE || localTileY !in 0 until REGION_SIZE) continue
            masks[plane].add(packRegionTile(localTileX, localTileY))
        }
        return masks.map { it.toSet() }.toTypedArray()
    }

    private fun loadObjects(
        region: Region,
        objectManager: ObjectManager,
        store: Store,
        regionId: Int,
        originBaseX: Int,
        originBaseY: Int,
        sceneObjectsPlaced: Int
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
            if (sceneObjectsPlaced + placed >= MAX_SCENE_OBJECTS) {
                if (!capWarned) {
                    log.warn(
                        "Scene object cap ({}) reached at region {} (placed={}, skipped remainder)",
                        MAX_SCENE_OBJECTS,
                        regionId,
                        sceneObjectsPlaced + placed
                    )
                    capWarned = true
                }
                break
            }

            if (!isSupportedLocationType(location.type)) {
                skippedType++
                continue
            }

            val position = location.position ?: continue
            val objectPlane = position.z
            if (objectPlane !in 0 until PLANE_COUNT) continue

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
                    val built = modelDefinitionToMesh(modelDef, orientation)
                    if (built.triangleCount == 0) {
                        skippedNoModel++
                        continue
                    }
                    meshCache[cacheKey] = built
                    mesh = built
                } else {
                    dedupedMeshes++
                    mesh = meshCache[cacheKey]!!
                }

                val localTileX = position.x - baseX
                val localTileY = position.y - baseY
                if (localTileX !in 0 until REGION_SIZE || localTileY !in 0 until REGION_SIZE) {
                    continue
                }

                val (worldX, worldZ) = OsrsCoordinateMapper.regionLocalTileToLuminaXZ(
                    localTileX,
                    localTileY,
                    regionId,
                    originBaseX,
                    originBaseY
                )
                val terrainY = OsrsCoordinateMapper.luminaYFromHeightUnits128(
                    sampleHeight(region, objectPlane, localTileX, localTileY)
                )
                val offsetScale = MODEL_SCALE
                val worldY = terrainY +
                    (-objectDef.offsetHeight * offsetScale) +
                    (-objectDef.offsetY * offsetScale)

                val node = sceneGraph.createNode("obj_${location.id}_${localTileX}_${localTileY}_p${objectPlane}")
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
            // OSRS object orientation is a Y-axis rotation; world Z is south (north = -Z), so negate Z.
            when (orientation and 3) {
                0 -> {
                    rotatedX[i] = x
                    rotatedY[i] = y
                    rotatedZ[i] = -z
                }
                1 -> {
                    rotatedX[i] = z
                    rotatedY[i] = y
                    rotatedZ[i] = x
                }
                2 -> {
                    rotatedX[i] = -x
                    rotatedY[i] = y
                    rotatedZ[i] = z
                }
                else -> {
                    rotatedX[i] = -z
                    rotatedY[i] = y
                    rotatedZ[i] = -x
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
            val rgb = OsrsColorDecoder.hslToRgb(hsl)
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

            // Z-mirror flips winding; swap two corners to restore outward-facing normals.
            indices[ii++] = baseVertex
            indices[ii++] = baseVertex + 2
            indices[ii++] = baseVertex + 1
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

    private fun packRegionTile(localTileX: Int, localTileY: Int): Long =
        (localTileX.toLong() shl 32) or (localTileY.toLong() and 0xFFFFFFFFL)

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
                val rgb = OsrsColorDecoder.underlayRgb(underlay.color)
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

    private fun shouldRenderUpperPlaneTile(
        region: Region,
        plane: Int,
        tileX: Int,
        tileY: Int,
        locationTiles: Set<Long>
    ): Boolean {
        val overlayId = region.getOverlayId(plane, tileX, tileY)
        val underlayId = region.getUnderlayId(plane, tileX, tileY)
        val hasLocation = locationTiles.contains(packRegionTile(tileX, tileY))
        return Companion.shouldRenderUpperPlaneTile(overlayId, underlayId, hasLocation)
    }

    private fun overlayRgb(overlay: OverlayDefinition): FloatArray? {
        OsrsColorDecoder.overlayRgb(overlay.rgbColor)?.let { return it }
        OsrsColorDecoder.overlayRgb(overlay.secondaryRgbColor)?.let { return it }
        if (overlay.texture >= 0) {
            return TEXTURED_OVERLAY_FALLBACK
        }
        return null
    }

    private fun buildChunkMesh(
        region: Region,
        plane: Int,
        startX: Int,
        startY: Int,
        underlayManager: UnderlayManager,
        overlayManager: OverlayManager,
        regionId: Int,
        originBaseX: Int,
        originBaseY: Int,
        locationTiles: Set<Long>
    ): MeshComponent {
        val tilesPerChunk = CHUNK_SIZE * CHUNK_SIZE
        val verts = FloatArray(tilesPerChunk * 4 * FLOATS_PER_VERTEX)
        val indices = IntArray(tilesPerChunk * 2 * 3)

        var vi = 0
        var ii = 0
        var builtTiles = 0
        for (localY in 0 until CHUNK_SIZE) {
            for (localX in 0 until CHUNK_SIZE) {
                val tileX = startX + localX
                val tileY = startY + localY
                if (plane > 0 && !shouldRenderUpperPlaneTile(
                        region,
                        plane,
                        tileX,
                        tileY,
                        locationTiles
                    )
                ) {
                    continue
                }

                val packedColor = packTileColorToUv(
                    tileColor(region, plane, tileX, tileY, underlayManager, overlayManager)
                )
                val baseVertex = vi

                for (corner in TILE_CORNERS) {
                    val cx = tileX + corner[0]
                    val cy = tileY + corner[1]
                    val off = vi * FLOATS_PER_VERTEX

                    val height = sampleHeight(region, plane, cx, cy)
                    val (luminaX, luminaZ) = OsrsCoordinateMapper.regionLocalTileToLuminaXZ(
                        cx,
                        cy,
                        regionId,
                        originBaseX,
                        originBaseY
                    )
                    verts[off] = luminaX
                    verts[off + 1] = OsrsCoordinateMapper.luminaYFromHeightUnits128(height)
                    verts[off + 2] = luminaZ

                    val normal = computeNormal(region, plane, cx, cy)
                    verts[off + 3] = normal[0]
                    verts[off + 4] = normal[1]
                    verts[off + 5] = normal[2]
                    verts[off + 6] = packedColor
                    verts[off + 7] = 0f

                    vi++
                }

                indices[ii++] = baseVertex
                indices[ii++] = baseVertex + 2
                indices[ii++] = baseVertex + 1
                indices[ii++] = baseVertex
                indices[ii++] = baseVertex + 3
                indices[ii++] = baseVertex + 2
                builtTiles++
            }
        }

        if (builtTiles == 0) {
            return MeshComponent(FloatArray(0), IntArray(0), 0, 0)
        }

        return MeshComponent(verts.copyOf(vi * FLOATS_PER_VERTEX), indices.copyOf(ii), vi, builtTiles * 2)
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

        // pos = (x, -h, -y); ∂pos/∂x = (1, -∂h/∂x, 0), ∂pos/∂y_north = (0, -∂h/∂y, -1)
        val dhdx = (hR - hL) / (2f * 128f)
        val dhdy = (hU - hD) / (2f * 128f)
        var nx = dhdx
        var ny = 1f
        var nz = dhdy
        val len = sqrt(nx * nx + ny * ny + nz * nz)
        if (len <= 0f) return floatArrayOf(0f, 1f, 0f)
        nx /= len
        ny /= len
        nz /= len
        return floatArrayOf(nx, ny, nz)
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
        private const val PLANE_COUNT = 4
        private const val FLOATS_PER_VERTEX = 8
        /** Max placed object instances across the entire multi-region scene (not per region). */
        const val MAX_SCENE_OBJECTS = 12000
        private val TEXTURED_OVERLAY_FALLBACK = floatArrayOf(0.35f, 0.42f, 0.28f)
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

        /** Upper-plane terrain: render when overlay, underlay, or a location exists on the tile. */
        fun shouldRenderUpperPlaneTile(
            overlayId: Int,
            underlayId: Int,
            hasLocation: Boolean
        ): Boolean = overlayId != 0 || underlayId != 0 || hasLocation
    }
}
