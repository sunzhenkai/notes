---
title: lldb
categories: 
  - [coding, c++, tools, lldb]
tags:
  - c++
    - lldb
date: "2022-01-10T00:00:00+08:00"
update: "2022-01-10T00:00:00+08:00"
---

# 配置

## 忽略 SIGNAL

```shell
process handle -p true -s false -n false SIGINT
process handle -p true -s false -n false SIGUSR1
process handle -p true -s false -n false SIGUSR2
process handle -p false -s false -n false SIGRTMIN
process handle -p false -s false -n false SIGRTMIN+1
process handle -p true -s false -n false SIGRTMIN+11
process handle -p true -s false -n false SIGRTMIN+12
process handle -p true -s false -n false SIGHUP
process handle -p true -s false -n false SIGQUIT
process handle -p true -s false -n false SIGILL
process handle -p true -s false -n false SIGABRT
process handle -p true -s false -n false SIGFPE
process handle -p true -s false -n false SIGSEGV
process handle -p true -s false -n false SIGALRM
process handle -p true -s false -n false SIGCONT
process handle -p true -s false -n false SIGSTOP
process handle -p true -s false -n false SIGTSTP
process handle -p true -s false -n false SIGTTIN
process handle -p true -s false -n false SIGTTOU
process handle -p true -s false -n false SIGTERM
# 或添加在配置文件 ~/.lldbinit 中
```

 # Signals

gdb 和 lldb 的 signal 有些差异，比如 gdb 中的 SIG34 在 lldb 中是 SIGRTMIN，SIG35 对应 SIGRTMIN+1。

## LLDB

```shell
AddSignal(1,      "SIGHUP",       false,    true,   true,   "hangup");
AddSignal(2,      "SIGINT",       true,     true,   true,   "interrupt");
AddSignal(3,      "SIGQUIT",      false,    true,   true,   "quit");
AddSignal(4,      "SIGILL",       false,    true,   true,   "illegal instruction");
AddSignal(5,      "SIGTRAP",      true,     true,   true,   "trace trap (not reset when caught)");
AddSignal(6,      "SIGABRT",      false,    true,   true,   "abort()/IOT trap", "SIGIOT");
AddSignal(7,      "SIGBUS",       false,    true,   true,   "bus error");
AddSignal(8,      "SIGFPE",       false,    true,   true,   "floating point exception");
AddSignal(9,      "SIGKILL",      false,    true,   true,   "kill");
AddSignal(10,     "SIGUSR1",      false,    true,   true,   "user defined signal 1");
AddSignal(11,     "SIGSEGV",      false,    true,   true,   "segmentation violation");
AddSignal(12,     "SIGUSR2",      false,    true,   true,   "user defined signal 2");
AddSignal(13,     "SIGPIPE",      false,    true,   true,   "write to pipe with reading end closed");
AddSignal(14,     "SIGALRM",      false,    false,  false,  "alarm");
AddSignal(15,     "SIGTERM",      false,    true,   true,   "termination requested");
AddSignal(16,     "SIGSTKFLT",    false,    true,   true,   "stack fault");
AddSignal(17,     "SIGCHLD",      false,    false,  true,   "child status has changed", "SIGCLD");
AddSignal(18,     "SIGCONT",      false,    false,  true,   "process continue");
AddSignal(19,     "SIGSTOP",      true,     true,   true,   "process stop");
AddSignal(20,     "SIGTSTP",      false,    true,   true,   "tty stop");
AddSignal(21,     "SIGTTIN",      false,    true,   true,   "background tty read");
AddSignal(22,     "SIGTTOU",      false,    true,   true,   "background tty write");
AddSignal(23,     "SIGURG",       false,    true,   true,   "urgent data on socket");
AddSignal(24,     "SIGXCPU",      false,    true,   true,   "CPU resource exceeded");
AddSignal(25,     "SIGXFSZ",      false,    true,   true,   "file size limit exceeded");
AddSignal(26,     "SIGVTALRM",    false,    true,   true,   "virtual time alarm");
AddSignal(27,     "SIGPROF",      false,    false,  false,  "profiling time alarm");
AddSignal(28,     "SIGWINCH",     false,    true,   true,   "window size changes");
AddSignal(29,     "SIGIO",        false,    true,   true,   "input/output ready/Pollable event", "SIGPOLL");
AddSignal(30,     "SIGPWR",       false,    true,   true,   "power failure");
AddSignal(31,     "SIGSYS",       false,    true,   true,   "invalid system call");
AddSignal(32,     "SIG32",        false,    false,  false,  "threading library internal signal 1");
AddSignal(33,     "SIG33",        false,    false,  false,  "threading library internal signal 2");
AddSignal(34,     "SIGRTMIN",     false,    false,  false,  "real time signal 0");
AddSignal(35,     "SIGRTMIN+1",   false,    false,  false,  "real time signal 1");
AddSignal(36,     "SIGRTMIN+2",   false,    false,  false,  "real time signal 2");
AddSignal(37,     "SIGRTMIN+3",   false,    false,  false,  "real time signal 3");
AddSignal(38,     "SIGRTMIN+4",   false,    false,  false,  "real time signal 4");
AddSignal(39,     "SIGRTMIN+5",   false,    false,  false,  "real time signal 5");
AddSignal(40,     "SIGRTMIN+6",   false,    false,  false,  "real time signal 6");
AddSignal(41,     "SIGRTMIN+7",   false,    false,  false,  "real time signal 7");
AddSignal(42,     "SIGRTMIN+8",   false,    false,  false,  "real time signal 8");
AddSignal(43,     "SIGRTMIN+9",   false,    false,  false,  "real time signal 9");
AddSignal(44,     "SIGRTMIN+10",  false,    false,  false,  "real time signal 10");
AddSignal(45,     "SIGRTMIN+11",  false,    false,  false,  "real time signal 11");
AddSignal(46,     "SIGRTMIN+12",  false,    false,  false,  "real time signal 12");
AddSignal(47,     "SIGRTMIN+13",  false,    false,  false,  "real time signal 13");
AddSignal(48,     "SIGRTMIN+14",  false,    false,  false,  "real time signal 14");
AddSignal(49,     "SIGRTMIN+15",  false,    false,  false,  "real time signal 15");
AddSignal(50,     "SIGRTMAX-14",  false,    false,  false,  "real time signal 16"); // switching to SIGRTMAX-xxx to match "kill -l" output
AddSignal(51,     "SIGRTMAX-13",  false,    false,  false,  "real time signal 17");
AddSignal(52,     "SIGRTMAX-12",  false,    false,  false,  "real time signal 18");
AddSignal(53,     "SIGRTMAX-11",  false,    false,  false,  "real time signal 19");
AddSignal(54,     "SIGRTMAX-10",  false,    false,  false,  "real time signal 20");
AddSignal(55,     "SIGRTMAX-9",   false,    false,  false,  "real time signal 21");
AddSignal(56,     "SIGRTMAX-8",   false,    false,  false,  "real time signal 22");
AddSignal(57,     "SIGRTMAX-7",   false,    false,  false,  "real time signal 23");
AddSignal(58,     "SIGRTMAX-6",   false,    false,  false,  "real time signal 24");
AddSignal(59,     "SIGRTMAX-5",   false,    false,  false,  "real time signal 25");
AddSignal(60,     "SIGRTMAX-4",   false,    false,  false,  "real time signal 26");
AddSignal(61,     "SIGRTMAX-3",   false,    false,  false,  "real time signal 27");
AddSignal(62,     "SIGRTMAX-2",   false,    false,  false,  "real time signal 28");
AddSignal(63,     "SIGRTMAX-1",   false,    false,  false,  "real time signal 29");
AddSignal(64,     "SIGRTMAX",     false,    false,  false,  "real time signal 30");
```

## GDB

```shell
AddSignal(1,      "SIGHUP",       false,    true,   true,   "hangup");
AddSignal(2,      "SIGINT",       true,     true,   true,   "interrupt");
AddSignal(3,      "SIGQUIT",      false,    true,   true,   "quit");
AddSignal(4,      "SIGILL",       false,    true,   true,   "illegal instruction");
AddSignal(5,      "SIGTRAP",      true,     true,   true,   "trace trap (not reset when caught)");
AddSignal(6,      "SIGABRT",      false,    true,   true,   "abort()/IOT trap", "SIGIOT");
AddSignal(7,      "SIGEMT",       false,    true,   true,   "emulation trap");
AddSignal(8,      "SIGFPE",       false,    true,   true,   "floating point exception");
AddSignal(9,      "SIGKILL",      false,    true,   true,   "kill");
AddSignal(10,     "SIGBUS",       false,    true,   true,   "bus error");
AddSignal(11,     "SIGSEGV",      false,    true,   true,   "segmentation violation");
AddSignal(12,     "SIGSYS",       false,    true,   true,   "invalid system call");
AddSignal(13,     "SIGPIPE",      false,    true,   true,   "write to pipe with reading end closed");
AddSignal(14,     "SIGALRM",      false,    false,  false,  "alarm");
AddSignal(15,     "SIGTERM",      false,    true,   true,   "termination requested");
AddSignal(16,     "SIGURG",       false,    true,   true,   "urgent data on socket");
AddSignal(17,     "SIGSTOP",      true,     true,   true,   "process stop");
AddSignal(18,     "SIGTSTP",      false,    true,   true,   "tty stop");
AddSignal(19,     "SIGCONT",      false,    false,  true,   "process continue");
AddSignal(20,     "SIGCHLD",      false,    false,  true,   "child status has changed", "SIGCLD");
AddSignal(21,     "SIGTTIN",      false,    true,   true,   "background tty read");
AddSignal(22,     "SIGTTOU",      false,    true,   true,   "background tty write");
AddSignal(23,     "SIGIO",        false,    true,   true,   "input/output ready/Pollable event");
AddSignal(24,     "SIGXCPU",      false,    true,   true,   "CPU resource exceeded");
AddSignal(25,     "SIGXFSZ",      false,    true,   true,   "file size limit exceeded");
AddSignal(26,     "SIGVTALRM",    false,    true,   true,   "virtual time alarm");
AddSignal(27,     "SIGPROF",      false,    false,  false,  "profiling time alarm");
AddSignal(28,     "SIGWINCH",     false,    true,   true,   "window size changes");
AddSignal(29,     "SIGLOST",      false,    true,   true,   "resource lost");
AddSignal(30,     "SIGUSR1",      false,    true,   true,   "user defined signal 1");
AddSignal(31,     "SIGUSR2",      false,    true,   true,   "user defined signal 2");
AddSignal(32,     "SIGPWR",       false,    true,   true,   "power failure");
AddSignal(33,     "SIGPOLL",      false,    true,   true,   "pollable event");
AddSignal(34,     "SIGWIND",      false,    true,   true,   "SIGWIND");
AddSignal(35,    "SIGPHONE",      false,    true,   true,   "SIGPHONE");
AddSignal(36,  "SIGWAITING",      false,    true,   true,   "process's LWPs are blocked");
AddSignal(37,      "SIGLWP",      false,    true,   true,   "signal LWP");
AddSignal(38,   "SIGDANGER",      false,    true,   true,   "swap space dangerously low");
AddSignal(39,    "SIGGRANT",      false,    true,   true,   "monitor mode granted");
AddSignal(40,  "SIGRETRACT",      false,    true,   true,   "need to relinquish monitor mode");
AddSignal(41,      "SIGMSG",      false,    true,   true,   "monitor mode data available");
AddSignal(42,    "SIGSOUND",      false,    true,   true,   "sound completed");
AddSignal(43,      "SIGSAK",      false,    true,   true,   "secure attention");
AddSignal(44,     "SIGPRIO",      false,    true,   true,   "SIGPRIO");
AddSignal(45,       "SIG33",      false,    false,  false,  "real-time event 33");
AddSignal(46,       "SIG34",      false,    false,  false,  "real-time event 34");
AddSignal(47,       "SIG35",      false,    false,  false,  "real-time event 35");
AddSignal(48,       "SIG36",      false,    false,  false,  "real-time event 36");
AddSignal(49,       "SIG37",      false,    false,  false,  "real-time event 37");
AddSignal(50,       "SIG38",      false,    false,  false,  "real-time event 38");
AddSignal(51,       "SIG39",      false,    false,  false,  "real-time event 39");
AddSignal(52,       "SIG40",      false,    false,  false,  "real-time event 40");
AddSignal(53,       "SIG41",      false,    false,  false,  "real-time event 41");
AddSignal(54,       "SIG42",      false,    false,  false,  "real-time event 42");
AddSignal(55,       "SIG43",      false,    false,  false,  "real-time event 43");
AddSignal(56,       "SIG44",      false,    false,  false,  "real-time event 44");
AddSignal(57,       "SIG45",      false,    false,  false,  "real-time event 45");
AddSignal(58,       "SIG46",      false,    false,  false,  "real-time event 46");
AddSignal(59,       "SIG47",      false,    false,  false,  "real-time event 47");
AddSignal(60,       "SIG48",      false,    false,  false,  "real-time event 48");
AddSignal(61,       "SIG49",      false,    false,  false,  "real-time event 49");
AddSignal(62,       "SIG50",      false,    false,  false,  "real-time event 50");
AddSignal(63,       "SIG51",      false,    false,  false,  "real-time event 51");
AddSignal(64,       "SIG52",      false,    false,  false,  "real-time event 52");
AddSignal(65,       "SIG53",      false,    false,  false,  "real-time event 53");
AddSignal(66,       "SIG54",      false,    false,  false,  "real-time event 54");
AddSignal(67,       "SIG55",      false,    false,  false,  "real-time event 55");
AddSignal(68,       "SIG56",      false,    false,  false,  "real-time event 56");
AddSignal(69,       "SIG57",      false,    false,  false,  "real-time event 57");
AddSignal(70,       "SIG58",      false,    false,  false,  "real-time event 58");
AddSignal(71,       "SIG59",      false,    false,  false,  "real-time event 59");
AddSignal(72,       "SIG60",      false,    false,  false,  "real-time event 60");
AddSignal(73,       "SIG61",      false,    false,  false,  "real-time event 61");
AddSignal(74,       "SIG62",      false,    false,  false,  "real-time event 62");
AddSignal(75,       "SIG63",      false,    false,  false,  "real-time event 63");
AddSignal(76,   "SIGCANCEL",      false,    true,   true,   "LWP internal signal");
AddSignal(77,       "SIG32",      false,    false,  false,  "real-time event 32");
AddSignal(78,       "SIG64",      false,    false,  false,  "real-time event 64");
AddSignal(79,       "SIG65",      false,    false,  false,  "real-time event 65");
AddSignal(80,       "SIG66",      false,    false,  false,  "real-time event 66");
AddSignal(81,       "SIG67",      false,    false,  false,  "real-time event 67");
AddSignal(82,       "SIG68",      false,    false,  false,  "real-time event 68");
AddSignal(83,       "SIG69",      false,    false,  false,  "real-time event 69");
AddSignal(84,       "SIG70",      false,    false,  false,  "real-time event 70");
AddSignal(85,       "SIG71",      false,    false,  false,  "real-time event 71");
AddSignal(86,       "SIG72",      false,    false,  false,  "real-time event 72");
AddSignal(87,       "SIG73",      false,    false,  false,  "real-time event 73");
AddSignal(88,       "SIG74",      false,    false,  false,  "real-time event 74");
AddSignal(89,       "SIG75",      false,    false,  false,  "real-time event 75");
AddSignal(90,       "SIG76",      false,    false,  false,  "real-time event 76");
AddSignal(91,       "SIG77",      false,    false,  false,  "real-time event 77");
AddSignal(92,       "SIG78",      false,    false,  false,  "real-time event 78");
AddSignal(93,       "SIG79",      false,    false,  false,  "real-time event 79");
AddSignal(94,       "SIG80",      false,    false,  false,  "real-time event 80");
AddSignal(95,       "SIG81",      false,    false,  false,  "real-time event 81");
AddSignal(96,       "SIG82",      false,    false,  false,  "real-time event 82");
AddSignal(97,       "SIG83",      false,    false,  false,  "real-time event 83");
AddSignal(98,       "SIG84",      false,    false,  false,  "real-time event 84");
AddSignal(99,       "SIG85",      false,    false,  false,  "real-time event 85");
AddSignal(100,      "SIG86",      false,    false,  false,  "real-time event 86");
AddSignal(101,      "SIG87",      false,    false,  false,  "real-time event 87");
AddSignal(102,      "SIG88",      false,    false,  false,  "real-time event 88");
AddSignal(103,      "SIG89",      false,    false,  false,  "real-time event 89");
AddSignal(104,      "SIG90",      false,    false,  false,  "real-time event 90");
AddSignal(105,      "SIG91",      false,    false,  false,  "real-time event 91");
AddSignal(106,      "SIG92",      false,    false,  false,  "real-time event 92");
AddSignal(107,      "SIG93",      false,    false,  false,  "real-time event 93");
AddSignal(108,      "SIG94",      false,    false,  false,  "real-time event 94");
AddSignal(109,      "SIG95",      false,    false,  false,  "real-time event 95");
AddSignal(110,      "SIG96",      false,    false,  false,  "real-time event 96");
AddSignal(111,      "SIG97",      false,    false,  false,  "real-time event 97");
AddSignal(112,      "SIG98",      false,    false,  false,  "real-time event 98");
AddSignal(113,      "SIG99",      false,    false,  false,  "real-time event 99");
AddSignal(114,     "SIG100",      false,    false,  false,  "real-time event 100");
AddSignal(115,     "SIG101",      false,    false,  false,  "real-time event 101");
AddSignal(116,     "SIG102",      false,    false,  false,  "real-time event 102");
AddSignal(117,     "SIG103",      false,    false,  false,  "real-time event 103");
AddSignal(118,     "SIG104",      false,    false,  false,  "real-time event 104");
AddSignal(119,     "SIG105",      false,    false,  false,  "real-time event 105");
AddSignal(120,     "SIG106",      false,    false,  false,  "real-time event 106");
AddSignal(121,     "SIG107",      false,    false,  false,  "real-time event 107");
AddSignal(122,     "SIG108",      false,    false,  false,  "real-time event 108");
AddSignal(123,     "SIG109",      false,    false,  false,  "real-time event 109");
AddSignal(124,     "SIG110",      false,    false,  false,  "real-time event 110");
AddSignal(125,     "SIG111",      false,    false,  false,  "real-time event 111");
AddSignal(126,     "SIG112",      false,    false,  false,  "real-time event 112");
AddSignal(127,     "SIG113",      false,    false,  false,  "real-time event 113");
AddSignal(128,     "SIG114",      false,    false,  false,  "real-time event 114");
AddSignal(129,     "SIG115",      false,    false,  false,  "real-time event 115");
AddSignal(130,     "SIG116",      false,    false,  false,  "real-time event 116");
AddSignal(131,     "SIG117",      false,    false,  false,  "real-time event 117");
AddSignal(132,     "SIG118",      false,    false,  false,  "real-time event 118");
AddSignal(133,     "SIG119",      false,    false,  false,  "real-time event 119");
AddSignal(134,     "SIG120",      false,    false,  false,  "real-time event 120");
AddSignal(135,     "SIG121",      false,    false,  false,  "real-time event 121");
AddSignal(136,     "SIG122",      false,    false,  false,  "real-time event 122");
AddSignal(137,     "SIG123",      false,    false,  false,  "real-time event 123");
AddSignal(138,     "SIG124",      false,    false,  false,  "real-time event 124");
AddSignal(139,     "SIG125",      false,    false,  false,  "real-time event 125");
AddSignal(140,     "SIG126",      false,    false,  false,  "real-time event 126");
AddSignal(141,     "SIG127",      false,    false,  false,  "real-time event 127");
AddSignal(142,    "SIGINFO",      false,    true,   true,   "information request");
AddSignal(143,    "unknown",      false,    true,   true,   "unknown signal");
AddSignal(145,      "EXC_BAD_ACCESS",       false,  true,   true,   "could not access memory");
AddSignal(146, "EXC_BAD_INSTRUCTION",       false,  true,   true,   "illegal instruction/operand");
AddSignal(147,      "EXC_ARITHMETIC",       false,  true,   true,   "arithmetic exception");
AddSignal(148,       "EXC_EMULATION",       false,  true,   true,   "emulation instruction");
AddSignal(149,        "EXC_SOFTWARE",       false,  true,   true,   "software generated exception");
AddSignal(150,      "EXC_BREAKPOINT",       false,  true,   true,   "breakpoint");
AddSignal(151,   "SIGLIBRT",      false,    true,   true,   "librt internal signal");
```

#  命令

## 查看所有 handle

```shell
(lldb) process handle
NAME         PASS   STOP   NOTIFY
===========  =====  =====  ======
SIGHUP       true   true   true 
SIGINT       true   false  true 
SIGQUIT      true   true   true 
SIGILL       true   true   true 
SIGTRAP      false  true   true 
SIGABRT      true   true   true 
SIGBUS       true   false  true 
SIGFPE       true   true   true 
SIGKILL      true   true   true 
SIGUSR1      true   false  true 
SIGSEGV      true   true   true 
SIGUSR2      true   false  true 
SIGPIPE      true   true   true 
SIGALRM      true   false  false
SIGTERM      true   true   true 
SIGSTKFLT    true   true   true 
SIGCHLD      true   false  true 
SIGCONT      true   false  true 
SIGSTOP      false  true   true 
SIGTSTP      true   true   true 
SIGTTIN      true   true   true 
SIGTTOU      true   true   true 
SIGURG       true   true   true 
SIGXCPU      true   true   true 
SIGXFSZ      true   true   true 
SIGVTALRM    true   true   true 
SIGPROF      true   false  false
SIGWINCH     true   true   true 
SIGIO        true   true   true 
SIGPWR       true   true   true 
SIGSYS       true   true   true 
SIG32        true   false  false
SIG33        true   false  false
SIGRTMIN     true   false  false
SIGRTMIN+1   true   false  false
SIGRTMIN+2   true   false  false
SIGRTMIN+3   true   false  false
SIGRTMIN+4   true   false  false
SIGRTMIN+5   true   false  false
SIGRTMIN+6   true   false  false
SIGRTMIN+7   true   false  false
SIGRTMIN+8   true   false  false
SIGRTMIN+9   true   false  false
SIGRTMIN+10  true   false  false
SIGRTMIN+11  true   false  false
SIGRTMIN+12  true   false  false
SIGRTMIN+13  true   false  false
SIGRTMIN+14  true   false  false
SIGRTMIN+15  true   false  false
SIGRTMAX-14  true   false  false
SIGRTMAX-13  true   false  false
SIGRTMAX-12  true   false  false
SIGRTMAX-11  true   false  false
SIGRTMAX-10  true   false  false
SIGRTMAX-9   true   false  false
SIGRTMAX-8   true   false  false
SIGRTMAX-7   true   false  false
SIGRTMAX-6   true   false  false
SIGRTMAX-5   true   false  false
SIGRTMAX-4   true   false  false
SIGRTMAX-3   true   false  false
SIGRTMAX-2   true   false  false
SIGRTMAX-1   true   false  false
SIGRTMAX     true   false  false
```

