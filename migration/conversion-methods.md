# Lakebook 转换方法与验证

输入来自语雀正常页面 UI 导出的 Lakebook。转换器仅用 tarfile 逐个读取 JSON，不 extractall，不下载图片，不登录或调用隐藏接口，不写网站 content，不润色或自动修改技术内容。原始备份与完整转换草稿保存在仓库外，不提交。

## 使用

安装和 CLI 用法见 [scripts/README.md](../scripts/README.md)。`convert_doc(doc, source_base=...)` 返回 `body_markdown`、`markdown`、`quality`。body_markdown 是正文；markdown 含源标题、原始日期、来源 ID/slug、math 标志和语雀来源链接。输出的逐篇质量报告包含源正文 hash、代码/公式 payload hash、anchor、图片 URL、格式规范化次数及 warning。CLI 没有自动匹配、覆盖、去重或发布文章的功能。

## 结构保留

优先 body_asl：本包 body HTML 已将 95 个公式栅格化，并平铺了 21 个 blockquote。代码卡片直接使用原 code payload 与 mode，动态长度 fence 防止正文中的反引号截断代码。mode=latex 的流程图/说明仍作为代码，不能仅根据语言名改为公式。

公式卡片保留 LaTeX；独立公式使用 `$$`，行内公式使用 `$`。图片保留 src、caption、宽高，crop 通过元数据和 CSS 视窗表示。复杂表格保留 HTML；源中平铺但带缩进的列表保留 HTML offset，避免虚构嵌套关系。source anchor、链接、引用、下划线、sup/sub、前景色和背景高亮尽可能保留。

未知卡片/节点输出可读原节点降级内容、conversion-warning 和质量报告 warning，不静默丢失。仅有图片的公式缺少 LaTeX、裁剪尺寸缺失等也记录 warning。

## Hugo 格式规范

- 若源正文含 H1，全篇正文标题统一 level +1，最高到 H6；源 H2 起步的不偏移。quality 的 level 保留源层级，rendered_level 记录实际层级，heading_level_offset 记录偏移。这避免正文与网站文章 H1 冲突，并让正文主章节进入从 H2 开始的目录。
- ASL strong/b、em/i 使用 inline HTML strong/em，避免中文紧邻标点时 Markdown delimiter 失效。普通文字中明确配对的双星号粗体也转换为 strong；单星号不自动识别，以免误判乘号。代码、inline code、数学 payload 不执行此规范。
- 普通文字的字面方括号输出 `&#91;` / `&#93;`，避免反斜杠方括号被 Goldmark LaTeX passthrough 当作公式；可见文本仍为原方括号。
- 空段落/格式节点（含零宽编辑器占位字符）不输出假水平线或空 emphasis；有源链接目标用途的 anchor 保留。真正的 hr 卡片保留。
- 按块状态将连续空行规范到最多一个空白行，fenced code、独立数学块、HTML table/pre 的 payload 不变。Pathtracer 的本地代码链接转为文件名与行号文本，保留有意义标签，映射输出 local-reference-normalization.json；不猜测公网仓库。

编辑器字体、行距、视觉段落缩进、代码折叠/高亮行、书签预览装饰等表现信息不强行映射，在 presentation_notes 中记录。图片裁剪仍需要浏览器对照检查；文本验证不等价于最终页面视觉验收。

## 本次包的完整性结果

| 项目 | 源数量 / 验证结果 |
| --- | --- |
| doc | 135 个，均有转换结果；95 个有实质源正文，40 个为空或仅空段落 |
| codeblock | 489 个；独立 CommonMark 渲染后逐段比对原 payload，仅允许 fence 必需的末尾单个换行 |
| math | 95 个，原 LaTeX code/hash 保留 |
| image | 68 个，源与渲染数量一致 |
| heading | 631 个，源与渲染数量/规范化层级一致 |
| 其他 | hr 144、bookmarkInline 11、bookmarklink 4、blockquote 21、table 8、list 450 |
| 格式规范 | 4 个含 H1 文档统一偏移；28 处普通文字双星号配对规范化；43 处本地引用转为可读文件/行号 |
| 质量 | 六类 811 个卡片全部转换；所有有意义源文本被访问并在独立渲染后保留；未知卡片/内容节点 0，独立验证问题文档 0 |

独立文本比对只允许移除明确成对的双星号格式 delimiter；代码仍按原字符逐段严格比对。CommonMark 验证使用 markdown-it-py，它是验证依赖，不是转换器运行依赖。Hugo/浏览器还须检查目录、MathJax、资源和站内链接；技术问题另列于 [content-review.md](content-review.md)，不由转换器修正。
