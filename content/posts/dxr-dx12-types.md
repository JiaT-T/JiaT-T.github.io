---
title: "DXR / DX12 常用类型"
slug: "dxr-dx12-types"
summary: "记录 IDxcBlob、DXC 编译产物和 XMVECTOR 等 DirectX 开发中的常用类型。"
categories: ["DirectX 12"]
tags: ["DirectX 12", "DX12", "DXR", "DXC", "HLSL"]
date: "2026-03-22T11:36:33.000Z"
lastmod: "2026-03-22T11:37:06.000Z"
draft: false
yuque_slug: "pdqkkw46v93xhzlt"
source: "https://www.yuque.com/u62694975/iaaa/pdqkkw46v93xhzlt"
---

<a id="u42ddaf45"></a><strong>类型<strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong><strong>\*</strong>\*\*\*\*</strong>

<a id="u444f1226"></a><strong> IDxcBlob </strong> :

<a id="ubd4bd6f7"></a>Blob的全名 ：  Binary Large Object（二进制大对象）

<a id="u3d606c6f"></a>`IDxcBlob` 属于 <strong>CPU 准备数据</strong> 这一阶段的产物  ， 本质上就是对一块内存的封装

<a id="uf33fe782"></a>作为 CPU（餐厅经理），你写了一份极为复杂的后厨操作指南（HLSL Shader 代码）。你把这份人类可读的指南送到了翻译部门（DirectX Shader Compiler, 简称 DXC），DXC 将其翻译成 GPU 能看懂的机器码（DXIL - DirectX Intermediate Language），然后把它塞进一个 `IDxcBlob` 这个“图纸管”里交还给你。

<a id="u745f385c"></a><strong>XMVECTOR</strong> ：

<a id="ue4d7c385"></a>一个四维向量

原文：[类型](<https://www.yuque.com/u62694975/iaaa/pdqkkw46v93xhzlt>)
