package com.lumina.renderer.rt

/**
 * Mirrors the diffuse/specular lobe gate in [closesthit.rchit].
 * Rough non-metallic surfaces skip specular bounce sampling to avoid GGX noise on terrain.
 */
object SpecularSamplingGate {
    const val METALLIC_THRESHOLD = 0.5f
    const val ROUGHNESS_THRESHOLD = 0.3f
    const val SPECULAR_PROB_MIN = 0.05f
    const val SPECULAR_PROB_MAX = 0.75f

    /** True when the path tracer may choose between diffuse and specular bounce lobes. */
    fun useSpecularLobe(metallic: Float, roughness: Float): Boolean =
        metallic >= METALLIC_THRESHOLD || roughness <= ROUGHNESS_THRESHOLD

    /**
     * Specular lobe probability for two-lobe sampling. Returns 0 when [useSpecularLobe] is false.
     * [f0Luminance] is luminance(F0) where F0 = mix(0.04, albedo, metallic).
     */
    fun specularProbability(metallic: Float, roughness: Float, f0Luminance: Float): Float {
        if (!useSpecularLobe(metallic, roughness)) {
            return 0f
        }
        return (f0Luminance + (1f - roughness) * 0.5f).coerceIn(SPECULAR_PROB_MIN, SPECULAR_PROB_MAX)
    }
}
