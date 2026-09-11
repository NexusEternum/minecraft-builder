package com.lumina.game.jagex

import org.slf4j.LoggerFactory
import java.lang.reflect.Field
import java.lang.reflect.Modifier
import java.util.Collections

/**
 * Injects entries into the JVM's cached environment map so [System.getenv] returns them.
 *
 * Required for in-process RuneLite boot: the Jagex game client reads `JX_*` variables via
 * [System.getenv], which cannot be set through supported APIs after the process starts.
 */
object ProcessEnvironmentInjector {
    private val log = LoggerFactory.getLogger(ProcessEnvironmentInjector::class.java)

    private val jxVarNames = setOf(
        JagexCredentials.PROPERTY_CHARACTER_ID,
        JagexCredentials.PROPERTY_SESSION_ID,
        JagexCredentials.PROPERTY_REFRESH_TOKEN,
        JagexCredentials.PROPERTY_DISPLAY_NAME,
        JagexCredentials.PROPERTY_ACCESS_TOKEN,
    )

    /**
     * Returns true when all supplied Jagex env vars are already present in the process environment.
     */
    fun jagexEnvAlreadyPresent(): Boolean =
        jxVarNames.all { name ->
            val value = System.getenv(name)
            value != null && value.isNotBlank()
        }

    /**
     * Injects [variables] into the process environment. Blank values are skipped.
     *
     * @return true when every non-blank entry was applied successfully
     */
    fun inject(variables: Map<String, String>): Boolean {
        val toApply = variables.filterValues { it.isNotBlank() }
        if (toApply.isEmpty()) {
            return true
        }

        return try {
            val processEnvironment = Class.forName("java.lang.ProcessEnvironment")
            val isWindows = System.getProperty("os.name").lowercase().contains("windows")

            if (isWindows) {
                val field = processEnvironment.getDeclaredField("theCaseInsensitiveEnvironment")
                field.isAccessible = true
                val env = field.get(null) as MutableMap<String, String>
                toApply.forEach { (key, value) -> env[key] = value }
            } else {
                val theEnvironment = processEnvironment.getDeclaredField("theEnvironment")
                theEnvironment.isAccessible = true
                val env = theEnvironment.get(null) as MutableMap<String, String>
                toApply.forEach { (key, value) -> env[key] = value }

                val unmodifiableField = processEnvironment.getDeclaredField("theUnmodifiableEnvironment")
                unmodifiableField.isAccessible = true
                val unmodifiableEnv = unmodifiableField.get(null)
                val backing = extractBackingMap(unmodifiableEnv)
                if (backing != null) {
                    toApply.forEach { (key, value) -> backing[key] = value }
                } else {
                    log.debug("Could not unwrap theUnmodifiableEnvironment; only theEnvironment was updated")
                }
            }

            true
        } catch (e: Exception) {
            log.warn(
                "Failed to inject Jagex environment variables via reflection (JDK {}). " +
                    "RuneLite will show the standard login screen. Cause: {}",
                System.getProperty("java.version"),
                e.toString(),
            )
            false
        }
    }

    @Suppress("UNCHECKED_CAST")
    private fun extractBackingMap(unmodifiableEnv: Any): MutableMap<String, String>? {
        if (unmodifiableEnv is MutableMap<*, *>) {
            return unmodifiableEnv as MutableMap<String, String>
        }

        if (Collections.unmodifiableMap(mutableMapOf<String, String>()).javaClass.isInstance(unmodifiableEnv)) {
            val backingField = unmodifiableEnv.javaClass.getDeclaredField("m")
            backingField.isAccessible = true
            return backingField.get(unmodifiableEnv) as? MutableMap<String, String>
        }

        for (field in unmodifiableEnv.javaClass.declaredFields) {
            if (Modifier.isStatic(field.modifiers) || field.type != Map::class.java) {
                continue
            }
            field.isAccessible = true
            val candidate = field.get(unmodifiableEnv) as? MutableMap<String, String>
            if (candidate != null) {
                return candidate
            }
        }

        return null
    }
}
