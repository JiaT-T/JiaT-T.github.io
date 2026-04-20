#### <font style="color:#DF2A3F;">第九十四题</font>：[二叉树的中序遍历](https://leetcode.cn/problems/binary-tree-inorder-traversal/)
非常基础的一个遍历，感觉没什么好说的....

首先确定递归函数的参数和返回值：void--因为这里直接传入了一个vector的引用

然后明确递归终止的条件：<font style="background-color:#FBDE28;">当前节点为空</font>

这也就意味着当前分支上的所有节点都已经遍历完了，所以应该进入下一个分支

比如中序遍历，顺序是“左中右”，所以inorder函数中就是先递归左分支，再将中间节点压入vector，最后遍历右分支

其他两个遍历以此类推

```cpp
void inorder(TreeNode* root, std::vector<int>& traversal)
{
    if(root == NULL) return;
    inorder(root->left, traversal);
    traversal.push_back(root->val);
    inorder(root->right, traversal);
}

vector<int> inorderTraversal(TreeNode* root)
{
    std::vector<int> traversal;        

    inorder(root, traversal);
    return traversal;
}
```

#### <font style="color:#DF2A3F;">第一百零一题</font>：[对称二叉树](https://leetcode.cn/problems/symmetric-tree/)
要判断一个二叉树是否对称，就是判断这个树<font style="background-color:#FBDE28;">根节点的左右子树是否能够翻转</font>，而判断能否翻转，则需要判断这棵二叉树的内外侧节点是否相同

因为需要拿到左右子树各自的信息，所以使用后序遍历

首先对特殊情况进行判断：

1.传入的左节点不为空，右节点为空，那么无法翻转

2.左空右不空同理

3.两边都为空时，可以翻转

4.两遍都不为空，但是值不同，不能翻转

5.只有当两者都不为空且值相等时，才进入递归逻辑，判断左子树的左节点与右子树的右节点能否翻转（外侧），以及左子树的右节点与右子树的左节点能否翻转（内侧）

最后，只有当左右节点都能反转时，才可以认为这棵树 / 子树能翻转

```cpp
bool Compare(TreeNode* left, TreeNode* right)
    {
        if(!left && right) return false;
        else if(left && !right) return false;
        else if(!left && !right) return true;
        else if(left->val != right->val) return false;
        else
        {
            bool outside = Compare(left->left, right->right);
            bool inside = Compare(left->right, right->left);
            return outside && inside;
        }
    }
    bool isSymmetric(TreeNode* root)
    {
        return Compare(root->left, root->right);
    }
```

#### <font style="color:#DF2A3F;">第一百零四题</font>：[二叉树的最大深度](https://leetcode.cn/problems/maximum-depth-of-binary-tree/)
求深度：用前序遍历；求高度：用后序遍历

而二叉树的最大深度，恰好就是root节点的高度，因此求root的高度即可

至于为什么不直接用后序遍历求深度，是因为代码量相对于求高度的方法更多



先沿着左右子树进行遍历，得到左右子树各自的最大深度，取最大值加1即可得到当前中间节点的深度

以此类推，可以逐步累加得到根节点（最上方的中间节点）的高度

```cpp
int maxDepth(TreeNode* root)
{
    if(root == NULL) return 0;
    int leftDepth = maxDepth(root->left);
    int rightDepth = maxDepth(root->right);
    int depth = 1 + std::max(leftDepth, rightDepth);
    return depth;        
}

// 精简版
int maxDepth(TreeNode* root)
{
    if(root == NULL) return 0;
    return 1 + std::max(maxDepth(root->left), maxDepth(root->right));        
}
```

#### <font style="color:#DF2A3F;">第一百零八题</font>：[将有序数组转换为二叉搜索树](https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/)
先回顾一下二叉搜索树的定义：<u>左子树的任一节点都小于根节点，右子树的任一节点都大于根节点</u>

现在拿到了一个有序数组，自然可以想到要从中间开始进行遍历，因此首先找到数组的中间节点，并以它作为根节点向左右进行遍历，因为数组已经有序，所以不需要再进行比较，只需要明确每一次构造的左右边界即可

至于为什么不需要考虑奇偶数组的情况，这是因为int的除法会自动向下取整，所以即使是偶数数组，也能够保证平衡（但不是对称）

```cpp
TreeNode* traversal(vector<int>& nums, int left, int right)
{
    if(left > right) return nullptr;
    int mid = (left + right) / 2;
    TreeNode* root = new TreeNode(nums[mid]);
    root->left = traversal(nums, left, mid - 1);
    root->right = traversal(nums, mid + 1, right);
    return root;
}

TreeNode* sortedArrayToBST(vector<int>& nums)
{
    return traversal(nums, 0, nums.size() - 1);
}
```

#### <font style="color:#DF2A3F;">第二百二十六题</font>：[翻转二叉树](https://leetcode.cn/problems/invert-binary-tree/)
以**前序遍历**为例，从根节点开始，逐步交换左右子树（先交换左子树，后交换右子树），直到所有叶子节点都交换完毕；**后序遍历**同理，先把左子树的所有节点交换完毕，再处理右子树，最后在root节点处将整个左右子树交换

而**中序遍历**是个特例，它会先交换左子树的所有节点，然后逐层返回到最顶部的root节点，将左子树和右子树交换，此时如果按照之前的逻辑，继续对右子树进行交换的话，相当于是对一开始的左子树又进行了一次交换，所有此时需要改变一下代码，进行对左子树）也就是一开始的右子树）进行交换，这样才能得到正确的结果

```cpp
// 前序
TreeNode* invertTree(TreeNode* root)
{
    if(root == nullptr) return nullptr;
    std::swap(root->left, root->right);
    invertTree(root->left);
    invertTree(root->right);

    return root;
}

// 中序
TreeNode* invertTree(TreeNode* root)
{
    if(root == nullptr) return nullptr;
    invertTree(root->left);
    std::swap(root->left, root->right);
    invertTree(root->left);
    
    return root;
}

// 后序
TreeNode* invertTree(TreeNode* root)
{
    if(root == nullptr) return nullptr;
    invertTree(root->left);
    invertTree(root->right);
    std::swap(root->left, root->right);

    return root;
}
```

#### <font style="color:#DF2A3F;">第五百四十三题</font>：[二叉树的直径](https://leetcode.cn/problems/diameter-of-binary-tree/)
最开始的想法是：分别求左右子树的最大深度，之后再加上二就是二叉树的直径

但是这个方法仅仅只是”局部最优解“而非”全局最优解“，因为二叉树的直径也可能不会跨越根节点（比如当左子树为深度非常大的满二叉树，而右子树仅仅只有一个节点时，那么直径就会在左子树出现），因此需要判断直径的计算是否会跨越根节点

```cpp
int maxDepth(TreeNode* curr, int& max_dep)
{
    if(!curr) return 0;
    
    int left_dep = maxDepth(curr->left, max_dep);
    int right_dep = maxDepth(curr->right, max_dep);
    max_dep = std::max(max_dep, left_dep + right_dep);
    return std::max(left_dep, right_dep) + 1;
}

int diameterOfBinaryTree(TreeNode* root)
{
    int max_dep = 0;
    maxDepth(root, max_dep);
    return max_dep;
}
```
