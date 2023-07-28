---
title: 树莓派连接游戏手柄
categories: 
	- [play,树莓派]
tags:
	- 树莓派
date: 2020/12/05 18:40:00
update: 2020/12/05 18:40:00
---

# 驱动

## xpadneo

### 依赖

```shell
# Raspbian
$ sudo apt install dkms raspberrypi-kernel-headers
```

### 安装

```shell
$ git clone https://github.com/atar-axis/xpadneo.git
$ cd xpadneo
$ sudo ./install.sh

# 如遇如下报错
# Your kernel headers for kernel 4.19.97-v7l+ cannot be found at
# /lib/modules/4.19.97-v7l+/build or /lib/modules/4.19.97-v7l+/source.
# 将 /lib/modules 下拷贝一份至缺失版本，如:
# sudo cp -r /lib/modules/5.4.79-v7l+ /lib/modules/4.19.97-v7l+
```

### 连接

```shell
$ bluetoothctl
$ [bluetooth]# scan on
...
# 长按xbox前侧配对键，至指示灯快速闪烁，出下如下新设备，记录其mac地址
[NEW] Device <MAC> Xbox Wireless Controller
...
[bluetooth]# pairable on
[bluetooth]# power on
[bluetooth]# pair <MAC>
[bluetooth]# trust <MAC>
[bluetooth]# connect <MAC>

# 如若报 Failed to connect: org.bluez.Error.Failed 错误，执行如下命令并重启系统
$ echo 'options bluetooth disable_ertm=Y' | sudo tee -a /etc/modprobe.d/bluetooth.conf
```

### 使用

#### Python

**安装依赖**

```shell
$ sudo pip3 install evdev asyncio
```

**测试**

```python
$ cd xpadneo/misc/examples # 克隆下来的Git仓库
$ python3 python_asyncio_evdev/gamepad.py
press x to stop, Y to rumble light, B to rumble once, trigger and joystick right to see analog value
 trigger_right =  32.98   joystick_right_x =  0
  
# 如果一切顺利，按手柄Y会感受到长震动；按B会感受到短震动；按X退出程序
```

**按键**

| 按键       | code | type | 值类型        |
| ---------- | ---- | ---- | ------------- |
| LT         | 10   | 03   | 区间，0~1023  |
| RT         | 09   | 03   | 区间，0~1023  |
| LB         | 310  | 01   | 单值，00，01  |
| RB         | 311  | 01   | 单值，00，01  |
| 左摇杆 Y轴 | 01   | 03   | 区间，0~65535 |
| 左摇杆 X轴 | 00   | 03   | 区间，0~65535 |
| 右摇杆 Y轴 | 05   | 03   | 区间，0~65535 |
| 右摇杆 X轴 | 02   | 03   | 区间，0~65535 |
| 视图       | 158  | 01   | 单值，00，01  |
| 菜单       | 315  | 01   | 单值，00，01  |
| 十字键 上  | 17   | 03   | 单值，00，-1  |
| 十字键 下  | 17   | 03   | 单值，00，01  |
| 十字键 左  | 16   | 03   | 单值，00，-1  |
| 十字键 右  | 16   | 03   | 单值，00，01  |
| Y          | 308  | 01   | 单值，00，01  |
| X          | 307  | 01   | 单值，00，01  |
| A          | 304  | 01   | 单值，00，01  |
| B          | 305  | 01   | 单值，00，01  |

**注**

- 摇杆X轴左侧为0，Y轴上侧为0