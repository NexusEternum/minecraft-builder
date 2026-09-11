#version 460
#extension GL_EXT_ray_tracing : require
#extension GL_EXT_scalar_block_layout : require
#extension GL_EXT_nonuniform_qualifier : require

layout(binding = 0, set = 0) uniform accelerationStructureEXT topLevelAS;

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

layout(binding = 5, set = 0, scalar) buffer VertexBuffer { float vertices[]; };
layout(binding = 6, set = 0, scalar) buffer IndexBuffer { uint indices[]; };
layout(binding = 7, set = 0, scalar) buffer MaterialBuffer {
    vec4 materialData[];
};
layout(binding = 8, set = 0, scalar) buffer InstanceInfoBuffer {
    uint instanceInfo[];
};

hitAttributeEXT vec2 attribs;

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

layout(location = 1) rayPayloadEXT bool shadowed;

struct Vertex {
    vec3 pos;
    vec3 normal;
    vec2 uv;
};

Vertex unpackVertex(uint index) {
    uint offset = index * 8;
    Vertex v;
    v.pos = vec3(vertices[offset], vertices[offset+1], vertices[offset+2]);
    v.normal = vec3(vertices[offset+3], vertices[offset+4], vertices[offset+5]);
    v.uv = vec2(vertices[offset+6], vertices[offset+7]);
    return v;
}

uint pcgHash(uint v) {
    uint state = v * 747796405u + 2891336453u;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u;
    return (word >> 22u) ^ word;
}

float randomFloat(inout uint seed) {
    seed = pcgHash(seed);
    return float(seed) / 4294967295.0;
}

vec3 cosineWeightedHemisphere(vec3 normal, inout uint seed) {
    float r1 = randomFloat(seed);
    float r2 = randomFloat(seed);
    float phi = 2.0 * 3.14159265 * r1;
    float cosTheta = sqrt(1.0 - r2);
    float sinTheta = sqrt(r2);

    vec3 w = normal;
    vec3 u = normalize(cross(abs(w.x) > 0.1 ? vec3(0,1,0) : vec3(1,0,0), w));
    vec3 v = cross(w, u);

    return normalize(u * cos(phi) * sinTheta + v * sin(phi) * sinTheta + w * cosTheta);
}

// GGX importance sampling
vec3 sampleGGX(vec3 normal, float roughness, inout uint seed) {
    float a = roughness * roughness;
    float r1 = randomFloat(seed);
    float r2 = randomFloat(seed);

    float phi = 2.0 * 3.14159265 * r1;
    float cosTheta = sqrt((1.0 - r2) / (1.0 + (a*a - 1.0) * r2));
    float sinTheta = sqrt(1.0 - cosTheta * cosTheta);

    vec3 w = normal;
    vec3 u = normalize(cross(abs(w.x) > 0.1 ? vec3(0,1,0) : vec3(1,0,0), w));
    vec3 v = cross(w, u);

    return normalize(u * cos(phi) * sinTheta + v * sin(phi) * sinTheta + w * cosTheta);
}

// Cook-Torrance BRDF
vec3 evaluatePBR(vec3 N, vec3 V, vec3 L, vec3 albedo, float roughness, float metallic) {
    roughness = max(roughness, 0.08);
    vec3 H = normalize(V + L);
    float NdotL = max(dot(N, L), 0.0);
    float NdotV = max(dot(N, V), 0.0);
    float NdotH = max(dot(N, H), 0.0);
    float VdotH = max(dot(V, H), 0.0);

    // Fresnel (Schlick)
    vec3 F0 = mix(vec3(0.04), albedo, metallic);
    vec3 F = F0 + (1.0 - F0) * pow(1.0 - VdotH, 5.0);

    // GGX NDF
    float a2 = roughness * roughness * roughness * roughness;
    float denom = NdotH * NdotH * (a2 - 1.0) + 1.0;
    float D = a2 / (3.14159265 * denom * denom);

    // Smith geometry
    float k = (roughness + 1.0) * (roughness + 1.0) / 8.0;
    float G1V = NdotV / (NdotV * (1.0 - k) + k);
    float G1L = NdotL / (NdotL * (1.0 - k) + k);
    float G = G1V * G1L;

    vec3 specular = (D * F * G) / max(4.0 * NdotV * NdotL, 0.001);
    specular = min(specular, vec3(4.0));
    vec3 diffuse = (1.0 - F) * (1.0 - metallic) * albedo / 3.14159265;

    return (diffuse + specular) * NdotL;
}

void main() {
    uint matIdx = gl_InstanceCustomIndexEXT & 0xFFFFFFu;
    uint indexTriBase = instanceInfo[matIdx];

    uint triIndex = indexTriBase + gl_PrimitiveID;
    uint i0 = indices[triIndex * 3u];
    uint i1 = indices[triIndex * 3u + 1u];
    uint i2 = indices[triIndex * 3u + 2u];

    Vertex v0 = unpackVertex(i0);
    Vertex v1 = unpackVertex(i1);
    Vertex v2 = unpackVertex(i2);

    vec3 bary = vec3(1.0 - attribs.x - attribs.y, attribs.x, attribs.y);
    vec3 worldPos = v0.pos * bary.x + v1.pos * bary.y + v2.pos * bary.z;
    vec3 normal = normalize(v0.normal * bary.x + v1.normal * bary.y + v2.normal * bary.z);

    worldPos = vec3(gl_ObjectToWorldEXT * vec4(worldPos, 1.0));
    normal = normalize(vec3(gl_ObjectToWorldEXT * vec4(normal, 0.0)));
    vec3 albedo = materialData[matIdx * 2u].xyz;
    float roughness = materialData[matIdx * 2u].w;
    vec3 emissive = materialData[matIdx * 2u + 1u].xyz;
    float metallic = materialData[matIdx * 2u + 1u].w;

    // Debug mode: maxBounces==0 outputs flat albedo with simple directional light
    if (camera.maxBounces == 0u) {
        vec3 sunDir = normalize(vec3(0.65, 0.45, 0.4));
        float NdotL = max(dot(normal, sunDir), 0.0);
        payload.color = albedo * (0.15 + 0.85 * NdotL) + emissive;
        payload.normal = normal;
        payload.depth = length(worldPos - gl_WorldRayOriginEXT);
        payload.worldPos = worldPos;
        payload.missed = false;
        payload.brdfWeight = vec3(0.0);
        payload.bounceDir = vec3(0.0);
        return;
    }

    vec3 sunDir = normalize(vec3(0.65, 0.45, 0.4));
    vec3 sunColor = vec3(3.0, 2.7, 2.2);

    shadowed = true;
    traceRayEXT(topLevelAS,
        gl_RayFlagsTerminateOnFirstHitEXT | gl_RayFlagsSkipClosestHitShaderEXT,
        0xFF, 0, 0, 1,
        worldPos + normal * 0.001,
        0.001, sunDir, 10000.0, 1);

    vec3 V = normalize(-gl_WorldRayDirectionEXT);
    vec3 directLight = vec3(0.0);
    if (!shadowed) {
        directLight = evaluatePBR(normal, V, sunDir, albedo, roughness, metallic) * sunColor;
        directLight = min(directLight, vec3(6.0));
        // Mirror-like surfaces get reflections from the traced bounce ray;
        // fade out the analytic highlight to avoid double-counting and fireflies.
        if (metallic > 0.5 && roughness < 0.15) {
            directLight *= roughness / 0.15;
        }
    }

    if (metallic > 0.5 || roughness < 0.3) {
        payload.bounceDir = sampleGGX(normal, roughness, payload.seed);
        payload.brdfWeight = clamp(mix(vec3(0.04), albedo, metallic), 0.0, 1.0);
    } else {
        payload.bounceDir = cosineWeightedHemisphere(normal, payload.seed);
        payload.brdfWeight = clamp(albedo * (1.0 - metallic), 0.0, 1.0);
    }

    vec3 ambient = albedo * vec3(0.01);
    payload.color = emissive + directLight + ambient;
    payload.normal = normal;
    payload.depth = length(worldPos - gl_WorldRayOriginEXT);
    payload.worldPos = worldPos;
    payload.missed = false;
}
