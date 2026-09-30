---
title: "LeetCode 栈：困难题组"
slug: "leetcode-stack-hard"
summary: "记录柱状图中最大矩形的思路与 C++ 实现。"
categories: ["LeetCode"]
tags: ["LeetCode", "C++", "栈", "单调栈"]
date: "2026-06-02T04:40:08.000Z"
lastmod: "2026-06-02T04:55:39.000Z"
draft: false
yuque_slug: "evf1id2gv1gqhd7o"
source: "https://www.yuque.com/u62694975/iaaa/evf1id2gv1gqhd7o"
problems: [84]
---

<a id="klBOh"></a>
#### <span style="color: #DF2A3F">第八十四题</span>：[<span style="color: inherit">柱状图中最大的矩形</span>](<https://leetcode.cn/problems/largest-rectangle-in-histogram/>)

<a id="u6dab688e"></a>这次与<a id="KTH7b"></a>[盛最多水的容器](<https://leetcode.cn/problems/container-with-most-water/>)非常相似，但不同的的是十一题只需要看两边的木板长度，而这一题需要考虑容器中间的最低高度

<a id="qOVXW"></a>
largestRectangleArea（）
```cpp
int largestRectangleArea(vector<int>& heights)
{
    // 当右边所有矩形都比当前矩形高时
    // 有可能不会计算以当前矩形为中心的结果
    // 在末尾设置一个 -1（比任何矩形都要低）
    // 可以强制触发”heights[right] <= heights[st.top()]“
    // 计算当前结果
    heights.push_back(-1);
    std::stack<int> st;
    // 同理，这里是为了防止左边都高于右边的情况
    st.push(-1);
    int area = 0;

    // 外层循环会对每一个矩形都进行一次 area 的计算
    for(int right = 0; right < heights.size(); right++)
    {
        // 内层循环则定义具体的计算步骤
        while(1 < st.size() && heights[right] <= heights[st.top()])
        {
            // 栈顶代表矩形的高
            int h = st.top();
            st.pop();
            // 栈顶下面的那个数代表左边界
            int left = st.top();
            // 计算面积
            area = std::max(area, heights[h] * (right - left - 1));
        }
        // 将当前的右边界作为下一次的左边界
        st.push(right);
    }
    return area;
}
```

原文：[hard](<https://www.yuque.com/u62694975/iaaa/evf1id2gv1gqhd7o>)
