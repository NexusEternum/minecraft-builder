package com.lumina.renderer.vulkan

import org.lwjgl.glfw.GLFW.*
import org.lwjgl.glfw.GLFWVulkan
import org.lwjgl.system.MemoryStack
import org.lwjgl.system.MemoryUtil.NULL
import org.lwjgl.vulkan.*
import org.lwjgl.vulkan.EXTDebugUtils.*
import org.lwjgl.vulkan.KHRAccelerationStructure.*
import org.lwjgl.vulkan.KHRBufferDeviceAddress.VK_BUFFER_USAGE_SHADER_DEVICE_ADDRESS_BIT_KHR
import org.lwjgl.vulkan.KHRDeferredHostOperations.VK_KHR_DEFERRED_HOST_OPERATIONS_EXTENSION_NAME
import org.lwjgl.vulkan.KHRRayTracingPipeline.VK_KHR_RAY_TRACING_PIPELINE_EXTENSION_NAME
import org.lwjgl.vulkan.KHRRayTracingPipeline.VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_RAY_TRACING_PIPELINE_FEATURES_KHR
import org.lwjgl.vulkan.KHRSurface.*
import org.lwjgl.vulkan.KHRSwapchain.*
import org.lwjgl.vulkan.VK13.*
import org.slf4j.LoggerFactory
import javax.inject.Singleton

@Singleton
class VulkanContext {
    private val log = LoggerFactory.getLogger(VulkanContext::class.java)

    var window: Long = NULL; private set
    var instance: VkInstance? = null; private set
    var physicalDevice: VkPhysicalDevice? = null; private set
    var device: VkDevice? = null; private set
    var graphicsQueue: VkQueue? = null; private set
    var presentQueue: VkQueue? = null; private set
    var surface: Long = NULL; private set
    var swapchain: Long = NULL; private set
    var swapchainImages: List<Long> = emptyList(); private set
    var swapchainImageViews: List<Long> = emptyList(); private set
    var swapchainFormat: Int = VK_FORMAT_B8G8R8A8_SRGB; private set
    var swapchainExtent: VkExtent2D? = null; private set
    var commandPool: Long = NULL; private set
    var graphicsQueueFamily: Int = -1; private set
    var presentQueueFamily: Int = -1; private set
    var rtSupported: Boolean = false; private set
    var width: Int = 1280; private set
    var height: Int = 720; private set

    private var debugMessenger: Long = NULL

    fun init(title: String = "Lumina", w: Int = 1280, h: Int = 720, enableValidation: Boolean = false) {
        width = w; height = h

        log.info("Initializing GLFW...")
        if (!glfwInit()) {
            log.error("Failed to initialize GLFW. Make sure your graphics drivers are installed.")
            throw RuntimeException("Failed to init GLFW")
        }

        if (!GLFWVulkan.glfwVulkanSupported()) {
            log.error("Vulkan is not supported on this system.")
            log.error("Make sure you have up-to-date GPU drivers installed:")
            log.error("  NVIDIA: https://www.nvidia.com/Download/index.aspx")
            log.error("  AMD:    https://www.amd.com/en/support")
            throw RuntimeException("Vulkan not supported by GLFW")
        }
        log.info("GLFW initialized, Vulkan supported")

        glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API)
        glfwWindowHint(GLFW_RESIZABLE, GLFW_TRUE)
        window = glfwCreateWindow(w, h, title, NULL, NULL)
        if (window == NULL) {
            log.error("Failed to create window ({}x{})", w, h)
            throw RuntimeException("Failed to create GLFW window")
        }
        log.info("Window created ({}x{})", w, h)

        log.info("Creating Vulkan instance...")
        createInstance(title, enableValidation)
        log.info("Creating surface...")
        createSurface()
        log.info("Picking physical device (GPU)...")
        pickPhysicalDevice()
        log.info("Creating logical device...")
        createLogicalDevice(enableValidation)
        log.info("Creating swapchain...")
        createSwapchain()
        log.info("Creating command pool...")
        createCommandPool()

        log.info("Vulkan initialized: {} (RT: {})", getDeviceName(), rtSupported)
    }

    private fun createInstance(appName: String, enableValidation: Boolean) {
        MemoryStack.stackPush().use { stack ->
            val appInfo = VkApplicationInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_APPLICATION_INFO)
                .pApplicationName(stack.UTF8(appName))
                .applicationVersion(VK_MAKE_VERSION(0, 1, 0))
                .pEngineName(stack.UTF8("Lumina Engine"))
                .engineVersion(VK_MAKE_VERSION(0, 1, 0))
                .apiVersion(VK_API_VERSION_1_3)

            val glfwExtensions = GLFWVulkan.glfwGetRequiredInstanceExtensions()
                ?: throw RuntimeException("No Vulkan extensions from GLFW")

            val extensionCount = glfwExtensions.capacity() + if (enableValidation) 1 else 0
            val extensions = stack.mallocPointer(extensionCount)
            for (i in 0 until glfwExtensions.capacity()) extensions.put(glfwExtensions.get(i))
            if (enableValidation) extensions.put(stack.UTF8(VK_EXT_DEBUG_UTILS_EXTENSION_NAME))
            extensions.flip()

            val createInfo = VkInstanceCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO)
                .pApplicationInfo(appInfo)
                .ppEnabledExtensionNames(extensions)

            if (enableValidation) {
                val layers = stack.mallocPointer(1).put(stack.UTF8("VK_LAYER_KHRONOS_validation")).flip()
                createInfo.ppEnabledLayerNames(layers)
            }

            val pInstance = stack.mallocPointer(1)
            check(vkCreateInstance(createInfo, null, pInstance) == VK_SUCCESS) { "Failed to create Vulkan instance" }
            instance = VkInstance(pInstance.get(0), createInfo)
        }
    }

    private fun createSurface() {
        val inst = instance!!
        MemoryStack.stackPush().use { stack ->
            val pSurface = stack.mallocLong(1)
            check(GLFWVulkan.glfwCreateWindowSurface(inst, window, null, pSurface) == VK_SUCCESS)
            surface = pSurface.get(0)
        }
    }

    private fun pickPhysicalDevice() {
        val inst = instance!!
        MemoryStack.stackPush().use { stack ->
            val count = stack.mallocInt(1)
            vkEnumeratePhysicalDevices(inst, count, null)
            check(count.get(0) > 0) { "No Vulkan-capable GPUs found" }

            val devices = stack.mallocPointer(count.get(0))
            vkEnumeratePhysicalDevices(inst, count, devices)

            var bestDevice: VkPhysicalDevice? = null
            var bestScore = -1

            for (i in 0 until count.get(0)) {
                val dev = VkPhysicalDevice(devices.get(i), inst)
                val props = VkPhysicalDeviceProperties.calloc(stack)
                vkGetPhysicalDeviceProperties(dev, props)

                var score = 0
                if (props.deviceType() == VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU) score += 1000
                score += props.limits().maxImageDimension2D()

                if (score > bestScore) {
                    bestScore = score
                    bestDevice = dev
                }
            }

            physicalDevice = bestDevice ?: throw RuntimeException("No suitable GPU")
            rtSupported = checkRTSupport()
        }
    }

    private fun checkRTSupport(): Boolean {
        val physDev = physicalDevice!!
        MemoryStack.stackPush().use { stack ->
            val count = stack.mallocInt(1)
            vkEnumerateDeviceExtensionProperties(physDev, null as CharSequence?, count, null)
            val props = VkExtensionProperties.calloc(count.get(0), stack)
            vkEnumerateDeviceExtensionProperties(physDev, null as CharSequence?, count, props)

            val available = mutableSetOf<String>()
            for (i in 0 until count.get(0)) {
                available.add(props.get(i).extensionNameString())
            }

            val rtExtensions = listOf(
                VK_KHR_ACCELERATION_STRUCTURE_EXTENSION_NAME,
                VK_KHR_RAY_TRACING_PIPELINE_EXTENSION_NAME,
                VK_KHR_DEFERRED_HOST_OPERATIONS_EXTENSION_NAME
            )

            return rtExtensions.all { it in available }.also {
                if (it) log.info("Hardware ray tracing supported")
                else log.warn("Hardware ray tracing NOT supported, using compute fallback")
            }
        }
    }

    private fun createLogicalDevice(enableValidation: Boolean) {
        val physDev = physicalDevice!!
        MemoryStack.stackPush().use { stack ->
            val queueFamilyCount = stack.mallocInt(1)
            vkGetPhysicalDeviceQueueFamilyProperties(physDev, queueFamilyCount, null)
            val queueFamilies = VkQueueFamilyProperties.calloc(queueFamilyCount.get(0), stack)
            vkGetPhysicalDeviceQueueFamilyProperties(physDev, queueFamilyCount, queueFamilies)

            graphicsQueueFamily = -1
            presentQueueFamily = -1
            val pSupported = stack.mallocInt(1)

            for (i in 0 until queueFamilyCount.get(0)) {
                if (queueFamilies.get(i).queueFlags() and VK_QUEUE_GRAPHICS_BIT != 0) {
                    graphicsQueueFamily = i
                }
                vkGetPhysicalDeviceSurfaceSupportKHR(physDev, i, surface, pSupported)
                if (pSupported.get(0) == VK_TRUE) {
                    presentQueueFamily = i
                }
                if (graphicsQueueFamily >= 0 && presentQueueFamily >= 0) break
            }

            val uniqueFamilies = setOf(graphicsQueueFamily, presentQueueFamily)
            val queueCreateInfos = VkDeviceQueueCreateInfo.calloc(uniqueFamilies.size, stack)
            val priority = stack.floats(1.0f)
            for ((idx, family) in uniqueFamilies.withIndex()) {
                queueCreateInfos.get(idx)
                    .sType(VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO)
                    .queueFamilyIndex(family)
                    .pQueuePriorities(priority)
            }

            val deviceExtensions = mutableListOf(VK_KHR_SWAPCHAIN_EXTENSION_NAME)
            if (rtSupported) {
                deviceExtensions.addAll(listOf(
                    VK_KHR_ACCELERATION_STRUCTURE_EXTENSION_NAME,
                    VK_KHR_RAY_TRACING_PIPELINE_EXTENSION_NAME,
                    VK_KHR_DEFERRED_HOST_OPERATIONS_EXTENSION_NAME,
                    "VK_KHR_buffer_device_address"
                ))
            }

            val ppExtensions = stack.mallocPointer(deviceExtensions.size)
            for (ext in deviceExtensions) ppExtensions.put(stack.UTF8(ext))
            ppExtensions.flip()

            val createInfo = VkDeviceCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO)
                .pQueueCreateInfos(queueCreateInfos)
                .ppEnabledExtensionNames(ppExtensions)

            if (rtSupported) {
                val bdaFeatures = VkPhysicalDeviceBufferDeviceAddressFeatures.calloc(stack)
                    .sType(VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_BUFFER_DEVICE_ADDRESS_FEATURES)
                    .bufferDeviceAddress(true)

                val asFeatures = VkPhysicalDeviceAccelerationStructureFeaturesKHR.calloc(stack)
                    .sType(KHRAccelerationStructure.VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_ACCELERATION_STRUCTURE_FEATURES_KHR)
                    .accelerationStructure(true)
                    .pNext(bdaFeatures.address())

                val rtpFeatures = VkPhysicalDeviceRayTracingPipelineFeaturesKHR.calloc(stack)
                    .sType(VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_RAY_TRACING_PIPELINE_FEATURES_KHR)
                    .rayTracingPipeline(true)
                    .pNext(asFeatures.address())

                val features2 = VkPhysicalDeviceFeatures2.calloc(stack)
                    .sType(VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_FEATURES_2)
                    .pNext(rtpFeatures.address())

                createInfo.pNext(features2.address())
            } else {
                val features = VkPhysicalDeviceFeatures.calloc(stack)
                createInfo.pEnabledFeatures(features)
            }

            val pDevice = stack.mallocPointer(1)
            check(vkCreateDevice(physDev, createInfo, null, pDevice) == VK_SUCCESS)
            device = VkDevice(pDevice.get(0), physDev, createInfo)

            val dev = device!!
            val pQueue = stack.mallocPointer(1)
            vkGetDeviceQueue(dev, graphicsQueueFamily, 0, pQueue)
            graphicsQueue = VkQueue(pQueue.get(0), dev)
            vkGetDeviceQueue(dev, presentQueueFamily, 0, pQueue)
            presentQueue = VkQueue(pQueue.get(0), dev)
        }
    }

    private fun createSwapchain() {
        val dev = device!!
        val physDev = physicalDevice!!
        MemoryStack.stackPush().use { stack ->
            val caps = VkSurfaceCapabilitiesKHR.calloc(stack)
            vkGetPhysicalDeviceSurfaceCapabilitiesKHR(physDev, surface, caps)

            val formatCount = stack.mallocInt(1)
            vkGetPhysicalDeviceSurfaceFormatsKHR(physDev, surface, formatCount, null)
            val formats = VkSurfaceFormatKHR.calloc(formatCount.get(0), stack)
            vkGetPhysicalDeviceSurfaceFormatsKHR(physDev, surface, formatCount, formats)

            swapchainFormat = VK_FORMAT_B8G8R8A8_SRGB
            var colorSpace = VK_COLOR_SPACE_SRGB_NONLINEAR_KHR
            for (i in 0 until formatCount.get(0)) {
                if (formats.get(i).format() == VK_FORMAT_B8G8R8A8_SRGB) {
                    colorSpace = formats.get(i).colorSpace()
                    break
                }
            }

            val extent = VkExtent2D.calloc(stack)
            if (caps.currentExtent().width() != -1) {
                extent.set(caps.currentExtent())
            } else {
                extent.width(width.coerceIn(caps.minImageExtent().width(), caps.maxImageExtent().width()))
                extent.height(height.coerceIn(caps.minImageExtent().height(), caps.maxImageExtent().height()))
            }
            swapchainExtent = VkExtent2D.create().set(extent)

            var imageCount = caps.minImageCount() + 1
            if (caps.maxImageCount() > 0) imageCount = imageCount.coerceAtMost(caps.maxImageCount())

            val createInfo = VkSwapchainCreateInfoKHR.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR)
                .surface(surface)
                .minImageCount(imageCount)
                .imageFormat(swapchainFormat)
                .imageColorSpace(colorSpace)
                .imageExtent(extent)
                .imageArrayLayers(1)
                .imageUsage(VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT or VK_IMAGE_USAGE_TRANSFER_DST_BIT)
                .preTransform(caps.currentTransform())
                .compositeAlpha(VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR)
                .presentMode(VK_PRESENT_MODE_FIFO_KHR)
                .clipped(true)

            if (graphicsQueueFamily != presentQueueFamily) {
                createInfo.imageSharingMode(VK_SHARING_MODE_CONCURRENT)
                createInfo.pQueueFamilyIndices(stack.ints(graphicsQueueFamily, presentQueueFamily))
            } else {
                createInfo.imageSharingMode(VK_SHARING_MODE_EXCLUSIVE)
            }

            val pSwapchain = stack.mallocLong(1)
            check(vkCreateSwapchainKHR(dev, createInfo, null, pSwapchain) == VK_SUCCESS)
            swapchain = pSwapchain.get(0)

            val pCount = stack.mallocInt(1)
            vkGetSwapchainImagesKHR(dev, swapchain, pCount, null)
            val pImages = stack.mallocLong(pCount.get(0))
            vkGetSwapchainImagesKHR(dev, swapchain, pCount, pImages)

            swapchainImages = (0 until pCount.get(0)).map { pImages.get(it) }
            swapchainImageViews = swapchainImages.map { createImageView(it, swapchainFormat) }
        }
    }

    private fun createImageView(image: Long, format: Int): Long {
        val dev = device!!
        MemoryStack.stackPush().use { stack ->
            val viewInfo = VkImageViewCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO)
                .image(image)
                .viewType(VK_IMAGE_VIEW_TYPE_2D)
                .format(format)
            viewInfo.subresourceRange()
                .aspectMask(VK_IMAGE_ASPECT_COLOR_BIT)
                .baseMipLevel(0).levelCount(1)
                .baseArrayLayer(0).layerCount(1)

            val pView = stack.mallocLong(1)
            check(vkCreateImageView(dev, viewInfo, null, pView) == VK_SUCCESS)
            return pView.get(0)
        }
    }

    private fun createCommandPool() {
        MemoryStack.stackPush().use { stack ->
            val poolInfo = VkCommandPoolCreateInfo.calloc(stack)
                .sType(VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO)
                .flags(VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT)
                .queueFamilyIndex(graphicsQueueFamily)
            val pPool = stack.mallocLong(1)
            check(vkCreateCommandPool(device!!, poolInfo, null, pPool) == VK_SUCCESS)
            commandPool = pPool.get(0)
        }
    }

    fun getDeviceName(): String {
        MemoryStack.stackPush().use { stack ->
            val props = VkPhysicalDeviceProperties.calloc(stack)
            vkGetPhysicalDeviceProperties(physicalDevice!!, props)
            return props.deviceNameString()
        }
    }

    fun destroy() {
        device?.let { dev ->
            vkDeviceWaitIdle(dev)
            if (commandPool != NULL) vkDestroyCommandPool(dev, commandPool, null)
            swapchainImageViews.forEach { vkDestroyImageView(dev, it, null) }
            if (swapchain != NULL) vkDestroySwapchainKHR(dev, swapchain, null)
            vkDestroyDevice(dev, null)
        }
        instance?.let { inst ->
            if (surface != NULL) vkDestroySurfaceKHR(inst, surface, null)
            vkDestroyInstance(inst, null)
        }
        if (window != NULL) { glfwDestroyWindow(window); glfwTerminate() }
        log.info("Vulkan context destroyed")
    }
}
