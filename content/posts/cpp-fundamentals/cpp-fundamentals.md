---
title: "Fundamentals of Cpp：现代 C++ 核心笔记"
date: 2026-04-19
description: "涵盖从 C++11 到 C++23 的核心特性，包含内存管理、RAII 及底层架构思考。"
categories: ["C++", "编程基础"]
tags: ["Modern C++", "RAII", "Memory Management"]
draft: false
TocOpen: true  # 这篇文章的目录默认保持展开
---

这里是整理的一些c++基础知识....

就这样吧....

---

# <font style="color:#DF2A3F;">语法------------------------------------------------------</font>
# 1.C++的三大特性
 封装，继承，多态（同时也是面向对象编程的三大特性）

## <font style="color:#117CEE;"> 1).简要解释一下上面三者</font>
·封装：隐藏内部具体的实现细节，对外部只暴露必要的接口来访问对象

·继承：允许一个类从另一个类继承属性和方法，从而实现代码复用和层次化抽象

 ·多态：同一个函数名拥有多种状态，或是同一个接口具有不同的行为

   ** LINK：**

[如何理解面向对象编程三大特性------封装、继承、多态](https://zhuanlan.zhihu.com/p/45445817)

##  <font style="color:#117CEE;">2).多态的类别</font>
·运行时多态（动态联编）：通过重载和模板实现

·编译时多态（静态联编）：通过继承和虚函数实现



# 2.虚函数
  简单来说，虚函数就是允许在基类（父类）中定义一个函数，并允许派生类（子类）对其进行**重写 (Override)**

## <font style="color:#117CEE;"> 1).虚函数的实现机制</font>
·通过虚函数表实现，虚函数表是一个由编译器生成的静态数组，位于类的全局静态内存区中，包含了一个类所有的虚函数的地址（即该类所有虚函数的入口）

·在类对象（不是类！）内存空间的头部，有一个虚函数表指针，它指向该类虚函数表的首地址

·当子类对象对父类虚函数进行重写的时候，虚函数表中相应的虚函数的地址会被更改为重写后的虚函数地址



##  <font style="color:#117CEE;">2).虚函数调用是在编译时确定还是运行时确定的？如何确定调用哪个函数？</font>
<font style="color:rgb(25, 27, 31);">·一般来说是在运行时确定，可以通过虚函数表中的地址来确定调用什么函数</font>

<font style="color:rgb(25, 27, 31);"></font>

## <font style="color:#117CEE;">3).能否在基类的构造函数和析构函数中调用虚函数？</font>
·在语法上来说没有问题，但是在实际调用时，无法实现多态的效果，因为构造函数会先初始化基类的成员，而此时子类的成员还是一片空白，如果这时使用子类中还未被初始化的成员，会出现错误；同理，析构函数是先从子类开始析构，如果在基类的析构函数中调用虚函数的话，因为此时子类已经被析构，是无法调用其特有成分的



## <font style="color:#117CEE;">4).当一个类需要被继承是，它的析构函数必须是虚函数</font>
如果基类的析构函数不为虚函数，那么当对派生类对象进行删除（delete）操作时，就只会调用基类的析构函数，这会导致内存泄漏；

而当基类包含虚析构函数时，在同样的情况下，编译器会先查询虚函数表，并调用对应的析构函数



# 3.C++的内存管理
## <font style="color:#117CEE;"> 1).C++有哪些内存区域</font>
·<u>栈</u>：由编译器自动分配与释放，多用于存储局部变量；速度极快，但空间有限（通常只有几MB）

·<u>堆</u>：需要手动控制生存周期， 从 `new` 或 `malloc` 开始，直到 `delete` 或 `free`；空间极大，分配位置不连续

·<u>全局/静态存储区</u>： 存储全局变量和静态变量，在程序启动时分配，程序退出时才释放  ；

**.data 段**：存储已初始化的全局/静态变量。

**.bss 段**：存储未初始化的全局/静态变量（自动初始化****为 0）。

·<u>常量存储区</u>： 存储只读数据  

·<u><font style="color:rgb(25, 27, 31);">自由存储区</font></u><font style="color:rgb(25, 27, 31);">：通过new和delete分配和释放空间的内存，具体实现可能是堆或者内存池</font>

·<u>代码区</u>：存储经过编译之后的机器指令（二进制代码）

**Link:**

[C++内存管理 - 还没放弃的老张 - 博客园](https://www.cnblogs.com/learning-zjx/p/10645659.html)



## <font style="color:#117CEE;"> 2).栈 与 堆 的区别</font>
1.堆的内存空间大，栈的内存空间小

2.堆的分配效率低，栈的分配效率高

3.分配和释放堆内存时会产生内存碎片，而栈不会

4.堆中的内存需要手动申请与释放，栈的内存由OS自动申请与释放

5.堆的地址从下往上，栈的地址从上往下



## <font style="color:#117CEE;">3).C++和C分别使用什么函数来做内存的分配和释放？有什么区别，能否混用？</font>
C++使用new/delete分配与释放内存，C使用malloc/free分配与释放内存

**区别：**

1.使用malloc分配内存时需要指定内存大小，而new不需要

2.malloc从堆中分配内存，new从自由存储区分配内存

3.对于类对象，new能够调用构造和析构函数，而malloc不行

4.使用new分配内存返回的是相应的类型指针，而malloc先返回的是void*，之后再强转为类型指针



## <font style="color:#117CEE;">4).什么是内存对齐？为什么要内存对齐？如何对齐？</font>
**含义：**内存对齐就是C++数据结构中的成员，其内存地址是否为对齐字节大小的倍数

**原因：**为了提高效率，计算机在内存中取数据时是按照一个固定长度的，比如在32位机上，计算机每次只取32位的数据，也就是4字节。如果不进行对齐，就有可能出现一个数据出现在两个地址上的情况，通过两次取出操作之后，还需要经过<font style="color:rgb(25, 27, 31);">掩码和移位等操作，效率极低；同时，也可能会造成内存浪费（产生了不必要的内存填充）</font>

**<font style="color:rgb(25, 27, 31);">做法</font>**<font style="color:rgb(25, 27, 31);">：申明成员变量时，字节对齐的数据依次申明，尽量将小数据成员放在一起，减少内存填充产生的浪费</font>



# 4.C++的类型转换
## <font style="color:#117CEE;"> 1).类型转换的种类</font>
1.**static_cast（最常用）**：隐式类型转换，用于转换C++内置的基本数据类型（enum, struct, int, float, double, char....)，但是不能进行无关类型的转换（如：非基类和子类）以及包含底层const的对象

2.**const_cast**：用于增加/去除const限定符，只能用于指针或引用

3.**dynamic_cast**：动态类型转换，主要用于将基类指针转换为派生类指针或引用的向下类型转换（也可以是向上类型转换)。如果指针转换失败则返回NULL，引用转换失败返回bad_cast异常。因为其在运行时会检查对象的虚表（安全性检查），因此基类中一定要存在虚函数，否则编译不通过

4.**reinterpret_cast**：重新解释转换，在编译期，将一段数据的二进制位转换成完全不同的类型，但是不改变其值，和C的强制转换差不多，可以将一个类型转换为其他任何想要的类型，比较不安全



## <font style="color:#117CEE;"> 2).static_cast与dynamic_cast的异同：</font>
<u>同</u>：两者都会进行类型安全检查

<u>异</u>：static_cast在编译期进行检查，dynamic_cast在运行期检查；

static_cast不需要基类拥有虚函数，dynamic_cast需要被转换对象的基类拥有虚函数



## <font style="color:#117CEE;">3).dynamic_cast的原理？如何自行实现？</font>
dynamic_cast是唯一一个在运行时进行类型检查的转换操作符，它的核心机制叫做RTTI（Run-Time Type information）

**<font style="background-color:#FBDE28;">PS：这里没写完，之后能看懂了再补上</font>**

**LINK：**

[[C++] - dynamic_cast介绍及工作原理、typeid、type_info_dynamiccast-CSDN博客](https://blog.csdn.net/zqxf123456789/article/details/106245816/)



# 5.C++的智能指针
智能指针是为了解决内存泄漏问题，它的本质是一个类，在函数结束时会自动调用析构函数并释放内存空间

## <font style="color:#117CEE;"> 1).类型：</font>
1.**unique_ptr(独占指针**）：在同一时间段，只能有一个智能指针指向对象，无法被拷贝，只能移动。内存开销极低

2.**shared_ptr(共享指针）**：多个共享指针可以指向同一个对象，采用引用计数的方法，当最后一个共享指针被销毁时才释放对象的内存空间。内存开销中等（因为既包含了指向数据的数据指针，又包含了指向用于计数的控制块的指针）

3.**weak_ptr(弱指针）**：通常与shared_ptr一起出现，用于解除两个shared_ptr互相引用时的死锁问题。内存开销低



## <font style="color:#117CEE;"> 2).shared_ptr的实现原理：</font>
**构造函数**：shared_ptr指向一个对象时，引用计数置1；同理，每当有一个shared_ptr被销毁时，引用计数--；

**拷贝构造函数**：每当有新的shared_ptr指向同一个对象时，引用计数++

**赋值运算符**：=左边的shared_ptr的引用计数减一，右边的则加一————e.g.ptr1 = ptr2，这意味着ptr1之前指向的控制块的引用计数减一，同时ptr2指向的控制块的引用计数加一；如果左边的引用计数减为0，则销毁所指向的对象，并释放内存空间



## <font style="color:#117CEE;"> 3).weak_ptr是如何解决shared_ptr的循环引用问题的：</font>
在shared_ptr的底层控制块中，其实存在着两个计数器：

+ `**shared_count**`_<font style="color:#117CEE;">：</font>_记录有多少个 `shared_ptr` 拥有该对象。当它变为 0，对象被析构
+ `**weak_count**`_<font style="color:#117CEE;">：</font>_记录有多少个 `weak_ptr` 观察该对象

 只有当两者同时变为 0 时，存储这些计数的“控制块”本身才会被释放  

回归正题，shared_ptr是“强占有”，只要它指向对象，引用计数就+1，对象就不能被销毁，而weak_ptr是“弱观察”，他也指向对象，但不会增加引用计数

**e.g.** A拥有B的shared_ptr，B拥有A的weak_ptr，此时指向A的最后一个shared_ptr被销毁，因为B占有的是weak_ptr，不会使A的引用计数加一，因此A的shared_count降为0，触发析构函数，这会导致存在于A中，指向B的shared_ptr也被析构，使得B的引用计数也降为0，B的析构函数也被调用，它内部的weak_ptr同样会被销毁，当最后一个weak_ptr也被销毁时，weak_count降为0，内存中的控制块才被释放



## <font style="color:#117CEE;">4).既然weak_ptr是为了解决shared_ptr的循环引用，那为什么不用raw ptr来解决这个问题：</font>
<font style="color:rgb(25, 27, 31);">如果使用了raw ptr，那么在它指向的shared_ptr被销毁之后，会出现 悬空指针 的情况；而weak_ptr会调用lock（）函数，如果所指向的shared_ptr被销毁，当再次使用weak_ptr时，lock（）函数会返回一个空的shared_ptr，其内部是nullptr</font>

<font style="color:rgb(25, 27, 31);"></font>

# 6.C++的说明符
## <font style="color:#117CEE;"> 1).类型：</font>
#### 1.const：
##### <font style="color:#117CEE;">（1）作用：</font>
用来定义常量，具有不可变性；

#####  <font style="color:#117CEE;">（2）什么是常量指针和指针常量：</font>
**<font style="background-color:#E7E9E8;">常量指针</font>**：指针指向的对象是常量，不可更改，但是指针的指向可以改变；

**<font style="background-color:#E7E9E8;">指针常量</font>**：指针本身是一个常量，其指向不可被更改，但是指向的对象可以被改变；

这里涉及到的是顶层const和底层const的概念：

顶层const：本身是cosnt类型

底层const：指向的对象是const类型

##### <font style="color:#117CEE;">  （3）const修饰的函数能否重载：</font>
const修饰的函数能够被重载。

const修饰的类成员函数既不能改变类的成员变量，也不能调用非const成员变量与非const成员函数，只能使用

const对象只能调用const成员函数，非cosnt对象可以调用所有成员函数

 非 const 对象优先选择非 const 函数以保留修改能力，而 const 对象则被严禁越权、仅能调用只读的 const 版本

####  2.static：
代表静态的意思，能够对变量与函数进行修饰

（1）当static作用于**文件作用域**时，该变量或函数只在本文件可见，其他文件既看不到也无法使用，避免了重定义的问题

（2）当static作用于**函数作用域**时，即作为局部静态变量时，只会在第一次调用函数的时候初始化，也只在该函数内可见

（3）当static用于**类的申明**时，即静态数据成员和静态成员函数，意味着类中的这些成员是所有类对象共有的

##### <font style="color:#117CEE;">·static变量什么时候初始化：</font>
static在类中申明时不占用内存，只有在第一次执行到该变量的声明处才进行初始化



文件域的静态变量和类的静态成员变量在main函数执行之前的静态初始化过程中分配内存并初始化，局部静态变量在第一次使用时分配内存并初始化



#### 3.constexpr：
告诉编译器，在编译阶段就能够确定该常量的值，需要直接得出结果，并将其硬编码进入程序中



#### 4.extern：
当它作为函数或者全局变量的声明时，提示编译器应当去其他的文件中寻找其定义；

当它与“C”连用时，告诉编译器按照C语言的规则去编译这段代码，而不是按照C++的规则



#### 5.explicit：
主要用于类的构造函数，告诉编译器禁止隐式类型转换



#### 6.volatile：
告诉编译器，每次使用该变量的时候一定要从编译器中真正取出，而不是使用寄存器中的备份



#### 7.mutable：
允许const成员函数（注意是仅限于类的成员函数）修改被其标记的变量



#### 8.auto与decltype：
| **<font style="color:rgb(31, 31, 31);">特性</font>** | **<font style="color:rgb(31, 31, 31);">auto</font>** | **<font style="color:rgb(31, 31, 31);">decltype</font>** |
| --- | --- | --- |
| **<font style="color:rgb(31, 31, 31);">推导依据</font>** | <font style="color:rgb(31, 31, 31);">变量的</font>**<font style="color:rgb(31, 31, 31);">初始化值</font>** | <font style="color:rgb(31, 31, 31);">任意</font>**<font style="color:rgb(31, 31, 31);">表达式/变量名</font>** |
| **<font style="color:rgb(31, 31, 31);">初始化</font>** | <font style="color:rgb(31, 31, 31);">必须初始化</font> | <font style="color:rgb(31, 31, 31);">不需要初始化</font> |
| **<font style="color:rgb(31, 31, 31);">修饰符处理</font>** | <font style="color:rgb(31, 31, 31);">默认丢弃 & 和顶层 const | <font style="color:rgb(31, 31, 31);">严格保留所有修饰符</font> |
| **<font style="color:rgb(31, 31, 31);">主要用途</font>** | <font style="color:rgb(31, 31, 31);">简化冗长的类型声明</font> | <font style="color:rgb(31, 31, 31);">泛型编程（模板）、定义返回类型</font> |




#### 9.noexcept
当他出现在函数末尾时，就是在告诉编译器：这个函数绝对不会出现任何异常，如果有，就直接终止程序。在移动构造函数中常常使用到，用于跨越vector的性能陷阱：<img src="https://cdn.nlark.com/yuque/0/2026/png/64464470/1775994274433-3ff9bb3d-a726-4701-9885-da205204d156.png" width="1125" title="" crop="0,0,1,1" id="u7df05be4" class="ne-image">



# 7.左值与右值
## <font style="color:#117CEE;"> 1).定义：</font>
**<u><font style="background-color:#FBDE28;">左值</font></u>**：具有明确内存地址，有名字，可由用户改变其值的变量，如int，float等等常见的变量；左值具有持久的状态，只有离开了作用域才会被销毁

**<u><font style="background-color:#FBDE28;">右值</font></u>**：临时生成的，没有名字，即将销毁的数据，如字面量40，返回非引用类型的函数调用等等

##  <font style="color:#117CEE;">2).什么是右值引用：</font>
就是只能绑定到右值的引用，通过“&&”取得；右值引用只能绑定于即将销毁的对象，因此可以自由的移动资源

## <font style="color:#117CEE;"> 3).为什么要使用右值引用：</font>
实现“移动语义”，避免昂贵的拷贝开销；

使用std：：move()函数可以将一个左值转化为右值引用

## <font style="color:#117CEE;"> 4).什么是拷贝构造函数：</font>
1._<u>定义</u>_：用于使用一个已有的类对象去初始化另一个同类型的类对象；再某些情况下，如果使用默认的构造函数，会出现错误，比如：类的成员包含一个指针，如使用默认构造函数，被初始化的对象中就也会出现一个指向相同对象的指针，如果其中的一个类对象被析构，那么其中的指针也会被delete，这样就会造成另一个指针的悬空引用

2._<u>深拷贝与浅拷贝</u>_：

浅拷贝：仅仅只是简单地复制指向某个对象的指针，而非再拷贝一份对象本身，因此新旧对象仍然是指向同一个地址

深拷贝：会额外创建一个与原对象一模一样的对象，新旧对象不共享内存

例（深拷贝）：

```cpp
// int width = 0;
// int height = 0;
// float* pixels = nullptr;

// 2. 深拷贝构造函数 (Copy Constructor)
SimpleImage(const SimpleImage& other)
{
    // TODO: 实现深拷贝逻辑
    size_t total_pixels = width * height;
    pixels = new float[total_pixels];
    // 使用 STL 算法进行高效的内存块拷贝
    std::copy(other.pixels, other.pixels + total_pixels, pixels);
    std::cout << "[Copy Constructor] Deep copy performed.\n";
}

// 3. 深拷贝赋值运算符 (Copy Assignment Operator)
SimpleImage& operator=(const SimpleImage& other)
{
    // 提示：考虑 Copy-and-Swap 惯用法
    // 检查自赋值：防止 img1 = img1 导致自我销毁
    if (this != &other)
    {
        size_t total_pixels = other.width * other.height;

        // 第一步：先分配新内存。如果这里抛出 std::bad_alloc 异常，原对象完好无损。
        float* new_pixels = new float[total_pixels];
        std::copy(other.pixels, other.pixels + total_pixels, new_pixels);

        // 第二步：释放自己旧的内存，防止内存泄露
        delete[] pixels;

        // 第三步：接管新内存和新状态
        pixels = new_pixels;
        width = other.width;
        height = other.height;

        std::cout << "[Copy Assignment] Deep copy performed.\n";
    }
    return *this;
}
```

##  <font style="color:#117CEE;">5).什么是移动构造函数：</font>
移动构造函数的参数是一个右值引用，这个函数不需要分配新的内存，而是直接接管传入参数的内存，并且在完成移动之后销毁原对象

相较于拷贝构造函数，移动构造函数不需要重新分配内存（前者传入的是左值引用），因此性能更高

```cpp
// 注意：强烈建议加上 noexcept 关键字
SimpleImage(SimpleImage&& other) noexcept
: width(other.width),
height(other.height),
pixels(other.pixels) // 第一步：直接把对方的指针拿过来（浅拷贝指针本身）
{
    // 第二步：将原对象“掏空”，使其处于合法但空的状态
    other.width = 0;
    other.height = 0;
    other.pixels = nullptr; // 致命操作：如果没有这一步，other 析构时会把我们刚抢来的内存删掉！

    std::cout << "[Move Constructor] Resource stolen! Zero overhead.\n";
}
```



# 8.内联函数与宏
##  <font style="color:#117CEE;">1).内联函数的作用与缺点：</font>
+ <u>作用</u>：直接在函数调用处展开定义，避免调用函数的开销
+ <u>缺点</u>：可能造成代码膨胀，尤其是递归函数；此外，内联函数不方便调试，每次修改后要重新编译头文件

## <font style="color:#117CEE;">  2).内联函数与宏的区别：</font>
(1).define宏指令在预处理阶段对命令进行替换，inline内联函数在编译期展开函数

(2).宏指令不会进行类型检查，因此可能出现类型安全问题；而内联函数会在编译期进行类型检查

(3).使用宏的时候可能要添加许多括号，容易出错



# 9.C++11的新特性
 1).auto关键字：自动推导变量的类型

 2).移动语义：右值引用、std::move等，消除不必要的拷贝

 3).智能指针：保证内存安全

 4).nullptr代替NULL：NULL的实际定义是 #define NULL 0,因此它实际上是int类型，假如现在有两个重载函	     数，参数类型分别为int和指针，如果想要通过空指针来使用第二个函数，实际却会调用第一个函数；而    	     nullptr的类型是 std::nullptr_t ，它可以被隐式转换为任何指针（float*， void*.....），所以也就可以避免函         数重载时出现的一些问题

 5).lambda 表达式：简单来说就是一个匿名函数，可以直接在代码运行的地方直接定义

 6).constexpr：在编译期进行优化

 7).并发编程：引入 std::thread

 8).统一使用大括号 { } 进行初始化



# 10.指针和引用的区别
 1).指针本质是一个地址，有自己的内存空间；引用只是一个别名

 2).指针可以更改指向的对象；而引用一经初始化之后，就不可更改

 3).指针可以初始化为空指针；引用则必须初始化为一个已有对象的引用

 4).指针可以是多级指针；引用只有一级



# 11.什么是重载、重写、隐藏
### 重载：
同名函数具有不同参数列表，根据传入的不同参数决定使用哪一个函数

### 重写（覆盖）：
指的是基类的虚函数被派生类重新定义，重写后的函数的返回值与参数列表必须与基类虚函数一样

### 隐藏：
当派生类中出现与基类的成员函数同名的函数时，基类的相应函数就会被隐藏（基类函数不能被声明为virtual）



# <font style="color:#DF2A3F;">STL、数据结构、算法------------------------------------------------------</font>










<font style="color:rgb(25, 27, 31);"></font>




