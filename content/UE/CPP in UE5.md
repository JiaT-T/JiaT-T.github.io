---
title: "C++ 管理引擎资产的简单练习"
date: 2026-06-26
author: "槐aaaa"
archiveGroup: "unreal"
---

通过这个小练习，完成后应该了解到的是：**C++ 负责定义逻辑与接口，而 UE 编辑器则负责创建与摆放对象、调整参数以及最终 Shader 的实现。**同时，也能够**学习 UE C++ 怎么把变量暴露到编辑器、怎么创建组件、怎么引用资产、怎么生成动态材质实例、怎么给蓝图提供接口**

这个练习也非常简单：通过 C++ 创建一个 Actor 对象，让它出现在 UE 的编辑器里，并且我们能够通过编辑器的 Details 面板来调整这个 Actor 的颜色、粗糙度、自发光强度等等

注：这里我使用的是 UE5.6 版本

## 创建一个 C++ 类

点击编辑器上方的 **工具** -> **新建 C++ 类** -> **Actor**，命名为“MaterialShowcaseActor”，之后创建

此时 UE 会自动生成两个文件：MaterialShowcaseActor.h 和 MaterialShowcaseActor.cpp，与大多数类一样，前者用于声明，后者用于定义，模板如下：

```cpp
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MaterialShowcaseActor.generated.h"

UCLASS()
// 注意这里的类名是项目的名字 + "_API"
class UE5_MATERIAL_LAB_API AMaterialShowcaseActor : public AActor
{
    GENERATED_BODY()

public:	
    // Sets default values for this actor's properties
    AMaterialShowcaseActor();

protected:
    // Called when the game starts or when spawned
    virtual void BeginPlay() override;

public:	
    // Called every frame
    virtual void Tick(float DeltaTime) override;
};
```

```cpp
#include "MaterialShowcaseActor.h"
#include "Components/StaticMeshComponent.h"
#include "Materials/MaterialInstanceDynamic.h"

// Sets default values
AMaterialShowcaseActor::AMaterialShowcaseActor()
{
    // Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
    PrimaryActorTick.bCanEverTick = true;
}

// Called when the game starts or when spawned
void AMaterialShowcaseActor::BeginPlay()
{
    Super::BeginPlay();
}

// Called every frame
void AMaterialShowcaseActor::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
}
```

可以看到，模板代码中包含一些奇奇怪怪的宏与类（比如 GENERATED_BODY()、AActor......），这些可以参见之前写的 [UE 反射系统](https://jiat-t.github.io/ue/reflection-system/) 与 [UE Gameplay Framework（一）](https://jiat-t.github.io/ue/gameplay-framework1/)。总之，关于这些东西是什么以及他们的作用，这里不再赘述

## 修改 .h 和 .cpp 文件

在 **MaterialShowcaseActor.h** 之中添加不同的属性与之后会用到的函数

```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MaterialShowcaseActor.generated.h"

UCLASS()
class UE5_MATERIAL_LAB_API AMaterialShowcaseActor : public AActor
{
    GENERATED_BODY()

public:	
    // Sets default values for this actor's properties
    AMaterialShowcaseActor();

protected:
    // Called when the game starts or when spawned
    virtual void BeginPlay() override;

/* ------------ 新增部分 ------------ */
    // Actor 被放置、Details 面板中的参数被修改时调用
    virtual void OnConstruction(const FTransform& Transform) override;
/* --------------------------------- */

public:	
    // Called every frame
    virtual void Tick(float DeltaTime) override;

/* ------------ 新增部分 ------------ */
public:
    // 模型组件：编辑器中可见，但不可替换；类型为 Components
    UPROPERTY(VisibleAnywhere, Category = "Components")
    TObjectPtr<UStaticMeshComponent> MeshComponent;

    // 原始材质引用：可编辑；类型为 Material
    UPROPERTY(EditAnywhere, Category = "Material")
    TObjectPtr<UMaterialInterface> SourceMaterial;

    // 基础色，后面的几个参数都可在 Details 面板中编辑
    UPROPERTY(EditAnywhere, Category = "Material")
    FLinearColor BaseColor = FLinearColor::White;

    // 粗糙度
    UPROPERTY(EditAnywhere, Category = "Material", meta = (ClampMin = "0.0", ClampMax = "1.0"))
    float Roughness = 0.5f;

    // 自发光强度
    UPROPERTY(EditAnywhere, Category = "Material", meta = (ClampMin = "0.0"))
    float EmissiveStrength = 0.0f;

    // 动态的材质实例
    // 这是因为我们不希望在运行时对源材质进行修改（会导致整个材质类的重新编译，同时也会影响所有使用这个材质的物体）
    // 以此需要在运行时创建一个动态实例，在这之上的修改只会作用于当前 Actor
    UPROPERTY()
    TObjectPtr<UMaterialInstanceDynamic> MaterialInstance;

    // 一个辅助函数，用于将 C++ 变量同步到材质
    void UpdateMaterialInstance();
/* --------------------------------- */
};
```

在 **MaterialShowcaseActor.cpp** 中对之前声明的函数进行定义

```cpp
#include "MaterialShowcaseActor.h"
#include "Components/StaticMeshComponent.h"
#include "Materials/MaterialInstanceDynamic.h"

// Sets default values
AMaterialShowcaseActor::AMaterialShowcaseActor()
{
    // Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
    PrimaryActorTick.bCanEverTick = true;

/* ------------ 新增部分 ------------ */
    // Actor 本身只是一个容器，真正的显示则是由一个个的组件所实现
    // 这里则是创建了一个 StaticMeshComponent
    MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComponent"));
    // 将这个组件设置为根组件，之后的旋转、缩放等操作都以此为基础进行
    RootComponent = MeshComponent;
/* --------------------------------- */
}

// Called when the game starts or when spawned
void AMaterialShowcaseActor::BeginPlay()
{
    Super::BeginPlay();

/* ------------ 新增部分 ------------ */
    // 如果没有在 Details 面板中填入材质，就不执行，避免空指针错误
    if (SourceMaterial)
    {
        // 根据 SourceMaterial 创建一份材质实例
        MaterialInstance = UMaterialInstanceDynamic::Create(SourceMaterial, this);
        // 并将这个材质实例绑定到 0 号材质槽中
        MeshComponent->SetMaterial(0, MaterialInstance);
        // 将 C++ 中定义的参数写入材质实例
        UpdateMaterialInstance();
    }
}

// 这个函数用来创建动态材质与更新参数
// 因此即使没有运行也可以在预览窗口中实时看到材质变化
void AMaterialShowcaseActor::OnConstruction(const FTransform& Transform)
{
    Super::OnConstruction(Transform);

    if (SourceMaterial)
    {
        MaterialInstance = UMaterialInstanceDynamic::Create(SourceMaterial, this);
        MeshComponent->SetMaterial(0, MaterialInstance);
        UpdateMaterialInstance();
    }
}

void AMaterialShowcaseActor::UpdateMaterialInstance()
{
    // 如果连材质实例都不存在，自然也就没必要更新，直接退出即可
    if (!MaterialInstance)
    {
        return;
    }

    // 这里是真正将 C++ 与材质连接在一起的地方
    // 需要注意的是，这里的字符串必须与材质蓝图中的参数名完全一致
    // 如果不一致，编译器倒是不会报错，但调整参数也不会有效果
    MaterialInstance->SetVectorParameterValue(TEXT("BaseColor"), BaseColor);
    MaterialInstance->SetScalarParameterValue(TEXT("Roughness"), Roughness);
    MaterialInstance->SetScalarParameterValue(TEXT("EmissiveStrength"), EmissiveStrength);
}
/* --------------------------------- */

// Called every frame
void AMaterialShowcaseActor::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
}
```

## 创建材质

在写代码时就已经可以知道，通过 C++ 类所创建的 Actor，必须得有一个材质进行承接，不然代码中的 if 语句会直接将流程跳过。

在 UE 的内容浏览器中创建一个名为“M_ShowCase”的材质，进入蓝图后创建三个参数——BaseColor、Roughness、EmissiveStrength 并进行如图连接：

<img src="/images/cpp-in-ue5/material-graph.png" width="749" title="" crop="0,0,1,0.6454" id="u1c5b9519" class="ne-image">

## 编译

这里既可以直接在 IDE 中进行编译，同时也可以点击 UE 编辑器下方栏中的编译按钮，之后在内容浏览器中就能找到“C++ 类 / YourProject / Public / MaterialShowcaseActor”

<img src="/images/cpp-in-ue5/compiled-actor.png" width="864" title="" crop="0,0,1,1" id="u755f83cb" class="ne-image">

## 设置 Actor

将此 Actor 拖入场景中，可以看到 Actor 是空的，什么也没有，这是因为 Actor 还没有绑定组件，在右侧的 Detail 栏中随便选一个 Static Mesh 即可，之后再把上一步创建的材质拖进材质槽位。此时如果对参数进行修改，正常情况下应该是会作用到 Actor 上的

## 总结：

至此，我们已经打通了 C++ 与引擎通信的第一层：

C++ class

-> UE 反射系统

-> Editor Details 面板

-> Actor 实例

-> Component

-> Material asset

-> Dynamic Material Instance

-> Runtime parameter update
