package com.lumina.renderer.rt

import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertFalse
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

class SpecularSamplingGateTest {
    @Test
    fun roughDielectricUsesPureDiffusePath() {
        assertFalse(SpecularSamplingGate.useSpecularLobe(metallic = 0f, roughness = 0.9f))
        assertEquals(0f, SpecularSamplingGate.specularProbability(0f, 0.9f, 0.04f))
    }

    @Test
    fun smoothDielectricKeepsSpecularLobe() {
        assertTrue(SpecularSamplingGate.useSpecularLobe(metallic = 0f, roughness = 0.05f))
        assertTrue(SpecularSamplingGate.specularProbability(0f, 0.05f, 0.04f) > 0f)
    }

    @Test
    fun metalKeepsSpecularLobeEvenWhenRough() {
        assertTrue(SpecularSamplingGate.useSpecularLobe(metallic = 1f, roughness = 0.9f))
    }

    @Test
    fun specularProbabilityIsCappedAt075() {
        val p = SpecularSamplingGate.specularProbability(metallic = 1f, roughness = 0.04f, f0Luminance = 0.9f)
        assertEquals(SpecularSamplingGate.SPECULAR_PROB_MAX, p, 0.001f)
    }

    @Test
    fun boundaryRoughnessAtThresholdUsesSpecularLobe() {
        assertTrue(SpecularSamplingGate.useSpecularLobe(metallic = 0f, roughness = 0.3f))
    }
}
