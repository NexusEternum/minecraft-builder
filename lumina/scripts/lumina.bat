@echo off
REM Lumina OSRS Client launcher for Windows
REM Usage: lumina.bat [--demo] [--developer-mode]

set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..

set FAT_JAR=%PROJECT_DIR%\launcher\build\libs\launcher-all.jar

if not exist "%FAT_JAR%" (
    echo Fat JAR not found. Building...
    cd /d "%PROJECT_DIR%" && gradlew.bat :launcher:fatJar
)

java ^
    -Xmx4g ^
    -XX:+UseZGC ^
    --add-opens java.base/java.lang=ALL-UNNAMED ^
    -Dorg.lwjgl.util.DebugLoader=true ^
    -jar "%FAT_JAR%" ^
    %*
