package com.lumina.scene.osrs

import net.runelite.cache.definitions.ModelDefinition
import net.runelite.cache.models.JagexColor
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Assertions.assertNotEquals
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

class OsrsObjectMeshBuilderTest {
    @Test
    fun applyRecolorReplacesExactHslMatch() {
        val original = JagexColor.packHSL(0, 6, 50).toInt()
        val replacement = JagexColor.packHSL(20, 6, 50).toInt()
        val other = JagexColor.packHSL(5, 6, 50).toInt()

        val find = shortArrayOf(original.toShort())
        val replace = shortArrayOf(replacement.toShort())

        assertEquals(replacement, OsrsObjectMeshBuilder.applyRecolor(original, find, replace))
        assertEquals(other, OsrsObjectMeshBuilder.applyRecolor(other, find, replace))
    }

    @Test
    fun meshCacheKeySeparatesRecoloredObjectDefinitions() {
        val sharedModel = 9001
        val orientation = 2
        val keyA = OsrsObjectMeshBuilder.meshCacheKey(objectId = 100, sharedModel, orientation)
        val keyB = OsrsObjectMeshBuilder.meshCacheKey(objectId = 200, sharedModel, orientation)
        assertNotEquals(keyA, keyB)
        assertEquals(keyA, OsrsObjectMeshBuilder.meshCacheKey(100, sharedModel, orientation))
    }

    @Test
    fun fabricatedRecolorChangesDecodedVertexColor() {
        val redHsl = JagexColor.packHSL(0, 6, 50).toInt()
        val blueHsl = JagexColor.packHSL(20, 6, 50).toInt()

        val model = triangleModel(redHsl)
        val uncolored = OsrsObjectMeshBuilder.modelDefinitionToMesh(model, orientation = 0)
        val recolored = OsrsObjectMeshBuilder.modelDefinitionToMesh(
            model,
            orientation = 0,
            recolorToFind = shortArrayOf(redHsl.toShort()),
            recolorToReplace = shortArrayOf(blueHsl.toShort())
        )

        val redPacked = uncolored.vertexData[6]
        val bluePacked = recolored.vertexData[6]
        assertNotEquals(redPacked, bluePacked, "recolor should change packed vertex color")

        val expectedBlue = OsrsColorDecoder.hslToRgb(blueHsl)
        val actualBlue = packedUvToLinearRgb(bluePacked)
        assertEquals(expectedBlue[0], actualBlue[0], 0.02f)
        assertEquals(expectedBlue[1], actualBlue[1], 0.02f)
        assertEquals(expectedBlue[2], actualBlue[2], 0.02f)
    }

    @Test
    fun supportedLocationTypesIncludeDiagonalWallsAndDecorationsExcludeRoofs() {
        assertTrue(OsrsObjectMeshBuilder.isSupportedLocationType(0))
        assertTrue(OsrsObjectMeshBuilder.isSupportedLocationType(4))
        assertTrue(OsrsObjectMeshBuilder.isSupportedLocationType(8))
        assertTrue(OsrsObjectMeshBuilder.isSupportedLocationType(9))
        assertTrue(OsrsObjectMeshBuilder.isSupportedLocationType(10))
        assertTrue(OsrsObjectMeshBuilder.isSupportedLocationType(22))
        for (roofType in 12..21) {
            assertFalse(
                OsrsObjectMeshBuilder.isSupportedLocationType(roofType),
                "roof type $roofType should stay excluded"
            )
        }
    }

    @Test
    fun typeNineUsesSameOrientationBakingAsCardinalWalls() {
        val model = triangleModel(JagexColor.packHSL(10, 4, 40).toInt())
        val orientationOne = OsrsObjectMeshBuilder.modelDefinitionToMesh(model, orientation = 1)
        val orientationThree = OsrsObjectMeshBuilder.modelDefinitionToMesh(model, orientation = 3)
        assertNotEquals(
            orientationOne.vertexData.copyOf(3),
            orientationThree.vertexData.copyOf(3),
            "diagonal wall orientations should rotate vertices"
        )
    }

    @Test
    fun retextureToFindMarksMatchingFacesAsTexturedFallback() {
        val model = texturedTriangleModel(textureId = 42)
        val fallback = OsrsColorDecoder.texturedFallbackLinear()
        val mesh = OsrsObjectMeshBuilder.modelDefinitionToMesh(
            model,
            orientation = 0,
            retextureToFind = shortArrayOf(42)
        )
        val rgb = packedUvToLinearRgb(mesh.vertexData[6])
        assertEquals(fallback[0], rgb[0], 0.02f)
        assertEquals(fallback[1], rgb[1], 0.02f)
        assertEquals(fallback[2], rgb[2], 0.02f)
    }

    private fun triangleModel(faceHsl: Int): ModelDefinition {
        val def = ModelDefinition()
        def.vertexCount = 3
        def.vertexX = intArrayOf(0, 128, 0)
        def.vertexY = intArrayOf(0, 0, 0)
        def.vertexZ = intArrayOf(0, 0, 128)
        def.faceCount = 1
        def.faceIndices1 = intArrayOf(0)
        def.faceIndices2 = intArrayOf(1)
        def.faceIndices3 = intArrayOf(2)
        def.faceColors = shortArrayOf(faceHsl.toShort())
        return def
    }

    private fun texturedTriangleModel(textureId: Int): ModelDefinition {
        val def = triangleModel(JagexColor.packHSL(0, 0, 0).toInt())
        def.faceTextures = shortArrayOf(textureId.toShort())
        return def
    }

    private fun packedUvToLinearRgb(packed: Float): FloatArray {
        val bits = packed.toBits()
        val r = ((bits shr 16) and 0xFF) / 255f
        val g = ((bits shr 8) and 0xFF) / 255f
        val b = (bits and 0xFF) / 255f
        return floatArrayOf(r, g, b)
    }
}
