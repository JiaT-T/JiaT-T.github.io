---
title: "GAMES104：如何构建游戏世界"
slug: "games104-game-world"
summary: "整理 Game Object 与组件化、Tick 更新、事件交互和场景空间管理的基本思路。"
categories: ["图形学"]
tags: ["GAMES104", "Game Engine", "Game Architecture", "Component", "Scene Management"]
date: "2026-03-26T01:08:36.000Z"
lastmod: "2026-04-02T05:50:08.000Z"
draft: false
yuque_slug: "bcpq57y01e04q16g"
source: "https://www.yuque.com/u62694975/iaaa/bcpq57y01e04q16g"
---

<a id="u2ad00f21"></a><strong>Game Objects：</strong>

<a id="u0ca4fe31"></a>Dynamic game objects：角色，载具...

<a id="u437bec7e"></a>Static game objects：房子，岩石....

<a id="u3f9bbc34"></a>Environment：天空，植被，地势....

<a id="ucd754ae4"></a>Other object：空气墙，检测区域....

<a id="u7033be66"></a>对于一个game object，它既存在Attributes（属性），也拥有Behaviours（行为），因此定义一个类来描述它是最好的方法；与此同时，在这个game object的基础上，还可以加上更多的属性与行为，使其成为另一个全新的对象，这里自然而然地会想到用继承来定义另一个新物体。

<a id="uceb7a831"></a>但是很多时候，这两个物体之间并不是严格的父类与子类的关系（e.g.水路两栖车到底派生自车类还是船类？），所以，现代游戏引擎通常会使用Component Base（组件化）的方法来解决这一问题：将单个game object的许多不同部件拆分出来，作为单独的函数，在ComponentBase这个基类中定义基础的属性接口

<a id="ue53f5b4b"></a><strong>总结</strong>：1.在游戏世界中，所有物体都被抽象为Game Object

<a id="uf6bce5f4"></a>2.所有的Game Objects又由许多的Component组成

<a id="uf33ace34"></a><em><span style="color: #117CEE">如何构建动态的世界：</span></em>

<a id="u35c4bfab"></a>通过Tick（）实现

<a id="ua15058a5"></a>游戏画面实际上是由大量连续帧组成的，以30fps为例，引擎每1/30秒就会调用一次Tick（）函数，对动画，物理等等进行更新，但这里的Tick（）并不是逐对象实现，而是逐组件实现的（e.g.先完成动画系统的更新，再去进行相机系统的更新）

<a id="ucaab5166"></a>Why：简单来说，就是现代计算机流水线的批处理效率比逐个处理单物体的效率要高

<a id="u21b443dd"></a><a id="u66c9caa5"></a><img src="/images/games104-game-world/games104-game-world-01.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="u84ffe2ea"></a><em><span style="color: #117CEE">如何创建交互：</span></em>

<a id="u732c89ac"></a>通过事件进行

<a id="ud0bdd3db"></a>当对象发生某个行为时，周围的其他对象可能需要对这一行为作出反应，在早期的游戏引擎中，这一部分通常是Hard Code，即在类中定义所有对象对于这一行为的反应。

<a id="uc634faf3"></a>但随着游戏对象的复杂化，硬编码的效率太低，有时甚至无法运行，于是出现了另一种方法：事件；对于每个对象，它并不需要知道周围其他对象应当作出何种反应，他只需要告诉对应的game object发生了什么事件，之后交由其他对象自行调用对应的方法并产生影响

<a id="u31083808"></a><em><span style="color: #117CEE">如何管理Game Objects：</span></em>

<a id="ub1a58506"></a>既然已经知道发生了某个事件，那应该如何寻找到受影响的物体？

<a id="u9466b6da"></a>在小型游戏中，可以通过将地图划分为一个一个的小格子，以此来判断哪些区域（格子）内的物体会受到影响；

<a id="u8ca4947b"></a>但是游戏内的资源分布往往是不均匀的，如果平均划分的话会产生性能浪费，所以应当使用更加高效的场景管理策略，比如：BVH，八叉树等等

<a id="u0a979e03"></a><em><span style="color: #117CEE">更加复杂的情况：</span></em>

<a id="ud6053fbb"></a>在很多情况下，消息的发送并不是单向的，而是会在多个系统之间双向进行，因此消息发送的顺序尤为重要；为了解决顺序的问题，引擎通常会将所有消息先收集起来，之后再按照一定的顺序进行发送（e.g.相当于邮局，对象将所有的信件都先寄邮局，之后再由邮局按照顺序统一发出）

原文：[如何构建游戏世界](<https://www.yuque.com/u62694975/iaaa/bcpq57y01e04q16g>)
