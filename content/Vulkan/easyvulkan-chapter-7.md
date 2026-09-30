---
title: "EasyVulkan 第七章学习笔记"
slug: "easyvulkan-chapter-7"
summary: "整理顶点与索引缓冲区、实例化绘制、Push Constant、Uniform Buffer 和贴图上传的数据传递流程。"
categories: ["Vulkan"]
tags: ["Vulkan", "EasyVulkan", "Buffer", "Descriptor Set", "Texture", "Rendering"]
date: "2026-07-26T06:12:13.000Z"
lastmod: "2026-07-26T06:29:55.000Z"
draft: false
yuque_slug: "wtm8ednr7m6i7g7m"
source: "https://www.yuque.com/u62694975/iaaa/wtm8ednr7m6i7g7m"
---

<a id="ud56dd595"></a>第七章的核心目标，是在第二章已经能够绘制三角形的基础上，继续完善 Vulkan 中最基础的数据传递流程。

<a id="u6aa07ee2"></a>这一章主要解决以下问题：

- <a id="uff7ff270"></a>如何将 CPU 中的顶点数据传入 GPU
- <a id="uabb745ae"></a>如何使用索引复用顶点
- <a id="u6f09486a"></a>如何一次绘制多个相同物体
- <a id="u556da365"></a>如何向着色器传递少量数据
- <a id="u4996c0cb"></a>如何向着色器传递较大数据
- <a id="u943bef50"></a>如何将图片数据上传为 Vulkan 图像
- <a id="u49017fec"></a>如何在着色器中使用贴图

<a id="u7d90dca7"></a>第七章完成后，整个程序将从“顶点写死在着色器中的简单三角形”，逐步扩展为一个具备顶点、索引、实例化、Uniform、Push Constant 和贴图能力的基础 Vulkan 渲染框架。

<a id="ouo4X"></a>

---

<a id="FHRVZ"></a>
## 一、Ch7-1 初识顶点缓冲区

<a id="u2eef5803"></a>在第二章中，三角形的顶点位置通常直接写在顶点着色器中，并通过 `gl_VertexIndex` 进行读取。

<a id="udc7a87db"></a>这种方式只适合绘制极其简单的测试图形。

<a id="ub6f3f838"></a>真正的渲染程序中，顶点数据通常保存在 CPU 内存中，然后上传到 GPU 的顶点缓冲区中。

<a id="u503c8a00"></a>整体流程为：

<a id="Jtwgq"></a>
```latex
CPU 顶点数组
→ 创建 VkBuffer
→ 分配 VkDeviceMemory
→ 上传顶点数据
→ 绑定顶点缓冲区
→ 顶点着色器读取数据
```

<a id="aT9M0"></a>
### 1. 顶点结构

<a id="u27dacc73"></a>顶点可以包含多个属性，例如：

<a id="JXKjL"></a>
```cpp
struct Vertex
{
    glm::vec2 position;
    glm::vec3 color;
    glm::vec2 texCoord;
};
```

<a id="ubed6aba6"></a>这些数据通常交错存储在同一个顶点数组中。

<a id="ud0d6f875"></a>例如：

<a id="zSUui"></a>
```latex
顶点0：位置、颜色、UV
顶点1：位置、颜色、UV
顶点2：位置、颜色、UV
```

<a id="SAZfp"></a>

---

<a id="iWKBG"></a>
### 2. VkBuffer 与 VkDeviceMemory

<a id="uf0a65a3c"></a>Vulkan 中，Buffer 对象与实际内存是分离的。

<a id="u05aceb06"></a>创建顶点缓冲区时，需要完成以下步骤：

<a id="OH9TX"></a>
```latex
创建 VkBuffer
→ 查询内存需求
→ 查找合适的内存类型
→ 分配 VkDeviceMemory
→ 将内存绑定到 Buffer
```

<a id="u3035c08a"></a>`VkBuffer` 只描述缓冲区本身，例如：

- <a id="u25acbda4"></a>缓冲区大小
- <a id="u5e040c27"></a>缓冲区用途
- <a id="u19ba36b9"></a>资源共享模式

<a id="u46df34dd"></a>真正存储数据的是 `VkDeviceMemory`。

<a id="u4f4315bc"></a>因此：

<a id="HIAKA"></a>
```latex
VkBuffer = 资源对象
VkDeviceMemory = 实际内存
```

<a id="u9a408383"></a>二者必须通过：

<a id="wuogV"></a>
```cpp
vkBindBufferMemory(...)
```

<a id="u2957e7bb"></a>进行绑定。

<a id="w3CbW"></a>

---

<a id="p99Yl"></a>
### 3. 顶点缓冲区用途

<a id="ude57e585"></a>创建顶点缓冲区时，需要指定：

<a id="eDBKz"></a>
```cpp
VK_BUFFER_USAGE_VERTEX_BUFFER_BIT
```

<a id="u686b58f4"></a>如果使用 Staging Buffer，则最终的顶点缓冲区通常还需要：

<a id="iAcVU"></a>
```cpp
VK_BUFFER_USAGE_TRANSFER_DST_BIT
```

<a id="ubed17ad9"></a>例如：

<a id="sufHF"></a>
```cpp
VK_BUFFER_USAGE_TRANSFER_DST_BIT |
VK_BUFFER_USAGE_VERTEX_BUFFER_BIT
```

<a id="k4yWU"></a>

---

<a id="HwUKe"></a>
### 4. 顶点输入描述

<a id="u76623751"></a>Graphics Pipeline 必须知道顶点缓冲区中的数据如何排列。

<a id="u5d2a734e"></a>主要通过以下两个结构体进行描述：

<a id="wEelO"></a>
```cpp
VkVertexInputBindingDescription
VkVertexInputAttributeDescription
```

<a id="fx4dJ"></a>
#### Binding Description

<a id="u2fc948d5"></a>Binding 描述整条顶点数据流。

<a id="u5044938a"></a>主要包含：

<a id="kUhcX"></a>
```cpp
binding
stride
inputRate
```

<a id="u3b43abcb"></a>例如：

<a id="tvlxb"></a>
```cpp
binding = 0;
stride = sizeof(Vertex);
inputRate = VK_VERTEX_INPUT_RATE_VERTEX;
```

<a id="ubd11e153"></a>其中：

- <a id="ud8564976"></a>`binding` 表示当前数据使用哪个 Binding
- <a id="ucb07df3d"></a>`stride` 表示相邻两个顶点之间的字节间隔
- <a id="u248c7029"></a>`inputRate` 表示数据按顶点更新还是按实例更新

<a id="vECCl"></a>

---

<a id="HHJFw"></a>
#### Attribute Description

<a id="u8a62b19c"></a>Attribute 描述顶点结构中的某一个具体属性。

<a id="u428e0c25"></a>主要包含：

<a id="sPPW3"></a>
```cpp
location
binding
format
offset
```

<a id="u92485e14"></a>例如：

<a id="tE8SZ"></a>
```cpp
location = 0;
binding = 0;
format = VK_FORMAT_R32G32_SFLOAT;
offset = offsetof(Vertex, position);
```

<a id="u84591a30"></a>这里的 `location` 必须与顶点着色器中的输入位置一致：

<a id="br0Bm"></a>
```glsl
layout(location = 0) in vec2 inPosition;
layout(location = 1) in vec3 inColor;
layout(location = 2) in vec2 inTexCoord;
```

<a id="u980778a1"></a>因此：

<a id="pkqKx"></a>
```latex
Binding 描述一整条数据
Attribute 描述数据中的某个成员
Location 对应 Shader 中的输入位置
```

<a id="JMI3g"></a>

---

<a id="QRfS6"></a>
### 5. 绑定顶点缓冲区

<a id="u28c555f5"></a>绘制之前，需要调用：

<a id="NjnCm"></a>
```cpp
vkCmdBindVertexBuffers(...)
```

<a id="uaf5cefcc"></a>之后再调用：

<a id="Xyg5s"></a>
```cpp
vkCmdDraw(...)
```

<a id="uf08b4075"></a>最终流程为：

<a id="xwnOv"></a>
```latex
创建顶点缓冲区
→ 配置 Pipeline Vertex Input
→ vkCmdBindVertexBuffers
→ vkCmdDraw
```

<a id="V7FiA"></a>

---

<a id="b5xmw"></a>
### 6. Staging Buffer

<a id="ud65905f4"></a>性能较高的顶点缓冲区通常放在 Device Local 内存中。

<a id="u1cbc1450"></a>但是 Device Local 内存通常无法直接被 CPU 写入。

<a id="u0a20034a"></a>因此需要使用 Staging Buffer。

<a id="u82edaf85"></a>整体流程为：

<a id="VHWxQ"></a>
```latex
CPU 数据
→ Host Visible Staging Buffer
→ vkCmdCopyBuffer
→ Device Local Vertex Buffer
```

<a id="u8309c376"></a>Staging Buffer 通常使用：

<a id="b6HvQ"></a>
```cpp
VK_BUFFER_USAGE_TRANSFER_SRC_BIT
```

<a id="ud7fcdb12"></a>最终顶点缓冲区使用：

<a id="YaFso"></a>
```cpp
VK_BUFFER_USAGE_TRANSFER_DST_BIT |
VK_BUFFER_USAGE_VERTEX_BUFFER_BIT
```

<a id="u30c36292"></a><strong>Staging Buffer </strong>只负责临时上传数据，上传完成后即可销毁。

<a id="WPx0F"></a>

---

<a id="cCNnZ"></a>
## 二、Ch7-2 初识索引缓冲区

<a id="u17397444"></a>索引缓冲区用于复用顶点。

<a id="u6a9a0bde"></a>例如，一个矩形由两个三角形组成。如果不使用索引缓冲区，需要六个顶点：

<a id="LDnQW"></a>
```latex
三角形1：0、1、2
三角形2：3、4、5
```

<a id="ub92af0d4"></a>其中部分顶点的位置实际上是重复的。使用索引缓冲区后，只需要四个顶点：

<a id="ptrw6"></a>
```cpp
Vertex vertices[] =
{
    左上,
    右上,
    左下,
    右下
};
```

<a id="u3d57ed3d"></a>再使用六个索引：

<a id="wcSeP"></a>
```cpp
uint16_t indices[] =
{
    0, 1, 2,
    1, 3, 2
};
```

<a id="z328a"></a>

---

<a id="g0bGV"></a>
### 1. 索引缓冲区用途

<a id="uc693b0e4"></a>索引缓冲区需要指定：

<a id="r7WIv"></a>
```cpp
VK_BUFFER_USAGE_INDEX_BUFFER_BIT
```

<a id="ubaa38cfa"></a>如果使用 Staging Buffer，则通常为：

<a id="dfyQj"></a>
```cpp
VK_BUFFER_USAGE_TRANSFER_DST_BIT |
VK_BUFFER_USAGE_INDEX_BUFFER_BIT
```

<a id="cTix9"></a>

---

<a id="Wgtio"></a>
### 2. 绑定索引缓冲区

<a id="u02a00bd8"></a>绘制前调用：

<a id="uMzlp"></a>
```cpp
vkCmdBindIndexBuffer(...)
```

<a id="udfb5bdd4"></a>其中必须指定索引类型：

<a id="Dpdda"></a>
```cpp
VK_INDEX_TYPE_UINT16
```

<a id="ucb8dfdd8"></a>或者：

<a id="jWkOq"></a>
```cpp
VK_INDEX_TYPE_UINT32
```

<a id="u6608c2ec"></a>索引类型必须与 CPU 中的索引数组类型保持一致。

<a id="u7112b42b"></a>例如：

<a id="h5D41"></a>
```cpp
std::vector<uint16_t>
```

<a id="u236276a8"></a>对应：

<a id="JYMnM"></a>
```cpp
VK_INDEX_TYPE_UINT16
```

<a id="sdlLo"></a>

---

<a id="cwlW7"></a>
### 3. 索引绘制

<a id="u11a4a07b"></a>绑定索引缓冲区后，使用：

<a id="iSG3I"></a>
```cpp
vkCmdDrawIndexed(...)
```

<a id="ubea33de7"></a>代替：

<a id="kT46G"></a>
```cpp
vkCmdDraw(...)
```

<a id="udae6848e"></a>整体流程为：

<a id="ymVIw"></a>
```latex
Vertex Buffer 提供顶点数据
Index Buffer 提供顶点编号
→ vkCmdBindVertexBuffers
→ vkCmdBindIndexBuffer
→ vkCmdDrawIndexed
```

<a id="uae874c7c"></a>索引缓冲区中保存的并不是顶点数据，而是顶点在顶点缓冲区中的编号。

<a id="ZvLU4"></a>

---

<a id="dsYJQ"></a>
## 三、Ch7-3 实例化绘制

<a id="ud0626d38"></a>实例化绘制用于一次 Draw Call 绘制多个相同结构的物体。

<a id="u7308edf8"></a>例如：

- <a id="u3595b47b"></a>大量草
- <a id="u913f38f8"></a>大量树木
- <a id="u8872fa9c"></a>粒子
- <a id="u689cf4b8"></a>子弹
- <a id="u959fa6af"></a>重复模型
- <a id="u5a4b7756"></a>大量相同网格

<a id="u7e6238fc"></a>如果每个物体都单独调用一次 Draw，会产生大量 CPU 到 GPU 的绘制调用开销。

<a id="u2ca46bd5"></a>实例化绘制可以通过一次调用绘制多个实例：

<a id="Pa8CX"></a>
```cpp
vkCmdDrawIndexed(
    commandBuffer,
    indexCount,
    instanceCount,
    0,
    0,
    0);
```

<a id="uf16af308"></a>其中：

<a id="mUMIs"></a>
```latex
indexCount = 每个实例使用多少索引
instanceCount = 绘制多少个实例
```

<a id="vL8eS"></a>

---

<a id="JjGCJ"></a>
### 1. 顶点数据与实例数据

<a id="ua3414582"></a>实例化绘制中，数据通常分为两类：

<a id="kvJlG"></a>
```latex
逐顶点数据
逐实例数据
```

<a id="u0de033d0"></a>逐顶点数据包括：

- <a id="ucdb68e1d"></a>顶点位置
- <a id="uad871be1"></a>法线
- <a id="u184ad95e"></a>UV
- <a id="u13f40e1b"></a>顶点颜色

<a id="ud5140845"></a>逐实例数据包括：

- <a id="u7f5f1ff0"></a>实例位置
- <a id="u8c4214ba"></a>实例颜色
- <a id="uc25ae239"></a>实例缩放
- <a id="ud8cf3b3c"></a>模型矩阵
- <a id="u8f2b1699"></a>实例编号

<a id="HhEQ8"></a>

---

<a id="l1Int"></a>
### 2. Input Rate

<a id="ucf7a76b2"></a>顶点数据使用：

<a id="DfO6h"></a>
```cpp
VK_VERTEX_INPUT_RATE_VERTEX
```

<a id="u62db0314"></a>实例数据使用：

<a id="gc1Bc"></a>
```cpp
VK_VERTEX_INPUT_RATE_INSTANCE
```

<a id="u65819417"></a>例如：

<a id="CyBL5"></a>
```cpp
VkVertexInputBindingDescription vertexBinding{};
vertexBinding.binding = 0;
vertexBinding.stride = sizeof(Vertex);
vertexBinding.inputRate = VK_VERTEX_INPUT_RATE_VERTEX;
```

<a id="u0890c685"></a>实例数据：

<a id="IcGBC"></a>
```cpp
VkVertexInputBindingDescription instanceBinding{};
instanceBinding.binding = 1;
instanceBinding.stride = sizeof(InstanceData);
instanceBinding.inputRate = VK_VERTEX_INPUT_RATE_INSTANCE;
```

<a id="u6a521862"></a>其中：

<a id="daao3"></a>
```latex
VERTEX：每处理一个顶点读取下一条数据
INSTANCE：每开始一个新实例读取下一条数据
```

<a id="ffDK2"></a>

---

<a id="EW2Nr"></a>
### 3. gl\_InstanceIndex

<a id="ud05a81cd"></a>Shader 中可以使用：

<a id="UjNHh"></a>
```glsl
gl_InstanceIndex
```

<a id="ua9a9278c"></a>获取当前实例编号。

<a id="ue87247bc"></a>例如：

<a id="YyzMn"></a>
```glsl
vec2 offset = offsets[gl_InstanceIndex];
```

<a id="u93f24e67"></a>这样可以根据实例编号给每个实例设置不同位置。

<a id="u3db80c09"></a>实例化绘制的核心意义是：

<a id="U5Wxv"></a>
```latex
一次 Draw Call
→ 绘制多个相同网格
→ 每个实例拥有不同数据
```

<a id="Jlyyq"></a>

---

<a id="lX0e2"></a>
## 四、Ch7-4 初识 Push Constant

<a id="u7ff215ed"></a>Push Constant 用于<strong>从 CPU 向 Shader 传递少量数据</strong>。

<a id="u9f8d0879"></a>它不需要：

- <a id="u0088bc3f"></a>创建 Buffer
- <a id="u7d2d2c41"></a>分配 Device Memory
- <a id="u4c09e463"></a>创建 Descriptor Set
- <a id="u18613513"></a>更新 Descriptor

<a id="uc3fe3fb6"></a>只需要在 Pipeline Layout 中声明，然后在录制命令时写入。

<a id="ueee2ad3d"></a>整体流程为：

<a id="jdQmy"></a>
```latex
定义 Push Constant 数据
→ 创建 Push Constant Range
→ 加入 Pipeline Layout
→ Shader 声明 Push Constant
→ vkCmdPushConstants
```

<a id="N8fmY"></a>

---

<a id="zU0Ck"></a>
### 1. Push Constant Range

<a id="u248a34ae"></a>创建 Pipeline Layout 时，需要声明：

<a id="kqN9n"></a>
```cpp
VkPushConstantRange pushConstantRange{};
```

<a id="u4e2979a6"></a>主要包含：

<a id="rUYVE"></a>
```cpp
stageFlags
offset
size
```

<a id="u24eb619f"></a>例如：

<a id="vI51F"></a>
```cpp
pushConstantRange.stageFlags = VK_SHADER_STAGE_VERTEX_BIT;
pushConstantRange.offset = 0;
pushConstantRange.size = sizeof(PushConstantData);
```

<a id="ysBme"></a>

---

<a id="qcpOj"></a>
### 2. Shader 中声明

<a id="uab84485d"></a>Shader 中使用：

<a id="bSk49"></a>
```glsl
layout(push_constant) uniform PushConstantBlock
{
    vec2 offset;
    vec4 color;
} pushConstant;
```

<a id="ud0b710cc"></a>C++ 中的结构体必须与 GLSL 中的数据布局对应。

<a id="u64be3eb8"></a>例如：

<a id="LIY7R"></a>
```cpp
struct PushConstantData
{
    glm::vec2 offset;
    glm::vec4 color;
};
```

<a id="u84bd794a"></a>需要特别注意内存对齐。

<a id="kSyvi"></a>

---

<a id="mWOY2"></a>
### 3. 写入 Push Constant

<a id="u2ddda422"></a>录制命令时调用：

<a id="LEsXC"></a>
```cpp
vkCmdPushConstants(...)
```

<a id="ud08d0504"></a>Push Constant 可以在 Draw Call 之间频繁修改。

<a id="u178e0ee7"></a>例如：

<a id="a2OAQ"></a>
```latex
Push Constant A
→ Draw Object A

Push Constant B
→ Draw Object B
```

<a id="uc854eee4"></a>因此它适合：

- <a id="ue4e835de"></a>每个物体的颜色
- <a id="u01de7471"></a>每个物体的位置
- <a id="u3ae708a7"></a>对象索引
- <a id="u3c902a89"></a>少量模型参数
- <a id="u28ffb3e6"></a>少量材质参数

<a id="eCdXU"></a>

---

<a id="z4P4a"></a>
### 4. Push Constant 特点

<a id="u05c12ae9"></a>优点：

- <a id="u6decc1a3"></a>使用简单
- <a id="ua29e44a4"></a>不需要 Descriptor
- <a id="ue401bf4c"></a>更新方便
- <a id="u4f1d05e6"></a>适合每次绘制都变化的数据

<a id="ua5c547b8"></a>缺点：

- <a id="u51cd48e5"></a>容量较小
- <a id="ue8475642"></a>不适合传递大量数据
- <a id="u654d6183"></a>大量 Push Constant 更新会增加命令缓冲区内容

<a id="ue53c1468"></a>Vulkan 保证至少支持：

<a id="RCxnS"></a>
```latex
128 Bytes
```

<a id="u47a97d21"></a>实际限制可以通过：

<a id="FaLi0"></a>
```cpp
maxPushConstantsSize
```

<a id="u3bf67323"></a>查询。

<a id="PkQqI"></a>

---

<a id="dAuaz"></a>
## 五、Ch7-5 初识 Uniform Buffer

<a id="u2b46d458"></a>Uniform Buffer 用于<strong>向 Shader 传递较大的只读数据</strong>。

<a id="udec73c0f"></a>常见用途包括：

- <a id="u0967ba01"></a>Model 矩阵
- <a id="u38d0a74f"></a>View 矩阵
- <a id="u31c0bd94"></a>Projection 矩阵
- <a id="u28f4366c"></a>相机位置
- <a id="u3a1de9c3"></a>时间
- <a id="u2735d987"></a>灯光信息
- <a id="u3e08ead8"></a>全局参数

<a id="ue458d2e8"></a>Uniform Buffer 本质上仍然是一个普通的 `VkBuffer`，但是用途被指定为：

<a id="QhmWf"></a>
```cpp
VK_BUFFER_USAGE_UNIFORM_BUFFER_BIT
```

<a id="Fv1DU"></a>

---

<a id="rZgi2"></a>
### 1. Uniform Buffer 完整流程

<a id="u4a9ac20b"></a>Uniform Buffer 需要配合描述符使用。

<a id="uec015c95"></a>整体流程为：

<a id="C5Vq7"></a>
```latex
创建 Uniform Buffer
→ 创建 Descriptor Set Layout
→ 创建 Descriptor Pool
→ 分配 Descriptor Set
→ 更新 Descriptor Set
→ 绑定 Descriptor Set
→ Shader 读取 Uniform Buffer
```

<a id="aOGA7"></a>

---

<a id="AKZMW"></a>
### 2. Descriptor Set Layout

<a id="uf16053b6"></a>Descriptor Set Layout 用于<strong>描述 Shader 将会使用什么资源</strong>。

<a id="u10348ecc"></a>例如：

<a id="MWJuz"></a>
```cpp
VkDescriptorSetLayoutBinding uboLayoutBinding{};
```

<a id="u92080da2"></a>主要包含：

<a id="Tm4DC"></a>
```cpp
binding
descriptorType
descriptorCount
stageFlags
```

<a id="u04d6a92f"></a>例如：

<a id="nSriT"></a>
```cpp
uboLayoutBinding.binding = 0;
uboLayoutBinding.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
uboLayoutBinding.descriptorCount = 1;
uboLayoutBinding.stageFlags = VK_SHADER_STAGE_VERTEX_BIT;
```

<a id="u87f5aab4"></a>这必须与 Shader 保持一致：

<a id="YcJSJ"></a>
```glsl
layout(set = 0, binding = 0) uniform UniformBufferObject
{
    mat4 model;
    mat4 view;
    mat4 projection;
} ubo;
```

<a id="Ft7FJ"></a>

---

<a id="KoERY"></a>
### 3. Descriptor Pool

<a id="u605ab931"></a>Descriptor Pool 用于<strong>分配 Descriptor Set</strong>。

<a id="uf0b66d6b"></a>创建时需要说明：

- <a id="u0a4de3d6"></a>可以分配多少个 Descriptor Set
- <a id="uf4e13976"></a>每种 Descriptor 类型有多少个

<a id="u511a4254"></a>例如：

<a id="TSJpK"></a>
```cpp
VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER
```

<a id="Q54VT"></a>

---

<a id="X1aoO"></a>
### 4. Descriptor Set

<a id="u49e394f7"></a>Descriptor Set 是实际<strong>绑定 Buffer 和 Shader 的对象</strong>。

<a id="u2b442403"></a>更新 Descriptor Set 时需要提供：

<a id="E8f3w"></a>
```cpp
VkDescriptorBufferInfo
```

<a id="u46bedf31"></a>其中包含：

<a id="d8eRk"></a>
```cpp
buffer
offset
range
```

<a id="ucd9f20ac"></a>然后通过：

<a id="chrhf"></a>
```cpp
vkUpdateDescriptorSets(...)
```

<a id="ube378aa7"></a>将 Uniform Buffer 写入 Descriptor Set。

<a id="vgGhp"></a>

---

<a id="eTKT5"></a>
### 5. 绑定 Descriptor Set

<a id="u7d27722f"></a>绘制之前调用：

<a id="iZ1Z8"></a>
```cpp
vkCmdBindDescriptorSets(...)
```

<a id="uee22e3df"></a>之后 Shader 才能读取对应 Uniform Buffer。

<a id="u2bcd6c64"></a>整体关系为：

<a id="oMkfp"></a>
```latex
Shader Binding
↕
Descriptor Set Layout
↕
Descriptor Set
↕
VkBuffer
```

<a id="GQahY"></a>

---

<a id="YIr76"></a>
### 6. 每帧 Uniform Buffer

<a id="u2db2ebdc"></a>如果程序存在多个 Frames In Flight，不建议所有帧共用同一个正在频繁修改的 Uniform Buffer。

<a id="ua624917a"></a>常见做法是：

<a id="wUqPw"></a>
```latex
Frame 0 → Uniform Buffer 0
Frame 1 → Uniform Buffer 1
```

<a id="ue8db6b7a"></a>每帧拥有：

- <a id="ua009da2a"></a>一个 Uniform Buffer
- <a id="uebf8da0c"></a>一块 Memory
- <a id="uef82fdd5"></a>一个 Descriptor Set

<a id="uf515cd65"></a>这样可以避免 CPU 修改数据时，GPU 仍在读取同一块内存。

<a id="IdDri"></a>

---

<a id="ftVjA"></a>
### 7. Dynamic Uniform Buffer

<a id="uc3ea50f5"></a>Dynamic Uniform Buffer 可以<strong>让多个对象共用同一个大 Buffer</strong>。

<a id="ud71ba061"></a>数据排列为：

<a id="rim8U"></a>
```latex
Object 0 Data
Object 1 Data
Object 2 Data
```

<a id="ud009a256"></a>绑定 Descriptor Set 时，再通过动态偏移指定当前读取哪一段数据。

<a id="ubbda9caa"></a>动态偏移必须满足：

<a id="bgn3H"></a>
```cpp
minUniformBufferOffsetAlignment
```

<a id="u534a50b7"></a>因此每段数据通常需要进行对齐。

<a id="u8121d3a4"></a>例如：

<a id="ME6cv"></a>
```cpp
alignedSize = (dataSize + alignment - 1) & ~(alignment - 1);
```

<a id="cMnXC"></a>

---

<a id="YFBxJ"></a>
### 8. Push Constant 与 Uniform Buffer 区别

<a id="DniqD"></a>
```latex
Push Constant：
少量数据
更新频繁
不需要 Descriptor
适合每次 Draw 不同的数据

Uniform Buffer：
数据较大
需要 Descriptor
适合矩阵、相机、灯光等全局数据
```

<a id="u65bd497a"></a>可以简单理解为：

<a id="d8kKn"></a>
```latex
Push Constant = 小而频繁
Uniform Buffer = 大而稳定
```

<a id="fpzkN"></a>

---

<a id="cFGVN"></a>
## 六、Ch7-6 拷贝图像到屏幕

<a id="ud545311d"></a>这一节开始正式接触 Vulkan Image。

<a id="u61e37f6e"></a>Buffer 与 Image 的区别：

<a id="zQSGA"></a>
```latex
Buffer：
线性数据
没有宽高
适合顶点、索引、Uniform

Image：
二维或三维图像数据
具有宽、高、格式、Mip Level
适合贴图、渲染目标、深度缓冲
```

<a id="u2781726f"></a>图像上传的整体流程为：

<a id="HQzxC"></a>
```latex
CPU 图片数据
→ Staging Buffer
→ VkImage
→ 图像布局转换
→ Copy 或 Blit
→ 交换链图像
```

<a id="TV4CT"></a>

---

<a id="vkT6s"></a>
### 1. 创建 VkImage

<a id="u7d5dd4f8"></a>创建 Image 时需要指定：

- <a id="u346bd13e"></a>Image Type
- <a id="u39ccafed"></a>Format
- <a id="ue01873e5"></a>Extent
- <a id="u2f4bec44"></a>Mip Levels
- <a id="uc97cabd3"></a>Array Layers
- <a id="ua7731959"></a>Tiling
- <a id="u47f71066"></a>Usage
- <a id="u5ae4aefe"></a>Initial Layout

<a id="ucd6280f4"></a>例如：

<a id="CDUi8"></a>
```cpp
VK_IMAGE_USAGE_TRANSFER_SRC_BIT
VK_IMAGE_USAGE_TRANSFER_DST_BIT
VK_IMAGE_USAGE_SAMPLED_BIT
```

<a id="u017ed5f6"></a>Image 与 Buffer 一样，也需要：

<a id="wByZu"></a>
```latex
创建 VkImage
→ 查询内存需求
→ 分配 VkDeviceMemory
→ vkBindImageMemory
```

<a id="uWwKe"></a>

---

<a id="VCRJF"></a>
### 2. Image Layout

<a id="u1fc3ced4"></a>Vulkan Image 在不同用途下需要处于不同 Layout。

<a id="u3c5496ad"></a>常见 Layout 包括：

<a id="Yt7hE"></a>
```cpp
VK_IMAGE_LAYOUT_UNDEFINED
VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL
VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL
VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL
VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL
VK_IMAGE_LAYOUT_PRESENT_SRC_KHR
```

<a id="ucabdb929"></a>例如：

<a id="nSTgz"></a>
```latex
准备接收复制
→ TRANSFER_DST_OPTIMAL

作为复制源
→ TRANSFER_SRC_OPTIMAL

被 Shader 读取
→ SHADER_READ_ONLY_OPTIMAL

用于屏幕显示
→ PRESENT_SRC_KHR
```

<a id="u2f38b997"></a>Image Layout 并不只是一个普通状态变量。

<a id="u02f37031"></a>它同时与以下内容有关：

- <a id="u8b171aab"></a>图像当前用途
- <a id="u6a69cf0f"></a>GPU 内部存储方式
- <a id="u660a90cc"></a>访问权限
- <a id="uc0c843f4"></a>同步关系

<a id="cUwzQ"></a>

---

<a id="EJoMF"></a>
### 3. Image Memory Barrier

<a id="ue0b84c33"></a>图像布局转换通常通过：

<a id="aYVtk"></a>
```cpp
VkImageMemoryBarrier
```

<a id="u4a6e0522"></a>配合：

<a id="J7KFy"></a>
```cpp
vkCmdPipelineBarrier(...)
```

<a id="u987f0ba6"></a>实现。

<a id="u6a824b18"></a>Barrier 需要描述：

- <a id="u26cb5d87"></a>旧布局
- <a id="u90f82f54"></a>新布局
- <a id="u8d6de16c"></a>源访问权限
- <a id="u342126f7"></a>目标访问权限
- <a id="uf8f7f825"></a>源管线阶段
- <a id="u425b3f49"></a>目标管线阶段
- <a id="ua9ec4efc"></a>图像范围

<a id="u20a232e0"></a>例如：

<a id="Kf8s8"></a>
```latex
UNDEFINED
→ TRANSFER_DST_OPTIMAL
```

<a id="u73afa4b1"></a>表示图像之后将作为复制目标。

<a id="u536f41c3"></a>再例如：

<a id="tkAie"></a>
```latex
TRANSFER_DST_OPTIMAL
→ SHADER_READ_ONLY_OPTIMAL
```

<a id="u2e1d6928"></a>表示图像复制完成后，将交给片段着色器读取。

<a id="sB1ck"></a>

---

<a id="gLxLS"></a>
### 4. Copy Buffer To Image

<a id="u2771c1e5"></a>通过：

<a id="IABBk"></a>
```cpp
vkCmdCopyBufferToImage(...)
```

<a id="u22c46bfe"></a>可以将 Staging Buffer 中的像素数据复制到 Image。

<a id="u53287833"></a>要求目标 Image 处于：

<a id="YKKiZ"></a>
```cpp
VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL
```

<a id="QmOuT"></a>

---

<a id="CkF4Z"></a>
### 5. Copy Image 与 Blit Image

<a id="ucc76df40"></a>`vkCmdCopyImage` 用于直接复制图像。

<a id="u68cfc36c"></a>`vkCmdBlitImage` 除了复制外，还可以：

- <a id="ua1640df0"></a>缩放
- <a id="ud1b151cd"></a>翻转
- <a id="u41877edd"></a>过滤
- <a id="u2df20cad"></a>在不同尺寸之间转换

<a id="u3aa4893f"></a>例如，通过交换源图像上下坐标，可以实现垂直翻转。

<a id="tdiSs"></a>

---

<a id="WGTnR"></a>
### 6. 拷贝到交换链

<a id="u1d80a913"></a>如果需要将图像复制到交换链图像，需要确保：

<a id="RBzMl"></a>
```latex
源图像 → TRANSFER_SRC_OPTIMAL
交换链图像 → TRANSFER_DST_OPTIMAL
```

<a id="u90bfa080"></a>复制完成后，再将交换链图像转换为：

<a id="zHX4C"></a>
```cpp
VK_IMAGE_LAYOUT_PRESENT_SRC_KHR
```

<a id="ue11820a5"></a>才能进行显示。

<a id="uc87eb3ee"></a>整体流程为：

<a id="oPjZy"></a>
```latex
Swapchain Image
PRESENT_SRC_KHR
→ TRANSFER_DST_OPTIMAL
→ 接收图像
→ PRESENT_SRC_KHR
```

<a id="trMH7"></a>

---

<a id="Ac9gZ"></a>
## 七、Ch7-7 使用贴图

<a id="u9bac7e3b"></a>贴图本质上是一个可以被 Shader 读取的 Vulkan Image。

<a id="u6d5eb844"></a>完整流程为：

<a id="OwP4Q"></a>
```latex
读取图片文件
→ Staging Buffer
→ Texture Image
→ 生成 Mipmap
→ 创建 Image View
→ 创建 Sampler
→ 创建 Combined Image Sampler Descriptor
→ Shader 采样
```

<a id="dY5U8"></a>

---

<a id="iCPNI"></a>
### 1. Texture Image

<a id="u44c32a6f"></a>贴图 Image 通常需要：

<a id="HIYQn"></a>
```cpp
VK_IMAGE_USAGE_TRANSFER_DST_BIT
VK_IMAGE_USAGE_SAMPLED_BIT
```

<a id="u9e66831c"></a>如果需要生成 Mipmap，还需要：

<a id="bVwZX"></a>
```cpp
VK_IMAGE_USAGE_TRANSFER_SRC_BIT
```

<a id="ud8d60ae7"></a>因此常见用途为：

<a id="L19hv"></a>
```cpp
VK_IMAGE_USAGE_TRANSFER_SRC_BIT |
VK_IMAGE_USAGE_TRANSFER_DST_BIT |
VK_IMAGE_USAGE_SAMPLED_BIT
```

<a id="l5uXf"></a>

---

<a id="iW7vs"></a>
### 2. Image View

<a id="ubc1ee706"></a>Shader 不能直接使用 `VkImage`。

<a id="u8f9b62b3"></a>必须先创建：

<a id="Kjoo4"></a>
```cpp
VkImageView
```

<a id="u5e67e62c"></a>Image View 用于描述：

- <a id="u53494c5d"></a>如何解释 Image
- <a id="ua9270d2d"></a>使用什么格式
- <a id="u4a74dfd6"></a>使用哪些 Mip Level
- <a id="uf0794b1c"></a>使用哪些 Array Layer
- <a id="ud8b9abe1"></a>使用哪个 Aspect

<a id="u9bcd0a3c"></a>可以简单理解为：

<a id="PYLfs"></a>
```latex
VkImage = 实际图像资源
VkImageView = 访问图像资源的视图
```

<a id="uee68b360"></a>同一个 Image 可以创建多个不同的 Image View。

<a id="MENMi"></a>

---

<a id="QfaRX"></a>
### 3. Sampler

<a id="u0fd6eceb"></a>Sampler 描述如何采样图像。

<a id="u4c9c55a4"></a>包括：

- <a id="u3ed61d29"></a>放大过滤
- <a id="ub87c7059"></a>缩小过滤
- <a id="ue1367af7"></a>Mipmap 过滤
- <a id="uabc5bd92"></a>UV 寻址模式
- <a id="ua6f29ea7"></a>各向异性过滤
- <a id="ud93ab3f8"></a>LOD 范围

<a id="ud69924b3"></a>常用参数包括：

<a id="S3R3k"></a>
```cpp
magFilter
minFilter
mipmapMode
addressModeU
addressModeV
addressModeW
minLod
maxLod
maxAnisotropy
```

<a id="uc94780ff"></a>例如：

<a id="pgBkM"></a>
```latex
Image = 贴图数据本身
Image View = 如何访问贴图
Sampler = 如何对贴图进行采样
```

<a id="VhD4c"></a>

---

<a id="rJNWc"></a>
### 4. Combined Image Sampler

<a id="u18afdaff"></a>贴图通常通过：

<a id="oLwXx"></a>
```cpp
VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER
```

<a id="u4a1c780f"></a>传递给 Shader。

<a id="u0e2bba2c"></a>需要创建：

<a id="WSlqR"></a>
```cpp
VkDescriptorImageInfo
```

<a id="uc3d8b0e2"></a>其中包含：

<a id="Qc6dT"></a>
```cpp
sampler
imageView
imageLayout
```

<a id="u3060f430"></a>然后通过：

<a id="qFfhC"></a>
```cpp
vkUpdateDescriptorSets(...)
```

<a id="u996f5617"></a>写入 Descriptor Set。

<a id="ctVZR"></a>

---

<a id="Qcnjz"></a>
### 5. Shader 采样

<a id="u19b142c8"></a>片段着色器中声明：

<a id="YUgCZ"></a>
```glsl
layout(set = 0, binding = 1) uniform sampler2D textureSampler;
```

<a id="u79deb362"></a>采样时使用：

<a id="OEcCt"></a>
```glsl
vec4 color = texture(textureSampler, inTexCoord);
```

<a id="u287b6832"></a>其中：

- <a id="ufc725729"></a>`textureSampler` 是贴图与采样器
- <a id="ubb21b3c9"></a>`inTexCoord` 是 UV
- <a id="u15c20e27"></a>返回值是采样得到的颜色

<a id="LQWnI"></a>

---

<a id="WfFcS"></a>
### 6. 纹理坐标

<a id="uca90715b"></a>UV 通常在以下范围内：

<a id="Kcl4z"></a>
```latex
U：0 到 1
V：0 到 1
```

<a id="u5d1a462a"></a>顶点结构中加入：

<a id="Z8gbc"></a>
```cpp
glm::vec2 texCoord;
```

<a id="uf277d89f"></a>顶点着色器将 UV 传给片段着色器：

<a id="AXRA2"></a>
```glsl
layout(location = 2) in vec2 inTexCoord;
layout(location = 0) out vec2 outTexCoord;
```

<a id="uc85923a8"></a>片段着色器接收：

<a id="bAPJe"></a>
```glsl
layout(location = 0) in vec2 inTexCoord;
```

<a id="G7oUQ"></a>

---

<a id="QTPPK"></a>
### 7. Mipmap

<a id="u200ced22"></a>Mipmap 是同一张贴图的多级缩小版本。

<a id="u5c7a82b4"></a>例如：

<a id="M3Lqt"></a>
```latex
1024 × 1024
512 × 512
256 × 256
128 × 128
...
1 × 1
```

<a id="u33b82b90"></a>Mipmap 数量计算方式为：

<a id="FQpXM"></a>
```cpp
floor(log2(max(width, height))) + 1
```

<a id="u69dba0e9"></a>生成 Mipmap 时，可以通过：

<a id="QFwPv"></a>
```cpp
vkCmdBlitImage(...)
```

<a id="ub2bbe070"></a>逐级缩小。

<a id="u0e92bd53"></a>例如：

<a id="m2k6M"></a>
```latex
Mip 0 → Mip 1
Mip 1 → Mip 2
Mip 2 → Mip 3
```

<a id="ua40ab6e9"></a>生成过程中需要不断进行 Image Layout 转换。

<a id="u2931feaa"></a>每一级在作为 Blit 源之前，需要转换为：

<a id="njxZo"></a>
```cpp
VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL
```

<a id="u42ec334a"></a>生成完成后，再转换为：

<a id="KHy6A"></a>
```cpp
VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL
```

<a id="u787662c9"></a>Mipmap 的主要作用是：

- <a id="uc13a7a90"></a>减少远处纹理闪烁
- <a id="uaccd7a32"></a>降低纹理缓存压力
- <a id="u488504ff"></a>提高缩小采样质量
- <a id="uca21b7df"></a>提升性能

<a id="i7vf7"></a>

---

<a id="FZCkM"></a>
## 八、第七章整体关系

<a id="u4371f3b3"></a>第七章的内容并不是相互独立的。

<a id="u8a9e81d1"></a>整体数据流程为：

<a id="EwoJx"></a>
```latex
Ch7-1
CPU 顶点数据
→ Vertex Buffer
→ Vertex Shader

Ch7-2
Index Buffer
→ 复用顶点
→ Indexed Draw

Ch7-3
Instance Data
→ 一次绘制多个实例

Ch7-4
Push Constant
→ 传递少量高频数据

Ch7-5
Uniform Buffer
→ Descriptor Set
→ 传递矩阵和全局数据

Ch7-6
Staging Buffer
→ VkImage
→ 图像复制和布局转换

Ch7-7
Texture Image
→ Image View
→ Sampler
→ Descriptor Set
→ Fragment Shader
```

<a id="HoWnb"></a>

---

<a id="CfMvb"></a>
## 九、各类数据的选择

<a id="eDhS8"></a>
### 1. 顶点缓冲区

<a id="u9555bff1"></a>适合：

- <a id="ubc1b6f29"></a>顶点位置
- <a id="u778ca006"></a>法线
- <a id="uf07df8b1"></a>UV
- <a id="ue029531c"></a>切线
- <a id="u94dba722"></a>顶点颜色

<a id="uf01c8701"></a>特点：

<a id="UFIEi"></a>
```latex
每个顶点读取一次
```

<a id="FbFE8"></a>

---

<a id="FjUK2"></a>
### 2. 索引缓冲区

<a id="u04fa885e"></a>适合：

- <a id="u2a956dda"></a>复用顶点
- <a id="u7c1a80f6"></a>减少重复几何数据

<a id="ud04768ca"></a>特点：

<a id="JxEK0"></a>
```latex
保存顶点编号
```

<a id="Ll0VT"></a>

---

<a id="wN4vd"></a>
### 3. 实例缓冲区

<a id="u43d8bb8f"></a>适合：

- <a id="ucb8af676"></a>大量相同网格
- <a id="u7418291f"></a>不同实例位置
- <a id="ucd2221e6"></a>不同实例颜色
- <a id="u1171e3cf"></a>不同实例模型矩阵

<a id="u4f4a6c10"></a>特点：

<a id="AK3zR"></a>
```latex
每个实例读取一次
```

<a id="aMlz8"></a>

---

<a id="nZXxi"></a>
### 4. Push Constant

<a id="u69f5005c"></a>适合：

- <a id="u05562b51"></a>少量数据
- <a id="u3f36665e"></a>高频修改
- <a id="u7897522b"></a>每个 Draw Call 都不同

<a id="u65485b00"></a>例如：

- <a id="u294dd553"></a>对象编号
- <a id="u3e981ef0"></a>小型变换参数
- <a id="uef41adb3"></a>颜色
- <a id="ub5d90384"></a>材质索引

<a id="JgA32"></a>

---

<a id="EjWpD"></a>
### 5. Uniform Buffer

<a id="u501e564f"></a>适合：

- <a id="ue58b31f4"></a>矩阵
- <a id="ue79d4d3e"></a>相机数据
- <a id="u4c2430bb"></a>灯光参数
- <a id="uac4d0c7d"></a>全局参数
- <a id="u3a435417"></a>较大只读数据

<a id="MeMyC"></a>

---

<a id="YnJvr"></a>
### 6. Texture Image

<a id="uc6ae6d08"></a>适合：

- <a id="u25c08ab3"></a>颜色贴图
- <a id="u6d5135ca"></a>法线贴图
- <a id="u9551b257"></a>深度贴图
- <a id="u94770820"></a>渲染结果
- <a id="u77efbe0b"></a>各种二维图像数据

<a id="R80w3"></a>

---

<a id="fhNRf"></a>
## 十、资源生命周期

<a id="u916bb665"></a>Vulkan 中资源的销毁顺序非常重要。

<a id="u6a561463"></a>Buffer 的销毁顺序：

<a id="hqblz"></a>
```latex
vkDestroyBuffer
→ vkFreeMemory
```

<a id="u3e60f36d"></a>Image 的销毁顺序：

<a id="ivK3T"></a>
```latex
vkDestroyImageView
→ vkDestroyImage
→ vkFreeMemory
```

<a id="ud8a5db50"></a>Sampler：

<a id="FlFqB"></a>
```latex
vkDestroySampler
```

<a id="ua1a05073"></a>Descriptor：

<a id="eXprC"></a>
```latex
vkDestroyDescriptorPool
vkDestroyDescriptorSetLayout
```

<a id="u5de6fe9f"></a>Pipeline：

<a id="Iq2s8"></a>
```latex
vkDestroyPipeline
→ vkDestroyPipelineLayout
```

<a id="u23274fad"></a>需要保证：

<a id="RDw8A"></a>
```latex
使用某资源的对象先销毁
被依赖的资源后销毁
```

<a id="ue149172d"></a>同时，在 GPU 仍可能使用资源时，不能直接销毁。

<a id="uaae16009"></a>通常需要等待：

- <a id="u529bfecb"></a>对应 Fence
- <a id="u616b1b2f"></a>Queue Idle
- <a id="u8091b895"></a>Device Idle

<a id="u81c7dbad"></a>但不应该在每一帧都使用：

<a id="h4ECK"></a>
```cpp
vkDeviceWaitIdle(...)
```

<a id="u6f720176"></a>来掩盖同步问题。

<a id="g87qZ"></a>

---

<a id="Nh9jf"></a>
## 十一、总结

<a id="u4c5682e7"></a>第七章主要完成了 Vulkan 中最基础的数据输入系统。

<a id="u74b68bd5"></a>从第二章中写死在 Shader 内部的三角形开始，逐步加入了：

<a id="JJydp"></a>
```latex
顶点缓冲区
索引缓冲区
实例化绘制
Push Constant
Uniform Buffer
Descriptor Set
图像复制
纹理采样
Mipmap
```

<a id="ud0ae0678"></a>最终形成了一条完整的数据传递链：

<a id="cBoEL"></a>
```latex
CPU 数据
→ Vulkan Buffer 或 Image
→ Device Memory
→ Descriptor 或 Vertex Input
→ Graphics Pipeline
→ Shader
→ 屏幕
```

<a id="u22d7d8f5"></a>可以将第七章概括为：

> <a id="u46b4a140"></a>
>
> <a id="u326ab696"></a>第七章解决了几何数据、实例数据、常量数据和图像数据如何从 CPU 传递到 GPU，并最终被 Vulkan Graphics Pipeline 和 Shader 使用的问题。

原文：[EasyVulkan 第七章学习笔记](<https://www.yuque.com/u62694975/iaaa/wtm8ednr7m6i7g7m>)
