+++
date = '2026-05-20T00:00:00+08:00'
draft = false
title = 'Design Modes'
summary = '整理单例模式与工厂模式的基础定义、实现方式和常见问题。'
tags = ['Design Patterns', 'C++', 'Technical Notes']
+++

## 一：单例模式

定义：一个类在全局只有一个实例对象，这个类自行实例化后向整个系统提供这个实例。

实现：禁止拷贝与赋值，防止破坏实例的唯一性。

缺点：全局状态强，调试困难。

```cpp
class Logger {
public:
    static Logger& instance() {
        static Logger inst;
        return inst;
    }

    void log(const std::string& msg) {
        // ...
    }

private:
    Logger() = default;
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;
};
```

常见问题：

> _为什么不使用全局变量？_

因为使用单例可以控制初始化时机（static 变量在第一次调用时才被初始化），并且单例可以对接口进行封装。

## 二：工厂模式

定义：
