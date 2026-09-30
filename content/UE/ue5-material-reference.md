---
title: "UE5 材质备忘录"
slug: "ue5-material-reference"
summary: "整理主材质、风格化着色、后处理描边、程序化表面、运行时材质控制与性能对比的练习方向。"
categories: ["Unreal Engine"]
tags: ["Unreal Engine", "Materials", "PBR", "NPR", "Rendering"]
date: "2026-06-09T07:36:23.000Z"
lastmod: "2026-06-21T07:43:56.000Z"
draft: false
yuque_slug: "xle6wz959o7asdvg"
source: "https://www.yuque.com/u62694975/iaaa/xle6wz959o7asdvg"
---

<a id="ua1531d0e"></a><strong>最推荐你做的展示项目</strong>

<a id="uc138ff13"></a>我建议你直接做一个仓库或 UE 项目，名字可以叫：

<a id="u3a824426"></a>UE5-Material-Lab

<a id="u38828f81"></a>内容不要太大，但结构要专业：

- <a id="uf430be9c"></a>01\_PBR\_MasterMaterial
- <a id="u3869d3c8"></a>02\_NPR\_ToonCharacter
- <a id="u3958d768"></a>03\_PostProcess\_Outline
- <a id="u223004ff"></a>04\_Procedural\_Surface
- <a id="u18a5e358"></a>05\_Runtime\_Material\_Control
- <a id="u1934f4d5"></a>06\_Material\_Optimization

<a id="u114d64b3"></a>每个 demo 都要有：

- <a id="u33ee3297"></a>效果截图或短视频
- <a id="u124723fe"></a>材质图截图
- <a id="uf554c0e8"></a>关键 Material Function 说明
- <a id="u2d55bafb"></a>参数面板截图
- <a id="uda305991"></a>性能视图截图
- <a id="ud627a5d0"></a>简短 README：目标、实现、关键节点、性能注意点

<a id="uc93d9e5b"></a>这样别人看你的项目时，不会觉得你只是“会用 UE 做材质”，而会看到你掌握了材质系统的工程化组织。

<a id="u4d14ef61"></a><strong>几个具体 demo 方向</strong>

<a id="u49ddcb02"></a>PBR Master Material：  
一个支持 packed ORM、normal map、detail normal、emissive、clear coat、wetness、vertex color blend 的主材质。重点展示参数体系和实例复用。

<a id="u72a4685e"></a>NPR Character Shader：  
ramp diffuse、step specular、rim light、matcap、outline。可以结合你之前 PGR/Unity 角色渲染经验迁移到 UE5。

<a id="ueb276a3d"></a>Post Process Outline：  
用 depth / normal / custom stencil 做边缘检测。重点写清楚 SceneTexture、CustomDepth、Blendable Location。

<a id="u97460ad3"></a>Procedural Surface：  
雪地、湿润、苔藓、沙地、岩石高度混合。重点是 world position、noise、triplanar、height blend。

<a id="u40a46dcf"></a>Runtime Material Control：  
C++ 或 Blueprint 控制Material Instance Dynamic，比如受伤变色、溶解进度、扫描线、雨天 wetness。这个能连接你说的“C++ 与引擎交互”。

<a id="u71fbf0ed"></a>Optimization Case Study：  
同一个材质做高/低两个版本，对比 texture samples、instruction count、shader complexity、static switch。这个非常加分，因为它体现工程判断。

原文：[UE5材质备忘录](<https://www.yuque.com/u62694975/iaaa/xle6wz959o7asdvg>)
