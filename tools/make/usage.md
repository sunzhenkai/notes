---
title: makefile 使用
categories: 
  - [工具,makefile]
tags:
  - makefile
date: 2021/02/03 00:00:00
update: 2021/02/03 00:00:00
---

# 格式

```makefile
target ... : prerequisites ...
	command
	...
	...
```

这里 target 无实际意义，类似于定义 scrope / function。

# 使用

## PHONY

定义虚假文件，避免和时间文件冲突，同时可以解决 `make: Nothing to be done for ***` 的异常。

```shell
➜  mf touch test       # 创建空白文件 test
➜  mf cat Makefile     # 打印 Makefile
test:
	ls
➜  mf make test         # 执行 test 目标
make: 'test' is up to date.			# Makefile 的 target 默认为文件，无法对应 Makefile 中定义的 test target
➜  mf vim Makefile      # 添加 .PHONY: test
➜  mf cat Makefile      # 打印 Makefile
.PHONY: test
test:
	ls
➜  mf make test         # 重新执行 target test
ls
Makefile	test
```

## 定义变量

`Makefile`

```makefile
VA := "I'm VA"        # 简单赋值
VB = "I'm VB"         # 递归赋值
VC ?= "I'm VC"        # 条件赋值，如果已定义则忽略
VC ?= "I,m VC Again"  # 测试条件赋值
VA += "I'm VA's Tail" # 追加赋值，以空格
VD := "I'm VD"
VE =  "I'm VE AND "$(VD) # 测试递归赋值
VD = "I'm VDD"

.PHONY: test

test:
	$(eval VF="I'm VF")  # 在 target 里面，这样定义变量
	@echo $(VA)
	@echo $(VB)
	@echo $(VC)
	@echo $(VD)
	@echo $(VE)
	@echo $(VF)
```

**执行**

```shell
$ make
I'm VA I'm VA's Tail
I'm VB
I'm VC
I'm VDD
I'm VE AND I'm VDD
I'm VF
```

## 不打印执行命令

`Makefile`

```makefile
# 以 @ 开头

tgt:
	@echo "HELLO"
```

**输出**

```shell
$ make
HELLO
```

# Example

```makefile
DEPS_DIR:=../../../../deps
LIB_DIR:=$(DEPS_DIR)/lib
BIN_DIR:=$(DEPS_DIR)/bin
INCLUDE_DIR:=$(DEPS_DIR)/include
PATH:=$(DEPS_DIR)/bin:$(PATH)
LD_LIBRARY_PATH=$(LIB_DIR)
LIBRARY_PATH=$(LIB_DIR)
DYLD_LIBRARY_PATH=$(LIB_DIR)
CXXFLAGS=-std=c++11 -L $(LIB_DIR) -I $(INCLUDE_DIR) -Wno-unused-command-line-argument

FBF=parser lexer   	# bison & flex source files
PJF=driver main		# for main programs
FILES=$(addsuffix .cpp, $(PJF))		# source files
OPF=$(addsuffix .o, $(PJF))		# main programs output
FBO=$(addsuffix .o, $(FBF))		# parser & lexer output file
EXE=wc

.PHONY: wc

all: wc

wc: $(FILES)
	@export PATH=$(PATH) && \
		export DYLD_LIBRARY_PATH=$(DYLD_LIBRARY_PATH) && \
		export LIBRARY_PATH=$(LIBRARY_PATH) && \
		$(MAKE) $(FBF) && \
		$(MAKE) $(OPF)  && \
		$(CXX) $(CXXFLAGS) -o $(EXE) $(OPF) $(FBO) && \
		echo "[PROCESS] compile wc done"


parser: parser.yy
	@export PATH=$(PATH) && \
		export DYLD_LIBRARY_PATH=$(DYLD_LIBRARY_PATH) && \
		export LIBRARY_PATH=$(LIBRARY_PATH) && \
		bison -v -d $< && \
		$(CXX) $(CXXFLAGS) -c -o parser.o parser.tab.cc && \
		echo "[PROCESS] compile parser done"

lexer: lexer.l
	@export PATH=$(PATH) && \
		export DYLD_LIBRARY_PATH=$(DYLD_LIBRARY_PATH) && \
		export LIBRARY_PATH=$(LIBRARY_PATH) && \
		flex -V && \
		flex --outfile=lexer.yy.cc $< && \
		$(CXX) $(CXXFLAGS) -c -o lexer.o lexer.yy.cc && \
      	echo "[PROCESS] compile lexer done"

clean:
	@rm parser.tab.* parser.output location.hh position.hh stack.hh lexer.yy.cc \
		$(FBO) $(OPF) $(EXE)

test:
	@wc wc.in%
```

**使用**

```shell
$ make       # make all
$ make test  # test
$ make clean # clean
```

# 参考

- [Ubuntu Wiki](https://wiki.ubuntu.org.cn/%E8%B7%9F%E6%88%91%E4%B8%80%E8%B5%B7%E5%86%99Makefile:MakeFile%E4%BB%8B%E7%BB%8D)