#### <font style="color:#DF2A3F;">第七十题</font>：[爬楼梯](https://leetcode.cn/problems/climbing-stairs/)
简单的斐波那契公式

要注意的是，这里使用递归会超时，然后最好不要使用数组（因为除了当前值的前两个，再往前的数据更本就用不到，应该使用临时变量，存储在栈上，用完就释放内存）

```cpp
int climbStairs(int n)
{
    if(n <= 2) return n;

    int prev1 = 1, prev2 = 2;
    int curr = 0;
    for(int i = 3; i <= n; i++)
    {
        curr = prev1 + prev2;
        prev1 = prev2;
        prev2 = curr;
    }
    return curr;
}
```



#### <font style="color:#DF2A3F;">第一百一十八题</font>：[杨辉三角](https://leetcode.cn/problems/pascals-triangle/)
[1]

[1,1]

[1,2,1]

[1,3,3,1]

[1,4,6,4,1]

把左端对齐，以符合二维数组的格式

根据杨辉三角的定义，可以知道，当前元素的值，等于左上方元素加正上方的元素，也就是

**v[i][j] = v[i-1][j-1] + v[i-1][j]**

又因为每一层的大小都比上一层多一个，所以每次循环都需要对数组向后扩容一位，并将所有元素初始化为1**  
**

```cpp
vector<vector<int>> generate(int numRows)
    {
        std::vector<std::vector<int>> vec(numRows);
        for(int i = 0; i < numRows; i++)
        {
            vec[i].resize(i+1, 1);
            for(int j = 1; j < i; j++)
            {
                vec[i][j] = vec[i-1][j-1] + vec[i-1][j];
            }
        }
        return vec;
    }
```
