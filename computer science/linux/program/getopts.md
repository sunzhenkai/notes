---
title: getopts
categories:
  - [linux, software]
tags:
  - linux
    - getopts
date: 2021/12/14 00:00:00
update: 2021/12/14 00:00:00
---

# 参数

```shell
# opts
:前缀	忽略错误
:后缀	参数后必须有值

# example
:abc:de:	忽略参数错误，-c、-e后必须有值
```

# 示例

```shell
co#!/bin/bash

# define usage info
usage() {
    cat <<EOF
Usage: $0 [-a] [-b name] msg
EOF
}

while getopts ":ab:Bc:" opt; do
    case $opt in
        a) echo "found -a" ; a="hello" ;;
        b) echo "found -b and value is: $OPTARG" ;;
        c) echo "found -c and value is: $OPTARG" ;;
        *) usage ;;
    esac
done

shift $(($OPTIND - 1))

echo "MSG: $1"

if [ -n "${a}" ] ; then         # or [ ! -z "${a}" ]
    echo "-a exists : ${a}"
else
    echo "-a not exists"
fi
```

```shell
#!/bin/bash

usage() {
    cat <<EOF
Usage: $0 [-h host] [-p port]
       $0 [-a host:port]
EOF
}

while getopts "h:p:a:" opt; do
    case $opt in
        h) rhost="$OPTARG" ;;
        p) rport="$OPTARG" ;;
        a) raddress="$OPTARG" ;;
        *) usage ; exit 1 ;;
    esac
done

if [[ ( -z "$raddress" ) && ( -z "$rhost" || -z "$rport" ) ]]; then
    usage
    exit 1
fi
```