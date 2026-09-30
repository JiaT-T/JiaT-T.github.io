# 语雀技术笔记迁移报告

本报告记录 `content/yuque-migration` 分支合入最新并行 main 后的本地静态验收快照，整合提交为 `f0d973a`。原始网站基线为 `f1566a2b6270fdf2ebaca7c459235fdebe8b3e00`；并行 main 的作品集、首页与导航等工作已保留。执行结果覆盖全部 135 个目录条目，逐项映射见本报告末表及 [yuque-manifest.json](yuque-manifest.json)。原始 Lakebook、完整转换草稿与私密源材料保留在仓库外，没有作为公开交付内容提交。

## 迁移结果

| 最终处理 | 条目数 |
| --- | ---: |
| 新建文章 | 37 |
| 填充既有空文章 | 1 |
| 补全既有文章 | 18 |
| 仅格式修复 | 2 |
| 保留既有成熟稿 | 29 |
| 映射既有章节 | 17 |
| 空条目不生成文章 | 23 |
| 草稿占位不发布 | 2 |
| 私密排除 | 6 |
| 合计 | 135 |

37 篇新文章与 11 个新目录索引带来 48 个新增 Markdown 文件；填空、补全和格式修复作用于既有文件。原基线 110 个 Markdown，加上并行 main 的 1 个作品集页面与迁移新增 48 个，最终为 159 个。空条目、草稿占位和私密排除项均在全表登记，不把它们计为新增正文。

既有成熟稿保留手工整理，只追加审核确认的缺失章节/真实算法变体或修复格式。旧文章 URL、已有完整代码与图片未被批量替换。同题重复代码通过核验的站内题锚点连接，不重复生成同一完整代码；不同实现继续保留。父文档有正文的 LeetCode 与回溯笔记作为 overview 文章保留，章节索引用于组织文章。

## 资源与内容保留

68 个源图片引用全部有覆盖：35 个位于新建/填空文章并本地化，6 个保留既有显示裁剪图，21 个与既有图片字节匹配，另 6 个既有远程引用完成本地化。因此网站新增图片文件为 41 个，而不是新增 68 个。两处源引用共享一个文件 hash 但显示裁剪不同，按引用分别核对。

旧的 40 个图片文件经 SHA-256 字节核对均不变；既有 1 个 MP4 的字节也不变。现有视频在本地浏览器能加载元数据、readyState 为 4、未报告播放资源错误。这不等价于所有外链或所有图片隐私已通过完整人工检查。

## 构建与验证

| 项目 | 合入并行 main 后结果 | 证据范围 |
| --- | ---: | --- |
| Hugo 构建 | 439 pages，82 static files | Hugo 0.167.0 extended 本地成功构建；pages 包含站点生成页，不能等同文章数 |
| 实际 HTML | 423 | 静态输出文件扫描 |
| kind=page | 100 | 97 个笔记档案条目、1 个 portfolio，以及 archives/search 两个功能页 |
| 六组归档 | 97 | LeetCode 35、C++ 9、图形学 27、DirectX 12 5、Vulkan 13、Unreal Engine 8 |
| 搜索索引 | 98 | 97 个笔记条目加 portfolio；38 篇新建/填空文章的实际 permalink 均出现一次 |
| 38 篇新建/填空文章 | 353 段代码、260 个标题、35 张图片 | 在已构建正文内按顺序、层级、代码字符和本地图片身份核对，全部通过；不是全站数量 |
| 本地链接/锚点 | 缺失目标 0 / 缺失锚点 0 | 已构建 HTML/CSS 静态引用范围；不表示 824 个外部引用全部可访问 |
| 数学 | 源 95 个 math 卡片；网站 9 个 math 页面静态检查无问题 | 95 是源转换卡片数，9 是文章页数；两者不能相减判断公式丢失。源 LaTeX/hash 保留，成熟稿与未发布私密稿分开处理 |

全 135 个源文档的临时转换另核对 489 段代码、631 个标题、95 个公式卡片和 68 个图片卡片，转换完整性通过。这证明转换范围内的保留，不能据此声称 135 篇全部发布或所有代码技术正确。实际 Hugo 新建/填空正文检查覆盖 38 篇；既有补全与保留另经 diff 审查。浏览器有 23 条检查记录，覆盖代表文章、MathJax、代码高亮、目录、图片、视频、首页、归档、分类和搜索；不把抽样检查扩张成所有页面视觉与运行时验收。

保留 5 个既有 favicon/站点图标缺失，以及 [content-review.md](content-review.md) 的 13 项技术待复核内容。迁移未为纠正原笔记而改写算法或着色器代码，不能宣称“全站零问题”。剩余问题与证据边界见 [failed-items.md](failed-items.md)；机器可读摘要见 [validation-summary.json](validation-summary.json)。

## 远端交付状态

内容分支已推送，[PR #7](https://github.com/JiaT-T/JiaT-T.github.io/pull/7) 已创建。用户已授权直接合并，根流程将提交最后的报告并完成合并；实际合并结果在本地交付报告中记录。线上验证按用户最新指示跳过，因此本报告不声称线上部署已核验，本地构建成功也不作为线上已更新的证明。

## 135 条目录处理全表

P1–P6 只表示被排除的私密记录，不公开其原标题、日期、正文、来源链接或身份信息。其余“生成路径”来自最终 Hugo 输出或已确认的网站映射；空条目和草稿不生成页面。

| 目录项 | 公开标题 / 占位 | 最终处理 | 网站生成路径 / 文件映射 |
| --- | --- | --- | --- |
| P1 | 私密占位 P1 | 私密排除 | — |
| P2 | 私密占位 P2 | 私密排除 | — |
| P3 | 私密占位 P3 | 私密排除 | — |
| P4 | 私密占位 P4 | 私密排除 | — |
| P5 | 私密占位 P5 | 私密排除 | — |
| P6 | 私密占位 P6 | 私密排除 | — |
| 6 | UE5 | 映射既有章节 | /ue/ |
| 7 | GAS | 新建文章 | /ue/gameplay-ability-system/ |
| 8 | 计网 / OS | 新建文章 | /cpp/network-and-os-notes/ |
| 9 | 可能的UE底层知识 | 新建文章 | /ue/ue-low-level-notes/ |
| 10 | UObject | 草稿占位不发布 | — |
| 11 | 序列化 | 新建文章 | /ue/ue-serialization/ |
| 12 | 反射系统 | 保留既有成熟稿 | /ue/reflection-system/ |
| 13 | GC（垃圾回收） | 空条目不生成文章 | — |
| 14 | GamePlay 架构（一） | 保留既有成熟稿 | /ue/gameplay-framework1/ |
| 15 | UE5材质备忘录 | 新建文章 | /ue/ue5-material-reference/ |
| 16 | UE 渲染管线（桌面端延迟渲染） | 新建文章 | /ue/ue-deferred-rendering-pipeline/ |
| 17 | 一个简单的 C++ 管理引擎资产练习 | 保留既有成熟稿 | /ue/cpp-in-ue5/ |
| 18 | Vulkan | 映射既有章节 | /vulkan/ |
| 19 | EasyVulkan 第六章学习笔记 | 新建文章 | /vulkan/easyvulkan-chapter-6/ |
| 20 | EasyVulkan 第七章学习笔记 | 新建文章 | /vulkan/easyvulkan-chapter-7/ |
| 21 | 基础知识 | 空条目不生成文章 | — |
| 22 | Fence | 空条目不生成文章 | — |
| 23 | 命令缓冲区与命令池 | 空条目不生成文章 | — |
| 24 | 队列族 | 保留既有成熟稿 | /vulkan/%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86/queuefamily/ |
| 25 | GLFW | 新建文章 | /vulkan/vulkan-glfw/ |
| 26 | 同步原语 | 新建文章 | /vulkan/vulkan-synchronization-primitives/ |
| 27 | VkResult | 新建文章 | /vulkan/vulkan-vkresult/ |
| 28 | 队列类型 | 保留既有成熟稿 | /vulkan/%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86/queue-categories/ |
| 29 | 初始化流程 | 保留既有成熟稿 | /vulkan/%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86/initialization/ |
| 30 | Window Surface | 新建文章 | /vulkan/vulkan-window-surface/ |
| 31 | 交换链（Swapchain） | 保留既有成熟稿 | /vulkan/%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86/swapchain/ |
| 32 | Layers(层) 与 Extensions(扩展) | 保留既有成熟稿 | /vulkan/%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86/layers-and-extensions/ |
| 33 | 验证层(⭐⭐⭐) | 保留既有成熟稿 | /vulkan/%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86/validationlayers/ |
| 34 | 物理设备(VkPhysicalDevice)与逻辑设备(VkDevice) | 保留既有成熟稿 | /vulkan/%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86/physical-and-logic-device/ |
| 35 | DX12 | 新建文章 | /posts/directx12-hresult/ |
| 36 | DXR | 新建文章 | /posts/directx-raytracing-notes/ |
| 37 | DX12 杂谈 | 补全既有文章 | /posts/dx12/ |
| 38 | DXR/DX12的类型/结构体/函数 | 空条目不生成文章 | — |
| 39 | 类型 | 新建文章 | /posts/dxr-dx12-types/ |
| 40 | 函数 | 新建文章 | /posts/dxr-dx12-functions/ |
| 41 | CG | 映射既有章节 | /graphics/ |
| 42 | CG面经 | 空条目不生成文章 | — |
| 43 | C 与 C++ | 空条目不生成文章 | — |
| 44 | GI（全局光照） | 空条目不生成文章 | — |
| 45 | C++ 设计模式 | 保留既有成熟稿 | /posts/design-modes/ |
| 46 | 如何混合法线贴图 | 仅格式修复 | /posts/others/normal-combination/ |
| 47 | 纹理贴图的压缩算法 | 空条目不生成文章 | — |
| 48 | 移动/桌面端渲染架构 | 草稿占位不发布 | — |
| 49 | 加速结构 | 保留既有成熟稿 | /posts/acceleration-structure/ |
| 50 | 排序算法 | 新建文章 | /cpp/sorting-algorithms/ |
| 51 | 渲染路径 | 保留既有成熟稿 | /graphics/rendering-paths/ |
| 52 | 阴影技术 | 保留既有成熟稿 | /posts/shadow-techniques/ |
| 53 | 项目细节 | 新建文章 | /graphics/pathtracer-project-details/ |
| 54 | 抗锯齿技术 | 保留既有成熟稿 | /posts/anti-aliasing/ |
| 55 | 辐射度量学 | 补全既有文章 | /graphics/%E8%BE%90%E5%B0%84%E5%BA%A6%E9%87%8F%E5%AD%A6/ |
| 56 | Shadow Map | 保留既有成熟稿 | /posts/shadow-maps/ |
| 57 | Split-Sum IBL | 保留既有成熟稿 | /graphics/split-sum-ibl/ |
| 58 | Pathtracer 梳理 | 新建文章 | /graphics/pathtracer-code-notes/ |
| 59 | PBR 的 MR / SG 模型 | 保留既有成熟稿 | /graphics/pbr-models/ |
| 60 | Fundamentals of Cpp | 保留既有成熟稿 | /posts/cpp-fundamentals/cpp-fundamentals/ |
| 61 | C++ 源码到 exe 的过程 | 保留既有成熟稿 | /cpp/cpp-to-exe/ |
| 62 | 只能在堆/栈上创建对象的类 | 保留既有成熟稿 | /posts/others/how-to-create-a-heaponly-or-stackonly-class/ |
| 63 | Data Race  与 Race Condition | 保留既有成熟稿 | /cpp/data-race-and-race-condition/ |
| 64 | Whitted-style 光线追踪与 Monte Carlo 路径追踪的主要区别 | 保留既有成熟稿 | /posts/others/witted-and-mote-carlo/ |
| 65 | Games101 | 空条目不生成文章 | — |
| 66 | 作业 | 空条目不生成文章 | — |
| 67 | 2 | 新建文章 | /graphics/games101-assignment-2/ |
| 68 | 3 | 空条目不生成文章 | — |
| 69 | 4 | 新建文章 | /graphics/games101-assignment-4/ |
| 70 | 5 | 新建文章 | /graphics/games101-assignment-5/ |
| 71 | 6 | 空条目不生成文章 | — |
| 72 | Games104 | 空条目不生成文章 | — |
| 73 | Notes | 空条目不生成文章 | — |
| 74 | 光照与材质 | 空条目不生成文章 | — |
| 75 | 引擎架构分层 | 新建文章 | /graphics/games104-engine-architecture/ |
| 76 | 如何构建游戏世界 | 新建文章 | /graphics/games104-game-world/ |
| 77 | 渲染实践 | 新建文章 | /graphics/games104-rendering-practice/ |
| 78 | 大气与云的渲染 | 新建文章 | /graphics/games104-atmosphere-and-clouds/ |
| 79 | LeetCode | 新建文章 | /leetcode/leetcode-overview/ |
| 80 | 栈 | 映射既有章节 | /leetcode/stack/ |
| 81 | easy | 补全既有文章 | /leetcode/stack/easy/leetcode-stack-easy/ |
| 82 | medium | 补全既有文章 | /leetcode/stack/medium/leetcode-stack-medium/ |
| 83 | hard | 新建文章 | /leetcode/stack/hard/leetcode-stack-hard/ |
| 84 | 堆 | 映射既有章节 | /leetcode/heap/ |
| 85 | easy | 新建文章 | /leetcode/heap/easy/leetcode-heap-easy/ |
| 86 | Medium | 保留既有成熟稿 | /leetcode/heap/medium/leetcode-heap-medium/ |
| 87 | Hard | 空条目不生成文章 | — |
| 88 | 子串 | 空条目不生成文章 | — |
| 89 | medium | 新建文章 | /leetcode/substring/medium/leetcode-substring-medium/ |
| 90 | hard | 新建文章 | /leetcode/substring/hard/leetcode-substring-hard/ |
| 91 | 回溯 | 新建文章 | /leetcode/back-track/backtracking-overview/ |
| 92 | medium | 补全既有文章 | /leetcode/back-track/medium/leetcode-back-track-medium/ |
| 93 | 矩阵 | 映射既有章节 | /leetcode/matrix/ |
| 94 | easy | 空条目不生成文章 | — |
| 95 | medium | 仅格式修复 | /leetcode/matrix/medium/leetcode-matrix-medium/ |
| 96 | 哈希 | 映射既有章节 | /leetcode/hash/ |
| 97 | easy | 补全既有文章 | /leetcode/hash/easy/leetcode-hash-medium/ |
| 98 | medium | 补全既有文章 | /leetcode/hash/medium/leetcode-hash-medium/ |
| 99 | 图论 | 映射既有章节 | /leetcode/graph/ |
| 100 | medium | 新建文章 | /leetcode/graph/medium/leetcode-graph-medium/ |
| 101 | 链表 | 映射既有章节 | /leetcode/list/ |
| 102 | easy | 保留既有成熟稿 | /leetcode/list/easy/leetcode-list-easy/ |
| 103 | medium | 补全既有文章 | /leetcode/list/medium/leetcode-list-medium/ |
| 104 | hard | 补全既有文章 | /leetcode/list/hard/leetcode-list-hard/ |
| 105 | 技巧 | 映射既有章节 | /leetcode/technique/ |
| 106 | easy | 保留既有成熟稿 | /leetcode/technique/easy/leetcode-technique-easy/ |
| 107 | medium | 保留既有成熟稿 | /leetcode/technique/medium/leetcode-technique-medium/ |
| 108 | 双指针 | 映射既有章节 | /leetcode/double-pointers/ |
| 109 | easy | 填充既有空文章 | /leetcode/double-pointers/easy/leetcode-double-pointers-easy/ |
| 110 | medium | 补全既有文章 | /leetcode/double-pointers/medium/leetcode-double-pointers-medium/ |
| 111 | 二叉树 | 映射既有章节 | /leetcode/binary-tree/ |
| 112 | easy | 补全既有文章 | /leetcode/binary-tree/easy/leetcode-binary-tree-easy/ |
| 113 | medium | 补全既有文章 | /leetcode/binary-tree/medium/leetcode-binary-tree-medium/ |
| 114 | hard | 新建文章 | /leetcode/binary-tree/hard/leetcode-binary-tree-hard/ |
| 115 | 字符串 | 空条目不生成文章 | — |
| 116 | easy | 新建文章 | /leetcode/string/easy/leetcode-string-easy/ |
| 117 | 普通数组 | 空条目不生成文章 | — |
| 118 | easy | 空条目不生成文章 | — |
| 119 | medium | 新建文章 | /leetcode/array/medium/leetcode-array-medium/ |
| 120 | 二分查找 | 映射既有章节 | /leetcode/binary-search/ |
| 121 | easy | 保留既有成熟稿 | /leetcode/binary-search/easy/leetcode-binary-search-easy/ |
| 122 | medium | 补全既有文章 | /leetcode/binary-search/medium/leetcode-binary-search-medium/ |
| 123 | hard | 空条目不生成文章 | — |
| 124 | 贪心算法 | 映射既有章节 | /leetcode/greedy-algorithm/ |
| 125 | easy | 补全既有文章 | /leetcode/greedy-algorithm/easy/leetcode-greedy-algorithm-easy/ |
| 126 | medium | 补全既有文章 | /leetcode/greedy-algorithm/medium/leetcode-greedy-algorithmmedium/ |
| 127 | 滑动窗口 | 映射既有章节 | /leetcode/sliding-window/ |
| 128 | medium | 补全既有文章 | /leetcode/sliding-window/medium/leetcode-sliding-window-medium/ |
| 129 | hard | 新建文章 | /leetcode/sliding-window/hard/leetcode-sliding-window-hard/ |
| 130 | 动态规划 | 映射既有章节 | /leetcode/dynamic-programming/ |
| 131 | easy | 保留既有成熟稿 | /leetcode/dynamic-programming/easy/leetcode-dynamic-programming-easy/ |
| 132 | medium | 补全既有文章 | /leetcode/dynamic-programming/medium/leetcode-dynamic-programming-easy/ |
| 133 | 多维动态规划 | 映射既有章节 | /leetcode/multidimensional-dynamic-programming/ |
| 134 | medium | 补全既有文章 | /leetcode/multidimensional-dynamic-programming/medium/leetcode-multidimensional-dynamic-programming-medium/ |
