---
title: "Rendering Paths"
date: 2026-06-23
author: "槐aaaa"
archiveGroup: "graphics"
summary: "整理前向渲染、延迟渲染、Tile-Based Rendering 和 Tile-Based Deferred Rendering 的基本思路与优缺点。"
---

## 前向渲染（Forward Rendering）

前向渲染走的是**传统的光栅化渲染管线**：

> 应用阶段 -> 几何阶段 -> 光栅化阶段 -> 像素处理阶段

也就是说，对于每一个物体，都需要对每一个光源进行一次计算，伪代码如下：

```cpp
for each object
{
    // 1. 几何阶段：顶点着色器处理物体的顶点
    vertexShader(object);

    for each primitive of the object
    {
        // 2. 光栅化：把三角形打散成一个个片段（fragments）
        fragments = rasterize(primitive);

        for each fragment in fragments
        {
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
            }
            else
            {
                discard;
            }
        }
    }
}
```

**好处**：天然支持 MSAA 以及透明物体渲染，不需要额外的 pass 或 G-Buffer，节省显存带宽。

**缺点**：

1. 如果场景中**存在大量光源与大量物体**，循环会被执行非常多次，复杂度可以粗略记为 **O(n * m)**，其中 `n` 是物体数量，`m` 是光源数量。
2. 由于深度测试通常发生在片元着色器之后，可能产生严重的 **Overdraw**。也就是说，一个像素会被绘制多次。如果 `pixelShader` 的计算量较大，比如包含复杂 BSDF 计算，就会造成明显的性能浪费。

## 延迟渲染（Deferred Rendering）

**核心思想是：先确定可见性，再进行光照计算。**

### G-Buffer

延迟渲染得以实现的基础是 **G-Buffer（Geometry Buffer，几何缓冲）**。在实际图形 API 中，G-Buffer 往往不是一张单一的超大纹理，而是通过 GPU 的 **MRT（Multi-Render Target，多渲染目标）** 技术，在一个 pass 里将不同信息写入多张 render target。

一种常见布局如下：

| Render Target | Format | R 通道 | G 通道 | B 通道 | A 通道 |
| --- | --- | --- | --- | --- | --- |
| RT0（Scene Color） | `RGBA8` | Albedo.r | Albedo.g | Albedo.b | Material ID |
| RT1（Normal） | `RGBA8` / `RGBA16F` | Normal.x | Normal.y | Normal.z | 间接光倍率 / 其它 |
| RT2（Metallic / Roughness） | `RGBA8` | Metallic | Roughness | AO | Shading Model |
| RT3（Velocity / Custom） | `RGBA8` | Emissive 或 Motion Vector，用于 TAA、动态模糊等 |  |  |  |
| Depth-Stencil Buffer | `D24S8` / `D32F` | Depth，由硬件深度缓冲区直接记录，不占用 MRT 的 RT 槽位 |  |  |  |

所有 RT 合起来组成 G-Buffer。相应地，更多 RT 意味着需要更高的显存带宽，这也是延迟渲染的主要**性能瓶颈**之一。

### 延迟渲染的过程

不同于前向渲染通常只有一个主要 pass，延迟渲染一般分为两个 pass：

1. **Geometry Pass**：填充 G-Buffer。
2. **Lighting Pass**：读取 G-Buffer 并执行光照计算。

#### Geometry Pass

几何阶段不进行光照计算，而是遍历场景中的每一个物体，并执行深度测试。确定最终呈现在屏幕上的像素之后，再在 Pixel Shader 中将该像素的信息写入对应的 RT。

> MRT：多重渲染目标技术，使得我们可以在一个 pass 中将所需信息写入多张 RT，而不是使用多个 pass，每个 pass 只写一张 RT。

#### Lighting Pass

此时几何信息已经全部写入 G-Buffer，所以只需要在屏幕空间根据 G-Buffer 进行光照计算。因为我们拿到的是最终可见像素的信息，所以不会再出现“同一个像素被反复执行复杂光照计算”的情况，可以大幅减少 Overdraw 带来的浪费。

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
            writeGBuffer(fragment);
        }
    }
}

// ==================== 2. 光照阶段 ====================
// 绘制一个覆盖全屏幕的巨型三角形或矩形
for each pixel on screen
{
    // 采样 G-Buffer 得到该像素的真实物理属性
    sampleGBuffer(pixel);

    // 核心：在这里才遍历光源，没有重复 shading 的浪费
    for each light in scene
    {
        pixelShader(pixel, light);
    }
}
```

**好处**：

1. 有效规避 Forward Rendering 的 **Overdraw** 问题，大幅减少重复 shading。
2. 对于多光源场景，Forward Rendering 必须在 Pixel Shader 中对每个片段遍历光源；Deferred Rendering 在第一个 pass 中已经拿到了几何信息，所以随着光源数量上升，复杂度更接近屏幕像素数量与光源数量的关系，可以粗略记为 **O(r * m)**，其中 `r` 是屏幕分辨率，`m` 是光源数量。

**缺点**：

1. **不天然支持 MSAA**：MSAA 的核心是记录子像素覆盖信息，而普通 G-Buffer 只保存每个像素的一份几何属性。如果要在延迟渲染中实现 MSAA，需要按照 MSAA 倍率额外存储更多 G-Buffer 数据。例如 4x MSAA 需要接近 4 倍的 G-Buffer 存储，显存带宽压力会明显上升。
2. **不适合半透明物体**：G-Buffer 的每个像素通常只能存储一个表面的信息，而半透明物体可能需要多个表面参与混合。常见做法是先对不透明物体执行延迟渲染，再对透明物体补一遍前向渲染。
3. **带宽占用高**：Geometry Pass 需要写入大量 G-Buffer 数据，Lighting Pass 又需要读取这些数据，对显存与显存带宽都有较高要求。

## 基于瓦片的渲染（Tile-Based Rendering，TBR）

前向渲染与延迟渲染都可以落在 **IMR（Immediate Mode Rendering，立即模式渲染）** 的范畴里。它的基本工作方式可以理解为：

> 拿到三角形 -> 顶点着色器 -> 光栅化 -> 片元着色器 -> 读写 VRAM

也就是说，**IMR 的策略**是：拿到三角形就直接丢进显存相关流程里进行渲染。桌面 GPU 通常有独立显存和较高带宽，所以可以承受这种读写方式。

移动端则不同。手机通常没有独立显存，CPU 和 GPU 需要共享系统内存，同时内存带宽也更受限制。如果仍然像桌面端那样频繁读写显存，就很容易遇到带宽瓶颈，并带来发热和耗电问题。

**TBR 的策略**是将屏幕画面划分成一个个 tile，比如 `16 x 16` 的小块，然后按 tile 进行渲染，以减少外部内存读写。

虽然移动端 GPU 没有独立显存，但 GPU 内部仍然有高速缓存或片上存储。只要能让一个 tile 内的计算尽量在片上完成，就可以省下大量带宽。这也是 **TBR 的核心思想**。

### 具体步骤

#### 几何阶段

GPU 拿到几何体信息后，先执行顶点着色器，得到顶点的屏幕空间位置，并将图元归类到不同的 tile。

#### 像素阶段

当一帧的 tile 划分完成后，GPU 再执行光栅化与片元着色器等后续流程。它会根据片上存储中的信息，将每一个 tile 内部的三角形一次性处理完，然后把计算好的 buffer 写回系统内存。

在这个过程中，Depth Buffer 与 Color Buffer 尽量停留在 GPU 片上存储中，因此可以显著减少外部内存带宽占用。

> 既然 TBR 可以减少带宽占用，为什么桌面端不普遍采用这种方式？

1. **核心瓶颈不同**：桌面 GPU 更强调吞吐量和运行速度，外部显存带宽相对充足；而 TBR 需要对几何进行分块和调度，可能增加额外开销。
2. **几何数量过载**：AAA 游戏中一帧可能有大量几何。如果在 GPU 端对这些几何逐个分块记录，不仅需要额外存储空间，也可能导致渲染流水线等待。
3. **不适合高度无序的渲染工作负载**：例如 Compute Shader、GPU Culling、Ray Tracing 等任务可能需要跨 tile 随机访问数据。遇到这种情况时，TBR 可能需要频繁把片上数据刷回外部内存，削弱原本的优势。

## 基于瓦片的延迟渲染（Tile-Based Deferred Rendering，TBDR）

相对前面提到的延迟渲染，TBDR 更像是移动端 GPU 在硬件层面提供的一套能力。它通常会结合一个硬件剔除单元：**HSR（Hidden Surface Removal，隐面剔除）**。

### 具体步骤

#### 几何与分块

这一步与 TBR 基本一致：CPU 发来绘制命令，GPU 执行 VS，并将三角形分块存储。

#### 光栅化与 HSR 测试

在每一个 tile 中，硬件会对三角形进行光栅化。之后它不会立刻执行片元着色器，而是先由 HSR 执行深度测试和隐藏面剔除。

#### 执行片元着色器并写回

此时，**片上高速缓存（On-Chip Buffer）**里留下的通常是最终可见的那层像素。GPU 再对这些像素执行光照计算，最后将计算完毕的像素一次性写回系统内存。

**优点**：由于 HSR 在硬件层面提前执行深度剔除，因此可以显著减少 Overdraw。

**缺点**：对 Alpha Test 不友好。一旦遇到 Alpha Test 物体，TBDR 的 HSR 流水线可能被强行打断。硬件需要等待 Pixel Shader 的结果，或者把已经处理好的数据刷回内存，这会导致 TBDR 的优势下降，甚至退化得比普通 TBR 更慢。

## 小结

这里粗略整理了桌面端与移动端常见的几类渲染路径。实际引擎中还会在这些基础路径上继续组合出 Forward+、Clustered Forward、Tile-Based Deferred 等更多变体。理解这些路径的关键，是先区分它们分别在解决什么瓶颈：是减少重复 shading、降低显存带宽，还是更好地组织大量光源和几何。

## Reference

- [移动端 GPU 架构知识汇总](https://zhuanlan.zhihu.com/p/381682257)
- [移动 GPU 渲染架构介绍](https://zhuanlan.zhihu.com/p/259760974)
