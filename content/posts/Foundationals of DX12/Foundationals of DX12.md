\###  核心概念：什么是 HRESULT？ (The Why)

从技术上讲，`HRESULT` 是一个 \*\*32位整数\*\*（`long`），它是 COM (Component Object Model) 组件的标准返回值。DirectX 是基于 COM 构建的，所以沿用了这一标准。



`HRESULT` 是与图形硬件沟通的第一道防线，它是 API 调用的“心跳报告”。  



&nbsp;在 D3D12 中，几乎所有的 API 调用（创建设备、分配内存、编译着色器）都会返回一个 `HRESULT`。如果你忽略它，你就是在蒙眼狂奔。  



\*\*HRESULT 是一个变量类型（C++中的 \*\*`\*\*long\*\*`\*\*），它是 Windows 编程中用来记录函数执行结果（包括错误类型、成功状态）的标准载体。\*\*



在 DirectX 12 和 Windows COM 编程中，它不仅记录“出错了”，还记录“错哪了”甚至“成功了但有些小状况”。







&nbsp;在 C++ 的头文件定义中，它其实就是一个 32 位的整数：  typedef long HRESULT;所以，当你看到 HRESULT hr = ... 时，你本质上是在存一个数字。 但是，这个数字并不是随机生成的，它像一个\*\*“比特位地图”\*\*。







\### 2. 它的内部结构（为什么它是 32 位的？）

虽然它只是一个整数，但它的 32 个二进制位（bit）被划分成了三个特定的区域。这就好比身份证号码，每一段数字都有特定含义。



我们通常用 16 进制来看它，比如常见的失败代码 `0x80070057`：



\+ \*\*第 31 位 (Severity - 严重性)\*\*：\*\*最重要的一位！\*\*

&nbsp;   - `0` = 成功 (Success)

&nbsp;   - `1` = 失败 (Fail)

&nbsp;   - 这就是为什么所有的错误代码（如 `0x8...`）开头都是 8（二进制 `1000...`），因为第 31 位是 1。

\+ \*\*第 16-30 位 (Facility - 来源)\*\*：表示是谁报错的。

&nbsp;   - 比如 `0x007` 代表 Win32 API，`0x87A` 代表 DXGI (DirectX Graphics Infrastructure)。

\+ \*\*第 0-15 位 (Code - 具体代码)\*\*：具体的错误原因。

&nbsp;   - 比如 `5` 代表 "Access Denied" (拒绝访问)，`57` 代表 "Invalid Argument" (参数无效)。







\*\*throw\*\*的含义：



<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1767858435646-14cf2102-0e62-45d5-8b6b-88855d231ff3.png" width="2560" title="" crop="0,0,1,1" id="ua3f2fe88" class="ne-image">







GUID ：  它本质上是一个 \*\*128位 (16字节)\*\* 的超大整数， 是每一个组件的“身份证”







\*\* IID\_PPV\_ARGS  ：\*\*



实现代码：#define IID\_PPV\_ARGS(ppType)  \_\_uuidof(\*\*\*\*(ppType)), (void\*\*\*\*)(ppType)



1.自动获取GUID，防止自己手误填错；



/\*假设你传入的是 \&device： 



&nbsp;1）device 的类型是 ID3D12Device\*（指向设备的指针）。 



2）ppType (也就是 \&device) 的类型是 ID3D12Device\*\*（指向指针的指针）。  



3）\*(ppType) 解引用一次，变成了 ID3D12Device\*。 



&nbsp;4）\*\*(ppType) 再解引用一次，变成了 ID3D12Device (类型本身)。 



&nbsp;结论：\_\_uuidof 直接去查\*\*“你传入的这个变量所属的类型”\*\*的身份证号。 如果你传的是 device，它就自动填 ID3D12Device 的 GUID。你根本没有机会填错\*/



2.进行类型转换，返回指向函数的指针







\*\*Fence\*\*:



实质： Fence 本质上就是一个所有的 CPU 和 GPU 都能访问的 64位整数 (`UINT64`)  



e.g.   1.<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1767871390115-d4ba0b9e-bd21-4d02-b6e9-dcac8b44fc62.png" width="1116" title="" crop="0,0,1,1" id="uc995e86f" class="ne-image"><img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1767871392729-a05ab7ee-5d12-4470-8389-4d0d70c2fe1c.png" width="1087" title="" crop="0,0,1,1" id="u3936e926" class="ne-image">



2\.



<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1768051600477-e26cb547-a5fc-4c3d-8141-1f316f916061.png" width="1077" title="" crop="0,0,1,1" id="uc226ff29" class="ne-image"><img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1768051604169-6e789970-c477-4a1c-a388-f0d5ba30374b.png" width="1133" title="" crop="0,0,1,1" id="udb8e8710" class="ne-image">



ps：这个方法是强制刷新命令队列，cpu会一直对单帧的绘制进行等待；后面用到了其他的方法，叫做双缓冲或三缓冲，意思是在提交了第一帧的命令之后，CPU不会傻等，而是去填写第二帧与第三帧命令，此时只有当第一帧还没有绘制完时，CPU才会等待



\*\*获取描述符大小：\*\*



作用：<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1767874749688-59343db3-8e6e-4c8e-a3ca-a5e7234857fb.png" width="1039" title="" crop="0,0,1,1" id="u55375e0c" class="ne-image">



\*\*\*\*



\*\*设置MSAA抗锯齿属性\*\*：



flag：



<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1767876663128-35d051cf-351b-43be-b98b-20e633fd4d73.png" width="1100" title="" crop="0,0,1,1" id="u60a8726b" class="ne-image">



D3D12 的硬件兼容性检查非常严格。



\+ 你不能直接问“支持 MSAA 吗？”

\+ 你必须精确地问：“对于 \*\*R8G8B8A8\*\* 这种颜色格式，做 \*\*4倍\*\* 采样，你支不支持？”

\+ 如果你换了颜色格式（比如 `DXGI\_FORMAT\_R16G16B16A16\_FLOAT` HDR格式），你得重新问一次，因为显卡可能支持普通颜色的 MSAA，但不支持 HDR 颜色的 MSAA。







\*\*命令队列和命令列表\*\*



<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1767952509657-16f8e367-8ee2-4a71-b5ef-98d6fe0bf871.png" width="1072" title="" crop="0,0,1,1" id="u8475330e" class="ne-image">



&nbsp;CPU 使用命令列表（List）作为工具，将指令数据写死在分配器（Allocator）提供的内存上，最后将整块内存的引用交给队列（Queue）去执行  







\*\*交换链：\*\*



<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1767956671742-e6cf4896-826f-47f9-9fd7-5ce49a6a4c03.png" width="1072" title="" crop="0,0,1,1" id="u677fabe6" class="ne-image">



<font style="color:rgb(25, 27, 31);background-color:rgb(244, 246, 249);">交换链本质就是观众在看A黑板而这时候你在写B黑板，之后在把B黑板调换位置，观众永远能看见完整画面</font>



<font style="color:rgb(25, 27, 31);background-color:rgb(244, 246, 249);"></font>



\*\*<font style="color:rgb(25, 27, 31);background-color:rgb(244, 246, 249);">CD3DX12\_CLEAR\_VALUE optClear</font>\*\*<font style="color:rgb(25, 27, 31);background-color:rgb(244, 246, 249);">：</font>



<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1768040901438-52c96713-c18b-492c-99c8-d7f5ae5880bc.png" width="700" title="" crop="0,0,1,1" id="uc287a13b" class="ne-image">



\*\*资源的转换：\*\*



<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1768045083192-efae522a-f5de-4826-8171-c8c017381636.png" width="1078" title="" crop="0,0,1,1" id="u52678255" class="ne-image">







关于为什么每次使用comptr类型变量都要调用Get（）方法：



<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1768052947743-4edacf00-3f94-487c-8f99-9523a8789996.png" width="1063" title="" crop="0,0,1,1" id="u7d414d1f" class="ne-image"><img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1768052950506-bce60ed6-4410-42db-b2c3-db74601909b0.png" width="1058" title="" crop="0,0,1,1" id="u2b422304" class="ne-image"><img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1768052952470-7ad53705-f76f-4f0d-af7b-06a71bb29b79.png" width="1061" title="" crop="0,0,1,1" id="u122b89fd" class="ne-image">







\*\*窗口的初始化：\*\*



&nbsp;在 Windows 中，你不能直接说“给我个窗口”。你必须先填写一张详细的“申请表”，定义这个窗口的行为和长相：WNDCLASS wc;



<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1768131688901-958357cd-13b6-44d0-afb9-37fbcd072a08.png" width="1073" title="" crop="0,0,1,1" id="ubad6968c" class="ne-image"><img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1768131688914-d159d54a-4230-4ac2-9589-f88d8ee55985.png" width="1077" title="" crop="0,0,1,1" id="u9af8d13e" class="ne-image"><img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1768131692429-7fda06bc-10a6-4796-9a5c-0ec3c42a4d25.png" width="1083" title="" crop="0,0,1,1" id="ufe0447d0" class="ne-image">



\*\*为什么rtv和dsv要用句柄访问而不是直接使用堆上的数据\*\*：



<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1768139340321-62ed2e2a-171d-4886-876e-87e72b260d31.png" width="1061" title="" crop="0,0,1,1" id="ub14d8276" class="ne-image"><img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1768139341573-b6898d4b-76e1-4cb5-8a1a-9c3cc0ad8449.png" width="1105" title="" crop="0,0,1,1" id="uad404180" class="ne-image"><img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1768139343380-7beed20c-cfb7-419c-b5ec-fb2098f4be10.png" width="1092" title="" crop="0,0,1,1" id="ueddc9e94" class="ne-image">







`\*\*D3D12\_RESOURCE\_STATE\_PRESENT\*\*` 是 CPU、GPU 渲染核心、显示控制器三者之间的一个\*\*契约\*\*。



它保证了当屏幕读取数据时，数据是\*\*完整的\*\*、\*\*可读的\*\*且\*\*不再被修改的\*\*。如果你不切换到这个状态直接 Present，Debug Layer 会直接报错，而在真机上，你可能会看到花屏、闪烁或者显卡驱动崩溃。



\*\*\*\*



\*\*深度/模板测试：\*\*



Part1 ：  

&nbsp;      实现镜面效果------



一种方法是模板测试，但这种方法仅局限于不产生形变的平面镜。



首先沿着镜面的对称轴（镜面Local Space的x轴（应该是吧？））再创建一个一样的模型，接着根据对称轴创建镜像矩阵，将光照方向也镜像，这个光照将用于镜像物体的渲染



之后我们需要在RenderItem结构体中添加layer成员变量，用于控制渲染过程使用的不同的passconstant ： 在BuildRenderItems（）中赋予属性，在Draw（）中进行调用



















