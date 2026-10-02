# JiaT-T · Graphics & Engine Notes

个人技术网站，优先展示 C++ 渲染器、实时图形 API 和 Unreal Engine 实验，同时保留图形学、引擎与编程笔记。

[在线网站](https://jiat-t.github.io/) · [项目入口](https://jiat-t.github.io/portfolio/)

首页精选 6 个 Rendering / UE 项目；说明与现有预览链接到各仓库。项目数据在 `data/portfolio.json`，不需要手改生成的 HTML。

## 本地构建

依赖 Git 和 **Hugo Extended 0.167.0**，与 GitHub Actions 一致。PaperMod 主题固定到 submodule 提交 `f207ce6d58899e1498af1c569d46ed7ee56d6966`。

```sh
git clone --recurse-submodules https://github.com/JiaT-T/JiaT-T.github.io.git
cd JiaT-T.github.io
# 若已有 clone：git submodule update --init --recursive
hugo server --bind 127.0.0.1
```

打开终端显示的本地地址。生成发布文件：`hugo --gc --minify`。

`public/`、`resources/` 和 `.hugo_build.lock` 为生成文件，不纳入源代码分支。修改源内容、配置或布局后重新生成。

## 内容与发布

- `content/`：笔记与项目介绍；`static/images/`：原有图片。
- `layouts/`、`assets/`：PaperMod 本地布局、样式与搜索扩展。
- `hugo.toml`：导航与站点设置；`data/portfolio.json`：精选项目。
- `.github/workflows/hugo.yml`：`main` 构建，发布到 `gh-pages`；Pages 使用该分支根目录。

PR 分支不会自动更新在线网站。停止跟踪生成文件也不会缩小已有 Git 历史。

## 引用与限制

网站基于 [Hugo](https://gohugo.io/) 和 [PaperMod](https://github.com/adityatelange/hugo-PaperMod)。主题保留自己的许可证；引用与配图遵循各自来源，未新增统一授权。

部分历史笔记仍在整理中。项目页描述源码或已有 UE 资产结构，不代表全部运行、性能或多人验证已完成。


## 视觉与组件

- 保留 PaperMod 与 Hugo Markdown 渲染，默认深色，可切换浅色并记住选择。
- `assets/css/extended/custom.css` 定义全局主题、排版和导航；`home.css`、`portfolio.css`、`reading.css` 分别负责首页、项目和技术阅读。
- 系统无衬线字体用于正文，首页大标题使用系统衬线字体，等宽字体用于代码及 metadata；无外部字体请求、UI 框架或装饰性 WebGL。
- 首页和 `/portfolio/` 共用 `layouts/partials/project-grid.html`；项目数据保留原说明，`imageSource` 记录截图来源。`assets/images/projects/` 为压缩后的真实预览，Hugo 输出响应式 WebP。
- 所有原文章 URL 保留；`/archives/` 按主题组织，原 `/posts/`、`/categories/`、`/search/` 仍可访问。
- 文章在桌面显示目录侧栏，小屏可折叠；历史语雀内联色值在阅读样式中做主题适配，不修改原笔记内容。
- `assets/js/site.js` 处理主题、移动菜单、代码复制；`reading.js` 处理目录。动效尊重 `prefers-reduced-motion`。
- 首页独立使用 `.home-main` 全幅画布，`home.css` 中的导航覆盖规则仅作用于首页。五幅由内置 `image_gen` 生成的无人物 2D 动画背景位于 `assets/images/scenes/`，顺序和名称在 `data/scenes.json`；生成说明与图片处理规格见该目录的 `SOURCES.md`，这些背景不属于项目截图。
- `assets/js/scenes.js` 管理左右箭头手动循环切换与 300ms 淡入，支持方向键和减少动态偏好。首图优先加载，后续图片按需加载并在解码成功后切换，失败保留当前画面；无 JavaScript 时显示首图。

视觉改动后建议检查首页、项目、归档、长代码文章、公式文章和搜索，并在 375 / 430 / 768 / 1440 / 1920px 下确认布局、深浅主题、目录、键盘操作与控制台。
