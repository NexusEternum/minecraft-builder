plugins {
    kotlin("jvm")
    application
}

application {
    mainClass.set("com.lumina.launcher.LuminaLauncherKt")
    applicationDefaultJvmArgs = listOf(
        "-ea",
        "-Xmx4g",
        "-Xss4m",
        "-XX:+UseZGC",
        "-XX:+DisableAttachMechanism",
        "-XX:CompileThreshold=1500",
        "--add-opens", "java.base/java.lang=ALL-UNNAMED",
        "--add-opens", "java.base/java.util=ALL-UNNAMED",
        "--add-opens", "java.base/java.net=ALL-UNNAMED",
        "--add-opens", "java.base/java.io=ALL-UNNAMED",
        "-Dorg.lwjgl.util.DebugLoader=true",
        "-Dorg.lwjgl.system.stackSize=2048"
    )
}

val lwjglVersion: String by project
val lwjglNatives: String = rootProject.extra["detectedLwjglNatives"] as String

// RuneLite's client POM pins guice:4.1.0:no_aop; conflict resolution to Lumina's 6.0.0
// keeps the classifier and breaks resolution (no guice-6.0.0-no_aop.jar exists).
configurations.configureEach {
    resolutionStrategy.eachDependency {
        if (requested.group == "com.google.inject" && requested.name == "guice") {
            useTarget("com.google.inject:guice:4.1.0:no_aop")
            because("RuneLite client requires guice no_aop classifier on the shared launcher classpath")
        }
    }
}

dependencies {
    implementation(project(":client-core"))
    implementation(project(":plugin-api"))
    implementation(project(":renderer"))
    implementation(project(":scene"))
    // RuneLite client kept off client-core compile classpath; loaded at runtime for --game.
    runtimeOnly(project(":game"))

    implementation("com.google.inject:guice:${property("guiceVersion")}")
    implementation("com.google.code.gson:gson:${property("gsonVersion")}")
    implementation("net.sf.jopt-simple:jopt-simple:${property("joptVersion")}")
    implementation("ch.qos.logback:logback-classic:${property("logbackVersion")}")

    implementation("com.squareup.okhttp3:okhttp:${property("okHttpVersion")}")
    implementation("com.fasterxml.jackson.core:jackson-databind:${property("jacksonVersion")}")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:${property("jacksonVersion")}")

    // LWJGL runtime natives for the fat JAR
    runtimeOnly("org.lwjgl:lwjgl::$lwjglNatives")
    runtimeOnly("org.lwjgl:lwjgl-glfw::$lwjglNatives")
    runtimeOnly("org.lwjgl:lwjgl-stb::$lwjglNatives")
    runtimeOnly("org.lwjgl:lwjgl-assimp::$lwjglNatives")
    runtimeOnly("org.lwjgl:lwjgl-shaderc::$lwjglNatives")
    runtimeOnly("org.lwjgl:lwjgl-vma::$lwjglNatives")
}

tasks.jar {
    manifest {
        attributes["Main-Class"] = "com.lumina.launcher.LuminaLauncherKt"
    }
}

tasks.register<Jar>("fatJar") {
    group = "build"
    description = "Assembles a fat JAR with all dependencies"
    archiveClassifier.set("all")
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE

    manifest {
        attributes["Main-Class"] = "com.lumina.launcher.LuminaLauncherKt"
    }

    from(sourceSets.main.get().output)
    dependsOn(configurations.runtimeClasspath)
    from({
        configurations.runtimeClasspath.get()
            .filter { it.name.endsWith("jar") }
            .map { zipTree(it) }
    })

    exclude("META-INF/*.SF", "META-INF/*.DSA", "META-INF/*.RSA")
}

tasks.register<JavaExec>("runDemo") {
    group = "application"
    description = "Run Lumina in demo mode with the test scene"
    mainClass.set("com.lumina.launcher.LuminaLauncherKt")
    classpath = sourceSets.main.get().runtimeClasspath
    args = listOf("--demo", "--developer-mode")
    jvmArgs = application.applicationDefaultJvmArgs.toList()
}

tasks.register<JavaExec>("runGame") {
    group = "application"
    description = "Boot the real OSRS client via embedded RuneLite"
    mainClass.set("com.lumina.launcher.LuminaLauncherKt")
    classpath = sourceSets.main.get().runtimeClasspath
    args = listOf("--game")
    jvmArgs = application.applicationDefaultJvmArgs.toList()
}
