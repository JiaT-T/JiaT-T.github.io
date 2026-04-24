\#### <font style="color:#DF2A3F;">第九十八题</font>：\[验证二叉搜索树](https://leetcode.cn/problems/validate-binary-search-tree/)

\*\*解法一\*\*：<u>通过中序遍历将整棵树装入vector，再判断数组是否单调</u>



具体实现非常简单，但不是一个好方法，因为他需要先将所有节点的数值装入容器，再进行比较，然而实际上每次比较只需要使用到两个节点，这会造成空间的浪费



所以应该使用“<font style="background-color:#FBDE28;">边遍历，边比较</font>”的方法



```cpp

void traversal(TreeNode\* root, std::vector<int>\& v)

{

&nbsp;   if(!root) return;



&nbsp;   traversal(root->left, v);



&nbsp;   v.push\_back(root->val);

&nbsp;   

&nbsp;   traversal(root->right, v);

}



bool isValidBST(TreeNode\* root)

{

&nbsp;   std::vector<int> vec;

&nbsp;   traversal(root, vec);



&nbsp;   int sz = vec.size();

&nbsp;   for(int i = 0; i < sz - 1; i++)

&nbsp;   {

&nbsp;       if(vec\[i+1] <= vec\[i]) return false;

&nbsp;   }

&nbsp;   return true;

}

```







\*\*解法二\*\*：<u>使用指针成员装载当前节点的父节点，并在访问当前节点时就继续比较</u>



这样就避免了在堆上分配内存，所有操作都只在栈上进行



相较于上一个方法，这个方法的空间复杂度从O(n)下降到了O(h),其中h为树的最大深度



```cpp

class Solution

{

public:

&nbsp;   bool isValidBST(TreeNode\* root)

&nbsp;   {

&nbsp;       if(!root) return true;                         // 遍历到叶子节点之后进行剪枝，返回上一个节点

&nbsp;       if(!isValidBST(root->left)) return false;      // 如果左子树底下的节点已经不满足规则，就没必要继续遍历了

&nbsp;       if(prev \&\& root->val <= prev->val) return false;

&nbsp;       prev = root;

&nbsp;       return isValidBST(root->right);                // 此时左边已经全部满足规则，只需要判断右子树是否也全部满足规则即可

&nbsp;   }

private :

&nbsp;   TreeNode\* prev = nullptr;

};

```



\#### <font style="color:#DF2A3F;">第一百零二题</font>：\[ 二叉树的层序遍历](https://leetcode.cn/problems/binary-tree-level-order-traversal/)

使用的是<font style="background-color:#FBDE28;">队列与深度优先搜索</font>



函数返回值为二维数组，因此需要使用多个一维数组将每一层的值存起来，而使用队列可以实现单独存储每一层的效果（FIFO）



首先判断根节点是否为空，不为空则直接入队



定义两个循环，外层循环用于记录每一层所有的值（相对于整棵树进行），内层循环用于将单层内的所有值一个一个的压入用于临时存储的vec中（相对于单层进行）



通过size，可以知道每一层需要弹出的元素的数量，从而得知哪些元素是同一层的







注：<font style="background-color:#FBDE28;">性能优化</font>：



1.提前将队列的首元素存储起来，避免后续对.front()函数的多次调用



2.使用std::move()可以避免不必要的拷贝（因为vec被来就是外层循环的局部变量，当res的push操作被执行时，也就意味着这一层的循环终止了）



```cpp

vector<vector<int>> levelOrder(TreeNode\* root)

{

&nbsp;   std::queue<TreeNode\*> que;

&nbsp;   std::vector<std::vector<int>> res;

&nbsp;   if(root) que.push(root);

&nbsp;   while(!que.empty())

&nbsp;   {

&nbsp;       int size = que.size();

&nbsp;       std::vector<int> vec;

&nbsp;       vec.reserve(size);

&nbsp;       while(size)

&nbsp;       {

&nbsp;           TreeNode\* curr = que.front();

&nbsp;           que.pop();



&nbsp;           vec.push\_back(curr->val);

&nbsp;           if(curr->left) que.push(curr->left);

&nbsp;           if(curr->right) que.push(curr->right);

&nbsp;           size--;

&nbsp;       }

&nbsp;       res.push\_back(std::move(vec));

&nbsp;   }

&nbsp;   return res;

}

```



\#### <font style="color:#DF2A3F;">第一百零五题</font>：\[从前序与中序遍历序列构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)

通过递归的方法来构造二叉树，可以拆解为三个步骤：  

&nbsp;	\*\*1).找到当前根节点\*\*  -->  \*\*2).找到左右子树的根节点\*\*  -->  \*\*3).递归深入\*\*



因为前序遍历会先遍历所有根节点，所以第一步只需要对数组 preorder 的下标进行递增即可



同时根据中序遍历的特性，左子树与右子树分别会位于 inorder 数组中根节点的左右两侧，所以需要使用一种快速的方法，能够通过根节点的值直接在 inorder 数组中找到根节点对应的下标（也可以说是位置），这里选用的是\*\*哈希表\*\*。如此一来，左右子树的所有元素就也被找到了，对拆分出来的两个数组再次递归调用即可



注：这里比较难理解的是递归时选取的左右边界



对于<font style="background-color:#FBDE28;">左子树</font>：



\*\*preorder的左边界\*\*要加1，因为preorder的第一个元素是根节点，往后一个节点就是这个根节点的左子树的根节点；\*\*右边界\*\*就是左边界位置直接加上左子树元素个数



\*\*inorder的左边界\*\*保持不变；\*\*右边界\*\*是根节点位置向前移动一位



对于<font style="background-color:#FBDE28;">右子树</font>：



\*\*preorder的左边界\*\*为初始左边界加上左子树元素的个数再加一（跨过根节点），\*\*右边界\*\*保持不变



\*\*inorder的左边界\*\*是根节点位置向后移动一位；\*\*右边界\*\*保持不变



```cpp

class Solution

{

public:

&nbsp;   TreeNode\* helper(vector<int>\& preorder, vector<int>\& inorder, int preorder\_left, int inorder\_left, int preorder\_right, int inorder\_right)

&nbsp;   {

&nbsp;       if(preorder\_left > preorder\_right) return nullptr;



&nbsp;       int root\_value = preorder\[preorder\_left];

&nbsp;       int inorder\_root = index\[root\_value];

&nbsp;       TreeNode\* root = new TreeNode(root\_value);



&nbsp;       int left\_tree\_size = inorder\_root - inorder\_left;



&nbsp;       root->left = helper(preorder, inorder, preorder\_left + 1, inorder\_left, preorder\_left + left\_tree\_size, inorder\_root - 1);



&nbsp;       root->right = helper(preorder, inorder, preorder\_left + left\_tree\_size + 1, inorder\_root + 1, preorder\_right, inorder\_right);



&nbsp;       return root;

&nbsp;   }



&nbsp;   TreeNode\* buildTree(vector<int>\& preorder, vector<int>\& inorder)

&nbsp;   {

&nbsp;       int sz = inorder.size();

&nbsp;       for(int i = 0; i < sz; i++)

&nbsp;       {

&nbsp;           index\[inorder\[i]] = i;

&nbsp;       }

&nbsp;       return helper(preorder, inorder, 0, 0, sz-1, sz-1);

&nbsp;   }

private :

&nbsp;   std::unordered\_map<int, int> index;

};

```



\#### <font style="color:#DF2A3F;">第一百一十四题</font>：\[二叉树展开为链表](https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/)

因为要求O(1)的空间复杂度，因此不能再使用额外的容器，所以这里使用了一个原地算法



思路如下：  

&nbsp;	最终结果是将原来的树退化为了一条沿着右子树不断延伸的链表，根据结果不难发现：越<u>是靠右的节点，在链表中的位置越靠前；而越是靠左的节点，在链表中的位置越往后</u>



因此，<font style="background-color:#FBDE28;">可以通过迭代，每次将父节点的整棵左子树插入父节点与右子树之间</font>



<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1776683950848-d74c54a3-3ad5-4764-a403-b247a3941bb4.png" width="562" title="" crop="0,0,1,1" id="u2c813c24" class="ne-image">



具体实现：



先确定迭代终止条件：当前节点为空



之后判断当前节点是否存在左节点（因为需要做的就是将左子树插入），如果左子树不存在，就可以认为此时位于最左边的节点，也就是此时这一支已经满足了单链表要求；然后就可以对右子树进行遍历，当到达右子树最后一个结点之后，就把父节点的整颗右子树挂在当前节点的右枝，再将根节点的左子树完整的移动到右子树，左子树置空即可



```cpp

void flatten(TreeNode\* root)

&nbsp;   {

&nbsp;       while(root)

&nbsp;       {

&nbsp;           if(root->left)

&nbsp;           {

&nbsp;               auto temp = root->left;

&nbsp;               while(temp->right) temp = temp->right;

&nbsp;               temp->right = root->right;

&nbsp;               root->right = root->left;

&nbsp;               root->left = nullptr;

&nbsp;           }

&nbsp;           root = root->right;

&nbsp;       }

&nbsp;   }

```



\#### <font style="color:#DF2A3F;">第二百三十题</font>：\[二叉搜索树中第 K 小的元素](https://leetcode.cn/problems/kth-smallest-element-in-a-bst/)

第一次的解法是通过中序遍历将树存入vector，再通过下标k直接访问元素，但是超时了......应该是vector每次扩容的开销太大了



下面直接分析代码：



对于这段程序，只需要执行到第k个元素就可以停止了，后面的没必要去遍历，所以这里通过k来决定退出条件。



首先遍历左子树（这里使用的还是中序遍历）， 一直到叶子节点的下一个空节点，如果在这个过程中，k已经被减为了零，那么当前节点就是我们需要找的节点；反之，如果左子树已经遍历完毕，而k不为零，就回到父节点，再在父节点处执行一次--k的判断。最后，如果根节点和它的左子树的遍历完毕后，k还是没有为零，就开始遍历整颗右子树



```cpp

int kthSmallest(TreeNode\* root, int\& k)

{

&nbsp;   if(!root) return -1;



&nbsp;   int res\_left = kthSmallest(root->left, k);

&nbsp;   if(res\_left != -1) return res\_left;



&nbsp;   if(--k == 0) return root->val;



&nbsp;   return kthSmallest(root->right, k);

}

```







\#### <font style="color:#DF2A3F;">第二百三十六题</font>：\[<font style="color:rgb(10, 132, 255);">二叉树的最近公共祖先</font>](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/)

\*\*思路：\*\*



因为需要从下往上进行遍历，所以采用的是后序遍历（左右中），这样就可以让中间节点拿到左右子树的信息，从而\*\*判断自身是否为公共祖先\*\*——如果子树没有搜索到目标节点，会返回空指针；只有<u>当左右子树的返回值都不为空时，才可以判断当前节点为公共祖先</u>



\*\*具体实现：\*\*



首先定义递归结束的条件——当前节点为空，或当前节点就是需要进行查找的节点



之后就开始对左右子树进行递归遍历，当目标节点存在于左右子树中时，就直接返回当前节点（理由如上）；当只有左子树找到目标节点而右子树没有搜索到时，就返回左节点（因为此时两个目标值都位于左子树中）；只有右子树搜索到时同理



```cpp

TreeNode\* traversal(TreeNode\* root, TreeNode\* p, TreeNode\* q)

{

&nbsp;   if(!root) return nullptr;

&nbsp;   if(root == p || root == q) return root;



&nbsp;   TreeNode\* left = traversal(root->left, p, q);

&nbsp;   TreeNode\* right = traversal(root->right, p, q);



&nbsp;   if(left \&\& right) return root;

&nbsp;   else if(left \&\& !right) return left;

&nbsp;   else if(!left \&\& right) return right;

&nbsp;   else return nullptr;

}



TreeNode\* lowestCommonAncestor(TreeNode\* root, TreeNode\* p, TreeNode\* q)

{

&nbsp;   return traversal(root, p, q);

}

```







\#### <font style="color:#DF2A3F;">第四百三十七题</font>：\[路径总和 III](https://leetcode.cn/problems/path-sum-iii/)

使用到了<font style="background-color:#FBDE28;">深搜和层序遍历</font>



注：此处并非最优解，但是我不想再看其他解法了....



更好的答案参见这里吧\[437. 路径总和 III - 力扣（LeetCode）](https://leetcode.cn/problems/path-sum-iii/solutions/2784856/zuo-fa-he-560-ti-shi-yi-yang-de-pythonja-fmzo/?envType=study-plan-v2\&envId=top-100-liked)



\*\*思路：\*\*



简单来说，就是通过层序遍历，从每一个节点出发，进行一次深度优先搜索，并在搜索过程中不断地将当前总和与目标和进行比较，若相等则将路径数量加一



\*\*具体实现：\*\*



dfs函数：从传入的节点出发，先将当前值加到当前总和上去，然后与目标值进行比较；接着递归深入左子树和右子树（需要传入当前总和），之后左右子树又会进行相同的判断



pathSum函数：定义队列，按照层序遍历的顺序每次访问一个节点，并调用dfs函数



```cpp

int pathSum(TreeNode\* root, int targetSum)

{

&nbsp;   if(!root) return 0;

&nbsp;   std::queue<TreeNode\*> q;

&nbsp;   q.push(root);

&nbsp;   int total = 0;

&nbsp;   while(!q.empty())

&nbsp;   {

&nbsp;       TreeNode\* curr = q.front();

&nbsp;       q.pop();

&nbsp;       total += dfs(curr, 0, targetSum);



&nbsp;       if(curr)

&nbsp;       {

&nbsp;           q.push(curr->left);

&nbsp;           q.push(curr->right); 

&nbsp;       }

&nbsp;   }   

&nbsp;   return total;

}

int dfs(TreeNode\* curr, long long curr\_sum, int targetSum)

{

&nbsp;   if(!curr) return 0;

&nbsp;   curr\_sum += curr->val;

&nbsp;   int count = 0;

&nbsp;   if(curr\_sum == targetSum) count++;



&nbsp;   count += dfs(curr->left, curr\_sum, targetSum);

&nbsp;   count += dfs(curr->right, curr\_sum, targetSum);



&nbsp;   return count;

}

```



