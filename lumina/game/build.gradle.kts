plugins {
    kotlin("jvm")
}

val runeliteClientVersion: String by project

dependencies {
    implementation("net.runelite:client:$runeliteClientVersion")
    implementation("ch.qos.logback:logback-classic:${property("logbackVersion")}")
}
