---
title: "UE Gameplay Ability System（GAS）"
slug: "gameplay-ability-system"
summary: "整理 GAS 的核心组件、技能生命周期、属性与效果、异步任务及多人预测逻辑。"
categories: ["Unreal Engine"]
tags: ["Unreal Engine", "GAS", "Gameplay Ability", "Ability Task", "Networking"]
date: "2026-07-28T04:13:04.000Z"
lastmod: "2026-07-28T04:17:42.000Z"
draft: false
yuque_slug: "ram4tq4ttst4qpgi"
source: "https://www.yuque.com/u62694975/iaaa/ram4tq4ttst4qpgi"
---

<a id="0137ea05"></a>
# UE 的 GAS 是什么

<a id="ua8b6f502"></a><strong>GAS（Gameplay Ability System）</strong>是 UE 用于构建技能、属性、Buff/Debuff、状态控制和多人同步的一套玩法框架。它主要解决的不是“播放一个技能动画”，而是技能规模扩大以后出现的复杂问题：

- <a id="u5bd25d0e"></a>技能能否释放；
- <a id="u3c8597c6"></a>消耗与冷却；
- <a id="ucd664005"></a>动画、命中和伤害的时序；
- <a id="u6ef8b701"></a>眩晕、霸体、无敌等状态互斥；
- <a id="u5ce50649"></a>Buff叠层和持续时间；
- <a id="u9ae9a57c"></a>客户端预测与服务器校验；
- <a id="u8ae00e19"></a>特效、音效和玩法逻辑分离。

<a id="u403ebe5a"></a>可以把GAS概括为：

<a id="fAeCA"></a>
```plain
ASC负责统筹
GA负责执行行为
GE负责修改状态
Attribute负责保存数值
Tag负责描述和约束状态
AbilityTask负责异步流程
GameplayCue负责表现
```

<a id="yhus8"></a>

---

<a id="161577d0"></a>
# 一、GAS的核心组成

<a id="a1406b12"></a>
## 1. Ability System Component：系统中枢

<a id="uef48d18c"></a>`UAbilitySystemComponent`，简称 <strong>ASC</strong>，是Actor进入GAS体系的入口。

<a id="u27661bee"></a>它负责管理：

- <a id="ua39e66fe"></a>当前拥有的技能；
- <a id="u9f42bcdf"></a>技能的授予、激活和移除；
- <a id="u525b667a"></a>Attribute和AttributeSet；
- <a id="u1dec4e9f"></a>当前生效的GameplayEffect；
- <a id="ue6e1c517"></a>当前拥有的GameplayTag；
- <a id="uae625ac2"></a>GameplayEvent；
- <a id="u686d8c88"></a>技能网络复制和预测。

<a id="u7078253e"></a>一般让Actor实现`IAbilitySystemInterface`，通过`GetAbilitySystemComponent()`返回ASC。ASC既可以放在Character上，也可以放在PlayerState上。将ASC放在PlayerState上，可以让属性、技能和长时间冷却在角色死亡、换Pawn后继续存在。([Epic Games Developers](<https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-ability-system-component-and-gameplay-attributes-in-unreal-engine?utm_source=chatgpt.com>))

<a id="63e39761"></a>
### ASC放在哪里

<a id="uf73cace6"></a><strong>放在Character：</strong>

- <a id="uee753a11"></a>实现简单；
- <a id="u0a5a6bea"></a>适合AI、怪物、生命周期与角色一致的对象；
- <a id="uf9e678a2"></a>Character销毁时，ASC及其状态通常也随之销毁。

<a id="u0c5fcc1f"></a><strong>放在PlayerState：</strong>

- <a id="u13c32ad0"></a>适合玩家角色；
- <a id="u5c7c8346"></a>Pawn死亡重生后仍可保留等级、技能和冷却；
- <a id="ue5250649"></a>需要处理PlayerState和新Pawn之间的初始化关系。

<a id="ub8de908f"></a>面试中经常问：

<a id="ud7f0b9ed"></a>玩家死亡并重新生成Character，技能冷却不应该重置，ASC应该放在哪里？

<a id="ud4badcb2"></a>通常回答：放在PlayerState，PlayerState作为长期Owner，当前Character作为技能实际操作的Avatar。

<a id="NHd98"></a>

---

<a id="24b17875"></a>
## 2. Gameplay Ability：一个可执行的能力

<a id="uf7181bfc"></a>`UGameplayAbility`，简称 <strong>GA</strong>，描述“角色要做什么”。

<a id="u1bf927c2"></a>例如：

- <a id="ud0f34c02"></a>普通攻击；
- <a id="ueed3c7c9"></a>翻滚；
- <a id="uf11574c4"></a>冲刺；
- <a id="ue91c8729"></a>格挡；
- <a id="ud6645e94"></a>喝药；
- <a id="u4297bdca"></a>火球术；
- <a id="u1102f56d"></a>受击；
- <a id="u70914d5a"></a>死亡；
- <a id="u7047cf9a"></a>被动技能。

<a id="ub1b078bf"></a>GA不只是一个函数。它可以跨越多帧执行，等待动画、输入、命中数据或GameplayEvent，并在结束或取消时统一清理。它支持成本、冷却、标签约束、网络执行策略和客户端预测。([Epic Games Developers](<https://dev.epicgames.com/documentation/unreal-engine/using-gameplay-abilities-in-unreal-engine?lang=en-US>))

<a id="e8b71c05"></a>
### 一个Ability的基本生命周期

<a id="Jm9qL"></a>
```plain
服务器授予Ability
        ↓
GiveAbility → FGameplayAbilitySpec
        ↓
TryActivateAbility
        ↓
CanActivateAbility
        ↓
ActivateAbility
        ↓
CommitAbility
        ↓
启动AbilityTask并等待动画/输入/事件
        ↓
造成效果或修改状态
        ↓
EndAbility / CancelAbility
```

<a id="u3d09aa59"></a>`GiveAbility`通常只能由权威端执行，并返回`FGameplayAbilitySpecHandle`。`TryActivateAbility`会先检查能否激活，再真正调用激活逻辑；`CommitAbility`一般负责应用技能消耗和冷却；能力执行结束后必须调用`EndAbility`，否则GAS会继续认为技能处于激活状态，相关阻塞标签也可能一直存在。([Epic Games Developers](<https://dev.epicgames.com/documentation/unreal-engine/using-gameplay-abilities-in-unreal-engine?lang=en-US>))

<a id="df18c9a1"></a>
### CommitAbility为什么重要

<a id="ud83a26d3"></a>一般不要一进入`ActivateAbility`就无条件扣蓝、扣体力。

<a id="u3d14e68c"></a>更典型的流程是：

<a id="qqrCo"></a>
```plain
ActivateAbility
→ 检查目标或开始瞄准
→ 确定技能确实可以执行
→ CommitAbility
→ 扣除资源并进入冷却
→ 执行后续技能流程
```

<a id="ubbfe1067"></a>如果`CommitAbility`失败，通常应立即结束Ability。

<a id="C8tr1"></a>

---

<a id="db667a63"></a>
## 3. Attribute与AttributeSet：角色数值

<a id="u5ebb6814"></a>`Attribute`是GAS管理的浮点型玩法数值，例如：

<a id="aVI0H"></a>
```plain
Health
MaxHealth
Mana
Stamina
AttackPower
Defense
MoveSpeed
CriticalRate
```

<a id="u275f81cd"></a>这些属性通常放在继承自`UAttributeSet`的类中。当前官方文档要求AttributeSet及其Attribute在原生C++中定义。([Epic Games Developers](<https://dev.epicgames.com/documentation/unreal-engine/gameplay-effects-for-the-gameplay-ability-system-in-unreal-engine?lang=en-US>))

<a id="37fd2211"></a>
### Base Value与Current Value

<a id="u6d898ba3"></a>`FGameplayAttributeData`包含两个重要值：

- <a id="uc32ad64e"></a><strong>Base Value</strong>：基础值或永久值；
- <a id="u87e6b361"></a><strong>Current Value</strong>：考虑当前临时Modifier后的最终值。

<a id="u173c4fc2"></a>例如：

<a id="n6ZnQ"></a>
```plain
基础移动速度：600
减速Debuff：-30%
Current MoveSpeed：420
```

<a id="u85582519"></a>减速结束后，Current恢复到600，而Base没有改变。AttributeSet将属性集中管理，并支持属性复制、临时修改和变化回调。([Epic Games Developers](<https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-attributes-and-attribute-sets-for-the-gameplay-ability-system-in-unreal-engine?utm_source=chatgpt.com>))

<a id="a02001d5"></a>
### 常见回调

<a id="preattributechange"></a>
#### PreAttributeChange

<a id="uc31fc131"></a>属性变化前执行，常用于限制范围：

<a id="PFrqa"></a>
```cpp
void UMyAttributeSet::PreAttributeChange(
    const FGameplayAttribute& Attribute,
    float& NewValue)
{
    Super::PreAttributeChange(Attribute, NewValue);

    if (Attribute == GetMoveSpeedAttribute())
    {
        NewValue = FMath::Clamp(NewValue, 0.0f, 1200.0f);
    }
}
```

<a id="u0a56f31a"></a>不建议在这里处理死亡、受击等复杂玩法反应。

<a id="postgameplayeffectexecute"></a>
#### PostGameplayEffectExecute

<a id="uc0ee657b"></a>Instant GameplayEffect完成修改后执行，适合：

- <a id="u81b7897b"></a>把Health限制在`0~MaxHealth`；
- <a id="uc8a16b93"></a>处理Damage元属性；
- <a id="ub25b9417"></a>触发死亡；
- <a id="u9d12459d"></a>更新玩法状态。

<a id="u00ae84c1"></a>官方也将`PreAttributeChange`定位为数值约束，将`PostGameplayEffectExecute`定位为效果执行后的最终处理和玩法反应。([Epic Games Developers](<https://dev.epicgames.com/documentation/unreal-engine/gameplay-effects-for-the-gameplay-ability-system-in-unreal-engine?lang=en-US>))

<a id="JYO6I"></a>

---

<a id="4693cbda"></a>
## 4. Gameplay Effect：改变角色状态

<a id="u72a4c5b5"></a>`UGameplayEffect`，简称 <strong>GE</strong>，负责描述“角色状态如何改变”。

<a id="u9beb39ca"></a>例如：

- <a id="u59e0477f"></a>造成100点伤害；
- <a id="u2501bca8"></a>恢复50点生命；
- <a id="u588fdffe"></a>增加20%攻击力，持续10秒；
- <a id="uec6609c2"></a>每秒受到5点毒伤，持续8秒；
- <a id="u8ee3c351"></a>永久增加最大生命；
- <a id="u05745692"></a>消耗30点体力；
- <a id="u85e3d670"></a>添加眩晕状态；
- <a id="ua8e59891"></a>添加技能冷却。

<a id="u218523e9"></a>GameplayEffect本身通常是不可变的数据资产；运行时真正携带等级、来源、目标、动态数值和上下文的是`FGameplayEffectSpec`。([Epic Games Developers](<https://dev.epicgames.com/documentation/unreal-engine/gameplay-effects-for-the-gameplay-ability-system-in-unreal-engine?lang=en-US>))

<a id="3b784434"></a>
### GE的三种持续类型

<table id="RzYnO"><colgroup><col width="250"><col width="250"><col width="250"></colgroup><tbody><tr id="uf31f33d5"><td id="ue854c5f1"><p id="udc1d5212"><span id="u070b1c8b">类型</span></p></td><td id="u8ffc2a86"><p id="u3247aa21"><span id="u95bfbe9d">用途</span></p></td><td id="uc93d5366"><p id="u5147ecb3"><span id="u2e7b45fb">示例</span></p></td></tr><tr id="uf7662191"><td id="u24d45804"><p id="u41a84f99"><span id="u191a3eed">Instant</span></p></td><td id="u9aaa9504"><p id="u81ca27e9"><span id="u79da0446">立即执行，不进入Active GE容器</span></p></td><td id="u1e074f4f"><p id="uc3aa26dc"><span id="ua2695f85">伤害、治疗、永久加点</span></p></td></tr><tr id="ud654b113"><td id="u4284b61a"><p id="u1bd9db4b"><span id="u5dc4da5e">Has Duration</span></p></td><td id="u5980da71"><p id="u0263016e"><span id="u562d8b53">持续一段时间</span></p></td><td id="u2738d492"><p id="ue7cdaae8"><span id="ud454b610">10秒加速、5秒眩晕</span></p></td></tr><tr id="ud55787f6"><td id="ube641c76"><p id="u8b8a6744"><span id="uaf4f7032">Infinite</span></p></td><td id="u39f1bae5"><p id="u06619675"><span id="u575b09f4">无限持续，直到主动移除</span></p></td><td id="ud0739da1"><p id="ud27bb0d9"><span id="ufb2a7560">装备加成、被动状态</span></p></td></tr></tbody></table>

<a id="u0607fc4c"></a>带持续时间的GE会进入ASC的Active Gameplay Effects Container；Instant GE执行后不会作为持续效果保存在其中。Periodic GE则会按设定周期重复执行。([Epic Games Developers](<https://dev.epicgames.com/documentation/unreal-engine/gameplay-effects-for-the-gameplay-ability-system-in-unreal-engine?lang=en-US>))

<a id="9968dcae"></a>
### Modifier、MMC与Execution Calculation

<a id="modifier"></a>
#### Modifier

<a id="u24e8064b"></a>适合简单数值操作：

<a id="Fo6Vh"></a>
```plain
Health - 100
AttackPower + 20
MoveSpeed × 0.7
```

<a id="mmc"></a>
#### MMC

<a id="u2b69c4d6"></a>`UGameplayModMagnitudeCalculation`用于计算一个Modifier的Magnitude。

<a id="u0e22fb49"></a>例如：

<a id="afjA9"></a>
```plain
护盾值 = 技能等级 × 50 + 法术强度 × 0.6
```

<a id="ufcc97220"></a>它主要负责“算出一个数”，然后交给Modifier使用。([Epic Games Developers](<https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/GameplayAbilities/UGameplayModMagnitudeCalculation/CalculateBaseMag-?lang=en-US&utm_source=chatgpt.com>))

<a id="execution-calculation"></a>
#### Execution Calculation

<a id="u7cffbec5"></a>`UGameplayEffectExecutionCalculation`适合复杂计算，并且可以一次输出多个属性修改。

<a id="u4dc7d1dc"></a>例如伤害公式：

<a id="crf3a"></a>
```plain
基础伤害
→ 读取攻击者攻击力
→ 读取目标防御力
→ 计算暴击
→ 计算元素抗性
→ 计算最终Damage
→ 同时产生生命削减、韧性削减和吸血
```

<a id="u02f8257c"></a>Execution可以读取来源和目标的属性快照，再向输出中添加多个Modifier。([Epic Games Developers](<https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/GameplayAbilities/UGameplayEffectExecutionCalculat-/Execute?utm_source=chatgpt.com>))

<a id="u8d34d6ef"></a>面试中经常问：

<a id="u01d8d954"></a>MMC和Execution Calculation有什么区别？

<a id="u5ed03d68"></a>可以回答：

<a id="u6dc50fbe"></a>MMC通常为一个Modifier计算Magnitude，更适合可复用的单值公式；Execution Calculation适合一次执行涉及来源属性、目标属性、多步判断和多个输出的复杂公式，例如伤害结算。

<a id="QI2lt"></a>

---

<a id="aa052c5b"></a>
## 5. Gameplay Tag：GAS的状态语言

<a id="u1278c166"></a>GameplayTag是层级化标签，例如：

<a id="P8fYQ"></a>
```plain
Ability.Attack.Light
Ability.Attack.Heavy
Ability.Movement.Dodge

State.Attacking
State.Stunned
State.Dead
State.Invincible

Cooldown.Skill.Fireball
Event.Melee.Hit
GameplayCue.Hit.Fire
```

<a id="u345aaf9a"></a>Tag不是普通字符串，也不仅是Enum。它们可以形成层级关系：

<a id="K1FGl"></a>
```plain
State.CrowdControl.Stun
```

<a id="u5b6cfa35"></a>同时也匹配更上层的：

<a id="Qglik"></a>
```plain
State.CrowdControl
State
```

<a id="u30ef813b"></a>GameplayTag可以用于描述对象类型、当前状态、事件和触发条件。([Epic Games Developers](<https://dev.epicgames.com/documentation/en-us/unreal-engine/using-gameplay-tags-in-unreal-engine>))

<a id="a6d8e72d"></a>
### Tag在Ability中的典型用途

<a id="ub1ae0b84"></a>假设角色处于：

<a id="XtvCq"></a>
```plain
State.Stunned
```

<a id="ucb9608c7"></a>翻滚Ability可以配置：

<a id="YUdTc"></a>
```plain
ActivationBlockedTags:
    State.Stunned
    State.Dead
```

<a id="u76eae92e"></a>攻击期间授予：

<a id="rod6g"></a>
```plain
ActivationOwnedTags:
    State.Attacking
```

<a id="u084c6496"></a>重攻击启动时，可以配置：

<a id="EmvAv"></a>
```plain
CancelAbilitiesWithTag:
    Ability.Attack.Light
```

<a id="u28582cfa"></a>GAS原生支持使用Tag：

- <a id="u55a45703"></a>阻止其他技能；
- <a id="u3eed8ad6"></a>取消正在执行的技能；
- <a id="ud87a1d3a"></a>要求角色必须具有某状态；
- <a id="ub6e699e4"></a>要求角色不得具有某状态；
- <a id="ub45e081f"></a>判断目标是否可被技能命中。([Epic Games Developers](<https://dev.epicgames.com/documentation/unreal-engine/using-gameplay-abilities-in-unreal-engine?lang=en-US>))

<a id="u9092afa9"></a>这比散落在各处的布尔变量更适合复杂技能系统：

<a id="Xsep5"></a>
```cpp
if (!bDead && !bStunned && !bAttacking && !bClimbing && ...)
```

<a id="u64c47954"></a>会逐渐变成：

<a id="YwIMk"></a>
```plain
ActivationBlockedTags:
    State.Dead
    State.Stunned
    State.Climbing
```

<a id="odKcy"></a>

---

<a id="2c9eb1c0"></a>
## 6. Ability Task：跨帧异步流程

<a id="ue4447f54"></a>GameplayAbility通常不依靠自己的Tick驱动流程，而是启动`UAbilityTask`。

<a id="u97aaca7a"></a>常见Task包括：

- <a id="u1f5a7589"></a>播放Montage并等待；
- <a id="u57e36b0a"></a>等待GameplayEvent；
- <a id="u8d66df77"></a>等待输入按下或释放；
- <a id="ubb766732"></a>等待延时；
- <a id="ub997d2e0"></a>等待目标数据；
- <a id="u9ed012be"></a>等待属性变化；
- <a id="u6faef421"></a>移动角色到指定位置。

<a id="ua64eda04"></a>AbilityTask可以跨越多帧，通过Delegate或蓝图输出引脚通知Ability，并会在所属Ability结束时最迟终止。([Epic Games Developers](<https://dev.epicgames.com/documentation/unreal-engine/gameplay-ability-tasks-in-unreal-engine?lang=en-US>))

<a id="u2cf970b2"></a>例如蓄力攻击：

<a id="RU3bN"></a>
```plain
ActivateAbility
→ WaitInputRelease
→ 玩家持续按住
→ 计算蓄力时间
→ 输入释放
→ 播放攻击Montage
→ 等待命中事件
→ 应用伤害GE
→ EndAbility
```

<a id="f15b0fdb"></a>
### AbilityTask和普通异步任务的区别

<a id="ufa560235"></a>AbilityTask并不等同于“把工作放到其他CPU线程”。

<a id="ua9c54008"></a>它主要是 <strong>玩法流程上的异步等待</strong>：

- <a id="u7f67e5b6"></a>等动画完成；
- <a id="ubb7387ec"></a>等网络目标数据；
- <a id="u3f47a1da"></a>等玩家输入；
- <a id="u006ff42c"></a>等事件；
- <a id="ua0f31b39"></a>等时间。

<a id="ub547127b"></a>它通常仍然参与游戏线程上的Ability流程。

<a id="GzUfW"></a>

---

<a id="f8259d1b"></a>
## 7. Gameplay Cue：只负责表现

<a id="ud114069b"></a>GameplayCue用于表现性反馈：

- <a id="ue4665645"></a>Niagara特效；
- <a id="u2fe43167"></a>音效；
- <a id="ud021f706"></a>镜头震动；
- <a id="u36225385"></a>材质变化；
- <a id="ud3f212ee"></a>命中特效；
- <a id="uc8200c1a"></a>Buff持续特效。

<a id="ud8c9663d"></a>常见生命周期：

- <a id="uc9a34443"></a>`OnActive`；
- <a id="u63978a08"></a>`WhileActive`；
- <a id="u5495b838"></a>`Removed`；
- <a id="u691c3b0d"></a>`Executed`。

<a id="u50419917"></a>GameplayCue需要使用以`GameplayCue`开头的Tag，例如：

<a id="s9tfo"></a>
```plain
GameplayCue.Hit.Slash
GameplayCue.Buff.Burning
```

<a id="ufb09b70d"></a>GameplayCue主要是网络友好的外观表现机制，不应承载扣血、添加状态等关键玩法逻辑。官方明确指出Cue不使用可靠复制，因此关键玩法结果不能依赖Cue是否成功播放。([Epic Games Developers](<https://dev.epicgames.com/documentation/unreal-engine/gameplay-effects-for-the-gameplay-ability-system-in-unreal-engine?lang=en-US>))

<a id="uf0e59394"></a>正确关系是：

<a id="GynpI"></a>
```plain
GameplayEffect决定目标受到伤害
GameplayCue负责播放受击火花和音效
```

<a id="ThVqy"></a>

---

<a id="65d23403"></a>
# 二、用你的近战攻击项目理解GAS

<a id="uacd448aa"></a>假设把你现在UE5 RPG项目里的近战攻击改成GAS，可以设计成下面这样。

<a id="099197a4"></a>
## 1. 按下攻击键

<a id="u31627b55"></a>Enhanced Input不直接调用“扣血函数”，而是让ASC尝试激活：

<a id="pwIN8"></a>
```plain
Ability.Attack.Light
```

<a id="284ef59a"></a>
## 2. GAS检查能否激活

<a id="uba1fa955"></a>检查：

<a id="D9b3V"></a>
```plain
角色是否死亡
角色是否眩晕
角色是否正在攀爬
体力是否足够
技能是否处于冷却
当前是否允许进入下一段连击
```

<a id="u74612945"></a>这些条件主要由Tag、Cost GE、Cooldown GE和`CanActivateAbility`共同处理。

<a id="588b368b"></a>
## 3. 激活攻击Ability

<a id="T7ZOA"></a>
```plain
GA_LightAttack
→ CommitAbility
→ 应用体力消耗
→ 应用攻击冷却
→ 添加State.Attacking
→ 播放Montage
```

<a id="e30bafce"></a>
## 4. 动画到达命中帧

<a id="u38767578"></a>Anim Notify发送GameplayEvent：

<a id="OxPq5"></a>
```plain
Event.Melee.Trace.Begin
```

<a id="u1f4c71a5"></a>Ability等待该Event，然后开始武器Trace。

<a id="e82b4dcb"></a>
## 5. 检测到目标

<a id="u6ce7e0c4"></a>生成Effect Spec：

<a id="j2K5M"></a>
```plain
GE_Damage
```

<a id="ucf6fddc7"></a>其中保存：

- <a id="u65b21f76"></a>攻击者；
- <a id="uf4501a78"></a>目标；
- <a id="u4e57f3da"></a>技能等级；
- <a id="u174f03be"></a>命中位置；
- <a id="ucfc8495d"></a>动态伤害；
- <a id="u0e347987"></a>暴击信息；
- <a id="u60b170d6"></a>Effect Context。

<a id="u99747b37"></a>之后将Spec应用到目标ASC。

<a id="ce5e187b"></a>
## 6. 目标结算伤害

<a id="u6f2354e2"></a>Execution Calculation读取：

<a id="q3F9W"></a>
```plain
攻击者AttackPower
目标Defense
技能倍率
暴击率
伤害类型
目标抗性
```

<a id="ufe50e236"></a>算出最终Damage。

<a id="u3874b9c6"></a>目标AttributeSet在`PostGameplayEffectExecute`中：

<a id="xmiUj"></a>
```plain
Health -= Damage
→ Clamp Health
→ Health <= 0时进入死亡流程
```

<a id="f75bff19"></a>
## 7. 播放表现

<a id="u1750ca3d"></a>触发：

<a id="AuYHh"></a>
```plain
GameplayCue.Hit.Slash
```

<a id="u2cf6f5dc"></a>播放粒子、声音、受击闪白，但不在Cue里执行扣血。

<a id="30b971c8"></a>
## 8. 攻击完成或被打断

<a id="Uklbx"></a>
```plain
Montage完成
→ EndAbility

收到State.Stunned
→ CancelAbility
→ 停止Montage
→ 清理Trace
→ 移除State.Attacking
```

<a id="ud4de0805"></a>完整数据流就是：

<a id="WH63c"></a>
```plain
输入
→ ASC
→ GameplayAbility
→ AbilityTask播放动画
→ GameplayEvent开启攻击检测
→ TargetData
→ GameplayEffectSpec
→ Execution Calculation
→ AttributeSet
→ GameplayCue
→ EndAbility
```

<a id="MbOZn"></a>

---

<a id="465c410a"></a>
# 三、GAS的多人网络逻辑

<a id="ue6777b4e"></a>GAS并不是让客户端直接决定伤害，而是在<strong>服务器权威</strong>的基础上，提供本地预测来改善操作手感。

<a id="local-predicted"></a>
## Local Predicted

<a id="u9e89ad3d"></a>玩家按下翻滚时：

1. <a id="ufa063534"></a>客户端立即播放翻滚和预测性状态；
2. <a id="u7ee7b8f9"></a>同时向服务器申请激活；
3. <a id="u8beae408"></a>服务器重新检查体力、冷却、Tag和权限；
4. <a id="ub5632734"></a>服务器接受则继续；
5. <a id="uae783069"></a>服务器拒绝则客户端撤销可回滚的预测结果。

<a id="u6e1af632"></a>官方提供四种主要Net Execution Policy：

- <a id="ufe5ab39d"></a>Local Predicted；
- <a id="u5997f756"></a>Local Only；
- <a id="u5ed5f1e8"></a>Server Initiated；
- <a id="u67309b35"></a>Server Only。([Epic Games Developers](<https://dev.epicgames.com/documentation/unreal-engine/using-gameplay-abilities-in-unreal-engine?lang=en-US>))

<a id="1cd08888"></a>
### 哪些技能适合Local Predicted

- <a id="ua5063a7d"></a>普通攻击；
- <a id="ub20264a7"></a>翻滚；  
  -冲刺；
- <a id="ufc1bf9a8"></a>跳跃；
- <a id="u2ea43442"></a>本地玩家频繁使用且对延迟敏感的技能。

<a id="b80b1947"></a>
### 哪些适合Server Only或Server Initiated

- <a id="u19ea1632"></a>AI能力；
- <a id="ubae48fda"></a>服务器控制的环境机关；
- <a id="u3f6b7fcd"></a>权威掉落；
- <a id="ue03612b4"></a>只在服务端完成的被动结算；
- <a id="ub7402736"></a>不需要客户端即时响应的逻辑。

<a id="u0a901bb9"></a>需要注意：可预测的非Instant GE通常更容易在服务器拒绝时回滚，而伤害等Instant属性变化不能简单依赖同样的回滚方式。因此通常让客户端预测动作、动画和部分状态，最终伤害仍由服务器权威确认。([Epic Games Developers](<https://dev.epicgames.com/documentation/en-us/unreal-engine/understanding-the-unreal-engine-gameplay-ability-system?utm_source=chatgpt.com>))

<a id="bhBb5"></a>

---

<a id="f104bb93"></a>
# 四、Ability的实例化策略

<a id="u5ff46851"></a>GAS提供三种Ability Instancing Policy。

<a id="non-instanced"></a>
## Non-Instanced

<a id="u53b3c702"></a>使用Ability的CDO执行，不生成实例。

<a id="u37020411"></a>优点：

- <a id="uf7c3ef13"></a>开销最低。

<a id="u016bf0af"></a>限制：

- <a id="u42ad61f3"></a>不能保存运行时成员状态；
- <a id="ucacfdc6d"></a>不能绑定依赖实例的Delegate；
- <a id="uc1bc37ef"></a>不能使用蓝图图表执行核心逻辑；
- <a id="uc2d11484"></a>不能复制成员变量或处理Ability自身RPC。

<a id="u1d3e9832"></a>适合大规模单位频繁执行、且完全无状态的简单能力。

<a id="instanced-per-actor"></a>
## Instanced Per Actor

<a id="u0246bf04"></a>每个Actor持有一个Ability实例，多次执行重复使用。

<a id="uf12c5be0"></a>优点：

- <a id="ua246b030"></a>可保存成员变量；
- <a id="u4c797c68"></a>适合复制和RPC；
- <a id="u642a11b9"></a>不会每次释放都创建新UObject。

<a id="u16d49dd6"></a>缺点：

- <a id="uc2b49e5d"></a>每次激活前必须清理上一次残留状态。

<a id="u7b6bf982"></a>大多数角色技能可以优先考虑这一策略。

<a id="instanced-per-execution"></a>
## Instanced Per Execution

<a id="u637e22bb"></a>每次激活都创建一个新实例。

<a id="u326e5d5f"></a>优点：

- <a id="u753bef49"></a>每次状态完全独立；
- <a id="u390cc4f4"></a>可以让同一Ability并发执行多份。

<a id="u4b61c168"></a>缺点：

- <a id="uad341732"></a>对象创建成本最高。

<a id="u2c0af3cf"></a>适合低频、复杂、可能并发执行的能力。([Epic Games Developers](<https://dev.epicgames.com/documentation/unreal-engine/using-gameplay-abilities-in-unreal-engine?lang=en-US>))

<a id="dew6g"></a>

---

<a id="4082db57"></a>
# 五、GAS最常见的错误

<a id="5da306bd"></a>
## 1. 忘记EndAbility

<a id="uc2236c91"></a>结果：

- <a id="u198720ff"></a>Ability永远处于Active；
- <a id="u2146bbe7"></a>激活标签不消失；
- <a id="u03364223"></a>被它阻塞的其他Ability无法使用；
- <a id="uec82b558"></a>AbilityTask和Delegate不能正常结束。

<a id="652f4456"></a>
## 2. 在GameplayCue里写玩法逻辑

<a id="u6d5277ee"></a>Cue可能丢失，只能用于表现，不能负责扣血或决定死亡。

<a id="1bf40ca4"></a>
## 3. 直接修改Health

<a id="u102a18a0"></a>例如：

<a id="qC3g5"></a>
```cpp
Health -= Damage;
```

<a id="u5c43ee6c"></a>这样会绕过：

- <a id="u90f4ae66"></a>GE上下文；
- <a id="u511cb497"></a>网络预测；
- <a id="u1a5e4539"></a>Effect Tag；
- <a id="u953e44ca"></a>属性回调；
- <a id="u4d5897f6"></a>伤害来源记录；  
  -统一结算流程。

<a id="ub6f96cad"></a>复杂项目中应尽量通过GE修改GAS Attribute。

<a id="0512a260"></a>
## 4. 所有状态都做成Attribute

<a id="u86cf2c0f"></a>`Health`适合Attribute，但“眩晕”“正在攻击”“无敌”更适合GameplayTag。

<a id="uc14f863c"></a>一般：

<a id="iBKHV"></a>
```plain
连续数值 → Attribute
离散状态 → GameplayTag
行为流程 → GameplayAbility
数值变化 → GameplayEffect
外观反馈 → GameplayCue
```

<a id="c42606f2"></a>
## 5. 在Ability中堆积所有伤害公式

<a id="uf4b227dd"></a>伤害公式应尽量放在可复用的MMC或Execution Calculation中，而不是每个攻击GA各写一次。

<a id="4b9d3804"></a>
## 6. Ability取消时没有清理外部资源

<a id="uca4c63c8"></a>需要清理：

- <a id="uf978f330"></a>Montage；
- <a id="ue0fc0e5f"></a>碰撞检测；
- <a id="ub61246b6"></a>定时器；
- <a id="uc38c5490"></a>自定义Delegate；
- <a id="u436aafec"></a>临时生成的Actor；
- <a id="u37fb6996"></a>锁定目标；
- <a id="uc31c69cb"></a>输入模式。

<a id="u4778c5d8"></a>AbilityTask能够随Ability结束，但Ability之外手工创建的资源仍需要自己管理。

<a id="g0vGX"></a>

---

<a id="e0e2a2ac"></a>
# 六、总结GAS：

<a id="u1f4ea890"></a><strong>GAS以ASC为中枢，用GA组织行为流程，用GE修改Attribute和Tag，用AbilityTask处理跨帧时序，用GameplayCue分离表现，并通过服务器权威与本地预测支持多人游戏。</strong>

原文：[GAS](<https://www.yuque.com/u62694975/iaaa/ram4tq4ttst4qpgi>)
