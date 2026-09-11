plugins {
    kotlin("jvm")
}

dependencies {
    api(project(":plugin-api"))
    implementation("com.google.inject:guice:${property("guiceVersion")}")
    implementation("com.google.code.gson:gson:${property("gsonVersion")}")
    implementation("javax.inject:javax.inject:1")
    implementation("net.runelite:cache:1.12.38")
}
