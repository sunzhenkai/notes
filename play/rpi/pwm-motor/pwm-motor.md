---
title: 树莓派 - PWM 调速马达
categories: 
  - [play,树莓派]
tags:
  - 树莓派
date: 2020/12/05 18:40:00
update: 2020/12/05 18:40:00
---

# L298N

 ![L298N motor controller board](./pwm-motor/L298N-H-Bridge-Motor-Controller-Annotated-1024x835.jpg)

## 接口

- OUT A，接马达 A
- OUT B ，接马达 B
- POWER，+5V、GND、+12V
    - 5V 电源，接 +5V + GND
    - 12V 电源，接 +12V + GND
- 控制端口，ENA、INA1、INA2、INB1、INB2、ENB
    - 接 GPIO 
    - ENA、INA1、INA2 控制马达 A
    - ENB、INB1、INB2 控制马达 B
