plugins {
    kotlin("jvm")
}

dependencies {
    api(project(":plugin-api"))
    implementation(project(":scene"))
    implementation(project(":renderer"))

    implementation("com.google.inject:guice:${property("guiceVersion")}")
    implementation("com.google.code.gson:gson:${property("gsonVersion")}")
    implementation("net.sf.jopt-simple:jopt-simple:${property("joptVersion")}")
    implementation("ch.qos.logback:logback-classic:${property("logbackVersion")}")

    implementation("com.squareup.okhttp3:okhttp:${property("okHttpVersion")}")
    implementation("com.fasterxml.jackson.core:jackson-databind:${property("jacksonVersion")}")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:${property("jacksonVersion")}")

    // Mixin for bytecode injection
    implementation("org.spongepowered:mixin:${property("mixinVersion")}")

    implementation("javax.inject:javax.inject:1")

    val lwjglVersion: String by project
    implementation("org.lwjgl:lwjgl-glfw:$lwjglVersion")

    testImplementation("org.junit.jupiter:junit-jupiter:${property("junitVersion")}")
}

tasks.test {
    useJUnitPlatform()
}
