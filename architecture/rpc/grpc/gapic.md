---
title: gapis
categories: 
    - [架构, rpc, gRPC]
tags:
    - gapis
    - gRPC
date: 2021/05/24 00:00:00
update: 2021/05/24 00:00:00
---

# Introduction

## 打包

使用 gRPC + protocol buffers 时，会面临三种打包方式，`proto library`、`grpc library`、`gapic library` 。不同的打包方式需要使用不同的工具/插件，以如下定义为例。

```protobuf
syntax = "proto3";

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
```

### proto library

首先是打包 proto library，需要下载 protoc 程序（在 [protobuf](https://github.com/protocolbuffers/protobuf) 的 release 页面下载）。

```shell
$ protoc --java_out=jv greeter.proto
```

这个命令只会生成数据结构，会忽略 service 定义。

### gRPC library

然后，是打包 gRPC library，需要下载对应的 generator，工具下载 / 本地编译步骤参考[这里](https://github.com/grpc/grpc-java/tree/master/compiler)，另外 gRPC 相关的库及代码在[这里](https://github.com/grpc)，命令参考如下。

```shell
$ protoc --plugin=protoc-gen-grpc-java=/Users/wii/Downloads/protoc-gen-grpc-java-1.38.0-osx-x86_64.exe --grpc-java_out=jv --java_out=jv greeter.proto
```

gRPC library 和 proto library 的区别是，会生成用于服务调用的 client 和 server 端代码。

### gapic library

最后，是打包 gapic library，同样需要下载对应的 generator，以 Java 为例，工具参考[gapic-generator-java](https://github.com/googleapis/gapic-generator-java)和[gapic-generator](https://github.com/googleapis/gapic-generator)。顺便，[artman](https://github.com/googleapis/artman) 作为一个可选的生成工具，已经停止维护。要打包 java 的 gapic library ，首先需要编译插件，从[gapic-generator](https://github.com/googleapis/gapic-generator) 下载  release 包，运行命令 `./gradlew fatjar` 进行编译。

首先，生成 description 文件。

```shell
$ protoc --include_imports --include_source_info -o greeter.description greeter.proto
```

接着，生成 proto message classes。

```shell
$ mkdir java-proto-lib-out
$ protoc --java_out=java-proto-lib-out greeter.proto
```

然后，生成 gRPC stub 。

```shell
$ mkdir java-grpc-lib-out
$ protoc --plugin=protoc-gen-grpc=/Users/wii/Downloads/protoc-gen-grpc-java-1.38.0-osx-x86_64.exe --grpc_out=java-grpc-lib-out greeter.proto
```

进一步，新建服务描述文件。

```yaml
type: google.api.Service
config_version: 3
name: greeter.gapic.cook.pub.wii

title: Example Library API
```

接着，生成客户端配置文件。

```shell
java -XX:-OmitStackTraceInFastThrow -cp /Users/wii/Downloads/gapic-generator-2.11.1/build/libs/gapic-generator-2.11.1-fatjar.jar \
    com.google.api.codegen.GeneratorMain GAPIC_CONFIG \
    --descriptor_set=greeter.proto.pb \
    --service_yaml=greeter-service.yaml \
    -o=/Users/wii/Data/tmp/grpc/greeter-gapic-config.yaml
# 输出文件使用绝对路径
```

然后，创建 package 的 metadata 配置文件。

```yaml
artifact_type: GAPIC
proto_deps:
- google-common-protos
api_name: greeter
api_version: v1
organization_name: solo-kingdom
proto_path: wii/cook/gapic/greeter/v1
```

最后，生成代码。

**java**

```shell
java -cp /Users/wii/Downloads/gapic-generator-2.11.1/build/libs/gapic-generator-2.11.1-fatjar.jar \
    com.google.api.codegen.GeneratorMain LEGACY_GAPIC_AND_PACKAGE \
    --descriptor_set=greeter.proto.pb \
    --service_yaml=greeter-service.yaml \
    --gapic_yaml=greeter-gapic-config.yaml \
    --package_yaml2=greeter-meta-config.yaml \
    --language=java \
    --o=java-code-gen
```

**python**

```shell
java -cp /Users/wii/Downloads/gapic-generator-2.11.1/build/libs/gapic-generator-2.11.1-fatjar.jar \
    com.google.api.codegen.GeneratorMain LEGACY_GAPIC_AND_PACKAGE \
    --descriptor_set=greeter.proto.pb \
    --service_yaml=greeter-service.yaml \
    --gapic_yaml=greeter-gapic-config.yaml \
    --language=python \
    --package_yaml2=greeter-meta-config.yaml \
    --o=python-code-gen
```

顺便，[这里](https://github.com/sunzhenkai/cook-grpc/tree/master/cook-gapic-playground)提供了一个示例。

最后，在使用 gapic 时，可能需要引用一些 google 的 proto 文件，比如 `google/api/annotation.proto` ，这些文件定义在[这里](https://github.com/googleapis/api-common-protos/tree/master/google)。

# Bazel

## rules_proto

## 获取 sha256

```shell
$ COMMIT_ID=734b8d41d39a903c70132828616f26cb2c7f908c
$ wget https://github.com/stackb/rules_proto/archive/${COMMIT_ID}.tar.gz
$ shasum -a 256 ${COMMIT_ID}.tar.gz
c89348b73f4bc59c0add4074cc0c620a5a2a08338eb4ef207d57eaa8453b82e8
```

# Artman

```shell
# install
$ pip3 install googleapis-artman
```

# 配置文件

生成 gapic 库时，指定的配置文件。

```bazel
java_gapic_library(
    name = "java_cook_gapic",
    srcs = [":cook_proto"],
    gapic_yaml = "cook_gapic.yaml",  # 这里指定的文件
    grpc_service_config = "cook_gapic_service_config.json",
    deps = [
        ":java_cook_proto",
        ":java_cook_grpc"
    ],
)
```

配置参考 `auth.proto` 内定义的 Authentication 结构。

```protobuf
// `Authentication` defines the authentication configuration for API methods
// provided by an API service.
//
// Example:
//
//     name: calendar.googleapis.com
//     authentication:
//       providers:
//       - id: google_calendar_auth
//         jwks_uri: https://www.googleapis.com/oauth2/v1/certs
//         issuer: https://securetoken.google.com
//       rules:
//       - selector: "*"
//         requirements:
//           provider_id: google_calendar_auth
//       - selector: google.calendar.Delegate
//         oauth:
//           canonical_scopes: https://www.googleapis.com/auth/calendar.read
message Authentication {
  // A list of authentication rules that apply to individual API methods.
  //
  // **NOTE:** All service configuration rules follow "last one wins" order.
  repeated AuthenticationRule rules = 3;

  // Defines a set of authentication providers that a service supports.
  repeated AuthProvider providers = 4;
}
```

可以看到，有两个字段，rules & providers。对于 rules，数据结构为 AuthenticationRule。

```protobuf
// Authentication rules for the service.
//
// By default, if a method has any authentication requirements, every request
// must include a valid credential matching one of the requirements.
// It's an error to include more than one kind of credential in a single
// request.
//
// If a method doesn't have any auth requirements, request credentials will be
// ignored.
message AuthenticationRule {
  // Selects the methods to which this rule applies.
  //
  // Refer to [selector][google.api.DocumentationRule.selector] for syntax details.
  string selector = 1;

  // The requirements for OAuth credentials.
  OAuthRequirements oauth = 2;

  // If true, the service accepts API keys without any other credential.
  // This flag only applies to HTTP and gRPC requests.
  bool allow_without_credential = 5;

  // Requirements for additional authentication providers.
  repeated AuthRequirement requirements = 7;
}
```

示例如下。

```
type: google.api.Service
config_version: 3
name: analyticsadmin.googleapis.com
title: Google Analytics Admin API

# 横线开头定义数组
apis:
- name: google.analytics.admin.v1alpha.AnalyticsAdminService

authentication:
  rules:
  - selector: 'google.analytics.admin.v1alpha.AnalyticsAdminService.*'
    oauth:
      canonical_scopes: |-
        https://www.googleapis.com/auth/analytics.edit
  - selector: '*'
  	allow_without_credential: true  # 无需认证
```

# Reference

- [rules_proto](https://github.com/stackb/rules_proto)
- [rules_proto](https://github.com/bazelbuild/rules_proto)

