package com.lumina.scene.osrs

import com.lumina.scene.graph.MeshComponent
import net.runelite.cache.definitions.ModelDefinition
import kotlin.math.sqrt

/**
 * Builds OSRS object meshes with per-object-definition recolor/retexture applied.
 *
 * Recolor semantics match [net.runelite.cache.definitions.ModelDefinition.recolor] /
 * RuneLite [net.runelite.api.ModelData.recolor]: exact HSL short match on each face color.
 */
object OsrsObjectMeshBuilder {
    private const val MODEL_SCALE = OsrsMapLoader.TILE_SCALE / 128f
    private const val FLOATS_PER_VERTEX = 8

    data class MeshCacheKey(
        val objectId: Int,
        val modelId: Int,
        val orientation: Int
    )

    /**
     * Location types we place in the scene.
     * Types 12–21 are roof pieces — deliberately excluded (roof hiding).
     */
    fun isSupportedLocationType(type: Int): Boolean =
        type in 0..3 ||
            type in 4..9 ||
            type in 10..11 ||
            type == 22

    fun meshCacheKey(objectId: Int, modelId: Int, orientation: Int): MeshCacheKey =
        MeshCacheKey(objectId, modelId, orientation and 3)

    /**
     * Apply object-definition recolor pairs before HSL decode.
     * Matches [ModelDefinition.recolor]: `if (faceColors[i] == find) faceColors[i] = replace`.
     */
    fun applyRecolor(hsl: Int, recolorToFind: ShortArray?, recolorToReplace: ShortArray?): Int {
        if (recolorToFind == null || recolorToReplace == null || recolorToFind.isEmpty()) {
            return hsl
        }
        val faceColor = hsl.toShort()
        for (i in recolorToFind.indices) {
            if (i >= recolorToReplace.size) break
            if (faceColor == recolorToFind[i]) {
                return recolorToReplace[i].toInt()
            }
        }
        return hsl
    }

    /** Faces whose texture id matches [retextureToFind] are treated as textured (fallback albedo). */
    fun isRetexturedFace(
        faceTextures: ShortArray?,
        face: Int,
        retextureToFind: ShortArray?
    ): Boolean {
        if (retextureToFind == null || retextureToFind.isEmpty() || faceTextures == null || face >= faceTextures.size) {
            return false
        }
        val texture = faceTextures[face]
        for (find in retextureToFind) {
            if (texture == find) return true
        }
        return false
    }

    fun modelDefinitionToMesh(
        model: ModelDefinition,
        orientation: Int,
        recolorToFind: ShortArray? = null,
        recolorToReplace: ShortArray? = null,
        retextureToFind: ShortArray? = null,
        textureColors: OsrsTextureColorCache? = null
    ): MeshComponent {
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
        val faceTextures = model.faceTextures
        val faceTransparencies = model.faceTransparencies

        val rotatedX = IntArray(vertexCount)
        val rotatedY = IntArray(vertexCount)
        val rotatedZ = IntArray(vertexCount)
        rotateVertices(srcX, srcY, srcZ, vertexCount, orientation, rotatedX, rotatedY, rotatedZ)

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

            val (nx, ny, nz) = computeFaceNormal(ax, ay, az, bx, by, bz, cx, cy, cz)

            val textureId = if (faceTextures != null && face < faceTextures.size) {
                faceTextures[face].toInt()
            } else {
                -1
            }
            val hasTexture = textureId != -1 || isRetexturedFace(faceTextures, face, retextureToFind)
            val rgb = if (hasTexture) {
                resolveTexturedFaceColor(textureId, textureColors)
            } else {
                val rawHsl = if (faceColors != null && face < faceColors.size) faceColors[face].toInt() else 0
                val hsl = applyRecolor(rawHsl, recolorToFind, recolorToReplace)
                OsrsColorDecoder.hslToRgb(hsl)
            }
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
            indices[ii++] = baseVertex + 2
            indices[ii++] = baseVertex + 1
        }

        return MeshComponent(verts, indices, outVertexCount, visibleFaces)
    }

    internal fun rotateVertices(
        srcX: IntArray,
        srcY: IntArray,
        srcZ: IntArray,
        vertexCount: Int,
        orientation: Int,
        rotatedX: IntArray,
        rotatedY: IntArray,
        rotatedZ: IntArray
    ) {
        for (i in 0 until vertexCount) {
            val x = srcX[i]
            val y = srcY[i]
            val z = srcZ[i]
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
    }

    private fun computeFaceNormal(
        ax: Float, ay: Float, az: Float,
        bx: Float, by: Float, bz: Float,
        cx: Float, cy: Float, cz: Float
    ): Triple<Float, Float, Float> {
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
        return Triple(nx, ny, nz)
    }

    internal fun resolveTexturedFaceColor(
        textureId: Int,
        textureColors: OsrsTextureColorCache?
    ): FloatArray {
        if (textureId >= 0 && textureColors != null) {
            return textureColors.linearRgbOrFallback(textureId)
        }
        return OsrsColorDecoder.texturedFallbackLinear()
    }

    private fun packTileColorToUv(color: FloatArray): Float {
        val r = (color[0] * 255f).toInt().coerceIn(0, 255)
        val g = (color[1] * 255f).toInt().coerceIn(0, 255)
        val b = (color[2] * 255f).toInt().coerceIn(0, 255)
        return Float.fromBits((r shl 16) or (g shl 8) or b)
    }
}
