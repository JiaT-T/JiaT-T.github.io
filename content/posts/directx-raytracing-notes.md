---
title: "DXR 基础笔记"
slug: "directx-raytracing-notes"
summary: "记录 DXR 着色器、TLAS 与 BLAS、光线追踪管线，以及资源描述结构在 CPU 与 GPU 之间的作用。"
categories: ["DirectX 12"]
tags: ["DirectX 12", "DX12", "DXR", "Ray Tracing", "Acceleration Structure"]
date: "2026-03-01T13:52:00.000Z"
lastmod: "2026-03-07T03:13:56.000Z"
draft: false
yuque_slug: "rk3k1k9ql8uytqkh"
source: "https://www.yuque.com/u62694975/iaaa/rk3k1k9ql8uytqkh"
---

<a id="ua75cee01"></a>DXR的五种着色器

<a id="ud5d7a87e"></a><a id="u504be805"></a><img src="/images/directx-raytracing-notes/directx-raytracing-notes-01.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="r9Mga"></a>

---

<a id="u95e15a6a"></a><strong>关于TLAS和BLAS：</strong>

<a id="u24c13e11"></a>在 DXR中，我们不再是简单地把顶点丢给管线去画三角形，而是要在三维空间中发射数百万条光线，并计算它们与场景的交点。这是一个极其恐怖的计算量。为了让顶级显卡能在几毫秒内算完，我们必须建立一种极其高效的空间数据结构

<a id="u96d810f8"></a>一种解决方法是，创建包围盒（BV），此时光线只需要对三个对面的交集求交，如果与BV存在交集，则进一步对包含在其中的物体进行求交；反之，如果光线与更大的BV都没有交集，就更不可能与位于其中的物体存在交集。

<a id="u5abf286a"></a>但当场景内的物体变多时，这样的计算速度仍然很低，于是可以采用层次包围盒的方法（BVH），即在多个包围盒形成的集合之外再镶套包围盒，检测原理同上。

<a id="ud1cd1110"></a>但但但但但是，整个场景中只存在一个BVH还是不够，因为这意味着如果场景中的一个物体出现了移动（哪怕只有1mm），整个场景都需要重新计算光照（光线弹射），因此将BVH又分层为TLAS（Top-Level Acceleration Structure）和BLAS（ Bottom-Level   Acceleration Structure）。

<a id="u7a3796e6"></a>其中，BLAS是单个物体在Local Space的BVH，TLAS实质是树，其子节点包含<em><strong>世界变换矩阵</strong></em>与一个指向特定BLAS显存地址的指针                                                                                              |

<a id="uf4b037bd"></a>用于将光线变换至BLAS所在的Local Sapce

<a id="H2Knf"></a>

---

<a id="u8c30189c"></a>构建RTPSO时的三个核心成员<a id="uaaf739fe"></a><img src="/images/directx-raytracing-notes/directx-raytracing-notes-02.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="R1kfv"></a>

---

<a id="u4b0e33c2"></a><strong>关于Desc的一些理解：</strong>

<a id="u0a444581"></a>在现代图形架构下，`DESC`（如 `D3D12_RESOURCE_DESC`）的本质是 <strong>CPU 向 GPU 驱动提交的一份“具备法律效力的显存施工图纸”</strong>。它的作用可以总结为三个维度：

1. <a id="u28b08e11"></a><strong>跨界通信的契约 (Bridge the Async Gap):</strong> 正如你所理解的，GPU 是无法凭空去 CPU 内存里抓取数据的。CPU 是下订单的餐厅经理，GPU 是后厨流水线。`DESC` 就是经理写在点菜单上的详细规格（要几斤肉、切多厚）。这纯粹是 <strong>CPU 端准备数据</strong>的过程，在调用分配 API 之前，GPU 完全不知道它的存在。
2. <a id="u1fb83c68"></a><strong>精准圈地与物理对齐 (Memory Carving):</strong> GPU 显存（VRAM）是高度碎片化且对齐要求极苛刻的。`DESC` 里的宽高、格式、Mip层数，让驱动程序能够精确计算出需要划拨多少字节的物理显存，并安排最优的底层存储布局（Swizzle Pattern）。
3. <a id="u62a4dd7e"></a><strong>权限与管线绑定声明 (Capability Locking):</strong> 我们说过，<strong>Root Signature (根签名)</strong> 是 C++ 函数的参数列表。那么，`DESC` 里的 `Flags` 字段，就决定了这个资源未来能不能作为实参传给特定的函数！如果你没在 `DESC` 里声明 `ALLOW_RENDER_TARGET`，哪怕这块内存再大，它也永远不能挂载到渲染管线的输出端。

<a id="jNXhX"></a>

---

<a id="u05d252c0"></a>CBV，SRV，UAV等等都是什么东西：<a id="u5de9a87f"></a><img src="/images/directx-raytracing-notes/directx-raytracing-notes-03.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="WkEwj"></a>

---

<a id="uc287837d"></a><strong>SBT（Shader Binding Stable）：</strong>

<a id="u42bdecbc"></a>不同于光栅化，在DXR中，CPU无法预知光线会打到哪里，因此，现在我的理解就是，

<a id="ue56d0781"></a><strong>SBT的作用</strong>是：因为CPU无法预知光线会打在哪个材质的表面，因此需要提前写好SBT，用于所击中的片元的渲染，比如当光线击中玻璃材质时，就调用CHS和AHS，当什么也没有击中时，调用MS；

<a id="ua41229d4"></a>也就是说，现在渲染的主体是一束光线，我们跟着光线的路径去渲染片元，而不是像光栅化的时候那样，逐物体的去进行渲染

<a id="WPnaI"></a>

---

<a id="uf158f9be"></a><strong>RayGen着色器的payload：</strong>

<a id="uc5ab5be5"></a>Payload 是一个完全驻留在 GPU 极速寄存器中的‘轻量级通信穿梭机’。它只负责在 DXR 异步遍历加速结构（BVH）时，收集并带回最核心的‘交点上下文（如实例 ID 和重心坐标）’或‘布尔状态（如阴影遮挡）’，从而将高延迟的‘显存读取（采样纹理、读取法线）’和‘重度光照计算’推迟并集中到 RayGen 着色器中执行，以保证 GPU 拥有最高的并行吞吐率（Occupancy）。    
<a id="u33eb8e51"></a><img src="/images/directx-raytracing-notes/directx-raytracing-notes-04.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="sG2Tg"></a>

---

<a id="u44de81ae"></a><strong>HitGroup的组成与作用：</strong><a id="u138017e2"></a><img src="/images/directx-raytracing-notes/directx-raytracing-notes-05.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="uTNAu"></a>

---

<a id="ub8ca7765"></a><strong>Vector的data（）函数的作用：</strong>

<a id="u9d242c7d"></a>`.data()`<strong> 的作用：剥开包装，暴露本质</strong> 如果你直接把 `matrices` 传给 `memcpy`，你拷贝的只是 `std::vector` 内部的那三个管理指针，传到 GPU 里全是垃圾数据，直接导致画面崩溃。

<a id="ud7a5b8ca"></a>`.data()`<strong> 方法的作用，就是向 </strong>`std::vector`<strong> 索要它内部那块</strong><strong>连续内存的起始原生指针 (Raw Pointer)</strong><strong>。</strong>

- <a id="ud71f5a7d"></a><strong>比喻：</strong>`std::vector`<strong> 就像是一艘高度现代化的集装箱货轮（有船长、航海日志、容量信息）。</strong>`memcpy`<strong> 是码头上的巨型起重机，它只负责吊装里面的货物（数据）。</strong>`.data()`<strong> 就是打开货舱盖，直接把第一个集装箱的挂钩交到起重机手里。</strong>

<a id="dWHo8"></a>

---

<a id="uc75d08ef"></a><strong>Register的四个槽位：</strong>

<a id="u8b4b506b"></a><strong>b:  体积小、更新频率高、所有线程共享的只读常量数据  </strong>

<a id="ue7e9e7ba"></a><strong>t:  只读的内存资源  (DXR的AS也在这个槽位）</strong>

<a id="udd09a1e0"></a><strong>s:  采样器  </strong>

<a id="ua32aec98"></a><strong>u: 允许 GPU 随意读写的资源  </strong>

<a id="u2107c0ea"></a><a id="u1e1a1681"></a><img src="/images/directx-raytracing-notes/directx-raytracing-notes-06.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="p65Ee"></a>

---

<a id="u998e0c70"></a><strong>基础：根签名与描述符：</strong>

<a id="u4edd13e3"></a><strong>根签名</strong>——相当于一张说明书，告诉了GPU每个槽位应该装些什么（slot1，slot2....)，它本身不包含任何资源

<a id="u34f3ee25"></a><strong>描述符</strong>——对送往GPU的资源进行描述的轻量级结构，既包含实际的资源，同时也包含如何使用该资源的描述

原文：[DXR](<https://www.yuque.com/u62694975/iaaa/rk3k1k9ql8uytqkh>)
