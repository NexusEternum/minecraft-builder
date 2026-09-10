plugins {
    kotlin("jvm")
    application
}

application {
    mainClass.set("com.lumina.launcher.LuminaLauncherKt")
    applicationDefaultJvmArgs = listOf(
        "-Xmx4g",
        "-XX:+UseZGC",
        "--add-opens", "java.base/java.lang=ALL-UNNAMED",
        "-Dorg.lwjgl.util.DebugLoader=true"
    )
}

val lwjglVersion: String by project
val lwjglNatives: String by project

dependencies {
    implementation(project(":client-core"))
    implementation(project(":plugin-api"))
    implementation(project(":renderer"))
    implementation(project(":scene"))

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
}

tasks.register<JavaExec>("runDemo") {
    group = "application"
    description = "Run Lumina in demo mode with the test scene"
    mainClass.set("com.lumina.launcher.LuminaLauncherKt")
    classpath = sourceSets.main.get().runtimeClasspath
    args = listOf("--demo", "--developer-mode")
    jvmArgs = listOf(
        "-Xmx4g",
        "-XX:+UseZGC",
        "--add-opens", "java.base/java.lang=ALL-UNNAMED"
    )
}
