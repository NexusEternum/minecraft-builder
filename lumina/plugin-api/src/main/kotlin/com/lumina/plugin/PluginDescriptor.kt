package com.lumina.plugin

@Target(AnnotationTarget.CLASS)
@Retention(AnnotationRetention.RUNTIME)
annotation class PluginDescriptor(
    val name: String,
    val description: String = "",
    val tags: Array<String> = [],
    val enabledByDefault: Boolean = true,
    val developerPlugin: Boolean = false,
    val loadInSafeMode: Boolean = false
)
