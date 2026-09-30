---
title: "DX12：HRESULT 与错误检查"
slug: "directx12-hresult"
summary: "整理 HRESULT 的返回值含义、位字段和成功与失败判断，以及 DirectX 12 调用中的错误检查方式。"
categories: ["DirectX 12"]
tags: ["DirectX 12", "DX12", "HRESULT", "COM", "Error Handling"]
date: "2026-01-08T06:51:51.000Z"
lastmod: "2026-05-19T13:38:41.000Z"
draft: false
yuque_slug: "rhd7wb13tid8hgze"
source: "https://www.yuque.com/u62694975/iaaa/rhd7wb13tid8hgze"
---

<a id="9b766925"></a>
### 核心概念：什么是 HRESULT？ (The Why)

<a id="u1da5dcf4"></a>从技术上讲，`HRESULT` 是一个 <strong>32位整数</strong>（`long`），它是 COM (Component Object Model) 组件的标准返回值。DirectX 是基于 COM 构建的，所以沿用了这一标准。

<a id="ub3c6201d"></a>`HRESULT` 是与图形硬件沟通的第一道防线，它是 API 调用的“心跳报告”。

<a id="u564874ce"></a>在 D3D12 中，几乎所有的 API 调用（创建设备、分配内存、编译着色器）都会返回一个 `HRESULT`。如果你忽略它，你就是在蒙眼狂奔。

<a id="ufc40ff52"></a><strong>HRESULT 是一个变量类型（C++中的 </strong>`long`<strong>），它是 Windows 编程中用来记录函数执行结果（包括错误类型、成功状态）的标准载体。</strong>

<a id="u0d0dbce6"></a>在 DirectX 12 和 Windows COM 编程中，它不仅记录“出错了”，还记录“错哪了”甚至“成功了但有些小状况”。

<a id="u7767eb7c"></a>在 C++ 的头文件定义中，它其实就是一个 32 位的整数：  typedef long HRESULT;所以，当你看到 HRESULT hr = ... 时，你本质上是在存一个数字。 但是，这个数字并不是随机生成的，它像一个<strong>“比特位地图”</strong>。

<a id="3af2e8ca"></a>
### 2. 它的内部结构（为什么它是 32 位的？）

<a id="u5b542639"></a>虽然它只是一个整数，但它的 32 个二进制位（bit）被划分成了三个特定的区域。这就好比身份证号码，每一段数字都有特定含义。

<a id="u42fc4fcd"></a>我们通常用 16 进制来看它，比如常见的失败代码 `0x80070057`：

- <a id="u3ae41162"></a><strong>第 31 位 (Severity - 严重性)</strong>：<strong>最重要的一位！</strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u02c78685"><code id="u7e73f3d6"><span id="ua96e150d">0</span></code><span id="u1b0b9097"> = 成功 (Success)</span></li><li id="u4f5e57e9"><code id="ub53c9fd1"><span id="ua2579bce">1</span></code><span id="u196a6ad0"> = 失败 (Fail)</span></li><li id="u4916511b"><span id="u559e551b">这就是为什么所有的错误代码（如 </span><code id="ubc5ea377"><span id="ufa57c520">0x8...</span></code><span id="u683f4d32">）开头都是 8（二进制 </span><code id="uf8a06da1"><span id="udf6eed64">1000...</span></code><span id="u68ef1b36">），因为第 31 位是 1。</span></li></ul>

- <a id="u524db7eb"></a><strong>第 16-30 位 (Facility - 来源)</strong>：表示是谁报错的。

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u8f668807"><span id="u36fb31af">比如 </span><code id="ud26a08f6"><span id="u4c9188e5">0x007</span></code><span id="u393e2425"> 代表 Win32 API，</span><code id="ufbb37916"><span id="u86e287a2">0x87A</span></code><span id="u872415e8"> 代表 DXGI (DirectX Graphics Infrastructure)。</span></li></ul>

- <a id="u6cd54154"></a><strong>第 0-15 位 (Code - 具体代码)</strong>：具体的错误原因。

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u83469258"><span id="ud66278e7">比如 </span><code id="uc6c4e09a"><span id="uad289e96">5</span></code><span id="u2d8a70e0"> 代表 "Access Denied" (拒绝访问)，</span><code id="u6fa18b57"><span id="u02c30f10">57</span></code><span id="u6115011b"> 代表 "Invalid Argument" (参数无效)。</span></li></ul>

<a id="uad7b634d"></a><strong>throw</strong>的含义：

<a id="u7e393ee7"></a><a id="ua3f2fe88"></a><img src="/images/directx12-hresult/directx12-hresult-01.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="u0772ce88"></a>GUID ：  它本质上是一个 <strong>128位 (16字节)</strong> 的超大整数， 是每一个组件的“身份证”

<a id="ud5c8878d"></a><strong> IID\_PPV\_ARGS  ：</strong>

<a id="u93973540"></a>实现代码：#define IID\_PPV\_ARGS(ppType)  \_\_uuidof(\*\*<strong>(ppType)), (void\*\*</strong>)(ppType)

<a id="u1bb5cdb3"></a>1.自动获取GUID，防止自己手误填错；

<a id="ua41d2b41"></a>/\*假设你传入的是 &amp;device：

<a id="uf258d1a0"></a>1）device 的类型是 ID3D12Device\*（指向设备的指针）。

<a id="u5066d0e2"></a>2）ppType (也就是 &amp;device) 的类型是 ID3D12Device\*\*（指向指针的指针）。

<a id="ue0cc2d82"></a>3）\*(ppType) 解引用一次，变成了 ID3D12Device\*。

<a id="u13f64a04"></a>4）\*\*(ppType) 再解引用一次，变成了 ID3D12Device (类型本身)。

<a id="u4c3fd156"></a>结论：\_\_uuidof 直接去查<strong>“你传入的这个变量所属的类型”</strong>的身份证号。 如果你传的是 device，它就自动填 ID3D12Device 的 GUID。你根本没有机会填错\*/

<a id="u459963fa"></a>2.进行类型转换，返回指向函数的指针

<a id="ue630d15a"></a><strong>Fence</strong>:

<a id="u057b1d89"></a>实质： Fence 本质上就是一个所有的 CPU 和 GPU 都能访问的 64位整数 (`UINT64`)

<a id="ufd7b9268"></a>e.g.   1.<a id="uc995e86f"></a><img src="/images/directx12-hresult/directx12-hresult-02.png" alt="" loading="lazy" style="max-width: 100%; height: auto"><a id="u3936e926"></a><img src="/images/directx12-hresult/directx12-hresult-03.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="u938e8ceb"></a>2.

<a id="u17f3b925"></a><a id="uc226ff29"></a><img src="/images/directx12-hresult/directx12-hresult-04.png" alt="" loading="lazy" style="max-width: 100%; height: auto"><a id="udb8e8710"></a><img src="/images/directx12-hresult/directx12-hresult-05.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="u4066a9ce"></a>ps：这个方法是强制刷新命令队列，cpu会一直对单帧的绘制进行等待；后面用到了其他的方法，叫做双缓冲或三缓冲，意思是在提交了第一帧的命令之后，CPU不会傻等，而是去填写第二帧与第三帧命令，此时只有当第一帧还没有绘制完时，CPU才会等待

<a id="ufb5e983a"></a><strong>获取描述符大小：</strong>

<a id="ub53a2890"></a>作用：<a id="u55375e0c"></a><img src="/images/directx12-hresult/directx12-hresult-06.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="uc838e021"></a><strong>设置MSAA抗锯齿属性</strong>：

<a id="ua09079f1"></a>flag：

<a id="u0f2ff304"></a><a id="u60a8726b"></a><img src="/images/directx12-hresult/directx12-hresult-07.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="u47577040"></a>D3D12 的硬件兼容性检查非常严格。

- <a id="u0b5a5a17"></a>你不能直接问“支持 MSAA 吗？”
- <a id="u1451e194"></a>你必须精确地问：“对于 <strong>R8G8B8A8</strong> 这种颜色格式，做 <strong>4倍</strong> 采样，你支不支持？”
- <a id="ua46b3ac1"></a>如果你换了颜色格式（比如 `DXGI_FORMAT_R16G16B16A16_FLOAT` HDR格式），你得重新问一次，因为显卡可能支持普通颜色的 MSAA，但不支持 HDR 颜色的 MSAA。

<a id="u720696f0"></a><strong>命令队列和命令列表</strong>

<a id="u35fd2e05"></a><a id="u8475330e"></a><img src="/images/directx12-hresult/directx12-hresult-08.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="ub98439f8"></a>CPU 使用命令列表（List）作为工具，将指令数据写死在分配器（Allocator）提供的内存上，最后将整块内存的引用交给队列（Queue）去执行

<a id="u24555bb0"></a><strong>交换链：</strong>

<a id="ufb8c471f"></a><a id="u677fabe6"></a><img src="/images/directx12-hresult/directx12-hresult-09.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="u929ea2ad"></a><span style="color: rgb(25, 27, 31); background-color: rgb(244, 246, 249)">交换链本质就是观众在看A黑板而这时候你在写B黑板，之后在把B黑板调换位置，观众永远能看见完整画面</span>

<a id="u9a99fe6c"></a><strong><span style="color: rgb(25, 27, 31); background-color: rgb(244, 246, 249)">CD3DX12\_CLEAR\_VALUE optClear</span></strong><span style="color: rgb(25, 27, 31); background-color: rgb(244, 246, 249)">：</span>

<a id="u7f365291"></a><a id="uc287a13b"></a><img src="/images/directx12-hresult/directx12-hresult-10.png" alt="" loading="lazy" width="700" height="261" style="max-width: 100%; height: auto">

<a id="udbb5e396"></a><strong>资源的转换：</strong>

<a id="ucfbd8ea4"></a><a id="u52678255"></a><img src="/images/directx12-hresult/directx12-hresult-11.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="ud1cde668"></a>关于为什么每次使用comptr类型变量都要调用Get（）方法：

<a id="ubd7eedcf"></a><a id="u7d414d1f"></a><img src="/images/directx12-hresult/directx12-hresult-12.png" alt="" loading="lazy" style="max-width: 100%; height: auto"><a id="u2b422304"></a><img src="/images/directx12-hresult/directx12-hresult-13.png" alt="" loading="lazy" style="max-width: 100%; height: auto"><a id="u122b89fd"></a><img src="/images/directx12-hresult/directx12-hresult-14.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="u2967cab4"></a><strong>窗口的初始化：</strong>

<a id="u7d6c6e45"></a>在 Windows 中，你不能直接说“给我个窗口”。你必须先填写一张详细的“申请表”，定义这个窗口的行为和长相：WNDCLASS wc;

<a id="u7a94585b"></a><a id="ubad6968c"></a><img src="/images/directx12-hresult/directx12-hresult-15.png" alt="" loading="lazy" style="max-width: 100%; height: auto"><a id="u9af8d13e"></a><img src="/images/directx12-hresult/directx12-hresult-16.png" alt="" loading="lazy" style="max-width: 100%; height: auto"><a id="ufe0447d0"></a><img src="/images/directx12-hresult/directx12-hresult-17.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="u690489eb"></a><strong>为什么rtv和dsv要用句柄访问而不是直接使用堆上的数据</strong>：

<a id="ua3b38fc4"></a><a id="ub14d8276"></a><img src="/images/directx12-hresult/directx12-hresult-18.png" alt="" loading="lazy" style="max-width: 100%; height: auto"><a id="uad404180"></a><img src="/images/directx12-hresult/directx12-hresult-19.png" alt="" loading="lazy" style="max-width: 100%; height: auto"><a id="ueddc9e94"></a><img src="/images/directx12-hresult/directx12-hresult-20.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

<a id="uad17e119"></a>`D3D12_RESOURCE_STATE_PRESENT` 是 CPU、GPU 渲染核心、显示控制器三者之间的一个<strong>契约</strong>。

<a id="u8a7b05c6"></a>它保证了当屏幕读取数据时，数据是<strong>完整的</strong>、<strong>可读的</strong>且<strong>不再被修改的</strong>。如果你不切换到这个状态直接 Present，Debug Layer 会直接报错，而在真机上，你可能会看到花屏、闪烁或者显卡驱动崩溃。

<a id="ue388c86d"></a><strong>深度/模板测试：</strong>

<a id="ua09f79a0"></a>Part1 ：  
       实现镜面效果------

<a id="u340819cc"></a>一种方法是模板测试，但这种方法仅局限于不产生形变的平面镜。

<a id="u663c6972"></a>首先沿着镜面的对称轴（镜面Local Space的x轴（应该是吧？））再创建一个一样的模型，接着根据对称轴创建镜像矩阵，将光照方向也镜像，这个光照将用于镜像物体的渲染

<a id="ueb4b0b14"></a>之后我们需要在RenderItem结构体中添加layer成员变量，用于控制渲染过程使用的不同的passconstant ： 在BuildRenderItems（）中赋予属性，在Draw（）中进行调用

原文：[DX12](<https://www.yuque.com/u62694975/iaaa/rhd7wb13tid8hgze>)
