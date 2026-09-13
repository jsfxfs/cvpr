# SpringBoot集成Redis - Redis分布式锁的实现之Jedis(setNXPX+Lua)

> Redis实际使用场景最为常用的还有通过Redis实现分布式锁。本文主要介绍Redis实现分布式锁。@pdai

## 知识准备

> 需要了解为何要用分布式锁，以及分布式锁常见的实现方式；以及如何通过Redis实现分布式锁的几种方式。

### 什么是分布式锁，分布式锁有哪些实现方式？

分布式锁相关的内容请参考 [分布式系统 - 分布式锁及实现方案](../../arch/分布式系统 - 分布式锁及实现方案.md)

### Redis的分布式锁有哪些实现方式？

> 主要有两种思路

- 单个Redis实例：setnx(key,当前时间+过期时间) + Lua
- Redis集群模式：Redlock

在实现使用时，由于很多redis客户端包含了上述实现方式，我们可以通过redis客户端进行，更多可以看[分布式系统 - 分布式锁及实现方案](../../arch/分布式系统 - 分布式锁及实现方案.md)

## 实现案例

> 本案例主要介绍 基于Jedis客户端下通过： **setnx(key,当前时间+过期时间) + Lua** 实现分布式锁

### 定义Redis的分布式锁类

> （具体看[分布式系统 - 分布式锁及实现方案](../../arch/分布式系统 - 分布式锁及实现方案.md) 中Redis实现分布式锁的部分）

**加锁**： set NX PX + 重试 + 重试间隔

向Redis发起如下命令: `SET productId:lock 0xx9p03001 NX PX 30000` 其中，"productId"由自己定义，可以是与本次业务有关的id，"0xx9p03001"是一串随机值，必须保证全局唯一(原因在后文中会提到)，“NX"指的是当且仅当key(也就是案例中的"productId:lock”)在Redis中不存在时，返回执行成功，否则执行失败。"PX 30000"指的是在30秒后，key将被自动删除。执行命令后返回成功，表明服务成功的获得了锁。

**解锁**：采用lua脚本

在删除key之前，一定要判断服务A持有的value与Redis内存储的value是否一致。如果贸然使用服务A持有的key来删除锁，则会误将服务B的锁释放掉。

```lua
if redis.call("get", KEYS[1])==ARGV[1] then
	return redis.call("del", KEYS[1])
else
	return 0
end
```

具体的封装类RedisDistributedLock如下：

```java
package tech.pdai.springboot.redis.jedis.lock.lock;

import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.data.redis.core.RedisCallback;
import org.springframework.data.redis.core.StringRedisTemplate;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisCluster;
import redis.clients.jedis.commands.JedisCommands;
import redis.clients.jedis.params.SetParams;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * @author pdai
 */
@Slf4j
public class RedisDistributedLock {

    /**
     * lua script for unlock.
     */
    private static final String UNLOCK_LUA;

    static {
        StringBuilder sb = new StringBuilder();
        sb.append("if redis.call(\"get\",KEYS[1]) == ARGV[1] ");
        sb.append("then ");
        sb.append("    return redis.call(\"del\",KEYS[1]) ");
        sb.append("else ");
        sb.append("    return 0 ");
        sb.append("end ");
        UNLOCK_LUA = sb.toString();
    }

    /**
     * unique lock flag based on thread local.
     */
    private final ThreadLocal<String> lockFlag = new ThreadLocal<>();

    private final StringRedisTemplate redisTemplate;

    public RedisDistributedLock(StringRedisTemplate redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    public boolean lock(String key, long expire, int retryTimes, long retryDuration) {
        // use JedisCommands instead of setIfAbsense
        boolean result = setRedis(key, expire);

        // retry if needed
        while ((!result) && retryTimes-- > 0) {
            try {
                log.debug("lock failed, retrying..." + retryTimes);
                Thread.sleep(retryDuration);
            } catch (Exception e) {
                return false;
            }

            // use JedisCommands instead of setIfAbsense
            result = setRedis(key, expire);
        }
        return result;
    }

    private boolean setRedis(String key, long expire) {
        try {
            RedisCallback<String> redisCallback = connection -> {
                JedisCommands commands = (JedisCommands) connection.getNativeConnection();
                String uuid = UUID.randomUUID().toString(); // change to distribute UUID generation.
                lockFlag.set(uuid);
                return commands.set(key, uuid, SetParams.setParams().nx().px(expire));
            };
            String result = redisTemplate.execute(redisCallback);
            return !StringUtils.isEmpty(result);
        } catch (Exception e) {
            log.error("set redis occurred an exception", e);
        }
        return false;
    }

    public boolean unlock(String key) {
        boolean success = false;
        try {
            List<String> keys = new ArrayList<>();
            keys.add(key);
            List<String> args = new ArrayList<>();
            args.add(lockFlag.get());

            // use lua script
            RedisCallback<Long> redisCallback = connection -> {
                Object nativeConnection = connection.getNativeConnection();

                if (nativeConnection instanceof JedisCluster) { // cluster mode
                    return (Long) ((JedisCluster) nativeConnection).eval(UNLOCK_LUA, keys, args);
                } else if (nativeConnection instanceof Jedis) { // single mode
                    return (Long) ((Jedis) nativeConnection).eval(UNLOCK_LUA, keys, args);
                }
                return 0L;
            };
            Long result = redisTemplate.execute(redisCallback);
            success = result != null && result > 0;
        } catch (Exception e) {
            log.error("release lock occurred an exception", e);
        } finally {
            if (success) {
                lockFlag.remove();
            }
        }
        return success;
    }

}
```

### 定义AOP拦截点

定义RedisLock注解

```java
package tech.pdai.springboot.redis.jedis.lock.annotation;

import java.lang.annotation.*;

/**
 * @author pdai
 */
@Target({ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Inherited
public @interface RedisLock {

    /**
     * redis lock key as value.
     *
     * @return lock key
     */
    String value() default "";

    /**
     * how long we hold the lock.
     *
     * @return mills
     */
    long expireMills() default 30000;

    /**
     * if lock failed, do we need to retry, default retry 0 means NO retry.
     *
     * @return retry times
     */
    int retryTimes() default 0;

    /**
     * when we retry to get lock, what's the duration for next retry.
     *
     * @return mills
     */
    long retryDurationMills() default 200;

}
```

### 定义AOP切面

定义AOP切面类RedisLockAspect，用来拦截@RedisLock注解方法，并调用RedisDistributedLock对方法加锁处理。

```java
package tech.pdai.springboot.redis.jedis.lock.lock;

import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.context.annotation.Configuration;
import tech.pdai.springboot.redis.jedis.lock.annotation.RedisLock;

import javax.annotation.Resource;
import java.lang.reflect.Method;
import java.util.Arrays;

/**
 * @author pdai
 */
@Slf4j
@Aspect
@Configuration
public class RedisLockAspect {

    /**
     * lock impl.
     */
    @Resource
    private RedisDistributedLock distributedLock;

    /**
     * AOP, around PJP.
     *
     * @param pjp ProceedingJoinPoint
     * @return Object
     * @throws Throwable Throwable
     */
    @Around("@annotation(tech.pdai.springboot.redis.jedis.lock.annotation.RedisLock)")
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        // get attribute through annotation
        Method method = ((MethodSignature) pjp.getSignature()).getMethod();
        RedisLock redisLock = method.getAnnotation(RedisLock.class);
        String key = redisLock.value();
        if (StringUtils.isEmpty(key)) {
            Object[] args = pjp.getArgs();
            key = Arrays.toString(args);
        }

        // do lock
        boolean lock = distributedLock.lock(key, redisLock.expireMills(), redisLock.retryTimes(),
                redisLock.retryDurationMills());
        if (!lock) {
            log.debug("get lock failed, key: {}", key);
            return null;
        }

        // execute method, and unlock
        log.debug("get lock success, key: {}", key);
        try {
            // execute
            return pjp.proceed();
        } catch (Exception e) {
            log.error("execute locked method occurred an exception", e);
        } finally {
            // unlock
            boolean releaseResult = distributedLock.unlock(key);
            log.debug("release lock: {}, success: {}", key, releaseResult);
        }

        return null;
    }

}
```

### 切面使用

只需要添加@RedisLock注解即可：

```java
@RedisLock
public void xxxMethod() {

}
```

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos