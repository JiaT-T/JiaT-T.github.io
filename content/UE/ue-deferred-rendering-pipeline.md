---
title: "UE 渲染管线（桌面端延迟渲染）"
slug: "ue-deferred-rendering-pipeline"
summary: "按场景准备、可见性筛选、几何缓冲、材质、光照与后处理梳理 UE 桌面端延迟渲染流程。"
categories: ["Unreal Engine"]
tags: ["Unreal Engine", "Rendering", "Deferred Rendering", "Culling"]
date: "2026-06-17T08:36:07.000Z"
lastmod: "2026-06-28T06:45:53.000Z"
draft: false
yuque_slug: "ozbxcaz6quwou5ur"
source: "https://www.yuque.com/u62694975/iaaa/ozbxcaz6quwou5ur"
---

<a id="u5c9de86f"></a>官方文档中的流程图如下：

<a id="u302d1836"></a><a id="u5d65deff"></a><img src="/images/ue-deferred-rendering-pipeline/ue-deferred-rendering-pipeline-01.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="uad67fad9"></a>因为步骤比较多，涉及到的源文件也非常繁杂，所以此处仅仅只是梳理一遍大概的渲染流程；之后我想我会更加具体地深入某一阶段的源码进行学习......

<a id="d5Tfo"></a>
## 1. 场景准备与遮蔽

<a id="u5c1f6580"></a><strong>核心</strong>：决定<strong>“</strong><strong><u>什么东西要画，什么东西不要画</u></strong><strong>”</strong>

<a id="u609f0c51"></a>在现代引擎的架构下，进行绘制操作时，性能的瓶颈往往不是着色器本身，而是 CPU 与 GPU 之间的高频通信，更具体地说是 CPU 向 GPU 提交的一个个 <strong>Draw Call</strong>（绘制指令）。我们都知道，CPU 想要将信息传递到 GPU，需要跨过一条漫长的 PCIE 总线，这一过程是极其耗费时间的（相对于 GPU 高速的绘制操作来说）

<a id="u6ebe76fa"></a>因此，<strong>提前筛选出最终可能会用到的信息</strong>是非常关键的

<a id="OKVUi"></a>
### 步骤

<a id="ua344e354"></a>具体操作由 CPU 的两个线程(抽象意义上的线程）来执行 —— <strong>游戏线程</strong> 与<strong> 绘制线程</strong>

<a id="fM3l6"></a>
#### 游戏线程

1. <a id="u16443a59"></a>处理<strong>动画</strong>、<strong>物理模拟</strong>、<strong>AI</strong>......
2. <a id="u698840df"></a><strong>遍历场景树</strong>，收集所有挂载着渲染组件的物体（如 StaticMesh、Skeletal Mesh......）
3. <a id="ue0c62e42"></a>计算每个物体的<strong>世界矩阵</strong>，并将数据打包

<a id="u44e499a5"></a>之后 UE 会将需要渲染的物体同步给绘制线程

<a id="ar7h4"></a>
#### 绘制线程

<a id="ud58d2526"></a>这一步主要执行<strong>剔除工作</strong>

1. <a id="uc99d6dd8"></a><strong>距离剔除</strong>

<a id="uace5ad97"></a>根据事先设定好的“<strong>最大绘制距离</strong>”将超出这个阈值的物体直接从渲染列表中剔除

<a id="u8fa08a33"></a><strong>应用</strong>：草丛、地上的碎石......

2. <a id="u9d2973e6"></a><strong>视锥剔除</strong>

<a id="u7a2e49e2"></a>场景中的每个可见物体都拥有<strong>包围盒 / 包围球</strong>，这一阶段会将包围盒与视锥体进行快速地<strong>相交测试</strong>，只要包围盒完全位于视锥体之外（比如玩家背面），就会被剔除

3. <a id="ua068d002"></a><strong>遮挡剔除</strong>

<a id="ub8b03ef6"></a>相对于前两步的“暴力删除”操作来说，遮挡剔除会更加复杂与耗时；并且不同于传统渲染管线中的 Depth-Test，UE 使用的是基于<strong> HZB（Hierarchical Z-Buffer，分层深度缓冲）</strong>的遮挡剔除技术

<a id="u67da314b"></a>在传统的 Z-Buffer 中，对于物体在屏幕上的每一个像素，都需要与 Z-Buffer 中对应的像素进行比较，虽然在工程实现上比较容易，但是一旦当物体占据了屏幕上的大量像素比如 500 x 500 个像素点时，那么光是测试这一个物体就需要读取与比较 250000 次深度值，开销极大

<a id="uef71102f"></a>HZB 则借鉴了 <strong>Mipmap </strong>的思想，将原本巨大的深度图进行了降采样分层（每 2 x 2 个像素生成一个新像素，这个新像素的值则为其中最远的像素深度值）

<a id="u1eb73f09"></a>如图，从左至右 Mip 层级分别为 4、5、6

<a id="uf4bc2169"></a><a id="uae364399"></a><figure><img src="/images/ue-deferred-rendering-pipeline/ue-deferred-rendering-pipeline-02.png" alt="https://miketuritzin.com/post/hierarchical-depth-buffers/" loading="lazy" style="max-width: 100%; height: auto"><figcaption>https://miketuritzin.com/post/hierarchical-depth-buffers/</figcaption></figure>

<a id="u53330dae"></a>这样一来，对于<strong>巨型物体</strong>（在屏幕上占据大量像素）使用<strong>低分辨率层级 HZB</strong>，<strong>较小的物体</strong>使用<strong>高分辨率层级 HZB</strong>，从而使得无论物体多大，引擎总能找到一个恰好匹配其大小的 HZB 层级，使得该物体的包围盒在那个层级下，只覆盖<strong>极少数的几个像素</strong>

> <a id="ue2f73f94"></a>
>
> <a id="uf2a399e1"></a>但是这样不会丢失精度吗？

<a id="uf3c1d813"></a>答案是基本不会损失精度。因为上一步仅仅只是决定用什么深度图，还没有进行比较。

<a id="u129f3bff"></a>而在深度比较中，引擎会提取该物体距离摄影机最近的点与 HZB 中的深度值进行比较。而如果<strong>最近的点都比最远的遮挡物还要远</strong>，那么这个物体必不可能被摄影机看到，可以直接丢掉

<a id="QLU2u"></a>
## 2. 几何体渲染

<a id="fViG9"></a>
## 3. 光栅化与几何缓冲

<a id="GpIt5"></a>
## 4. 渲染纹理

<a id="RTm98"></a>
## 5. 像素着色器与材质

<a id="BYQCf"></a>
## 6. 反射

<a id="gKLPB"></a>
## 7. 静态光照与阴影

<a id="dPXyn"></a>
## 8. 动态光照与阴影

<a id="Mb8xv"></a>
## 9. 雾与透明度

<a id="fIdza"></a>
## 10. 后处理效果

<a id="ufb5e0b7a"></a>【Reference】<a id="PDU7u"></a>[https://dev.epicgames.com/documentation/unreal-engine/introduction-to-rendering-in-unreal-engine-for-unity-developers#rendering-in-unreal-engine](<https://dev.epicgames.com/documentation/unreal-engine/introduction-to-rendering-in-unreal-engine-for-unity-developers#rendering-in-unreal-engine>)

原文：[UE 渲染管线（桌面端延迟渲染）](<https://www.yuque.com/u62694975/iaaa/ozbxcaz6quwou5ur>)
