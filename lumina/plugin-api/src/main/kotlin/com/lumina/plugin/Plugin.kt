package com.lumina.plugin

import com.google.inject.Injector

abstract class Plugin {
    lateinit var injector: Injector
        internal set

    open fun startUp() {}
    open fun shutDown() {}
    open val name: String get() = this::class.simpleName ?: "Unknown"
}
