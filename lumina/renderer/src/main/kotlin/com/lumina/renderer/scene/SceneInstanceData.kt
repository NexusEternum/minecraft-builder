package com.lumina.renderer.scene

import com.lumina.scene.graph.Transform

/** One TLAS instance: shared BLAS + per-instance transform and shader indices. */
data class SceneInstanceRecord(
    val instanceIndex: Int,
    val blasId: Int,
    val indexTriBase: Int,
    val transform: Transform,
    val nodeName: String
)
