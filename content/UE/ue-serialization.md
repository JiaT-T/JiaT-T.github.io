---
title: "UE 序列化"
slug: "ue-serialization"
summary: "记录序列化的基本含义、数据格式需要考虑的问题及 UE 序列化参考资料。"
categories: ["Unreal Engine"]
tags: ["Unreal Engine", "Serialization", "UObject"]
date: "2026-06-17T05:58:55.000Z"
lastmod: "2026-06-17T12:04:18.000Z"
draft: false
yuque_slug: "olf5vtkv97pprwff"
source: "https://www.yuque.com/u62694975/iaaa/olf5vtkv97pprwff"
---

<a id="DObdX"></a>
## 一：什么是序列化

<a id="ue66e5006"></a>最简单的说法是：<strong>将任意对象 / 数据编排为事先约定好的格式，使得之后的反序列化可以直接拿出来使用</strong>

<a id="ub5ad9205"></a>但是这里的“事先约定的格式”可能是非常复杂的，需要考虑多个方面，比如：如果对所有数据进行打包？序列化后的格式是否具有跨平台性？能否通过网络发送？......

<a id="lWI2k"></a>
## 二：UE 中的序列化

<a id="u2666fce6"></a><strong>【Reference】</strong>

<a id="ua260be9e"></a>[https://zhuanlan.zhihu.com/p/2756361343](<https://zhuanlan.zhihu.com/p/2756361343>)

原文：[序列化](<https://www.yuque.com/u62694975/iaaa/olf5vtkv97pprwff>)
