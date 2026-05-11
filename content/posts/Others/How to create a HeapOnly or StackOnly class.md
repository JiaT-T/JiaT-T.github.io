---
title: "如何构造只能在堆/栈上创建对象的类"
date: 2026-05-10
categories: ["C++", "编程基础"]
tags: ["Modern C++", "RAII", "Memory Management"]
draft: false
TocOpen: true  # 这篇文章的目录默认保持展开
---
**核心思想：****<font style="background-color:#FBDE28;">阻止栈资源的释放</font>**

当编译器在栈上分配资源时，必须确保其能够在离开作用域时通过调用析构函数被释放。如果人为指定析构函数不可见，那么编译器就会报错，从而阻止了栈上的资源分配。也就是说，需要**<u>破坏编译器在在栈上自动管理生命周期的能力</u>**：

**private ：**

**HeapOnly() = default;**

此时类对象位于堆上，需要通过指针进行管理，因此在类中定义一个“静态工厂函数”：	

**static std::unique_ptr<HeapOnly> create(){ return std::unique_ptr<HeapOnly>(new HeapOnly()); }**

****

### <font style="color:#117CEE;">二：只能在栈上创建对象的类</font>
**核心思想：禁止一切形式的 new 操作**

当我们在外部使用“new T（）”创建类对象时，编译器会在类或全局作用域下寻找 new 的重载，如果将 new 标记为 delete，就能从源头切断堆上的分配：

// 禁止**单个对象**的堆分配

**void* operatornew(std::size_t)= delete;**

**voidoperatordelete(void*)= delete;**

// 禁止**数组形式**的堆分配

**void* operatornew[](std::size_t) = delete;**

**voidoperatordelete[](void*) = delete;**

			
