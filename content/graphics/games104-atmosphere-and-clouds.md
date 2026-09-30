---
title: "GAMES104：大气与云的渲染"
slug: "games104-atmosphere-and-clouds"
summary: "记录高度场地形、三角形与四叉树细分的基本思路，以及地形 LOD 和层级管理问题。"
categories: ["图形学"]
tags: ["Computer Graphics", "GAMES104", "Terrain", "Heightfield", "LOD"]
date: "2026-06-14T10:28:47.000Z"
lastmod: "2026-06-14T11:00:12.000Z"
draft: false
yuque_slug: "ngr6yns3m64phwpl"
source: "https://www.yuque.com/u62694975/iaaa/ngr6yns3m64phwpl"
---

<a id="Cabh8"></a>
## 一：地形的几何

<a id="Hpxyl"></a>
### Heighfield：

<a id="u9ee63daa"></a>根据高度图偏移顶点

<a id="u33109b1f"></a>缺点：远处的细分层级太高，存在 LoD 的优化空间

<a id="rDLHn"></a>
### 细分方式：

1. <a id="u807708c3"></a><strong>二分的方法</strong>：每次选取三角形最长边的中点进行切分
2. <a id="u25558877"></a><strong>QuadTree-Based Subdivision</strong>：优点——容易构建、资源更易于管理...，缺点——网格细分不如三角形灵活、叶节点的层级需要连续....

原文：[大气与云的渲染](<https://www.yuque.com/u62694975/iaaa/ngr6yns3m64phwpl>)
