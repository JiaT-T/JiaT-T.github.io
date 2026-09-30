---
title: "GAMES104：引擎架构分层"
slug: "games104-engine-architecture"
summary: "记录资源层、功能层、核心层、平台层与工具层的职责，以及引擎分层和依赖方向。"
categories: ["图形学"]
tags: ["GAMES104", "Game Engine", "Game Architecture", "Resource Management"]
date: "2026-03-25T07:55:05.000Z"
lastmod: "2026-03-25T09:53:46.000Z"
draft: false
yuque_slug: "hlcti7lg4g2b7lp2"
source: "https://www.yuque.com/u62694975/iaaa/hlcti7lg4g2b7lp2"
---

<a id="ued45a183"></a><strong>资源层，平台层，工具层，功能层，核心层........</strong>

<a id="uc7a16d0d"></a><strong><span style="background-color: #FBDE28">资源层</span></strong>：将resource转化成assets，因为在其他DCC软件中（如：maya，3dmax)，他们的文件格式(.max，.maya....)往往是兼容自身软件，其中包含着大量的无用信息，因此，引擎需要将其转换成更加高效的	类型(DDS)。

<a id="uf6f270ac"></a>而在Resource Layer中，每个资源都会有一个独特的GUID（Globally Unique Identifier，全局唯一标识符），勇于查找该对象并使用。即使文件的路径发生了改变，也可以通过GUID识别到需要使用的文件

<a id="u8d798127"></a>这一层也负责资产生命周期的管理，不同的资源有着不同的生命周期，而有限的内存要求我们及时释放不需要的资源，主要的方法有Garbage Collection（GC）和Deferred Loading

<a id="uf17f752e"></a><strong><span style="background-color: #FBDE28">功能层</span></strong>：物理，渲染，动画等等功能的实现

<a id="ua3c314ac"></a>e.g.Tick（）函数：分为TickLogic（）和TickRender（），分别处理逻辑与渲染计算，要求每帧更新

<a id="ubd95abac"></a>多线程的发展趋势：在过去，CPU只有单核，物理，渲染等等的计算往往只会写在这一条线程上；随着硬件的发展，CPU的核心数量增加，也就使得多个线程可以并行计算（如：一个核心负责动画功能，一个核心则负责物理解算....）；但未来的引擎一定是采用的“Job System”，也就是将单个功能拆解为多个小的job，分散至不同的核心中进行计算，充分利用所有的性能，但是因为牵扯到多个系统的计算先后顺序问题，因此比较复杂

<a id="u345cba1f"></a><strong><span style="background-color: #FBDE28">核心层</span></strong>：顾名思义，引擎中最重要的部分，是整个引擎的基础。

<a id="uafa76af4"></a>因为游戏引擎极度重视效率，像是C++的STL就不能使用（会产生内存空洞），因此我们需要在这一层自定义数据结构，以确保运行的高效性。同时也要求核心层的代码质量高，且不能轻易修改

<a id="ubec60e00"></a><strong><span style="background-color: #FBDE28">平台层</span></strong>：在不同的平台上（Windows，Mac....），文件路径，图形API，硬件架构等都可能有很大差异，因此引擎还需要对这些不同的平台进行不同的处理

<a id="u42858f32"></a><strong><span style="background-color: #FBDE28">工具层</span></strong>：需要允许别人能够创建游戏内容，开发方式灵活，有时候代码量可能会比整个引擎还大

<a id="u904aa64c"></a>外部的DCC工具（3DMAX，MAYA，Houdini等）也属于这一层

<a id="qw1Qf"></a>
### 为什么要进行分层？

<a id="u462ba948"></a>游戏引擎非常复杂，进行分层可以解耦与降低复杂度，

<a id="u97ce2a00"></a><a id="u1c4d7444"></a><img src="/images/games104-engine-architecture/games104-engine-architecture-01.png" alt="" loading="lazy" width="314" height="267" style="max-width: 100%; height: auto">

<a id="ue1552c00"></a>如图，越向上越灵活，越往下越稳定

<a id="u1ed8e586"></a>一般来说，只允许上层调用下层的功能，而禁止下层调用上层的功能

原文：[引擎架构分层](<https://www.yuque.com/u62694975/iaaa/hlcti7lg4g2b7lp2>)
