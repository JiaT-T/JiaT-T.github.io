---
title: "Vulkan VkResult"
slug: "vulkan-vkresult"
summary: "整理 VkResult 的成功与状态码、常见错误码及 Vulkan 调用中的返回值检查。"
categories: ["Vulkan"]
tags: ["Vulkan", "VkResult", "Error Handling"]
date: "2026-06-07T05:34:34.000Z"
lastmod: "2026-06-07T05:36:39.000Z"
draft: false
yuque_slug: "zucwsv0166un96bw"
source: "https://www.yuque.com/u62694975/iaaa/zucwsv0166un96bw"
---

<a id="uddfebd57"></a>在 Vulkan 中，`VkResult` 是一个非常核心的<strong>枚举类型（Enumeration）</strong>，专门用来作为绝大多数 Vulkan 函数的<strong>返回值</strong>。

<a id="u4a0ac058"></a>因为 Vulkan 是一个极度显式的低级 API，驱动程序内部几乎不会帮你做任何隐式错误处理，也不会抛出 C++ 异常。任何一个操作（比如创建对象、分配显存、提交命令）成功与否，都必须通过 `VkResult` 显式地反馈给开发者。

<a id="AmiBo"></a>
### VkResult 的两大分类

<a id="ua6fcf3a5"></a>`VkResult` 的枚举值主要分为两大阵营：<strong>成功/状态码（Success/Status Codes）</strong> 和 <strong>错误码（Error Codes）</strong>。

<a id="DLPa3"></a>
#### 核心成功码（通常 ≥ 0）

<a id="u78beb0ad"></a>这些值代表函数不仅成功执行，还可能带回了一些运行时状态信息：

- <a id="uf1565a4c"></a>`VK_SUCCESS`<strong> (0):</strong> 最完美的情况，函数成功执行且没有发生任何意外。
- <a id="ueeee7a80"></a>`VK_NOT_READY`<strong>:</strong> 一个围栏（Fence）或查询还没有完成。
- <a id="u5a620068"></a>`VK_TIMEOUT`<strong>:</strong> 某个等待操作（比如等待一个信号量或围栏）在指定时间内没有完成。
- <a id="u5ffe2fd8"></a>`VK_INCOMPLETE`<strong>:</strong> 缓冲区太小，无法返回所有请求的结果（例如获取交换链图像时，提供的数组长度不够，只返回了一部分）。

<a id="zc1nV"></a>
#### 核心错误码（通常 &lt; 0）

<a id="ub60c6720"></a>这些值代表操作彻底失败。由于 Vulkan 遵循 <strong>RAII</strong>（资源获取即初始化）和严苛的显式内存管理，很多错误都直接指向内存和驱动底层：

- <a id="u4eb0a990"></a>`VK_ERROR_OUT_OF_HOST_MEMORY`<strong>:</strong> CPU 端（主机）内存不足，无法完成分配。
- <a id="ucebf48a1"></a>`VK_ERROR_OUT_OF_DEVICE_MEMORY`<strong>:</strong> GPU 端（设备）显存不足。这是开发中非常需要警惕的错误，通常需要你重新规划 `VkDeviceMemory` 的分配策略。
- <a id="ubf8ad528"></a>`VK_ERROR_INITIALIZATION_FAILED`<strong>:</strong> 初始化失败，通常是因为显卡驱动不支持 Vulkan 或者是某些层（Validation Layers）没找对。
- <a id="u1e12a21c"></a>`VK_ERROR_DEVICE_LOST`<strong>:</strong> 极其致命的错误。GPU 挂起了、掉线了、或者因为耗时过长被操作系统强制重置了（TDR）。
- <a id="ub16fba32"></a>`VK_ERROR_OUT_OF_DATE_KHR`<strong>:</strong> 交换链（Swapchain）特有错误。当窗口大小改变（比如用户拖动了窗口）或者屏幕旋转时，原有的交换链图像与当前的 Surface（表面）不再匹配，必须重建交换链。

<a id="25f9c7fa"></a>
### 总结

<a id="u5abf076f"></a>把 `VkResult` 看作是 Vulkan 驱动与你的 C++ 代码之间沟通的“体检报告”。通过它，你能第一时间抓到是 <strong>CPU 内存爆了</strong>、<strong>GPU 显存穿了</strong>、还是<strong>用户偷偷拉大窗口</strong>了。

原文：[VkResult](<https://www.yuque.com/u62694975/iaaa/zucwsv0166un96bw>)
