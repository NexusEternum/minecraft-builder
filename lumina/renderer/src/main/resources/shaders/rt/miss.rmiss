#version 460
#extension GL_EXT_ray_tracing : require
#extension GL_EXT_scalar_block_layout : require

layout(location = 0) rayPayloadInEXT RayPayload {
    vec3 color;
    vec3 normal;
    float depth;
    vec3 worldPos;
    uint seed;
    bool missed;
    vec3 brdfWeight;
    vec3 bounceDir;
} payload;

layout(binding = 4, set = 0, scalar) uniform CameraUBO {
    mat4 viewInverse;
    mat4 projInverse;
    mat4 prevViewProj;
    vec3 position;
    float fov;
    uint frameCount;
    uint spp;
    uint maxBounces;
    float time;
} camera;

// Hosek-Wilkie sky model approximation
vec3 proceduralSky(vec3 dir) {
    float timeOfDay = camera.time;
    float sunAngle = timeOfDay * 3.14159265; // still used for sky gradient tint below
    vec3 sunDir = normalize(vec3(0.65, 0.45, 0.4));

    float sunDot = max(dot(dir, sunDir), 0.0);
    float horizon = 1.0 - abs(dir.y);

    // Sky gradient
    vec3 zenithColor = mix(vec3(0.1, 0.15, 0.4), vec3(0.2, 0.4, 0.8), clamp(sin(sunAngle), 0.0, 1.0));
    vec3 horizonColor = mix(vec3(0.8, 0.4, 0.2), vec3(0.6, 0.7, 0.9), clamp(sin(sunAngle), 0.0, 1.0));
    vec3 skyColor = mix(zenithColor, horizonColor, horizon * horizon);

    // Sun disk
    float sunSize = pow(sunDot, 256.0) * 4.0;
    vec3 sunGlow = vec3(1.4, 1.2, 0.9) * pow(sunDot, 8.0) * 0.5;

    // Ground
    if (dir.y < 0.0) {
        skyColor = mix(horizonColor * 0.4, horizonColor, exp(dir.y * 20.0));
    }

    return (skyColor + sunGlow) * 0.6 + vec3(sunSize);
}

void main() {
    payload.color = proceduralSky(gl_WorldRayDirectionEXT);
    payload.normal = vec3(0.0);
    payload.depth = 10000.0;
    payload.worldPos = gl_WorldRayOriginEXT + gl_WorldRayDirectionEXT * 10000.0;
    payload.missed = true;
    payload.brdfWeight = vec3(0.0);
    payload.bounceDir = vec3(0.0);
}
