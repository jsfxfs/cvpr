# SpringBoot集成Redis - 基于RedisTemplate+Lettuce数据类封装

> 前两篇文章介绍了SpringBoot基于RedisTemplate的数据操作，那么如何对这些操作进行封装呢？本文主要介绍基于RedisTemplate的封装。@pdai

## 知识准备

> 需要对封装的场景有理解。@pdai

### 有了RedisTemplate为什么还要进一步封装？

RedisTemplate中的操作和方法众多，为了程序保持方法使用的一致性，屏蔽一些无关的方法以及对使用的方法进一步封装。

PS：同样的类似思路也体现在很多场景中，比如[Tomcat Request利用外观模式改造](../../framework/tomcat/Tomcat - 如何设计一个简单的web容器.md#%E5%88%A9%E7%94%A8%E5%A4%96%E8%A7%82%E6%A8%A1%E5%BC%8F%E6%94%B9%E9%80%A0)。

## 实现案例

> 本文主要展示基于RedisTemplate的部分简单封装的示例。@pdai

### RedisService封装

RedisService接口类

```java
package tech.pdai.springboot.redis.lettuce.enclosure.service;

import org.springframework.data.redis.core.RedisCallback;

import java.util.Collection;
import java.util.Set;

/**
 * Redis Service.
 *
 * @author pdai
 */
public interface IRedisService<T> {

    void set(String key, T value);

    void set(String key, T value, long time);

    T get(String key);

    void delete(String key);

    void delete(Collection<String> keys);

    boolean expire(String key, long time);

    Long getExpire(String key);

    boolean hasKey(String key);

    Long increment(String key, long delta);

    Long decrement(String key, long delta);

    void addSet(String key, T value);

    Set<T> getSet(String key);

    void deleteSet(String key, T value);

    T execute(RedisCallback<T> redisCallback);
}
```

RedisService的实现类

```java
package tech.pdai.springboot.redis.lettuce.enclosure.service.impl;

import org.springframework.data.redis.core.RedisCallback;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import tech.pdai.springboot.redis.lettuce.enclosure.service.IRedisService;

import javax.annotation.Resource;
import java.util.Collection;
import java.util.Set;
import java.util.concurrent.TimeUnit;

/**
 * @author pdai
 */
@Service
public class RedisServiceImpl<T> implements IRedisService<T> {

    @Resource
    private RedisTemplate<String, T> redisTemplate;

    @Override
    public void set(String key, T value, long time) {
        redisTemplate.opsForValue().set(key, value, time, TimeUnit.SECONDS);
    }

    @Override
    public void set(String key, T value) {
        redisTemplate.opsForValue().set(key, value);
    }

    @Override
    public T get(String key) {
        return redisTemplate.opsForValue().get(key);
    }

    @Override
    public void delete(String key) {
        redisTemplate.delete(key);
    }

    @Override
    public void delete(Collection<String> keys) {
        redisTemplate.delete(keys);
    }

    @Override
    public boolean expire(String key, long time) {
        return redisTemplate.expire(key, time, TimeUnit.SECONDS);
    }

    @Override
    public Long getExpire(String key) {
        return redisTemplate.getExpire(key, TimeUnit.SECONDS);
    }

    @Override
    public boolean hasKey(String key) {
        return redisTemplate.hasKey(key);
    }

    @Override
    public Long increment(String key, long delta) {
        return redisTemplate.opsForValue().increment(key, delta);
    }

    @Override
    public Long decrement(String key, long delta) {
        return redisTemplate.opsForValue().increment(key, -delta);
    }

    @Override
    public void addSet(String key, T value) {
        redisTemplate.opsForSet().add(key, value);
    }

    @Override
    public Set<T> getSet(String key) {
        return redisTemplate.opsForSet().members(key);
    }

    @Override
    public void deleteSet(String key, T value) {
        redisTemplate.opsForSet().remove(key, value);
    }

    @Override
    public T execute(RedisCallback<T> redisCallback) {
        return redisTemplate.execute(redisCallback);
    }

}
```

### RedisService的调用

UserController类中调用RedisService

```java
package tech.pdai.springboot.redis.lettuce.enclosure.controller;


import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import tech.pdai.springboot.redis.lettuce.enclosure.entity.User;
import tech.pdai.springboot.redis.lettuce.enclosure.entity.response.ResponseResult;
import tech.pdai.springboot.redis.lettuce.enclosure.service.IRedisService;

/**
 * @author pdai
 */
@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private IRedisService<User> redisService;

    /**
     * @param user user param
     * @return user
     */
    @ApiOperation("Add")
    @PostMapping("add")
    public ResponseResult<User> add(User user) {
        redisService.set(String.valueOf(user.getId()), user);
        return ResponseResult.success(redisService.get(String.valueOf(user.getId())));
    }

    /**
     * @return user list
     */
    @ApiOperation("Find")
    @GetMapping("find/{userId}")
    public ResponseResult<User> edit(@PathVariable("userId") String userId) {
        return ResponseResult.success(redisService.get(userId));
    }

}
```

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos