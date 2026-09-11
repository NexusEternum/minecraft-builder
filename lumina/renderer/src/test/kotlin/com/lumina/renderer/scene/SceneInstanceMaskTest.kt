package com.lumina.renderer.scene

import com.lumina.scene.graph.MaterialComponent
import com.lumina.scene.osrs.OsrsObjectMeshBuilder
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test

class SceneInstanceMaskTest {
    @Test
    fun materialTranslucentFlagMapsToTlasInstanceMask() {
        fun maskFor(material: MaterialComponent): Int =
            if (material.translucent) {
                OsrsObjectMeshBuilder.RT_INSTANCE_MASK_TRANSLUCENT
            } else {
                OsrsObjectMeshBuilder.RT_INSTANCE_MASK_OPAQUE
            }

        assertEquals(0x1, maskFor(MaterialComponent()))
        assertEquals(0x2, maskFor(MaterialComponent(translucent = true)))
    }

    @Test
    fun sceneInstanceRecordDefaultsToOpaqueMask() {
        val record = SceneInstanceRecord(
            instanceIndex = 0,
            blasId = 1,
            indexTriBase = 0,
            transform = com.lumina.scene.graph.Transform(),
            nodeName = "test"
        )
        assertEquals(0x1, record.rayTraceMask)
    }
}
