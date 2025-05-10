---
title: bazel - deps
categories: 
  - [工具,bazel]
tags:
  - bazel
date: "2021-07-01T00:00:00+08:00"
update: "2021-07-01T00:00:00+08:00"
---

# google-apis

```bazel
http_archive(
    name = "com_google_googleapis",
    strip_prefix = "googleapis-8b976f7c6187f7f68956207b9a154bc278e11d7e",
    urls = ["https://github.com/googleapis/googleapis/archive/8b976f7c6187f7f68956207b9a154bc278e11d7e.tar.gz"],
)

load("@com_google_googleapis//:repository_rules.bzl", "switched_rules_by_language")

switched_rules_by_language(
    name = "com_google_googleapis_imports",
    gapic = True,
    grpc = True,
    java = True,
    python = True,
)
```

# google api common protos

```bazel
com_google_googleapis 包含了 common protos; 暂时保留
http_archive(
    name = "com_google_api_common_protos",
    strip_prefix = "api-common-protos-1db64f2e971e7ea0e15769164a67643539f0994f",
    urls = ["https://github.com/googleapis/api-common-protos/archive/1db64f2e971e7ea0e15769164a67643539f0994f.tar.gz"],
)
```

