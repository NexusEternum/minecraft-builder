package com.lumina.plugins.example

import com.lumina.plugin.*

@PluginDescriptor(
    name = "Example Plugin",
    description = "A simple example plugin demonstrating the Lumina plugin API",
    tags = ["example", "demo"]
)
class ExamplePlugin : Plugin() {
    private val log = org.slf4j.LoggerFactory.getLogger(ExamplePlugin::class.java)

    override fun startUp() {
        log.info("Example plugin started!")
    }

    override fun shutDown() {
        log.info("Example plugin stopped!")
    }

    @Subscribe
    fun onGameTick(event: GameTick) {
        // Called every game tick (~600ms)
    }

    @Subscribe
    fun onGameStateChanged(event: GameStateChanged) {
        log.info("Game state changed: {} -> {}", event.previous, event.current)
    }

    @Subscribe
    fun onFrameRendered(event: FrameRendered) {
        log.debug("Frame: {}ms ({}fps)", String.format("%.1f", event.frameTimeMs), event.fps)
    }
}
