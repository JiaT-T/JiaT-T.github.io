---
title: "GAMES104：渲染实践"
slug: "games104-rendering-practice"
summary: "整理 GPU 执行架构、渲染资源组织、可见性裁剪、纹理压缩与 Cluster/Nanite 模型管线。"
categories: ["图形学"]
tags: ["Computer Graphics", "GAMES104", "Rendering", "GPU", "Culling", "Nanite"]
date: "2026-06-09T10:32:42.000Z"
lastmod: "2026-06-09T12:38:02.000Z"
draft: false
yuque_slug: "wx6sx5vc0lk8i525"
source: "https://www.yuque.com/u62694975/iaaa/wx6sx5vc0lk8i525"
math: true
---

<a id="VYDtO"></a>
## 一：游戏渲染中的挑战

1. <a id="u10efacb3"></a>游戏画面中可能有成千上万种效果需要绘制，非常复杂
2. <a id="uaa9ec657"></a>引擎必须要深度适配现代的硬件
3. <a id="u009ee98a"></a>需要保持每一秒帧数的稳定
4. <a id="u8bae22be"></a>对 CPU 的占用不能过高，需要保留算力供其他模块调用

<a id="soHcT"></a>
## 二：了解 GPU

<a id="VIl1z"></a>
### 1. SIMD（Single Instruction Multiple Data) 与 SIMT（Single Instruction Multiple Threads)

<ol data-yuque-indent="1" style="margin-left: 2em"><li id="ucf3702c6"><strong><span id="u45801644">SIMD（单指令多数据流）</span></strong><span id="u2e96d7e9">：将多个相同通道的数据打包进入一个超大的寄存器，仅调用一条指令，让一个算术逻辑单元  （ALU）对这些数据执行相同操作</span></li><li id="ue582793f"><strong><span id="u682d4aac">SIMT（单指令多线程）</span></strong><span id="u85756342">：将大量独立线程组织成逻辑组，并行的对数据进行处理</span></li></ol>

<a id="ufbb9d825"></a><a id="ub71e4730"></a><img src="/images/games104-rendering-practice/games104-rendering-practice-01.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="TZAQP"></a>
### 2. GPU 架构

<ol start="3" data-yuque-indent="1" style="margin-left: 2em"><li id="u4f5e8f30"><span id="u60ae0653">GPC（Graphics Processing Cluster）</span></li><li id="u934af524"><span id="ua080b37f">SM（Streaming Multiprocessor）</span></li><li id="u1d63faae"><span id="u51b977a3">Texture Units</span></li><li id="uaca12b02"><span id="ua6d1d18d">CUDA Core</span></li><li id="ud4aebba4"><span id="u288979de">Warp</span></li></ol>

<a id="u918dfcda"></a><a id="u6b0ec4de"></a><img src="/images/games104-rendering-practice/games104-rendering-practice-02.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="IDLtY"></a>
### 3. CPU 与 GPU 之间的数据流动

<a id="u7e0163a7"></a>在游戏引擎中有一个原则：尽可能只<strong>让数据单向传输</strong>，即只让数据从 CPU 传入 GPU，而不从 GPU 中读取数据并传输到 CPU

<a id="u253995a1"></a>同时要利用好 Cache 的作用——因为如果 CPU 无法在自己的 Cache 中寻找到所需数据的话，就需要去内存寻找，而这会极大拖慢运行速度

<a id="ude67e001"></a><strong>Cache Hit</strong>：CPU 在缓存上找到数据     <strong>Cache Miss</strong>：CPU 无法在缓存上找到数据

<a id="u9ea63ea1"></a><a id="ub820865e"></a><img src="/images/games104-rendering-practice/games104-rendering-practice-03.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="YrbNI"></a>
## 三：可渲染物体

<a id="ub74f816c"></a><strong>组成</strong>：Mesh Primitive、Vertex Buffer 与 Index Buffer、Material、Textures、Shaders

<a id="u772131e8"></a>对于一个 mesh，根据材质的不同，会被切分为多个 submesh；一个 buffer 用来存储一整个 mesh，而每一个 submesh 占其中一小段

<a id="u2a879991"></a>但是如果对于每一个几何体，都开辟一个 buffer 去存储数据，会造成<strong>内存浪费</strong>（比如：多个物体共用一张贴图，但是却开辟了多个内存空间为每个物体单独存储一张相同的贴图）

<a id="u406b832d"></a>解决方法——<strong>Resource Pool</strong>：

<a id="uc6c61782"></a>将 Shader、Texture、Mesh 等数据放入一个 Pool 中，确保资源可以复用

<a id="EfUkx"></a>
## 四：可见性裁剪

<a id="u5996a0e9"></a>通过判断包围体是否位于视锥体中来执行裁剪操作

<a id="ub8a89450"></a>常见的<strong>包围体</strong>：Sphere、AABB、OBB......

<a id="ufda24839"></a><strong>层次视锥剔除</strong>：Quad Tree Culling、BVH......

<a id="u2fd08518"></a>现代游戏中通常存在着大量可动的物体，因此包围结构不仅要能够进行快速地求交，更要能够执行快速地重建，而 BVH 恰好满足这几点，这也是现代游戏引擎中用的最多的算法

<a id="l9sU3"></a>
#### Portal and PVS Data：

<a id="u6d236ee5"></a><strong>Portal（门）与 PVS（预计算可见性集合）都是经典的室内空间剔除技术</strong>，Portal 是在运行时由 CPU 沿着房间之间相连的“门窗”进行递归裁剪，只渲染视野穿过这些孔洞所能看到的区域；而 PVS 则是将世界切成网格，在离线阶段提前烘焙出每个网格点“可能看到”的物体列表，运行时玩家走到哪就直接 <a id="Io3S5"></a>$O(1)$ 查表剔除，不耗费运行时算力。两者皆以结构的封闭性换取极致的渲染性能

<a id="Qqc36"></a>
#### GPU Culling：

<a id="u4f097a30"></a>指的是将原本由 CPU 负责的画面可见性裁剪工作，完全移交给 GPU（通常利用 Compute Shader）来完成的技术。

<a id="u53fd106b"></a>在传统渲染管线中，CPU 需要逐个计算物体的包围盒是否在视野内，然后再向 GPU 发送渲染指令（Draw Call）。当场景中物体达到数十万级别时，CPU 会因庞大的计算量和频繁的提交产生严重的性能瓶颈。

<a id="u6e2c2192"></a>而 <strong>GPU Culling</strong> 颠覆了这一流程：CPU 直接把场景中所有物体的数据一次性打包扔给显存，随后 GPU 利用自身恐怖的并行算力，在微秒级别内瞬间完成数十万物体的视锥体和遮挡测试，直接在显存中生成最终需要渲染的物体列表并自主绘制。

<a id="T67gd"></a>
## 五：纹理压缩

<a id="u69e75046"></a>在游戏引擎中，图片不是以诸如 PNG、JPEG 等格式存在的，因为这些压缩方式并不支持随机访问，并且计算的复杂度非常高

<a id="u67d692dd"></a>实际用到的压缩技术是——<strong>Block Compression</strong>：  
将一张图片分为多个色块（比如 4 x 4），对于每一个色块，只存储其中的像素的最大值与最小值，而其他像素可以认为是这两个像素值插值得到的结果

<a id="u3ace54ea"></a>在 PC 上：有 BC7（modern）、DXTC（old）等

<a id="u15f7e8bb"></a>在移动端上：有 ASTC（modern）、ETC / PVRTC（old）等

<a id="scwYP"></a>
## 六：建模工具

<a id="u88ab4ee1"></a>多边形建模、雕刻、扫描、程序化建模.....

<a id="ZYMA6"></a>
## 七：新的模型管线

<a id="oJxpb"></a>
#### Cluster-Based Mesh Pipeline

<a id="ub34564c6"></a>核心思想是<strong>放弃以“单个三角形”或“整个模型（Mesh）”为单位的传统处理方式，改由将模型切分成固定大小的“网格簇（Cluster）”作为基础计算单元，并完全由 GPU 驱动进行并行渲染。</strong>

<a id="CyfFO"></a>
#### Nanite

<a id="u744a2218"></a>相当于是 Cluster-Based Mesh Pipeline 的更进一步

原文：[渲染实践](<https://www.yuque.com/u62694975/iaaa/wx6sx5vc0lk8i525>)
