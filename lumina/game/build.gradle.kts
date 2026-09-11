plugins {
    kotlin("jvm")
}

val runeliteClientVersion: String by project

configurations.configureEach {
    resolutionStrategy.eachDependency {
        if (requested.group == "com.google.inject" && requested.name == "guice") {
            useTarget("com.google.inject:guice:4.1.0:no_aop")
            because("RuneLite client requires guice no_aop classifier")
        }
    }
}

dependencies {
    implementation(project(":plugin-api"))
    implementation("net.runelite:client:$runeliteClientVersion")
    implementation("ch.qos.logback:logback-classic:${property("logbackVersion")}")
}

tasks.test {
    jvmArgs(
        "--add-opens", "java.base/java.lang=ALL-UNNAMED",
        "--add-opens", "java.base/java.util=ALL-UNNAMED",
    )
}
