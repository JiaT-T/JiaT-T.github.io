+++
title = "11"
problems = [11, 5, 16, 26, 165]
+++

#### <font style="color:#DF2A3F;">第十一题</font>：[<font style="color:rgb(10, 132, 255);">盛最多水的容器</font>](https://leetcode.cn/problems/container-with-most-water/)

如果直接用两个for循环遍历所有容积情况，时间复杂度是O(n^2)，会超时.....



所有需要使用正确的算法



那么这题使用的就是双指针的方法。



&nbsp; 

&nbsp;      首先分析思路：虽然说是双指针，但实际上使用的是两个索引的方法--定义left=0（最左边），right=数组大小-1（最右边），然后计算出初始的容积大小



我们发现，移动长板（向里走，也就是将索引向里挪一位）会使水槽的宽度会变窄，即使移动过后得到的板子是更长的板子，容积仍然会变小，更短的板子同理（短板效应）；但是如果移动的是短板，假如下一块板子是更长的，那么就有可能会使容积变大（e.g.第一块板子长为1，最后一块板子长为7，一共九块板子，那么此时容积就是（1x8）=8，接下俩移动短板，第二块板子长为8，此时容积为（7x7）=49，容积变大了）



所以，只需要找到两块板子中更短的那块，固定住长板，只移动短板就行
```cpp

int maxArea(vector<int>& height)

    {

        int left = 0, right = static_cast<int>(height.size()) - 1;

        int volumn = std::min(height[left],height[right]) * right;

        while(left < right)

        {

            if(height[left] < height[right])

            {

                left++;

            }

            else

            {

                right--;

            }

            volumn = std::max(volumn, (std::min(height[left],height[right]) * (right - left)));

        }

        return volumn;

    }
```

<a id="T4KX3"></a>
#### 第五题：[最长回文子串](<https://leetcode.cn/problems/longest-palindromic-substring/>)

<a id="u533c851a"></a>使用的是“<strong>中心扩散法</strong>”

<a id="u13dfc938"></a>参考了这里的解法：<a id="VJdpF"></a>[https://leetcode.cn/problems/longest-palindromic-substring/solutions/2958179/mo-ban-on-manacher-suan-fa-pythonjavacgo-t6cx/](<https://leetcode.cn/problems/longest-palindromic-substring/solutions/2958179/mo-ban-on-manacher-suan-fa-pythonjavacgo-t6cx/>)

<a id="uab0df562"></a>对于奇回文串，我们从最中间的一个元素开始向两边扩散，比如“bab”，第一次判断时 left = right，条件符合，所以 left--， right++；然后进入第二次判断，此时两者指向的字符都是‘b'，条件依然满足....直到左右指针指向的字符不同时，计算当前字符串长度

<a id="u0cd1f00d"></a>对于偶回文串，还是从中间开始扩散，只不过这次需要选取两个元素

<a id="ud9861e3c"></a>为了将两种情况合并处理，可以将 i 的最大范围改为 2n - 1，因为

- <a id="ue42e5f85"></a><strong>奇数长度回文中心</strong>：每个字符本身就是一个中心 → `n` 个
- <a id="uab6b0129"></a><strong>偶数长度回文中心</strong>：每两个相邻字符之间是一个中心 → `n - 1` 个

<a id="u9a4e8d28"></a>两者相加，所有回文中心的数量就是 <strong>2n - 1</strong> 个

<a id="y3ZCb"></a>
longestPalindrome（）
```cpp
string longestPalindrome(string s) 
{
    int left = 0, right = 0;
    int n = s.size();
    for(int i = 0; i < 2 * n - 1; i++)
    {
        int l = i / 2, r = (i + 1) / 2;
        while(0 <= l && r < n && s[l] == s[r])
        {
            l--;
            r++;
        }
        if(r - l - 1 > right - left)
        {
            right = r;
            left = l + 1;
        }
    }
    return s.substr(left, right - left);
}
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ozm4mkuk4gloh4gq)

<a id="tb3Ir"></a>
#### 第十六题：[最接近的三数之和](<https://leetcode.cn/problems/3sum-closest/>)

<a id="u1cb8d51f"></a>与上一题（15题）一样，使用的是双指针与双循环，这样可以将O(n^3)的时间复杂度降低至O(n^2)

<a id="u4da54687"></a>首先对数组进行排序，方便后续左右指针的移动

<a id="u28ee7133"></a>如果当前的和恰好与目标值相同，就直接返回

<a id="u8b0c5c53"></a>接着与最接近的值进行比较，如果当前值更加接近，则替换

<a id="u5dc1cd9a"></a>最后判断当前的和与目标值的大小关系，如果更小，说明需要找到更大的数，因此将左指针右移，反之，将右指针左移

<a id="TDPjD"></a>
threeSumClosest（）
```cpp
int threeSumClosest(vector<int>& nums, int target)
    {
        int length = nums.size();
        std::sort(nums.begin(), nums.end());
        int closest_sum = nums[0] + nums[1] + nums[2];

        for(int i = 0; i < length - 2; i++)
        {
            int left = i + 1, right = length - 1;
            while(left < right)
            {
                int current_sum = nums[i] + nums[left] + nums[right];
                if(current_sum == target) return current_sum;
                if(std::abs(current_sum - target) < std::abs(closest_sum - target))
                    closest_sum = current_sum;
                if(current_sum < target)
                    left++;
                else 
                    right--;
            }
        }
        return closest_sum;
    }
```

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ozm4mkuk4gloh4gq)

<a id="PZjti"></a>
#### 第二十六题：[删除有序数组中的重复项](<https://leetcode.cn/problems/remove-duplicates-from-sorted-array/>)

<a id="uc2b2cb1d"></a>使用的是双指针

<a id="u3c384589"></a>这里如果使用最原始的方法：如果当前元素与上一个相同则删除(erase），会导致O(n^2)的时间复杂度——————erase（）会将删除元素后面的元素向前移动

<a id="u4fa07d21"></a>而这里，我们定义了两个指针，一个慢指针（k），一个快指针（i）；将两个指针对应的值进行比较，如果不同，就将慢指针后移，同时将慢指针所指元素覆盖为当前元素

<a id="u13339e5b"></a>在这个方法中，我们并没有真正执行“删除”操作，而是对数组进行了重新排列，将重复的元素放到数组末尾，因为最终的返回值是有效的数字个数，因此末尾的区域也就会变成垃圾数据，不需要再去关心它们

<a id="Iw5u9"></a>
removeDuplicates（）
同一份实现已收录于[第 26 题解法](/leetcode/list/medium/leetcode-list-medium/#第二十六题)。

来源：[语雀原笔记](https://www.yuque.com/u62694975/iaaa/ozm4mkuk4gloh4gq)

<a id="TUFHn"></a>
#### 第一百六十五题：[比较版本号](<https://leetcode.cn/problems/compare-version-numbers/>)

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

