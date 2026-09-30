---
title: "CPU 路径追踪器项目细节"
slug: "pathtracer-project-details"
summary: "整理个人 CPU 路径追踪器的模块分工、PBR 与 IBL、MIS 采样及 BVH 和多线程性能优化。"
categories: ["图形学"]
tags: ["Computer Graphics", "Path Tracing", "PBR", "IBL", "MIS", "C++"]
date: "2026-05-26T05:46:15.000Z"
lastmod: "2026-05-26T14:12:44.000Z"
draft: false
yuque_slug: "erbuu8ky9dn39bpn"
source: "https://www.yuque.com/u62694975/iaaa/erbuu8ky9dn39bpn"
---

<a id="u731bd154"></a><strong>第 1 题：简历深挖 / 项目动机</strong>

<a id="uad9e4e30"></a><strong>你简历里写了一个支持 PBR / IBL / MIS 的 CPU 路径追踪渲染器。请你介绍一下这个项目的整体架构：从场景加载、光线生成、材质采样、光照估计到最终成像，主要模块是怎么串起来的？</strong>

1. <a id="uf239222f"></a><strong><span style="color: #262626">总体架构</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="uf555dfc4"><span id="ua583e72b" style="color: #262626">项目主要分成 Camera、Scene / Hittable、BVH、Material、PDF、Environment、Renderer 几个模块。</span></li><li id="u372a20d3"><span id="u2811ed84" style="color: #262626">渲染时按 tile 并行遍历像素，每个像素发射多条 camera ray，累积 radiance 后输出 PPM。</span></li></ul>

2. <a id="u5de8543b"></a><strong><span style="color: #262626">场景与加速结构</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u508b56cd"><span id="u3b7b050b" style="color: #262626">OBJ/MTL 解析生成 Triangle / Material。</span></li><li id="uc2e0dd86"><span id="uc6c990f8" style="color: #262626">三角形和几何体统一进 Hittable 接口。</span></li><li id="u43416fda"><span id="u4512c916" style="color: #262626">构建 BVH，减少每条 ray 的相交测试成本。</span></li></ul>

3. <a id="u3cdee44b"></a><strong><span style="color: #262626">光线与材质</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u019abbff"><span id="u097146fa" style="color: #262626">Camera 生成 primary ray。</span></li><li id="u6eefb56c"><span id="u81bff454" style="color: #262626">命中物体后通过 Material 接口计算 BSDF、PDF、scatter 方向。</span></li><li id="u84fe255e"><span id="u83878a68" style="color: #262626">材质接口拆成 Scatter / Eval / PDF，是为了让 Lambert、Metal、Dielectric、PBR 材质共用同一套积分流程。</span></li></ul>

4. <a id="ua65110dd"></a><strong><span style="color: #262626">光照估计</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="uec77583f"><span id="u0a03d1ae" style="color: #262626">使用 Monte Carlo 估计渲染方程。</span></li><li id="u4117458c"><span id="u3781a458" style="color: #262626">直接光部分结合 light sampling / environment sampling / BSDF sampling。</span></li><li id="uc9c4b4c8"><span id="ua989b0fb" style="color: #262626">使用 MIS 的 power heuristic 平衡不同采样策略，减少只靠随机打中光源带来的高噪声问题。</span></li></ul>

5. <a id="u86480865"></a><strong><span style="color: #262626">结果与优化</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u56916066"><span id="uf44b4fc5" style="color: #262626">支持 PBR、IBL、HDRI 环境光、normal map、OBJ/MTL。</span></li><li id="u886be492"><span id="ue2741051" style="color: #262626">用 BVH、多线程 tile 渲染和 thread-local RNG 优化性能。</span></li><li id="u164c8365"><span id="u3ac8415a" style="color: #262626">基准场景下从 65.33s 降到 29.99s，约 2.18x 提速。</span></li></ul>

<a id="ua751c025"></a><span style="color: #262626">你这题改进的关键是：少讲“路径追踪一般怎么做”，多讲“我的代码里哪些模块承担什么职责”。</span>

<a id="ue678ec49"></a><strong><span style="color: rgb(26, 28, 31)">第 2 题：专业深挖 / MIS</span></strong>

<a id="ud16c43f2"></a><strong><span style="color: rgb(26, 28, 31)">你简历里写到实现了 HDRI 环境光重要性采样 和 light / BSDF 的 MIS 采样框架。请你解释一下：为什么只做 BSDF 采样或者只做光源采样都不够？MIS 在你的渲染器里具体解决了什么问题？</span></strong>

1. <a id="u9e990522"></a><strong><span style="color: rgb(26, 28, 31)">为什么单一采样不够</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="ud8ae81dd"><span id="u1e11f446" style="color: rgb(26, 28, 31)">Monte Carlo 积分的方差和</span><span id="u6d158730" style="color: rgb(26, 28, 31)">f(x) / pdf(x)</span><span id="u5a870140" style="color: rgb(26, 28, 31)">的波动有关。</span></li><li id="ua070cb70"><span id="u69db309a" style="color: rgb(26, 28, 31)">如果采样分布和被积函数不匹配，就会出现高方差和 firefly。</span></li><li id="u07b7f753"><span id="u29a694f0" style="color: rgb(26, 28, 31)">BSDF 采样适合 glossy / specular lobe 明显的方向，但对小面积光源命中率低。</span></li><li id="u036df396"><span id="uc553496e" style="color: rgb(26, 28, 31)">Light sampling 能稳定采到光源方向，但对高光材质或复杂 BSDF 方向不一定匹配。</span></li></ul>

2. <a id="u8c3de0fc"></a><strong><span style="color: rgb(26, 28, 31)">MIS 解决什么问题</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="ubdcae46c"><span id="u86f016f8" style="color: rgb(26, 28, 31)">MIS 不是二选一，而是把不同采样策略的贡献按权重合并。</span></li><li id="u8a89c416"><span id="u489b9d62" style="color: rgb(26, 28, 31)">我的项目里主要结合了 light sampling、environment sampling 和 BSDF sampling。</span></li><li id="u20be4d72"><span id="u4922dd00" style="color: rgb(26, 28, 31)">使用 power heuristic，根据当前方向在不同策略下的 PDF 计算权重，降低单一策略失配带来的噪点。</span></li></ul>

3. <a id="uffc60095"></a><strong><span style="color: rgb(26, 28, 31)">IBL 场景下为什么更需要 MIS</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u307d4e49"><span id="u5971cd4f" style="color: rgb(26, 28, 31)">HDRI 环境光可以看作包围场景的无限远光源。</span></li><li id="ua04c3d8e"><span id="u2f65083d" style="color: rgb(26, 28, 31)">如果只靠 BSDF 随机采样，可能很难稳定采到 HDR 中高亮区域。</span></li><li id="u975687ad"><span id="u1333e125" style="color: rgb(26, 28, 31)">因此对 HDRI 按亮度和球面面积做重要性采样，再和 BSDF 采样通过 MIS 合并，可以更稳定估计环境光贡献。</span></li></ul>

4. <a id="u3a5a9b2d"></a><strong><span style="color: rgb(26, 28, 31)">一句结果</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u6d1abe62"><span id="u6671ed45" style="color: rgb(26, 28, 31)">所以 MIS 在我的渲染器里主要用于降低直接光、HDRI 和高光材质组合下的方差，让相同 spp 下的图像更稳定。</span></li></ul>

<a id="u9d14f3fa"></a><strong><span style="color: rgb(26, 28, 31)">第 3 题：专业深挖 / PBR 材质接口</span></strong>

<a id="u85928cad"></a><strong><span style="color: rgb(26, 28, 31)">你简历里写了 Scatter / Eval / PDF 分离式材质接口。请你解释一下为什么要这样拆？如果不拆，把所有材质逻辑都写在 </span></strong><strong><span style="color: rgb(26, 28, 31)">ray\_color()</span></strong><strong><span style="color: rgb(26, 28, 31)"> 或颜色递归函数里，会带来什么问题？</span></strong>

1. <a id="u18a8a4ca"></a><strong><span style="color: rgb(26, 28, 31)">三个接口职责</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="uaeb0bdd8"><span id="udf67a8a2" style="color: rgb(26, 28, 31)">Scatter</span><span id="u092a3f5a" style="color: rgb(26, 28, 31)">：根据材质和入射方向采样下一条 ray，返回采样方向、衰减、是否为 delta/specular 路径等。</span></li><li id="u943a2268"><span id="u0fabca27" style="color: rgb(26, 28, 31)">Eval</span><span id="ufabc7950" style="color: rgb(26, 28, 31)">：给定</span><span id="u2c938d63" style="color: rgb(26, 28, 31)">wo</span><span id="uf1ed5728" style="color: rgb(26, 28, 31)">和</span><span id="u3f378b73" style="color: rgb(26, 28, 31)">wi</span><span id="ue1c63b1e" style="color: rgb(26, 28, 31)">，计算该方向组合下的 BSDF/BRDF 值。</span></li><li id="u3b19bfbc"><span id="u70ba1416" style="color: rgb(26, 28, 31)">PDF</span><span id="u9d638779" style="color: rgb(26, 28, 31)">：计算该材质在某个采样方向上的概率密度，用于 Monte Carlo 权重和 MIS。</span></li></ul>

2. <a id="ubbc52c23"></a><strong><span style="color: rgb(26, 28, 31)">为什么要拆</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="ud9d5845b"><span id="ud0ef31b1" style="color: rgb(26, 28, 31)">路径追踪主流程只关心“采样方向、评价 BSDF、计算 PDF、递归/迭代累积 radiance”。</span></li><li id="ufd4d2714"><span id="ua5c41f8c" style="color: rgb(26, 28, 31)">不同材质只需要实现自己的采样和评价逻辑，主渲染函数不需要知道 Lambert、Metal、Dielectric、PBR 的细节。</span></li><li id="ucc9931e0"><span id="ubf7d7b38" style="color: rgb(26, 28, 31)">这样</span><span id="u1a1272de" style="color: rgb(26, 28, 31)">ray_color()</span><span id="u1452e48b" style="color: rgb(26, 28, 31)">保持为统一积分框架，而不是堆满材质分支。</span></li></ul>

3. <a id="u810147f0"></a><strong><span style="color: rgb(26, 28, 31)">和 MIS 的关系</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u0d3c1555"><span id="u930747a3" style="color: rgb(26, 28, 31)">MIS 需要知道同一个方向在 BSDF sampling 和 light sampling 下各自的 PDF。</span></li><li id="uf3104b7a"><span id="u7b12a69b" style="color: rgb(26, 28, 31)">如果没有独立的</span><span id="u87c6329b" style="color: rgb(26, 28, 31)">PDF</span><span id="u6c353e6f" style="color: rgb(26, 28, 31)">和</span><span id="ubf03af50" style="color: rgb(26, 28, 31)">Eval</span><span id="u0a3521eb" style="color: rgb(26, 28, 31)">，就很难把 light sampling 采到的方向再拿回材质上正确计算 BSDF 与 pdf。</span></li><li id="u4ec4f76e"><span id="u21fcab19" style="color: rgb(26, 28, 31)">所以接口拆分不是单纯为了代码好看，而是为了支持多采样策略组合。</span></li></ul>

4. <a id="u9fa0ad3f"></a><strong><span style="color: rgb(26, 28, 31)">扩展性</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u001b6460"><span id="u49d2625d" style="color: rgb(26, 28, 31)">后续增加 GGX、normal map、metallic-roughness、透明材质时，只改材质类，不破坏主渲染流程。</span></li><li id="u26829738"><span id="u0a5bbbf5" style="color: rgb(26, 28, 31)">这更接近引擎里的模块化设计思路。</span></li></ul>

<a id="ue8255c17"></a><span style="color: rgb(26, 28, 31)">你这题可以补一句关键总结：</span><strong><span style="color: rgb(26, 28, 31)">Scatter 负责“怎么采”，Eval 负责“这个方向贡献是多少”，PDF 负责“这个方向被采到的概率是多少”。</span></strong>

<a id="ub00f463f"></a><strong><span style="color: rgb(26, 28, 31)">第 4 题：专业问题 / DirectX 12 管线</span></strong>

<a id="u1ff5a93a"></a><strong><span style="color: rgb(26, 28, 31)">你简历里写了一个 DirectX 12 实时渲染器。请你讲一下在 DX12 中，一帧从 CPU 端提交命令到最终显示到屏幕，大致会经过哪些步骤？重点说一下 Command List、Command Queue、Back Buffer、Present 和 Fence 的作用。</span></strong>

1. <a id="u3c404bc7"></a><strong><span style="color: rgb(26, 28, 31)">获取当前 Back Buffer</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="uef0517e2"><span id="u1affd405" style="color: rgb(26, 28, 31)">每帧先通过 Swap Chain 获取当前 back buffer index。</span></li><li id="u951c9871"><span id="u7a9dd807" style="color: rgb(26, 28, 31)">Back Buffer 是这一帧的渲染目标之一，最终会被 Present 到屏幕。</span></li></ul>

2. <a id="uae294bb0"></a><strong><span style="color: rgb(26, 28, 31)">重置命令资源</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u86db85a8"><span id="uded12ac0" style="color: rgb(26, 28, 31)">等待对应 frame resource 的 Fence，确保 GPU 不再使用这一帧的 CommandAllocator。</span></li><li id="u8f3f978a"><span id="u8c9484f9" style="color: rgb(26, 28, 31)">Reset CommandAllocator 和 CommandList，开始录制本帧命令。</span></li></ul>

3. <a id="uf350cf49"></a><strong><span style="color: rgb(26, 28, 31)">资源状态转换</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="uea1afc6e"><span id="u9a1cb289" style="color: rgb(26, 28, 31)">将 Back Buffer 从</span><span id="ub8c0043c" style="color: rgb(26, 28, 31)">PRESENT</span><span id="u5740a98d" style="color: rgb(26, 28, 31)">转到</span><span id="ucf890d71" style="color: rgb(26, 28, 31)">RENDER_TARGET</span><span id="ua4fea490" style="color: rgb(26, 28, 31)">。</span></li><li id="u571b6e67"><span id="uca9536a3" style="color: rgb(26, 28, 31)">设置 RTV / DSV，清空颜色缓冲和深度缓冲。</span></li></ul>

4. <a id="ub31f3468"></a><strong><span style="color: rgb(26, 28, 31)">录制绘制命令</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u95a36939"><span id="u9201e1ea" style="color: rgb(26, 28, 31)">设置 Root Signature、PSO、Descriptor Heap、Viewport、Scissor、Vertex Buffer、Index Buffer 等。</span></li><li id="ud0e3d32f"><span id="ub0ec0b9e" style="color: rgb(26, 28, 31)">调用 DrawCall，把绘制命令写入 Command List。</span></li></ul>

5. <a id="ua16f706e"></a><strong><span style="color: rgb(26, 28, 31)">切回显示状态并提交</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u2f4910f7"><span id="ub0495b26" style="color: rgb(26, 28, 31)">渲染结束后，将 Back Buffer 从</span><span id="u546f9865" style="color: rgb(26, 28, 31)">RENDER_TARGET</span><span id="u2d7b023f" style="color: rgb(26, 28, 31)">转回</span><span id="u6aea49b8" style="color: rgb(26, 28, 31)">PRESENT</span><span id="u9527dcf7" style="color: rgb(26, 28, 31)">。</span></li><li id="u29395f14"><span id="ub0b4e51b" style="color: rgb(26, 28, 31)">Close CommandList。</span></li><li id="u04942f4c"><span id="ub7a0b3e6" style="color: rgb(26, 28, 31)">通过 Command Queue 执行：</span><span id="u646afb34" style="color: rgb(26, 28, 31)">ExecuteCommandLists()</span><span id="u612dfa1b" style="color: rgb(26, 28, 31)">。</span></li></ul>

6. <a id="u87015bb8"></a><strong><span style="color: rgb(26, 28, 31)">显示与同步</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="uc1dc8c7b"><span id="uf54790a8" style="color: rgb(26, 28, 31)">调用</span><span id="ua489bef9" style="color: rgb(26, 28, 31)">SwapChain-&gt;Present()</span><span id="u401cd7f5" style="color: rgb(26, 28, 31)">，把当前 Back Buffer 交给显示系统。</span></li><li id="u12a6c03d"><span id="u5153a6f2" style="color: rgb(26, 28, 31)">用</span><span id="ua0215c5e" style="color: rgb(26, 28, 31)">CommandQueue-&gt;Signal(fence, value)</span><span id="u8c92e0d8" style="color: rgb(26, 28, 31)">标记 GPU 进度。</span></li><li id="u55b0549d"><span id="u5664a270" style="color: rgb(26, 28, 31)">下一次复用同一帧资源前，CPU 检查 Fence 是否完成。</span></li></ul>

<a id="uf0096f66"></a><span style="color: rgb(26, 28, 31)">一句话版本：</span>

<a id="u7d76c2f3"></a><em><span style="color: rgb(26, 28, 31)">CPU 每帧重置并录制 Command List，把 Back Buffer 从 Present 状态切到 Render Target，完成清屏、绑定管线和 DrawCall 后再切回 Present，通过 Command Queue 提交给 GPU 执行，最后 Swap Chain Present 显示；Fence 用来确认 GPU 执行进度，避免 CPU 提前复用仍在被 GPU 使用的资源。</span></em>

<a id="u5e49a8dd"></a><strong><span style="color: rgb(26, 28, 31)">第 5 题：行为面试 / 问题解决</span></strong>

<a id="u1400a40e"></a><strong><span style="color: rgb(26, 28, 31)">你在做 PathTracer 或 DX12 Renderer 的时候，应该遇到过渲染结果不对、画面发黑、噪点异常、性能很慢这类问题。请选一个你印象最深的 bug 或性能问题，按“问题现象 - 排查过程 - 根因 - 解决方案 - 结果”的结构讲一下</span></strong>

<a id="u958ce76a"></a><span style="color: rgb(26, 28, 31)">可以这样答：</span>

1. <a id="ufd24bcf6"></a><strong><span style="color: rgb(26, 28, 31)">问题现象</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u6d445885"><span id="uc76fe5d8" style="color: rgb(26, 28, 31)">接入 HDRI / IBL 后，背景能显示 HDR 环境，但画面出现大量 firefly。</span></li><li id="u8d605bfc"><span id="u26087fe0" style="color: rgb(26, 28, 31)">同样 spp 下，环境高亮区域附近噪点明显比面积光场景严重。</span></li></ul>

2. <a id="ue675d4fa"></a><strong><span style="color: rgb(26, 28, 31)">排查过程</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u722b1b25"><span id="ue8756451" style="color: rgb(26, 28, 31)">先确认不是 gamma、颜色空间或贴图读取错误，因为背景显示方向和颜色基本正确。</span></li><li id="u4204b634"><span id="ub4f014ee" style="color: rgb(26, 28, 31)">再对比面积光采样和环境光采样，发现原来的 light sampling 更适合有限面积光源，不适合直接套到无限远环境光。</span></li><li id="u74b1d177"><span id="u06dbc759" style="color: rgb(26, 28, 31)">重点检查环境光采样的两个部分：采样分布和 PDF。</span></li></ul>

3. <a id="ubcc14510"></a><strong><span style="color: rgb(26, 28, 31)">根因</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u736ba566"><span id="u38673c8e" style="color: rgb(26, 28, 31)">HDRI 的亮度分布很不均匀，高能量集中在少数 texel。</span></li><li id="u8ba2bf8b"><span id="u9cfde36a" style="color: rgb(26, 28, 31)">如果只靠 BSDF 采样，或者环境光 PDF 计算不正确，就会导致偶发的高贡献样本，形成 firefly。</span></li><li id="u83b4bb74"><span id="uc85db228" style="color: rgb(26, 28, 31)">环境贴图还涉及经纬图到球面方向的转换，PDF 需要考虑</span><span id="ub7f5e00a" style="color: rgb(26, 28, 31)">sin(theta)</span><span id="u4eb556a4" style="color: rgb(26, 28, 31)">，不能只按纹理坐标面积处理。</span></li></ul>

4. <a id="ua5993192"></a><strong><span style="color: rgb(26, 28, 31)">解决方案</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u5ba49d66"><span id="u24b3c814" style="color: rgb(26, 28, 31)">在</span><span id="u3fd25226" style="color: rgb(26, 28, 31)">Environment</span><span id="u556b9b7e" style="color: rgb(26, 28, 31)">模块中为 HDRI 单独实现重要性采样。</span></li><li id="ufb7009c6"><span id="u927b4f66" style="color: rgb(26, 28, 31)">按</span><span id="ue73553b6" style="color: rgb(26, 28, 31)">luminance * sin(theta)</span><span id="ue0c9945b" style="color: rgb(26, 28, 31)">构建二维分布 / CDF。</span></li><li id="u4d263df9"><span id="u0db85e97" style="color: rgb(26, 28, 31)">增加环境光自己的 PDF 接口，并在直接光估计和 MIS 权重中使用正确的环境光 PDF。</span></li><li id="u02d3a54a"><span id="uc6a05d75" style="color: rgb(26, 28, 31)">用 AI 辅助检查公式推导和代码边界，但最终通过渲染结果和噪点变化验证。</span></li></ul>

5. <a id="u0ecac367"></a><strong><span style="color: rgb(26, 28, 31)">结果</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u825888e4"><span id="u2455ce16" style="color: rgb(26, 28, 31)">firefly 明显减少。</span></li><li id="u2c11c946"><span id="ude3c8ccd" style="color: rgb(26, 28, 31)">相同采样数下 HDRI 高亮区域的收敛更稳定。</span></li><li id="u581e3241"><span id="u25c55254" style="color: rgb(26, 28, 31)">也让后续 light sampling、environment sampling、BSDF sampling 能通过 MIS 放到统一框架里。</span></li></ul>

<a id="ub660605f"></a><span style="color: rgb(26, 28, 31)">这题你可以保留“AI 辅助验证”，但主表达要从“我问了 AI”改成“我定位到 PDF 和采样分布不匹配，然后用工具辅助校验”。</span>

<a id="u089e8392"></a><strong><span style="color: rgb(26, 28, 31)">第 6 题：专业问题 / HDRI 环境光采样</span></strong>

<a id="u1e5f2a80"></a><strong><span style="color: rgb(26, 28, 31)">你刚才提到了给 </span></strong><strong><span style="color: rgb(26, 28, 31)">Environment</span></strong><strong><span style="color: rgb(26, 28, 31)"> 增加自己的 PDF 接口。那我继续追问：如果使用经纬度 HDR 贴图做环境光采样，为什么构建采样分布时通常要乘上 </span></strong><strong><span style="color: rgb(26, 28, 31)">sin(theta)</span></strong><strong><span style="color: rgb(26, 28, 31)">？如果不乘，会造成什么问题？</span></strong>

1. <a id="ua2394577"></a><strong><span style="color: rgb(26, 28, 31)">经纬图不是等面积映射</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u0f847b02"><span id="u4ff38d85" style="color: rgb(26, 28, 31)">HDRI 经纬图中每个 texel 在 2D 贴图上面积一样。</span></li><li id="ued7cf800"><span id="ubde9d352" style="color: rgb(26, 28, 31)">但映射到球面后，不同纬度对应的立体角不同。</span></li><li id="ucb5b927e"><span id="u51500079" style="color: rgb(26, 28, 31)">球面面积微元是：</span><span id="uc765bbcd" style="color: rgb(26, 28, 31)">domega = sin(theta) dtheta dphi</span><span id="u53ae5412" style="color: rgb(26, 28, 31)">。</span></li></ul>

2. <a id="u3254b462"></a><strong><span style="color: rgb(26, 28, 31)">为什么乘</span></strong><strong><span style="color: rgb(26, 28, 31)">sin(theta)</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="ucb8674fe"><span id="u421198d2" style="color: rgb(26, 28, 31)">赤道附近</span><span id="ud71a96f1" style="color: rgb(26, 28, 31)">sin(theta)</span><span id="u5504f8fb" style="color: rgb(26, 28, 31)">接近 1，同样大小 texel 对应更大的球面面积。</span></li><li id="u8e23c3b5"><span id="u483098f9" style="color: rgb(26, 28, 31)">极点附近</span><span id="ude8687d2" style="color: rgb(26, 28, 31)">sin(theta)</span><span id="u90b1b884" style="color: rgb(26, 28, 31)">接近 0，同样大小 texel 对应更小的球面面积。</span></li><li id="u424402de"><span id="u09683700" style="color: rgb(26, 28, 31)">所以构建环境光重要性采样分布时，通常用</span><span id="u60c62077" style="color: rgb(26, 28, 31)">luminance(texel) * sin(theta)</span><span id="u1f6753cc" style="color: rgb(26, 28, 31)">，让采样概率同时反映亮度和球面面积。</span></li></ul>

3. <a id="u7f7c2afa"></a><strong><span style="color: rgb(26, 28, 31)">不乘的后果</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u57d556fb"><span id="u157aff9e" style="color: rgb(26, 28, 31)">会把极点附近的小立体角 texel 采得过多。</span></li><li id="ufe45f193"><span id="u6e690b50" style="color: rgb(26, 28, 31)">PDF 和真实积分测度不匹配，可能导致噪声变大、能量分布偏差，严重时环境光亮度估计不稳定。</span></li><li id="u062376ba"><span id="u35c92c81" style="color: rgb(26, 28, 31)">在 MIS 中还会影响权重计算，因为环境采样 PDF 不准确。</span></li></ul>

<a id="u6d649df0"></a><span style="color: rgb(26, 28, 31)">一句话版：</span>

<a id="u6b4b3c01"></a><em><span style="color: rgb(26, 28, 31)">因为经纬图到球面的映射不是等面积的，球面面积微元包含 </span></em><em><span style="color: rgb(26, 28, 31)">sin(theta)</span></em><em><span style="color: rgb(26, 28, 31)">。构建环境光采样分布时乘上它，是为了让 texel 的采样概率和它实际覆盖的立体角匹配，否则极区会被过度采样，PDF 也会和真实环境光积分不一致。</span></em>

<a id="ue5762035"></a><strong><span style="color: rgb(26, 28, 31)">第 7 题：简历深挖 / 性能优化</span></strong>

<a id="u8a3d46f5"></a><strong><span style="color: rgb(26, 28, 31)">你简历里写 PathTracer 通过 BVH、多线程 tile 渲染和 thread-local RNG，把渲染时间降低了 2.18 倍。请你具体讲一下这个优化是怎么做的？为什么 tile 并行可以避免数据竞争？有没有哪些部分仍然可能成为瓶颈？</span></strong>

1. <a id="udaed0621"></a><strong><span style="color: rgb(26, 28, 31)">原始问题</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="ub0c539fe"><span id="u527d3ca2" style="color: rgb(26, 28, 31)">最初是单线程扫描线渲染，每个像素按顺序计算。</span></li><li id="u15e416b4"><span id="u016a7be8" style="color: rgb(26, 28, 31)">路径追踪每个像素要发射多个 sample，每个 sample 又可能递归多次 bounce，CPU 多核利用率不足。</span></li></ul>

2. <a id="u387c145b"></a><strong><span style="color: rgb(26, 28, 31)">tile 并行</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u00b0b214"><span id="u58e71662" style="color: rgb(26, 28, 31)">我把图像划分成固定大小的 tile，例如每个 tile 包含一块连续像素区域。</span></li><li id="ua0b646e1"><span id="u6b485ff2" style="color: rgb(26, 28, 31)">多线程并行处理不同 tile。</span></li><li id="ue8393d3e"><span id="u2aad98aa" style="color: rgb(26, 28, 31)">每个 tile 只写自己负责的像素范围，最终 framebuffer 的索引由</span><span id="u9e974e0b" style="color: rgb(26, 28, 31)">(x, y)</span><span id="uebb4e0bc" style="color: rgb(26, 28, 31)">唯一确定，所以不同线程不会写同一个像素，避免数据竞争。</span></li><li id="u06e190a2"><span id="ub137a3cc" style="color: rgb(26, 28, 31)">相比“每个像素一个任务”，tile 粒度可以减少任务调度开销，也有更好的 cache locality。</span></li></ul>

3. <a id="u40d05839"></a><strong><span style="color: rgb(26, 28, 31)">thread-local RNG</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u076447ad"><span id="u2f1fcdc9" style="color: rgb(26, 28, 31)">路径追踪采样需要大量随机数。</span></li><li id="u18a3c700"><span id="ud9d310bf" style="color: rgb(26, 28, 31)">如果多个线程共享 RNG，会有锁竞争或数据竞争。</span></li><li id="udbe7c121"><span id="u1dd668c3" style="color: rgb(26, 28, 31)">所以我使用 thread-local RNG，让每个线程有自己的随机数状态，减少同步开销。</span></li></ul>

4. <a id="u730aae9e"></a><strong><span style="color: rgb(26, 28, 31)">BVH 优化</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u2fcca65c"><span id="ueedc4537" style="color: rgb(26, 28, 31)">未加 BVH 时，每条 ray 都要遍历大量三角形。</span></li><li id="u8d3eb4fb"><span id="ua3144dfc" style="color: rgb(26, 28, 31)">BVH 用层次包围盒先剔除不可能命中的区域。</span></li><li id="u2c3a56b7"><span id="u3e4221c0" style="color: rgb(26, 28, 31)">ray 先和 AABB 求交，只有命中包围盒才继续访问子节点或叶子三角形，从而显著减少三角形求交次数。</span></li></ul>

5. <a id="u4669b64d"></a><strong><span style="color: rgb(26, 28, 31)">量化结果</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="uceb67c4f"><span id="uec9b6aaa" style="color: rgb(26, 28, 31)">在 800x450 / 400 spp / 20 depth 的基准下，串行渲染约 65.33s，并行后约 29.99s，整体提速约 2.18x。</span></li></ul>

6. <a id="ucbf19e64"></a><strong><span style="color: rgb(26, 28, 31)">剩余瓶颈</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u3635e2bb"><span id="ufa8db8a7" style="color: rgb(26, 28, 31)">高 spp 仍然是主要成本。</span></li><li id="u10d25045"><span id="u7a65c133" style="color: rgb(26, 28, 31)">复杂场景下 BVH traversal、材质 BSDF 计算、环境光采样和内存访问仍然占比较高。</span></li><li id="u81c3abd3"><span id="u2fe6b399" style="color: rgb(26, 28, 31)">不同 tile 的复杂度不同，也可能造成线程负载不均衡。</span></li></ul>

<a id="u92b003b2"></a><span style="color: rgb(26, 28, 31)">一句话总结可以这样说：</span>

> <a id="u1358eac1"></a>
>
> <a id="u1ab29e20"></a><em><span style="color: rgb(26, 28, 31)">tile 并行的关键不是让线程随便抢像素，而是把 framebuffer 划分成互不重叠的写入区域；再配合 thread-local RNG 避免随机数状态竞争，BVH 则减少每条 ray 的求交成本。</span></em>

<a id="ua4871273"></a><strong><span style="color: rgb(26, 28, 31)">第 8 题：专业问题 / DirectX 12 IBL</span></strong>

<a id="uead8a690"></a><strong><span style="color: rgb(26, 28, 31)">你在 DX12 Renderer 里写了 split-sum IBL，并预计算了 irradiance map、prefiltered environment map 和 BRDF LUT。请你解释一下这三个贴图分别解决什么问题？运行时渲染一个 PBR 物体时，它们是怎么被用到的？</span></strong>

1. <a id="u7f6082cb"></a><strong><span style="color: rgb(26, 28, 31)">为什么需要 split-sum IBL</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u7b71f1ae"><span id="u46ba0f74" style="color: rgb(26, 28, 31)">离线路径追踪可以对环境光做大量采样。</span></li><li id="u9a7b181d"><span id="uda7e9194" style="color: rgb(26, 28, 31)">实时渲染不能每个像素每帧采很多条环境光方向。</span></li><li id="u55b31436"><span id="ub5a564d5" style="color: rgb(26, 28, 31)">所以把环境光积分拆成可以预计算的部分和运行时快速查表的部分。</span></li></ul>

2. <a id="ua2d0fba2"></a><strong><span style="color: rgb(26, 28, 31)">irradiance map</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u49f01bec"><span id="ud5a094ec" style="color: rgb(26, 28, 31)">解决 diffuse IBL。</span></li><li id="uf1e6ecce"><span id="ubaffc9d9" style="color: rgb(26, 28, 31)">它对环境贴图按每个法线方向做半球卷积。</span></li><li id="ub99357b1"><span id="uf010848a" style="color: rgb(26, 28, 31)">运行时用法线</span><span id="udced9700" style="color: rgb(26, 28, 31)">N</span><span id="u713f6e26" style="color: rgb(26, 28, 31)">采样 irradiance map，再乘以 diffuse albedo，近似漫反射环境光。</span></li></ul>

3. <a id="ucbc989f1"></a><strong><span style="color: rgb(26, 28, 31)">prefiltered environment map</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u93faf5f2"><span id="ua81c4194" style="color: rgb(26, 28, 31)">解决 specular IBL 中环境反射采样成本高的问题。</span></li><li id="u919b97c9"><span id="uff7cd487" style="color: rgb(26, 28, 31)">按不同 roughness 对 HDR 环境贴图做 GGX 重要性采样预滤波，并存到不同 mip level。</span></li><li id="u7405dc22"><span id="u252ca370" style="color: rgb(26, 28, 31)">运行时用反射方向</span><span id="u241d5c84" style="color: rgb(26, 28, 31)">R</span><span id="u1aa984cd" style="color: rgb(26, 28, 31)">采样，并根据 roughness 选择 mip，roughness 越大结果越模糊。</span></li></ul>

4. <a id="u8bd9fa83"></a><strong><span style="color: rgb(26, 28, 31)">BRDF LUT</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u8ac49f98"><span id="u27c205d6" style="color: rgb(26, 28, 31)">解决 specular BRDF 积分中和视角、粗糙度相关的部分。</span></li><li id="u38d62427"><span id="u5e9d77e7" style="color: rgb(26, 28, 31)">输入是</span><span id="u18365c8e" style="color: rgb(26, 28, 31)">NdotV</span><span id="u23f2f8ae" style="color: rgb(26, 28, 31)">和</span><span id="uc7678ade" style="color: rgb(26, 28, 31)">roughness</span><span id="u4fc88cae" style="color: rgb(26, 28, 31)">。</span></li><li id="u25b1f492"><span id="u8113f062" style="color: rgb(26, 28, 31)">输出通常是 scale / bias 两个值，用来和</span><span id="u2579ac9d" style="color: rgb(26, 28, 31)">F0</span><span id="u71bbaa7d" style="color: rgb(26, 28, 31)">组合。</span></li></ul>

5. <a id="u8539764b"></a><strong><span style="color: rgb(26, 28, 31)">运行时组合</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u6001afb4"><span id="ue7a9b0d4" style="color: rgb(26, 28, 31)">diffuse：</span><span id="u08ac6580" style="color: rgb(26, 28, 31)">irradiance(N) * albedo</span></li><li id="ua8dee090"><span id="u5a3ead27" style="color: rgb(26, 28, 31)">specular：</span><span id="u03c0f848" style="color: rgb(26, 28, 31)">prefilteredEnv(R, roughness) * (F0 * brdf.x + brdf.y)</span></li><li id="ud3805fe5"><span id="u21eae314" style="color: rgb(26, 28, 31)">最后再加上直接光、阴影、tone mapping 等。</span></li></ul>

<a id="u58ef8212"></a><span style="color: rgb(26, 28, 31)">一句话总结：</span>

<a id="u23d20933"></a><em><span style="color: rgb(26, 28, 31)">irradiance map 负责漫反射环境光，prefiltered environment map 负责不同粗糙度下的环境反射，BRDF LUT 负责视角和粗糙度相关的 BRDF 积分项；三者合起来让 PBR 材质在实时渲染中用少量纹理采样近似 IBL 积分。</span></em>

<a id="u975f5d61"></a><span style="color: rgb(26, 28, 31)">这题你的方向是对的，补上 </span><span style="color: rgb(26, 28, 31)">N</span><span style="color: rgb(26, 28, 31)">、</span><span style="color: rgb(26, 28, 31)">R</span><span style="color: rgb(26, 28, 31)">、</span><span style="color: rgb(26, 28, 31)">roughness mip</span><span style="color: rgb(26, 28, 31)">、</span><span style="color: rgb(26, 28, 31)">NdotV</span><span style="color: rgb(26, 28, 31)">、</span><span style="color: rgb(26, 28, 31)">F0</span><span style="color: rgb(26, 28, 31)"> 这些关键词，会更像真正写过 shader。</span>

<a id="ua270bf20"></a><strong><span style="color: rgb(26, 28, 31)">第 9 题：行为面试 / AI 工具使用</span></strong>

<a id="uc898c7bb"></a><strong><span style="color: rgb(26, 28, 31)">JD 里提到熟练使用 CodeBuddy、Codex、Claude Code 等 AI 工具，并且你简历里也写了使用 AI 工具辅助开发。请你讲一个具体例子：你在项目里是怎么使用 AI 工具提升开发效率的？你如何判断 AI 给出的方案是正确的，而不是直接照抄？</span></strong>

1. <a id="u45a1eff2"></a><strong><span style="color: rgb(26, 28, 31)">场景</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u98032315"><span id="u33c5c286" style="color: rgb(26, 28, 31)">在 PathTracer 中集成 PBR 流程时，我一开始掌握了 Cook-Torrance、GGX、Fresnel 等公式，但不确定怎么接入现有渲染器架构。</span></li></ul>

2. <a id="u96f0695b"></a><strong><span style="color: rgb(26, 28, 31)">AI 的作用</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="u9ba94e17"><span id="u26345449" style="color: rgb(26, 28, 31)">我先用 AI 帮我拆分实现路径，比如材质接口、BSDF eval、PDF、采样、贴图解析、测试场景。</span></li><li id="u6ef81d58"><span id="uf81d58fa" style="color: rgb(26, 28, 31)">然后让 AI 结合源码指出现有架构适合在哪些模块接入，而不是直接生成一整套代码。</span></li></ul>

3. <a id="u668bd44d"></a><strong><span style="color: rgb(26, 28, 31)">自己的判断</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="uac509b4e"><span id="u10a2fb50" style="color: rgb(26, 28, 31)">我会先复习公式和参考开源实现，确认 AI 方案是否符合渲染方程和现有代码结构。</span></li><li id="uce81ea8b"><span id="u5dcd606c" style="color: rgb(26, 28, 31)">对关键部分，比如 GGX VNDF、normal map、IBL、MIS，我会重点检查 PDF、坐标空间和能量项是否一致。</span></li></ul>

4. <a id="u157469cb"></a><strong><span style="color: rgb(26, 28, 31)">验证方式</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="ub76f19b6"><span id="u7bb75a2d" style="color: rgb(26, 28, 31)">每完成一个小模块，就用固定测试场景验证，例如不同 roughness、metallic、normal map、HDRI 光照。</span></li><li id="ub315664f"><span id="u390cf974" style="color: rgb(26, 28, 31)">再让 AI 做 code review，检查边界条件、变量含义和潜在 bug。</span></li><li id="u4e0378ab"><span id="u1d17d146" style="color: rgb(26, 28, 31)">最后通过渲染结果和性能数据确认效果，比如多线程优化后的 2.18x 提速。</span></li></ul>

5. <a id="u9899b8a3"></a><strong><span style="color: rgb(26, 28, 31)">总结</span></strong>

<ul data-yuque-indent="1" style="margin-left: 2em"><li id="ub474a2d9"><span id="u9a07e0e0" style="color: rgb(26, 28, 31)">AI 主要提升了方案拆解、资料对比和代码审查效率，但最终是否采用，还是由我基于公式、源码结构、测试图和 benchmark 判断。</span></li></ul>

<a id="uf27e1de3"></a><span style="color: rgb(26, 28, 31)">一句话版本：</span>

<a id="u22e2fc32"></a><em><span style="color: rgb(26, 28, 31)">我不会直接照抄 AI 代码，而是把 AI 当作方案拆解和 review 工具；关键图形逻辑会用公式推导、源码结构、固定测试场景和渲染结果来交叉验证。</span></em>

原文：[项目细节](<https://www.yuque.com/u62694975/iaaa/erbuu8ky9dn39bpn>)
