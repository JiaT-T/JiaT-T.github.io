---
title: "GAMES101 作业 5：基础光线追踪"
slug: "games101-assignment-5"
summary: "整理从像素坐标生成相机光线的空间变换流程，以及三角形求交的基础实现。"
categories: ["图形学"]
tags: ["Computer Graphics", "GAMES101", "Ray Tracing", "C++"]
date: "2026-03-26T07:38:19.000Z"
lastmod: "2026-03-26T08:38:15.000Z"
draft: false
yuque_slug: "vcqo0i8o7smmgqv7"
source: "https://www.yuque.com/u62694975/iaaa/vcqo0i8o7smmgqv7"
---

<a id="uc877e585"></a>作业五是实现基础的光线追踪（光线生成与三角形求交）

<a id="u5e86f53b"></a><strong>1.光线生成</strong>：

<a id="ue993f029"></a><strong>目标</strong>：<u>将屏幕上（不是屏幕空间！）的2D像素坐标映射为3D世界的一条线</u>

<a id="u0cfa036c"></a>需要将像素从光栅空间-&gt;NDC空间-&gt;屏幕空间-&gt;相机空间-&gt;世界空间

<a id="ud3ad629e"></a><span style="color: #117CEE">（1）<strong>\*光栅空间-&gt;NDC空间</strong>\*</span>

<a id="u72970652"></a>拿到像素的左上角顶点坐标，加0.5得到像素中心坐标， 之后将x，y分别除以width，height，映射到【0，1】区间内

<a id="u4ee523c7"></a>即：<strong>（x + 0.5f) / width;  (y + 0.5f) / height</strong>;

<a id="u9a94e26a"></a><span style="color: #117CEE">（2）<strong>\*NDC空间-&gt;屏幕空间</strong>\*</span>

<a id="u16e5b4d5"></a>将坐标从【0，1】映射到【-1，1】区间，

<a id="u56a27bac"></a>即：<strong>x = 2 \* x - 1； y = 1 - 2 \* y</strong>;

<a id="uc99aec9e"></a>注：在光栅空间中，y轴向下；而屏幕空间的y轴向上，因此需要用1-...

<a id="u09567c9f"></a><span style="color: #117CEE">（3）<strong>\*屏幕空间-&gt;相机空间</strong>\*</span>

<a id="u83eae7d1"></a>这里需要引入相机的物理属性 （宽高比和视场角）  ，将2D坐标拉伸为3D的相机坐标

<a id="u14e79381"></a>屏幕空间的【-1，1】区间是一个正方形（因为x，y都处于这个区间中），但是屏幕大多是长方形的（如1920x1080），因此需要对x坐标进行拉伸；同时还要根据xy原始的大小对其进行放大

<a id="u30bc8e91"></a>即：<strong> x = x \* radio \* sacle;   y = y \* scale</strong>;

<a id="u5213c641"></a><span style="color: #117CEE">（4）<strong>\*相机空间-&gt;世界空间</strong>\*</span>

<a id="uebae53d9"></a>将上一步得到的坐标（x，y，-1）乘以 世界到相机的旋转矩阵的逆矩阵，即可求得在世界空间的坐标

<a id="ued00cee1"></a>但是因为这里的相机位于原点处，且方向看向-z，因此不需要做任何处理

<a id="udebcb026"></a>之后调用castRay（）函数就可得到这一像素在世界空间发出的光线

<a id="owJVr"></a>
loop
```cpp
for (int j = 0; j < scene.height; ++j)
    {
        for (int i = 0; i < scene.width; ++i)
            {
                // generate primary ray direction
                float x = i;
                float y = j;
                // TODO: Find the x and y positions of the current pixel to get the direction
                // vector that passes through it.
                // Also, don't forget to multiply both of them with the variable *scale*, and
                // x (horizontal) variable with the *imageAspectRatio*

                // Rasterized Space -> NDC Space
                float x_ndc = (x + 0.5f) / scene.width;
                float y_ndc = (y + 0.5f) / scene.height;

                // NDC Space -> Screen Space
                float x_screen = 2 * x_ndc - 1;
                float y_screen = 1 - y_ndc * 2;

                // Screen Space -> Camera Space
                float x_camera = x_screen * imageAspectRatio * scale;
                float y_camera = y_screen * scale;

                // camera Space -> World Space
                Vector3f dir = Vector3f(x_camera, y_camera, -1); // Don't forget to normalize this direction!
                dir = normalize(dir);
                framebuffer[m++] = castRay(eye_pos, dir, scene, 0);
            }
```

<a id="u94465045"></a><strong>2.光线与三角形求交</strong>：

<a id="u10500e52"></a>使用的是 <span style="background-color: #FBDE28">Möller-Trumbore 算法</span> ：

<ul data-yuque-indent="2" style="margin-left: 4em"><li id="uf2799d8f"><span id="ub591632c">射线方程：P = O + t*D</span></li><li id="uffe0c747"><span id="u279d570e">三角形内部点：P = V_0 + u*E_1 + vE*_2</span></li></ul>

<a id="ube59fe9c"></a>联立可得到线性方程组：

<a id="u0981569a"></a><a id="u9d60b30f"></a><img src="/images/games101-assignment-5/games101-assignment-5-01.png" alt="" loading="lazy" width="206" height="88" style="max-width: 100%; height: auto">

<a id="u09550c9b"></a>之后可以解得t,u,v的值，u，v是 三角形内部的重心坐标  ，t（tNear）是光线撞上三角形所用的最短的时间

<a id="u8f731192"></a>判断条件：(u，v&lt; 0)或(u + v &gt;1)则交点位于三角形之外，t&lt;0则说明三角形在光线后面，这三种情况都意味着光线未能与三角形相交

<a id="s0wg9"></a>
rayTriangleIntersect（）
```cpp
bool rayTriangleIntersect(const Vector3f& v0, const Vector3f& v1, const Vector3f& v2, const Vector3f& orig,
const Vector3f& dir, float& tnear, float& u, float& v)
{
    // TODO: Implement this function that tests whether the triangle
    // that's specified bt v0, v1 and v2 intersects with the ray (whose
    // origin is *orig* and direction is *dir*)
    // Also don't forget to update tnear, u and v.
    Vector3f e1 = v1 - v0, e2 = v2 - v0, s = orig - v0;
    Vector3f s1 = crossProduct(dir, e2);

    float S1dotE1 = dotProduct(s1, e1);
    if (std::abs(S1dotE1) < 0.0001f) return false;
    float invS1dotE1 = 1 / S1dotE1;

    u     = dotProduct(s1, s) * invS1dotE1;
    if (u < 0.0f || u > 1.0f) return false;

    Vector3f s2 = crossProduct(s, e1);
    v     = dotProduct(s2, dir) * invS1dotE1;
    if (v < 0.0f || v > 1.0f) return false;

    tnear = dotProduct(s2, e2) * invS1dotE1;
    if (tnear >= .0f) return true;

    return false;
}
```

<a id="u55af10da"></a>附：结果图------

<a id="u7324c1a6"></a><a id="u39c14c8d"></a><img src="/images/games101-assignment-5/games101-assignment-5-02.png" alt="" loading="lazy" style="max-width: 100%; height: auto">

原文：[5](<https://www.yuque.com/u62694975/iaaa/vcqo0i8o7smmgqv7>)
