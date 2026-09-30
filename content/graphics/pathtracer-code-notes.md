---
title: "Pathtracer 梳理"
slug: "pathtracer-code-notes"
summary: "按路径追踪、几何与 BVH、材质接口、PBR 和 IBL/MIS 梳理个人渲染器的代码职责与工程优化。"
categories: ["图形学"]
tags: ["Computer Graphics", "Path Tracing", "BVH", "PBR", "MIS", "C++"]
date: "2026-06-02T06:16:19.000Z"
lastmod: "2026-06-02T08:17:15.000Z"
draft: false
yuque_slug: "xkyt3prgqt2mnn3g"
source: "https://www.yuque.com/u62694975/iaaa/xkyt3prgqt2mnn3g"
---

<a id="u9b620401"></a>这个项目面试时可以按“基础路径追踪 -&gt; 资产/几何 -&gt; PBR -&gt; IBL/MIS -&gt; 工程性能”的顺序讲。

<a id="uce68ae99"></a><strong>1. 基础路径追踪架构</strong>

<a id="u7fa8d237"></a>核心知识点：Ray、HitRecord、Camera、Material、递归路径追踪讲解：路径追踪的核心是从相机发射射线，找到最近交点，根据材质生成下一条采样射线，递归累积直接光、间接光和自发光。此项目中的实现：`Camera.h:413` 负责 `ray_color()` 递归积分；`Ray.h` 表示射线；`Hittable.h` 用 `HitRecord` 保存交点、法线、材质、UV、TBN 等信息。一句话总结：这个项目的底层是一套标准 CPU 路径追踪框架，核心链路是“相机射线 -&gt; 求交 -&gt; 材质采样 -&gt; 递归估计辐射”。

<a id="u9af950ee"></a><strong>2. 几何与 BVH 加速</strong>

<a id="u1ceaa09d"></a>核心知识点：Sphere、Triangle、Quad、AABB、BVH讲解：路径追踪如果每条光线遍历所有物体，复杂度很高，所以需要用包围盒和 BVH 把求交范围快速缩小。此项目中的实现：`BVH.h:7` 用 `BVH_Node` 递归构建左右子树；`AABB.h` 做包围盒测试；`Triangle.h:95` 还实现了三角形光源采样所需的 `pdf_value()` 和 `random()`。这部分对应早期 [PR #18](<https://github.com/JiaT-T/PathTracer-CPP/pull/18>)：三角形 PDF / random sampling 和 WaveFront OBJ loader。一句话总结：BVH 是这个离线渲染器能渲染网格模型的基础性能结构。

<a id="uf5948a24"></a><strong>3. 材质抽象</strong>

<a id="u1397711b"></a>核心知识点：Scatter / Eval / PDF讲解：面试里这点很重要。不要只说“材质会反射光”，要说你把材质拆成三件事：`Scatter` 决定怎么采样下一条方向，`Eval` 计算这个方向上的 BRDF 值，`PDF` 返回这个采样方向的概率密度。三者必须一致，否则渲染会有偏。此项目中的实现：`Material.h:26` 的 `Material` 基类提供 `Scatter()`、`Eval()`、`PDF()`；传统材质包括 `Lambertian`、`Metal`、`Dielectric`、`Diffuse_Light`、`isotropic`，PBR 材质也接入同一套接口。一句话总结：这个接口设计让材质采样、BRDF 评估和概率密度可以统一进入路径积分器和 MIS。

<a id="u109a2499"></a><strong>4. Russian Roulette</strong>

<a id="u37119f2a"></a>核心知识点：路径终止、无偏估计、方差控制讲解：路径不能无限递归，简单用固定 `max_depth` 会截断能量；Russian Roulette 是在一定 bounce 后按概率终止路径，未终止的路径用生存概率补偿能量。面试里重点讲“它不是加速技巧本身，而是控制长路径计算成本，同时尽量保持无偏”。此项目中的实现：Issue [#12](<https://github.com/JiaT-T/PathTracer-CPP/issues/12>) 要求用 Russian Roulette 替代原来的固定深度；[PR #20](<https://github.com/JiaT-T/PathTracer-CPP/pull/20>) 引入基于材质反照率的动态生存概率，并配合 firefly clamping 控制低采样下的高亮噪点。一句话总结：Russian Roulette 让递归路径在深度较大时更经济，同时保留物理上合理的能量估计。

<a id="u674d3fb7"></a><strong>5. OBJ / MTL 资产导入</strong>

<a id="u6c814233"></a>核心知识点：tinyobjloader、顶点/法线/UV、材质映射讲解：从硬编码球体过渡到真实模型，关键不只是读顶点，还要正确读面索引、UV、法线、材质 ID，并把 MTL 中的贴图路径映射到渲染器材质。此项目中的实现：`ObjLoader.h:13` 使用 tinyobjloader；`ObjLoader.h:99` 通过 `material_id` 找每个 face 的材质；`ObjLoader.h:166` 读取 diffuse / normal / roughness / metallic 贴图。对应 [PR #28](<https://github.com/JiaT-T/PathTracer-CPP/pull/28>)，目标是让 OBJ 材质能自动进入 `PBR_Material`。一句话总结：OBJ/MTL 这条链路让项目从“手写测试场景”升级成“可导入真实 PBR 资产”。

<a id="ua333730a"></a><strong>6. 纹理与颜色空间</strong>

<a id="u33101b5c"></a>核心知识点：sRGB、Linear、数据贴图讲解：PBR 项目里颜色空间很容易被问。baseColor 是颜色，要从 sRGB 转 linear；roughness、metallic、normal 是数据，不应该做 sRGB 变换。此项目中的实现：`Texture.h:7` 区分 `color_space::SRGB` 和 `color_space::Linear`；`Texture.h:22` 做 sRGB 到 linear；`ObjLoader.h:177` 明确 normal / roughness / metallic 作为 linear 数据贴图加载。一句话总结：正确的颜色空间处理是 PBR 结果可信的前提。

<a id="udef33529"></a><strong>7. Normal Map 与 TBN</strong>

<a id="u5c093ff4"></a>核心知识点：切线空间、TBN、shading normal / geometric normal讲解：normal map 的值在切线空间里，不能直接当世界空间法线用；需要三角形根据 UV 计算 tangent / bitangent，再和法线组成 TBN，把贴图法线变换到世界空间。还要区分几何法线和着色法线，避免求交偏移、正反面判断和视觉法线混在一起。此项目中的实现：`Triangle.h:126` 计算 tangent space；`Triangle.h:212` 同时保留 `geo_n` 和 `n`；`Material.h:388` 在 `PBR_Material` 中采样 normal map；`ObjLoader.h:255` 根据文件名判断 OpenGL / DirectX normal map 约定。对应 [PR #27](<https://github.com/JiaT-T/PathTracer-CPP/pull/27>) 和 Issue [#29](<https://github.com/JiaT-T/PathTracer-CPP/issues/29>)。一句话总结：normal map 不是简单改法线，而是 UV、TBN、几何法线和着色法线共同配合的资产链路。

<a id="ufe474ab0"></a><strong>8. PBR 材质，非常重要</strong>

<a id="u1563cb8a"></a>核心知识点：metallic-roughness、GGX、Schlick Fresnel、Smith、能量守恒讲解：面试里可以这样说：我实现的是 metallic-roughness 工作流，baseColor 决定基础颜色，metallic 控制材质在电介质和金属之间过渡，roughness 控制微表面粗糙程度。镜面项用 GGX 描述微表面法线分布，Schlick Fresnel 描述视角越擦边反射越强，Smith 几何项描述微表面之间的遮挡。diffuse 和 specular 不是随便相加，而是根据 metallic 和 Fresnel 做能量分配，避免材质反射出超过入射光的能量。此项目中的实现：`Material.h:203` 是 `PBR_Material`；`Material.h:227` 的 `Scatter()` 建立 diffuse cosine PDF 和 GGX PDF 的混合采样；`Material.h:246` 的 `Eval()` 计算 PBR BRDF；`Material.h:309` 包含 GGX、Smith、Fresnel 组合。Issue [#25](<https://github.com/JiaT-T/PathTracer-CPP/issues/25>) 是 PBR 主目标，[PR #26](<https://github.com/JiaT-T/PathTracer-CPP/pull/26>) 和 [PR #28](<https://github.com/JiaT-T/PathTracer-CPP/pull/28>) 分别推进基础 PBR 与资产驱动 PBR。一句话总结：PBR 部分的重点不是“用了几个公式”，而是把材质参数、BRDF 评估、采样 PDF 和贴图工作流接成了一条一致的物理材质链路。

<a id="ue3639340"></a><strong>9. GGX VNDF 采样</strong>

<a id="u2d26eb0c"></a>核心知识点：NDF 采样 vs VNDF 采样、可见微表面讲解：普通 GGX 半程向量采样可能采到很多从当前视角不可见的微表面，尤其低 roughness 金属会浪费样本并产生高亮噪点。VNDF 采样会根据 view direction 采样“可见法线分布”，更适合光滑金属。此项目中的实现：`PDF.h:101` 是 `GGX_PDF`；`PDF.h:107` 标注其用于 PBR 的 VNDF specular PDF；`PDF.h:169` 通过 roughness space 拉伸视线方向并采样 visible-normal domain。PR #28 的评论记录里也有 “NDF -&gt; VNDF” 的验证图。一句话总结：VNDF 采样是这个 PBR 材质在光滑金属上减少无效样本和 firefly 的关键优化。

<a id="ucd21713a"></a><strong>10. IBL，非常重要</strong>

<a id="u2ae14ebe"></a>核心知识点：HDRI、经纬图、亮度重要性采样、solid-angle PDF讲解：IBL 不是只把环境贴图当背景。真正用于路径追踪时，环境图应该同时提供两件事：miss 时返回环境辐射；作为无穷远光源被显式采样。因为经纬图不是等面积映射，采样权重不能只看像素亮度，还要考虑球面面积权重，也就是靠近极点的 texel 在球面上面积更小。面试里要说清楚“亮度分布 + 球面面积权重 + PDF 转 solid angle”，不要只说“按亮的地方多采样”。此项目中的实现：`Environment.h:23` 是 `LatLong_Environment`；`Environment.h:199` 构建采样分布；`Environment.h:261` 用两级 CDF 采样 row / column；`Environment.h:285` 的 `texel_weight()` 使用 luminance 和 `sin(theta)`；`Environment.h:73` 把 UV PDF 转为 solid-angle PDF。一句话总结：这个项目的 IBL 重点是让 HDRI 从“可见背景”升级成“可被重要性采样的真实环境光源”。

<a id="u6d561423"></a><strong>11. MIS，非常重要</strong>

<a id="u7a266ad9"></a>核心知识点：Light sampling、BSDF sampling、Power Heuristic讲解：直接光照有两个常见采样策略：从光源采样，或者从 BSDF 采样。光源采样适合面积光和环境高亮区域；BSDF 采样适合镜面/金属方向性很强的材质。MIS 不是二选一，而是把两个估计器按 PDF 可靠性加权组合，避免某个策略在特定场景下方差过高。此项目中的实现：`Camera.h:18` 有 power heuristic；`Camera.h:436` 构建 light PDF，把几何光和环境光合并；`Camera.h:542` 显式计算 light-side direct estimator；`Camera.h:556` 显式计算 BSDF-side direct estimator；`Camera.h:641` 单独处理 indirect continuation。对应 [PR #30](<https://github.com/JiaT-T/PathTracer-CPP/pull/30>)。一句话总结：MIS 是这个项目把 PBR、面积光和 HDRI 环境光稳定结合起来的核心采样框架。

<a id="u64929434"></a><strong>12. 第一跳 direct lighting 重构</strong>

<a id="u4c971acb"></a>核心知识点：采样预算、direct / indirect 分离、emission guard讲解：第一跳对画面噪点影响最大，但如果每增加一个样本就递归整条路径，成本会爆炸。更好的做法是第一跳加强 direct lighting，间接路径仍保持单次 continuation。还要避免 direct lighting 已经显式估计了发光体后，递归又把同一个 emission 加一次。此项目中的实现：PR #30 把第一跳拆成 `sample_direct_light_once()`、`sample_direct_bsdf_once()`、`sample_indirect_once()`；`Camera.h:496` 的递归版本带 `allow_emission`；`Camera.h:679` 间接 continuation 关闭重复 emission。一句话总结：这一步体现的是渲染器工程优化思路：把采样预算集中用在最影响噪点的 direct term 上。

<a id="u87d34e0a"></a><strong>13. 多线程，非常重要</strong>

<a id="u778d4bf7"></a>核心知识点：tile-based parallel rendering、`std::execution::par`、thread-local RNG、mutex / atomic讲解：路径追踪每个像素、每个 sample 基本独立，天然适合并行。但不能简单“多线程写图像”就完事，必须说明共享数据边界：每个 tile 写 framebuffer 的不重叠区域，所以像素写入不需要锁；进度计数用 atomic；预览窗口和日志刷新属于共享状态，要用 mutex 控制；随机数生成器必须 thread-local，否则多个线程共享 RNG 会产生数据竞争和采样相关性。此项目中的实现：`Camera.h:114` 定义 `RenderTile`；`Camera.h:125` 的 `render_impl()` 统一串行/并行渲染；`Camera.h:219` 用 `std::for_each(std::execution::par, tiles.begin(), tiles.end(), render_tile)` 调度；`My_Common.h:29` 使用 `thread_local std::mt19937`。benchmark：800x450 / 400 spp / depth 20，从 65.3296s 降到 29.9941s，约 2.178x。一句话总结：这个多线程实现的面试重点是“任务划分 + 共享数据隔离 + 同步边界”，而不是只说用了并行库。

<a id="u8b6b57d2"></a><strong>14. 实时预览窗口</strong>

<a id="u80ca6d80"></a>核心知识点：渲染过程反馈、preview buffer、UI 状态同步讲解：离线路径追踪时间长，实时预览能让用户看到 tile 渲染进度，但预览只应该读已经完成的 tile 数据，不能干扰渲染主流程。此项目中的实现：`PPMPreviewWindow.h` 负责窗口显示；`Camera.h:276` 把 tile 结果 blit 到 preview buffer；对应 [Issue #23](<https://github.com/JiaT-T/PathTracer-CPP/issues/23>) 和 [PR #24](<https://github.com/JiaT-T/PathTracer-CPP/pull/24>)。一句话总结：实时预览是工程可用性提升，不改变积分算法，但要求和多线程渲染正确同步。

<a id="u3b46e41e"></a><strong>15. 展示场景与验证</strong>

<a id="u28d541c9"></a>核心知识点：功能验证场景、benchmark、README showcase讲解：项目不只是堆功能，还要有能验证功能的场景：PBR 球、normal map 对比、OBJ PBR 自动映射、HDRI + area light 的 IBL/MIS 场景、README 综合展示场景。此项目中的实现：`Renderer.cpp` 中有 `PBR_Test()`、`PBR_Benchmark()`、`PBR_Normal_Map_Test()`、`Obj_PBR_Test()`、`PBR_IBL_Test()`、`README_Showcase()`。README 也明确列了当前能力和 benchmark 数据。一句话总结：这些场景是你面试时证明“功能真的跑通了”的证据链。

<a id="ufaaddbfb"></a><strong>面试总总结</strong>

<a id="u93a8b610"></a>这个项目可以概括为：我从基础 CPU 路径追踪出发，先完成射线求交、材质递归、BVH、OBJ 加载和实时预览；随后把材质系统重构为 `Scatter / Eval / PDF`，接入 metallic-roughness PBR、GGX/VNDF、纹理颜色空间和 TBN normal map；再把 HDRI 环境光升级为可显式采样的 IBL 光源，并通过 light / BSDF MIS 降低 PBR + IBL 场景的方差；最后用 tile-based `std::execution::par`、thread-local RNG、atomic/mutex 同步完成 CPU 多线程加速，获得约 2.18x 的实测提升。

原文：[Pathtracer 梳理](<https://www.yuque.com/u62694975/iaaa/xkyt3prgqt2mnn3g>)
