+++
slug = "compare-version-numbers"
title = "比较版本号"
problems = [165]
problem_id = 165
difficulty = "Medium"
weight = 165
summary = "比较版本号的解题思路与 C++ 实现。"
source = "https://www.yuque.com/u62694975/iaaa/ozm4mkuk4gloh4gq"
+++

题目：[比较版本号](https://leetcode.cn/problems/compare-version-numbers/)


<a id="第一百六十五题比较版本号"></a>

<a id="TUFHn"></a>

<a id="ud1123ddf"></a>这题的核心是：<strong>以每一个‘.‘作为分界线</strong>，将 string 转换为 int，逐段进行比较，如果相同，就进入下一段进行比较；如果不同，则根据数值的大小选择返回值

<a id="QtlUe"></a>
compareVersion（）
```cpp
int compareVersion(string version1, string version2)
{
    // 定义两个版本各自的指针
    int i = 0, j = 0;
    int n1 = version1.size(), n2 = version2.size();

    while(i < n1 || j < n2)
    {
        int num1 = 0, num2 = 0;

        // 将 v1 转化为 int，直到遇到’.‘
        while(i < n1 && version1[i] != '.')
        {
            num1 = num1 * 10 + (version1[i] - '0');
            i++;
        }
        // 将 v2 转化为 int，直到遇到’.‘
        while(j < n2 && version2[j] != '.')
        {
            num2 = num2 * 10 + (version2[j] - '0');
            j++;
        }

        // 如果不等，直接返回
        if(num1 != num2)
        {
            return num1 < num2 ? -1 : 1;
        }

        // 跳过’.'并进入下一段
        i++;
        j++;
    }
    // 如果在 while 循环中没有返回
    // 就说明两个版本号相同
    return 0;
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ozm4mkuk4gloh4gq)
