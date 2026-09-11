package com.lumina.scene.graph

import org.slf4j.LoggerFactory
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.atomic.AtomicInteger
import javax.inject.Singleton

@Singleton
class SceneGraph {
    private val log = LoggerFactory.getLogger(SceneGraph::class.java)
    private val idCounter = AtomicInteger(0)
    private val entities = ConcurrentHashMap<Int, SceneNode>()
    @Volatile var dirty = true
        private set
    /** When true, the next TLAS rebuild must not be throttled (e.g. after full scene upload). */
    @Volatile var tlasRebuildImmediate = false
        private set

    fun createNode(name: String = "node"): SceneNode {
        val id = idCounter.incrementAndGet()
        val node = SceneNode(id, name)
        entities[id] = node
        dirty = true
        return node
    }

    fun removeNode(id: Int) {
        entities.remove(id)
        dirty = true
    }

    fun getNode(id: Int): SceneNode? = entities[id]

    fun allNodes(): Collection<SceneNode> = entities.values

    fun nodesWithComponent(type: Class<*>): List<SceneNode> {
        return entities.values.filter { it.hasComponent(type) }.sortedBy { it.id }
    }

    fun clearDirty() { dirty = false }

    fun markDirty(immediateTlasRebuild: Boolean = false) {
        dirty = true
        if (immediateTlasRebuild) {
            tlasRebuildImmediate = true
        }
    }

    fun clearTlasRebuildImmediate() {
        tlasRebuildImmediate = false
    }

    fun clear() {
        entities.clear()
        dirty = true
        log.info("Scene graph cleared")
    }

    val nodeCount: Int get() = entities.size
}
