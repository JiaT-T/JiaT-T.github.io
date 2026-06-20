---
title: "Split-Sum IBL"
slug: "split-sum-ibl"
date: 2026-06-20T00:00:00+08:00
draft: false
summary: "整理 PBR IBL 中 Irradiance Map、Prefiltered Environment Map 与 BRDF LUT 的拆分思路和运行时组合方式。"
categories: ["图形学"]
tags: ["Computer Graphics", "Rendering", "PBR", "IBL"]
---

基于辐射度方程的拆分，IBL 主要分为处理漫反射（Diffuse）和镜面反射（Specular）两个核心部分。

## 1. Irradiance Map（辐照度图）

**Irradiance Map** 用于解决 PBR 中的漫反射（Diffuse Lambertian）光照部分。

### 核心原理

漫反射片元会接收半球方向（Hemisphere）上所有入射光线的贡献。常规计算需要对整个半球进行蒙特卡洛积分：

$I = \int_{\Omega} L_i(p, \omega_i)(\mathbf{n} \cdot \omega_i)d\omega_i$

在实时渲染中，不可能对每个像素都运行这种高采样率的积分。

### 怎么做与存什么

因为漫反射与观察视角（View Direction）无关，只与表面的法线方向（Normal $\mathbf{n}$）有关。因此，我们可以预先旋转一个半球微表面，计算出每一个可能的法线方向 $\mathbf{n}$ 所能接收到的总辐射度，然后将这个结果存储在一张新的立方体贴图（Cube Map）中。

- **输入：** 原始的高动态范围环境贴图（HDR Environment Map）。
- **采样/存储：** 其纹理坐标代表**法线方向**。当着色器计算漫反射时，直接用片元的法线 $\mathbf{n}$ 去采样 Irradiance Map，即可在 $O(1)$ 时间内得到环境光对该点的漫反射贡献。
- **视觉特征：** 由于半球积分相当于一个极低通滤波器（Low-pass Filter），Irradiance Map 看起来非常模糊，丢失了所有高频细节，只保留宏观的色彩趋向。这张贴图的每一个像素坐标（u, v）代表一个方向，每一个像素的值（RGB）代表“**如果法线朝向这个方向，所能接收到的总辐射度**”。

## 2. Prefiltered Environment Map（预滤波环境贴图）

**Prefiltered Environment Map** 用于解决镜面反射（Specular）部分的第一部分。

### 核心原理

Epic Games 在推广微表面模型（Microfacet Model）的 IBL 时，引入了**裂项近似（Split-Sum Approximation）**，将镜面反射的积分项拆分为两部分。第一部分只关注环境光与表面粗糙度的关系：

$\int_{\Omega} L_i(p, \omega_i)d\omega_i \approx \frac{1}{N}\sum_{i=1}^{N}L_i(p, \omega_k)$

### 怎么做与存什么

镜面反射不仅与法线有关，还与反射视角和表面的粗糙度（Roughness）紧密相关。粗糙度决定了反射波瓣（Specular Lobe）的宽窄：表面越光滑，波瓣越窄，反射越清晰；表面越粗糙，波瓣越宽，反射越模糊。

- **存储结构：** 利用 Mipmaps 机制。一张 Prefiltered Map 包含多个 Mip 级别。
- **Mip 映射关系：**
  - **Mip 0：** 存储粗糙度 = 0 时的反射，也就是完全镜面反射，接近原始环境贴图。
  - **Mip 1 到 Mip N：** 随着 Mip 级别升高，对应存储的粗糙度线性增加，积分采样时使用的微表面分布函数（GGX NDF）波瓣越宽。
- **采样方式：** 运行时，Shader 根据片元的反射向量 $\mathbf{R}$ 和材质的**粗糙度**，利用 `textureLod` 函数去对应的 Mip 级别中进行三线性插值采样。

## 3. LUT（Look-Up Table / 镜面反射积分查找表）

**LUT** 用于解决镜面反射拆分后的第二部分，也就是环境 BRDF 项。

### 核心原理

裂项近似拆出来的第二部分，代表了在特定粗糙度下，不同入射角所带来的能量衰减与菲涅尔效应的整合，包括几何遮蔽 $G$ 项和菲涅尔 $F$ 项的积分：

$\int_{\Omega} f_r(\omega_i, \omega_o)(\mathbf{n} \cdot \omega_i)d\omega_i$

这个积分虽然复杂，但它的自变量只有两个：**法线与视角夹角的余弦值 $\cos\theta_v$，即 $\mathbf{n} \cdot \mathbf{v}$**，以及**材质的粗糙度（Roughness）**。

### 怎么做与存什么

由于这两个自变量的范围都在 $[0, 1]$ 之间，因此可以将其预计算并存储在一张二维纹理中，这就是 IBL 的 **BRDF LUT**。

- **纹理坐标：**
  - Horizontal（X 轴）/ $U$：$\mathbf{n} \cdot \mathbf{v}$
  - Vertical（Y 轴）/ $V$：粗糙度（Roughness）
- **存储通道：**
  - 通过数学变换，该积分最后可以化简为 $F_0 \cdot A + B$ 的形式。
  - 纹理的 **R 通道**存储比例系数 $A$。
  - 纹理的 **G 通道**存储偏移系数 $B$。
- **运行时使用：** Shader 用 $\mathbf{n} \cdot \mathbf{v}$ 和粗糙度采样这张二维 LUT 纹理，读出 $A$ 和 $B$，结合材质自身的 $F_0$（基础反射率），通过 $F_0 \cdot A + B$ 即可恢复出镜面反射 BRDF 的缩放值。

## 总结：运行时如何组装？

在 PBR 像素着色器中，IBL 的计算流程极其精简和高效。

### 1. 漫反射

$\text{Diffuse} = \text{TextureCube}(\text{IrradianceMap}, \mathbf{n}) \times \text{Albedo}$

### 2. 镜面反射

- 用反射向量 $\mathbf{R}$ 和粗糙度采样预过滤贴图：$\text{LD} = \text{TextureCubeLod}(\text{PrefilteredMap}, \mathbf{R}, \text{Roughness})$
- 用 $\mathbf{n} \cdot \mathbf{v}$ 和粗糙度采样查找表：$(A, B) = \text{Texture2D}(\text{BRDF_LUT}, \mathbf{n} \cdot \mathbf{v}, \text{Roughness})$
- 融合结果：$\text{Specular} = \text{LD} \times (F_0 \times A + B)$

### 3. 最终环境光

根据能量守恒（菲涅尔系数 $k_s$ 和漫反射系数 $k_d$）将两部分相加。
