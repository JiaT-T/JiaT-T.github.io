---
title: "GLFW 与 Vulkan 窗口创建"
slug: "vulkan-glfw"
summary: "整理 GLFW 的跨平台窗口与输入职责，以及 Vulkan 实例扩展查询和窗口 Surface 创建方式。"
categories: ["Vulkan"]
tags: ["Vulkan", "GLFW", "Window System", "Rendering"]
date: "2026-06-07T06:41:45.000Z"
lastmod: "2026-06-07T06:44:40.000Z"
draft: false
yuque_slug: "tu6m6ag7e2eddccz"
source: "https://www.yuque.com/u62694975/iaaa/tu6m6ag7e2eddccz"
---

<a id="u56a242c8"></a><span style="color: rgb(31, 31, 31)">在图形学开发中，</span><strong><span style="color: rgb(31, 31, 31)">GLFW</span></strong><span style="color: rgb(31, 31, 31)"> 是一个非常轻量级、跨平台的 </span><strong><span style="color: rgb(31, 31, 31)">C 语言开源库</span></strong><span style="color: rgb(31, 31, 31)">。它的核心任务非常纯粹：</span><strong><span style="color: rgb(31, 31, 31)">帮你处理窗口创建、操作系统上下文管理以及用户输入</span></strong><span style="color: rgb(31, 31, 31)">。</span>

<a id="uf9f010f7"></a><span style="color: rgb(31, 31, 31)">如果要写 Vulkan、OpenGL 或 OpenGL ES 程序，不能直接让代码在空无一物的操作系统上画画，必须先向 Windows、Linux 或 macOS 申请一个“窗口”，并捕获键盘鼠标的操作。GLFW 就是干这个脏活累活的。</span>

<a id="32a4e16e"></a>
### <span style="color: rgb(31, 31, 31)">1. 为什么需要 GLFW？（解决跨平台痛点）</span>

<a id="ub0ab38a7"></a><span style="color: rgb(31, 31, 31)">如果不使用任何第三方库，纯手写一个能在屏幕上弹出来的窗口，代码会变成这样：</span>

- <a id="u64967fef"></a><strong><span style="color: rgb(31, 31, 31)">在 Windows 上：</span></strong><span style="color: rgb(31, 31, 31)"> 调用 </span>`Win32 API`<span style="color: rgb(31, 31, 31)">，写一堆 </span>`WNDCLASSEX`<span style="color: rgb(31, 31, 31)">、</span>`CreateWindowEx`<span style="color: rgb(31, 31, 31)">，还要写一个极其繁琐的 </span>`WindowProc`<span style="color: rgb(31, 31, 31)"> 消息循环来处理 Windows 系统的各种消息。</span>
- <a id="u9c930b40"></a><strong><span style="color: rgb(31, 31, 31)">在 Linux 上：</span></strong><span style="color: rgb(31, 31, 31)"> 得去和 </span>`X11 (Xlib)`<span style="color: rgb(31, 31, 31)"> 或者更现代的 </span>`Wayland`<span style="color: rgb(31, 31, 31)"> 协议打交道，处理各种底层的 Display 和 Window 句柄。</span>
- <a id="u70f1e94a"></a><strong><span style="color: rgb(31, 31, 31)">在 macOS 上：</span></strong><span style="color: rgb(31, 31, 31)"> 得用 Objective-C 或 Swift 去调用 Cocoa 框架。</span>

<a id="u40c1c280"></a><span style="color: rgb(31, 31, 31)">这会导致图形引擎还没开始写画三角形的代码，就已经被不同操作系统的平台初始化代码淹没了。</span>

<a id="u46711c00"></a><strong><span style="color: rgb(31, 31, 31)">GLFW 的出现，把这些平台差异完全抹平了。</span></strong><span style="color: rgb(31, 31, 31)"> 无论在什么操作系统上，创建窗口的代码都精简成了统一的一行：</span>`glfwCreateWindow`<span style="color: rgb(31, 31, 31)">。</span>

<a id="b4dcdb9b"></a>
### <span style="color: rgb(31, 31, 31)">2. GLFW 的核心职能</span>

<a id="u5d7adc01"></a><span style="color: rgb(31, 31, 31)">GLFW 的功能非常克制和专一，它</span><strong><span style="color: rgb(31, 31, 31)">只管窗口和输入，不管怎么画画</span></strong><span style="color: rgb(31, 31, 31)">：</span>

- <a id="ucbdf6c99"></a><strong><span style="color: rgb(31, 31, 31)">窗口管理 (Window Management)：</span></strong><span style="color: rgb(31, 31, 31)"> 创建和销毁桌面窗口、处理窗口缩放、最大化/最小化、移动、多显示器全屏切换等。</span>
- <a id="u9b490f8a"></a><strong><span style="color: rgb(31, 31, 31)">图形上下文管理 (Context Management)：</span></strong><span style="color: rgb(31, 31, 31)"> 配置和初始化 OpenGL/OpenGL ES 的上下文，或者专门</span><strong><span style="color: rgb(31, 31, 31)">为 Vulkan 提供跨平台的 Surface 创建支持</span></strong><span style="color: rgb(31, 31, 31)">。</span>
- <a id="u9615ae10"></a><strong><span style="color: rgb(31, 31, 31)">输入事件处理 (Input Handling)：</span></strong><span style="color: rgb(31, 31, 31)"> 极度简单的回调机制。可以轻松捕获键盘按键（按下、抬起、连发）、鼠标移动、鼠标点击、滚轮滚动，甚至还支持手柄/摇杆（Joystick）的输入。</span>
- <a id="uba89fd89"></a><strong><span style="color: rgb(31, 31, 31)">高精度计时器：</span></strong><span style="color: rgb(31, 31, 31)"> 提供了一个跨平台的高精度时间函数 </span>`glfwGetTime()`<span style="color: rgb(31, 31, 31)">，非常适合用来计算游戏引擎的帧间隔时间（Delta Time）。</span>

<a id="21368b72"></a>
### <span style="color: rgb(31, 31, 31)">3. 它在 Vulkan 开发中的特殊生态位</span>

<a id="ua74c45bb"></a><span style="color: rgb(31, 31, 31)">如果是在写 OpenGL，GLFW 会顺便创建好 OpenGL 的渲染上下文（Context）。但在 </span><strong><span style="color: rgb(31, 31, 31)">Vulkan</span></strong><span style="color: rgb(31, 31, 31)"> 中，情况发生了一点变化。</span>

<a id="u6fd16859"></a><span style="color: rgb(31, 31, 31)">Vulkan 是一个完全隐式无关的 API，它默认不感知窗口系统。我们在前面聊过，Vulkan 要想把画面扔到屏幕上，必须借助 </span><strong><span style="color: rgb(31, 31, 31)">WSI（窗口系统集成）扩展</span></strong><span style="color: rgb(31, 31, 31)">（比如 </span>`VK_KHR_surface`<span style="color: rgb(31, 31, 31)">）。</span>

<a id="uba92c123"></a><span style="color: rgb(31, 31, 31)">为了创建这个 </span>`VkSurfaceKHR`<span style="color: rgb(31, 31, 31)">，如果纯手写，需要针对 Windows 调用 </span>`vkCreateWin32SurfaceKHR`<span style="color: rgb(31, 31, 31)">，针对 Linux 调用 </span>`vkCreateXlibSurfaceKHR`<span style="color: rgb(31, 31, 31)">。</span>

<a id="udb7d3684"></a><span style="color: rgb(31, 31, 31)">而 GLFW 为 Vulkan 提供了极好的原生支持，它直接提供了两个极简的 API，完美融入 Vulkan 初始化工作流：</span>

<a id="e448b41f"></a>
#### <span style="color: rgb(31, 31, 31)">① 剥离 OpenGL 上下文</span>

<a id="udf3991c5"></a><span style="color: rgb(31, 31, 31)">在创建窗口前，通过设置 Hint 告诉 GLFW：“我不需要你帮我初始化 OpenGL，我是给 Vulkan 用的”：</span>

<a id="L98Av"></a>
```plain
glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API); 
GLFWwindow* window = glfwCreateWindow(800, 600, "Vulkan Window", nullptr, nullptr);
```

<a id="256fe14f"></a>
#### <span style="color: rgb(31, 31, 31)">② 自动获取 Instance 级别扩展</span>

<a id="u0b5184ab"></a><span style="color: rgb(31, 31, 31)">我们在初始化 Vulkan </span>`VkInstance`<span style="color: rgb(31, 31, 31)"> 时，需要开启平台特定的窗口扩展。GLFW 可以直接把当前操作系统需要的所有全局扩展名称打包：</span><span style="color: rgb(255, 255, 255)">++</span>

<a id="AF59H"></a>
```plain
uint32_t glfwExtensionCount = 0;
const char** glfwExtensions;
glfwExtensions = glfwGetRequiredInstanceExtensions(&glfwExtensionCount);

// 随后直接把 glfwExtensions 塞进 VkInstanceCreateInfo 的 enabledExtensionNames 中
```

<a id="ee66f0ba"></a>
#### <span style="color: rgb(31, 31, 31)">③ 一键创建跨平台 Surface</span>

<a id="ua1f54f19"></a><span style="color: rgb(31, 31, 31)">当选好显卡，准备把窗口和 Vulkan 绑定时，一行代码就能搞定原本需要分平台宏判断（</span>`#ifdef _WIN32`<span style="color: rgb(31, 31, 31)">）的 Surface 创建工作：</span>

<a id="RQSO4"></a>
```plain
VkSurfaceKHR surface;
if (glfwCreateWindowSurface(instance, window, nullptr, &surface) != VK_SUCCESS)
{
    throw std::runtime_error("failed to create window surface!");
}
```

<a id="264366bb"></a>
### <span style="color: rgb(31, 31, 31)">4. GLFW vs SDL2 vs GLUT (横向对比)</span>

<a id="ua9c70be5"></a><span style="color: rgb(31, 31, 31)">当然还有其他类似的库，它们之间的侧重点各有不同：</span>

<table id="I9QDY"><colgroup><col width="250"><col width="250"><col width="250"></colgroup><tbody><tr id="uc1fbce1a"><td id="u64d53ec2"><p id="u8d2a2bb7"><strong><span id="uc3a8e3d6" style="color: rgb(31, 31, 31)">库名称</span></strong></p></td><td id="u17140f14"><p id="u20ecab06"><strong><span id="ue1a7eeb7" style="color: rgb(31, 31, 31)">特点与定位</span></strong></p></td><td id="u925f0eb6"><p id="ue8e34daa"><strong><span id="uf09bf184" style="color: rgb(31, 31, 31)">适用场景</span></strong></p></td></tr><tr id="ud8c6c1ca"><td id="uded6094f"><p id="u604c6946"><strong><span id="ufb90a4ed" style="color: rgb(31, 31, 31)">GLFW</span></strong></p></td><td id="uf7573643"><p id="u142039d1"><strong><span id="ufb0a96a6" style="color: rgb(31, 31, 31)">极其现代、轻量、纯粹。</span></strong><span id="ub0266b4c" style="color: rgb(31, 31, 31)"> 只专注于窗口和输入，API 设计非常符合现代 C/C++ 程序员的习惯。没有臃肿的历史包袱。</span></p></td><td id="ub2065568"><p id="ud44cb3f6"><span id="u91166364" style="color: rgb(31, 31, 31)">现代图形学学习、自研现代渲染器（Vulkan/OpenGL）、游戏引擎底层窗口封装。</span></p></td></tr><tr id="ubddb2df3"><td id="u718abf1f"><p id="ue839d133"><strong><span id="u66e30197" style="color: rgb(31, 31, 31)">SDL2 / SDL3</span></strong></p></td><td id="uf35ec0ed"><p id="u213867bd"><strong><span id="u3599ec04" style="color: rgb(31, 31, 31)">巨无霸级别的多媒体库。</span></strong><span id="ud1d3c155" style="color: rgb(31, 31, 31)"> 除了窗口和输入，它还自带音频播放、线程管理、文件 IO、甚至自带一个 2D 渲染引擎。</span></p></td><td id="ude09442c"><p id="ud5d0fb47"><span id="u28420d99" style="color: rgb(31, 31, 31)">跨平台商业游戏开发、模拟器开发（因为它管得极宽）。</span></p></td></tr><tr id="u9ee82694"><td id="u8b64a4c7"><p id="u87376a1a"><strong><span id="ud6aa616e" style="color: rgb(31, 31, 31)">GLUT / FreeGLUT</span></strong></p></td><td id="ud6a07933"><p id="u3591559e"><strong><span id="u30633825" style="color: rgb(31, 31, 31)">古老、过时的化石库。</span></strong><span id="uc2350a4f" style="color: rgb(31, 31, 31)"> 控制权在库本身（回调地狱），很难和现代渲染管线及多线程很好地融合。</span></p></td><td id="ue73b56c0"><p id="uf569d209"><span id="u04daba89" style="color: rgb(31, 31, 31)">工业界和现代开发已基本淘汰，仅在一些高校非常老旧的 OpenGL 1.x/2.x 课设中能看到。</span></p></td></tr></tbody></table>

<a id="25f9c7fa"></a>
### <span style="color: rgb(31, 31, 31)">总结</span>

<a id="u873f3430"></a><strong><span style="color: rgb(31, 31, 31)">GLFW</span></strong><span style="color: rgb(31, 31, 31)"> 是现代图形学开发的“标准敲门砖”。它就像一顶安全帽，把各家操作系统底层最恶心、最繁琐的窗口创建和消息循环脏活全部挡在外面，让我们能够把 100% 的精力优雅地集中在 Vulkan 队列族、交换链、着色器和渲染管线的编写上。</span>

原文：[GLFW](<https://www.yuque.com/u62694975/iaaa/tu6m6ag7e2eddccz>)
