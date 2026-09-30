---
title: "Vulkan Window Surface"
slug: "vulkan-window-surface"
summary: "整理 VkSurfaceKHR 的窗口系统职责、GLFW 创建流程，以及呈现队列检查和交换链之间的关系。"
categories: ["Vulkan"]
tags: ["Vulkan", "Window System", "Surface", "Swapchain", "GLFW"]
date: "2026-06-07T12:48:57.000Z"
lastmod: "2026-06-12T01:59:11.000Z"
draft: false
yuque_slug: "eeg2ouxti0x7ocyb"
source: "https://www.yuque.com/u62694975/iaaa/eeg2ouxti0x7ocyb"
---

<a id="u0fe2825b"></a><span style="color: rgb(31, 31, 31)">在 Vulkan 中，</span><strong><span style="color: rgb(31, 31, 31)">Window Surface（窗口表面，通常对应句柄 </span></strong>`VkSurfaceKHR`<strong><span style="color: rgb(31, 31, 31)">）</span></strong><span style="color: rgb(31, 31, 31)"> 是一个连接 </span><strong><span style="color: rgb(31, 31, 31)">Vulkan 图形管道</span></strong><span style="color: rgb(31, 31, 31)"> 与 </span><strong><span style="color: rgb(31, 31, 31)">操作系统的窗口系统（OS Window System）</span></strong><span style="color: rgb(31, 31, 31)"> 的</span><strong><span style="color: rgb(31, 31, 31)">跨平台抽象层桥梁</span></strong><span style="color: rgb(31, 31, 31)">。</span>

<a id="u31333fcd"></a><span style="color: rgb(31, 31, 31)">简单来说：Vulkan 本身是一个极其纯粹的硬件渲染 API，它甚至不知道屏幕、窗口、或者“显示”是什么。它只负责在显存里往一片内存（Image）里涂颜色。</span>

<a id="uf6fc55db"></a><span style="color: rgb(31, 31, 31)">而 </span><strong><span style="color: rgb(31, 31, 31)">Window Surface</span></strong><span style="color: rgb(31, 31, 31)"> 就是我们向操作系统申请的一块“画布”，有了它，Vulkan 才知道应该把显存里画好的图像投递到屏幕的哪个具体窗口上。</span>

<a id="ade89f3e"></a>
### <span style="color: rgb(31, 31, 31)">1. 为什么不能直接画在窗口上？（核心痛点）</span>

<a id="u1bde5005"></a><span style="color: rgb(31, 31, 31)">在老旧图形 API 比如 OpenGL 中，API 会隐式地处理与操作系统的对接。但 Vulkan 为了追求绝对的平台无关性，把底牌彻底掀开了：</span>

- <a id="ubad1164f"></a><strong><span style="color: rgb(31, 31, 31)">Vulkan 的世界：</span></strong><span style="color: rgb(31, 31, 31)"> 只有物理设备、逻辑设备、命令缓冲区、渲染管线、显存。</span>
- <a id="u0dbf9ade"></a><strong><span style="color: rgb(31, 31, 31)">操作系统的世界：</span></strong><span style="color: rgb(31, 31, 31)"> Windows 认的是 </span>`HWND`<span style="color: rgb(31, 31, 31)">（窗口句柄）和 </span>`HDC`<span style="color: rgb(31, 31, 31)">；Linux 认的是 </span>`Window`<span style="color: rgb(31, 31, 31)"> 变体（X11 或 Wayland）；macOS 认的是 </span>`CAMetalLayer`<span style="color: rgb(31, 31, 31)">。</span>

<a id="u95cb71e3"></a><span style="color: rgb(31, 31, 31)">这两者由于设计哲学完全不同，根本无法直接对话。</span>

<a id="ua53558e0"></a>`VkSurfaceKHR`<strong><span style="color: rgb(31, 31, 31)"> 就是那个连接两者的中间人。</span></strong><span style="color: rgb(31, 31, 31)"> 它把操作系统的原生窗口句柄（比如 Windows 的 </span>`HWND`<span style="color: rgb(31, 31, 31)">）包装起来，变成一个通用的、Vulkan 认识的对象。</span>

<a id="6f00ef9a"></a>
### <span style="color: rgb(31, 31, 31)">2. 名字后面的 </span>`KHR`<span style="color: rgb(31, 31, 31)"> 代表什么？</span>

<a id="uf5a23a8e"></a><span style="color: rgb(31, 31, 31)">如果仔细观察，会发现核心的 Vulkan 对象（如 </span>`VkDevice`<span style="color: rgb(31, 31, 31)">、</span>`VkImage`<span style="color: rgb(31, 31, 31)">）后面都没有后缀，而 </span>`VkSurfaceKHR`<span style="color: rgb(31, 31, 31)"> 后面跟着 </span>`KHR`<span style="color: rgb(31, 31, 31)">。</span>

<a id="u1f707a49"></a><span style="color: rgb(31, 31, 31)">其中，</span>`KHR`<span style="color: rgb(31, 31, 31)"> 代表 </span><strong><span style="color: rgb(31, 31, 31)">Khronos 官方扩展</span></strong><span style="color: rgb(31, 31, 31)">（Window System Integration, WSI）。</span>

- <a id="ufa86e2ed"></a><span style="color: rgb(31, 31, 31)">因为并不是所有的 Vulkan 程序都需要显示器。比如运行在高性能服务器上的 AI 训练、离线光线追踪渲染器，它们只需要把渲染结果保存为图片，不需要弹出一个窗口。</span>
- <a id="u19d4ff8e"></a><span style="color: rgb(31, 31, 31)">因此，窗口显示功能被剥离出了核心规范，放进了扩展里。</span>`VkSurfaceKHR`<span style="color: rgb(31, 31, 31)"> 就是由全局扩展 </span>`VK_KHR_surface`<span style="color: rgb(31, 31, 31)"> 引入的。</span>

<a id="cca00233"></a>
### <span style="color: rgb(31, 31, 31)">3. Window Surface 是如何创建的？</span>

<a id="u1b575793"></a><span style="color: rgb(31, 31, 31)">由于每个操作系统的窗口系统底层实现完全不同，Vulkan 官方针对不同平台提供了专属的“特化创建函数”。</span>

<a id="uda94503f"></a><span style="color: rgb(31, 31, 31)">如果纯手写跨平台代码，需要写一堆宏条件编译：</span>

<a id="LeyjF"></a>
```cpp
#if defined(VK_USE_PLATFORM_WIN32_KHR)
    // Windows 专用的创建表单
    VkWin32SurfaceCreateInfoKHR createInfo{};
    createInfo.hwnd = hwnd; // 传入 Win32 的窗口句柄
    vkCreateWin32SurfaceCreateInfoKHR(...);
    #elif defined(VK_USE_PLATFORM_XLIB_KHR)
    // Linux X11 专用
    VkXlibSurfaceCreateInfoKHR createInfo{};
    vkCreateXlibSurfaceKHR(...);
#endif
```

<a id="7ae98655"></a>
#### <span style="color: rgb(31, 31, 31)">C++ 现代工程实践（配合 GLFW）</span>

<a id="u8d3eef36"></a><span style="color: rgb(31, 31, 31)">但是现在几乎没有人会去纯手写上面那些恶心的平台宏。我们通常会使用 </span>`GLFW`<span style="color: rgb(31, 31, 31)">。GLFW 会在内部自动判断当前的操作系统，只需要一行代码，它就能把 </span>`VkSurfaceKHR`<span style="color: rgb(31, 31, 31)"> 完美创建出来：</span>

<a id="sEQ0u"></a>
```cpp
VkSurfaceKHR surface;
// GLFW 内部会自动调用 vkCreateWin32SurfaceKHR 或 vkCreateXlibSurfaceKHR
if (glfwCreateWindowSurface(instance, window, nullptr, &surface) != VK_SUCCESS) {
    throw std::runtime_error("Failed to create window surface!");
}
```

<a id="24b34717"></a>
### <span style="color: rgb(31, 31, 31)">4. 拥有 Surface 之后，下一步做什么？</span>

<a id="u3d968538"></a><span style="color: rgb(31, 31, 31)">创建好 Window Surface 只是第一步。在整个 Vulkan 初始化生命周期里，它是后续两个极为核心的步骤的</span><strong><span style="color: rgb(31, 31, 31)">强依赖参数</span></strong><span style="color: rgb(31, 31, 31)">：</span>

<a id="77c42037"></a>
#### <span style="color: rgb(31, 31, 31)">① 筛选硬件队列族（Present Support Check）</span>

<a id="ub609bcd1"></a><span style="color: rgb(31, 31, 31)">我们在聊“呈现队列”时提过，你需要拿着这个创建好的 </span>`surface`<span style="color: rgb(31, 31, 31)"> 去质问物理显卡：“你的哪个队列族，能把画画好之后的图像安全地扔进这个 </span>`surface`<span style="color: rgb(31, 31, 31)"> 里显示出来？”</span>

<a id="oarUa"></a>
```cpp
VkBool32 presentSupport = VK_FALSE;
vkGetPhysicalDeviceSurfaceSupportKHR(physicalDevice, queueFamilyIndex, surface, &presentSupport);
```

<a id="b7bda48f"></a>
#### <span style="color: rgb(31, 31, 31)">② 创建交换链（Swapchain）</span>

<a id="u5283b1af"></a><span style="color: rgb(31, 31, 31)">这是 Surface 最重要的归宿。有了 Surface，你才能向显卡申请</span><strong><span style="color: rgb(31, 31, 31)">交换链（Swapchain）</span></strong><span style="color: rgb(31, 31, 31)">。</span>

<a id="u9f4b8cee"></a><span style="color: rgb(31, 31, 31)">交换链会在这个 Surface 背后开辟一个“前台缓冲区”和“后台缓冲区”（通常是 2~3 张图形图片，即双重缓冲或三重缓冲）。GPU 在后台缓冲区拼命画画，画完之后，通过交换链，把图片平铺到这个 Surface 上展示给玩家看。</span>

<a id="25f9c7fa"></a>
### <span style="color: rgb(31, 31, 31)">总结</span>

- <a id="ub201d1ac"></a><strong><span style="color: rgb(31, 31, 31)">Window Surface（</span></strong>`VkSurfaceKHR`<strong><span style="color: rgb(31, 31, 31)">）</span></strong><span style="color: rgb(31, 31, 31)"> 不是一块真实的显存，也不是一个可以往里写数据的缓冲区。</span>
- <a id="u11d0a68c"></a><span style="color: rgb(31, 31, 31)">它是一个</span><strong><span style="color: rgb(31, 31, 31)">抽象的“显示表面占位符”</span></strong><span style="color: rgb(31, 31, 31)">。</span>
- <a id="u504e9c66"></a><span style="color: rgb(31, 31, 31)">它的唯一任务，就是把操作系统的原生窗口死死地和 Vulkan 的世界锚定在一起。后续所有关于</span><strong><span style="color: rgb(31, 31, 31)">屏幕刷新率、垂直同步、交换链双缓冲、窗口缩放格式</span></strong><span style="color: rgb(31, 31, 31)">的配置，全部都要基于这个 Surface 来展开。</span>

原文：[Window Surface](<https://www.yuque.com/u62694975/iaaa/eeg2ouxti0x7ocyb>)
