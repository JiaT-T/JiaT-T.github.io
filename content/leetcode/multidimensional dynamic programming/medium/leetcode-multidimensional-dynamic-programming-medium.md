第六十二题：不同路径
解法一：
定义状态：dp[ i ][ j ] 指的是”走到点（i，j）的不同路径数量
状态转移：dp[ i ][ j ] = dp[ i - 1 ][ j ] + dp[ i ][ j - 1]，即“要想走到点(i, j)，只有两个选择——从（i-1，j）向下走，或者从（i，j-1）向右走
int uniquePaths(int m, int n)
{
    int dp[m][n];
    for(int i = 0; i < m; i++) dp[i][0] = 1;
    for(int i = 0; i < n; i++) dp[0][i] = 1;
    for(int i = 1; i < m; i++)
    {
        for(int j = 1; j < n; j++)
        {
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        }
    }
    return dp[m - 1][n - 1];
}
解法二：
第一个方法的空间复杂度是m*n，然而在每一次的计算中，实际只用到了两个元素，所以可以进行优化
只需要维护一个一维数组，dp[j]代表着当前元素，使用dp[j]自加dp[j-1]（左边的元素），等价于 dp[i][j] = dp[i - 1][j] + dp[i][j - 1]，因为旧的dp[j]就是当前元素的上面一个元素
int uniquePaths(int m, int n)
{
    std::vector<int> dp(n, 1);
    for(int i = 1; i < m; i++)
    {
        for(int j = 1; j < n; j++)
        {
            dp[j] += dp[j - 1];
        }
    }
    return dp[n - 1];
}

第六十四题：最小路径和
和上面那题基本一样，只不过状态转移方程变成了”dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]“
int minPathSum(vector<vector<int>>& grid)
{
    int r = grid.size(), c = grid[0].size();
    int dp[r][c];
    dp[0][0] = grid[0][0];
    for(int i = 1; i < r; i++) dp[i][0] = grid[i][0] + dp[i - 1][0];
    for(int i = 1; i < c; i++) dp[0][i] = grid[0][i] + dp[0][i - 1];

    for(int i = 1; i < r; i++)
    {
        for(int j = 1; j < c; j++)
        {
            dp[i][j] = std::min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j];
        }
    }
    return dp[r - 1][c - 1];
}