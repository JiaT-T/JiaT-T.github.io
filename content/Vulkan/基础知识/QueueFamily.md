---
title: "Vulkan 队列族"
date: 2026-06-09T14:00:00+08:00
draft: false
summary: "用硬件执行能力和现实类比梳理 Vulkan Queue Family 与 VkQueue 的关系。"
categories: ["Vulkan"]
tags: ["Vulkan", "Computer Graphics", "Rendering"]
---

在讲队列族（Queue Family）之前，我们可以用一个非常形象的现实生活场景来理解它：

想象一下，GPU 是一个大型的**高效工厂**，而队列族就是这个工厂里的**不同车间**。

- **车间 A（图形渲染车间）：** 里面有一批专门负责涂色、画画的工人，也配有搬运工。

- **车间 B（纯数据搬运车间）：** 里面全是搬运工，专门负责把原材料（数据）从外面的仓库（CPU/内存）搬进工厂内部（显存）。

每个车间里的工人，就是一条条具体的**队列（VkQueue）**。你把任务（Command Buffer）写在单子上，丢给某一个车间的某一个工人，他们就会开始排队干活。

在 Vulkan 中，**队列族（Queue Family）** 就是对具有**相同硬件功能、共享相同硬件特质的一组队列**的抽象分类。

> - **分类是按“族（Family）”来分的**：图形是一族，计算可能是一族，传输可能是一族。

> - **“队列（Queue）”是族里面的具体执行成员**：同一个族里的所有队列，**功能是完全一模一样的**。

### 1. 为什么 Vulkan 要引入“族”的概念？

传统的图形 API（如 OpenGL）通常隐式地提供一个“大总管”上下文，不管下达什么指令它都吞下去，但我们根本不知道 GPU 底层是谁在干活。

而 Vulkan 为了追求极致的性能和多线程掌控力，把 GPU 的底层硬件底牌彻底掀开了：

GPU 芯片内部其实是由不同的物理硬件引擎（Execution Engines）组成的。有的硬件电路专门跑光栅化，有的专门跑通用计算，有的专门做 DMA 内存传输。

Vulkan 为了能压榨这些硬件，它把这些互相独立、功能不同的硬件执行管道分组，每一组就是一个 **Queue Family**。

### 2. 队列族的四大核心属性

当用代码去枚举并检查显卡的队列族时（通过 `vkGetPhysicalDeviceQueueFamilyProperties`），每一个队列族都会报告它具备以下几个核心属性：

#### ① 队列标志 (`queueFlags`)

这决定了这个车间能干什么活。它是以下几个标志位的组合：

- `VK_QUEUE_GRAPHICS_BIT`：能处理图形管线任务（画画）。

- `VK_QUEUE_COMPUTE_BIT`：能处理通用计算（算物理、算AI）。

- `VK_QUEUE_TRANSFER_BIT`：能高效搬运数据（内存拷贝）。

- `VK_QUEUE_SPARSE_BINDING_BIT`：能处理虚拟/稀疏内存绑定。

#### ② 队列数量 (`queueCount`)

也就是这个车间里有多少个“打工人”（实例）。

比如某个图形队列族的 `queueCount = 1`，说明这个车间虽然能画画，但只有一条流水线，你只能实例化出一个 `VkQueue` 句柄来用。如果 `queueCount = 4`，就可以同时创建 4 个独立的 `VkQueue` 句柄，从多个 CPU 线程同时往这 4 个队列里提交任务，实现真正的多线程并行提交。

#### ③ 时间戳支持精度 (`timestampValidBits`)

这个队列族在执行性能分析（Profiling）时，支持多少位的计时器精度。如果值为 0，说明该队列族不支持时间戳查询。

#### ④ 图像传输的最小粒度 (`minImageTransferGranularity`)

该队列族在搬运图像数据时，支持的最小对齐宽高（比如 $1 \times 1 \times 1$ 或者 $4 \times 4 \times 1$）。

### 3. 实际硬件中，队列族长什么样？

硬件厂商（NVIDIA, AMD, Intel）在底层设计上各有想法，这也导致了在不同的显卡上，队列族的分布截然不同。

我们可以看看两种最典型的显卡队列族分布（假设我们要找图形、计算、传输三种功能）：

#### 情况 A：全能型“大车间”（常见于桌面离散显卡，如 NVIDIA）

有些显卡非常简单粗暴，它可能只提供 **1 到 2 个队列族**：

- **Queue Family 0:** `queueCount = 1`, 标志位是 `GRAPHICS | COMPUTE | TRANSFER`。这个族是个全能车间，什么都能干。

- **Queue Family 1:** `queueCount = 1`, 标志位只有 `TRANSFER`。这是一个纯搬运工车间。

在这种显卡上，图形任务、计算任务往往都是找 `Family 0` 创建的同一个 `VkQueue` 去排队执行。

#### 情况 B：专职型“独立车间”（常见于支持强异步计算的显卡，如 AMD）

有些显卡为了追求极致的异步并行（Async Compute），会分得很细：

- **Queue Family 0 (Graphics):** `queueCount = 1`，带 `GRAPHICS | COMPUTE | TRANSFER`。

- **Queue Family 1 (Compute):** `queueCount = 2`，只带 `COMPUTE | TRANSFER`。**没有图形能力！**

- **Queue Family 2 (Transfer):** `queueCount = 2`，只带 `TRANSFER`。**纯 DMA 拷贝引擎！**

在现代游戏引擎中，这种架构就非常爽。我们可以让主线程把渲染画面的命令丢给 `Family 0`；同时让另一个后台线程把粒子物理模拟计算丢给 `Family 1` 的独立计算队列。两边在 GPU 硬件层面上是**同时并行跑**的，互不干扰，这就叫**异步计算（Async Compute）**。

### 总结

在 Vulkan 的初始化流程中，必经之路是：

1. 遍历所有可用的物理显卡。

2. 遍历该显卡上的所有 **队列族（Queue Family）**。

3. 挑选出满足你需求的族（比如既支持 `GRAPHICS` 又能支持窗口 `PRESENT` 的族）。

4. 记住这个族的 **索引值（Queue Family Index）**。

5. 在创建逻辑设备（`VkDevice`）时，指定在这个族里创建几个具体的 **队列（VkQueue）** 供以后干活使用。

