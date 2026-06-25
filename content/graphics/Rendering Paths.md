---
title: "Rendering Paths"
date: 2026-06-25
author: "槐aaaa"
archiveGroup: "graphics"
---

## 前向渲染（Forward Rendering）

前向渲染走的就是**传统的光栅化渲染管线**：<u>应用阶段 -> 几何阶段 -> 光栅化阶段 -> 像素处理阶段</u>

也就是说，对于每一个物体，都需要对每一个光源进行一次计算，伪代码如下

```cpp
for each object
{
    // 1. 几何阶段：顶点着色器处理物体的顶点
    vertexShader(object); 

    for each primitive of the object
    {
        // 2. 光栅化：把三角形打散成一个个像素点（Fragments）
        fragments = rasterize(primitive); 

        for each fragment in fragments
        {
            // 初始化最终的像素颜色
            float4 finalColor = ambient; 

            // 3. 核心：前向渲染会对每个片段遍历所有光源
            for each light
            {
                finalColor += pixelShader(fragment, light);
            }

            // 4. 逐片段操作：深度测试与写入
            if (depthTest passed)
            {
                writeToColorBuffer(fragment.screenX, fragment.screenY, finalColor);
                writeToDepthBuffer(fragment.screenX, fragment.screenY, fragment.depth);
            } else
            {
                discard; // 深度测试失败，丢弃
            }
        }
    }
}
```

**好处**：天然支持 MSAA 以及透明物体的渲染，不需要额外的 Pass 或者 G-Buffer，节省带宽

**缺点**：

1. 从伪代码中就可以看出，如果场景中**存在大量光源与大量物体**，循环就会被执行非常多次，其复杂度为 **O(n * m)**，其中 n 是物体数量，m 是光源数量
2. 由于深度测试位于片元着色器之后，所以可能会产生非常严重的 **OverDraw**，即一个像素被绘制多次，这在 pixelShader 的计算量偏大的情况下（比如 **BSDF** 的计算）是不可接受的——产生了非常严重的**性能浪费**

## 延迟渲染（Deferred Rendering）

**核心思想是：****<u>先确定可见性，再进行光照计算</u>**

### G-Buffer

延迟渲染得以实现的基础是 **G-Buffer（几何缓冲）**，在实际的图形 API 中 G-Buffer往往不是一张单一的超大纹理，而是通过 GPU 的 **MRT（Multi-Render Target）**技术，在一个 Pass 里将不同的信息（比如 Albedo、Normal......）写入**多张 RT** 中，一种常见的布局如下：

| **Render Target** | **Format** | **R 通道 (8 bit)** | **G 通道 (8 bit)** | **B 通道 (8 bit)** | **A 通道 (8 bit)** |
| --- | --- | --- | --- | --- | --- |
| **RT0 (Scene Color)** | `RGBA8` | 固有色 (Albedo.r) | 固有色 (Albedo.g) | 固有色 (Albedo.b) | 材质 ID (Material ID) |
| **RT1 (Normal)** | `RGBA8`<br/> 或 `RGBA16F` | 法线X(Normal.x) | 法线 Y(Normal.y) | 法线 Z(Normal.z) | 间接光倍率 / 其它 |
| **RT2 (Metallic/Roughness)** | `RGBA8` | 金属度(Metallic) | 粗糙度 (Roughness) | 环境光遮蔽 (AO) | 阴影遮蔽 (Shading Model) |
| **RT3 (Velocity/Custom)** | `RGBA8` | 自发光 (Emissive) 或 屏幕空间速度矢量 (Motion Vector)，用于 TAA 抗锯齿和动态模糊 |  | | |
| **Depth-Stencil Buffer** | `D24S8`<br/> / `D32F` | **深度值 (Depth)**：不占用 MRT 的 RT 槽位，是由硬件深度缓冲区直接记录的。 | | | |

所有的 RT 合起来组成 G-Buffer，相应地，更多的 RT 意味着需要更高的显存带宽，这也是延迟渲染的主要**性能瓶颈**之一

### 延迟渲染的过程

不同于前向渲染的单 Pass（通常情况下只有一个 Pass），延迟渲染使用到了两个Pass，分别是 Geometry Pass 和 Light Pass。前者负责填充 G-Buffer，后者负责执行着色

#### Geometry Pass ：

几何阶段不进行任何光照计算，而是遍历场景中的每一个物体，并执行深度测试，确定了最终呈现在平面上的像素之后，再在 Pixel Shader 中将这个像素的信息逐个填入对应的 RT 中

> MRT：多重渲染目标技术，使得我们可以在一个 Pass 中就将所需的所有信息写入多张 RT 中，而不是使用多个 Pass，每个 Pass 只写一张 RT
>

#### Light Pass：

此时几何信息已经全都被我们拿到了，所以只需要在屏幕空间无脑地根据 G-Buffer 进行计算即可；同时也正因为我们拿到的都是最后一定会呈现在屏幕上的像素的信息，所以完全不会出现“一个像素被绘制多次”的情况，大大减少了 OverDraw

伪代码如下：

```cpp
// ==================== 1. 几何阶段 ====================
for each object in scene
{
    for each fragment of object
    {
        if (depthTest passed)
        {
            // 不计算光照，只填充几何属性
            writeRT;
        }
    }
}

// ==================== 2. 光照阶段 ====================
// 绘制一个覆盖全屏幕的巨型三角形或矩形
for each pixel on screen
{
    // 采样 G-Buffer 得到该像素的真实物理属性
    sample G-Buffer;
    // 核心：在这里才遍历光源，没有 Overdraw 浪费
    for each light in scene
    {
        pixelShader
    }
}
```

**好处**：

1. 有效规避了 Forward Rendeirng 的 **OverDraw** 现象，大大提高了性能；
2. 针对多光源场景，Forward Rendeirng 必须在 Pixel Shader 中一个一个地进行遍历，而 Deferred Rendering 由于第一个 Pass 已经拿到了所有的几何信息，所以随着光源数量的上升，复杂度只会呈**线性增加**，而非与物体数量相关联——此时复杂度为 **O(r * m)**，其中 r 为屏幕分辨率，m 为光源数量

**缺点**：

1. **不支持 MSAA**：MSAA 的核心是在 Pixel Shader 中将片元所覆盖的像素进行划分，再根据所覆盖的子像素与所有子像素的比例决定“柔化系数”。但是在 Deferred Rendering 中，光栅化与 Pixel Shader 位于两个不同的 Pass 中，Pixel shader 能拿到的只有上一个 Pass 传下来的信息，即 G-Buffer 纹理中每个像素对应的标量 / 向量信息，而对于“片元覆盖了多少子像素”这类信息，G-Buffer 中并没有记录。但也并不是说延迟渲染中完全不能实现 MSAA，只是如果这样做的话，需要根据 MSAA 的倍率额外存储更多的 RT（以 4x MSAA 为例，需要用 4 倍的 G-Buffer 尺寸来存储子像素），而这会导致显存带宽的崩溃
2. **不支持半透明物体**：G-Buffer 的每一个像素只能存储一个表面的信息，而对于半透明物体，一个像素可能需要用到多个表面的信息。解决方法是先对不透明物体进行一次延迟渲染，然后再对透明物体补一次前向渲染
3. **带宽占用极高**：Geometry Pass 需要写入大量信息进入 G-Buffer，Light Pass 又需要读出这些巨量信息，这对显存以及显存的带宽是极大的负担

## 基于瓦片的渲染（Tile-Based Rendering，TBR）

前两种渲染路径都属于 **IMR（Immediate Mode Rendering，立即模式渲染）** 的范畴，它的运作方式是：

**拿到三角形 -> 顶点着色器 -> 光栅化 -> 片元着色器 <-> 读写 VRAM**

也就是说，**IMR 的策略**是<u>拿到三角形就直接丢进显存进行渲染</u>，完全不管这会占用多少带宽。而之所以可以这么做，完全是因为桌面端的 GPU 性能支持这种力大砖飞的方法——拥有独立显存，同时总线功耗极高，动辄就是上百瓦，完全不怕疯狂读取显存

但是移动端就完全不一样了，手机上没有独立的显存，CPU 与 GPU 需要共享一块系统内存，同时这块内存的带宽也极低，如果还是像桌面端那样频繁的进行读取操作，手机就会因为带宽堵塞而发烫，很快就会没电

**TBR 的策略**则是将屏幕画面划分为一块一块的 tile（比如 16 x 16 的块），然后对整个 tile 进行渲染，以达到节省带宽的目的（因为一次将多个三角形打包进入显卡）

虽然移动端的 GPU 没有独立的显存，但是 GPU 上还是存在着一块<u>高速的 L1、L2 缓存</u>，因此如果可以将所有计算都一次性在这片内存上完成，就可以省下大笔带宽，这也是 **TBR 的核心思想**

### 具体步骤

#### 几何阶段：

GPU 拿到几何体信息后，先执行顶点着色器，得到顶点的物理位置，并将其归类进不同的 tile

#### 像素阶段：

当一帧结束，此时 GPU 必须要进行渲染了，它才会执行光栅化与片元着色器等后续流程，根据高速缓存中存储的信息，将每一个 tile 内部的三角形一次性画完，然后将计算好的 Buffer 写回系统内存。在此过程中，由于 Depth-Buffer 与 Color-Buffer 始终没有离开过 GPU，因此完全不存在带宽的高占用情况

> 既然 TBR 可以减少带宽占用，为什么桌面端不采用这种方式？
>

1. **核心瓶颈不同**：桌面端 GPU 不在乎这些带宽的占用，因为性能高到完全足以应付，桌面端注重的是极致的吞吐量与运行速度，而 TBR 需要等待每一帧刷新之后才执行光照计算，效率不如 IMR
2. **几何数量过载**：3A 游戏中，每一帧动辄就是成百上千万的面数，如果在 GPU 端对这些几何体一一记载的话，不仅显存空间不够，还会导致渲染流水线的断层，即 GPU 必须先把海量的顶点进行归类之后，才能继续进行下一步的计算
3. **无法用于无序渲染**：诸如 Compute Shader、GPU Culling、Ray-Tracing 都是完全无序的、动态的，或者需要随机访问全场景的。而 TBR 一旦遇到这种需要跨 tile 访问的情况，就要将已经处理好的数据重新刷新会显存，导致 TBR 的优势荡然无存

## 基于瓦片的延迟渲染（Tile-Based Deferred Rendering，TBDR）

相对于前面说过的延迟渲染，TBDR 属于移动端 GPU 自带的硬件层面的能力，它的内部增加了一个强悍的硬件剔除单元——**HSR（Hidden Surface Removal，隐面剔除）**

### **具体步骤**

#### 几何与分块：

这一步与 TBR 完全一致，CPU 发来绘制命令，GPU 执行 VS 并将三角形分块存储

#### 光栅化与 HSR 测试：

在每一个 tile 中，硬件会对每一个三角形进行光栅化，之后不是直接执行片元着色器，而是**由 HSR 进行深度测试**

#### 执行片元着色器并写回：

此时，**片上高速缓存（On-Chip Buffer）**里留下的，一定是最终能被眼睛看到的、唯一的那层像素，接着 GPU 才会对这些像素执行光照计算。最后将所有计算完毕的像素，一次性打包回系统内存

优点：由于 HSR 在硬件层面的深度测试，因此基本不存在 OverDraw 的情况

缺点：Alpha Test 不友好，一旦遇到 Alpha Test 的物体，TBDR 会被迫**强行打断 HSR 流水线**。硬件必须停下来，先把这个草叶物体之前的所有东西画像素、刷新深度，或者挂起等待 Pixel Shader 执行完返回结果。这就导致 TBDR 瞬间退化，甚至比普通 TBR 还要慢  

## 小结

这里只是泛泛地谈了下移动端与桌面端常见的渲染策略，以这些方法为主流还可以拓展出更多更加优秀的渲染路径，不过就这样吧，下面引用的文章中已经有了详细的记载，不知道的直接去查即可

**【Reference】**

[**https://zhuanlan.zhihu.com/p/381682257**](https://zhuanlan.zhihu.com/p/381682257)

[**https://zhuanlan.zhihu.com/p/259760974**](https://zhuanlan.zhihu.com/p/259760974)
