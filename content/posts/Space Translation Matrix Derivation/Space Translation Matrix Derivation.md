\## <font style="color:#DF2A3F;">空间变换的过程</font>：

\*\*模型/局部空间（Model/Local Space）    --> \*\*



\*\*世界空间（World Space）                       --> \*\*



\*\*观察/摄像机空间（View/Camera Space）--> \*\*



\*\*齐次裁剪空间（Clip Space）                     --> \*\*



\*\*标准设备坐标空间（NDC Space）             --> \*\*



\*\*屏幕空间（Screen Space）\*\*



\*\*\*\*



\### <font style="color:#117CEE;">1 . 模型空间（Model Space） --> 世界空间（World Space）</font>

a .<u> 模型空间中的点</u> 乘上 <u>模型矩阵</u> 即可变换到 <u>世界空间</u> ————\*\* \*\*\_\*\*P\*\*\_<sub>\_\*\*World \*\*\_</sub>\_\*\*= M\*\*\_<sub>\_\*\*Model\*\*\_</sub>\_\*\* \* P\*\*\_<sub>\_\*\*Model\*\*\_</sub>



\*\*\*\*



b . $ M\_{model} = M\_{translation} \\cdot M\_{rotation} \\cdot M\_{scaling} $



其中，S是\*\*缩放矩阵（Scaling Matrix）\*\*，R是\*\*旋转矩阵（Rotation Matrix）\*\*，T是\*\*平移矩阵	       	 （Translation Matrix）\*\*



坐标的变换必须严格按照“\*\*先缩放，后旋转，再平移\*\*”的顺序进行



\*\*i. 缩放矩阵 (Scaling Matrix) \*\* ：



$ M\_{scaling} = \\begin{bmatrix} 

s\_x \& 0 \& 0 \& 0 \\\\ 

0 \& s\_y \& 0 \& 0 \\\\ 

0 \& 0 \& s\_z \& 0 \\\\ 

0 \& 0 \& 0 \& 1 

\\end{bmatrix} $



&nbsp;   \*\*   ii. 旋转矩阵 (Rotation Matrix)\*\*  ：



$ 绕 X 轴旋转 \\theta：R\_x(\\theta) = \\begin{bmatrix} 

1 \& 0 \& 0 \& 0 \\\\ 

0 \& \\cos\\theta \& -\\sin\\theta \& 0 \\\\ 

0 \& \\sin\\theta \& \\cos\\theta \& 0 \\\\ 

0 \& 0 \& 0 \& 1 

\\end{bmatrix} $



$ 绕 Y 轴旋转 \\theta：R\_y(\\theta) = \\begin{bmatrix} 

\\cos\\theta \& 0 \& \\sin\\theta \& 0 \\\\ 

0 \& 1 \& 0 \& 0 \\\\ 

-\\sin\\theta \& 0 \& \\cos\\theta \& 0 \\\\ 

0 \& 0 \& 0 \& 1 

\\end{bmatrix} $

---
title: "MVP矩阵推导"
date: 2026-04-27
description: "图形渲染管线的顶点处理阶段使用到的三个矩阵"
categories: ["图形学"]
draft: false
TocOpen: true  # 这篇文章的目录默认保持展开
---

$ 绕 Z 轴旋转 \\theta：R\_z(\\theta) = \\begin{bmatrix} 

\\cos\\theta \& -\\sin\\theta \& 0 \& 0 \\\\ 

\\sin\\theta \& \\cos\\theta \& 0 \& 0 \\\\ 

0 \& 0 \& 1 \& 0 \\\\ 

0 \& 0 \& 0 \& 1 

\\end{bmatrix} $



\*\*  iii. 平移矩阵 (Translation Matrix)  \*\*：



$ M\_{translation} = \\begin{bmatrix} 

1 \& 0 \& 0 \& t\_x \\\\ 

0 \& 1 \& 0 \& t\_y \\\\ 

0 \& 0 \& 1 \& t\_z \\\\ 

0 \& 0 \& 0 \& 1 

\\end{bmatrix} $







c . $ M\_{model} = M\_{translation} \\cdot M\_{rotation} \\cdot M\_{scaling} = \\begin{bmatrix} 

R\_{11} \\cdot s\_x \& R\_{12} \\cdot s\_y \& R\_{13} \\cdot s\_z \& t\_x \\\\ 

R\_{21} \\cdot s\_x \& R\_{22} \\cdot s\_y \& R\_{23} \\cdot s\_z \& t\_y \\\\ 

R\_{31} \\cdot s\_x \& R\_{32} \\cdot s\_y \& R\_{33} \\cdot s\_z \& t\_z \\\\ 

0 \& 0 \& 0 \& 1 

\\end{bmatrix} $







\###   

<font style="color:#117CEE;">2 . 世界空间（World Space） --> 观察/摄像机空间</font>\*\*<font style="color:#117CEE;">（View/Camera Space）</font>\*\*

a .<u> 世界空间中的点</u> 乘上 <u>观察矩阵</u> 即可变换到观察空间 ———— \_\*\*P\*\*\_<sub>\_\*\*view \*\*\_</sub>\_\*\*= M\*\*\_<sub>\_\*\*view\*\*\_</sub>\_\*\* \* P\*\*\_<sub>\_\*\*world\*\*\_</sub>



b .$ M\_{view} = R\_{view} \\cdot T\_{view} $







