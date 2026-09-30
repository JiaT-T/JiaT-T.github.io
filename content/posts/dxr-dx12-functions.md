---
title: "DXR / DX12 常用函数"
slug: "dxr-dx12-functions"
summary: "整理 TraceRay 的参数、光线递归深度设置和 OMSetStencilRef 等函数的用途。"
categories: ["DirectX 12"]
tags: ["DirectX 12", "DX12", "DXR", "HLSL", "Ray Tracing"]
date: "2026-03-22T11:36:51.000Z"
lastmod: "2026-03-22T11:37:20.000Z"
draft: false
yuque_slug: "ylfz9hlyr71qgbrb"
source: "https://www.yuque.com/u62694975/iaaa/ylfz9hlyr71qgbrb"
---

<a id="u773eff04"></a><strong>函数<strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong>\*\*\*\*</strong>

<a id="u73fefba8"></a><strong>TraceRay（）函数 </strong>：  
	  作为启动RT Cores的指令，根据之前填写好的payload，在BVH中进行包围盒与三角形的相交测试

<a id="uf6165c16"></a>在调用时，需要给出八个参数，e.g :

<a id="u54fab257"></a>TraceRay

<a id="u41cd8195"></a>(

<a id="u3a9786e5"></a>SceneBVH, 	// 1. RaytracingAccelerationStructure: 整个 3D 世界的加速结构

<a id="u4c5b0a2d"></a>RAY\_FLAG\_NONE, 		// 2. RayFlags: 光线行为标志位

<a id="u9d8643f6"></a>0xFF, 		// 3. InstanceInclusionMask: 剔除掩码 (0xFF 表示与所有物体发生交互，不忽略任何人)

<a id="u65e11b56"></a>0, 			// 4. RayContributionToHitGroupIndex: SBT 命中组的基址偏移 (决定调用哪个 ClosestHit)

<a id="u4e99923c"></a>1, 			// 5. MultiplierForGeometryContributionToHitGroupIndex: SBT 几何体步进乘数

<a id="u9c3c0256"></a>0,  			// 6. MissShaderIndex: 如果啥都没撞到，调用 SBT 里的第几个 Miss 着色器

<a id="u5ecb5a67"></a>Ray, 			// 7. RayDesc: 光线的起点、方向、长短

<a id="ud0c7707d"></a>payload	        // 8. Payload: 随光线传递的背包

<a id="u78364175"></a>);

<a id="ue73e2bf2"></a><strong>SetMaxRecursionDepth（）函数 ：</strong>

<a id="u17d67eee"></a>在CreateRaytracingPipeline（）中被调用，提前告诉GPU这条光线会弹射几次（在括号中填充数值）

<a id="ue170d1d6"></a><strong>OMSetStencilRef（）函数 ：</strong>

<a id="ucf33136a"></a>全称是 `ID3D12GraphicsCommandList::OMSetStencilRef`

<a id="u5e2f1757"></a>可以拆解为：<strong>O</strong>utput <strong>M</strong>erger <strong>SetStencilRef</strong>erence，它用于在渲染管线的最后一个阶段（输出合并阶段）设置<strong>模板测试（Stencil Test）的参考值</strong>。

<a id="u0ebe1202"></a><strong>XMMatrixShadow（）函数 ：</strong>

<a id="udc0240fa"></a>用于构建在特定平面内投影所用的阴影矩阵，定义如下：

<a id="u297c0b35"></a>inline XMMATRIX XM\_CALLCONV XMMatrixShadow(

<a id="ufc0371b9"></a>FXMVECTOR ShadowPlane,

<a id="ue0b5bfcb"></a>FXMVECTOR LightPosition);

原文：[函数](<https://www.yuque.com/u62694975/iaaa/ylfz9hlyr71qgbrb>)
