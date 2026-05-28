+++
date = '2026-05-20T00:00:00+08:00'
draft = false
title = 'Design Modes'
summary = '整理单例模式与工厂模式的基础定义、实现方式和常见问题。'
tags = ['Design Patterns', 'C++', 'Technical Notes']
+++

## 一：单例模式
定义：一个类在全局只有一个实例对象，这个类自行实例化后向整个系统提供这个实例

实现：**禁止拷贝与赋值**，防止破坏实例的唯一性

缺点：全局状态强，调试困难

---

1. **懒汉式单例模式：**

```cpp
class Singleton
{
public:
    // 在第一次调用 getSingleton() 才初始化
	static Singleton* getSingleton()
	{
		// 局部静态变量
		// 在程序结束后自动释放内存
		// 防止内存泄漏
        // 同时也确保了线程安全
		static Singleton instance;
		return &instance;
	}

private:
	Singleton() {}
	~Singleton() {}
	Singleton(const Singleton&);
	Singleton& operator=(const Singleton&);
};
```

2. **饿汉式单例模式：**

```cpp
class Singleton
{
public:
    static Singleton* getSingleton()
    {
        return &instance;
    }

private:
    Singleton() {}
    ~Singleton() {}
    Singleton(const Singleton&);
    Singleton& operator=(const Singleton&);

    // 饿汉式的实例是定义在类外的
    // 在 main() 之前进行初始化
    static Singleton instance;
};
```

**常见问题：**

> _为什么不直接使用全局变量？_
>

因为使用单例可以控制初始化时机（static 变量在第一次调用时才被初始化），并且单例可以对接口进行封装

## 二：工厂模式
定义：
