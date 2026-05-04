#### <font style="color:#DF2A3F;"> 第三十一题</font>：[<font style="color:rgb(10, 132, 255);">下一个排列</font>](https://leetcode.cn/problems/next-permutation/)
思路：<u>找到下一个排序，意思就是将当前数组视作一串数字，通过对元素的重新组合，找到</u><u><font style="background-color:#FBDE28;">第一个大于当前数字的数字</font></u>

具体实现：  
	首先从后往前找到第一个逆序的数字，保存它的下标——如：123546718，这里会保存数字“4”的下标，也就是 4，之后再在 46718 这个范围内从后往前寻找第一个小于 5 的数字，并将其进行交换（123146758）；最后将46758进行降序·排序即可得到下一个排序

```cpp
void nextPermutation(vector<int>& nums)
{
    int sz = nums.size();
    if(sz <= 1) return;
    int i = sz - 1;
    while(0 < i && nums[i] <= nums[i - 1])
    {
        i--;
    }

    // 如果 i == 0，说明整个序列都是降序的（如 54321），已经是最大排列
    if(0 < i)
    {
        int j = sz - 1;
        while(nums[j] <= nums[i - 1])
        {
            j--;
        }

        std::swap(nums[i - 1], nums[j]);
    }
    std::sort(nums.begin() + i, nums.end());
}
```



#### <font style="color:#DF2A3F;">第七十五题</font>：[颜色分类](https://leetcode.cn/problems/sort-colors/)
<font style="background-color:#FBDE28;">解法一：</font>

先通过一次遍历得到红、白、蓝三个颜色各自的数量，之后再通过一次O(n)的遍历（三个循环的时间复杂度加起来是O(n) )把颜色进行排序

虽然O(2n) = O(n)，但这样还是遍历了两次，有没有只需要遍历一次的办法？

```cpp
void sortColors(vector<int>& nums)
{
    int r = 0, w = 0, b = 0;
    for(int num : nums)
    {
        switch(num)
        {
            case 0: r++; break;
            case 1: w++; break;
            case 2: b++; break;
        }
    }
    for(int i = 0; i < r; i++) nums[i] = 0;
    for(int j = r; j < r + w; j++) nums[j] = 1;
    for(int k = r + w; k < r + w + b; k++) nums[k] = 2;
}
```



解法二：



#### <font style="color:#DF2A3F;">第二百八十七题</font>：[寻找重复数](https://leetcode.cn/problems/find-the-duplicate-number/)
用到了**”环形链表”**的思想

对于含有唯一 一个重复元素的数组，使用快慢指针进行遍历，fast每次两步（nums[nums[fast]]），slow每次一步（nums[slow]），那么之后一定会产生一个环，而入口就是那个重复的元素

之后只需要再指定一个从起点出发的指针，与slow一起再次进行遍历，最终相遇的位置就是重复数字的位置

（关于环形更具体的解释参见“链表 -> Medium”）

```cpp
int findDuplicate(vector<int>& nums) 
{
    int fast = nums[nums[0]], slow = nums[0];
    while(fast != slow)
    {
        fast = nums[nums[fast]];
        slow = nums[slow];
    }

    int finder = 0;
    while(finder != slow)
    {
        finder = nums[finder];
        slow = nums[slow];
    }
    return slow;
}
```




