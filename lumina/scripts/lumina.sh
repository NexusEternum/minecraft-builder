#!/bin/bash
# Lumina OSRS Client launcher for Linux
# Usage: ./lumina.sh [--demo] [--developer-mode]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Check for Java 21+
JAVA_VERSION=$(java -version 2>&1 | head -1 | cut -d'"' -f2 | cut -d'.' -f1)
if [ -z "$JAVA_VERSION" ] || [ "$JAVA_VERSION" -lt 21 ]; then
    echo "Error: Java 21 or newer is required. Found: $(java -version 2>&1 | head -1)"
    echo "Install with: sudo apt install openjdk-21-jdk"
    exit 1
fi

# Check for Vulkan support
if ! vulkaninfo --summary > /dev/null 2>&1; then
    echo "Warning: vulkaninfo not found. Make sure Vulkan drivers are installed."
    echo "  NVIDIA: sudo apt install nvidia-driver-XXX"
    echo "  AMD:    sudo apt install mesa-vulkan-drivers"
fi

FAT_JAR="$PROJECT_DIR/launcher/build/libs/launcher-all.jar"

if [ ! -f "$FAT_JAR" ]; then
    echo "Fat JAR not found. Building..."
    cd "$PROJECT_DIR" && ./gradlew :launcher:fatJar
fi

exec java \
    -Xmx4g \
    -XX:+UseZGC \
    --add-opens java.base/java.lang=ALL-UNNAMED \
    -Dorg.lwjgl.util.DebugLoader=true \
    -jar "$FAT_JAR" \
    "$@"
