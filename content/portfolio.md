---
title: "渲染与引擎项目"
description: "C++、实时图形 API 与 Unreal Engine 技术实验"
hideMeta: true
layout: "portfolio"
---

这里优先展示渲染与引擎方向的六个项目。代码、现有预览、运行依赖与当前限制见各仓库 README；性能数字应结合原始测试条件阅读。

## CPU 渲染与 C++

[PathTracer-CPP](https://github.com/JiaT-T/PathTracer-CPP)：GGX/VNDF、灯光与环境重要性采样的 MIS、BVH、并行 Tile、渐进累积与 A-Trous 降噪。适合从光传输、采样和加速结构三个角度阅读。

[Soft-Raster-Renderer](https://github.com/JiaT-T/Soft-Raster-Renderer)：小型软件光栅化器，展示三角形插值、深度测试、Shadow Map、TBN 与 SSAO。原始示例模型未完整提交，需准备有使用权限的资源。

## 实时图形 API

[DX12-Renderer](https://github.com/JiaT-T/DX12-Renderer)：Win32/DirectX 12 的资源与渲染流程，HLSL PBR、IBL、阴影 PCF、HDR 和 ACES。外部模型与 HDRI 的许可及获取方式需要独立确认。

[Vulkan-Renderer](https://github.com/JiaT-T/Vulkan-Renderer)：前向、延迟与离屏渲染实验，以及深度/G-buffer 可视化、透明混合和 SDR/HDR 输出。重点是资源、Render Pass、同步与输出路径的显式管理。

## Unreal Engine

[UE5-FFT-Ocean](https://github.com/JiaT-T/UE5-FFT-Ocean)：基于 Epic 社区 FFT 海面教程，使用 Niagara GPU Simulation Stage 和 USH/HLSL。仓库保留教程来源，包含海面材质、泡沫、散射与级联相关迭代；教程基础结构与个人调试工作应分别理解。

[UE5-Procedural-Grassland](https://github.com/JiaT-T/UE5-Procedural-Grassland)：通过 PCG 与材质资产组织草地生成、WPO、实例数据、LOD 和交互 Render Target。主要实现位于 UE 资产图中，源码中的模板角色代码不能代替对 PCG/材质图的检查。

## 继续阅读

[图形学笔记](/graphics/) · [Vulkan 笔记](/vulkan/) · [Unreal Engine 笔记](/ue/) · [C++ 笔记](/cpp/) · [完整笔记索引](/archives/)
