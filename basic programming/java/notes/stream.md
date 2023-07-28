---
title: java stream
categories: 
	- [coding,java,notes]
tags:
	- java
date: 2021/02/07 00:00:00
update: 2021/02/07 00:00:00
---

# collect

**group + toMap**

```java
class Info {
    final String key;
    final String value;

    Info(String key, String value) {
        this.key = key;
        this.value = value;
    }

    public String getKey() {
        return key;
    }

    public String getValue() {
        return value;
    }

    @Override
    public String toString() {
        return "Info{" +
                "key='" + key + '\'' +
                ", value='" + value + '\'' +
                '}';
    }
}

List<Info> infos = new ArrayList<>();
infos.add(new Info("A", "B"));
infos.add(new Info("C", "D"));
Map<String, String> mp = infos.stream().collect(Collectors.toMap(Info::getKey, Info::getValue));
System.out.println(mp);

// 以 Info 的 key 值进行分组
Map<Info, Map<String, String>> data = new HashMap<>();
data.put(new Info("A", "A"), new HashMap<>());
data.put(new Info("A", "B"), new HashMap<>());
data.put(new Info("A", "C"), new HashMap<>());
data.put(new Info("B", "A"), new HashMap<>());
data.put(new Info("B", "B"), new HashMap<>());
data.put(new Info("B", "C"), new HashMap<>());
Map<String, Map<Info, Map<String, String>>> rd = data.entrySet()
        .stream()
        .collect(Collectors.groupingBy(kv -> kv.getKey().getKey(),
                Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue)));
System.out.println(rd);

// output
{A=B, C=D}
{A={Info{key='A', value='B'}={}, Info{key='A', value='A'}={}, Info{key='A', value='C'}={}}, B={Info{key='B', value='A'}={}, Info{key='B', value='B'}={}, Info{key='B', value='C'}={}}}
```

**group + mapping**

```java
// 以 Pair.left group，并合并 Pair.right
List<Pair<String, Map<String, String>>> data = new ArrayList<>();
data.add(Pair.of("A", new HashMap<String, String>(){{put("B", "C");}}));
data.add(Pair.of("D", new HashMap<String, String>(){{put("E", "F");}}));
Map<String, Map<String, String>> r = data.stream().collect(Collectors.groupingBy(Pair::getLeft, Collectors.mapping(Pair::getRight,
        Collector.of(HashMap::new, Map::putAll, (x, y) -> {
            x.putAll(y);
            return x;
        }))));
System.out.println(r);

// output
{A={B=C}, D={E=F}}
```



