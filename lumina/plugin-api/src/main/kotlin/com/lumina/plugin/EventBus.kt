package com.lumina.plugin

import org.slf4j.LoggerFactory
import java.lang.reflect.Method
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.CopyOnWriteArrayList
import javax.inject.Singleton

@Target(AnnotationTarget.FUNCTION)
@Retention(AnnotationRetention.RUNTIME)
annotation class Subscribe(val priority: Int = 0)

@Singleton
class EventBus {
    private val log = LoggerFactory.getLogger(EventBus::class.java)

    private data class Subscriber(
        val instance: Any,
        val method: Method,
        val priority: Int
    )

    private val subscribers = ConcurrentHashMap<Class<*>, CopyOnWriteArrayList<Subscriber>>()

    fun register(instance: Any) {
        for (method in instance::class.java.declaredMethods) {
            val sub = method.getAnnotation(Subscribe::class.java) ?: continue
            if (method.parameterCount != 1) {
                log.warn("@Subscribe method {} must have exactly 1 parameter", method.name)
                continue
            }
            method.isAccessible = true
            val eventType = method.parameterTypes[0]
            val list = subscribers.computeIfAbsent(eventType) { CopyOnWriteArrayList() }
            list.add(Subscriber(instance, method, sub.priority))
            list.sortByDescending { it.priority }
        }
    }

    fun unregister(instance: Any) {
        for (list in subscribers.values) {
            list.removeIf { it.instance === instance }
        }
    }

    fun post(event: Any) {
        var clazz: Class<*>? = event::class.java
        while (clazz != null && clazz != Any::class.java) {
            subscribers[clazz]?.forEach { sub ->
                try {
                    sub.method.invoke(sub.instance, event)
                } catch (e: Exception) {
                    log.error("Error dispatching {} to {}.{}",
                        event::class.simpleName, sub.instance::class.simpleName, sub.method.name, e)
                }
            }
            clazz = clazz.superclass
        }
    }
}
