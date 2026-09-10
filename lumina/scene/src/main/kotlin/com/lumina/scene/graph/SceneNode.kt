package com.lumina.scene.graph

import java.util.concurrent.ConcurrentHashMap

class SceneNode(
    val id: Int,
    var name: String
) {
    private val components = ConcurrentHashMap<Class<*>, Any>()
    var parent: SceneNode? = null
        internal set
    private val _children = mutableListOf<SceneNode>()
    val children: List<SceneNode> get() = _children

    fun <T : Any> addComponent(component: T): SceneNode {
        components[component::class.java] = component
        return this
    }

    @Suppress("UNCHECKED_CAST")
    fun <T> getComponent(type: Class<T>): T? = components[type] as? T

    fun hasComponent(type: Class<*>): Boolean = components.containsKey(type)

    fun removeComponent(type: Class<*>) { components.remove(type) }

    fun addChild(child: SceneNode) {
        child.parent = this
        _children.add(child)
    }

    fun removeChild(child: SceneNode) {
        child.parent = null
        _children.remove(child)
    }
}
