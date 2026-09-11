package com.lumina.renderer.scene

import com.lumina.scene.graph.MaterialComponent
import com.lumina.scene.graph.MeshComponent
import com.lumina.scene.graph.SceneGraph
import com.lumina.scene.graph.Transform
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test

class SceneBufferManagerInstancingTest {
    @Test
    fun uniqueMeshDedupCountsSharedGeometryOnce() {
        val graph = SceneGraph()
        val mesh = MeshComponent(
            floatArrayOf(0f, 0f, 0f, 0f, 1f, 0f, 0f, 0f, 1f, 0f, 0f, 0f, 1f, 0f, 0f, 0f),
            intArrayOf(0, 1, 2),
            3,
            1
        )

        repeat(3) { i ->
            val node = graph.createNode("inst_$i")
            node.addComponent(Transform(x = i.toFloat(), z = i * 2f))
            node.addComponent(mesh)
            node.addComponent(MaterialComponent())
        }

        val meshNodes = graph.nodesWithComponent(MeshComponent::class.java)
        val unique = LinkedHashSet<MeshComponent>()
        for (node in meshNodes) {
            unique.add(node.getComponent(MeshComponent::class.java)!!)
        }
        assertEquals(3, meshNodes.size)
        assertEquals(1, unique.size)
    }
}
