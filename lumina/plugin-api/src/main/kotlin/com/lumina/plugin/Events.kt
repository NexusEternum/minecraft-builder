package com.lumina.plugin

// Game lifecycle events
open class GameEvent

class GameStateChanged(val previous: GameState, val current: GameState) : GameEvent()
enum class GameState { STARTING, LOGIN_SCREEN, LOADING, LOGGED_IN, CONNECTION_LOST, HOPPING }

class GameTick : GameEvent()

class ClientShutdown : GameEvent()

// Scene events
class SceneLoaded(val sceneId: Int) : GameEvent()
class SceneChanged : GameEvent()

// Rendering events  
class BeforeRender : GameEvent()
class AfterRender : GameEvent()
class FrameRendered(val frameTimeMs: Double, val fps: Int) : GameEvent()

// Entity events
class NpcSpawned(val npcId: Int, val x: Int, val y: Int, val z: Int) : GameEvent()
class NpcDespawned(val npcId: Int) : GameEvent()
class PlayerSpawned(val name: String, val x: Int, val y: Int, val z: Int) : GameEvent()
class PlayerDespawned(val name: String) : GameEvent()

class ItemSpawned(val itemId: Int, val x: Int, val y: Int, val z: Int) : GameEvent()
class ItemDespawned(val itemId: Int) : GameEvent()

class GameObjectSpawned(val objectId: Int, val x: Int, val y: Int, val z: Int) : GameEvent()
class GameObjectDespawned(val objectId: Int) : GameEvent()

// Chat events
class ChatMessage(val type: ChatMessageType, val sender: String, val message: String) : GameEvent()
enum class ChatMessageType { GAME, PUBLIC, PRIVATE, CLAN, TRADE, SYSTEM }

// Menu events
class MenuOptionClicked(val option: String, val target: String, val id: Int) : GameEvent()

// Config events
class ConfigChanged(val group: String, val key: String, val oldValue: Any?, val newValue: Any?) : GameEvent()

// Plugin lifecycle
class PluginLoaded(val plugin: Plugin) : GameEvent()
class PluginStarted(val plugin: Plugin) : GameEvent()
class PluginStopped(val plugin: Plugin) : GameEvent()
