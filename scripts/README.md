# Yuque Lakebook 转换工具

此工具将正常语雀页面 UI 导出的 `.lakebook` 转为供复核的 Markdown 和质量 JSON。它读取备份文件，不自动覆盖网站文章，也不进行部署、源文章删除、润色或技术纠错。

需要 Python 3.10+。转换器唯一第三方依赖是 BeautifulSoup4；CommonMark 渲染工具仅在独立验证时需要。以下命令从仓库根目录执行，输入和输出目录都放在仓库外；路径可换为自己的实际路径，无须修改脚本。

```powershell
python -m venv ../work/yuque-venv
../work/yuque-venv/Scripts/python -m pip install -r scripts/requirements.txt
../work/yuque-venv/Scripts/python scripts/yuque_convert.py ../work/Programming.lakebook --output ../work/converted --source-base https://www.yuque.com/u62694975/iaaa
```

macOS/Linux 使用 `../work/yuque-venv/bin/python`。`--output` 必须明确指定临时目录；重跑会更新该转换目录中的同 slug 草稿和质量报告，不删除源备份。不要把输出目录指定为 `content`。

输出包括每个源 slug 对应的 `.md` 与 `.quality.json`、汇总 conversion-quality.json，以及输出目录上一级的 local-reference-normalization.json。原始 Lakebook、完整转换草稿、逐篇质量数据可能含私密内容，均不得提交到公开仓库；公开迁移清单只放经审查的映射或匿名占位号。

## Python API

```python
from pathlib import Path
from yuque_convert import convert_doc, iter_lakebook

for member_name, doc in iter_lakebook(Path("../work/Programming.lakebook")):
    result = convert_doc(doc, source_base="https://www.yuque.com/u62694975/iaaa")
    body = result["body_markdown"]
    quality = result["quality"]
    # 由调用者先核对映射、隐私、成熟稿及重复题组；此处没有 content 写入。
```

模块 `yuque_convert` 可从脚本目录 import；API 同时接受原 doc 与 `{"doc": ...}` wrapper。body_markdown 不含 frontmatter/来源段；markdown 带原始日期和来源，不能直接拿它覆盖成熟稿。

## 迁移前后的复核

先盘点 source slug 与现有页面映射，确认空稿、私密稿、成熟稿和缺失章节；只发布审核过的正文。成熟文章保留手工编辑，新章节按映射追加。同题同一代码避免复制整段，跨题组通过已验证的站内题锚点连接；不同解法保留并注明题组。

独立 CommonMark 验证可以另装 `markdown-it-py`；它不在基础 requirements 中。验证应逐段对比原 ASL code、公式 payload/hash、文本、图片和标题层级，再执行 Hugo 构建、浏览器目录/公式/图片/代码检查。转换算法与本次验证结果见 [conversion-methods.md](../migration/conversion-methods.md)，技术待复核项见 [content-review.md](../migration/content-review.md)。
