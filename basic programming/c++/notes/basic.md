---
title: c++基础
categories: 
  - [coding, c++]
tags:
  - c++
date: 2020/11/10 21:00:00
---

[toc]

# 组织

## 文件

## 包

## 文件

| 文件名后缀 | 说明       |
| ---------- | ---------- |
| .c         | c 源文件   |
| .h         | c 同文件   |
| .cpp       | c++ 源文件 |
| .hpp       | c++ 头文件 |
| .hh        | c++ 头文件 |
| .hxx       | c++ 头文件 |
| .h++       | c++ 头文件 |

**原则**

- 通常的，`.h` 和 `.c` 对应 c 代码，`.hpp` 和 `.cpp` 对应 c++ 代码
  - 除此之外的后缀，多是项目规范，保持一惯性即可
- 保持 `.h` 文件是 c 兼容的代码（不包含 c++ 代码）
- 如果想编写 c 和 c++ 的混合代码
  - 可以在 `.hpp` 中使用 `extern "C"` 来实现
- 不要使用 `.H` 和 `.C` 后缀，因为部分文件系统不区分大小写，比如 windows，macos 在格式化分区时也有不区分大小写的选项

# 输入输出

标准输入输出包含：

- cin
- cout
- cerr
- clog
  - 带缓冲区，常用于写日志数据

```c++
// 持续输入
while (cin >> num)
  sum += num;

// 读取到类对象
cin >> Item;
```

# 基础

## 变量

###  初始化

C++ 支持两种初始化方式，复制初始化和直接初始化。

```c++
int val(1024);   // 直接初始化；效率更高
int val = 1024;  // 复制初始化
```

对于内置类型来说，复制初始化和直接初始化几乎没有差别。函数体外定义的内置变量都初始化成0，函数体内定义的内置变量不进行自动初始化。变量在使用前必须被定义，且只允许被定义一次。

### 声明

为了让多个文件可以访问相同的变量，C++ 区分了声明和定义。声明用于向程序表明变量存在，及其类型和名字；定义用于为变量分配空间，还可对变量进行初始化。

```c++
extern int i;	 // 声明变量
int i;  			 // 定义变量

extern int i = 1;  // 有初始化的声明，可视为定义
```

# 数据类型

| 类型        | 含义           | 最小存储空间 |
| ----------- | -------------- | ------------ |
| bool        | 布尔型         | ---          |
| char        | 字符           | 8位          |
| wchar_t     | 宽字符型       | 16位         |
| short       | 短整型         | 16位         |
| int         | 整型           | 16位         |
| long        | 长整型         | 32位         |
| float       | 单精度浮点数   | 6位有效数字  |
| double      | 双精度浮点型   | 10位有效数字 |
| long double | 扩展精度浮点型 | 10位有效数字 |

```c++
wchar_t wc = L'a'; // 字符前面加 L 表示宽字符 
```

## 类型

### 数字

### 字符串

**初始化**

```c++
string s(10, '0');
```

**子串**

```c++
str.substr(3, 5);    // [3, 8)
str.substr(5);       // [5, ~)
```

### 布尔

## 限定

### static

```c++
class A {
public:
    static A Instance() {  // 实现单例
        static A _a;       // static 修饰，只会创建一次 A 对象
        return _a;
    }
};
```

## 常量

## 定义

# 数据结构

## 数组

```c++
// 创建
int i[5];
int j[2][2];

// 初始化
int i[] = {1, 2, 3};
int j[][1] = {{1}, {2}, {3}};

// 二维数组初始化
int k[2][2] = {{1, 2}, {3}};
1 2
3 0
  
// 静态数组
int i[5] = {0};     // 创建静态数组, 并初始化, 没设置的元素被重置为 0
std::cout << sizeof(i) << std::endl;		// 20, 5 * 4. 5 个元素, 每个占用 4 字节空间
int b[3][3] = {0};	// 多维数组

// 动态数组
int size = 3;
int *c = new int[size];		// 创建动态数组
std::cout << sizeof(c) << " - " << sizeof(*c) << std::endl;		// 8 - 4. 8: 64位机器, 指针大小, 4: int 元素大小
memset(c, 0, size * sizeof(*c));			// 必须要乘 size 才能算出总的占用内存
delete[] c;
```

## 列表

```c++
// 初始化
vector<int> iv{1, 2, 3}		// [1, 2, 3]
vector<int> iv(3, 1);     // [1, 1, 1]
```

## 集合

## 映射

```c++
// 初始化
std::map<int, int> m = {
        {1, 2},
        {2, 3}
    };

std::map<std::string, std::vector<int> > mapOfOccur = {
        { "Riti", { 3, 4, 5, 6 } },
        { "Jack", { 1, 2, 3, 5 } }
    };

// 遍历
std::map<int, int> m = ...;
for (auto &entry : m) {
  std::cout << entry.first << " -> " << entry.second << std::endl;
}

// 插入
map<int, string> mp;
mp.insert(pair<int,string>(1,"aaaaa"));
mp.insert(make_pair<int,string>(2,"bbbbb"));
mp.insert(map<int, string>::value_type(3,"ccccc"));
mp[4] = "ddddd";

std::map<char,int> mp;
mp.emplace('x',100);

// 查找
std::map<char,int>::iterator it = mp.find('x');
if (it != mp.end())
  // exists
else
  // not exists

// 删除
std::map<char,int>::iterator it = mp.find('x');
if (it != mp.end())
    mp.erase(it);
```

# 语法

## 程序结构

## 注释

## 运算符

## 条件控制

## 循环

## 判断

## 函数

## 类

### 特殊成员函数

```c++
// 默认构造函数 (Default constructor)
classname ()
// 非默认函数
explicit classname(type param)
// 拷贝构造函数 (Copy constructor)
classname(const classname &other) 
// 赋值构造 (Copy assignment operator)
classname& operator=(const classname &other)
// move 构造 (Move constructor)
classname(classname &&other)
// 赋值 move 构造 (Move assignment operator)
classname& operator=(classname &&other)

// 析构函数 Destructor
~classname()
```

|         Function         |            syntax for class MyClass             |
| :----------------------: | :---------------------------------------------: |
|   Default constructor    |                  `MyClass();`                   |
|     Copy constructor     |        `MyClass(const MyClass& other);`         |
|     Move constructor     |      `MyClass(MyClass&& other) noexcept;`       |
| Copy assignment operator |   `MyClass& operator=(const MyClass& other);`   |
| Move assignment operator | `MyClass& operator=(MyClass&& other) noexcept;` |
|        Destructor        |                  `~MyClass();`                  |

# 特性

## 语法糖

### default

`default` 关键词为类的**特殊默认无参**函数（构造、析构、拷贝构造、拷贝赋值）提供默认行为。

```c++
class A
{
public:
    A() = default;
    A(const A&);
    A& operator = (const A&);
    ~A() = default;
};

A::A(const X&) = default;  							// 拷贝构造函数
A& A::operator= (const A&) = default;   // 拷贝赋值操作符
```

### delete

和 `default` ，屏蔽默认行为。

```c++
class A
{
    A& operator=(const A&) = delete;    // assignment operator disabled
};

A a, b;
a = b;   // ERROR: 拷贝赋值操作被禁用
```

### thread_local

### lambda

lambda 表达式格式如下。

```c++
[函数对象参数] (操作符重载函数参数) mutable 或 exception 声明 -> 返回值类型 {函数体}
```

**函数对象参数**

| 值        | 参数范围                                           | 参数传递方式                    | 备注                                                        |
| --------- | -------------------------------------------------- | ------------------------------- | ----------------------------------------------------------- |
| 空        | 没有函数对象参数                                   | -                               | -                                                           |
| =         | 表达式所有可访问局部变量（包括所在类的 this 对象） | 值传递                          | -                                                           |
| &         | 表达式所有可访问局部变量（包括所在类的 this 对象） | 引用传递                        | -                                                           |
| this      | 函数体内可以使用 Lambda 所在类中的成员变量         | TBD                             | -                                                           |
| a         | a                                                  | 值传递                          | 变量默认为 const，如果需要修改需为函数体添加 mutable 修饰符 |
| &a        | a                                                  | 引用传递                        |                                                             |
| a，&b     | a，b                                               | a 为值传递，b 为引用传递        | -                                                           |
| =，&a，&b | 表达式所有可访问局部变量（包括所在类的 this 对象） | a、b 引用传递，其他参数是值传递 | -                                                           |
| &，a，b   | 表达式所有可访问局部变量（包括所在类的 this 对象） | a、b 值传递，其他参数是引用传递 | -                                                           |

## 空指针处理

## 函数式编程

## 泛型编程

```c++
// 从标准输入读取T类型数据
template <typename T>
T r() {
    T t;
    cin >> t;
    return t;
}

// 使用
int x = r<int>();
```

```c++
// 值交换
template <typename T>
void swapT(T& a, T& b) {
    a ^= b;
    b ^= a;
    a ^= b;
}

// 使用
vector<int> iv{1, 2, 3};
swapT(iv[0], iv[2]);
// 1 2 3 -> 3 2 1
```

不限于类型。

```c++
template<unsigned N>
void f() {
    std::cout << N << std::endl;
}

int main() {
    f<10>();
    return 0;
}
```

### 类型推演

**重用方法**

```shell
std::is_same<TA, TB>
typeid()
std::is_same_v<TA, TB>  #include <variant>
```

**类型读取及定义**

```c++
template<auto object, class T=std::decay_t<decltype(*object)>>
int Function();
```

**类型判断**

```c++
#include <concepts>

 template<typename Type>
 concept CharTypes = std::is_same<Type, char>::value ||
                        std::is_same<Type, wchar_t>::value || std::is_same<Type, char8_t>::value ||
                        std::is_same<Type, char16_t>::value || std::is_same<Type, char32_t>::value;

template<CharTypes T>
    class Some{};
```

```c++
#include <variant>

template<class T>
void f(T t) {
  if (std::is_same_v<T, std::string>) {
    // DO SOMETHING
  }
}
```



## 宏定义 define

### `##`

连接形参，忽略前后空白符。

```c++
#define Concat(a, b) a##b

int ab = 1, ax = 2, xa = 3;
std::cout << Concat(a, b) << std::endl; // output: 1
std::cout << AppendX(a) << std::endl; // output: 2
std::cout << XAppend(a) << std::endl; // output: 3
```

```c++
// not ok
#define select(m, key) m##[#key]
// ok
#define select(m, key) (m)[#key]

//--- .
// not ok
#define select(m, key) m##.##key
#define select(m, key) m.##key
// ok
#define select(m, key) m.key


// 使用
std::map<std::string, std::string> m;
m["a"] = "0";
auto v = select(m, a);

// 在使用宏变量时，外加小括号, 比如 #define add(a, b) (a) + (b)
```

### `#@`

字符化形参。

### `#`

字符串化形参。

```c++
#define ToString(a) #a
std::cout << ToString(abc) << std::endl;  // abc

// 拼接
#define ToSV(member) #member##sv
ToSV(time)  // 等价于 "time"sv
```

## Parameter pack

[Parameter pack](https://en.cppreference.com/w/cpp/language/parameter_pack)。

> A template parameter pack is a template parameter that accepts zero or more template arguments (non-types, types, or templates). A function parameter pack is a function parameter that accepts zero or more function arguments.
>
> A template with at least one parameter pack is called a *variadic template*.

包含至少一个参数包的模板称为可变模板。

## 右值引用`&&`

C++ 11 引入右值引用主要是为了解决以下几个问题：

1. **优化复制大对象的性能问题。**

在传递一个对象时，如果使用常规的左值引用，就需要进行拷贝构造函数的调用，这会导致复制大对象的时候开销很大。而右值引用可以避免这种情况的发生。因为右值引用本身不会进行对象的拷贝操作，只是将对象所在的内存地址绑定到右值引用上，从而提高代码执行效率。

2. **实现移动语义，支持转移资源所有权。**

在C++11中，新增了std::move函数，可以将一个对象的资源所有权转移到另一个对象中，这就是移动语义。通过将对象的内部数据指针从源对象转移到目标对象，可以避免创建和销毁临时对象，从而提高代码执行效率。而实现移动语义，需要使用右值引用的特性。

总之，右值引用的引入，旨在提高C++代码的性能和效率，支持更加高效的对象传递和资源管理方式，并且为C++编程带来更多的灵活性和扩展性。

其他优化场景。

- 函数中返回一个临时变量时，编译器会自动调用移动构造函数，并将临时变量的资源所有权移动到函数的返回值中，从而避免进行数据拷贝

```c++
// 示例 1
std::string GetString() {
    std::string t = "abc";
    std::string res = t + "def";
    std::cout << "A " << static_cast<void *>(res.data()) << std::endl;
    return res; // 函数返回临时变量, 未进行对象拷贝
}

int main() {
    auto r = GetString(); // 右值引用赋值给左值变量, 不进行对象拷贝
    std::cout << "B " << static_cast<void *>(r.data()) << std::endl;
    std::cout << "---" << std::endl;
    auto r2 = std::move(GetString());
    std::cout << "B " << static_cast<void *>(r2.data()) << std::endl;
    return 0;
} /* output
A 0x16eeeb100
B 0x16eeeb100
---
A 0x16eeeb0c0
B 0x16eeeb0d8
*/
```

### 注意

- 对右值调用 `std::move` 没有作用

# 其他

## 常量

```c++
// MAX / MIN
INT_MAX
INT_MIN
```

# 进阶

## C++ 程序质量保障

- 代码覆盖率（code coverage）
- 内存检查
  - asan
  - valgrind
- CPU Profiler﻿

## malloc

常用的 malloc 库，及实践。

- jemalloc
- tcmalloc
  - 性能要好于 jemalloc
- mimalloc
  - 偶尔会 core

## RAII

RAII（Resource Acquisition Is Initialization，资源获取即初始化）使用局部变量来管理资源，是 C++ 中常用的资源管理方式。

# 时间

- time unit
  - std::chrono::microseconds
  - std::chrono::milliseconds
  - std::chrono::second
  - std::chrono::minutes
  - std::chrono::hours
  - std::chrono::days
  - std::chrono::months
  - std::chrono::years
- clock
  - steady_clock 单调递增时钟
  - system_clock 系统时间时钟
  - high_resolution_clock 高精度时钟
- time_point
- duration
- duration_cast

```c++
std::chrono::time_point<Clock,Duration>::time_point
```

**sample**

```c++
using namespace std::chrono_literals; // 8h, 24m, 15s
// 当前时间
std::chrono::system_clock::now(); // return time_point
// duration
std::chrono::duration(10s); // 10 秒
```

