---
title: "EasyVulkan 第六章学习笔记"
slug: "easyvulkan-chapter-6"
summary: "整理 Vulkan 新版本特性查询与启用、pNext 扩展链、无图像帧缓冲和动态渲染的使用流程。"
categories: ["Vulkan"]
tags: ["Vulkan", "EasyVulkan", "Dynamic Rendering", "Framebuffer", "Rendering"]
date: "2026-07-26T06:35:09.000Z"
lastmod: "2026-07-26T08:05:58.000Z"
draft: false
yuque_slug: "douio0pyg8snnk8n"
source: "https://www.yuque.com/u62694975/iaaa/douio0pyg8snnk8n"
---

<a id="ud80b324f"></a>第六章的核心目标，是学习 Vulkan 1.1、Vulkan 1.2 和 Vulkan 1.3 中加入的新特性，以及如何在程序中查询、启用和使用这些特性。

<a id="ue7ea89ec"></a>这一章主要包含以下内容：

- <a id="u03d38c55"></a>如何查询 Vulkan Loader 支持的最高版本
- <a id="u15bc94a3"></a>如何查询物理设备支持的特性
- <a id="u1e4c9bc5"></a>如何使用 `pNext` 扩展结构体
- <a id="ub2a8b502"></a>如何启用新版本 Vulkan 功能
- <a id="u363f21d0"></a>如何使用无图像帧缓冲
- <a id="u30a79167"></a>如何使用动态渲染
- <a id="ucd2707a5"></a>如何在不依赖传统 Render Pass 和 Framebuffer 的情况下完成绘制

<a id="ua220ee10"></a>第六章与第七章的侧重点不同，

<a id="u7c0653fc"></a>第七章主要解决：数据如何进入 GPU

<a id="u76f78903"></a>第六章主要解决：如何使用现代 Vulkan 功能组织渲染流程

<a id="ue88d60e7"></a>这一章最重要的内容是：

<a id="ATWro"></a>
```latex
Ch6-0 新版本特性查询
Ch6-2 动态渲染
```

<a id="nfYkS"></a>

---

<a id="s3I98"></a>
## 一、Ch6-0 使用新版本特性

<a id="uc8638175"></a>Vulkan 在后续版本中不断增加新的功能。

<a id="uecaa68ad"></a>例如：

- <a id="ufb7d024f"></a>Vulkan 1.1
- <a id="u244955fc"></a>Vulkan 1.2
- <a id="u3c1e2fe1"></a>Vulkan 1.3
- <a id="uf59fb948"></a>各种 KHR 扩展
- <a id="u05596c5e"></a>各种 EXT 扩展
- <a id="u211efcab"></a>厂商扩展

<a id="u9129a58a"></a>这些新功能通常不能直接使用。

<a id="u1bb830cf"></a>在使用之前需要完成：

<a id="NZXAu"></a>
```latex
确认 Loader 支持
→ 确认物理设备支持
→ 查询对应 Feature
→ 创建逻辑设备时启用
→ 获取对应函数
→ 正式使用
```

<a id="Wh13i"></a>

---

<a id="w03C0"></a>
### 1. Vulkan Loader 版本

<a id="u16c2a25c"></a>Vulkan 程序通常不会直接与显卡驱动中的 Vulkan 实现交互。

<a id="ufa49fbc2"></a>程序首先通过 Vulkan Loader 加载 Vulkan API。

<a id="ue54257a0"></a>Loader 支持的 Vulkan 版本可以通过：

<a id="TLpau"></a>
```cpp
vkEnumerateInstanceVersion(...)
```

<a id="u309d3545"></a>查询。

<a id="u88de6a35"></a>例如：

<a id="xLVaf"></a>
```cpp
uint32_t apiVersion = VK_API_VERSION_1_0;

if (vkEnumerateInstanceVersion != nullptr) {
    vkEnumerateInstanceVersion(&apiVersion);
}
```

<a id="u05a056e2"></a>版本号可以通过以下宏拆分：

<a id="JTA6l"></a>
```cpp
VK_API_VERSION_MAJOR(apiVersion)
VK_API_VERSION_MINOR(apiVersion)
VK_API_VERSION_PATCH(apiVersion)
```

<a id="u61aaefc5"></a>需要注意：

<a id="hbV9V"></a>
```latex
Loader 支持 Vulkan 1.3
不代表当前 GPU 一定支持 Vulkan 1.3
```

<a id="ue393c999"></a>Loader 版本表示当前运行环境能够识别和加载的 Vulkan API 版本。

<a id="u90391419"></a>物理设备版本表示具体 GPU 和驱动实际支持的 Vulkan 版本。

<a id="WM775"></a>

---

<a id="fd5s7"></a>
### 2. VkApplicationInfo 中的 API 版本

<a id="ua2899b28"></a>创建 Vulkan Instance 时，需要填写：

<a id="lTtvS"></a>
```cpp
VkApplicationInfo
```

<a id="ua710a5b8"></a>其中：

<a id="znzcQ"></a>
```cpp
apiVersion
```

<a id="u7bf9454b"></a>表示程序希望使用的 Vulkan API 版本。

<a id="u46cfe4fd"></a>例如：

<a id="aSam4"></a>
```cpp
VkApplicationInfo applicationInfo{};
applicationInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
applicationInfo.apiVersion = VK_API_VERSION_1_3;
```

<a id="ue9dd5909"></a>但是不能直接假设运行环境一定支持 Vulkan 1.3。

<a id="u8a14c956"></a>更合理的做法是：

<a id="xoRBm"></a>
```latex
查询 Loader 最高版本
→ 根据程序需求选择版本
→ 不能超过 Loader 支持版本
```

<a id="u83491a23"></a>例如：

<a id="Ximph"></a>
```cpp
uint32_t requestedVersion = VK_API_VERSION_1_3;
uint32_t finalVersion = std::min(loaderVersion, requestedVersion);
```

<a id="UMDK5"></a>

---

<a id="XkjDs"></a>
### 3. 物理设备 API 版本

<a id="u2660e4ae"></a>物理设备属性中包含：

<a id="WwLTR"></a>
```cpp
VkPhysicalDeviceProperties::apiVersion
```

<a id="u53b40946"></a>可以通过：

<a id="Yq3RP"></a>
```cpp
vkGetPhysicalDeviceProperties(...)
```

<a id="u5831c36e"></a>查询。

<a id="u9b5b5080"></a>也可以使用新版接口：

<a id="KfMWL"></a>
```cpp
vkGetPhysicalDeviceProperties2(...)
```

<a id="u94bbc86a"></a>设备支持版本与 Loader 支持版本必须同时考虑。

<a id="ubfd96877"></a>可以简单理解为：

<a id="HUKYf"></a>
```latex
Loader Version
= 当前系统最多能够加载哪个 Vulkan 版本

Physical Device Version
= 当前 GPU 和驱动实际实现了哪个 Vulkan 版本

Application Version
= 程序希望使用哪个 Vulkan 版本
```

<a id="u5e8333d6"></a>最终可用版本受到三者共同限制。

<a id="mS8Ps"></a>

---

<a id="FTqJo"></a>
## 二、Feature、Property 与 Extension

<a id="u6bc951ad"></a>Vulkan 中经常会遇到三类设备能力信息：

<a id="OkFL2"></a>
```latex
Feature
Property
Extension
```

<a id="mxngp"></a>

---

<a id="rRTGd"></a>
### 1. Feature

<a id="u6f89ab50"></a>Feature 表示<strong>某项功能是否受到支持</strong>。

<a id="u2bfccae2"></a>例如：

<a id="Fs4Eb"></a>
```cpp
samplerAnisotropy
geometryShader
tessellationShader
dynamicRendering
imagelessFramebuffer
```

<a id="u5230826f"></a>Feature 通常是布尔值：

<a id="YVOZN"></a>
```cpp
VK_TRUE
VK_FALSE
```

<a id="u6e6bb431"></a>例如：

<a id="wPCYz"></a>
```latex
samplerAnisotropy = VK_TRUE
```

<a id="ua0dc3668"></a>表示设备支持各向异性过滤。

<a id="u576739d2"></a>但是：

<a id="wSknM"></a>
```latex
支持某项 Feature
不等于已经启用某项 Feature
```

<a id="u4792a1e4"></a>创建逻辑设备时，<strong>只有显式开启的 Feature 才能使用</strong>。

<a id="MRZQU"></a>

---

<a id="n5ltF"></a>
### 2. Property

<a id="ue413da1f"></a>Property 表示<strong>设备的属性或限制</strong>。

<a id="ufab0ffa4"></a>例如：

<a id="vZFiJ"></a>
```cpp
maxImageDimension2D
maxPushConstantsSize
minUniformBufferOffsetAlignment
maxSamplerAnisotropy
```

<a id="ud3821840"></a>这些通常不是开关，而是具体数值。

<a id="u010a0704"></a>例如：

<a id="m2wUV"></a>
```latex
maxPushConstantsSize = 256
```

<a id="ue0a48e40"></a>表示设备允许的 Push Constant 最大容量为 256 字节。

<a id="ud305124a"></a>Property <strong>只能查询，不能开启</strong>。

<a id="Zz2Yt"></a>

---

<a id="hndlc"></a>
### 3. Extension

<a id="uf7b0ae54"></a>Extension 表示<strong> Vulkan 核心版本之外提供的额外功能</strong>。

<a id="u08302327"></a>例如：

<a id="iUs8K"></a>
```latex
VK_KHR_swapchain
VK_KHR_dynamic_rendering
VK_KHR_create_renderpass2
```

<a id="u9ac9a5c6"></a>扩展通常需要：

1. <a id="u3a5cc7d5"></a>查询是否支持
2. <a id="uad619e9d"></a>在创建 Instance 或 Device 时添加扩展名称
3. <a id="u8b5ef4f1"></a>查询对应 Feature
4. <a id="u5b240e48"></a>开启对应 Feature
5. <a id="ubb570028"></a>使用扩展函数

<a id="u45f1ecbd"></a>部分扩展会在后续 Vulkan 版本中提升为核心功能。

<a id="u0c5aa42b"></a>例如：

<a id="zaIbM"></a>
```latex
VK_KHR_dynamic_rendering
```

<a id="uca97e93f"></a>后来成为 Vulkan 1.3 核心功能。

<a id="LOC57"></a>

---

<a id="lrtm1"></a>
## 三、VkPhysicalDeviceFeatures2

<a id="u3aa5a89c"></a>旧版 Vulkan 使用：

<a id="Hstk0"></a>
```cpp
VkPhysicalDeviceFeatures
```

<a id="u6239e41f"></a>查询和开启设备功能。

<a id="u22058234"></a>随着功能越来越多，单个结构体无法容纳所有新特性。

<a id="u5f8a28bf"></a>因此 Vulkan 引入：

<a id="arfcv"></a>
```cpp
VkPhysicalDeviceFeatures2
```

<a id="u04572006"></a>其核心作用是：

<a id="Qqn8m"></a>
```latex
通过 pNext 链连接其他 Feature 结构体
```

<a id="u2d64b1df"></a>例如：

<a id="FBBJl"></a>
```cpp
VkPhysicalDeviceFeatures2 features2{};
features2.sType =
    VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_FEATURES_2;
```

<a id="udc913a73"></a>然后通过 `pNext` 连接 Vulkan 1.1、1.2 和 1.3 Feature：

<a id="e2xqw"></a>
```cpp
VkPhysicalDeviceVulkan11Features features11{};
VkPhysicalDeviceVulkan12Features features12{};
VkPhysicalDeviceVulkan13Features features13{};
```

<a id="u4f142079"></a>连接关系可以写成：

<a id="KlAiR"></a>
```latex
VkPhysicalDeviceFeatures2
→ VkPhysicalDeviceVulkan11Features
→ VkPhysicalDeviceVulkan12Features
→ VkPhysicalDeviceVulkan13Features
```

<a id="u47858a24"></a>例如：

<a id="Vrwv4"></a>
```cpp
features2.pNext = &features11;
features11.pNext = &features12;
features12.pNext = &features13;
features13.pNext = nullptr;
```

<a id="u97aa0511"></a>最后调用：

<a id="mtt5m"></a>
```cpp
vkGetPhysicalDeviceFeatures2(
    physicalDevice,
    &features2
);
```

<a id="ue515353e"></a>设备会将支持情况写入每个结构体。

<a id="QKiVK"></a>

---

<a id="PaBPL"></a>
## 四、pNext 链

<a id="u30466e45"></a>`pNext` 是 Vulkan 中极其重要的扩展机制。

<a id="u880a3f19"></a>大量 Vulkan 结构体都包含：

<a id="eQqmP"></a>
```cpp
const void* pNext;
```

<a id="u86f25fe4"></a>或者：

<a id="z5wqM"></a>
```cpp
void* pNext;
```

<a id="ufa30c1cd"></a>`pNext` 用于<strong>在不修改原有结构体定义的情况下，为 API 添加新功能</strong>。

<a id="u555689ab"></a>可以理解为：

<a id="FC6Q0"></a>
```latex
基础结构体
→ 扩展结构体 A
→ 扩展结构体 B
→ 扩展结构体 C
```

<a id="u12e852e4"></a>每个结构体通常包含：

<a id="eyKAF"></a>
```cpp
sType
pNext
```

<a id="uf687d7c0"></a>其中：

- <a id="u1710014c"></a>`sType` 表示当前结构体的真实类型
- <a id="u82b5cfa2"></a>`pNext` 指向链中的下一个结构体

<a id="Oh1M6"></a>

---

<a id="KPtf6"></a>
### 1. pNext 链示例

<a id="u2e8541ac"></a>例如查询动态渲染支持：

<a id="NbWsE"></a>
```cpp
VkPhysicalDeviceDynamicRenderingFeatures dynamicRenderingFeatures{};
dynamicRenderingFeatures.sType =
    VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_DYNAMIC_RENDERING_FEATURES;
```

<a id="u07264568"></a>然后连接到：

<a id="t6K7p"></a>
```cpp
VkPhysicalDeviceFeatures2 features2{};
features2.sType =
    VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_FEATURES_2;
features2.pNext = &dynamicRenderingFeatures;
```

<a id="ueef227a1"></a>最后：

<a id="EYaVt"></a>
```cpp
vkGetPhysicalDeviceFeatures2(
    physicalDevice,
    &features2
);
```

<a id="u1640fe39"></a>查询完成后：

<a id="IjIB2"></a>
```cpp
dynamicRenderingFeatures.dynamicRendering
```

<a id="u01b3ef4d"></a>会表示设备是否支持动态渲染。

<a id="kRiM5"></a>

---

<a id="kibx3"></a>
### 2. 为什么需要 pNext

<a id="ueba46d71"></a>如果没有 `pNext`，每增加一个 Vulkan 新功能，都可能需要修改原有结构体。

<a id="ubdd281b1"></a>这样会破坏：

- <a id="ueb4d5d62"></a>API 兼容性
- <a id="u2f4f84be"></a>二进制兼容性
- <a id="u16efdd5e"></a>旧代码
- <a id="u0ac4d3e3"></a>旧驱动

<a id="uc0b16005"></a>通过 `pNext`，Vulkan 可以保持旧结构体不变，同时不断加入新功能。

<a id="uc343de3d"></a>因此：

<a id="eABhN"></a>
```latex
pNext 是 Vulkan 的结构体扩展机制
```

<a id="ue0ee140f"></a>以后学习以下功能时都会频繁使用：

- <a id="u4ed3cf4a"></a>Dynamic Rendering
- <a id="ud0c1f97f"></a>Synchronization2
- <a id="u5cf66b04"></a>Descriptor Indexing
- <a id="uaab00aea"></a>Buffer Device Address
- <a id="u02f0391d"></a>Ray Tracing
- <a id="uc86d6ee5"></a>Mesh Shader
- <a id="ucfd6dcf0"></a>Timeline Semaphore

<a id="GnLcQ"></a>

---

<a id="UfFoB"></a>
### 3. pNext 链注意事项

<a id="u214f71b5"></a>构建 `pNext` 链时需要注意：

1. <a id="ue212f21e"></a>每个结构体必须填写正确的 `sType`
2. <a id="u224159f4"></a>最后一个结构体的 `pNext` 必须为 `nullptr`
3. <a id="ufb6b7af1"></a>结构体生命周期必须覆盖 API 调用过程
4. <a id="u8d73c99d"></a>不要将同一个结构体重复加入链
5. <a id="u544541de"></a>不要错误地形成循环链表
6. <a id="u20f79894"></a>不要使用已经离开作用域的局部变量
7. <a id="u43a37604"></a>查询结构和启用结构不能随意混用
8. <a id="u81ce6297"></a>同一类结构通常不应重复出现

<a id="u3fbef557"></a>例如，以下结构体不能在调用前被销毁：

<a id="t70Qa"></a>
```cpp
VkPhysicalDeviceFeatures2 features2;
VkPhysicalDeviceDynamicRenderingFeatures dynamicRenderingFeatures;
```

<a id="ub423e3c7"></a>因为 `features2.pNext` 指向后者。

<a id="huMIj"></a>

---

<a id="wRYkc"></a>
## 五、查询与启用的区别

<a id="u2dae7f56"></a>Vulkan 中必须区分：

<a id="yHn5t"></a>
```latex
查询功能支持
创建设备时启用功能
```

<a id="u31a97645"></a>查询过程通常使用：

<a id="Suz1K"></a>
```cpp
vkGetPhysicalDeviceFeatures2(...)
```

<a id="uf95fc6c0"></a>创建逻辑设备时则将需要开启的结构体连接到：

<a id="nolPl"></a>
```cpp
VkDeviceCreateInfo::pNext
```

<a id="uc1bf0475"></a>例如：

<a id="VzVq6"></a>
```cpp
VkPhysicalDeviceDynamicRenderingFeatures dynamicRenderingFeatures{};
dynamicRenderingFeatures.sType =
    VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_DYNAMIC_RENDERING_FEATURES;
dynamicRenderingFeatures.dynamicRendering = VK_TRUE;
```

<a id="ue4b976e6"></a>然后：

<a id="oQESI"></a>
```cpp
VkDeviceCreateInfo deviceCreateInfo{};
deviceCreateInfo.sType =
    VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
deviceCreateInfo.pNext =
    &dynamicRenderingFeatures;
```

<a id="ua56db5da"></a>需要遵守：

<a id="i1mgO"></a>
```latex
先查询
→ 确认支持
→ 再设置为 VK_TRUE
→ 创建逻辑设备
```

<a id="u177debbc"></a>不能在设备不支持时强行开启。

<a id="bL1R9"></a>

---

<a id="Pelpb"></a>
### 1. 支持但未启用

<a id="ufdaa132a"></a>例如设备返回：

<a id="rF5Gl"></a>
```cpp
dynamicRendering = VK_TRUE;
```

<a id="ub3262140"></a>只表示设备支持动态渲染。

<a id="ua8dd83ef"></a>如果创建逻辑设备时没有将：

<a id="Py86l"></a>
```cpp
dynamicRendering = VK_TRUE;
```

<a id="ud33f4789"></a>加入启用链，那么逻辑设备仍然不能合法使用该功能。

<a id="u7f0d3635"></a>因此：

<a id="yBcXG"></a>
```latex
Supported Feature
≠ Enabled Feature
```

<a id="a2T33"></a>

---

<a id="lTHKE"></a>
## 六、VkPhysicalDeviceProperties2

<a id="u739b5d57"></a>新版属性查询使用：

<a id="biC3A"></a>
```cpp
VkPhysicalDeviceProperties2
```

<a id="u2aa4c151"></a>与 `VkPhysicalDeviceFeatures2` 类似，它也可以通过 `pNext` 连接更多属性结构体。

<a id="u931de84e"></a>例如：

<a id="ktOPK"></a>
```cpp
VkPhysicalDeviceProperties2 properties2{};
properties2.sType =
    VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_PROPERTIES_2;
```

<a id="u6c6205f3"></a>然后调用：

<a id="Bz4Zx"></a>
```cpp
vkGetPhysicalDeviceProperties2(
    physicalDevice,
    &properties2
);
```

<a id="udb164279"></a>基础属性位于：

<a id="cxujj"></a>
```cpp
properties2.properties
```

<a id="u63223995"></a>其中包括：

- <a id="u3e075e4b"></a>GPU 名称
- <a id="u67587ca2"></a>GPU 类型
- <a id="uca603534"></a>API 版本
- <a id="u34b2a5bc"></a>驱动版本
- <a id="ucb9d5ead"></a>Vendor ID
- <a id="u5e187114"></a>Device ID
- <a id="u8b61c72f"></a>设备限制

<a id="u513056ba"></a>例如：

<a id="U7crw"></a>
```cpp
properties2.properties.deviceName
properties2.properties.apiVersion
properties2.properties.deviceType
properties2.properties.limits
```

<a id="RYpPJ"></a>

---

<a id="xiAl7"></a>
### 1. Features2 与 Properties2 的区别

<a id="yosuu"></a>
```latex
Features2
用于查询功能是否受到支持

Properties2
用于查询设备属性和具体限制
```

<a id="u0235f0d5"></a>例如：

<a id="cKgoI"></a>
```latex
samplerAnisotropy
属于 Feature

maxSamplerAnisotropy
属于 Property
```

<a id="u7fc5585a"></a>使用各向异性过滤时，需要同时检查：

<a id="K2XCk"></a>
```latex
Feature：是否支持各向异性过滤
Property：最大允许使用多大的各向异性倍率
```

<a id="TKgMr"></a>

---

<a id="AC5Sg"></a>
## 七、VkPhysicalDeviceMemoryProperties2

<a id="u95770911"></a>新版内存属性查询使用：

<a id="AfuG8"></a>
```cpp
VkPhysicalDeviceMemoryProperties2
```

<a id="u94e5559f"></a>例如：

<a id="XlHvZ"></a>
```cpp
VkPhysicalDeviceMemoryProperties2 memoryProperties2{};
memoryProperties2.sType =
    VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_MEMORY_PROPERTIES_2;
```

<a id="ue5158932"></a>然后调用：

<a id="AqxJ9"></a>
```cpp
vkGetPhysicalDeviceMemoryProperties2(
    physicalDevice,
    &memoryProperties2
);
```

<a id="u0e2bc096"></a>实际内存属性位于：

<a id="jducN"></a>
```cpp
memoryProperties2.memoryProperties
```

<a id="ub8d97394"></a>其中包含：

- <a id="ud20d8b3e"></a>Memory Type
- <a id="u4c182323"></a>Memory Heap
- <a id="u5db1a0ad"></a>Memory Property Flags
- <a id="uaf4ae37c"></a>Heap Size

<a id="u7a4ab077"></a>它与旧版：

<a id="xYrJq"></a>
```cpp
vkGetPhysicalDeviceMemoryProperties(...)
```

<a id="uc6c1ae93"></a>的核心功能相同，但可以通过 `pNext` 查询更多扩展内存信息。

<a id="vF6pb"></a>

---

<a id="h93mf"></a>
## 八、Ch6-1 无图像帧缓冲

<a id="u5a9a3513"></a>传统 Vulkan Framebuffer 在创建时，必须直接指定具体的 Image View。

<a id="u42c0c848"></a>例如：

<a id="KsjUm"></a>
```latex
Framebuffer 0
→ Swapchain Image View 0

Framebuffer 1
→ Swapchain Image View 1

Framebuffer 2
→ Swapchain Image View 2
```

<a id="u1a6dd96a"></a>交换链有几张图像，通常就需要创建几个 Framebuffer。

<a id="Mmmqd"></a>

---

<a id="vqmed"></a>
### 1. 传统 Framebuffer

<a id="u6638dfa5"></a>创建普通 Framebuffer 时，需要提供：

<a id="GqtpT"></a>
```cpp
VkFramebufferCreateInfo
```

<a id="u82961a36"></a>其中：

<a id="lMftt"></a>
```cpp
pAttachments
```

<a id="ub278189f"></a>直接指向具体的 Image View。

<a id="u301aa229"></a>例如：

<a id="qp9vX"></a>
```cpp
framebufferCreateInfo.attachmentCount = 1;
framebufferCreateInfo.pAttachments =
    &swapchainImageView;
```

<a id="ub52e0fc4"></a>因此 Framebuffer 与具体 Image View 绑定。

<a id="W9lWl"></a>

---

<a id="LXjbD"></a>
### 2. Imageless Framebuffer

<a id="uc3fdb90f"></a>无图像帧缓冲的英文名称为：

<a id="M0Q83"></a>
```latex
Imageless Framebuffer
```

<a id="uf64d0e4b"></a>它并不是完全没有图像。

<a id="u77bad73f"></a>它只是：

<a id="O1WEK"></a>
```latex
创建 Framebuffer 时
不立即绑定具体 Image View
```

<a id="ue5170471"></a>创建时只描述附件必须满足的条件：

- <a id="u88a969fc"></a>格式
- <a id="u51e7d2a0"></a>Usage
- <a id="u37761293"></a>宽度
- <a id="u5cf55104"></a>高度
- <a id="uc8b6c071"></a>图层数
- <a id="ue2b2c7f7"></a>View Format

<a id="ue050d20d"></a>真正开始 Render Pass 时，再提供当前实际使用的 Image View。

<a id="MzykD"></a>

---

<a id="Enmv4"></a>
### 3. 启用 Imageless Framebuffer

<a id="u553b4c3b"></a>首先需要查询并开启：

<a id="FylMN"></a>
```cpp
imagelessFramebuffer
```

<a id="u99fec384"></a>对应结构体通常为：

<a id="c2YAb"></a>
```cpp
VkPhysicalDeviceImagelessFramebufferFeatures
```

<a id="u9ea45cd8"></a>例如：

<a id="RW0Cp"></a>
```cpp
VkPhysicalDeviceImagelessFramebufferFeatures imagelessFeatures{};
imagelessFeatures.sType =
    VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_IMAGELESS_FRAMEBUFFER_FEATURES;
```

<a id="u27ec072b"></a>查询支持后，在创建逻辑设备时设置：

<a id="EudHv"></a>
```cpp
imagelessFeatures.imagelessFramebuffer = VK_TRUE;
```

<a id="Khqzw"></a>

---

<a id="L0nI5"></a>
### 4. 创建无图像 Framebuffer

<a id="ue4458ac5"></a>创建 Framebuffer 时，需要设置：

<a id="h9dqX"></a>
```cpp
VK_FRAMEBUFFER_CREATE_IMAGELESS_BIT
```

<a id="u5864d961"></a>例如：

<a id="fgxPq"></a>
```cpp
VkFramebufferCreateInfo framebufferCreateInfo{};
framebufferCreateInfo.sType =
    VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO;
framebufferCreateInfo.flags =
    VK_FRAMEBUFFER_CREATE_IMAGELESS_BIT;
```

<a id="u0d035193"></a>然后通过：

<a id="P1QTY"></a>
```cpp
VkFramebufferAttachmentsCreateInfo
```

<a id="u2abc87f3"></a>描述所有附件。

<a id="u94d3a62c"></a>每个附件使用：

<a id="D5dSl"></a>
```cpp
VkFramebufferAttachmentImageInfo
```

<a id="u7fa6ebe0"></a>描述。

<a id="u92b9f695"></a>其中包含：

- <a id="uc6216f50"></a>Image Usage
- <a id="u4591b06a"></a>Width
- <a id="ub2f66e8c"></a>Height
- <a id="ufcacd0f6"></a>Layer Count
- <a id="u58638bd2"></a>View Format

<a id="u95feffa3"></a>例如：

<a id="cqazN"></a>
```latex
这个附件必须是颜色附件
格式必须与交换链格式一致
尺寸必须与交换链尺寸一致
图层数为 1
```

<a id="Zy7be"></a>

---

<a id="mZSjc"></a>
### 5. 开始 Render Pass 时提供 Image View

<a id="u1b082eef"></a>开始 Render Pass 时，通过：

<a id="RJBlN"></a>
```cpp
VkRenderPassAttachmentBeginInfo
```

<a id="u963afc99"></a>提供实际使用的 Image View。

<a id="uc944808f"></a>然后将其连接到：

<a id="kMIDP"></a>
```cpp
VkRenderPassBeginInfo::pNext
```

<a id="u8c461cb8"></a>整体流程为：

<a id="CdeF0"></a>
```latex
创建 Framebuffer
→ 只描述附件要求
→ 不绑定具体 Image View

开始 Render Pass
→ 提供当前交换链 Image View
→ 使用同一个 Framebuffer
```

<a id="u00c34746"></a>因此多个交换链图像理论上可以共用同一个 Imageless Framebuffer。

<a id="vQBYW"></a>

---

<a id="fb4nO"></a>
### 6. Imageless Framebuffer 优点

<a id="u248e4e53"></a>优点：

- <a id="ue95ef367"></a>减少 Framebuffer 对象数量
- <a id="ucec63bd5"></a>Framebuffer 不再固定绑定某个 Image View
- <a id="uaaddd218"></a>可以延迟决定实际附件
- <a id="u76bdd0fa"></a>某些场景下资源组织更灵活

<a id="E0XLT"></a>

---

<a id="Glk0q"></a>
### 7. Imageless Framebuffer 缺点

<a id="u187ad644"></a>缺点：

- <a id="ube5bf42e"></a>配置更加复杂
- <a id="ua87975a7"></a>仍然需要 Render Pass
- <a id="u58a70b76"></a>仍然需要 Framebuffer 对象
- <a id="ue2f11752"></a>对现代渲染架构帮助有限
- <a id="uec001143"></a>很多情况下节省的对象数量并不重要
- <a id="u933f486d"></a>后续 Dynamic Rendering 使用更直接

<a id="u65ccbb44"></a>可以简单理解为：

<a id="ZBrAo"></a>
```latex
Imageless Framebuffer
只是让 Framebuffer 不再固定绑定 Image View

Dynamic Rendering
则直接取消了 Framebuffer 和 Render Pass 对象
```

<a id="u80edfc98"></a>因此 Ch6-1 更适合作为：

<a id="Hl5P1"></a>
```latex
学习新特性启用和 pNext 链的练习
```

<a id="u16fc60f5"></a>而不是后续渲染架构的重点。

<a id="obMz1"></a>

---

<a id="YgRKs"></a>
## 九、Ch6-2 动态渲染

<a id="u478e86f6"></a>动态渲染是第六章最重要的内容

<a id="ub1462f1c"></a>传统 Vulkan 绘制前需要创建：

<a id="qAwOa"></a>
```latex
VkRenderPass
VkFramebuffer
```

<a id="u0e7c95e3"></a>录制命令时使用：

<a id="VWmm2"></a>
```cpp
vkCmdBeginRenderPass(...)
vkCmdEndRenderPass(...)
```

<a id="u05923d11"></a>动态渲染改为：

<a id="ouu8a"></a>
```cpp
vkCmdBeginRendering(...)
vkCmdEndRendering(...)
```

<a id="u51d88141"></a><strong>不再需要传统的 Render Pass 和 Framebuffer 对象</strong>。

<a id="bCEuO"></a>

---

<a id="GhXRl"></a>
## 十、传统 Render Pass 渲染流程

<a id="udcf7f405"></a>传统渲染流程通常为：

<a id="vYXcb"></a>
```latex
创建 Render Pass
→ 创建 Framebuffer
→ 创建 Graphics Pipeline
→ Begin Render Pass
→ Bind Pipeline
→ Draw
→ End Render Pass
```

<a id="u0f52a49f"></a>Render Pass 中提前定义：

- <a id="u1bff2669"></a>颜色附件
- <a id="uac4f2e34"></a>深度附件
- <a id="u7c473c27"></a>模板附件
- <a id="uc2754363"></a>Load Operation
- <a id="u488cea2b"></a>Store Operation
- <a id="u735322d5"></a>初始布局
- <a id="u1fd58b78"></a>最终布局
- <a id="ub1f318b6"></a>Subpass
- <a id="uf64c065a"></a>Subpass Dependency

<a id="u13431671"></a>Framebuffer 则负责绑定具体的 Image View。

<a id="O3HJc"></a>

---

<a id="CuxaK"></a>
## 十一、动态渲染流程

<a id="u830fc4be"></a>动态渲染流程为：

<a id="k8yeL"></a>
```latex
创建 Graphics Pipeline
→ 指定附件格式
→ 准备 Rendering Attachment
→ Begin Rendering
→ Bind Pipeline
→ Draw
→ End Rendering
```

<a id="ud3ef2327"></a>主要使用三个结构体：

<a id="TzKjO"></a>
```cpp
VkPipelineRenderingCreateInfo
VkRenderingAttachmentInfo
VkRenderingInfo
```

<a id="AzipE"></a>

---

<a id="i9xgv"></a>
## 十二、VkPipelineRenderingCreateInfo

<a id="u971dd408"></a>使用动态渲染时，创建 Graphics Pipeline 不再提供传统 Render Pass。

<a id="ude9a1d06"></a>传统方式：

<a id="cu6EV"></a>
```cpp
graphicsPipelineCreateInfo.renderPass = renderPass;
```

<a id="u0b4290b3"></a>动态渲染中：

<a id="X5mYW"></a>
```cpp
graphicsPipelineCreateInfo.renderPass = VK_NULL_HANDLE;
```

<a id="u8a589cc4"></a>但是 Graphics Pipeline 仍然需要知道附件格式。

<a id="u47a45ae6"></a>因此使用：

<a id="weqxv"></a>
```cpp
VkPipelineRenderingCreateInfo
```

<a id="u5eada0b6"></a>例如：

<a id="KElwo"></a>
```cpp
VkPipelineRenderingCreateInfo pipelineRenderingInfo{};
pipelineRenderingInfo.sType =
    VK_STRUCTURE_TYPE_PIPELINE_RENDERING_CREATE_INFO;
pipelineRenderingInfo.colorAttachmentCount = 1;
pipelineRenderingInfo.pColorAttachmentFormats =
    &swapchainFormat;
```

<a id="u33526beb"></a>然后连接到：

<a id="AyTcz"></a>
```cpp
VkGraphicsPipelineCreateInfo::pNext
```

<a id="ubda52643"></a>整体关系为：

<a id="MhTUl"></a>
```latex
VkGraphicsPipelineCreateInfo
→ pNext
→ VkPipelineRenderingCreateInfo
```

<a id="u9a70d712"></a>如果存在深度附件，还需要填写：

<a id="TDdhk"></a>
```cpp
depthAttachmentFormat
```

<a id="ue5cf15e5"></a>如果存在模板附件，还需要填写：

<a id="wwuhI"></a>
```cpp
stencilAttachmentFormat
```

<a id="kIWdq"></a>

---

<a id="atOgo"></a>
## 十三、VkRenderingAttachmentInfo

<a id="u5c3e71d1"></a>每一个实际渲染附件通过：

<a id="hzgRL"></a>
```cpp
VkRenderingAttachmentInfo
```

<a id="uc9d53312"></a>描述。

<a id="u6a1044a7"></a>颜色附件通常包括：

- <a id="u9d4fe6d4"></a>Image View
- <a id="uba8c8c96"></a>Image Layout
- <a id="uaf565131"></a>Load Operation
- <a id="ucec1d5a3"></a>Store Operation
- <a id="uf48f0f87"></a>Clear Value
- <a id="u0660a264"></a>Resolve 相关信息

<a id="u34c6c801"></a>例如：

<a id="aKJFw"></a>
```cpp
VkRenderingAttachmentInfo colorAttachment{};
colorAttachment.sType =
    VK_STRUCTURE_TYPE_RENDERING_ATTACHMENT_INFO;
colorAttachment.imageView =
    swapchainImageViews[imageIndex];
colorAttachment.imageLayout =
    VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;
colorAttachment.loadOp =
    VK_ATTACHMENT_LOAD_OP_CLEAR;
colorAttachment.storeOp =
    VK_ATTACHMENT_STORE_OP_STORE;
```

<a id="BhCga"></a>

---

<a id="fmX85"></a>
### 1. Load Operation

<a id="uf44d4603"></a>Load Operation 决定渲染开始时如何处理附件原有内容。

<a id="u820ec656"></a>常见值：

<a id="l66zZ"></a>
```cpp
VK_ATTACHMENT_LOAD_OP_LOAD
VK_ATTACHMENT_LOAD_OP_CLEAR
VK_ATTACHMENT_LOAD_OP_DONT_CARE
```

<a id="uc0ca7fa4"></a>含义：

<a id="aR1UR"></a>
```latex
LOAD
保留并读取原有内容

CLEAR
使用 Clear Value 清空

DONT_CARE
不关心之前的内容
```

<a id="LPSfF"></a>

---

<a id="CUJon"></a>
### 2. Store Operation

<a id="u78203469"></a>Store Operation 决定渲染结束后是否保存结果。

<a id="u8ffbb74c"></a>常见值：

<a id="YbVQM"></a>
```cpp
VK_ATTACHMENT_STORE_OP_STORE
VK_ATTACHMENT_STORE_OP_DONT_CARE
```

<a id="uc3f09a82"></a>如果最终图像需要显示或继续使用，通常需要：

<a id="lEOYi"></a>
```cpp
VK_ATTACHMENT_STORE_OP_STORE
```

<a id="iJxJD"></a>

---

<a id="NylbY"></a>
## 十四、VkRenderingInfo

<a id="uec2d6a0d"></a>整个动态渲染过程通过：

<a id="BXWlI"></a>
```cpp
VkRenderingInfo
```

<a id="u6f86d776"></a>描述。

<a id="ua6644276"></a>主要包含：

- <a id="u9bcb7b1e"></a>Render Area
- <a id="u50444f06"></a>Layer Count
- <a id="u3eee2759"></a>View Mask
- <a id="u4aa0dd1d"></a>Color Attachment
- <a id="ubb8955ac"></a>Depth Attachment
- <a id="ufa7e15b3"></a>Stencil Attachment

<a id="ub78db5b3"></a>例如：

<a id="swWwI"></a>
```cpp
VkRenderingInfo renderingInfo{};
renderingInfo.sType =
    VK_STRUCTURE_TYPE_RENDERING_INFO;
renderingInfo.renderArea.offset = {0, 0};
renderingInfo.renderArea.extent = swapchainExtent;
renderingInfo.layerCount = 1;
renderingInfo.colorAttachmentCount = 1;
renderingInfo.pColorAttachments =
    &colorAttachment;
```

<a id="ud2055237"></a>开始渲染：

<a id="H2v36"></a>
```cpp
vkCmdBeginRendering(
    commandBuffer,
    &renderingInfo
);
```

<a id="u9f733513"></a>结束渲染：

<a id="ZQLRP"></a>
```cpp
vkCmdEndRendering(commandBuffer);
```

<a id="Ja0uJ"></a>

---

<a id="LFeei"></a>
## 十五、启用动态渲染

<a id="u40ef47bc"></a>动态渲染在 Vulkan 1.3 中成为核心功能。

<a id="ua25c390c"></a>如果使用 Vulkan 1.3，可以通过：

<a id="FOiNG"></a>
```cpp
VkPhysicalDeviceVulkan13Features
```

<a id="u294d87a4"></a>启用。

<a id="u304d1a5c"></a>例如：

<a id="IbFOy"></a>
```cpp
VkPhysicalDeviceVulkan13Features features13{};
features13.sType =
    VK_STRUCTURE_TYPE_PHYSICAL_DEVICE_VULKAN_1_3_FEATURES;
features13.dynamicRendering = VK_TRUE;
```

<a id="u4149bb57"></a>较低版本 Vulkan 中，可以通过：

<a id="i8RFE"></a>
```latex
VK_KHR_dynamic_rendering
```

<a id="u0ce31b95"></a>扩展使用。

<a id="udeddfa7e"></a>此时需要：

- <a id="u60be82f2"></a>检查扩展是否支持
- <a id="u0e16e928"></a>启用扩展
- <a id="u89379719"></a>查询动态渲染 Feature
- <a id="uc7c0b2df"></a>开启动态渲染
- <a id="u7619cb98"></a>获取对应函数入口

<a id="wDsNs"></a>

---

<a id="pl6wC"></a>
## 十六、核心函数与扩展函数

<a id="u6c5c4341"></a>在 Vulkan 1.3 中，核心函数名称为：

<a id="y8krI"></a>
```cpp
vkCmdBeginRendering
vkCmdEndRendering
```

<a id="ue77076de"></a>扩展版本可能为：

<a id="JRFrS"></a>
```cpp
vkCmdBeginRenderingKHR
vkCmdEndRenderingKHR
```

<a id="uc1606a84"></a>如果程序同时支持核心和扩展路径，需要明确选择。

<a id="u13357681"></a>不能在未确认函数可用时直接调用。

<a id="hPuxw"></a>

---

<a id="QfhLV"></a>
## 十七、动态渲染中的图像布局

<a id="u9c028a25"></a>传统 Render Pass 可以通过：

<a id="muYjW"></a>
```latex
initialLayout
finalLayout
Subpass Dependency
```

<a id="u3f9eb6e8"></a>隐式完成部分图像布局转换和同步。

<a id="ud91fa000"></a>动态渲染没有传统 Render Pass，因此这些工作需要程序自己完成。

<a id="u07a3e8f4"></a>渲染开始前，交换链图像通常需要转换为：

<a id="qHLsy"></a>
```cpp
VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL
```

<a id="ud1ed69d2"></a>渲染结束后，需要转换为：

<a id="eKADA"></a>
```cpp
VK_IMAGE_LAYOUT_PRESENT_SRC_KHR
```

<a id="u7f9f32de"></a>整体流程为：

<a id="tXFLZ"></a>
```latex
PRESENT_SRC_KHR
→ COLOR_ATTACHMENT_OPTIMAL
→ 动态渲染
→ PRESENT_SRC_KHR
```

<a id="bdUTI"></a>

---

<a id="ymLry"></a>
## 十八、动态渲染中的 Image Barrier

<a id="u6d214645"></a>布局转换通常需要使用：

<a id="Dxvfi"></a>
```cpp
VkImageMemoryBarrier
```

<a id="u82ad2d90"></a>或者 Synchronization2 中的：

<a id="vZlWW"></a>
```cpp
VkImageMemoryBarrier2
```

<a id="u2b628b78"></a>传统 Barrier 调用：

<a id="HHg2Q"></a>
```cpp
vkCmdPipelineBarrier(...)
```

<a id="uf166726d"></a>Synchronization2 调用：

<a id="JZUnD"></a>
```cpp
vkCmdPipelineBarrier2(...)
```

<a id="ub9c8f634"></a>Barrier 需要明确：

- <a id="udb81016d"></a>旧布局
- <a id="ua4094d0d"></a>新布局
- <a id="ue9d5c805"></a>源管线阶段
- <a id="u6256f6a7"></a>目标管线阶段
- <a id="u56c73951"></a>源访问权限
- <a id="u84cf2624"></a>目标访问权限
- <a id="ue2823574"></a>Image Subresource Range

<a id="yl35n"></a>

---

<a id="IbokB"></a>
### 1. 呈现到颜色附件

<a id="u276ff29a"></a>渲染开始前：

<a id="IB8iy"></a>
```latex
旧布局：
VK_IMAGE_LAYOUT_PRESENT_SRC_KHR

新布局：
VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL
```

<a id="u25d636ee"></a>目标访问通常需要包含：

<a id="W52Nd"></a>
```cpp
VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT
```

<a id="u6f6c9652"></a>目标阶段通常需要包含：

<a id="qTMpW"></a>
```cpp
VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT
```

<a id="wVeEF"></a>

---

<a id="bCc2G"></a>
### 2. 颜色附件到呈现

<a id="u7c85a82c"></a>渲染完成后：

<a id="qQYbp"></a>
```latex
旧布局：
VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL

新布局：
VK_IMAGE_LAYOUT_PRESENT_SRC_KHR
```

<a id="ufdc35327"></a>需要确保颜色附件写入完成后，图像才能交给呈现系统。

<a id="azK5A"></a>

---

<a id="mX82R"></a>
## 十九、Dynamic Viewport 和 Scissor

<a id="ue322a6b2"></a>交换链尺寸发生变化后，如果 Viewport 和 Scissor 被固定写入 Pipeline，可能需要重新创建 Graphics Pipeline。

<a id="u7897d125"></a>更灵活的方式是使用动态状态：

<a id="Av1Uy"></a>
```cpp
VK_DYNAMIC_STATE_VIEWPORT
VK_DYNAMIC_STATE_SCISSOR
```

<a id="ue9c969b2"></a>录制命令时调用：

<a id="b2vKu"></a>
```cpp
vkCmdSetViewport(...)
vkCmdSetScissor(...)
```

<a id="ue133495b"></a>这样窗口尺寸变化后，只需要更新命令中的 Viewport 和 Scissor。

<a id="u4466b65f"></a>不过附件格式发生变化时，仍可能需要重新创建 Pipeline。

<a id="ubbb0e1f3"></a>因为：

<a id="j48Of"></a>
```cpp
VkPipelineRenderingCreateInfo
```

<a id="u421f1bd4"></a>中记录了附件格式。

<a id="sP2nd"></a>

---

<a id="mmQ8M"></a>
## 二十、动态渲染与深度附件

<a id="ue878cbbc"></a>如果动态渲染使用深度缓冲，需要额外创建：

- <a id="ud66739ad"></a>Depth Image
- <a id="uf9cee5f5"></a>Depth Memory
- <a id="udee9b4be"></a>Depth Image View

<a id="u3d2b23df"></a>深度附件使用另一个：

<a id="LrTjY"></a>
```cpp
VkRenderingAttachmentInfo
```

<a id="u1c767cd6"></a>例如：

<a id="JbtHn"></a>
```cpp
VkRenderingAttachmentInfo depthAttachment{};
depthAttachment.sType =
    VK_STRUCTURE_TYPE_RENDERING_ATTACHMENT_INFO;
depthAttachment.imageView = depthImageView;
depthAttachment.imageLayout =
    VK_IMAGE_LAYOUT_DEPTH_ATTACHMENT_OPTIMAL;
depthAttachment.loadOp =
    VK_ATTACHMENT_LOAD_OP_CLEAR;
depthAttachment.storeOp =
    VK_ATTACHMENT_STORE_OP_DONT_CARE;
```

<a id="u283351a0"></a>然后：

<a id="sbfJ5"></a>
```cpp
renderingInfo.pDepthAttachment =
    &depthAttachment;
```

<a id="u4dfce107"></a>Pipeline 创建时也必须填写正确的：

<a id="BQrmS"></a>
```cpp
depthAttachmentFormat
```

<a id="px2MP"></a>

---

<a id="Tfxnq"></a>
## 二十一、Render Pass 与 Dynamic Rendering 的区别

<a id="si9Fn"></a>
### 1. 传统 Render Pass

<a id="u98eee782"></a>需要：

<a id="BY7jE"></a>
```latex
VkRenderPass
VkFramebuffer
VkRenderPassBeginInfo
vkCmdBeginRenderPass
vkCmdEndRenderPass
```

<a id="ufa2af61e"></a><strong>优点</strong>：

- <a id="u00a8d5ae"></a>能够提前描述完整渲染流程
- <a id="uc65d2def"></a>适合复杂 Subpass
- <a id="u7275c830"></a>某些移动 GPU 可利用 Subpass 优化
- <a id="ued2ebe6a"></a>教程和参考代码丰富

<a id="ucc11005f"></a><strong>缺点</strong>：

- <a id="u295fbf2d"></a>对象较多
- <a id="u0dc23ecd"></a>配置复杂
- <a id="uef2cbb87"></a>与附件格式和 Framebuffer 绑定较紧
- <a id="ud2193e4c"></a>交换链重建时涉及资源较多

<a id="WWFUc"></a>

---

<a id="pGo8A"></a>
### 2. Imageless Framebuffer

<a id="u7ec2e457"></a>需要：

<a id="KN39u"></a>
```latex
VkRenderPass
VkFramebuffer
VkRenderPassAttachmentBeginInfo
vkCmdBeginRenderPass
vkCmdEndRenderPass
```

<a id="uf39e5837"></a>区别是：

<a id="caJge"></a>
```latex
Framebuffer 创建时不固定 Image View
```

<a id="ucf037a20"></a><strong>优点</strong>：

- <a id="u77c12d29"></a>一个 Framebuffer 可以适配多个 Image View
- <a id="ufeeca9fd"></a>附件绑定更灵活

<a id="u2f0bbf98"></a><strong>缺点</strong>：

- <a id="u990c9100"></a>仍然需要 Render Pass
- <a id="u8ac769fb"></a>仍然需要 Framebuffer
- <a id="u99bf2c26"></a>配置并没有明显简化
- <a id="u14b202a6"></a>实际收益有限

<a id="PgeQr"></a>

---

<a id="k6ohw"></a>
### 3. Dynamic Rendering

<a id="ub2cf0c01"></a>需要：

<a id="W5OlJ"></a>
```latex
VkPipelineRenderingCreateInfo
VkRenderingAttachmentInfo
VkRenderingInfo
vkCmdBeginRendering
vkCmdEndRendering
```

<a id="uf74c2c6a"></a>不需要：

<a id="Sig9Z"></a>
```latex
VkRenderPass
VkFramebuffer
```

<a id="u79209228"></a><strong>优点</strong>：

- <a id="uc92fd9b3"></a>对象更少
- <a id="u10b64c7e"></a>渲染流程更直接
- <a id="ubfbb2e3f"></a>附件可以在录制命令时指定
- <a id="u0cf32ce3"></a>适合现代渲染架构
- <a id="u48e1b302"></a>交换链重建更加简单
- <a id="u655e4a6b"></a>更适合模块化渲染 Pass

<a id="u6eed38ec"></a><strong>缺点</strong>：

- <a id="u4f68fad7"></a>需要自己处理布局转换
- <a id="u179729f8"></a>需要更明确地处理同步
- <a id="u5e9c509d"></a>复杂 Subpass 场景仍需考虑传统 Render Pass
- <a id="u4c1d2545"></a>必须确认设备版本和功能支持

<a id="P7oqO"></a>

---

<a id="uhXor"></a>
## 二十二、三种方式的整体对比

<a id="xCBPp"></a>
```latex
传统 Render Pass：

提前创建 Render Pass
提前创建 Framebuffer
Render Pass 隐式处理部分布局和依赖
适合传统固定渲染流程
```

<a id="iRgFY"></a>
```latex
Imageless Framebuffer：

保留 Render Pass
保留 Framebuffer
Framebuffer 不固定具体 Image View
实际开始渲染时再提供附件
```

<a id="nEQJv"></a>
```latex
Dynamic Rendering：

不创建 Render Pass
不创建 Framebuffer
开始渲染时直接指定附件
布局转换和同步由程序显式处理
```

<a id="u7c42b184"></a>可以概括为：

<a id="UeO07"></a>
```latex
Legacy Render Pass
= 固定渲染描述 + 固定附件

Imageless Framebuffer
= 固定渲染描述 + 延迟指定附件

Dynamic Rendering
= 渲染时动态指定附件和操作
```

<a id="QLX55"></a>

---

<a id="xK95r"></a>
## 二十三、交换链重建差异

<a id="n8oTN"></a>
### 1. 传统 Render Pass

<a id="uc5022356"></a>交换链重建时通常需要考虑：

- <a id="ue8d799db"></a>Swapchain
- <a id="u30360b38"></a>Swapchain Image View
- <a id="u8393ff60"></a>Framebuffer
- <a id="u9264b11d"></a>Render Pass
- <a id="u475a0a10"></a>Graphics Pipeline
- <a id="u782e707d"></a>Depth Buffer
- <a id="ua629f98b"></a>Command Buffer

<a id="ua5a75919"></a>如果交换链格式没有变化，Render Pass 和 Pipeline 有时可以保留。

<a id="lCtVg"></a>

---

<a id="vVQyL"></a>
### 2. Imageless Framebuffer

<a id="u935d410f"></a>仍然需要考虑：

- <a id="u4ceb50ce"></a>Swapchain
- <a id="u3a61f30b"></a>Swapchain Image View
- <a id="ua2352e2e"></a>Imageless Framebuffer 的尺寸和附件条件
- <a id="uc04d85ba"></a>Graphics Pipeline
- <a id="u4414ec99"></a>Command Buffer

<a id="uf705d732"></a>即使 Framebuffer 不绑定具体 Image View，它仍然记录：

- <a id="u789054bf"></a>Width
- <a id="ud2faea89"></a>Height
- <a id="u9db6c178"></a>Layer Count
- <a id="u390b72ac"></a>Attachment Requirements

<a id="uadece332"></a>因此尺寸变化时通常仍需要重新创建。

<a id="Z9f5w"></a>

---

<a id="c2qLm"></a>
### 3. Dynamic Rendering

<a id="u0b66e696"></a>不需要重建：

- <a id="u470dde2d"></a>Render Pass
- <a id="u9c3c5ed4"></a>Framebuffer

<a id="u17296f7d"></a>但仍需要处理：

- <a id="ua38b85ec"></a>Swapchain
- <a id="u59b4507b"></a>Swapchain Image View
- <a id="u8072ebda"></a>Viewport
- <a id="u7cff8db6"></a>Scissor
- <a id="u748adc6a"></a>Depth Image
- <a id="u67444b31"></a>屏幕尺寸相关附件
- <a id="u221bcdb5"></a>附件格式变化时的 Pipeline

<a id="ua790ab9c"></a>因此动态渲染只是减少了一部分对象，并不代表交换链重建完全消失。

<a id="qqzGP"></a>

---

<a id="Dp3i1"></a>
## 二十四、第六章常见问题

<a id="KvqF2"></a>
### 1. 只查询 Feature，但没有启用

<a id="uad2a5b0b"></a>错误理解：

<a id="dRC2u"></a>
```latex
设备支持 Dynamic Rendering
所以可以直接使用
```

<a id="u60d5ace9"></a>正确流程：

<a id="pDkIY"></a>
```latex
查询支持
→ 创建逻辑设备时启用
→ 再使用
```

<a id="B9lRU"></a>

---

<a id="xugVF"></a>
### 2. pNext 指向无效内存

<a id="u855cdc06"></a>例如：

<a id="IDvtD"></a>
```cpp
void Setup() {
    VkPhysicalDeviceDynamicRenderingFeatures features{};
    deviceCreateInfo.pNext = &features;
}
```

<a id="u9ef9fa22"></a>函数结束后，`features` 被销毁。

<a id="ufb220deb"></a>之后再使用：

<a id="RO2yw"></a>
```cpp
deviceCreateInfo
```

<a id="u917e12be"></a>就会产生悬空指针。

<a id="D5S5h"></a>

---

<a id="b9q4w"></a>
### 3. sType 填写错误

<a id="u0b8430df"></a>每个扩展结构体必须填写对应的：

<a id="ZSsRR"></a>
```cpp
sType
```

<a id="ub9350c13"></a>错误的 `sType` 会导致驱动无法正确识别结构体。

<a id="G3z4d"></a>

---

<a id="JREg3"></a>
### 4. 动态渲染 Pipeline 没有指定附件格式

<a id="ue6192712"></a>Dynamic Rendering 创建 Pipeline 时没有 Render Pass。

<a id="u9f5a7dbf"></a>因此必须通过：

<a id="r1WMl"></a>
```cpp
VkPipelineRenderingCreateInfo
```

<a id="u3d785914"></a>提供附件格式。

<a id="ua4833360"></a>否则 Pipeline 与实际附件不兼容。

<a id="Aln9H"></a>

---

<a id="Hbifp"></a>
### 5. 没有进行交换链图像布局转换

<a id="u41899c52"></a>动态渲染不会自动将交换链图像从呈现布局转换为颜色附件布局。

<a id="u2f8d9d93"></a>必须显式完成：

<a id="lakUZ"></a>
```latex
PRESENT_SRC_KHR
→ COLOR_ATTACHMENT_OPTIMAL
→ PRESENT_SRC_KHR
```

<a id="oTMMD"></a>

---

<a id="WSNHu"></a>
### 6. Image Layout 与实际用法不一致

<a id="u1b196b1e"></a>例如：

<a id="gioAo"></a>
```latex
RenderingAttachmentInfo 中声明：
COLOR_ATTACHMENT_OPTIMAL

但图像实际仍然是：
PRESENT_SRC_KHR
```

<a id="uc0214e3a"></a>这会触发 Validation Layer 错误。

<a id="yYN3n"></a>

---

<a id="UhWfH"></a>
### 7. 使用 vkDeviceWaitIdle 掩盖问题

<a id="u8cf68c7a"></a>在每帧调用：

<a id="RdW4v"></a>
```cpp
vkDeviceWaitIdle(...)
```

<a id="u9a3696ec"></a>虽然可能暂时避免资源竞争，但会严重降低并行能力。

<a id="ua5043399"></a>正确做法是使用：

- <a id="ub47f57dc"></a>Fence
- <a id="u5a242c10"></a>Semaphore
- <a id="u1ed49fc6"></a>Pipeline Barrier
- <a id="u573281fd"></a>正确的帧资源管理

<a id="h14mi"></a>

---

<a id="EsDlk"></a>
## 二十五、第六章整体关系

<a id="uead451a8"></a>第六章各节的关系为：

<a id="eRPCE"></a>
```latex
Ch6-0
查询和启用新版本特性
→ 学习 Feature、Property、Extension 和 pNext

Ch6-1
使用 Imageless Framebuffer
→ 练习新特性启用和扩展结构体

Ch6-2
使用 Dynamic Rendering
→ 移除传统 Render Pass 和 Framebuffer
→ 显式处理附件、布局和同步
```

<a id="u91d189a7"></a>Ch6-0 是基础。

<a id="ucf3a167b"></a>Ch6-1 和 Ch6-2 都依赖：

- <a id="ub2f94484"></a>版本查询
- <a id="u329b7d1d"></a>Feature 查询
- <a id="u2981321f"></a>pNext 链
- <a id="ub3e72054"></a>逻辑设备 Feature 启用

<a id="ulwwm"></a>

---

<a id="RN22F"></a>
## 二十六、第六章总结

<a id="u408a7cba"></a>第六章主要学习了 Vulkan 新版本功能的查询、启用和使用方法。

<a id="ue0b3090c"></a>首先通过 Ch6-0 学习：

<a id="C6c3y"></a>
```latex
Vulkan 版本查询
Feature 查询
Property 查询
Memory Property 查询
pNext 链
逻辑设备 Feature 启用
```

<a id="ueba04033"></a>然后通过 Ch6-1 学习：

<a id="n0qfP"></a>
```latex
Imageless Framebuffer
延迟指定 Image View
Framebuffer 扩展结构体
Render Pass Begin 扩展结构体
```

<a id="ud31648d0"></a>最后通过 Ch6-2 学习：

<a id="Gz97q"></a>
```latex
Dynamic Rendering
不再创建 Render Pass
不再创建 Framebuffer
渲染时动态指定附件
显式处理布局和同步
```

<a id="u01da11ec"></a>第六章最核心的数据关系可以概括为：

<a id="zzAe3"></a>
```latex
查询设备能力
→ 开启设备功能
→ 创建兼容 Pipeline
→ 准备渲染附件
→ 转换图像布局
→ Begin Rendering
→ Draw
→ End Rendering
→ 转换为呈现布局
```

<a id="ud52ba77e"></a>可以将第六章概括为：

> <a id="u1e34e8ef"></a>
>
> <a id="u38977d8d"></a>第六章解决了如何查询和开启现代 Vulkan 功能，并使用 Dynamic Rendering 替代传统 Render Pass 与 Framebuffer 完成绘制的问题。

原文：[EasyVulkan 第六章学习笔记](<https://www.yuque.com/u62694975/iaaa/douio0pyg8snnk8n>)
