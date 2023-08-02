---
title: bazel - usage
categories: 
  - [工具,bazel]
tags:
  - bazel
date: 2021/05/24 00:00:00
update: 2021/05/24 00:00:00
---

# 查看所有 Targets

```shell
$ bazel query //... --output label_kind
```

# 修改输出路径

```shell
# 仍会在项目创建 bazel-* 软链, 一般无需修改
$ bazel --output_base=output build //...       # 修改输出路径
$ bazel --output_user_root=output build //...  # 修改输出 & 安装路径
```

# 使用 github 依赖

**在 WORKSPACE 中指定**

```bazel
http_archive(
    name = "com_google_googleapis",
    strip_prefix = "googleapis-8b976f7c6187f7f68956207b9a154bc278e11d7e",
    urls = ["https://github.com/googleapis/googleapis/archive/8b976f7c6187f7f68956207b9a154bc278e11d7e.tar.gz"],
)
```

> 这里的 8b976f7c6187f7f68956207b9a154bc278e11d7e 为 commit id，下载 url 为 **https://github.com/{user}/{repo}/archive/{commit}.tar.gz**

**BUILD 文件中引用**

```bazel
proto_library(
    name = "person_proto",
    srcs = ["person.proto"],
    deps = [
        "@com_google_googleapis//google/api:annotations_proto",  # 这里引用
        "@com_google_googleapis//google/api:client_proto",
        "@com_google_googleapis//google/api:field_behavior_proto",
        "@com_google_googleapis//google/api:resource_proto",
        "@com_google_protobuf//:empty_proto",
        "@com_google_protobuf//:field_mask_proto",
        "@com_google_protobuf//:any_proto",
    ],
)
```

**proto 中引用**

```protobuf
import "google/api/annotations.proto";
import "google/api/client.proto";
import "google/api/field_behavior.proto";
import "google/api/resource.proto";
```

# 部署 jar 包

**WORKSPACE 中添加依赖**

```bazel
RULES_JVM_EXTERNAL_TAG = "4.0"
RULES_JVM_EXTERNAL_SHA = "31701ad93dbfe544d597dbe62c9a1fdd76d81d8a9150c2bf1ecf928ecdf97169"

http_archive(
    name = "rules_jvm_external",
    strip_prefix = "rules_jvm_external-%s" % RULES_JVM_EXTERNAL_TAG,
    sha256 = RULES_JVM_EXTERNAL_SHA,
    url = "https://github.com/bazelbuild/rules_jvm_external/archive/%s.zip" % RULES_JVM_EXTERNAL_TAG,
)

load("@rules_jvm_external//:defs.bzl", "maven_install")

maven_install(
    artifacts = [
        "junit:junit:4.12",
        "androidx.test.espresso:espresso-core:3.1.1",
        "org.hamcrest:hamcrest-library:1.3",
    ],
    repositories = [
        # Private repositories are supported through HTTP Basic auth
        # "http://test:Test1234@localhost:8081/artifactory/maven-repo-demo",
        "https://maven.google.com",
        "https://repo1.maven.org/maven2",
    ],
)

load("@rules_jvm_external//:repositories.bzl", "rules_jvm_external_deps")
rules_jvm_external_deps()
load("@rules_jvm_external//:setup.bzl", "rules_jvm_external_setup")
rules_jvm_external_setup()
```

**BUILD 文件添加 exporter**

```bazel
java_gapic_library(
    name = "java_cook_gapic",
    srcs = [":cook_proto"],
    gapic_yaml = "cook_gapic.yaml",
    grpc_service_config = "cook_gapic_service_config.json",
    deps = [
        ":java_cook_proto",
    ],
)

# 定义 exporter
java_export(
    name = "java_cook_gapic_export",
    maven_coordinates = "pub.wii.cook:cook-v1:0.0.1",
    # pom_template = "pom.tmpl",  # You can omit this
    # srcs = glob(["*.java"]),    # 如果是 java 项目, 这里部署的是 gapic 生成的 jar 包, 先注释掉
    runtime_deps = [
        ":java_cook_gapic"
    ],
)
```

**执行 exporter**

```shell
# 部署到本地
$ bazel run --define "maven_repo=file://$HOME/.m2/repository" //cook/v1:java_cook_gapic_export.publish

# 部署到 maven 仓库, 注意这里要用 https 协议, 不支持 http
$ bazel run --define "maven_repo=https://127.0.0.1:8081/artifactory/maven-repo-demo" --define "maven_user=test" --define "maven_password=Test1234" //cook/v1:java_cook_gapic_export.publish
```

