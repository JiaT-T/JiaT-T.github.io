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

