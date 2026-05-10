\### <font style="color:#117CEE;">一：Linear Blending</font>

代码实现：



```cpp

float3 normal\_1 = tex2D(normal\_tex1, uv).xyz \* 2.0f - 1.0f;

float3 normal\_2 = tex2D(normal\_tex2, uv).xyz \* 2.0f - 1.0f;

float3 n = normalize(normal\_1 + normal\_2);

```



这是一种非常暴力的方法，实现起来也是最简单的（相加后再归一化即可）；虽然最终可以实现混合法线贴图的效果，但是会导致\*\*混合后的法线变平，细节也就会更加模糊\*\*



产生这种结果的原因有两个，可以分别从\*\*几何维度与物理维度\*\*的方向来分析：  

<font style="background-color:#F1A2AB;">1.几何维度：</font>



法线本质上是定义在球面上的向量，当我们使用线性的公式对两个法线向量进行混合时，计算的路径实际上是沿着“弦”而非“弧”进行的；这会导致\*\*两个法线向量相加得到的中间向量的模始终小于 1\*\*，虽然可以通过normalize 将模长拉回至 1，但这又会使得“\*\* 角速度非均匀\*\*  ”，表现在混合后的法线上就是：<u>混合结果在中间部分的变化比两端更慢，并且高频的法线会在这种非线性的映射中被抹平</u>，产生“\*\*细节模糊\*\*”；细节模糊的另一个原因是——当两个法线的方向差异过大（接近180度，也就是反向）时，这样的<u>线性混合得到的结果会趋近于垂直向上，丢失了原有的细节</u>



<font style="background-color:#F1A2AB;">2.物理维度：</font>



法线贴图存储的并不是颜色，而是物体表面的偏导数（斜率），如果使用处理颜色的办法去混合两个法线，\*\*只会导致数据的平均，而不是细节的叠加\*\*



\_e.g. 有两张法线贴图，一张代表“砖块的粗糙纹理”，另一张代表“划痕”，线性混合的行为逻辑是：“我有 50% 像砖块，50% 像划痕”， 但真实的逻辑应该是：“在砖块的斜率基础上，叠加划痕的斜率”\_



---



---

title: "如何混合法线贴图"

date: 2026-05-10

categories: \["图形学"]

draft: false

TocOpen: true  # 这篇文章的目录默认保持展开

---



代码实现：



```cpp

float3 normal\_1 = tex2D(normal\_tex1, uv).xyz \* 2.0f - 1.0f;

float3 normal\_2 = tex2D(normal\_tex2, uv).xyz \* 2.0f - 1.0f;

float3 n  = normal\_1 < 0.5 ? 2 \* normal\_1 \* normal\_2 : 1 – 2 \* (1 - normal\_1) \* (1 - normal\_2);

n = normalize(n \* 2 - 1);

```



相比于线性混合，Overlay Blending 是对两张法线贴图进行了类似 PS 中“正片叠底”的处理，虽然 overlay 对于增强二维图像的对比度又很好的效果，但是法线贴图本身并不应该被当作颜色贴图进行处理；overlay 并不理解法线贴图存储的是斜率信息，因此他会对x、y、z分量无差别地进行非线性缩放，这会导致严重的数学错误与视觉伪影



---



\### <font style="color:#117CEE;">三：Partical Derivative Blending</font>

代码实现：



```cpp

float3 normal\_1 = tex2D(texBase, uv).xyz\*2 - 1;

float3 normal\_2 = tex2D(texDetail, uv).xyz\*2 - 1;

float2 pd = normal\_1.xy/normal\_1.z + normal\_2.xy/normal\_2.z; //Add the PDs

float3 n  = normalize(float3(pd, 1));

```



根据导数的线性性质：



$ \\frac{\\partial F\_{total}}{\\partial x} = \\frac{\\partial f\_1}{\\partial x} + \\frac{\\partial f\_2}{\\partial x} $



可以得知要想混合两个法线，需要\*\*对它们在切空间中对应的表面梯度进行线性累加，然后将合成后的梯度重新投影回法线空间\*\*



虽然这在数学上的定义是完美的，但实际的应用会涉及到两次除法以及一次 normalize，开销比较大，所以在离实时渲染中一般不会直接使用这个方法，但是在离线渲染中，由于编译器的优化，这几步对于整个的渲染流程的性能的影响微乎其微，所以用它可以得到非常好的混合法线质量



