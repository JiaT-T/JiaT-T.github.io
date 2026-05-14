---
title: "Whitted-style 光线追踪与 Monte Carlo 路径追踪的主要区别"
date: 2026-05-14
categories: ["图形学", "光线追踪"]
tags: ["Ray-Tracing", "CG"]
draft: false
TocOpen: true  # 这篇文章的目录默认保持展开
---
\### 一：Whitted-style 光线追踪

\+ 流程：

&nbsp;   - 从相机发出主光线

&nbsp;   - 命中物体之后根据材质种类继续发射：

&nbsp;       \* 反射光线

&nbsp;       \* 折射光线

&nbsp;       \* 阴影光线

&nbsp;   - 最后通过递归计算所有光线对像素的贡献值

\+ 主要用于\*\*模拟直接光照与理想情况下的反射、折射现象\*\*，对于真实世界的漫反射、全局光照、颜色渗透等并不擅长，因为它的路径通常是确定的——遇到镜面就反射，遇到玻璃就折射.....







\### 二：Monte Carlo 路径追踪

\+ 流程：

&nbsp;   - 从相机发出射线

&nbsp;   - 命中物体后根据 BRDF 随机选择次级射线发射方向

&nbsp;       \* 漫反射方向

&nbsp;       \* 高光方向

&nbsp;       \* 透射方向

&nbsp;       \* ......

&nbsp;   - 经过多次采样之后求得平均值

\+ 因为光线传播方向的多样性，路径追踪可以\*\*很好的模拟诸如漫反射间接光、软阴影、全局光照等现象\*\*







\### 三：简单对比

| \*\*<font style="color:rgb(252, 252, 252);">项目</font>\*\* | \*\*<font style="color:rgb(252, 252, 252);">递归式光线追踪</font>\*\* | \*\*<font style="color:rgb(252, 252, 252);">路径追踪</font>\*\* |

| --- | --- | --- |

| <font style="color:rgb(252, 252, 252);">代表算法</font> | <font style="color:rgb(252, 252, 252);">Whitted Ray Tracing</font> | <font style="color:rgb(252, 252, 252);">Monte Carlo Path Tracing</font> |

| <font style="color:rgb(252, 252, 252);">光线传播</font> | <font style="color:rgb(252, 252, 252);">反射、折射递归分支</font> | <font style="color:rgb(252, 252, 252);">随机采样一条或多条路径</font> |

| <font style="color:rgb(252, 252, 252);">主要效果</font> | <font style="color:rgb(252, 252, 252);">镜面、玻璃、阴影</font> | <font style="color:rgb(252, 252, 252);">全局光照、软阴影、间接光</font> |

| <font style="color:rgb(252, 252, 252);">漫反射间接光</font> | <font style="color:rgb(252, 252, 252);">通常不自然支持</font> | <font style="color:rgb(252, 252, 252);">天然支持</font> |

| <font style="color:rgb(252, 252, 252);">结果</font> | <font style="color:rgb(252, 252, 252);">比较干净</font> | <font style="color:rgb(252, 252, 252);">有噪声，需要采样收敛</font> |

| <font style="color:rgb(252, 252, 252);">成本</font> | <font style="color:rgb(252, 252, 252);">相对低</font> | <font style="color:rgb(252, 252, 252);">通常更高</font> |

| <font style="color:rgb(252, 252, 252);">物理真实性</font> | <font style="color:rgb(252, 252, 252);">有限</font> | <font style="color:rgb(252, 252, 252);">更接近物理真实</font> |

















