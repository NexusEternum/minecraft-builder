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
    uint pathDepth;
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

// 1.5° half-angle: visible penumbras at OSRS scale (tile 2.56u, walls 2–4u tall)
// without overly soft contact shadows. Solid-angle normalization folded into sunColor.
const float SUN_HALF_ANGLE = 1.5 * 3.14159265 / 180.0;

vec3 sampleSunDirection(vec3 sunCenter, inout uint seed) {
    float r1 = randomFloat(seed);
    float r2 = randomFloat(seed);
    float cosTheta = mix(cos(SUN_HALF_ANGLE), 1.0, r1);
    float sinTheta = sqrt(1.0 - cosTheta * cosTheta);
    float phi = 2.0 * 3.14159265 * r2;

    vec3 w = sunCenter;
    vec3 u = normalize(cross(abs(w.x) > 0.1 ? vec3(0, 1, 0) : vec3(1, 0, 0), w));
    vec3 v = cross(w, u);

    return normalize(u * cos(phi) * sinTheta + v * sin(phi) * sinTheta + w * cosTheta);
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

// GGX importance sampling of microfacet normal H (upper hemisphere around shading normal)
vec3 sampleGGXNormal(vec3 normal, float roughness, inout uint seed) {
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

float luminance(vec3 c) {
    return dot(c, vec3(0.2126, 0.7152, 0.0722));
}

vec3 fresnelSchlick(vec3 F0, float NdotV) {
    return F0 + (1.0 - F0) * pow(1.0 - NdotV, 5.0);
}

// Specular bounce: reflect view around GGX-sampled half-vector; resample if below horizon.
vec3 sampleSpecularBounce(vec3 N, vec3 V, float roughness, inout uint seed) {
    roughness = max(roughness, 0.04);
    for (int attempt = 0; attempt < 4; attempt++) {
        vec3 H = sampleGGXNormal(N, roughness, seed);
        vec3 L = normalize(reflect(-V, H));
        if (dot(N, L) > 0.0) {
            return L;
        }
    }
    return cosineWeightedHemisphere(N, seed);
}

// Cook-Torrance BRDF
vec3 evaluatePBR(vec3 N, vec3 V, vec3 L, vec3 albedo, float roughness, float metallic) {
    roughness = max(roughness, 0.04);
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

    if (metallic > 1.5) {
        // Vertex-color mode: albedo packed into uv.x bits (rgb8)
        uint packed0 = floatBitsToUint(v0.uv.x);
        // NOTE: all three vertices of a terrain triangle carry the same tile color,
        // so just use v0's.
        vec3 tileRgb = vec3(
            float((packed0 >> 16) & 0xFFu),
            float((packed0 >> 8) & 0xFFu),
            float(packed0 & 0xFFu)
        ) / 255.0;
        albedo *= tileRgb;
        metallic = 0.0;
    }

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

    vec3 sunCenter = normalize(vec3(0.65, 0.45, 0.4));
    vec3 sunColor = vec3(3.0, 2.7, 2.2);
    vec3 sunDir = sampleSunDirection(sunCenter, payload.seed);

    // v1 approximation — opaque-only shadow ray; glass attenuation via second translucent-only ray below.
    shadowed = true;
    traceRayEXT(topLevelAS,
        gl_RayFlagsTerminateOnFirstHitEXT | gl_RayFlagsSkipClosestHitShaderEXT,
        0x01, 0, 0, 1,
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

        // Second ray: translucent-only (mask 0x2). If stained glass is in the sun path,
        // attenuate and tint. True per-pane tint needs an any-hit/hit-shader fetch — future work.
        shadowed = true;
        traceRayEXT(topLevelAS,
            gl_RayFlagsTerminateOnFirstHitEXT | gl_RayFlagsSkipClosestHitShaderEXT,
            0x02, 0, 0, 1,
            worldPos + normal * 0.001,
            0.001, sunDir, 10000.0, 1);
        if (shadowed) {
            directLight *= 0.5 * vec3(0.65, 0.85, 0.7);
        }
    }

    roughness = max(roughness, 0.04);
    vec3 F0 = mix(vec3(0.04), albedo, metallic);
    float NdotV = max(dot(normal, V), 0.0);
    vec3 F = fresnelSchlick(F0, NdotV);
    // Rough dielectrics: pure diffuse bounce (pre-b28). Smooth dielectrics + metals: two-lobe sampling.
    bool useSpecularLobe = metallic >= 0.5 || roughness <= 0.3;
    float pSpec = 0.0;
    float pDiff = 1.0;
    if (useSpecularLobe) {
        pSpec = clamp(luminance(F0) + (1.0 - roughness) * 0.5, 0.05, 0.75);
        pDiff = 1.0 - pSpec;
    }

    if (useSpecularLobe && randomFloat(payload.seed) < pSpec) {
        payload.bounceDir = sampleSpecularBounce(normal, V, roughness, payload.seed);
        // Specular throughput: Fresnel (not albedo for dielectrics); unbiased via 1/pSpec.
        payload.brdfWeight = min(max(F / pSpec, vec3(0.0)), vec3(4.0));
    } else {
        payload.bounceDir = cosineWeightedHemisphere(normal, payload.seed);
        if (useSpecularLobe) {
            // Diffuse throughput: albedo scaled by (1-metallic); unbiased via 1/pDiff.
            payload.brdfWeight = min(max(albedo * (1.0 - metallic) / pDiff, vec3(0.0)), vec3(4.0));
        } else {
            payload.brdfWeight = min(max(albedo * (1.0 - metallic), vec3(0.0)), vec3(4.0));
        }
    }

    vec3 ambient = albedo * vec3(0.01);
    payload.color = emissive + directLight + ambient;
    payload.normal = normal;
    payload.depth = length(worldPos - gl_WorldRayOriginEXT);
    payload.worldPos = worldPos;
    payload.missed = false;
}
