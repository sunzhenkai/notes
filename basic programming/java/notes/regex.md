---
title: java - 正则
categories: 
  - [coding,java,notes]
tags:
  - java
date: "2021-05-11T00:00:00+08:00"
update: "2021-05-11T00:00:00+08:00"
---

# match

```java
// string.match: yes OR no
private static final String REGEX = "^@encrypt\\{(.*)}$";
"@encrypt{file:mysql.username}".match(REGEX); // return true

// Pattern
String REGEX = "^@encrypt\\{(.*)}$";
Pattern PT = Pattern.compile(REGEX);
Matcher m = PT.matcher(value);

m.find();  // find matched subsequence one by one; yes OR no
m.match(); // match entire string; yes OR no

// group
```

