---
title: "UE Gameplay Framework（一）"
date: 2026-06-15T20:00:00+08:00
draft: false
summary: "按职责、网络复制和生命周期梳理 Unreal Engine Gameplay Framework 中常用类的分工。"
categories: ["Unreal Engine"]
tags: ["Unreal Engine", "Gameplay Framework", "Game Architecture"]
---

**Reference:** [Gameplay Framework in Unreal Engine](https://dev.epicgames.com/documentation/unreal-engine/gameplay-framework-in-unreal-engine?application_version=5.7)


## 一：规则与全局状态

这部分决定一局游戏如何开始、如何结束，以及哪些状态需要同步给所有玩家。

### GameMode

**职责：** 定义一局游戏的权威规则与流程，例如玩家如何加入、默认 Pawn / Controller / HUD / PlayerState 使用哪些类、如何生成玩家、胜负条件如何判定。

**网络特点：** `GameMode` 只存在于服务器端。客户端不能直接访问或信任 `GameMode`，否则玩家就可以通过修改本地逻辑作弊。

**适合存放：** 只需要服务器知道的规则判断，例如是否允许重生、是否满足胜利条件、玩家进入游戏时应该生成什么角色。

### GameState

**职责：** 保存“所有玩家都应该知道的全局状态”，例如当前比赛阶段、队伍分数、剩余时间、目标进度，以及所有玩家的 `PlayerState` 列表。

**网络特点：** `GameState` 由服务器维护，并复制到所有客户端。它不是用来制定规则的，而是用来把服务器认可的比赛状态同步给所有人。

**容易混淆：** “谁赢了、能不能重生、应该在哪里出生”这类规则通常由 `GameMode` 判定；“当前比分、比赛是否已经结束、所有玩家列表”这类共享结果适合放在 `GameState`。

### PlayerState

**职责：** 保存某个玩家的可复制状态，例如玩家名、分数、队伍、击杀数、死亡数、延迟，或者需要在换 Pawn 后仍然保留的玩家数据。

**生命周期：** `PlayerState` 跟“玩家”绑定，而不是跟某个具体角色模型绑定。Pawn 死亡、重生或被替换时，`PlayerState` 通常仍然代表同一个玩家。

**网络特点：** `PlayerState` 会复制给所有客户端，所以适合放其他玩家也需要看到的数据。只属于本地 UI 或本地输入的数据，不应该放在这里。

## 二：控制与决策

这部分处理“谁在下命令”，以及命令如何作用到可控制实体上。

### Controller

`Controller` 是非物理的“意志”或决策对象，负责控制一个 `Pawn`。Controller 本身不代表游戏世界中的身体，它通过 `Possess` 控制 Pawn。

### PlayerController

**职责：** 表示玩家的控制意图，处理输入、相机相关控制、与本地玩家 UI / HUD 的交互，并控制一个 Pawn。

**网络特点：** 在多人游戏中，`PlayerController` 通常只存在于服务器和对应的拥有者客户端上，并不会像 `PlayerState` 那样完整复制给所有客户端。因此公共玩家信息更适合放在 `PlayerState`。

### AIController

**职责：** 表示 AI 的决策逻辑，可以运行行为树、黑板、状态树、导航等系统，并控制一个 AI Pawn。

**使用场景：** NPC、怪物、自动炮台、机器人等不由人类玩家直接输入控制的实体。

## 三：世界中的实体与组件

这部分解决“什么东西存在于世界中，以及它如何组成”。

### World

`World` 是运行中关卡和 Actor 的上下文，包含当前加载的关卡、Actor、GameMode、GameState 等对象。它不是单个玩法规则类，而是游戏世界运行时的容器。

### Actor

`Actor` 是关卡中最基础的可放置、生成、复制和销毁对象。它本身更像一个容器，真正的可视化、碰撞、音效、粒子、移动能力通常由组件提供。

### Component

`Component` 用来把功能模块化地挂到 Actor 上。

- `SceneComponent` 提供 Transform 和层级关系。
- `PrimitiveComponent` 可以参与渲染或碰撞。
- `MovementComponent` 负责移动逻辑。
- 自定义 `ActorComponent` 适合封装背包、交互、状态机等可复用功能。

### Pawn

`Pawn` 是可以被 `Controller` 控制的 Actor，代表一个可被“意志”驱动的实体。玩家角色、AI 敌人、载具、无人机都可以是 Pawn。

### Character

`Character` 是 `Pawn` 的常用子类，专门面向类人角色或需要角色移动模型的实体。

默认常见组件包括：

- `CapsuleComponent`：胶囊碰撞体。
- `SkeletalMeshComponent`：骨骼网格。
- `CharacterMovementComponent`：角色移动组件，提供行走、跳跃、网络移动预测等常用能力。

如果实体不需要这套角色移动能力，例如飞船、炮塔、棋子，直接继承 `Pawn` 或 `Actor` 往往更合适。

## 四：生命周期与跨关卡数据

这部分处理“哪些数据能跨关卡存在，以及模块化系统放在哪里”。

### GameInstance

`GameInstance` 在游戏启动后创建，在游戏退出前一直存在，通常会跨关卡保留。它适合保存全局配置、账号状态、匹配入口状态、当前存档槽等不依赖单局比赛的运行数据。

**注意：** `GameInstance` 不会像 `GameState` 一样自动复制给其他客户端。多人游戏里需要同步的数据应放在服务器权威对象中，再通过复制或 RPC 同步。

### GameInstanceSubsystem

`GameInstanceSubsystem` 是跟随 `GameInstance` 生命周期的模块化功能对象。它适合拆分长期存在的服务，例如存档管理、音频设置、账号服务、全局资源管理等。

如果功能只应该存在于某个世界或某个本地玩家，还可以根据需求使用 `WorldSubsystem`、`LocalPlayerSubsystem` 等更合适的 Subsystem 类型。

## 五：视角、界面与辅助工具

### Camera

相机表示玩家或系统观察世界的方式。它可以来自角色上的 `CameraComponent`，也可以来自独立的 `CameraActor`，并不只和玩家当前控制的角色有关。过场动画、观战视角、固定镜头、编辑器预览都可能使用不同的相机来源。

### HUD 与 UI

`HUD` 是与玩家显示相关的 Actor，传统上用于绘制屏幕覆盖信息；现代项目中更常用 UMG / Widget 来构建菜单、血条、背包、准星等 UI。

每个本地玩家通常拥有自己的界面层。需要所有玩家共享的数据不要直接存在 UI 里，而应该从 `GameState`、`PlayerState` 或其他权威数据源读取。

### GameplayStatics

`GameplayStatics` 是一组静态辅助函数集合，用于快速访问常见玩法操作，例如获取玩家、打开关卡、播放音效、生成对象、查找 GameMode / GameState 等。

它适合做便捷入口，但不适合把项目核心逻辑都塞进去。长期维护的系统逻辑更应该放在明确的 Actor、Component、Subsystem 或 Gameplay Ability 等结构中。

## 总结


- **GameMode：** 服务器权威规则
- **GameState：** 所有人都能看到的全局状态
- **PlayerState：** 某个玩家的可复制状态
- **Controller：** 控制意图
- **Pawn / Character：** 被控制的世界实体
- **Actor / Component：** 世界对象与模块化能力
- **GameInstance / Subsystem：** 跨关卡生命周期与长期服务
- **HUD / UI / Camera：** 本地展示、交互和观察方式
