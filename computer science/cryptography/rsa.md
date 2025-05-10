---
title: rsa 加密解密
categories: 
  - [计算机科学,密码学]
tags:
  - 密码学
date: "2021-11-29T00:00:00+08:00"
update: "2021-11-29T00:00:00+08:00"
---

# 数据

## 公钥

```
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCOhQ81fJEKI/b0+iKtK0/WN7wcMJKuGL5QhzuRDyFLCADbKPkB7uGKfkQ1QDcntjZ8k4+mx2oGBKF5E1vSB+bD7SP7fkSgDmdCzGLSJX04Q9H95xuEfFsTXwW8dGh4uQDFt/dTIY2WAx8RnGhiJFKq6y9mj+tcofnzLbQNfy2PoQIDAQAB
```

## 私密

```
MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAI6FDzV8kQoj9vT6Iq0rT9Y3vBwwkq4YvlCHO5EPIUsIANso+QHu4Yp+RDVANye2NnyTj6bHagYEoXkTW9IH5sPtI/t+RKAOZ0LMYtIlfThD0f3nG4R8WxNfBbx0aHi5AMW391MhjZYDHxGcaGIkUqrrL2aP61yh+fMttA1/LY+hAgMBAAECgYBuMZNA17+NB6G6aGzHV+WyzAU2Bphi497ChM0Zq4kial2/Fj7xr7HTUy2Jvszmd4xJZg579VOUs5/l7YHhMxrI2sUadaenkdJ/LmdHICRT4BAFdDnM78UsY1/YgtoA06r63ZkaE6PJ2UPMCgcYMqV5OkAFwt8oTDSGlBb4EZuUAQJBAMbR+tolF96tHPb96BKbowIytRQZpC3KMutnzY74davY4BvAnvzoUTs0d89Xi+1+YxmI0UahejGdyMEWOryNJYkCQQC3gf3B8Kmaic3hz1ghslsdY5n1sE8piJH/9owvToc54MVQc9sfFC9f+e6v8yjblHFeaoYTL6NUz9MUmeHAgatZAkB+VGnaNnuGR+UBo6/UMwROnz2jue8yESptnZVlZMYQHUu5FplvBYan4dzG6E/G5em+Dcs739qusB0hYyiLKfxRAkAiGKweqenJhgtUBqOYdzxIxKXpqZ272N1P0u6PJ6cmkOX4od438xcuXREFbkfMLNO3uFE7JWHSs17D+CejDjTZAkAWlJVrwvcgdPDun/xF2FK8YoonJFPJxFD/jrVPuoZ+HxYa9sytwuaAU8jTv8WDF4er1ZO4N3TENE+SedxuH0zW
```

## 数据串

```
hello world
```

## 加密

### java

```
UgnRdVY7thSMN8dM5gg+wcMu7g8PmQclLFnoswkT9J8aB8RfU+LQhfKupRVifipg03LvVGedqQmXyF5Gz8AoDIW22q5kpLxpdS3sZdf2kQY6snDSHubtPszG+/jB05fYaCGCPvoJw1oD+HHWl6dF5GvTYvLcZykRAJtvr5vCjTg=
```

### node

```
iQMK9U8wYsLdhssRVRVY0CA40SdM3PEP7KhuP74ICPA7AH0ckUw5Rq9C8RKAIBh0fO8hIYC+kPN9xUCKNUlFGy09xtBEOgRybg8JZZC8mEjeA0hHMbQePI4fxQa74IWYY646ihj7KCtaE55yE6G8yV7hRPFyjdPJieXEKhSJsmM=
```

### js

```
hOv454LZNZhPoS2nbtnH7S1phhkdVVX0NtF7xx37H4tNKelTguQ0i/obZXBGVRC7FoP0CAP7lrqo/VlT276D9kLXHUGSl/9FW1Q4fNcj4iMZedjcQJaZNOSZ4Vlti/9cXUeuUXaGG6vS3V49EfMy/FELFy+zpbijcnrIAar6uh4=
```

## 解密

| 加密\解密 | java     | node     | js       |
| --------- | -------- | -------- | -------- |
| java      | 可以解密 | 可以解密 | 可以解密 |
| node      | 可以解密 | 可以解密 | 可以解密 |
| js        | 可以解密 | 可以解密 | 可以解密 |

# Java

```java
package pub.wii.cook.springboot.utils;

import lombok.SneakyThrows;

import javax.crypto.Cipher;
import java.security.KeyFactory;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

public class RSAUtil {

    private final static String publicKey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCOhQ81fJEKI/b0+iKtK0/WN7wcMJKuGL5QhzuRDyFLCADbKPkB7uGKfkQ1QDcntjZ8k4+mx2oGBKF5E1vSB+bD7SP7fkSgDmdCzGLSJX04Q9H95xuEfFsTXwW8dGh4uQDFt/dTIY2WAx8RnGhiJFKq6y9mj+tcofnzLbQNfy2PoQIDAQAB";
    private final static String privateKey = "MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAI6FDzV8kQoj9vT6Iq0rT9Y3vBwwkq4YvlCHO5EPIUsIANso+QHu4Yp+RDVANye2NnyTj6bHagYEoXkTW9IH5sPtI/t+RKAOZ0LMYtIlfThD0f3nG4R8WxNfBbx0aHi5AMW391MhjZYDHxGcaGIkUqrrL2aP61yh+fMttA1/LY+hAgMBAAECgYBuMZNA17+NB6G6aGzHV+WyzAU2Bphi497ChM0Zq4kial2/Fj7xr7HTUy2Jvszmd4xJZg579VOUs5/l7YHhMxrI2sUadaenkdJ/LmdHICRT4BAFdDnM78UsY1/YgtoA06r63ZkaE6PJ2UPMCgcYMqV5OkAFwt8oTDSGlBb4EZuUAQJBAMbR+tolF96tHPb96BKbowIytRQZpC3KMutnzY74davY4BvAnvzoUTs0d89Xi+1+YxmI0UahejGdyMEWOryNJYkCQQC3gf3B8Kmaic3hz1ghslsdY5n1sE8piJH/9owvToc54MVQc9sfFC9f+e6v8yjblHFeaoYTL6NUz9MUmeHAgatZAkB+VGnaNnuGR+UBo6/UMwROnz2jue8yESptnZVlZMYQHUu5FplvBYan4dzG6E/G5em+Dcs739qusB0hYyiLKfxRAkAiGKweqenJhgtUBqOYdzxIxKXpqZ272N1P0u6PJ6cmkOX4od438xcuXREFbkfMLNO3uFE7JWHSs17D+CejDjTZAkAWlJVrwvcgdPDun/xF2FK8YoonJFPJxFD/jrVPuoZ+HxYa9sytwuaAU8jTv8WDF4er1ZO4N3TENE+SedxuH0zW";

    @SneakyThrows
    public static PublicKey getPublicKey(String base64PublicKey) {
        PublicKey publicKey;
        X509EncodedKeySpec keySpec =
                new X509EncodedKeySpec(Base64.getDecoder().decode(base64PublicKey.getBytes()));
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        publicKey = keyFactory.generatePublic(keySpec);
        return publicKey;
    }

    @SneakyThrows
    public static PrivateKey getPrivateKey(String base64PrivateKey) {
        PKCS8EncodedKeySpec keySpec =
                new PKCS8EncodedKeySpec(Base64.getDecoder().decode(base64PrivateKey.getBytes()));
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        return keyFactory.generatePrivate(keySpec);
    }

    @SneakyThrows
    public static String encrypt(String data, String publicKey) {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.ENCRYPT_MODE, getPublicKey(publicKey));
        return Base64.getEncoder().encodeToString(cipher.doFinal(data.getBytes()));
    }

    @SneakyThrows
    public static String decrypt(byte[] data, PrivateKey privateKey) {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.DECRYPT_MODE, privateKey);
        return new String(cipher.doFinal(data));
    }

    public static String decrypt(String data, String base64PrivateKey) {
        return decrypt(Base64.getDecoder().decode(data.getBytes()), getPrivateKey(base64PrivateKey));
    }

    public static void main(String[] args) {
        // 加密
        String encryptedString = encrypt("hello world", publicKey);
        System.out.println(encryptedString);
        // 解密
        String decryptedString = RSAUtil.decrypt(encryptedString, privateKey);
        System.out.println(decryptedString);
    }
}
```

# Node

```shell
npm i node-rsa
```

```js
const NodeRSA = require('node-rsa')
const privateKey = 'MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAI6FDzV8kQoj9vT6Iq0rT9Y3vBwwkq4YvlCHO5EPIUsIANso+QHu4Yp+RDVANye2NnyTj6bHagYEoXkTW9IH5sPtI/t+RKAOZ0LMYtIlfThD0f3nG4R8WxNfBbx0aHi5AMW391MhjZYDHxGcaGIkUqrrL2aP61yh+fMttA1/LY+hAgMBAAECgYBuMZNA17+NB6G6aGzHV+WyzAU2Bphi497ChM0Zq4kial2/Fj7xr7HTUy2Jvszmd4xJZg579VOUs5/l7YHhMxrI2sUadaenkdJ/LmdHICRT4BAFdDnM78UsY1/YgtoA06r63ZkaE6PJ2UPMCgcYMqV5OkAFwt8oTDSGlBb4EZuUAQJBAMbR+tolF96tHPb96BKbowIytRQZpC3KMutnzY74davY4BvAnvzoUTs0d89Xi+1+YxmI0UahejGdyMEWOryNJYkCQQC3gf3B8Kmaic3hz1ghslsdY5n1sE8piJH/9owvToc54MVQc9sfFC9f+e6v8yjblHFeaoYTL6NUz9MUmeHAgatZAkB+VGnaNnuGR+UBo6/UMwROnz2jue8yESptnZVlZMYQHUu5FplvBYan4dzG6E/G5em+Dcs739qusB0hYyiLKfxRAkAiGKweqenJhgtUBqOYdzxIxKXpqZ272N1P0u6PJ6cmkOX4od438xcuXREFbkfMLNO3uFE7JWHSs17D+CejDjTZAkAWlJVrwvcgdPDun/xF2FK8YoonJFPJxFD/jrVPuoZ+HxYa9sytwuaAU8jTv8WDF4er1ZO4N3TENE+SedxuH0zW'

var key = NodeRSA(privateKey, 'pkcs8-private-pem',
{'environment': 'node', 'encryptionScheme': 'pkcs1', 'signingScheme': 'sha256'});

// 加密
var encryptedData = key.encrypt('hello world', 'base64')
console.log(encryptedData)
// 解密
var decryptedData = key.decrypt(encryptedData, 'utf-8')
console.log(decryptedData)
```

# JS

使用 openstack 实现的 [jsencrypt.js](https://github.com/openstack/xstatic-jsencrypt/blob/master/xstatic/pkg/jsencrypt/data/jsencrypt.js) 。

```java
var encrypt=new JSEncrypt(); 
encrypt.setPrivateKey('MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAI6FDzV8kQoj9vT6Iq0rT9Y3vBwwkq4YvlCHO5EPIUsIANso+QHu4Yp+RDVANye2NnyTj6bHagYEoXkTW9IH5sPtI/t+RKAOZ0LMYtIlfThD0f3nG4R8WxNfBbx0aHi5AMW391MhjZYDHxGcaGIkUqrrL2aP61yh+fMttA1/LY+hAgMBAAECgYBuMZNA17+NB6G6aGzHV+WyzAU2Bphi497ChM0Zq4kial2/Fj7xr7HTUy2Jvszmd4xJZg579VOUs5/l7YHhMxrI2sUadaenkdJ/LmdHICRT4BAFdDnM78UsY1/YgtoA06r63ZkaE6PJ2UPMCgcYMqV5OkAFwt8oTDSGlBb4EZuUAQJBAMbR+tolF96tHPb96BKbowIytRQZpC3KMutnzY74davY4BvAnvzoUTs0d89Xi+1+YxmI0UahejGdyMEWOryNJYkCQQC3gf3B8Kmaic3hz1ghslsdY5n1sE8piJH/9owvToc54MVQc9sfFC9f+e6v8yjblHFeaoYTL6NUz9MUmeHAgatZAkB+VGnaNnuGR+UBo6/UMwROnz2jue8yESptnZVlZMYQHUu5FplvBYan4dzG6E/G5em+Dcs739qusB0hYyiLKfxRAkAiGKweqenJhgtUBqOYdzxIxKXpqZ272N1P0u6PJ6cmkOX4od438xcuXREFbkfMLNO3uFE7JWHSs17D+CejDjTZAkAWlJVrwvcgdPDun/xF2FK8YoonJFPJxFD/jrVPuoZ+HxYa9sytwuaAU8jTv8WDF4er1ZO4N3TENE+SedxuH0zW')

// 加密
var encryptedData = encrypt.encrypt('hello world')
// 解密
var decryptedData = encrypt.decrypt(encryptedData, 'utf-8')
```

# 参考

- https://stackoverflow.com/questions/42638068/signing-decoding-with-base-64-pkcs-8-in-node-js
- https://www.devglan.com/online-tools/rsa-encryption-decryption
- https://www.devglan.com/java8/rsa-encryption-decryption-java
- https://github.com/openstack/xstatic-jsencrypt/blob/master/xstatic/pkg/jsencrypt/data/jsencrypt.js