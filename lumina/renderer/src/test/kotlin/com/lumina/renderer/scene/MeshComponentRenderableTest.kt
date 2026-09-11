package com.lumina.renderer.scene

import com.lumina.scene.graph.MeshComponent
import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

class MeshComponentRenderableTest {
    @Test
    fun emptyMeshIsNotRenderable() {
        val empty = MeshComponent(FloatArray(0), IntArray(0), 0, 0)
        assertFalse(empty.isRenderable())
    }

    @Test
    fun meshWithTrianglesButNoVerticesIsNotRenderable() {
        val mesh = MeshComponent(FloatArray(0), intArrayOf(0, 1, 2), 0, 1)
        assertFalse(mesh.isRenderable())
    }

    @Test
    fun validMeshIsRenderable() {
        val mesh = MeshComponent(
            floatArrayOf(0f, 0f, 0f, 0f, 1f, 0f, 0f, 0f),
            intArrayOf(0, 1, 2),
            1,
            1
        )
        assertTrue(mesh.isRenderable())
    }
}
