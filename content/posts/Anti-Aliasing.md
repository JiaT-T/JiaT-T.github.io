+++
date = '2026-05-22T00:00:00+08:00'
draft = false
title = '抗锯齿技术'
summary = '整理 SSAA、MSAA、FXAA、SMAA、TAA、DLSS/DLAA 以及路径追踪中的抗锯齿思路。'
tags = ['Computer Graphics', 'Rendering', 'Anti-Aliasing', 'Technical Notes']
+++

**【Reference】：**

**SSAA、MSAA：**[**https://www.zhihu.com/question/20236638/answer/44821615**](https://www.zhihu.com/question/20236638/answer/44821615)

**FXAA：**[**https://zhuanlan.zhihu.com/p/431384101**](https://zhuanlan.zhihu.com/p/431384101)

**SMAA：**[**https://zhuanlan.zhihu.com/p/342211163**](https://zhuanlan.zhihu.com/p/342211163)

**TAA：**[**https://zhuanlan.zhihu.com/p/425233743**](https://zhuanlan.zhihu.com/p/425233743)

---

**锯齿产生的原因**：本质是**采样频率不足以还原物体的高频细节**，更通俗一点的说法是”试图用离散的像素去表现连续的物体“

<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1779428749513-148dd1bb-b859-4321-9cc6-0c042ed8ef6a.png" width="953" title="" crop="0,0,1,1" id="uaffc4f63" class="ne-image">

## 一：空间与硬件级的抗锯齿

### 1. 超采样抗锯齿（Super Sample Anti-Aliasing， SSAA）

SSAA 的做法非常暴力：先以原分辨率的 N 倍分辨率对场景进行渲染，然后再通过降采样得到原分辨率的图像（e.g. 以 4x SSAA 为例，欲渲染一张 1024 x 1024 的图像，先以 4096 x 4096 为分辨率渲染一张图像，再将降采样至1024 x 1024）。这在数学上是完美的抗锯齿，但是**光栅化与着色的计算量都会增加 N 倍**，所以基本上不会使用这个方法。

### 2. 多重采样抗锯齿（Multi Sample Anti-Aliasing， MSAA）

MSAA 可以说是 SSAA 的改进版

在光栅化阶段，当判断三角形是否被像素所覆盖时会采样多个覆盖样本（如下图）

<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1779352139875-cae9e2f8-8663-4c92-835d-f5e6d6e64629.png" width="444" title="" crop="0,0,1,1" id="u8b4c21ae" class="ne-image">

之后执行像素着色器的时候，还是只会在像素中央计算一次，但是要**乘以“覆盖样本与总样本数的比值”**（这里为 0.5）

相对于 SSAA，MSAA 的计算量更小，但是 MSAA 也有缺点：**与延迟渲染不兼容**

因为延迟渲染是分为 G-Buffer（几何缓冲区） 和 Lighting 两个 Pass，以 4x MSAA 为例，这意味着如果强行在  Deferred Shading 中使用 MSAA，每个像素都需要额外存储 4 个亚像素样本的数据，这样不仅会使得显存的占用翻 4 倍，还会导致显存带宽的崩溃（在几何阶段写入 4 倍的数据，在光照阶段读出 4 倍的数据）

## 二：后处理抗锯齿

### 1. 快速近似抗锯齿（Fast Approximate Anti-Aliasing， FXAA）

FXAA 将抗锯齿问题降维成 2D 图像的边缘检测与定向模糊问题，使其与渲染管线完全解耦

操作步骤：

1. **提取像素亮度值：**

    1. $Luma = R \times 0.299 + G \times 0.587 + B \times 0.114$

    2. 实际场景中可以直接使用 G 通道进行优化，因为绿色对亮度的贡献最大

2. **对比度检测（边缘检测）：**

    1. 额外采样上、下、左、右四个方向的亮度值，找出最大、最小亮度，并计算的差值（局部对比度）：$ L_{max} - L_{min} $；如果该差值大于等于设定的阈值，就可以认为此像素位于边缘处，需要进行抗锯齿；反之则认为不处于边缘，不参与后续的模糊过程，这里也是 FXAA 高性能的原因（直接舍弃）

3. **确定边缘朝向：**

    1. 对于通过对比度检测的像素，需要再额外采样左上、左下、右上、右下四个角的亮度

    2. 分别计算水平方向与竖直方向上的变化幅度：
```glsl
// 计算水平方向的亮度变化幅度
float Vertical = abs(N + S - 2 * M) * 2 + abs(NE + SE - 2 * E) + abs(NW + SW - 2 * W);
// 计算垂直方向亮度变化幅度
float Horizontal = abs(E + W - 2 * M) * 2 + abs(NE + NW - 2 * N) + abs(SE + SW - 2 * S);
// 判断边界的方向
bool IsHorizontal = Vertical > Horizontal;
// 根据边界方向，先算出后面搜索时的步长
float2 PixelStep = IsHorizontal ? float2(0, _MainTex_TexelSize.y) : float2(_MainTex_TexelSize.x, 0);
```
    3. 再确定正负方向：
```glsl
float Positive = abs((IsHorizontal ? N : E) - M);
float Negative = abs((IsHorizontal ? S : W) - M);
if(Positive < Negative) PixelStep = -PixelStep;
```
4. **沿边缘搜索**

    1. 自定义“最大迭代次数”，**在边缘处通过循环进行搜索**，每次步进时记录当前像素对比度，直到对比度发生显著变化，此时可以认为找到了锯齿的“**端点**”

    2. 通过计算当前像素到两个端点的距离，FXAA 能够推断出当前像素在边缘的位置

5. **混合系数计算：**

    1. 根据下图权重计算像素参与抗锯齿混合的强度
```glsl
float Filter = 2 * (N + E + S + W) + NE + NW + SE + SW;
Filter = Filter / 12;
// 计算出基于亮度的混合系数
Filter = abs(Filter -  M);
Filter = saturate(Filter / Contrast);
// 使输出结果更加平滑
float PixelBlend = smoothstep(0, 1, Filter);
PixelBlend = PixelBlend * PixelBlend;
```
    2. 

<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1779358478026-85d3bdb6-1a23-4a90-a78b-b407350b1d5a.png" width="432" title="" crop="0,0,1,1" id="ZSkky" class="ne-image">

6. **混合：**

    1. 根据步骤 4 计算出的比例，可以得到一个偏移量：
    2. 如果像素靠近边缘中心，偏移量就大；靠近端点，偏移量就小
    3. 将原始的 UV 坐标垂直于边缘方向移动这个偏移量，进行一次双线性插值（Bilinear）采样，得到混合后的最终颜色 

### 2. 亚像素形态学抗锯齿（Subpixel Morphological Anti-Aliasing， SMAA）

FXAA 存在一些局限性：仅仅通过亮度差异暴力地寻找边缘，存在**边缘检测不准**的问题，并且可能导致**图像模糊**

SMAA 通过引入大量预计算内容，对不同边缘类型进行匹配，基本解决了这些问题

核心——**模式匹配算法**：  

SMAA 会**提前计算不同的边缘形态**（如 Z 型，U 型，L 型...），并将**对应的偏移权重**（对应 FXAA 第 6 步）存储在贴图中。之后，在进行渲染时，shader 只需要像查表一样对不同的边缘类型进行判断，从而找到最精确的亚像素偏移

SMAA 通常需要使用三个 Pass：

- **Pass 1：边缘检测**

    - 与 FXAA 类似，通过亮度对边缘进行判断，但是 SMAA 还会额外采样深度或模板信息进行判断

- **Pass 2：权重计算**

    - 将边缘检测结果与模式贴图进行匹配，计算出每个边缘像素需要向哪个方向、移动多少距离

- **Pass 3：混合**

    - 通过 Pass 2 得到的权重信息，对当前像素与邻近像素进行混合

## 三：时间抗锯齿

### TAA（Temporal Anti-Aliasing）

**核心思想：既然增加当前帧的采样太昂贵，就把采样的成本分摊到过去的多帧中**

**操作步骤：**

1. **亚像素投影抖动：**

    1. 在执行完顶点着色器，进行透视除法之前，使用某种**低差异序列**（通常是 [Halton 序列](https://zhida.zhihu.com/search?content_id=182626622&content_type=Article&match_order=1&q=Halton+%E5%BA%8F%E5%88%97&zhida_source=entity)）对透视投影矩阵的【2，0】和【2，1】进行替换，

    2. 目的：即使物体完全静止，每一帧的像素边界也都存在差异，不仅保证 TAA 在物体未运动时也能生效，同时也使得每一帧的边缘基本都不一样，从而实现混合后的抗锯齿效果

2. **拿到运动矢量：**

    1. 因为需要使用过去帧，所以必须知道当前像素在上一帧的哪个位置，也就是说，在渲染 G-Buffer 时，要同时输出一张 **Velocity 贴图**，并且还需要传入**上一帧的世界、投影矩阵**，使用当前的世界坐标反推出像素在屏幕空间中的位移

3. **历史重投影：**

    1. 进入 TAA Pass 之后，需要先**移除像素采样时添加的抖动值**，然后**减去 Motion Vector** 得到上一帧的历史 uv 坐标，最后使用**双线性插值**计算颜色 
```c
// 减去抖动坐标值，得到当前实际的像素中心UV值
uv -= _Jitter;
// 减去Motion值，算出上帧的投影坐标
float2 uvLast = uv - motionVectorBuffer.Sample(point, uv);
//使用双线性模式采样
float3 historyColor = historyBuffer.Sample(linear, uvLast);
```
    2. 但是这一步可能会因为**遮挡关系的变化**而出现错误（e.g. 一个物体在上一帧被其他物体挡住，这一帧因为镜头的移动而出现在屏幕上，此时是无法通过上一帧的信息去对原本被挡住的物体进行平滑的）；因此可以在采样点周围判断深度，取距离镜头最近的点来采样 Motion Vector 的值

4. **历史修正：**

    1. 由于物体在不断运动，随时可能发生遮挡剔除，或是光照发生剧烈变化，此时重投影后拿到的历史帧数据是完全错误的，如果还是直接混合，就会产生“鬼影”

    2. **解决方法——邻域钳制：**

> 核心思想：如果历史帧的像素合法，那么就一定不会偏离当前像素的邻域太远。

        1. **Clamp：**

            1. 以当前像素为中心，采样一个 3x3 的像素矩阵，找出其中颜色的最大值与最小值，作为钳制的范围；此时 C_max 与 C_min 构成了一个 AABB，代表颜色的合法范围

            2. 通过运动矢量得到上一帧的像素颜色值，强行将其限制在 AABB 中： 

            3. float3 ClampedHistory = clamp(HistoryColor, ColorMin, ColorMax);  

        2. 但是 Clamp 可能会导致极其**不自然的颜色断层**，所以可以使用 Clipping

        3. **Clipping：**

            1. 计算得到当前帧的中心像素与上一帧像素的连线，并求得这条线段与 AABB 的交点，将其作为混合结果

## 四：超分辨率抗锯齿

### 1. DLSS (Deep Learning Super Sampling)

TAA 效果的好坏，基本依赖于“历史修正”这一步做得好不好，然而物理世界中的现象有时是无法通过手写代码来建立完美的数学模型的，而 AI 在这里的优势就体现出来了：NVDIA 通过向超大型计算机输入大量超高分辨率的图像作为真值，让一个卷积神经网络（CNN）去学习“如何在运动、遮挡、光影剧变的情况下，完美重构出无锯齿的高清图像" ，其判断精度远高于人为的判断

DLSS 的**核心逻辑**是：低分辨率渲染 -> 神经网络时空重构 -> 高分辨率输出

- **硬件层渲染**：引擎以较低的分辨率（例如 1080p）渲染场景的所有 G-Buffer 和着色。由于分辨率低，光栅化和光线追踪的计算开销暴跌，帧率得以大幅提升

- **亚像素抖动**：与 TAA 相同，低分辨率渲染时相机依然带有微小的亚像素 Jittering

- **硬件加速输入**：将低分辨率的当前帧颜色、深度图、运动矢量以及高分辨率的历史缓冲区一同送入 GPU 专属的 **Tensor Cores（张量核心）**

- **AI 重构**：神经网络利用其庞大的参数，在空间（上下左右）和时间（前后多帧）两个维度同时进行高级插值与过滤，最终输出一张没有锯齿、细节甚至超越原生渲染的图像（例如 4K）

### 2. DLAA（Deep Learning Anti-Aliasing）

DLAA 相当于是去除了”空间放大“操作的 DLSS

**运行机制**：引擎直接以**原生目标分辨率**（如 4K 渲染 + 4K 输出）运行。它把完整的高清当前帧、高清深度、高清速度图送入神经网络。AI 不再需要无中生有地猜测缺失的像素，它所有的算力都被毫无保留地倾注在“如何在时间轴上做到最完美的、绝无鬼影与蠕动的顶级抗锯齿”

**优点**：细节保留更加完整，同时彻底消除了 TAA 的动态模糊感

**代价：**在帧率上可能不如 DLSS

## 五：光线追踪/路径追踪中的抗锯齿

### 抖动采样（Jitter Sampling）

在光线追踪中，通常不需要挂载一个复杂的 TAA Pass，只需要在生成主射线时，对其在屏幕空间中穿过的 uv 坐标添加一个微小的抖动；随着 SPP（ Samples Per Pixel  ）的累加求均值，锯齿会随着噪点一起消失

