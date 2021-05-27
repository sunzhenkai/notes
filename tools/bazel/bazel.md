---
title: bazel
categories: 
	- [工具,bazel]
tags:
	- bazel
date: 2021/05/22 00:00:00
update: 2021/05/22 00:00:00
---

# Description

Bazel 是一个开源的构建、测试工具，类似于 Make、Maven和Gradle。

# Conception

## Workspace

[workspace](https://docs.bazel.build/versions/4.1.0/build-ref.html#workspace) 是一个目录，包含需要构建的源文件；该目录应该包含一个名为 `WORKSPACE` / `WORKSPACE.bzl`  的文本文件（同时则`WORKSPACE.bzl` 优先，可能为空或者包含[外部依赖](https://docs.bazel.build/versions/4.1.0/external.html)）。

## Repositories

代码组织在 repositories 内，包含 `WORKSPACE` 文件的文件加被称为主 repositories，亦称为 `@` 。其他的外部 repositories 在 WORKSPACE 文件使用 [workspace 规则](https://docs.bazel.build/versions/4.1.0/be/workspace.html)中定义。

## Packages

一个 repository 中，组织代码的主要单元是 package。一个 package 是一个相关文件及其之间相互依赖关系的集合。一个 package 定义为包含 `BUILD` 或者 `BUILD.bazel`  的文件夹，该文件位于 resposity 的顶级目录下。一个 package 包含目录下所有的文件及子文件夹下的文件，但不包括包含 BUILD 文件的文件夹下的文件。

```shell
src/my/app/BUILD
src/my/app/app.cc
src/my/app/data/input.txt
src/my/app/tests/BUILD
src/my/app/tests/test.cc
```

上面目录包含两个 package，`my/app` 、`my/app/tests`，`my/app/data` 不是 package，只是 package `my/app` 下的一个文件夹。

## Targets

package 是一个容器。package 内的元素称为 targets。大多数 targets 是两个主要类型（files、rules）中的一个。此外，还有另外一种很少用的类型的 target，[package groups](https://docs.bazel.build/versions/4.1.0/be/functions.html#package_group)。

文件又被分为源文件（source files）和生成文件（generated files），生成文件是根据特定规则由源文件生成。

第二种 target 是规则。一个规则指定一系列输入和输出文件之间的关系，包括必要的步骤来驱动从源文件到生成文件的转换。一个规则的输出总是生成文件（generated files）。规则的输入，可以是源文件，也可以是生成的文件。所以，一条规则的输出可能是另一个规则的输出，从而构造较长的规则链。

Package groups 是一系列的 packages，主要目的是用来限制特定规则的访问。package group 使用 `package_group` 方法定义，包含两个参数：包含的package列表和名称。

## Labels

每个 targets 只属于一个package。target 的名称被称作它的 label，典型的 label 示例如下。

```bazel
@myrepo//my/app/main:app_binary
```

指向相同 repository 的 label，repository 名称可以省略。所以，`@myrepo` 内部，label 通常如下。

```
//my/app/main:app_binary
```

每个 label 包含两部分，package 名称（`my/app/main`） 和一个 target 名称（ `app_binray`）。每个 label 唯一标示一个 target。label 有时以其他样式展示，当省略冒号时，target 名称被认为和package name 的最后一个组件相同，比如，以下两个 label 含义相同。

```
//my/app
//my/app:app 
```

label 以 `//` 开始，package 则从不以此开头，所以 `my/app` 是包含 target `//my/app` 的 package。

在 BUILD 文件内部，label 的 package name 部分可以省略，冒号也可以作为可选项省略。所以，在 package `my/app` 下的 BUILD 文件（比如，`//my/app:BUILD`）内，下面的 labels 含义是相同的。

```bazel
//my/app:app
//my/app
:app
app
```

相似的，在 BUILD 文件内，属于 package 的文件，可以使用相对于 package 文件夹的相对路径来表示。

```bazel
generate.cc
testdata/input.txt
```

但是，在其他 package 内或命令行，这些文件 target 必须使用完整的label来引用，比如 `//my/app:generate.cc`。

以 `@//` 开头的 label 指向 main reposity，即使在外部库中依然可以使用。因此在外部reposity 中使用时， `@//a/b/c` 和 `//a/b/c` 不同，前面的形式返回 main repository，后面的形式只在外部 reposity 中查找。

### label 的词法规范

#### Target name

target-name 是 package 内 target 的 name。BUILD 文件中 rule 的 name 是其定义中 name 属性的值；文件的 name 是相对于包含 BUILD 文件夹路径的相对路径。不用使用 `.. ` 在其他 package 中引用文件，使用 `//packagename:filename` 代替。文件的相对路径不可以有前置和后置的 `/` （`/foo` 和 `foo/` 是禁止的）和连续的 `/` （`foo//bar` 也是禁止的），`..` 和 `./` 也是禁止的。

在文件名中使用 `/` 很常见，所以不建议在 rule 名称中使用 `/`。

#### Package name

Package name 是包含 BUILD 文件的文件夹相对于顶层目录的相对路径，比如 `my/app`。package name 不应该包含 `//` ，或以 `/` 结尾。

## Rules

rule 指定了输入和输出之间的关系，以及构建和输出的步骤。rules 可以是一个或多个不同类型的 classes（生成编译的可执行文件、测试程序及其它[支持的输出类型](https://docs.bazel.build/versions/4.1.0/be/overview.html)）。

Rule 的 name 在以定义的 name 属性指定，虽然名称可以随意定义，但对于`*_binary` 和 `*_test` 规则来说，rule 名称决定输出文件名称。

```
cc_binary(
    name = "my_app",
    srcs = ["my_app.cc"],
    deps = [
        "//absl/base",
        "//absl/strings",
    ],
)
```

## BUILD files

BUILD 文件使用命令式语言 starlark 处理。值得注意的是，starlark 程序不能随意执行 I/O 操作，这使得 BUILD 文件的解释过程是幂等的，只依赖一系列已知的输入，这保证了构建过程的可复制性。

通常，顺序很重要，变量必须在使用前定义。但是，大多数时候 BUILD 文件仅有一系列规则组成，他们的相对顺序不重要。

为了鼓励代码和数据分离，BUILD 文件不允许包含函数定义、for语句、if语句，他们应该定义在 `bzl` 文件中。此外，`*args` 和 `**kwargs` 也不被允许，应该准确的列出所有的参数。

BUILD 文件应该仅适用 ASCII 字符编写。

### 加载扩展

bazel 扩展文件以 `.bzl` 结尾，使用 `load` 命令从扩展中加载一个符号。

```
load("//foo/bar:file.bzl", "some_library")
```

上面命令会加载文件 `foo/var/file.bzl` 并添加 `some_library` 到环境变量，该命令可以加载 rules、functions、常量。可以通过添加额外的参数，来加载多个标识。参数必须是字符串常量，不能使用变量。load 命令必须在文件的顶层，比如，不能放在 function 里面。可以重命名标识。

```bazel
load("//foo/bar:file.bzl", some_library_alias = "some_library")
load(":my_rules.bzl", "some_rule", nice_alias = "some_other_rule")
```

在 `.bzl` 文件中以 `_` 开头的标识，不能被导出，也即不能再其他文件中被load。

## Types of build rule

主要的构建规则成簇出现，根据语言进行分组。

- `*_binary` 
- `*_test`
- `*_library` 

## Dependencies

基于关系的依赖在 targets 之间组成 DAG 图。

### 依赖类型

#### srcs 依赖

被规则直接使用的文件。

#### deps 依赖

规则指向独立编译的模块，提供头文件、标识、库、数据等。

#### data 依赖

构造系统只在隔离的文件夹运行测试，只有在配置的 data 列表中配置的文件可用。因此，如果一个可执行文件、库、测试程序的执行需要一些文件，需要在data字段中指定，比如。

```
# I need a config file from a directory named env:
java_binary(
    name = "setenv",
    ...
    data = [":env/default_env.txt"],
)

# I need test data from another directory
sh_test(
    name = "regtest",
    srcs = ["regtest.sh"],
    data = [
        "//data:file1.txt",
        "//data:file2.txt",
        ...
    ],
)
```

这些文件，可以使用相对路径 `/path/to/data/file` 访问。测试程序中，可以通过拼接测试源目录和相对workspace的路径进行拼接来访问，比如 `${TEST_SRCDIR}/workspace/path/to/data/file`。

