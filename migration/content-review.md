# 内容技术复核清单

迁移保留作者的解释与代码；本清单记录可能的知识性问题、题号冲突和环境限制，供后续单独复核，不作为批量改写正文的依据。证据来自源 ASL、既有网站正文及逐节迁移审查；短摘仅用于定位。未编译或执行这些算法/着色器示例。私密占位号 P1–P6 的正文、标题、日期及身份信息不进入本报告。

| Article | Section | Original claim | Potential issue | Reason |
| --- | --- | --- | --- | --- |
| 目录 #37：DX12 杂谈 | Command Queue 的三种类型 / Copy Queue | “优先级最高、开销最小” | 将队列类型与创建优先级混为一谈；性能也不宜绝对化。 | [Microsoft 的 D3D12_COMMAND_QUEUE_DESC](https://learn.microsoft.com/en-us/windows/win32/api/d3d12/ns-d3d12-d3d12_command_queue_desc) 将 Type 与 Priority 分开，Priority 用于选择 normal 或 high；仅凭 Copy 类型不能推断总是最高优先级。原段保留并标注待复核。 |
| 目录 #37：DX12 杂谈 | 一帧绘制 / 第二次资源状态切换 | “从 PRESENT 切回 RENDER_TARGET” | 绘制结束、提交显示之前的切换方向与流程不符。 | 源前段已从 PRESENT 转为 RENDER_TARGET；网站成熟稿已整理为绘制结束后转回 PRESENT。保留成熟稿，未用源反向表述覆盖。 |
| 目录 #46：如何混合法线贴图 | Overlay Blending / 着色器代码 | `1 – 2` | U+2013 en dash 不是通常的减号 token，可能导致着色器编译失败。 | 该字符存在于原 ASL code payload，独立转换核对一致；不是迁移时产生的转义损坏。原代码保留，需后续编译核验。 |
| Games104：引擎架构分层 | 核心层 | “C++的STL就不能使用” | “所有标准容器都会产生内存空洞，游戏引擎因此不能使用”的推论过于绝对。 | 容器、分配器、访问模式和引擎策略需要分别讨论。[C++ 标准草案 vector 概述](https://eel.is/c++draft/vector.overview) 明确非 bool vector 是连续容器并支持分配器；这不能推出所有 STL 一律不可用。是否自定义应另据具体约束与测量复核。 |
| 目录 #78：大气与云的渲染 | 正文“地形的几何 / Heightfield / 细分方式” | 标题写“大气与云”，正文实际讨论地形高度图与网格细分。 | 标题与现有内容不一致，可能是未完成或误命名的笔记。 | 源 ASL 只有地形与细分相关小节；迁移保留原题与正文，不补写大气或云渲染内容。 |
| 目录 #90：LeetCode 子串困难题组 | 最小覆盖子串 | “第七十八题” | 源题号与题目链接冲突。 | [LeetCode 官方题目](https://leetcode.cn/problems/minimum-window-substring/description/) 标识为 76。文章正文原标题保持，目录 metadata 按题目链接识别 76，并记录源 78 的冲突。未采用网友解法纠错。 |
| 目录 #85：LeetCode 堆简单题组 | 库存管理 III | “第一百五十九题” | 缺少 LCR 命名空间，会与普通 159 题混淆。 | [LeetCode 官方题目入口](https://leetcode.cn/problems/zui-xiao-de-kge-shu-lcof/) 对应 LCR 159 库存管理 III。源标题和代码保持，目录 metadata 使用 LCR 159；复核对象是官方题号/标题，不是社区题解算法。 |
| 既有 LeetCode 链表 Easy（目录 #102） | 环形链表 | 标题与 problems 含 `114` | 潜在错号：题目名/链接对应 141，而 114 是二叉树展开为链表。 | 参见官方 [141 环形链表](https://leetcode.cn/problems/linked-list-cycle/) 与 [114 二叉树展开为链表](https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/)。既有 114 数字、标题和代码均未自动修改。 |
| 目录 #113：LeetCode 二叉树 Medium | 第 114 题 / 展开思路 | “越是靠右的节点，在链表中的位置越靠前” | 左右顺序描述与本段代码及先序要求不一致。 | 源代码将左子树移到 root.right，并把原右子树接在其后；[官方第 114 题](https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/) 要求先序顺序、左指针为 null。保留原解释、代码及题号，单独复核措辞。 |
| 目录 #113：LeetCode 二叉树 Medium | 第 98 题 / 递归上下界变体 | `long`、`LONG_MIN`、`LONG_MAX` 作为排他边界 | 依赖 long 的位宽；某些平台会误拒 int 的极值节点。 | [Microsoft 整数范围](https://learn.microsoft.com/en-us/cpp/c-language/cpp-integer-limits?view=msvc-170) 中 LONG_MIN/MAX 与 INT_MIN/MAX 相同；结合源 `<=` 比较，这是平台边界风险。代码未改，后续需明确平台与极值用例。 |
| 目录 #113：LeetCode 二叉树 Medium | 第 437 题 / 前缀和变体 | `this auto&&` 递归 lambda | 需要支持显式对象参数的 C++23 编译环境，不能默认所有早期 C++ 标准均可编译。 | [WG21 P0847R7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p0847r7.html) 与 [标准草案 lambda 规则](https://eel.is/c++draft/expr.prim.lambda.closure) 说明该语法机制。保留源写法；复核编译器、标准开关与头文件，不降级改写。 |
| 目录 #128：LeetCode 滑动窗口 Medium | 第 1493 题 / 更新最大窗口长度 | `std::max(right - left + 1 - 1,)` | 第二个参数缺失，原代码不能据此视为可编译示例。 | 原 ASL 与转换后的 code payload 一致，属于源代码不完整；新增段标为原笔记/代码待复核，没有推测或补入参数。 |
| 目录 #70：GAMES101 作业 5 | rayTriangleIntersect / 重心坐标范围 | 正文要求将 `u + v > 1` 判为三角形外。 | 原代码只分别检查 u、v 是否在 0 到 1 内，缺少联合范围检查，与解释不一致。 | 已逐字符核对原 ASL code 卡片：两个独立范围判断后直接计算 tnear，未检查 u + v。两者各自合法仍可能和大于 1，因此存在接受三角形外交点的风险；迁移保留原代码，需后续用边界射线单独验证。 |

不同算法实现的同题可保留；同一完整代码块只因缩进不同，不应再次复制整段。已确认第 5 题两个源题组的实现不同，第 26 题双指针/链表题组的代码仅缩进不同。迁移流程应在核验实际页面 URL 与题锚点后，用站内链接指向保留的完整代码；原始 Lakebook 与临时转换正文仍完整保留于仓库外。
