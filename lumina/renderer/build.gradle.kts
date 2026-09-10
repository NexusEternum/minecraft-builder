plugins {
    kotlin("jvm")
}

val lwjglVersion: String by project
val lwjglNatives: String by project

dependencies {
    api(project(":plugin-api"))
    implementation(project(":scene"))

    implementation("com.google.inject:guice:${property("guiceVersion")}")

    // LWJGL core + Vulkan + GLFW + STB + Assimp
    implementation(platform("org.lwjgl:lwjgl-bom:$lwjglVersion"))
    implementation("org.lwjgl:lwjgl")
    implementation("org.lwjgl:lwjgl-vulkan")
    implementation("org.lwjgl:lwjgl-glfw")
    implementation("org.lwjgl:lwjgl-stb")
    implementation("org.lwjgl:lwjgl-assimp")
    implementation("org.lwjgl:lwjgl-shaderc")
    implementation("org.lwjgl:lwjgl-vma")

    runtimeOnly("org.lwjgl:lwjgl::$lwjglNatives")
    runtimeOnly("org.lwjgl:lwjgl-glfw::$lwjglNatives")
    runtimeOnly("org.lwjgl:lwjgl-stb::$lwjglNatives")
    runtimeOnly("org.lwjgl:lwjgl-assimp::$lwjglNatives")
    runtimeOnly("org.lwjgl:lwjgl-shaderc::$lwjglNatives")
    runtimeOnly("org.lwjgl:lwjgl-vma::$lwjglNatives")

    // JOML for math
    implementation("org.joml:joml:1.10.8")

    implementation("javax.inject:javax.inject:1")
}
