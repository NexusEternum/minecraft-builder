plugins {
    kotlin("jvm")
    application
}

application {
    mainClass.set("com.lumina.launcher.LuminaLauncherKt")
}

dependencies {
    implementation(project(":client-core"))
    implementation(project(":plugin-api"))

    implementation("com.google.inject:guice:${property("guiceVersion")}")
    implementation("com.google.code.gson:gson:${property("gsonVersion")}")
    implementation("net.sf.jopt-simple:jopt-simple:${property("joptVersion")}")
    implementation("ch.qos.logback:logback-classic:${property("logbackVersion")}")

    implementation("com.squareup.okhttp3:okhttp:${property("okHttpVersion")}")
    implementation("com.fasterxml.jackson.core:jackson-databind:${property("jacksonVersion")}")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:${property("jacksonVersion")}")
}

tasks.jar {
    manifest {
        attributes["Main-Class"] = "com.lumina.launcher.LuminaLauncherKt"
    }
}
