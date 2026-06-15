+++
title = "11"
problems = [11]
+++

\#### <font style="color:#DF2A3F;">第十一题</font>：\[<font style="color:rgb(10, 132, 255);">盛最多水的容器</font>](https://leetcode.cn/problems/container-with-most-water/)

如果直接用两个for循环遍历所有容积情况，时间复杂度是O(n^2)，会超时.....



所有需要使用正确的算法



那么这题使用的就是双指针的方法。



&nbsp; 

&nbsp;      首先分析思路：虽然说是双指针，但实际上使用的是两个索引的方法--定义left=0（最左边），right=数组大小-1（最右边），然后计算出初始的容积大小



我们发现，移动长板（向里走，也就是将索引向里挪一位）会使水槽的宽度会变窄，即使移动过后得到的板子是更长的板子，容积仍然会变小，更短的板子同理（短板效应）；但是如果移动的是短板，假如下一块板子是更长的，那么就有可能会使容积变大（e.g.第一块板子长为1，最后一块板子长为7，一共九块板子，那么此时容积就是（1x8）=8，接下俩移动短板，第二块板子长为8，此时容积为（7x7）=49，容积变大了）



所以，只需要找到两块板子中更短的那块，固定住长板，只移动短板就行



```cpp

int maxArea(vector<int>\& height)

&nbsp;   {

&nbsp;       int left = 0, right = static\_cast<int>(height.size()) - 1;

&nbsp;       int volumn = std::min(height\[left],height\[right]) \* right;

&nbsp;       while(left < right)

&nbsp;       {

&nbsp;           if(height\[left] < height\[right])

&nbsp;           {

&nbsp;               left++;

&nbsp;           }

&nbsp;           else

&nbsp;           {

&nbsp;               right--;

&nbsp;           }

&nbsp;           volumn = std::max(volumn, (std::min(height\[left],height\[right]) \* (right - left)));

&nbsp;       }

&nbsp;       return volumn;

&nbsp;   }

```







