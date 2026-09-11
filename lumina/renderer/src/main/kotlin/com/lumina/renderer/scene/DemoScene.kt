package com.lumina.renderer.scene

import com.lumina.scene.graph.*
import org.slf4j.LoggerFactory
import javax.inject.Inject
import javax.inject.Singleton
import kotlin.math.*

@Singleton
class DemoScene @Inject constructor(
    private val sceneGraph: SceneGraph
) {
    private val log = LoggerFactory.getLogger(DemoScene::class.java)

    fun generate() {
        log.info("Generating demo scene...")
        sceneGraph.clear()

        addGroundPlane(200f, floatArrayOf(0.35f, 0.55f, 0.25f))
        addStoneFloor(20f, 0.01f)

        addBox(0f, 2.5f, -8f, 5f, 5f, 5f,
            floatArrayOf(0.9f, 0.1f, 0.1f), roughness = 0.3f, metallic = 0.0f, name = "red_cube")

        addBox(10f, 1.5f, -5f, 3f, 3f, 3f,
            floatArrayOf(0.1f, 0.4f, 0.9f), roughness = 0.05f, metallic = 0.95f, name = "metal_cube")

        addSphere(-8f, 3f, -6f, 3f, 32, 16,
            floatArrayOf(0.95f, 0.95f, 0.95f), roughness = 0.02f, metallic = 1.0f, name = "chrome_sphere")

        addSphere(5f, 2f, 5f, 2f, 24, 12,
            floatArrayOf(1.0f, 0.76f, 0.33f), roughness = 0.1f, metallic = 1.0f, name = "gold_sphere")

        addSphere(-4f, 1.5f, 7f, 1.5f, 24, 12,
            floatArrayOf(0.1f, 0.9f, 0.3f), roughness = 0.6f, metallic = 0.0f, name = "green_sphere")

        addBox(-12f, 5f, -12f, 1f, 10f, 1f,
            floatArrayOf(0.7f, 0.7f, 0.7f), roughness = 0.4f, metallic = 0.0f, name = "pillar_1")
        addBox(12f, 5f, -12f, 1f, 10f, 1f,
            floatArrayOf(0.7f, 0.7f, 0.7f), roughness = 0.4f, metallic = 0.0f, name = "pillar_2")
        addBox(-12f, 5f, 12f, 1f, 10f, 1f,
            floatArrayOf(0.7f, 0.7f, 0.7f), roughness = 0.4f, metallic = 0.0f, name = "pillar_3")
        addBox(12f, 5f, 12f, 1f, 10f, 1f,
            floatArrayOf(0.7f, 0.7f, 0.7f), roughness = 0.4f, metallic = 0.0f, name = "pillar_4")

        addBox(0f, 6f, 3f, 0.3f, 0.3f, 0.3f,
            floatArrayOf(10f, 10f, 8f), roughness = 1.0f, metallic = 0.0f,
            emissive = floatArrayOf(10f, 10f, 8f), name = "light_orb")

        addSphere(8f, 4f, -10f, 0.5f, 16, 8,
            floatArrayOf(0.2f, 0.5f, 10f), roughness = 1.0f, metallic = 0.0f,
            emissive = floatArrayOf(0.2f, 0.5f, 10f), name = "blue_light")

        addBox(15f, 0.5f, 0f, 8f, 1f, 6f,
            floatArrayOf(0.6f, 0.4f, 0.2f), roughness = 0.7f, metallic = 0.0f, name = "wooden_platform")
        addBox(15f, 1.5f, -1f, 6f, 0.2f, 4f,
            floatArrayOf(0.5f, 0.35f, 0.15f), roughness = 0.8f, metallic = 0.0f, name = "table_top")

        addBox(-15f, 2f, 0f, 10f, 4f, 0.3f,
            floatArrayOf(0.85f, 0.85f, 0.85f), roughness = 0.01f, metallic = 1.0f, name = "mirror_wall")

        addStaircase(-5f, 0f, -15f, 8, 0.5f, 1.5f, 3f)

        val meshCount = sceneGraph.nodesWithComponent(MeshComponent::class.java).size
        val triCount = sceneGraph.nodesWithComponent(MeshComponent::class.java)
            .sumOf { it.getComponent(MeshComponent::class.java)?.triangleCount ?: 0 }
        log.info("Demo scene generated: {} meshes, {} triangles", meshCount, triCount)
    }

    private fun addGroundPlane(size: Float, color: FloatArray) {
        val hs = size / 2f
        val verts = floatArrayOf(
            -hs, 0f, -hs,  0f, 1f, 0f,  0f, 0f,
             hs, 0f, -hs,  0f, 1f, 0f,  1f, 0f,
             hs, 0f,  hs,  0f, 1f, 0f,  1f, 1f,
            -hs, 0f,  hs,  0f, 1f, 0f,  0f, 1f,
        )
        val indices = intArrayOf(0, 1, 2, 0, 2, 3)
        val node = sceneGraph.createNode("ground_plane")
        node.addComponent(Transform())
        node.addComponent(MeshComponent(verts, indices, 4, 2))
        node.addComponent(MaterialComponent(albedo = color, roughness = 0.8f, metallic = 0.0f))
    }

    private fun addStoneFloor(size: Float, y: Float) {
        val tileSize = 2f
        val tiles = (size / tileSize).toInt()
        val offset = -size / 2f

        for (tx in 0 until tiles) {
            for (tz in 0 until tiles) {
                val x = offset + tx * tileSize + tileSize / 2f
                val z = offset + tz * tileSize + tileSize / 2f
                val checker = (tx + tz) % 2 == 0
                val gray = if (checker) 0.55f else 0.45f

                val hs = tileSize / 2f - 0.02f
                val verts = floatArrayOf(
                    -hs, y, -hs, 0f, 1f, 0f, 0f, 0f,
                     hs, y, -hs, 0f, 1f, 0f, 1f, 0f,
                     hs, y,  hs, 0f, 1f, 0f, 1f, 1f,
                    -hs, y,  hs, 0f, 1f, 0f, 0f, 1f,
                )
                val node = sceneGraph.createNode("stone_${tx}_${tz}")
                node.addComponent(Transform(x = x, z = z))
                node.addComponent(MeshComponent(verts, intArrayOf(0, 1, 2, 0, 2, 3), 4, 2))
                node.addComponent(MaterialComponent(
                    albedo = floatArrayOf(gray, gray, gray), roughness = 0.5f, metallic = 0.0f))
            }
        }
    }

    private fun addBox(cx: Float, cy: Float, cz: Float,
                       sx: Float, sy: Float, sz: Float,
                       color: FloatArray, roughness: Float = 0.5f, metallic: Float = 0.0f,
                       emissive: FloatArray = floatArrayOf(0f, 0f, 0f), name: String = "box") {
        val hx = sx / 2f; val hy = sy / 2f; val hz = sz / 2f

        val faces = arrayOf(
            // front (+Z)
            floatArrayOf(-hx,-hy, hz, 0f,0f,1f,  hx,-hy, hz, 0f,0f,1f,  hx, hy, hz, 0f,0f,1f, -hx, hy, hz, 0f,0f,1f),
            // back (-Z)
            floatArrayOf( hx,-hy,-hz, 0f,0f,-1f, -hx,-hy,-hz, 0f,0f,-1f, -hx, hy,-hz, 0f,0f,-1f,  hx, hy,-hz, 0f,0f,-1f),
            // right (+X)
            floatArrayOf( hx,-hy, hz, 1f,0f,0f,  hx,-hy,-hz, 1f,0f,0f,  hx, hy,-hz, 1f,0f,0f,  hx, hy, hz, 1f,0f,0f),
            // left (-X)
            floatArrayOf(-hx,-hy,-hz, -1f,0f,0f, -hx,-hy, hz, -1f,0f,0f, -hx, hy, hz, -1f,0f,0f, -hx, hy,-hz, -1f,0f,0f),
            // top (+Y)
            floatArrayOf(-hx, hy, hz, 0f,1f,0f,  hx, hy, hz, 0f,1f,0f,  hx, hy,-hz, 0f,1f,0f, -hx, hy,-hz, 0f,1f,0f),
            // bottom (-Y)
            floatArrayOf(-hx,-hy,-hz, 0f,-1f,0f,  hx,-hy,-hz, 0f,-1f,0f,  hx,-hy, hz, 0f,-1f,0f, -hx,-hy, hz, 0f,-1f,0f),
        )

        val verts = FloatArray(6 * 4 * 8)
        val indices = IntArray(6 * 6)
        var vi = 0; var ii = 0

        for (face in faces) {
            val baseVert = vi / 8
            for (q in 0 until 4) {
                verts[vi++] = face[q * 6 + 0]
                verts[vi++] = face[q * 6 + 1]
                verts[vi++] = face[q * 6 + 2]
                verts[vi++] = face[q * 6 + 3]
                verts[vi++] = face[q * 6 + 4]
                verts[vi++] = face[q * 6 + 5]
                verts[vi++] = if (q == 1 || q == 2) 1f else 0f // u
                verts[vi++] = if (q == 2 || q == 3) 1f else 0f // v
            }
            indices[ii++] = baseVert; indices[ii++] = baseVert + 1; indices[ii++] = baseVert + 2
            indices[ii++] = baseVert; indices[ii++] = baseVert + 2; indices[ii++] = baseVert + 3
        }

        val node = sceneGraph.createNode(name)
        node.addComponent(Transform(x = cx, y = cy, z = cz))
        node.addComponent(MeshComponent(verts, indices, 24, 12))
        node.addComponent(MaterialComponent(albedo = color, roughness = roughness, metallic = metallic, emissive = emissive))
    }

    private fun addSphere(cx: Float, cy: Float, cz: Float, radius: Float,
                          segments: Int, rings: Int,
                          color: FloatArray, roughness: Float = 0.5f, metallic: Float = 0.0f,
                          emissive: FloatArray = floatArrayOf(0f, 0f, 0f), name: String = "sphere") {
        val vertCount = (rings + 1) * (segments + 1)
        val triCount = rings * segments * 2
        val verts = FloatArray(vertCount * 8)
        val indices = IntArray(triCount * 3)

        var vi = 0
        for (r in 0..rings) {
            val phi = PI * r / rings
            val sinPhi = sin(phi).toFloat()
            val cosPhi = cos(phi).toFloat()
            for (s in 0..segments) {
                val theta = 2.0 * PI * s / segments
                val sinTheta = sin(theta).toFloat()
                val cosTheta = cos(theta).toFloat()

                val nx = cosTheta * sinPhi
                val ny = cosPhi
                val nz = sinTheta * sinPhi

                verts[vi++] = nx * radius
                verts[vi++] = ny * radius
                verts[vi++] = nz * radius
                verts[vi++] = nx
                verts[vi++] = ny
                verts[vi++] = nz
                verts[vi++] = s.toFloat() / segments
                verts[vi++] = r.toFloat() / rings
            }
        }

        var ii = 0
        for (r in 0 until rings) {
            for (s in 0 until segments) {
                val a = r * (segments + 1) + s
                val b = a + segments + 1

                indices[ii++] = a; indices[ii++] = b; indices[ii++] = a + 1
                indices[ii++] = a + 1; indices[ii++] = b; indices[ii++] = b + 1
            }
        }

        val node = sceneGraph.createNode(name)
        node.addComponent(Transform(x = cx, y = cy, z = cz))
        node.addComponent(MeshComponent(verts, indices, vertCount, triCount))
        node.addComponent(MaterialComponent(albedo = color, roughness = roughness, metallic = metallic, emissive = emissive))
    }

    private fun addStaircase(startX: Float, startY: Float, startZ: Float,
                             steps: Int, stepHeight: Float, stepDepth: Float, stepWidth: Float) {
        for (i in 0 until steps) {
            addBox(
                startX, startY + stepHeight * (i + 0.5f), startZ + stepDepth * i,
                stepWidth, stepHeight, stepDepth,
                floatArrayOf(0.6f, 0.55f, 0.5f), roughness = 0.6f, metallic = 0.0f,
                name = "stair_$i"
            )
        }
    }
}
