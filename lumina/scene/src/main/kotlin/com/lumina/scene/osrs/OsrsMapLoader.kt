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

    /**
     * Highest plane to load for terrain and objects (0 = ground only).
     * OSRS-style roof hiding: when the player is on plane N, planes 0..N are shown
     * and planes above N are excluded.
     */
    var maxVisiblePlane: Int = 0

    /** @deprecated Use [maxVisiblePlane]; kept for tests that toggled upper-plane terrain. */
    var loadUpperPlanes: Boolean
        get() = maxVisiblePlane > 0
        set(value) {
            maxVisiblePlane = if (value) PLANE_COUNT - 1 else 0
        }

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
        originBaseY: Int,
        playerWorldTileX: Int = originBaseX,
        playerWorldTileY: Int = originBaseY,
        maxVisiblePlane: Int = this.maxVisiblePlane
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
        this.maxVisiblePlane = maxVisiblePlane.coerceIn(0, PLANE_COUNT - 1)

        val validRegionIds = OsrsCoordinateMapper.normalizeRegionIds(regionIds)
        if (validRegionIds.isEmpty()) {
            log.warn("No valid region IDs in {}", regionIds.contentToString())
            return false
        }

        val sortedRegionIds = OsrsCoordinateMapper.sortRegionsByDistanceFromPlayer(
            validRegionIds,
            playerWorldTileX,
            playerWorldTileY
        )
        log.info(
            "Loading {} regions nearest-first from player tile ({}, {}), maxVisiblePlane={}",
            sortedRegionIds.size,
            playerWorldTileX,
            playerWorldTileY,
            this.maxVisiblePlane
        )

        return try {
            Store(cacheDir).use { store ->
                store.load()

                val underlayManager = UnderlayManager(store)
                underlayManager.load()

                val overlayManager = OverlayManager(store)
                overlayManager.load()

                val textureColors = OsrsTextureColorCache.build(store)

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

                for (regionId in sortedRegionIds) {
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

                    val xteaKey = xteaKeyManager.getKey(regionId)
                    val locDef = if (xteaKey == null) {
                        log.warn("No XTEA key for region {} — object locations will not decrypt", regionId)
                        null
                    } else {
                        try {
                            regionLoader.loadLocDef(regionId)
                        } catch (e: Exception) {
                            log.warn(
                                "Location decrypt/load failed for region {} (XTEA key present): {}",
                                regionId,
                                e.message
                            )
                            null
                        }
                    }
                    if (locDef != null) {
                        region.loadLocations(locDef)
                        val locationCount = region.locations?.size ?: 0
                        log.info("Region {}: {} locations decoded", regionId, locationCount)
                    } else if (xteaKey != null) {
                        log.warn("No object locations for region {} (empty loc archive)", regionId)
                    }

                    val stats = buildScene(
                        region,
                        underlayManager,
                        overlayManager,
                        textureColors,
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

                logRegionLoadSummary(
                    sortedRegionIds,
                    originBaseX,
                    originBaseY,
                    loadedCount,
                    totalTiles,
                    totalTerrainMeshes,
                    totalTerrainTriangles,
                    totalObjects,
                    sceneObjectsPlaced
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
        val objectPlaced: Int = 0,
        val overlayWaterTiles: Int = 0,
        val modelFaceWaterMeshes: Int = 0
    )

    private fun buildScene(
        region: Region,
        underlayManager: UnderlayManager,
        overlayManager: OverlayManager,
        textureColors: OsrsTextureColorCache,
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

        if (!bridgeHandlingLogged && maxVisiblePlane > 0) {
            log.info("Bridge tile plane shifting (tile setting 0x2) not implemented — plane 0 only for bridged tiles")
            bridgeHandlingLogged = true
        }

        val locationTilesByPlane = if (maxVisiblePlane > 0) {
            buildLocationTileMasks(region)
        } else {
            Array(PLANE_COUNT) { emptySet() }
        }
        var tileCount = 0
        var terrainTriangleCount = 0
        var terrainMeshCount = 0
        var overlayWaterTiles = 0
        var waterTilesByOverlayId = 0
        var waterTilesByTextureId = 0
        val planeLimit = maxVisiblePlane + 1

        for (plane in 0 until planeLimit) {
            for (chunkX in 0 until CHUNKS_PER_AXIS) {
                for (chunkY in 0 until CHUNKS_PER_AXIS) {
                    val startX = chunkX * CHUNK_SIZE
                    val startY = chunkY * CHUNK_SIZE

                    val chunkMeshes = buildChunkMeshes(
                        region,
                        plane,
                        startX,
                        startY,
                        underlayManager,
                        overlayManager,
                        textureColors,
                        regionId,
                        originBaseX,
                        originBaseY,
                        locationTilesByPlane[plane]
                    )
                    overlayWaterTiles += chunkMeshes.waterTiles
                    waterTilesByOverlayId += chunkMeshes.waterTilesByOverlayId
                    waterTilesByTextureId += chunkMeshes.waterTilesByTextureId
                    val terrainMesh = chunkMeshes.terrain
                    val waterMesh = chunkMeshes.water

                    if (terrainMesh.triangleCount > 0) {
                        val node = sceneGraph.createNode("terrain_${regionId}_p${plane}_${chunkX}_${chunkY}")
                        node.addComponent(Transform())
                        node.addComponent(terrainMesh)
                        node.addComponent(
                            MaterialComponent(
                                albedo = floatArrayOf(1f, 1f, 1f),
                                roughness = 0.9f,
                                metallic = 2.0f
                            )
                        )
                        tileCount += terrainMesh.triangleCount / 2
                        terrainTriangleCount += terrainMesh.triangleCount
                        terrainMeshCount++
                    }

                    if (waterMesh.triangleCount > 0) {
                        val waterNode = sceneGraph.createNode("water_${regionId}_p${plane}_${chunkX}_${chunkY}")
                        waterNode.addComponent(Transform())
                        waterNode.addComponent(waterMesh)
                        waterNode.addComponent(
                            MaterialComponent(
                                albedo = OsrsWaterOverlay.ALBEDO_LINEAR.copyOf(),
                                roughness = OsrsWaterOverlay.ROUGHNESS,
                                metallic = OsrsWaterOverlay.METALLIC
                            )
                        )
                        tileCount += waterMesh.triangleCount / 2
                        terrainTriangleCount += waterMesh.triangleCount
                        terrainMeshCount++
                    }
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
            textureColors,
            regionId,
            originBaseX,
            originBaseY,
            sceneObjectsPlaced
        )

        log.info(
            "Loaded OSRS region {} at origin ({}, {}): {} tiles, {} terrain meshes, {} terrain triangles, " +
                "{} overlay water tiles (by overlay-id={}, by texture-id={}), {} objects placed " +
                "(skipped-no-model={}, skipped-type={}, skipped-cap={}, deduped={}, model-face water meshes={})",
            regionId,
            originBaseX,
            originBaseY,
            tileCount,
            terrainMeshCount,
            terrainTriangleCount,
            overlayWaterTiles,
            waterTilesByOverlayId,
            waterTilesByTextureId,
            objectStats.placed,
            objectStats.skippedNoModel,
            objectStats.skippedType,
            objectStats.skippedCap,
            objectStats.dedupedMeshes,
            objectStats.modelFaceWaterMeshes
        )

        return SceneBuildStats(
            tileCount,
            terrainMeshCount,
            terrainTriangleCount,
            objectStats.placed,
            overlayWaterTiles,
            objectStats.modelFaceWaterMeshes
        )
    }

    private data class ObjectLoadStats(
        val placed: Int = 0,
        val skippedNoModel: Int = 0,
        val skippedType: Int = 0,
        val skippedCap: Int = 0,
        val dedupedMeshes: Int = 0,
        val modelFaceWaterMeshes: Int = 0
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
        textureColors: OsrsTextureColorCache,
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
        val meshCache = HashMap<OsrsObjectMeshBuilder.MeshCacheKey, OsrsObjectMeshBuilder.ObjectMeshBuildResult>()

        var placed = 0
        var skippedNoModel = 0
        var skippedType = 0
        var skippedCap = 0
        var dedupedMeshes = 0
        var modelFaceWaterMeshes = 0

        for (location in locations) {
            if (sceneObjectsPlaced + placed >= MAX_SCENE_OBJECTS) {
                skippedCap++
                continue
            }

            if (!OsrsObjectMeshBuilder.isSupportedLocationType(location.type)) {
                skippedType++
                continue
            }

            val position = location.position ?: continue
            val objectPlane = position.z
            if (objectPlane !in 0 until PLANE_COUNT) continue
            if (!isObjectPlaneVisible(objectPlane, maxVisiblePlane)) continue

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
                val cacheKey = OsrsObjectMeshBuilder.meshCacheKey(location.id, modelId, orientation)
                var meshes = meshCache[cacheKey]
                if (meshes == null) {
                    val modelDef = loadModelDefinition(store, modelLoader, modelDefCache, modelId)
                    if (modelDef == null) {
                        skippedNoModel++
                        continue
                    }
                    val built = OsrsObjectMeshBuilder.modelDefinitionToMeshes(
                        modelDef,
                        orientation,
                        objectDef.recolorToFind,
                        objectDef.recolorToReplace,
                        objectDef.retextureToFind,
                        textureColors = textureColors
                    )
                    if (!built.hasGeometry) {
                        skippedNoModel++
                        continue
                    }
                    meshCache[cacheKey] = built
                    meshes = built
                } else {
                    dedupedMeshes++
                }

                // Region.loadLocations() stores absolute world tile coords (region base + loc-local).
                val worldTileX = position.x
                val worldTileY = position.y
                val localTileX = worldTileX - baseX
                val localTileY = worldTileY - baseY
                if (localTileX !in 0 until REGION_SIZE || localTileY !in 0 until REGION_SIZE) {
                    continue
                }

                val (worldX, worldZ) = OsrsCoordinateMapper.worldTileToLuminaXZ(
                    worldTileX.toFloat(),
                    worldTileY.toFloat(),
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

                val transform = Transform(
                    x = worldX + objectDef.offsetX * offsetScale,
                    y = worldY,
                    z = worldZ
                )
                val objectMaterial = MaterialComponent(
                    albedo = floatArrayOf(1f, 1f, 1f),
                    roughness = 0.85f,
                    metallic = 2.0f
                )

                val node = sceneGraph.createNode("obj_${location.id}_${localTileX}_${localTileY}_p${objectPlane}")
                node.addComponent(transform)
                node.addComponent(meshes.opaque)
                node.addComponent(objectMaterial)
                placed++

                val translucentMesh = meshes.translucent
                if (translucentMesh != null && translucentMesh.triangleCount > 0) {
                    val glassNode = sceneGraph.createNode(
                        "obj_${location.id}_${localTileX}_${localTileY}_p${objectPlane}_glass"
                    )
                    glassNode.addComponent(
                        Transform(
                            x = transform.x,
                            y = transform.y,
                            z = transform.z
                        )
                    )
                    glassNode.addComponent(translucentMesh)
                    glassNode.addComponent(
                        MaterialComponent(
                            albedo = floatArrayOf(1f, 1f, 1f),
                            roughness = 0.85f,
                            metallic = 2.0f,
                            translucent = true
                        )
                    )
                    placed++
                }

                val waterMesh = meshes.water
                if (waterMesh != null && waterMesh.triangleCount > 0) {
                    val waterNode = sceneGraph.createNode(
                        "obj_${location.id}_${localTileX}_${localTileY}_p${objectPlane}_water"
                    )
                    waterNode.addComponent(
                        Transform(
                            x = transform.x,
                            y = transform.y,
                            z = transform.z
                        )
                    )
                    waterNode.addComponent(waterMesh)
                    waterNode.addComponent(
                        MaterialComponent(
                            albedo = OsrsWaterOverlay.ALBEDO_LINEAR.copyOf(),
                            roughness = OsrsWaterOverlay.ROUGHNESS,
                            metallic = OsrsWaterOverlay.METALLIC
                        )
                    )
                    placed++
                    modelFaceWaterMeshes++
                }
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

        if (skippedCap > 0) {
            log.warn(
                "objects skipped due to cap: {} (region {}), scene total would be {}",
                skippedCap,
                regionId,
                sceneObjectsPlaced + placed + skippedCap
            )
        }

        return ObjectLoadStats(placed, skippedNoModel, skippedType, skippedCap, dedupedMeshes, modelFaceWaterMeshes)
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

    private fun packRegionTile(localTileX: Int, localTileY: Int): Long =
        (localTileX.toLong() shl 32) or (localTileY.toLong() and 0xFFFFFFFFL)

    private fun tileColor(
        region: Region,
        plane: Int,
        x: Int,
        y: Int,
        underlayManager: UnderlayManager,
        overlayManager: OverlayManager,
        textureColors: OsrsTextureColorCache
    ): FloatArray {
        val overlayId = region.getOverlayId(plane, x, y)
        if (overlayId > 0) {
            val overlay = overlayManager.provide(overlayId)
            if (overlay != null) {
                val rgb = overlayRgb(overlay, textureColors)
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
        val hasLocation = locationTiles.contains(packRegionTile(tileX, tileY))
        return Companion.shouldRenderUpperPlaneTile(overlayId, hasLocation)
    }

    private fun overlayRgb(overlay: OverlayDefinition, textureColors: OsrsTextureColorCache): FloatArray? {
        if (OsrsColorDecoder.isMagentaTextureMarker(overlay.rgbColor) ||
            OsrsColorDecoder.isMagentaTextureMarker(overlay.secondaryRgbColor)
        ) {
            // Textured overlay (water, cobblestone, etc.) — use per-texture average when available.
            if (overlay.texture >= 0) {
                return textureColors.linearRgbOrFallback(overlay.texture)
            }
            return OsrsColorDecoder.texturedFallbackLinear()
        }
        OsrsColorDecoder.overlayRgb(overlay.rgbColor)?.let { return it }
        OsrsColorDecoder.overlayRgb(overlay.secondaryRgbColor)?.let { return it }
        if (overlay.texture >= 0) {
            return textureColors.linearRgbOrFallback(overlay.texture)
        }
        return null
    }

    private fun classifyWaterTile(
        region: Region,
        plane: Int,
        tileX: Int,
        tileY: Int,
        overlayManager: OverlayManager
    ): OsrsWaterOverlay.WaterTileClassification {
        val overlayId = region.getOverlayId(plane, tileX, tileY)
        val overlay = if (overlayId > 0) overlayManager.provide(overlayId) else null
        return OsrsWaterOverlay.classifyWaterTile(overlayId, overlay)
    }

    private data class ChunkMeshResult(
        val terrain: MeshComponent,
        val water: MeshComponent,
        val waterTiles: Int,
        val waterTilesByOverlayId: Int,
        val waterTilesByTextureId: Int
    )

    private fun buildChunkMeshes(
        region: Region,
        plane: Int,
        startX: Int,
        startY: Int,
        underlayManager: UnderlayManager,
        overlayManager: OverlayManager,
        textureColors: OsrsTextureColorCache,
        regionId: Int,
        originBaseX: Int,
        originBaseY: Int,
        locationTiles: Set<Long>
    ): ChunkMeshResult {
        val tilesPerChunk = CHUNK_SIZE * CHUNK_SIZE
        val terrainVerts = FloatArray(tilesPerChunk * 4 * FLOATS_PER_VERTEX)
        val terrainIndices = IntArray(tilesPerChunk * 2 * 3)
        val waterVerts = FloatArray(tilesPerChunk * 4 * FLOATS_PER_VERTEX)
        val waterIndices = IntArray(tilesPerChunk * 2 * 3)

        var terrainVi = 0
        var terrainIi = 0
        var terrainTiles = 0
        var waterVi = 0
        var waterIi = 0
        var waterTiles = 0
        var waterTilesByOverlayId = 0
        var waterTilesByTextureId = 0

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

                val waterClass = classifyWaterTile(region, plane, tileX, tileY, overlayManager)
                val water = waterClass.isWater
                val packedColor = if (water) {
                    0f
                } else {
                    packTileColorToUv(
                        tileColor(region, plane, tileX, tileY, underlayManager, overlayManager, textureColors)
                    )
                }

                val verts = if (water) waterVerts else terrainVerts
                var vi = if (water) waterVi else terrainVi
                var ii = if (water) waterIi else terrainIi
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

                val indices = if (water) waterIndices else terrainIndices
                indices[ii++] = baseVertex
                indices[ii++] = baseVertex + 2
                indices[ii++] = baseVertex + 1
                indices[ii++] = baseVertex
                indices[ii++] = baseVertex + 3
                indices[ii++] = baseVertex + 2

                if (water) {
                    waterVi = vi
                    waterIi = ii
                    waterTiles++
                    if (waterClass.byOverlayId) waterTilesByOverlayId++
                    if (waterClass.byTextureId) waterTilesByTextureId++
                } else {
                    terrainVi = vi
                    terrainIi = ii
                    terrainTiles++
                }
            }
        }

        val terrainMesh = if (terrainTiles == 0) {
            MeshComponent(FloatArray(0), IntArray(0), 0, 0)
        } else {
            MeshComponent(
                terrainVerts.copyOf(terrainVi * FLOATS_PER_VERTEX),
                terrainIndices.copyOf(terrainIi),
                terrainVi,
                terrainTiles * 2
            )
        }

        val waterMesh = if (waterTiles == 0) {
            MeshComponent(FloatArray(0), IntArray(0), 0, 0)
        } else {
            MeshComponent(
                waterVerts.copyOf(waterVi * FLOATS_PER_VERTEX),
                waterIndices.copyOf(waterIi),
                waterVi,
                waterTiles * 2
            )
        }

        return ChunkMeshResult(
            terrain = terrainMesh,
            water = waterMesh,
            waterTiles = waterTiles,
            waterTilesByOverlayId = waterTilesByOverlayId,
            waterTilesByTextureId = waterTilesByTextureId
        )
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

    private fun logRegionLoadSummary(
        regionIds: IntArray,
        originBaseX: Int,
        originBaseY: Int,
        loadedCount: Int,
        totalTiles: Int,
        totalTerrainMeshes: Int,
        totalTerrainTriangles: Int,
        totalObjects: Int,
        sceneObjectsPlaced: Int
    ) {
        var minWorldX = Int.MAX_VALUE
        var minWorldY = Int.MAX_VALUE
        var maxWorldX = Int.MIN_VALUE
        var maxWorldY = Int.MIN_VALUE
        val regionBases = StringBuilder()
        for (regionId in regionIds) {
            val (regionBaseX, regionBaseY) = OsrsCoordinateMapper.regionOriginTiles(regionId)
            if (regionBases.isNotEmpty()) regionBases.append(", ")
            regionBases.append("$regionId@($regionBaseX,$regionBaseY)")
            minWorldX = minOf(minWorldX, regionBaseX)
            minWorldY = minOf(minWorldY, regionBaseY)
            maxWorldX = maxOf(maxWorldX, regionBaseX + REGION_SIZE - 1)
            maxWorldY = maxOf(maxWorldY, regionBaseY + REGION_SIZE - 1)
        }

        log.info(
            "Loaded {} OSRS regions at scene-load origin ({}, {}): {} tiles, {} terrain meshes, " +
                "{} terrain triangles, {} objects placed (cap {}/{}); region bases: [{}]; " +
                "world tile AABB ({}, {})..({}, {})",
            loadedCount,
            originBaseX,
            originBaseY,
            totalTiles,
            totalTerrainMeshes,
            totalTerrainTriangles,
            totalObjects,
            sceneObjectsPlaced,
            MAX_SCENE_OBJECTS,
            regionBases,
            minWorldX,
            minWorldY,
            maxWorldX,
            maxWorldY
        )
    }

    companion object {
        const val TILE_SCALE = 2.56f
        private const val MODEL_SCALE = TILE_SCALE / 128f
        private const val REGION_SIZE = 64
        private const val CHUNK_SIZE = 8
        private const val CHUNKS_PER_AXIS = REGION_SIZE / CHUNK_SIZE
        private const val PLANE_COUNT = 4
        private const val FLOATS_PER_VERTEX = 8 // terrain vertices; object mesh layout is in OsrsObjectMeshBuilder
        /** Max placed object instances across the entire multi-region scene (not per region). */
        const val MAX_SCENE_OBJECTS = 12000
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

        /**
         * Upper-plane terrain: render when overlay != 0 or a location exists on the tile.
         * Underlay alone is excluded — b16 used underlay != 0 and blanketed the entire world
         * with invisible height sheets because every upper plane tile has a copied underlay id.
         */
        fun shouldRenderUpperPlaneTile(
            overlayId: Int,
            hasLocation: Boolean
        ): Boolean = overlayId != 0 || hasLocation

        /** Objects on planes above [maxVisiblePlane] are hidden (OSRS roof culling). */
        fun isObjectPlaneVisible(objectPlane: Int, maxVisiblePlane: Int): Boolean =
            objectPlane in 0 until PLANE_COUNT && objectPlane <= maxVisiblePlane.coerceIn(0, PLANE_COUNT - 1)

        /** @deprecated b16 filter; underlay-only tiles are intentionally excluded. */
        @Deprecated("Underlay-only upper tiles blanket the world; use two-arg overload")
        fun shouldRenderUpperPlaneTile(
            overlayId: Int,
            underlayId: Int,
            hasLocation: Boolean
        ): Boolean = shouldRenderUpperPlaneTile(overlayId, hasLocation)
    }
}
