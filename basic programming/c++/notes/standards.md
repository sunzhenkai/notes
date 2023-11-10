---
title: c++ 各标准版本特性
categories: 
  - [coding, c++]
tags:
  - c++
date: 2023/11/07 00:00:00
---

# 版本说明

WG21（The ISO C++ committee）有严格的时间限制，每 3 年推出一版新的标准。最新的版本信息参考 WG21 [官网](https://isocpp.org/)。每个正式标准确定前，会使用草案名（draft），比如 `c++1z`、`c++2a`。

# 各版本特性

## C++ 20（C++2a）

### 语言特性

- **[协程 coroutines](https://github.com/AnthonyCalandra/modern-cpp-features#coroutines)**
- [concepts](https://github.com/AnthonyCalandra/modern-cpp-features#concepts)
- [designated initializers](https://github.com/AnthonyCalandra/modern-cpp-features#designated-initializers)
- [template syntax for lambdas](https://github.com/AnthonyCalandra/modern-cpp-features#template-syntax-for-lambdas)
- [range-based for loop with initializer](https://github.com/AnthonyCalandra/modern-cpp-features#range-based-for-loop-with-initializer)
- [[[likely\]] and [[unlikely]] attributes](https://github.com/AnthonyCalandra/modern-cpp-features#likely-and-unlikely-attributes)
- [deprecate implicit capture of this](https://github.com/AnthonyCalandra/modern-cpp-features#deprecate-implicit-capture-of-this)
- [class types in non-type template parameters](https://github.com/AnthonyCalandra/modern-cpp-features#class-types-in-non-type-template-parameters)
- [constexpr virtual functions](https://github.com/AnthonyCalandra/modern-cpp-features#constexpr-virtual-functions)
- [explicit(bool)](https://github.com/AnthonyCalandra/modern-cpp-features#explicitbool)
- [immediate functions](https://github.com/AnthonyCalandra/modern-cpp-features#immediate-functions)
- [using enum](https://github.com/AnthonyCalandra/modern-cpp-features#using-enum)
- [lambda capture of parameter pack](https://github.com/AnthonyCalandra/modern-cpp-features#lambda-capture-of-parameter-pack)
- [char8_t](https://github.com/AnthonyCalandra/modern-cpp-features#char8_t)
- [constinit](https://github.com/AnthonyCalandra/modern-cpp-features#constinit)

### 库特性

- [concepts library](https://github.com/AnthonyCalandra/modern-cpp-features#concepts-library)
- [synchronized buffered outputstream](https://github.com/AnthonyCalandra/modern-cpp-features#synchronized-buffered-outputstream)
- [std::span](https://github.com/AnthonyCalandra/modern-cpp-features#stdspan)
- [bit operations](https://github.com/AnthonyCalandra/modern-cpp-features#bit-operations)
- [math constants](https://github.com/AnthonyCalandra/modern-cpp-features#math-constants)
- [std::is_constant_evaluated](https://github.com/AnthonyCalandra/modern-cpp-features#stdis_constant_evaluated)
- [std::make_shared supports arrays](https://github.com/AnthonyCalandra/modern-cpp-features#stdmake_shared-supports-arrays)
- [starts_with and ends_with on strings](https://github.com/AnthonyCalandra/modern-cpp-features#starts_with-and-ends_with-on-strings)
- [check if associative container has element](https://github.com/AnthonyCalandra/modern-cpp-features#check-if-associative-container-has-element)
- [std::bit_cast](https://github.com/AnthonyCalandra/modern-cpp-features#stdbit_cast)
- [std::midpoint](https://github.com/AnthonyCalandra/modern-cpp-features#stdmidpoint)
- [std::to_array](https://github.com/AnthonyCalandra/modern-cpp-features#stdto_array)

## C++ 17（C++1z）

### 语言特性

- [template argument deduction for class templates](https://github.com/AnthonyCalandra/modern-cpp-features#template-argument-deduction-for-class-templates)
- [declaring non-type template parameters with auto](https://github.com/AnthonyCalandra/modern-cpp-features#declaring-non-type-template-parameters-with-auto)
- [folding expressions](https://github.com/AnthonyCalandra/modern-cpp-features#folding-expressions)
- [new rules for auto deduction from braced-init-list](https://github.com/AnthonyCalandra/modern-cpp-features#new-rules-for-auto-deduction-from-braced-init-list)
- [constexpr lambda](https://github.com/AnthonyCalandra/modern-cpp-features#constexpr-lambda)
- [lambda capture this by value](https://github.com/AnthonyCalandra/modern-cpp-features#lambda-capture-this-by-value)
- [inline variables](https://github.com/AnthonyCalandra/modern-cpp-features#inline-variables)
- [nested namespaces](https://github.com/AnthonyCalandra/modern-cpp-features#nested-namespaces)
- [structured bindings](https://github.com/AnthonyCalandra/modern-cpp-features#structured-bindings)
- [selection statements with initializer](https://github.com/AnthonyCalandra/modern-cpp-features#selection-statements-with-initializer)
- [constexpr if](https://github.com/AnthonyCalandra/modern-cpp-features#constexpr-if)
- [utf-8 character literals](https://github.com/AnthonyCalandra/modern-cpp-features#utf-8-character-literals)
- [direct-list-initialization of enums](https://github.com/AnthonyCalandra/modern-cpp-features#direct-list-initialization-of-enums)
- [[[fallthrough\]], [[nodiscard]], [[maybe_unused]] attributes](https://github.com/AnthonyCalandra/modern-cpp-features#fallthrough-nodiscard-maybe_unused-attributes)
- [__has_include](https://github.com/AnthonyCalandra/modern-cpp-features#__has_include)
- [class template argument deduction](https://github.com/AnthonyCalandra/modern-cpp-features#class-template-argument-deduction)

### 库特性

- [std::variant](https://github.com/AnthonyCalandra/modern-cpp-features#stdvariant)
- [std::optional](https://github.com/AnthonyCalandra/modern-cpp-features#stdoptional)
- [std::any](https://github.com/AnthonyCalandra/modern-cpp-features#stdany)
- [std::string_view](https://github.com/AnthonyCalandra/modern-cpp-features#stdstring_view)
- [std::invoke](https://github.com/AnthonyCalandra/modern-cpp-features#stdinvoke)
- [std::apply](https://github.com/AnthonyCalandra/modern-cpp-features#stdapply)
- [std::filesystem](https://github.com/AnthonyCalandra/modern-cpp-features#stdfilesystem)
- [std::byte](https://github.com/AnthonyCalandra/modern-cpp-features#stdbyte)
- [splicing for maps and sets](https://github.com/AnthonyCalandra/modern-cpp-features#splicing-for-maps-and-sets)
- [parallel algorithms](https://github.com/AnthonyCalandra/modern-cpp-features#parallel-algorithms)
- [std::sample](https://github.com/AnthonyCalandra/modern-cpp-features#stdsample)
- [std::clamp](https://github.com/AnthonyCalandra/modern-cpp-features#stdclamp)
- [std::reduce](https://github.com/AnthonyCalandra/modern-cpp-features#stdreduce)
- [prefix sum algorithms](https://github.com/AnthonyCalandra/modern-cpp-features#prefix-sum-algorithms)
- [gcd and lcm](https://github.com/AnthonyCalandra/modern-cpp-features#gcd-and-lcm)
- [std::not_fn](https://github.com/AnthonyCalandra/modern-cpp-features#stdnot_fn)
- [string conversion to/from numbers](https://github.com/AnthonyCalandra/modern-cpp-features#string-conversion-tofrom-numbers)

## C++ 14（C++1y）

### 语言特性

- [binary literals](https://github.com/AnthonyCalandra/modern-cpp-features#binary-literals)
- [generic lambda expressions](https://github.com/AnthonyCalandra/modern-cpp-features#generic-lambda-expressions)
- [lambda capture initializers](https://github.com/AnthonyCalandra/modern-cpp-features#lambda-capture-initializers)
- [return type deduction](https://github.com/AnthonyCalandra/modern-cpp-features#return-type-deduction)
- [decltype(auto)](https://github.com/AnthonyCalandra/modern-cpp-features#decltypeauto)
- [relaxing constraints on constexpr functions](https://github.com/AnthonyCalandra/modern-cpp-features#relaxing-constraints-on-constexpr-functions)
- [variable templates](https://github.com/AnthonyCalandra/modern-cpp-features#variable-templates)
- [[[deprecated\]] attribute](https://github.com/AnthonyCalandra/modern-cpp-features#deprecated-attribute)

### 库特性

- [user-defined literals for standard library types](https://github.com/AnthonyCalandra/modern-cpp-features#user-defined-literals-for-standard-library-types)
- [compile-time integer sequences](https://github.com/AnthonyCalandra/modern-cpp-features#compile-time-integer-sequences)
- [std::make_unique](https://github.com/AnthonyCalandra/modern-cpp-features#stdmake_unique)

## C++ 11（C++0x / C++1x）

### 语言特性

- [移动语义 move semantics](https://github.com/AnthonyCalandra/modern-cpp-features#move-semantics)
- [可变参数模板 variadic templates](https://github.com/AnthonyCalandra/modern-cpp-features#variadic-templates)
- [右值引用 rvalue references](https://github.com/AnthonyCalandra/modern-cpp-features#rvalue-references)
- [转发引用 forwarding references](https://github.com/AnthonyCalandra/modern-cpp-features#forwarding-references)
- [初始化列表 initializer lists](https://github.com/AnthonyCalandra/modern-cpp-features#initializer-lists)
- [静态断言 static assertions](https://github.com/AnthonyCalandra/modern-cpp-features#static-assertions)
- [auto](https://github.com/AnthonyCalandra/modern-cpp-features#auto) 自动类型推导 & 返回值占位
- [lambda 表达式 lambda expressions](https://github.com/AnthonyCalandra/modern-cpp-features#lambda-expressions)
- [表达式类型推导 decltype](https://github.com/AnthonyCalandra/modern-cpp-features#decltype)
- [类型重命名 type aliases](https://github.com/AnthonyCalandra/modern-cpp-features#type-aliases)
- [nullptr](https://github.com/AnthonyCalandra/modern-cpp-features#nullptr)
- [strongly-typed enums](https://github.com/AnthonyCalandra/modern-cpp-features#strongly-typed-enums)
- [attributes](https://github.com/AnthonyCalandra/modern-cpp-features#attributes)
- [constexpr](https://github.com/AnthonyCalandra/modern-cpp-features#constexpr)
- [delegating constructors](https://github.com/AnthonyCalandra/modern-cpp-features#delegating-constructors)
- [user-defined literals](https://github.com/AnthonyCalandra/modern-cpp-features#user-defined-literals)
- [explicit virtual overrides](https://github.com/AnthonyCalandra/modern-cpp-features#explicit-virtual-overrides)
- [final specifier](https://github.com/AnthonyCalandra/modern-cpp-features#final-specifier)
- **[default functions](https://github.com/AnthonyCalandra/modern-cpp-features#default-functions)**
- **[deleted functions](https://github.com/AnthonyCalandra/modern-cpp-features#deleted-functions)**
- [range-based for loops](https://github.com/AnthonyCalandra/modern-cpp-features#range-based-for-loops)
- [special member functions for move semantics](https://github.com/AnthonyCalandra/modern-cpp-features#special-member-functions-for-move-semantics)
- [converting constructors](https://github.com/AnthonyCalandra/modern-cpp-features#converting-constructors)
- [explicit conversion functions](https://github.com/AnthonyCalandra/modern-cpp-features#explicit-conversion-functions)
- [inline-namespaces](https://github.com/AnthonyCalandra/modern-cpp-features#inline-namespaces)
- [non-static data member initializers](https://github.com/AnthonyCalandra/modern-cpp-features#non-static-data-member-initializers)
- [right angle brackets](https://github.com/AnthonyCalandra/modern-cpp-features#right-angle-brackets)
- [ref-qualified member functions](https://github.com/AnthonyCalandra/modern-cpp-features#ref-qualified-member-functions)
- [trailing return types](https://github.com/AnthonyCalandra/modern-cpp-features#trailing-return-types)
- [noexcept specifier](https://github.com/AnthonyCalandra/modern-cpp-features#noexcept-specifier)
- [char32_t and char16_t](https://github.com/AnthonyCalandra/modern-cpp-features#char32_t-and-char16_t)
- [raw string literals](https://github.com/AnthonyCalandra/modern-cpp-features#raw-string-literals)

### 库特性

- [std::move](https://github.com/AnthonyCalandra/modern-cpp-features#stdmove)
- [std::forward](https://github.com/AnthonyCalandra/modern-cpp-features#stdforward)
- [std::thread](https://github.com/AnthonyCalandra/modern-cpp-features#stdthread)
- [std::to_string](https://github.com/AnthonyCalandra/modern-cpp-features#stdto_string)
- [type traits](https://github.com/AnthonyCalandra/modern-cpp-features#type-traits)
- [smart pointers](https://github.com/AnthonyCalandra/modern-cpp-features#smart-pointers)
- [std::chrono](https://github.com/AnthonyCalandra/modern-cpp-features#stdchrono)
- [tuples](https://github.com/AnthonyCalandra/modern-cpp-features#tuples)
- [std::tie](https://github.com/AnthonyCalandra/modern-cpp-features#stdtie)
- [std::array](https://github.com/AnthonyCalandra/modern-cpp-features#stdarray)
- [unordered containers](https://github.com/AnthonyCalandra/modern-cpp-features#unordered-containers)
- [std::make_shared](https://github.com/AnthonyCalandra/modern-cpp-features#stdmake_shared)
- [std::ref](https://github.com/AnthonyCalandra/modern-cpp-features#stdref)
- [memory model](https://github.com/AnthonyCalandra/modern-cpp-features#memory-model)
- [std::async](https://github.com/AnthonyCalandra/modern-cpp-features#stdasync)
- [std::begin/end](https://github.com/AnthonyCalandra/modern-cpp-features#stdbeginend)

# 参考

- [modern-cpp-features](https://github.com/AnthonyCalandra/modern-cpp-features)