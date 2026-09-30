---
title: "回溯算法模板"
slug: "backtracking-overview"
summary: "记录回溯算法的结果集合、当前路径、终止条件以及撤销操作的 C++ 模板。"
categories: ["LeetCode"]
tags: ["LeetCode", "C++", "回溯"]
date: "2026-04-26T06:46:04.000Z"
lastmod: "2026-05-17T05:35:09.000Z"
draft: false
yuque_slug: "gh4zd0hsiauprnm7"
source: "https://www.yuque.com/u62694975/iaaa/gh4zd0hsiauprnm7"
---

<a id="u751a2a04"></a><strong>模板：</strong>

<a id="x9i11"></a>
回溯模板
```cpp
class Solution
{
private:
    vector<Type_> res;
    Type_ path;
public:
    void backtracking(输入参数)
    {
        if (终止条件)
        {
            res.push_back(path);
            return;
        }

        for (本层要使用的集合)
        {
            处理节点;
            backtracking(...);
            回溯，即撤销之前的结果;
        }
    }

    vector<Type_> func(输入参数)
    {
        backtracking(...);
        return res;
    }
};
```

原文：[回溯](<https://www.yuque.com/u62694975/iaaa/gh4zd0hsiauprnm7>)
