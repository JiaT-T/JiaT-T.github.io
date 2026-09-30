---
title: "GAMES101 作业 2：三角形光栅化"
slug: "games101-assignment-2"
summary: "记录三角形内部判断、包围盒遍历、重心坐标与深度测试的光栅化实现。"
categories: ["图形学"]
tags: ["Computer Graphics", "GAMES101", "Rasterization", "C++"]
date: "2026-03-19T06:55:49.000Z"
lastmod: "2026-03-19T07:15:54.000Z"
draft: false
yuque_slug: "kac10rzqpbkt848b"
source: "https://www.yuque.com/u62694975/iaaa/kac10rzqpbkt848b"
---

<a id="ub85a0e3e"></a>作业2 是实现三角形的光栅化 ：

<a id="u3e8992d0"></a>需要修改的函数如下：

<a id="uc2797063"></a>• rasterize\_triangle(): 执行三角形栅格化算法

<a id="ue5a6e242"></a>• static bool insideTriangle(): 测试点是否在三角形内

<a id="u2e083394"></a>首先判断点是否在三角形内部

<a id="u65f687a1"></a>通过<strong>计算重心坐标</strong>，得到alpha，beta，gamma的值，将其与零进行比较，如果其中存在一个值小于零，那么就可以判断此点不在三角形之内，之后就只需要对内部的点进行深度测试与颜色赋值

<a id="u86152720"></a><strong>数学原理：</strong>重心坐标计算出来的三个值实际上是任意一点对三角形的三个顶点的权重，而位于三角形内的点，其权重必然大于等于零

<a id="XZu0r"></a>
insideTriangle（）
```cpp
static bool insideTriangle(float x, float y, const Vector3f* _v)
{   
    // TODO : Implement this function to check if the point (x, y) is inside the triangle represented by _v[0], _v[1], _v[2]

    auto bar = computeBarycentric2D(x, y, _v);
    if (std::get<0>(bar) < 0 || std::get<1>(bar) < 0 || std::get<2>(bar) < 0)
        return false;
    return true;
}
```

<a id="u4849cca0"></a>光栅化在rasterize\_triangle()函数内进行，在这个函数中需要执行是否在内部的判断以及深度测试（extra：双重采样）

<a id="u00f9df60"></a>这里使用的是包围盒算法——找出恰好能够将三角形包围在内的包围盒，之后就只需要在这和盒子内进行每一个像素点的遍历，而不是遍历整个画面

<a id="dWCOK"></a>
rasterize\_triangle（）
```cpp
void rst::rasterizer::rasterize_triangle(const Triangle& t) {
    auto v = t.toVector4();

    // TODO : Find out the bounding box of current triangle.
    // iterate through the pixel and find if the current pixel is inside the triangle

    // Create Bounding Box
    float X_max = (std::max(std::max(v[0].x(), v[1].x()), v[2].x()));
    float X_min = (std::min(std::min(v[0].x(), v[1].x()), v[2].x()));
    float Y_max = (std::max(std::max(v[0].y(), v[1].y()), v[2].y()));
    float Y_min = (std::min(std::min(v[0].y(), v[1].y()), v[2].y()));

    for (int x = X_min; x <= X_max; x++)
        {
            for (int y = Y_min; y < Y_max; y++)
                {
                    if (insideTriangle(x, y, t.v))
                    {
                        auto[alpha, beta, gamma] = computeBarycentric2D(x, y, t.v);
                        float w_reciprocal = 1.0/(alpha / v[0].w() + beta / v[1].w() + gamma / v[2].w());
                        float z_interpolated = alpha * v[0].z() / v[0].w() + beta * v[1].z() / v[1].w() + gamma * v[2].z() / v[2].w();
                        z_interpolated *= w_reciprocal;

                        if (z_interpolated < depth_buf[get_index(x, y)])
                        {
                            depth_buf[get_index(x, y)] = z_interpolated;
                            Vector3f point = { (float)x,(float)y, z_interpolated }, color = t.getColor();
                            set_pixel(point, color);
                        }
                    }
                }
        }
}
```

原文：[2](<https://www.yuque.com/u62694975/iaaa/kac10rzqpbkt848b>)
