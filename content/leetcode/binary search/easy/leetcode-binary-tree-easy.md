#### <font style="color:#DF2A3F;">第三十五题</font>：[搜索插入位置](https://leetcode.cn/problems/search-insert-position/)
定义左闭右开区间

当left = right时，意味着值被找到了

```cpp
int searchInsert(vector<int>& nums, int target)
{
    int left = 0, right = nums.size();
    while(left < right)
    {
        int mid = left + (right - left) / 2;
        if(nums[mid] < target) 
            left = mid + 1;           
        else
            right = mid;
    }
    return left;
}
```
