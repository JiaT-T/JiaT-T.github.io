---
title: "UE 反射系统"
slug: "reflection-system"
date: 2026-06-17T00:00:00+08:00
draft: false
summary: "整理 Unreal Engine 反射系统的作用、常用宏、UHT/UBT 生成流程，以及它和编辑器、蓝图、序列化、GC 的关系。"
categories: ["Unreal Engine"]
tags: ["Unreal Engine", "Reflection", "UHT", "UBT", "Game Architecture"]
---

先贴一个完整流程，后面再作具体讲解：

- 通过 `UFUNCTION()`、`UPROPERTY()`、`UCLASS()` 等宏标记需要进入反射系统的数据。
- UBT 在正式编译前调用 UHT，UHT 扫描头文件中被标记的类型、函数和属性。
- UHT 生成对应的 `.generated.h` 和 `.gen.cpp` 等中间代码。
- C++ 编译器继续编译项目代码和 UHT 生成的代码。
- 运行时可以通过 `UClass`、`UFunction`、`FProperty` 等元信息访问类型、函数和属性。
- 引擎基于这些元信息驱动编辑器显示、蓝图调用、序列化、网络复制和 GC 引用追踪等系统。

## 一：什么是反射，为什么需要反射？

在 C++ 运行期，如果想要得到类、函数、变量的具体信息，通常是不可行的。C++ 编译完成后，变量名、函数签名、成员偏移等信息不会自动保留成一套可查询的运行时类型系统。

反射的目的就是让引擎在运行期也能拿到这些结构化信息。以类为例，反射数据通常包含类名、父类、成员函数、成员变量、变量类型、成员在对象内存中的偏移值等。

UE 不是反射所有 C++ 代码，只有被手动标记的类型、函数和属性才会被 UHT 捕获。UHT 会把这些信息生成到 `.generated.h`、`.gen.cpp` 等文件中，再参与后续编译。

一句话总结：

> UE 反射系统把被标记的 C++ 类、属性、函数注册到引擎的类型系统里，让引擎能在运行时识别和操作它们。

## 二：常用宏

![UE 反射系统常用宏](/images/ue-reflection-system/reflection-macros.jpeg)

### `UPROPERTY()`

表示这个成员变量要被 UE 识别。它可以参与编辑器显示、蓝图访问、序列化、GC 引用追踪、网络复制等流程。

```cpp
UPROPERTY(EditAnywhere, BlueprintReadWrite)
int32 Health;
```

### `UENUM()`

用于枚举反射，方便蓝图和编辑器使用。

```cpp
UENUM()
enum class EWeaponType : uint8
{
    Sword,
    Bow
};
```

### `USTRUCT()`

用于结构体反射，比如背包物品数据、技能配置等。

```cpp
USTRUCT()
struct FItemData
{
    GENERATED_BODY()
};
```

### `UCLASS()`

表示这个 C++ 类要进入 UE 反射系统。通常用于 `UObject` 派生类，比如 `AActor`、`UActorComponent`、`UUserWidget` 等。

```cpp
UCLASS()
class AMyActor : public AActor
{
    GENERATED_BODY()
};
```

### `UFUNCTION()`

表示这个函数要被 UE 识别。它可以暴露给蓝图，也可以用于 RPC、事件、反射调用等。

```cpp
UFUNCTION(BlueprintCallable)
void Attack();
```

## 三：UHT 与 UBT

UHT 与 UBT 通常作为独立程序参与构建流程。简单说，UBT 负责组织 UE 项目的整体构建，UHT 负责从头文件里提取反射信息并生成代码。

### UHT（Unreal Header Tool）

UHT 的核心职责是扫描头文件，找到 UE 特有的反射宏，例如 `UCLASS()`、`USTRUCT()`、`UENUM()`、`UPROPERTY()`、`UFUNCTION()`，然后生成对应的反射辅助代码。

`.generated.h` 主要包含 `GENERATED_BODY()` 展开所需的声明、注册入口和样板代码。

`.gen.cpp` 主要负责生成类、属性、函数等元信息的注册代码，让运行时能构造出引擎可识别的 `UClass`、`FProperty`、`UFunction` 等对象。

### UBT（Unreal Build Tool）

在传统 C++ 开发中，构建系统通常通过 CMake、Visual Studio 工程或其他工程文件来描述。UE 需要跨平台构建，同时代码规模很大，所以使用了自己的构建系统 UBT。

UBT 的主要职责：

- **解析依赖：** UE 的模块通常带有 `.Build.cs` 和 `.Target.cs` 文件，用来描述模块依赖、目标类型和构建设置。UBT 会在编译前解析这些依赖关系。
- **调度构建：** UBT 会检查文件改动，按需调用 UHT 生成反射代码，再调用 MSVC、Clang 等编译器完成实际编译，最后输出 `.exe`、`.dll` 等产物。

## 四：运行时的元信息层

反射信息虽然由 UHT 生成成 C++ 代码，但在运行时会表现为一组描述其他 C++ 类型的对象。也就是用 `UClass`、`UFunction`、`FProperty` 这类对象，去描述我们自己写的 `AMyCharacter`、`Health`、`Attack()` 等类、属性和函数。

为什么需要单独的元信息层？

> 因为普通 C++ 类和变量在编译后不会天然保留一套可供引擎查询的名字、类型、偏移、标记等信息。运行时如果只拿到对象地址，引擎不知道哪个成员叫 `Health`，也不知道它是不是蓝图可读写、是否需要序列化、是否是 UObject 引用。

UHT 生成的反射注册代码会把这些信息整理出来。例如某个类的元信息里可以保存类名 `"AMyCharacter"`、类大小 `sizeof(AMyCharacter)`，以及属性数组。属性元信息中又可以保存 `"Health"`、属性类型、对象内偏移和各种标记。

### `UClass`

通过 `UClass`，UE 可以知道：

- 类名
- 父类
- 类大小
- 构造方式
- 有哪些属性
- 有哪些函数
- 有哪些接口
- 默认对象 CDO
- 蓝图元数据

### `UFunction`

`UFunction` 表示一个函数的元信息，它能描述：

- 函数名
- 参数列表
- 返回值
- 是否蓝图可调用
- 是否 RPC
- 是否事件

### `FProperty`

`FProperty` 表示一个属性的元信息，它能描述：

- 属性名
- 属性类型
- 偏移量
- 是否可编辑
- 是否蓝图可读写
- 是否需要序列化
- 是否是 UObject 引用

## 五：反射与 GC 的关系

UE 的 GC 需要知道哪些 `UObject` 还可以被访问。对于被 `UPROPERTY()` 标记的 UObject 引用，反射系统会记录属性类型和内存偏移。GC 做可达性分析时，就能根据这些元信息找到对象内部保存的 UObject 指针，并继续沿着引用关系遍历。

如果一个 UObject 指针只是普通裸指针，而且没有通过 `UPROPERTY()` 或其他 GC 引用收集机制暴露给引擎，GC 通常就无法把它当作有效引用追踪。这也是 UE 中 UObject 引用经常需要配合 `UPROPERTY()` 使用的原因。

## Reference

- [Unreal C++ 反射实现分析（一）](https://zhuanlan.zhihu.com/p/60622181)
- [Unreal C++ 反射实现分析（二）](https://zhuanlan.zhihu.com/p/656818991)
