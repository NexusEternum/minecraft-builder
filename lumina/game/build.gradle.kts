plugins {
    kotlin("jvm")
}

val runeliteClientVersion: String by project

dependencies {
    implementation("net.runelite:client:$runeliteClientVersion")
    implementation("ch.qos.logback:logback-classic:${property("logbackVersion")}")
}

tasks.test {
    jvmArgs(
        "--add-opens", "java.base/java.lang=ALL-UNNAMED",
        "--add-opens", "java.base/java.util=ALL-UNNAMED",
    )
}
