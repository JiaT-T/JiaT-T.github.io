+++
title = "33、34、74、153"
+++

#### <font style="color:#DF2A3F;">第三十三题</font>：[搜索旋转排序数组](https://leetcode.cn/problems/search-in-rotated-sorted-array/)
一开始的想法是：先遍历一遍旋转后的数组，分别找到两个各自单调的子数组，之后对这两个数组分别进行二分查找；但这会导致线性的时间复杂度，而不是题目要求的logn

而下面这种方法就是不通过遍历，**直接在二分查找中对有序的子数组进行判断**

具体实现：

仍然是先定义左右边界（左闭右开），之后进入循环

当mid对应的值恰好与target相等时，则mid就是我们要找的下标

若是不等，则根据当前中点值与最右值得比较结果，对左数组与右数组进行选择

之后再在这两个子数组中进行二分查找

```cpp
int search(vector<int>& nums, int target)
{
    int left = 0, right = nums.size() - 1;
    while(left <= right)
    {
        int mid = left + (right - left) / 2;
        if(nums[mid] == target)
            return mid;
        else if(nums[left] <= nums[mid])
        {
            // 进入左数组
            if(nums[left] <= target && target < nums[mid])
                right = mid;
            else
                left = mid + 1;
        }
        else
        {
            //进入右数组
            if(nums[mid] < target && target <= nums[right])
                left = mid + 1;
            else
                right = mid;
        }
    }
    return -1;
}
```



#### <font style="color:#DF2A3F;">第三十四题</font>：[在排序数组中查找元素的第一个和最后一个位置](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/)
**lowerBound函数**：返回第一个 >= target的数的下标

<u>实现原理</u>：内部是一个while循环，当循环结束时，应当恰好有 left = right 成立，此时right代表					的就是“第一个 >= target的数的下标”————

                - **左阵营 (**`**left**`**)**：在这个索引左边的数，我们确定**全部**都 < target
                - **右阵营 (**`**right**`**)**：在这个索引（包含自身）右边的数，我们确定**全部**都  >= target

又因为target的第一个数恰好满足这个条件，使用**lowerBound**返回的实际上是target的右边界

之后在主函数中如法炮制，通过**求得target+1的首位，再减去1**，所得到的就是target的右边界

```cpp
vector<int> searchRange(vector<int>& nums, int target)
{
    int start = lowerBound(nums, target);
    if(start == nums.size() || nums[start] != target)
        return {-1, -1};
    int end = lowerBound(nums, target + 1) - 1;
    return {start, end};
}

// 返回第一个 >= target的数的下标
int lowerBound(vector<int>& nums, int target)
{
    int left = 0, right = nums.size();
    while(left < right)
    {
        int mid = left + (right - left) / 2;

        if(target <= nums[mid])
            right = mid;
        else
            left = mid + 1;
    }
    return right;
}
```



#### <font style="color:#DF2A3F;">第七十四题</font>：[搜索二维矩阵](https://leetcode.cn/problems/search-a-2d-matrix/)
<font style="background-color:#FBDE28;">解法一：</font>

把二维矩阵转入一维数组，再对这个数组进行二分查找

空间、时间复杂度都为O(M * N)

```cpp
bool searchMatrix(vector<vector<int>>& matrix, int target) 
{
    std::vector<int> vec;
    vec.reserve(matrix.size() * matrix[0].size());
    for(auto row : matrix)
    {
        for(auto element : row)
        {
            vec.push_back(element);
        }
    }
    return std::binary_search(vec.begin(), vec.end(), target);
}
```

  
 	<font style="background-color:#FBDE28;">解法二：</font>

核心公式：_<font style="color:#117CEE;">a</font>_<font style="color:#117CEE;">[ </font>_<font style="color:#117CEE;">i </font>_<font style="color:#117CEE;">]=</font>_<font style="color:#117CEE;">matrix </font>_<font style="color:#117CEE;">[ </font>_<font style="color:#117CEE;">i </font>_<font style="color:#117CEE;">/ </font>_<font style="color:#117CEE;">n </font>_<font style="color:#117CEE;">][ </font>_<font style="color:#117CEE;">i </font>_<font style="color:#117CEE;">mod </font>_<font style="color:#117CEE;">n </font>_<font style="color:#117CEE;">]</font>

实际上并不需要再开辟一个M*N的空间用于存储二维矩阵，可以直接根据一维数组下标与行列的关系找到对应元素

```cpp
bool searchMatrix(vector<vector<int>>& matrix, int target) 
{
    int rows = matrix.size(), cols = matrix[0].size();
    int left = 0, right = rows * cols;
    while(left < right)
    {
        int mid = left + (right - left) / 2;
        int x = matrix[mid / cols][mid % cols];
        if(target == x) 
            return true;
        else if(x < target)
            left = mid + 1;
        else if(target < x)
            right = mid;
    }
    return false;
}
```



#### <font style="color:#DF2A3F;">第一百五十三题</font>：[寻找旋转排序数组中的最小值](https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array/)
可以将旋转后的数组视为两个并排的上升台阶，前一部分是“**高位台阶**”，后一部分是“**低位台阶**”（只有当旋转nums.size()的整数倍时才会出现前低后高的情况）

高位台阶中的每一级都大于低位台阶的最大级，也就是数组的最后一位；因此，如果<u> nums.back() < nums[mid]</u> 的话，就可以认为最小值一定在 **mid 右边**；反之，<u>nums[mid]  <= nums.back()</u> 的话，最小值就在 **mid 左边** 或 **nums[mid] 自身就是最小值**

根据这一特性，只需要比较 _x_ 和 _nums_[_n_−1] 的大小关系，就**间接地**知道了 _x_ 和数组最小值的位置关系，从而不断地缩小数组最小值所在位置的范围，二分找到数组最小值

```cpp
int findMin(vector<int>& nums)
{
    int left = 0, right = nums.size();
    while(left < right)
    {
        int mid = left + (right - left) / 2;
        if(nums[mid] <= nums.back())
            right = mid;
        else 
            left = mid + 1;
    }
    return nums[left];
}
```
