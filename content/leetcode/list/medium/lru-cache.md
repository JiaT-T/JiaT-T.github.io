+++
slug = "lru-cache"
title = "LRU 缓存"
problems = [146]
problem_id = 146
difficulty = "Medium"
weight = 146
summary = "LRU 缓存的解题思路与 C++ 实现。"
+++

题目：[LRU 缓存](https://leetcode.cn/problems/lru-cache/)


<a id="第一百四十六题lru-缓存"></a>



使用到的是<font style="background-color:#FBDE28;">哈希表和链表</font>（重点是链表迭代器）

这题难点在于“逐出最久未使用的关键字”，首先明确思路：既然要求常数时间的复杂度，那么就一定会要用到哈希表（查找），但是又要求有一个数据结构可以存储元素使用的顺序，并且改变顺序时也要是O(1)的时间复杂度，那么就也要使用到链表（通过调用 _Splice函数_ 可以改变迭代器位置，从而在常数时间内实现顺序的改变）

但是如何将哈希表与链表结合起来？答：<font style="background-color:#FBDE28;">将value和iterator绑定在一起</font>，这样就通过key就既可以得到value的值，又可以实现iterator的移动

具体实现：

首先拿到最大容量，避免后续多次函数调用产生的开销；



然后开始定义 **get** 函数：

    - 如果哈希表内能够找到对应的key，那么就认为这个元素被访问了一次，因此也就需要将其放在链表的尾部，这里可以通过key在哈希表中找到对应的iterator
    - splice（）函数的语法之一（移动单个节点）：
                    * **void splice(const_iterator pos, list& other, const_iterator it);**
    -  将 `other` 链表中由 `it` 指向的那个元素剪切到 `this` 链表的 `pos` 位置



最后实现 **put** 函数：

    - 这里有两种情况需要处理：1.当前key已经存在	2.容量已满
    - 1.key重复：
        * 意味着需要覆写之前的value，将其移至list尾部，这里还是使用到splice（）
    - 2.容量已满：
        * 此时需要删除头节点，直接pop_front()即可；同时也要同步删除哈希表中对应的元素

最后将新插入的元素添加到两个容器即可

```cpp
class LRUCache
{
public:
    LRUCache(int capacity) : capacity(capacity)
    {
        cache.reserve(capacity);
    }

    int get(int key)
    {
        if(cache.contains(key))
        {
            auto it = cache.find(key);
            order.splice(order.end(), order, it->second.second);
            return it->second.first;
        }
        else return -1;
    }

    void put(int key, int value)
    {
        auto it = cache.find(key);
        if(it != cache.end()) // 如果value已经存在，则更新
        {
            it->second.first = value;
            order.splice(order.end(), order, it->second.second);
            return;
        }
        if(cache.size() >= capacity) // 处理超出容量情况
        {
            cache.erase(order.front());
            order.pop_front();
        }

        order.push_back(key);
        cache[key] = {value, std::prev(order.end())};
    }

private :
    int capacity;
    std::unordered_map<int, std::pair<int, std::list<int>::iterator>> cache;  // 键，值，迭代器
    std::list<int> order;
};
```
