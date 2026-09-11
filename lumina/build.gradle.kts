val kotlinVersion: String by project

plugins {
    kotlin("jvm") version "2.0.21" apply false
}

allprojects {
    group = "com.lumina"
    version = "0.1.0-SNAPSHOT"

    repositories {
        mavenCentral()
        maven("https://repo.spongepowered.org/maven")
        maven("https://repo.runelite.net")
    }
}

val detectedLwjglNatives: String by extra {
    when {
        org.gradle.internal.os.OperatingSystem.current().isWindows -> "natives-windows"
        org.gradle.internal.os.OperatingSystem.current().isMacOsX -> {
            if (System.getProperty("os.arch") == "aarch64") "natives-macos-arm64" else "natives-macos"
        }
        else -> "natives-linux"
    }
}

subprojects {
    apply(plugin = "org.jetbrains.kotlin.jvm")

    val kotlinVersion: String by project
    val lwjglVersion: String by project
    val lwjglNatives = detectedLwjglNatives
    val junitVersion: String by project

    dependencies {
        "implementation"(kotlin("stdlib"))
        "implementation"("org.slf4j:slf4j-api:${property("slf4jVersion")}")

        "testImplementation"("org.junit.jupiter:junit-jupiter:$junitVersion")
        "testRuntimeOnly"("org.junit.platform:junit-platform-launcher")
    }

    tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile> {
        compilerOptions {
            jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_21)
            freeCompilerArgs.addAll("-Xjsr305=strict")
        }
    }

    tasks.withType<JavaCompile> {
        sourceCompatibility = "21"
        targetCompatibility = "21"
    }

    tasks.withType<Test> {
        useJUnitPlatform()
    }
}
