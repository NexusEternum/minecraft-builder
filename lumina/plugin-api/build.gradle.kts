plugins {
    kotlin("jvm")
}

dependencies {
    implementation("com.google.inject:guice:${property("guiceVersion")}")
    implementation("com.google.code.gson:gson:${property("gsonVersion")}")
    implementation("javax.inject:javax.inject:1")
}
