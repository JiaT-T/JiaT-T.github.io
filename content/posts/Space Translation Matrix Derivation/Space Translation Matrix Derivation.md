## <font style="color:#DF2A3F;">空间变换的过程</font>：
**模型/局部空间（Model/Local Space）    --> **

**世界空间（World Space）                       --> **

**观察/摄像机空间（View/Camera Space）--> **

**齐次裁剪空间（Clip Space）                     --> **

**标准设备坐标空间（NDC Space）             --> **

**屏幕空间（Screen Space）**

****

### <font style="color:#117CEE;">1 . 模型空间（Model Space） --> 世界空间（World Space）</font>
a .<u> 模型空间中的点</u> 乘上 <u>模型矩阵</u> 即可变换到 <u>世界空间</u> ————** **_**P**_<sub>_**World **_</sub>_**= M**_<sub>_**Model**_</sub>_** * P**_<sub>_**Model**_</sub>

****

b . $ M_{model} = M_{translation} \cdot M_{rotation} \cdot M_{scaling} $

其中，S是**缩放矩阵（Scaling Matrix）**，R是**旋转矩阵（Rotation Matrix）**，T是**平移矩阵	       	 （Translation Matrix）**

坐标的变换必须严格按照“**先缩放，后旋转，再平移**”的顺序进行

**i. 缩放矩阵 (Scaling Matrix) ** ：

$ M_{scaling} = \begin{bmatrix} 
s_x & 0 & 0 & 0 \\ 
0 & s_y & 0 & 0 \\ 
0 & 0 & s_z & 0 \\ 
0 & 0 & 0 & 1 
\end{bmatrix} $

    **   ii. 旋转矩阵 (Rotation Matrix)**  ：

$ 绕 X 轴旋转 \theta：R_x(\theta) = \begin{bmatrix} 
1 & 0 & 0 & 0 \\ 
0 & \cos\theta & -\sin\theta & 0 \\ 
0 & \sin\theta & \cos\theta & 0 \\ 
0 & 0 & 0 & 1 
\end{bmatrix} $

$ 绕 Y 轴旋转 \theta：R_y(\theta) = \begin{bmatrix} 
\cos\theta & 0 & \sin\theta & 0 \\ 
0 & 1 & 0 & 0 \\ 
-\sin\theta & 0 & \cos\theta & 0 \\ 
0 & 0 & 0 & 1 
\end{bmatrix} $

$ 绕 Z 轴旋转 \theta：R_z(\theta) = \begin{bmatrix} 
\cos\theta & -\sin\theta & 0 & 0 \\ 
\sin\theta & \cos\theta & 0 & 0 \\ 
0 & 0 & 1 & 0 \\ 
0 & 0 & 0 & 1 
\end{bmatrix} $

**  iii. 平移矩阵 (Translation Matrix)  **：

$ M_{translation} = \begin{bmatrix} 
1 & 0 & 0 & t_x \\ 
0 & 1 & 0 & t_y \\ 
0 & 0 & 1 & t_z \\ 
0 & 0 & 0 & 1 
\end{bmatrix} $



c . $ M_{model} = M_{translation} \cdot M_{rotation} \cdot M_{scaling} = \begin{bmatrix} 
R_{11} \cdot s_x & R_{12} \cdot s_y & R_{13} \cdot s_z & t_x \\ 
R_{21} \cdot s_x & R_{22} \cdot s_y & R_{23} \cdot s_z & t_y \\ 
R_{31} \cdot s_x & R_{32} \cdot s_y & R_{33} \cdot s_z & t_z \\ 
0 & 0 & 0 & 1 
\end{bmatrix} $



###   
<font style="color:#117CEE;">2 . 世界空间（World Space） --> 观察/摄像机空间</font>**<font style="color:#117CEE;">（View/Camera Space）</font>**
a .<u> 世界空间中的点</u> 乘上 <u>观察矩阵</u> 即可变换到观察空间 ———— _**P**_<sub>_**view **_</sub>_**= M**_<sub>_**view**_</sub>_** * P**_<sub>_**world**_</sub>

b .$ M_{view} = R_{view} \cdot T_{view} $


