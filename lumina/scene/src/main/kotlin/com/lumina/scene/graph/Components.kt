package com.lumina.scene.graph

data class Transform(
    var x: Float = 0f, var y: Float = 0f, var z: Float = 0f,
    var rotX: Float = 0f, var rotY: Float = 0f, var rotZ: Float = 0f,
    var scaleX: Float = 1f, var scaleY: Float = 1f, var scaleZ: Float = 1f
)

data class MeshComponent(
    val vertexData: FloatArray,
    val indexData: IntArray,
    val vertexCount: Int,
    val triangleCount: Int,
    var blasId: Int = -1
) {
    override fun equals(other: Any?) = this === other
    override fun hashCode() = System.identityHashCode(this)
}

data class MaterialComponent(
    var albedo: FloatArray = floatArrayOf(0.8f, 0.8f, 0.8f),
    var roughness: Float = 0.5f,
    var metallic: Float = 0.0f,
    var emissive: FloatArray = floatArrayOf(0f, 0f, 0f),
    var textureId: Int = -1,
    var normalMapId: Int = -1,
    var roughnessMapId: Int = -1,
    /** When true, TLAS instance mask is translucent — shadow rays skip this geometry. */
    var translucent: Boolean = false
) {
    override fun equals(other: Any?) = this === other
    override fun hashCode() = System.identityHashCode(this)
}

data class LightComponent(
    var type: LightType = LightType.POINT,
    var color: FloatArray = floatArrayOf(1f, 1f, 1f),
    var intensity: Float = 1f,
    var radius: Float = 10f,
    var dirX: Float = 0f, var dirY: Float = -1f, var dirZ: Float = 0f
) {
    enum class LightType { POINT, DIRECTIONAL, SPOT, AREA }
    override fun equals(other: Any?) = this === other
    override fun hashCode() = System.identityHashCode(this)
}

data class AnimationComponent(
    var currentFrame: Int = 0,
    var frameCount: Int = 0,
    var frameDuration: Float = 0.1f,
    var elapsed: Float = 0f,
    var playing: Boolean = true
)

data class OsrsEntityComponent(
    val osrsId: Int,
    val entityType: OsrsEntityType,
    var orientation: Int = 0
)

enum class OsrsEntityType { TILE, OBJECT, NPC, PLAYER, PROJECTILE, ITEM }
