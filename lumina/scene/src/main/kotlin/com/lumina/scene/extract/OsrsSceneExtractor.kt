package com.lumina.scene.extract

import com.lumina.scene.graph.*
import org.slf4j.LoggerFactory
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class OsrsSceneExtractor @Inject constructor(
    private val sceneGraph: SceneGraph
) {
    private val log = LoggerFactory.getLogger(OsrsSceneExtractor::class.java)

    fun extractTilePaint(
        tileX: Int, tileY: Int, plane: Int,
        heights: IntArray, colors: IntArray,
        textureId: Int
    ) {
        val verts = buildTileQuad(tileX, tileY, plane, heights)
        val rgb = colors.map { hslToRgb(it) }

        val node = sceneGraph.createNode("tile_${tileX}_${tileY}_$plane")
        node.addComponent(Transform(
            x = tileX * TILE_SIZE, y = 0f, z = tileY * TILE_SIZE
        ))
        node.addComponent(MeshComponent(
            vertexData = verts,
            indexData = intArrayOf(0, 1, 2, 0, 2, 3),
            vertexCount = 4,
            triangleCount = 2
        ))
        node.addComponent(MaterialComponent(
            albedo = if (rgb.isNotEmpty()) rgb[0] else floatArrayOf(0.4f, 0.6f, 0.3f),
            textureId = textureId
        ))
        node.addComponent(OsrsEntityComponent(0, OsrsEntityType.TILE))
    }

    fun extractTileModel(
        tileX: Int, tileY: Int, plane: Int,
        vertexX: FloatArray, vertexY: FloatArray, vertexZ: FloatArray,
        faceA: IntArray, faceB: IntArray, faceC: IntArray,
        faceColors: IntArray, faceTextures: IntArray?,
        baseX: Int, baseY: Int
    ) {
        val triCount = faceA.size
        val vertData = FloatArray(triCount * 3 * 8)
        val idxData = IntArray(triCount * 3)

        for (i in 0 until triCount) {
            val indices = intArrayOf(faceA[i], faceB[i], faceC[i])
            val rgb = hslToRgb(faceColors[i])
            for (j in 0..2) {
                val vi = i * 3 + j
                val off = vi * 8
                vertData[off] = vertexX[indices[j]] + (tileX + baseX) * TILE_SIZE
                vertData[off + 1] = vertexY[indices[j]]
                vertData[off + 2] = vertexZ[indices[j]] + (tileY + baseY) * TILE_SIZE
                vertData[off + 3] = 0f  // nx
                vertData[off + 4] = 1f  // ny
                vertData[off + 5] = 0f  // nz
                vertData[off + 6] = rgb[0] * 0.5f + 0.5f * (j.toFloat() / 2f)  // u placeholder
                vertData[off + 7] = rgb[1] * 0.5f + 0.5f * (j.toFloat() / 2f)  // v placeholder
                idxData[vi] = vi
            }
        }

        val node = sceneGraph.createNode("tilemodel_${tileX}_${tileY}_$plane")
        node.addComponent(Transform())
        node.addComponent(MeshComponent(vertData, idxData, triCount * 3, triCount))
        node.addComponent(MaterialComponent())
        node.addComponent(OsrsEntityComponent(0, OsrsEntityType.TILE))
    }

    fun extractModel(
        objectId: Int, entityType: OsrsEntityType,
        vertexX: FloatArray, vertexY: FloatArray, vertexZ: FloatArray,
        faceA: IntArray, faceB: IntArray, faceC: IntArray,
        faceColors: IntArray, faceTextures: IntArray?,
        worldX: Float, worldY: Float, worldZ: Float, orientation: Int
    ) {
        val triCount = faceA.size
        if (triCount == 0) return

        val vertData = FloatArray(triCount * 3 * 8)
        val idxData = IntArray(triCount * 3)

        for (i in 0 until triCount) {
            val indices = intArrayOf(faceA[i], faceB[i], faceC[i])
            val rgb = if (i < faceColors.size) hslToRgb(faceColors[i]) else floatArrayOf(0.5f, 0.5f, 0.5f)

            val ax = vertexX[indices[0]]; val ay = vertexY[indices[0]]; val az = vertexZ[indices[0]]
            val bx = vertexX[indices[1]]; val by = vertexY[indices[1]]; val bz = vertexZ[indices[1]]
            val cx = vertexX[indices[2]]; val cy = vertexY[indices[2]]; val cz = vertexZ[indices[2]]
            val e1x = bx - ax; val e1y = by - ay; val e1z = bz - az
            val e2x = cx - ax; val e2y = cy - ay; val e2z = cz - az
            var nx = e1y * e2z - e1z * e2y
            var ny = e1z * e2x - e1x * e2z
            var nz = e1x * e2y - e1y * e2x
            val len = Math.sqrt((nx * nx + ny * ny + nz * nz).toDouble()).toFloat()
            if (len > 0f) { nx /= len; ny /= len; nz /= len }

            for (j in 0..2) {
                val vi = i * 3 + j
                val off = vi * 8
                vertData[off] = vertexX[indices[j]]
                vertData[off + 1] = vertexY[indices[j]]
                vertData[off + 2] = vertexZ[indices[j]]
                vertData[off + 3] = nx; vertData[off + 4] = ny; vertData[off + 5] = nz
                vertData[off + 6] = rgb[0]; vertData[off + 7] = rgb[1]
                idxData[vi] = vi
            }
        }

        val node = sceneGraph.createNode("${entityType.name.lowercase()}_$objectId")
        node.addComponent(Transform(x = worldX, y = worldY, z = worldZ))
        node.addComponent(MeshComponent(vertData, idxData, triCount * 3, triCount))
        node.addComponent(MaterialComponent(albedo = floatArrayOf(0.7f, 0.7f, 0.7f)))
        node.addComponent(OsrsEntityComponent(objectId, entityType, orientation))
    }

    fun clear() = sceneGraph.clear()

    companion object {
        const val TILE_SIZE = 128f

        fun hslToRgb(hsl: Int): FloatArray {
            if (hsl == -1 || hsl == 12345678) return floatArrayOf(0f, 0f, 0f)
            val h = ((hsl shr 10) and 0x3F).toFloat() / 63f
            val s = ((hsl shr 7) and 0x07).toFloat() / 7f
            val l = (hsl and 0x7F).toFloat() / 127f
            val c = (1f - Math.abs(2f * l - 1f)) * s
            val x = c * (1f - Math.abs((h * 6f) % 2f - 1f))
            val m = l - c / 2f
            val (r1, g1, b1) = when {
                h < 1f / 6f -> Triple(c, x, 0f)
                h < 2f / 6f -> Triple(x, c, 0f)
                h < 3f / 6f -> Triple(0f, c, x)
                h < 4f / 6f -> Triple(0f, x, c)
                h < 5f / 6f -> Triple(x, 0f, c)
                else -> Triple(c, 0f, x)
            }
            return floatArrayOf(r1 + m, g1 + m, b1 + m)
        }

        private fun buildTileQuad(tileX: Int, tileY: Int, plane: Int, heights: IntArray): FloatArray {
            val x0 = 0f; val z0 = 0f
            val x1 = TILE_SIZE; val z1 = TILE_SIZE
            val h = if (heights.isNotEmpty()) heights[0].toFloat() else 0f
            return floatArrayOf(
                x0, h, z0, 0f, 1f, 0f, 0f, 0f,
                x1, h, z0, 0f, 1f, 0f, 1f, 0f,
                x1, h, z1, 0f, 1f, 0f, 1f, 1f,
                x0, h, z1, 0f, 1f, 0f, 0f, 1f
            )
        }
    }
}
