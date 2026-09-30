---
title: "GAMES101 作业 4：Bézier 曲线"
slug: "games101-assignment-4"
summary: "记录 De Casteljau 递归插值绘制 Bézier 曲线的方法，以及采样步长与曲线绘制代码。"
categories: ["图形学"]
tags: ["Computer Graphics", "GAMES101", "Bezier Curve", "C++"]
date: "2026-03-22T06:46:41.000Z"
lastmod: "2026-03-22T08:31:25.000Z"
draft: false
yuque_slug: "fwq5chksbcy7lq6v"
source: "https://www.yuque.com/u62694975/iaaa/fwq5chksbcy7lq6v"
---

<a id="ub54d6ca4"></a>作业4是使用 De Casteljau 算法实现 Bézier 曲线

<a id="ufd84c3a2"></a>De Casteljau 算法的核心是递归，使用递归，通过输入的多个顶点计算出连续插值后的最后一个顶点

<a id="udbdaf44d"></a><strong>核心函数：</strong>

<a id="Cwmgo"></a>
recursive\_bezier（）
```cpp
cv::Point2f recursive_bezier(const std::vector<cv::Point2f> &control_points, float t) 
{
    // TODO: Implement de Casteljau's algorithm
    if (control_points.size() == 1) return control_points.front();

    std::vector<cv::Point2f> next_points;
    for (int i = 0; i < control_points.size() - 1; i++)
        {
            next_points.push_back(((1 - t) * control_points[i] + t * control_points[i + 1]));
        }
    
    return recursive_bezier(next_points, t);
}
```

<a id="u98cd4473"></a>在循环中计算当前顶点与下一顶点的插值点，并将其push\_back进要在下一层递归中使用的顶点组；每次递归都会使总顶点数减一，直到只剩最后一个顶点，将其作为返回值输出

<a id="FO82n"></a>
bezier（）
```cpp
void bezier(const std::vector<cv::Point2f> &control_points, cv::Mat &window) 
{
    // TODO: Iterate through all t = 0 to t = 1 with small steps, and call de Casteljau's 
    // recursive Bezier algorithm.
    for (double t = 0; t <= 1; t += 0.0001)
        {
            auto point = recursive_bezier(control_points, t);
            window.at<cv::Vec3b>(point.y, point.x)[1] = 255;
        }
}
```

<a id="u57126d26"></a>在这个函数中，通过对t值进行细微的调整，可以得到平滑的曲线效果（本质就是在两个点之间计算出大量的插值点）

<a id="u67091c20"></a>Extra：为曲线添加反走样

<a id="ub51d53bc"></a>我们在循环中所计算的坐标是有零1有整的，比如（10.2，15.8），但是程序会把它转换为距离最近的整数（10，16），这也是锯齿产生的原因

<a id="ELbVL"></a>
bezier（）
```cpp
void bezier(const std::vector<cv::Point2f> &control_points, cv::Mat &window) 
{
    // TODO: Iterate through all t = 0 to t = 1 with small steps, and call de Casteljau's 
    // recursive Bezier algorithm.

    for (double t = 0; t <= 1; t += 0.0001) 
        {
            int color = 0;
            auto point = recursive_bezier(control_points, t);
            int x = std::floor(point.x);
            int y = std::floor(point.y);

            std::vector<cv::Point2f> near_pixels
                {
                cv::Point2f(x + 1, y + 1), cv::Point2f(x + 1, y),
                cv::Point2f(x, y + 1), cv::Point2f(x, y)
                };
            for (const auto& near : near_pixels)
                {
                    int nx = static_cast<int>(near.x);
                    int ny = static_cast<int>(near.y);

                    if (nx < 0 || nx >= window.cols || ny < 0 || ny >= window.rows) continue;

                    float distance = std::sqrt((point.x - near.x) * (point.x - near.x) +
                    (point.y - near.y) * (point.y - near.y));

                    float weight = 1.0f - (distance / 1.414f);
                    int new_green = std::max(0, static_cast<int>(weight * 255.0f));

                    auto& pixel = window.at<cv::Vec3b>(ny, nx);
                    pixel[1] = std::max(static_cast<int>(pixel[1]), new_green);
                }
        }
}
```

<a id="ucdca8337"></a>有两种方法，一种是通过周围的点计算当前的颜色值，但是在这个循环中，这个方法有些麻烦

<a id="u882a1f85"></a>所以，另一种方法是使用当前点的颜色值，通过欧氏距离插值，赋予周围的点颜色

<a id="u725aa0ef"></a>流程：

<a id="u0a89b312"></a>1.先对当前坐标取整，并计算包围着当前的的四个点（2x2采样）

<a id="u77766fa0"></a>2.通过遍历，分别计算distance并赋予颜色值（取最大值）

原文：[4](<https://www.yuque.com/u62694975/iaaa/fwq5chksbcy7lq6v>)
