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

- 构造函数
- 析构函数
- 拷贝构造函数
- 拷贝赋值运算符

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

## define

### `##`

连接形参，忽略前后空白符。

```c++
#define Concat(a, b) a##b

int ab = 1, ax = 2, xa = 3;
std::cout << Concat(a, b) << std::endl; // output: 1
std::cout << AppendX(a) << std::endl; // output: 2
std::cout << XAppend(a) << std::endl; // output: 3
```

### `#@`

字符化形参。

### `#`

字符串化形参。

```c++
#define ToString(a) #a
std::cout << ToString(abc) << std::endl;  // abc
```



# 其他

## 常量

```c++
// MAX / MIN
INT_MAX
INT_MIN
```



