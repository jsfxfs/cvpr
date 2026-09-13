# ▶SpringBoot集成Redis - 基于RedisTemplate+Jedis的数据操作

> Redis是最常用的KV数据库，Spring 通过模板方式（RedisTemplate）提供了对Redis的数据查询和操作功能。本文主要介绍基于RedisTemplate + Jedis方式对Redis进行查询和操作的案例。@pdai

## 知识准备

> 需要对Redis的基础和基础数据类型有理解，且需要对Spring中对数据库操作常见的模板方式的封装了解，并了解RedisTemplate。

### Redis基础和5种基础数据类型

> Redis 相关的知识体系，请参考 [Redis知识体系](../../db/nosql-redis/db-redis-overview.md)

首先对redis来说，所有的key（键）都是字符串。我们在谈基础数据结构时，讨论的是存储值的数据类型，主要包括常见的5种数据类型，分别是：String、List、Set、Zset、Hash。

![](https://www.pdai.tech/images/db/redis/db-redis-ds-1.jpeg)

| 结构类型 | 结构存储的值 | 结构的读写能力 |
| --- | --- | --- |
| **String字符串** | 可以是字符串、整数或浮点数 | 对整个字符串或字符串的一部分进行操作；对整数或浮点数进行自增或自减操作； |
| **List列表** | 一个链表，链表上的每个节点都包含一个字符串 | 对链表的两端进行push和pop操作，读取单个或多个元素；根据值查找或删除元素； |
| **Set集合** | 包含字符串的无序集合 | 字符串的集合，包含基础的方法有看是否存在添加、获取、删除；还包含计算交集、并集、差集等 |
| **Hash散列** | 包含键值对的无序散列表 | 包含方法有添加、获取、删除单个元素 |
| **Zset有序集合** | 和散列一样，用于存储键值对 | 字符串成员与浮点数分数之间的有序映射；元素的排列顺序由分数的大小决定；包含方法有添加、获取、删除单个元素以及根据分值范围或成员来获取元素 |

### 什么是Jedis

Jedis是Redis的Java客户端，在SpringBoot 1.x版本中也是默认的客户端。在SpringBoot 2.x版本中默认客户端是Luttuce。

### Spring中的Template和RedisTemplate

> Spring 通过模板方式（RedisTemplate）提供了对Redis的数据查询和操作功能。

**什么是模板模式**？

模板方法模式(Template pattern): 在一个方法中定义一个算法的骨架, 而将一些步骤延迟到子类中. 模板方法使得子类可以在不改变算法结构的情况下, 重新定义算法中的某些步骤。

![](https://www.pdai.tech/images/pics/c3c1c0e8-3a78-4426-961f-b46dd0879dd8.png)

**Spring中有哪些模板模式的设计**？

比如：jdbcTemplate, mongodbTemplate, elasticsearchTemplate...等等

**RedisTemplate对于Redis5种基础类型的操作**？

```java
redisTemplate.opsForValue(); // 操作字符串
redisTemplate.opsForHash(); // 操作hash
redisTemplate.opsForList(); // 操作list
redisTemplate.opsForSet(); // 操作set
redisTemplate.opsForZSet(); // 操作zset
```

**对HyperLogLogs（基数统计）类型的操作**?

相关内容请[参考: Redis特殊数据类型 HyperLogLogs](../../db/nosql-redis/db-redis-data-type-special.md#hyperloglogs%E5%9F%BA%E6%95%B0%E7%BB%9F%E8%AE%A1)

```java
redisTemplate.opsForHyperLogLog();
```

**对geospatial (地理位置)类型的操作**?

相关内容请[参考: Redis特殊数据类型 geospatial](../../db/nosql-redis/db-redis-data-type-special.md#geospatial-%E5%9C%B0%E7%90%86%E4%BD%8D%E7%BD%AE)

```java
redisTemplate.opsForGeo();
```

**对于BitMap的操作**？也是在opsForValue()方法返回类型ValueOperations中

相关内容请[参考: Redis特殊数据类型 BitMap](../../db/nosql-redis/db-redis-data-type-special.md#bitmap-%E4%BD%8D%E5%AD%98%E5%82%A8)

```java
Boolean setBit(K key, long offset, boolean value);
Boolean getBit(K key, long offset);
```

**对于Stream的操作**？

相关内容请[参考: Redis Stream 详解](../../db/nosql-redis/db-redis-data-type-stream.md)

```java
redisTemplate.opsForStream();
```

## 实现案例

> 本例子主要基于SpringBoot2+ 使用Jedis客户端，通过RedisTemplate模板方式访问Redis数据。

### 包依赖

引入spring-boot-starter-data-redis包，SpringBoot2中默认的客户端是Lettuce, 所以需要exclude掉lettuce-core包，并引入jedis的包。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
    <exclusions>
        <exclusion>
            <artifactId>lettuce-core</artifactId>
            <groupId>io.lettuce</groupId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
</dependency>
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-pool2</artifactId>
    <version>2.9.0</version>
</dependency>
```

### yml配置

如下是常用的Jedis的使用配置

```yaml
spring:
  redis:
    database: 0
    host: 127.0.0.1
    port: 6379
    password: test
    jedis:
      pool:
        min-idle: 0
        max-active: 8
        max-idle: 8
        max-wait: -1ms
    connect-timeout: 30000ms
```

### RedisConfig配置

通过@Bean的方式配置RedisTemplate，主要是设置RedisConnectionFactory以及各种类型数据的Serializer。

```java
package tech.pdai.springboot.redis.jedis.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.GenericJackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;

/**
 * Redis configuration.
 *
 * @author pdai
 */
@Configuration
public class RedisConfig {

    /**
     * redis template.
     *
     * @param factory factory
     * @return RedisTemplate
     */
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory factory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(factory);
        template.setKeySerializer(new StringRedisSerializer());
        template.setHashKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
        template.setHashValueSerializer(new GenericJackson2JsonRedisSerializer());
        template.afterPropertiesSet();
        return template;
    }
}
```

### RedisTemplate的使用

我们以整个系列文章一致的UserController简单示例下

```java
package tech.pdai.springboot.redis.jedis.controller;


import io.swagger.annotations.ApiOperation;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.web.bind.annotation.*;
import tech.pdai.springboot.redis.jedis.entity.User;
import tech.pdai.springboot.redis.jedis.entity.response.ResponseResult;

import javax.annotation.Resource;

/**
 * @author pdai
 */
@RestController
@RequestMapping("/user")
public class UserController {

    // 注意：这里@Autowired是报错的，因为@Autowired按照类名注入的
    @Resource
    private RedisTemplate<String, User> redisTemplate;

    /**
     * @param user user param
     * @return user
     */
    @ApiOperation("Add")
    @PostMapping("add")
    public ResponseResult<User> add(User user) {
        redisTemplate.opsForValue().set(String.valueOf(user.getId()), user);
        return ResponseResult.success(redisTemplate.opsForValue().get(String.valueOf(user.getId())));
    }

    /**
     * @return user list
     */
    @ApiOperation("Find")
    @GetMapping("find/{userId}")
    public ResponseResult<User> edit(@PathVariable("userId") String userId) {
        return ResponseResult.success(redisTemplate.opsForValue().get(userId));
    }

}
```

### 简单测试

插入数据：redisTemplate.opsForValue().set();

![](https://www.pdai.tech/images/spring/springboot/springboot-redis-jedis-2.png)

获取数据：redisTemplate.opsForValue().get();

![](https://www.pdai.tech/images/spring/springboot/springboot-redis-jedis-1.png)

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos