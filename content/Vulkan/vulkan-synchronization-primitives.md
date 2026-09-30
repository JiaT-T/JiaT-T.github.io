---
title: "Vulkan 同步原语"
slug: "vulkan-synchronization-primitives"
summary: "比较 Fence、Semaphore、Pipeline Barrier 与 Event 的同步范围、常见用途和相关 API。"
categories: ["Vulkan"]
tags: ["Vulkan", "Synchronization", "Fence", "Semaphore", "Pipeline Barrier"]
date: "2026-06-12T09:13:28.000Z"
lastmod: "2026-06-14T02:06:17.000Z"
draft: false
yuque_slug: "eoz37blkm9xp59gy"
source: "https://www.yuque.com/u62694975/iaaa/eoz37blkm9xp59gy"
---

<a id="udf4a321b"></a>在 Vulkan 中，由于驱动层不会隐式地进行任何自动同步，因此所有的资源读写、执行顺序等操作都需要手动地进行管理。 Vulkan 核心的同步原语有四种：<strong>Fence（栅栏）</strong>、<strong>Semaphore（信号量）</strong>、<strong>Event（事件）</strong> 和 <strong>Pipeline Barrier（管线屏障）。</strong>

<a id="IAkj1"></a>
## <span style="color: #DF2A3F">1. Fence（栅栏）：CPU 与 GPU 之间的同步</span>

<a id="ud242cbc2"></a>Fence 主要用于<strong>让 CPU 等待 GPU</strong> 完成某些操作。

- <a id="u31a0be02"></a><strong>特点：</strong> 它有两种状态：Signaled（触发/绿灯）和 Unsignaled（未触发/红灯）。通常由 GPU 在执行完某个 Queue 的命令后将其置为 Signaled，而 CPU 在另一端阻塞等待。
- <a id="u6357bf5d"></a><strong>常见用途：</strong> 帧率控制（避免 CPU 提交命令的速度远超 GPU 渲染速度）。例如，在开始录制新一帧的 Command Buffer 之前，CPU 必须等待上一帧对应的 Fence 被触发。
- <a id="ue4677740"></a><strong>核心 API：</strong> \* `vkQueueSubmit`（传入 Fence，当 Queue 中的任务执行完毕时，GPU 会自动将该 Fence 设为 Signaled）

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u6848a204"><code id="u9233bb91"><span id="u1764e292">vkWaitForFences</span></code><span id="u36e82940">（CPU 端阻塞等待）</span></li><li id="u63c4da66"><code id="u7a737bac"><span id="ue12dd042">vkResetFences</span></code><span id="u040bc829">（使用前必须手动重置为 Unsignaled）</span></li></ul>

<a id="GnCfD"></a>
## <span style="color: #DF2A3F">2. Semaphore（信号量）：GPU Queue 之间的同步</span>

<a id="u6d4b588f"></a>Semaphore 用于 <strong>GPU 内部不同 Queue 之间</strong> 或者 <strong>同一 Queue 内不同提交（Submit）之间</strong> 的粗粒度同步。CPU 无法直接等待或触发它。

<a id="uf4c73944"></a>Vulkan 中的 Semaphore 分为两种：

- <a id="ua391bcd1"></a><strong>Binary Semaphore（二元信号量）：</strong> 只有两种状态（Signaled/Unsignaled）。常用于交换链图像获取与渲染的同步。
- <a id="u86e47488"></a><strong>Timeline Semaphore（时间轴信号量，Vulkan 1.2+）：</strong> 包含一个单调递增的 64 位整数值。当它的值大于或等于指定的等待值时，同步完成。它允许更灵活的粗粒度依赖管理（甚至支持 CPU 等待或增加其数值）。
- <a id="u45f6f136"></a><strong>常见用途：</strong>`vkAcquireNextImageKHR`（获取交换链图像后触发 Semaphore） \$\\rightarrow\$`vkQueueSubmit`（等待该 Semaphore 产生后才开始渲染渲染管线）。
- <a id="u2f02cb29"></a><strong>核心机制：</strong> 在 `vkQueueSubmit` 的 `VkSubmitInfo` 结构体中，分别填入 `pWaitSemaphores`（执行前需要等待谁）和 `pSignalSemaphores`（执行完后去触发谁）。

<a id="mtCYA"></a>
## <span style="color: #DF2A3F">3. Pipeline Barrier（管线屏障）：GPU 内部 / 管线阶段之间的同步</span>

<a id="u9ac32d32"></a>Pipeline Barrier 是 Vulkan 中最频繁、最精细、也最复杂的同步手段。它用于 <strong>同一 Queue 内部的不同命令之间</strong> 的同步，解决管线内各阶段（Pipeline Stages）的读写冲突，并负责处理<strong>内存可见性（Memory Visibility）</strong><strong>和</strong><strong>图像布局转换（Layout Transition）</strong>。

<a id="ue87ebf4c"></a>当你在 Command Buffer 中插入一个 Barrier 时，需要显式指定以下几个要素：

- <a id="uc334ef40"></a><strong>Source Stage / Destination Stage（源阶段 / 目标阶段）：</strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u95f3bcfb"><span id="u0b3f856b">规定了哪些先前的指令（Src）必须在哪些后续指令（Dst）开始之前执行完毕。例如：等待顶点着色器（</span><code id="u5505b215"><span id="u879cbaa4">VS</span></code><span id="udfe6b81a">）写完，才允许片段着色器（</span><code id="u959029f0"><span id="u0a538f8b">FS</span></code><span id="u8cb970ac">）去读。</span></li></ul>

- <a id="u84ea2b66"></a><strong>Access Masks（访问掩码）：</strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u4e9e12e2"><span id="u0dc9ee6c">规定了内存的读写类型，解决 RAW（写后读）、WAR（读后写）、WAW（写后写）冲突。</span></li><li id="u4536d985"><strong><span id="u01bf8773">Execution Dependency（执行依赖）：</span></strong><span id="u711f3f76"> 确保 Dst 阶段在 Src 阶段结束后才执行。</span></li><li id="ub4d76ca1"><strong><span id="u117ddb23">Memory Dependency（内存依赖）：</span></strong><span id="u2fe64079"> 确保 Src 阶段写入 L1/L2 Cache 的数据刷新到全局内存（Make Available），并让 Dst 阶段能正确从内存读取（Make Visible）。</span></li></ul>

- <a id="ub5def292"></a><strong>Image Layout Transitions（图像布局转换）：</strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u8a6433bd"><span id="u760df38f">GPU 对不同用途的 Image 有不同的内部瓦片（Tiling）或压缩优化。在将一个 Image 从“渲染目标（Color Attachment）”变成“采样纹理（Shader Read Only）”时，必须通过 Image Memory Barrier 进行布局转换，否则会导致硬件读取错误。</span></li></ul>

<a id="OYmUD"></a>
## <span style="color: #DF2A3F">4. Event（事件）：GPU 内部的细粒度延迟同步</span>

<a id="ua9e03f12"></a>Event 类似于 Pipeline Barrier 的“拆分版”，它允许<strong>异步的、非阻塞的</strong>在 GPU 管线中标记进度。

- <a id="u7904a05c"></a><strong>特点：</strong> Barrier 是立刻在命令流中划定一道分界线，而 Event 允许你在前面的命令走到某个阶段时“设置（Set）”它，在很久之后的另一个地方再去“等待（Wait）”它。
- <a id="u8946d94f"></a><strong>常见用途：</strong> 减少 GPU 的管线气泡（Bubble）。例如，你在管线早期生成了一段数据，只要在该数据真正被使用的后继阶段之前进行等待即可，中途的其他管线阶段可以并发执行。
- <a id="uacc783db"></a><strong>核心 API：</strong>`vkCmdSetEvent` 和 `vkCmdWaitEvents`。

<a id="DSHjG"></a>
## 总结与对比

<a id="u396907d9"></a>为了理清它们的关系，可以通过它们在流水线中的协作层次来区分：

<a id="yj1ID"></a>
| <a id="u43506953"></a><strong>同步原语</strong> | <a id="uaad8da5d"></a><strong>控制主体</strong> | <a id="ufcbde4cc"></a><strong>作用域</strong> | <a id="u822b525d"></a><strong>粒度</strong> | <a id="u8041c323"></a><strong>主要应用场景</strong> |
| --- | --- | --- | --- | --- |
| <a id="u3f6044aa"></a><strong>Fence</strong> | <a id="u1ac40b1f"></a><strong>CPU 与 GPU</strong> | <a id="ufbcda8c0"></a>整个 Queue 提交的任务 | <a id="udb563b5a"></a>最粗 | <a id="u907f274d"></a>帧同步、等待一帧彻底渲染完、重建交换链 |
| <a id="uab136cf6"></a><strong>Semaphore</strong> | <a id="u2de277bc"></a><strong>GPU 与 GPU</strong> | <a id="u4117deb1"></a>Queue 之间 或 Submit 之间 | <a id="u99bb3d29"></a>粗 | <a id="u6f3be6d8"></a>等待 Image 可用、计算队列与渲染队列交替 |
| <a id="u4be45198"></a><strong>Pipeline Barrier</strong> | <a id="u78d1a4be"></a><strong>GPU 内部</strong> | <a id="u7e6d4967"></a>同一 Queue 的 Command 之间 | <a id="u15e284a2"></a>细（管线阶段级） | <a id="u85a6662b"></a>资源读写保护、Texture Layout 转换 |
| <a id="u75804ce0"></a><strong>Event</strong> | <a id="uf0a65ae2"></a><strong>GPU 内部</strong> | <a id="u1f57c8c7"></a>同一 Queue 的 Command 之间 | <a id="ud74f88c6"></a>精细（支持异步拆分） | <a id="ue67506a3"></a>消除复杂的依赖气泡、细粒度资源复用 |

原文：[同步原语](<https://www.yuque.com/u62694975/iaaa/eoz37blkm9xp59gy>)
