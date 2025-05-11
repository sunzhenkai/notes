---
title: flex & bison 实现语法解析
categories: 
  - 计算机科学
  - 编译原理
tags:
  - flex
  - bison
date: "2021-01-28T00:00:00+08:00"
---

# 简述

flex/lex 和 bison/yacc 是 linux 下用来生成词法分析器和语法分析器的工具。flex和lex、bison和yacc 数据同质的程序，相对于flex和lex，bison和yacc之间兼容性更好。

# 工具介绍

## bison

Bison是一个通用解析器生成器，可以将带注释的上下文无关语法，转换为使用LALR解析表的确定性 LR 或广义LR（GLR）解析器。可熟练运用bison后，可以用它开发各种语言解析器。

Bison向上兼容Yacc，所有正确编写的Yacc语法都可与Bison一起工作，无需修改。

## yacc

Yacc（Yet Another Compiler Compiler）是一个用来生成编译器的编译器。yacc 生成的编译器主要是用C语言写成的语法解析器（parser），需要与词法解析器（lex）一起使用，再把两部分产生出来的C程序一并编译。

Yacc的输入是巴克斯范式（BNF）表达的语法规则，以及语法规约的处理代码，输出的是基于表驱动的编译器，包含输入的语法规约的处理代码部分。

Yacc是开发编译器的工具，采用LALR语法分析方法。

## lex

在计算机科学里面，lex是一个产生词法分析器的程序。Lex常与 yacc 语法分析器产生程序（parser generator）一起使用。

## flex

flex 是一个词法分析器，用于生成扫描器，识别文本中词汇模式。

# 编译器

一个语言编译器或解释器，通常分解为两个部分：

- 读取源文件并发现其中的结构
- 处理他的结构等，生成目标程序

Lex 和 Yacc 可以生成代码片段，解决第一个任务。发现源文件结构的任务可以分解为子任务：

- 分解词法源文件为 tokens（Lex）
- 找到程序的层次结构（Yacc）

# 语法

## lex 词法分析器

lex通过扫描词法源文件，从中提取token，可看做关键词。lex工具会生成一个 `yylex` 函数，语法解析器通过调用这个函数获取信息。lex的输入文件一般会被命名为 `*.l` 文件，通过 `[f]lex XX.l` 得到文件 `lex.yy.c`。

### 语法格式

Lex程序主要由一系列带有指令的正则表达式组成，这些指令确定了正则表达式匹配后相应的动作（action）。由flex生成的词法分析器可以读取输入，匹配输入与所有的正则表达式，并执行每次匹配后适当的关联动作。

Flex程序包含是哪个部分，通过 `%%` 分隔。第一部分包含声明和选项设置，第二部分是一系列的模式和动作，第三部分是会被拷贝到生成的词法分析器里面的C代码，通常是与动作代码相关的程序。

```
Definition section
%%
Rules section
%%
C code section
```

**第一部分**

在声明部分，`%{` 和 `%}` 之间的代码会被原样照抄到生成的 C 文件的开头部分。

**第二部分**

每个模式处在一行的开头处，接着是模式匹配时所需要执行的 C 代码，这里的 C 代码是使用 `{}` 括住的一行或者多行语句。模式必须在行首出现，flex会把空白开始的行当做代码复制到生成C程序中。

### 文本统计示例

**程序**

```c
%{
int chars = 0;
int words = 0;
int lines = 0;
%}

%%
[a-zA-Z]+   { words++; chars += strlen(yytext) }
\n          { chars++; lines++; }
.           { chars++; }
%%

int main(int argc, char **argv) {
  yylex();
  printf("%8d%8d%8d\n", lines, words, chars);
  return 0;
}
```

在这个示例中，末尾的C代码为主程序，负责调用flex提供的词法分析程序yylex()，并输出结果。

**编译**

```shell
$ flex flex-wc.l					# 运行命令后会生成文件 lex.yy.c
$ cc -lfl -o wc lex.yy.c 	# 编译词法解析
$ ./wc
```

注：对于使用命令将 flex 安装到系统，可以直接执行上述命令。如若将 flex 编译至特定目录，并使用的话，需要制定库环境变量，以使程序可正确运行。

```shell
$ export FLEX_BIN_PATH="/.../bin"    # flex 程序路径
$ export FLEX_LIB_PATH="/.../lib"    # flex 库文件路径
$ export LD_LIBRARY_PATH=${FLEX_LIB_PATH}    # 用于 linux 系统
$ export DYLD_LIBRARY_PATH=${FLEX_LIB_PATH}	 # 用于 mac os 系统
$ export PATH="$FLEX_BIN_PATH:$PATH"
# 编译执行
$ flex flex-wc.l
$ cc -L"${LIB_PATH}" -lfl -o wc lex.yy.c		
$ ./wc
hello world
^D
       1       2      12
```

**示例说明**

该实例程序，仅使用 flex 实现。首先，按照 flex 的语法，定义了词法文件 `wc.l`，其中包含 3 个模式 `[a-zA-Z]+`、`\n` 、`.` ，分别用于匹配单词、换行、任意字符。这里需要注意，模式匹配具有排他性，输入被一个模式匹配，则不会重复被其他模式匹配，因此在匹配到单词后，需要使用 `chars += strlen(yytext)` 来修正字符统计值。然后，使用 flex 程序解析 `wc.l` ，生成 `lex.yy.c` 文件。最后，编译生成的文件，并执行。

## yacc / bison 语法分析器

语法分析器，借助 lex 生成的 token，将关键字组合成语法。语法分析器会生成一个 yyparse 函数，这个函数会不断调用词法分析器生成的 `yylex` 函数来得到 token 信息。词法分析器输入的源文件一般命名为 `*.y` ，通过命令 `yacc -d XX.y` 得到文件 `y.tab.h` 和 `y.tab.c` ，前者包含了 lex 需要的 token 类型定义，需要被 include 进 `*.l` 文件中。

## flex & bison

单纯的 flex 程序，可以解决简单的解析问题，但对于复杂的场景，需要语法分析器的支持。flex 仅解析输入中的模式，并执行相应的动作，对于复杂的语法需要语法分析器的支持。

**计算器示例**

接下来，用一个计算器程序示例，展示 flex 和 bison 是如何一起工作。简单些，我们首先实现一个 flex 程序，可以复述（无需解析运算符优先级及计算）简单的表达式。

```c++
%%
"+" { printf("PLUS\n"); }
"-" { printf("MINUS\n"); }
"*" { printf("TIMES\n"); }
"/" { printf("DIVIDE\n"); }
"|" { printf("ABS\n"); }
[0-9]+ { printf("NUMBER %s\n", yytext); }
\n  { printf("NEW LINE\n"); }
[ \t] { }
.   { printf("Mystery character %s\n", yytext); }
%%
```

**编译运行**

```shell
$ flex cal.l
$ cc -o cal lex.yy.c
$ ./cal
12+34
NUMBER 12
PLUS
NUMBER 34
NEW LINE
5 6 / 7q
NUMBER 5
NUMBER 6
DIVIDE
NUMBER 7
Mystery character q
NEW LINE
```

上述程序，只是简单识别了我们的意图，并执行了打印操作。为了让我们的示例更像一个计算器，我们需要支持类似于真正的计算，并支持运算符的优先级等特性。对于这种高阶解析，需要借助 bison 来完成。

flex 作为词法分析器，可以生成一个 token 流，方便语法分析器处理。当程序需要一个 token 时，通过调用 `yylex()` 来读取一小部分输入，然后返回相应的记号，通过再次调用 `yylex()` 获取更多 token。

**token 编号和 token 值**

flex 返回 token 时，实际包含两部分，token 编号和 token 值。这里的编号是一个较小的随意整数，如果返回 0 则意味着文件的结束。当 bison 创建一个语法分析器时， bison 自动地从 258 起指派每个记号编号，并且创建一个包含这些编号定义的 .h 文件。在这里，我们在 flex 程序中，为每个 token 分配一个固定的编号。重写上面计算器的 flex 源文件。

```c++
%{
enum yytokentype {
    NUMBER = 258,
    ADD = 259,
    SUB = 260,
    MUL = 261,
    DIV = 262,
    ABS = 263,
    EOL = 264,
    POW = 265
};
int yylval;
%}

%%

"+" { return ADD; }
"-" { return SUB; }
"*" { return MUL; }
"/" { return DIV; }
"|" { return ABS; }
"^" { return POW; }
[0-9]+ { yylval = atoi(yytext); return NUMBER; }
\n  { return EOL; }
[ \t] { }
.   { printf("Mystery character %c\n", *yytext); }

%%

/*int main(int argc, char **argv)
{
    int tok;
    while (tok = yylex()) {
        printf("%d", tok);
        if (tok == NUMBER) printf(" = %d\n", yylval);
        else printf("\n");
    }
}*/
```

继续编译运行。

```shell
$ $ flex cal.l
$ cc -o cal lex.yy.c
$ ./cal
a / 34 + |45
Mystery character a
262
258 = 34
259
263
258 = 45
264
```

至此，我们有了一个可以返回特定 token 编号及 token 值的词法解析器，接下来关注其如何与语法分析器一起工作。

**语法分析器**

语法分析器的作用是，找出输入记号之间的关系，一种常见的关系表达式就是语法分析树。

**BNF文法**

为了编写一个语法分析器，需要一定的方法描述语法分析器所使用的把一系列记号转化为语法分析书的规则。在计算机最常用的语言就是上下文无关文法（Content-Free Grammar，CFG），书写上下文无关文法的标准格式就是 BackusNaur范式（BackusNaur Form，BNF）。

幸运的是，BNF相当简单。对于表达式 1 * 2 + 3 * 4 + 5 ，下面的 BNF 语法足以处理。

```
<exp> ::= <factor>
	| <exp> + <factor>
<factor> ::= NUMBER
	| <factor> * NUMBER
```

每一行就是一条规则，用来说明如何创建语法分析树的分支。`::=` 被解读为 _是_ 或 _变成_；`|` 为 _或者_，创建同类分支的另一种方式。规则左边的名称是语法符号。大致来说，所有的记号都被认为是语法符号，但是有一些语法符号并不是记号。

有效的BNF总是带有递归性的，规则会直接或者间接地指向自身。这些简单的规则被递归地使用以匹配任何极端复杂的加法和乘法序列。

**bison 规则描述语言**

bison 规则基本符合 BNF 文法，下面是计算器程序的 bison 代码。

```c
%{
#include <stdio.h>
#include <math.h>
int yylex();
void yyerror(char *s);
%}

/* 声明 Tokens; 在这里的声明要和 cal.l 声明的 yytokentype 顺序一致 */
%token NUMBER
%token ADD SUB MUL DIV ABS EOL
%token POW

%%

calclist: /* 空规则 */
	| calclist exp EOL { printf("= %d\n", $2); }
	;

exp: factor
	| exp ADD factor { $$ = $1 + $3; }
	| exp SUB factor { $$ = $1 - $3; }
	;

factor: term
    | factor MUL term { $$ = $1 * $3; }
    | factor DIV term { $$ = $1 / $3; }
    | term POW term   { $$ = pow($1, $3); }
    ;

term: NUMBER
    | SUB NUMBER   { $$ = -$2 }
    | ABS term ABS { $$ = $2 >= 0 ? $2 : -$2; }
    ;

%%

int main(int argc, char **argv)
{
    yyparse();
    return 0;
}

void yyerror(char *s)
{
    fprintf(stderr, "error: %s\n", s);
}
```

bison 程序包含了与flex程序相同的三部分结构：声明部分、规则部分和C代码部分。

声明部分， `%{` 和 `%}` 之间内容同样会被拷贝进代码，`%token` 用于声明标记，以便让 bison 语法分析程序知晓符号。没有声明为记号的语法符号，应该出现在至少一条规则的左边。

规则部分，包含了BNF定义的规则，使用分号分隔不同规则。每条规则中的每个语法符号都有一个语义值，目标符号（冒号左边符号）的值使用 `$$` 代替，右边语法符号的语义值分别用 `$1、$2 ... ` 代替。

**联合 bison & flex 编译**

```shell
$ bison -d cal.y
$ flex cal.l
$ gcc -Wno-parentheses -o calc cal.tab.c lex.yy.c -lfl
$ ./calc   # 执行
1 + 2
= 3
3 - -2
= 5
1 + -2
= -1
1 + |-1|
= 2
```

# 高级语法

## flex

### 正则表达式

| 表达式       | 说明                                                         | 实例           |
| ------------ | ------------------------------------------------------------ | -------------- |
| []           | 字符类，匹配方括号内任意一个字符                             | `[a-z]、[\^a-c]` |
| [a-z]{-}[jv] | 去除字符类中某些字符                                         | -              |
| ^            | 匹配行首                                                     | -              |
| $            | 匹配行尾                                                     | -              |
| {}           |                                                              | `{5} {1,5}`     |
| \            | 转义                                                         |                |
| *            | 匹配0个或多个前面的表达式                                    |                |
| +            | 匹配1个或多个前面的表达式                                    |                |
| ?            | 匹配0个或1个前面的表达式                                     |                |
| \|           | 选择操作符，匹配前或后的表达式                               | foo\|bar       |
| "......."    | 引号内解释为字面常量                                         |                |
| ()           | 把一系列正则表达式组成一个新的正则表达式                     |                |
| /            | 尾部上下文，匹配斜线前的表达式，但是要求其后紧跟着斜线后的表达式 |                |

### 解析文件

词法分析器总是从 `yyin` 读取输入，可以通过重新设定 `yyin` 实现从文件读取。也可以使用 `yyrestart` 指定输入源，此外，`yyrestart` 可以重置解析，并通过调用 `yylex` 重新开始。

```c++
%option noyywrap

%{
int chars = 0;
int words = 0;
int lines = 0;
%}

%%

[a-zA-Z]+   { ++words; chars += strlen(yytext); }
\n          { ++chars; ++lines; }
.           { ++chars; }

%%

int main(int argc, char **argv) {
    yyin = fopen("wc.in", "r");
    // yyrestart(fopen("wc.in", "r"));  // 也可以使用 yyrestart 指定输入源
    yylex();
    printf("%8d%8d%8d\n", lines, words, chars);
}
```

### 输入

flex 词法分析器支持从文件或标准输入读取数据，flex 提供将数据预读取到缓冲区的机制，提高效率，行为大致如下。

```c++
YY_BUFFER_STATE bp;
extern FILE* yyin;
... // 第一次调用语法分析器之前所需要做的事情
if (!yyin) yyin = stdin;
bp = yy_create_buffer(yyin, YY_BUF_SIZE); // YY_BUF_SIZE 由 flex 定义，通常 16k
yy_switch_to_buffer(bp);
```

通过如下宏定义，可重新定义用于输入到缓冲区的宏。

```c++
#define YY_INPUT(buf, result, max_size) ...
```

每当词法分析器的输入缓冲区为空时，就会调用 YY_INPUT，buf 是缓冲区，max_size 是缓冲区大小，result 则用来放置实际读取的长度。

### 输出

默认没有匹配的输入，都会被拷贝到 yyout 中，通过默认添加如下规则实现。

```c++
. ECHO
#define ECHO fwrite(yytext, yyleng, 1, yyout)
```

上面代码，定义一个规则 `.` 用于匹配所有未被识别的输入，并执行默认的行为 `fwrite(yytext, yyleng, 1, yyout)`。

### option

flex 在文件头部通过 `%option` 定义选项。

```c++
%option noyywrap nodefault yylineno case-insensitive
```

| 选项             | 说明                            |
| ---------------- | ------------------------------- |
| noyywrap         |                                 |
| nodefault        | 屏蔽默认行为                    |
| yylineno         | 定义变量 yylineno，保存当前行号 |
| case-insensitive | 生成大小写无关的词法分析器      |
| yyclass          | 指定 scanner 的类名             |
| c++              | 生成c++代码                     |
| debug            |                                 |

## bison

flex 可以识别正则表达式，bison 可以识别语法。flex 把输入流分解为若干个片段，而bison则分析这些记号并给予逻辑进行组合。

### %token

```c++
// 规则
%token <type> name "string-literal"
  
// 示例
%token NUM 300    // 为 token 指定数字编码
%token XNUM 0x12d // a GNU extension
%union {              /* define stack type */
  double val;
  symrec *tptr;
}
%token <val> NUM      /* define token NUM and its type */
  
// 为 token 指定字符常量
%token ARROW "=>"     /* yylex 可通过 token 名称和 字符常量来获取 toKen 类型编码 */
```

### %union

`%union` 用于指定语义值的类型集合，定义语法和 c 中的 union 类似。

```c++
%union {
  double val;
  symrec *tptr;
}
```

上述声明，声明有两个可选类型 `double` 和 `symrec *`，并给定名字 `val` 和 `tptr` ，这些名字用在 `%token` 、 `%nterm` 和 `%type` 声明中，为终结符和非终结符指定类型。

```c++
%token <val> expr stmt   // 声明 expr、stmt 类型名称为 val，即 double
```

### %type

每个语义值（即 `$$`）都有其类型，默认为 `int`，可以通过如下方式借助 bison api 修改默认语义值类型。

```c++
%define api.value.type {double}
%define api.value.type {struct semantic_type}
```

也可通过定义宏 `YYSTYPE` 借助编译器修改，值得注意的是，Bison并不知道 `YYSTYPE` 的值，甚至不知道其是否定义，因此无法提供部分支持。

```c++
%define YYSTYPE double
```

当使用 `%union` 指定多值类型时，必须为每个要指定值的非终结符声明值类型。这是通过 `%type` 声明完成的，类似于如下。

```c++
%type <type> nonterminal...
```

这里的 `nonterminal` 是非终结符的名字，`type` 是 `%union` 中声明的可选类型名称。

### %code

在指定位置插入代码。

```c++
%code [place] {
  ... code ...
}
```

`[place]` 用于指定位置，可选项有 `top`、`provides` 、`requires` ，对应的位置分别为文件的顶部、在YYSTYPE与YYLTYPE定义之前和之后。

### %defines

生成解析器头文件，包含语法中定义的标记种类名称的定义及其它一些声明。如果解析器实现文件名为 name.c ，则解析器头文件名称为 name.h ，可通过 `%define api.header.include` 重新设定文件名。

### %define

```
$define variable
$define variable value
$define variable {value}
$define variable "value"
```

**variable**

| variable          | 说明                                     | 默认              | 示例 |
| ----------------- | ---------------------------------------- | ----------------- | ---- |
| api.filename.type | 文件名称在 location 和 position 中的类型 | const std::string |      |
| api.namespace     | 为 parser 类指定 namespace               |                   |      |
| api.parser.class  | 为 parser 类指定类名                     |                   |      |
| api.value.type    | 语义值类型                               |                   |      |

**api.value.type**

| 取值            | 适用语言 | 说明                                                         |
| --------------- | -------- | ------------------------------------------------------------ |
| union-directive | c，c++   | 使用 %union 直接定义，无需指定 api.value.type                |
| union           | c，c++   | 这种方式通过在定义token是指定，比如`%token <int> INT "integer"` ，大多数c++对象不能保存在union中，使用 variant 代替 |
| variant         | c++      | 类似于 union，但是适用于允许任意类型的 c++ 对象              |
| {type}          | -        | 自定义类型                                                   |

```c++
%code requires
{
  struct my_value
  {
    enum
    {
      is_int, is_str
    } kind;
    union
    {
      int ival;
      char *sval;
    } u;
  };
}
%define api.value.type {struct my_value}   // 使用自定义类型
%token <u.ival> INT "integer"
%token <u.sval> STR "string"
```

默认类型：

- 如果定义 `%union` ，则是 union-directive
- 如果使用类型标签（`%token <type> ...`），则是指定类型
- 否则为 undefined

### %parse-param

定义解析器参数，比如。

```c++
%parse-param {int *nastiness} {int *randomness}
```

那么像如下方式，调用解析器。

```c++
{
  int nastiness, randomness;
  …  /* Store proper data in nastiness and randomness. */
  value = yyparse (&nastiness, &randomness);
  …
}
```

在语法的action中，像如下使用变量。

```c++
exp: …    { …; *randomness += 1; … }
```

下面的定义。

```c++
%parse-param {int *randomness}
```

会生成如下签名。

```c++
void yyerror (int *randomness, const char *msg);
int  yyparse (int *randomness);
```

如果 `%define api.pure full` 和 `%locations ` 被使用，那么签名会如下所示。

```c++
void yyerror (YYLTYPE *llocp, int *randomness, const char *msg);
int  yyparse (int *randomness);
```

### %locations

使用 `%locations` 时，c++解析器支持位置追踪，具体参照[这里](https://www.gnu.org/software/bison/manual/html_node/Tracking-Locations.html)。

# 参考

- https://zhuanlan.zhihu.com/p/120812270
- http://dinosaur.compilertools.net/
- http://www.jonathanbeard.io/tutorials/FlexBisonC++
- https://my.oschina.net/Greedxuji/blog/4275989
- 《flex 与 bison》
- https://www.gnu.org/software/bison/manual/html_node/_0025define-Summary.html
- https://www.gnu.org/software/bison/manual/html_node/Parser-Function.html
- https://www.gnu.org/software/bison/manual/html_node/Tracking-Locations.html