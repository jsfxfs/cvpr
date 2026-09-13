# SpringBoot接口 - 如何实现接口限流之分布式

> 上文中介绍了单实例下如何在业务接口层做限流，本文主要介绍分布式场景下限流的方案，以及什么样的分布式场景下需要在业务层加限流而不是接入层; 并且结合[开源的ratelimiter-spring-boot-starter](https://gitee.com/kailing/ratelimiter-spring-boot-starter)为例，作者是kailing， 学习**思路+代码封装+starter封装**。 @pdai

## 准备知识点

> 上文我们提到了分布式限流的思路：

我们需要**分布式限流**和**接入层限流**来进行全局限流。

1. redis+lua实现中的lua脚本
2. 使用Nginx+Lua实现的Lua脚本
3. 使用 OpenResty 开源的限流方案
4. 限流框架，比如Sentinel实现降级限流熔断

## 实现思路之redis+lua封装

> redis+lua是代码层实现较为常见的方案，网上有很多的封装， 我这里找一个给你分享下。以[gitee开源的ratelimiter-spring-boot-starter](https://gitee.com/kailing/ratelimiter-spring-boot-starter)为例，作者是kailing， 值得初学者学习**思路+代码封装+starter封装**：

### 使用场景：为什么有些分布式场景下，还会在代码层进行控制限流？

基于 redis 的偏业务应用的分布式限流组件，使得项目拥有分布式限流能力变得很简单。限流的场景有很多，常说的限流一般指网关限流，控制好洪峰流量，以免打垮后方应用。这里突出`偏业务应用的分布式限流`的原因，是因为区别于网关限流，业务侧限流可以轻松根据业务性质做到细粒度的流量控制。比如如下场景，

- 案例一：

有一个公开的 openApi 接口， openApi 会给接入方派发一个 appId，此时，如果需要根据各个接入方的 appId 限流，网关限流就不好做了，只能在业务侧实现

- 案例二：

公司内部的短信接口，内部对接了多个第三方的短信通道，每个短信通道对流量的控制都不尽相同，假设有的第三方根据手机号和短信模板组合限流，网关限流就更不好做了

让我们看下，作者kailing是如何封装实现ratelimiter-spring-boot-starter的。

### 源代码的要点

- **Redis 客户端采用redisson，AOP拦截方式**

所以引入如下包

```bash
ext {
    redisson_Version = '3.15.1'
}

dependencies {
    compile "org.redisson:redisson:${redisson_Version}"
    compile 'org.springframework.boot:spring-boot-starter-aop'
    compileOnly 'org.springframework.boot:spring-boot-starter-web'

    annotationProcessor 'org.springframework.boot:spring-boot-configuration-processor'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    testImplementation 'org.springframework.boot:spring-boot-starter-web'
    testImplementation 'org.springdoc:springdoc-openapi-ui:1.5.2'
}
```

- **RateLimit注解**

作者考虑了时间表达式，限流后的自定义回退后的拒绝逻辑, 用户自定义Key（PS：**这里其实可以加一些默认的Key生成策略**，比如**按照方法**策略， **按照方法&IP** 策略, **按照自定义策略**等，默认为按照方法）

```java
package com.taptap.ratelimiter.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * @author kl (http://kailing.pub)
 * @since 2021/3/16
 */
@Target(value = {ElementType.METHOD})
@Retention(value = RetentionPolicy.RUNTIME)
public @interface RateLimit {

    /**
     * 时间窗口流量数量
     * @return rate
     */
    long rate();

    /**
     * 时间窗口流量数量表达式
     * @return rateExpression
     */
    String rateExpression() default "";

    /**
     * 时间窗口，最小单位秒，如 2s，2h , 2d
     * @return rateInterval
     */
    String rateInterval();

    /**
     * 获取key
     * @return keys
     */
    String [] keys() default {};

    /**
     * 限流后的自定义回退后的拒绝逻辑
     * @return fallback
     */
    String fallbackFunction() default "";

    /**
     * 自定义业务 key 的 Function
     * @return key
     */
    String customKeyFunction() default "";

}
```

- **AOP拦截**

around环绕方式， 通过定义RateLimiterService获取方法注解的信息，存放在为RateLimiterInfo

如果还定义了回调方法，被限流后还会执行回调方法，回调方法也在RateLimiterService中。

```java
package com.taptap.ratelimiter.core;

import com.taptap.ratelimiter.annotation.RateLimit;
import com.taptap.ratelimiter.exception.RateLimitException;
import com.taptap.ratelimiter.model.LuaScript;
import com.taptap.ratelimiter.model.RateLimiterInfo;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.redisson.api.RScript;
import org.redisson.api.RedissonClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by kl on 2017/12/29.
 * Content : 切面拦截处理器
 */
@Aspect
@Component
@Order(0)
public class RateLimitAspectHandler {

    private static final Logger logger = LoggerFactory.getLogger(RateLimitAspectHandler.class);

    private final RateLimiterService rateLimiterService;
    private final RScript rScript;

    public RateLimitAspectHandler(RedissonClient client, RateLimiterService lockInfoProvider) {
        this.rateLimiterService = lockInfoProvider;
        this.rScript = client.getScript();
    }

    @Around(value = "@annotation(rateLimit)")
    public Object around(ProceedingJoinPoint joinPoint, RateLimit rateLimit) throws Throwable {
        RateLimiterInfo limiterInfo = rateLimiterService.getRateLimiterInfo(joinPoint, rateLimit);

        List<Object> keys = new ArrayList<>();
        keys.add(limiterInfo.getKey());
        keys.add(limiterInfo.getRate());
        keys.add(limiterInfo.getRateInterval());
        List<Long> results = rScript.eval(RScript.Mode.READ_WRITE, LuaScript.getRateLimiterScript(), RScript.ReturnType.MULTI, keys);
        boolean allowed = results.get(0) == 0L;
        if (!allowed) {
            logger.info("Trigger current limiting,key:{}", limiterInfo.getKey());
            if (StringUtils.hasLength(rateLimit.fallbackFunction())) {
                return rateLimiterService.executeFunction(rateLimit.fallbackFunction(), joinPoint);
            }
            long ttl = results.get(1);
            throw new RateLimitException("Too Many Requests", ttl);
        }
        return joinPoint.proceed();
    }


}
```

这里LuaScript加载定义的lua脚本

```java
package com.taptap.ratelimiter.model;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.util.StreamUtils;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

/**
 * @author kl (http://kailing.pub)
 * @since 2021/3/18
 */
public final class LuaScript {

    private LuaScript(){}
    private static final Logger log = LoggerFactory.getLogger(LuaScript.class);
    private static final String RATE_LIMITER_FILE_PATH = "META-INF/ratelimiter-spring-boot-starter-rateLimit.lua";
    private static String rateLimiterScript;

    static {
        InputStream in = Thread.currentThread().getContextClassLoader()
                .getResourceAsStream(RATE_LIMITER_FILE_PATH);
        try {
            rateLimiterScript =  StreamUtils.copyToString(in, StandardCharsets.UTF_8);
        } catch (IOException e) {
            log.error("ratelimiter-spring-boot-starter Initialization failure",e);
        }
    }

    public static String getRateLimiterScript() {
        return rateLimiterScript;
    }
}
```

lua脚本放在META-INF/ratelimiter-spring-boot-starter-rateLimit.lua， 如下

```lua
--
-- Created by IntelliJ IDEA.
-- User: kl
-- Date: 2021/3/18
-- Time: 11:17 上午
-- To change this template use File | Settings | File Templates.
local rateLimitKey = KEYS[1];
local rate = tonumber(KEYS[2]);
local rateInterval = tonumber(KEYS[3]);
local limitResult = 0;
local ttlResult = 0;
local currValue = redis.call('incr', rateLimitKey);
if (currValue == 1) then
    redis.call('expire', rateLimitKey, rateInterval);
    limitResult = 0;
else
    if (currValue > rate) then
        limitResult = 1;
        ttlResult = redis.call('ttl', rateLimitKey);
    end
end
return { limitResult, ttlResult }
```

- **starter自动装配**

RateLimiterAutoConfiguration + RateLimiterProperties + spring.factories

```java
package com.taptap.ratelimiter.configuration;

import com.taptap.ratelimiter.core.BizKeyProvider;
import com.taptap.ratelimiter.core.RateLimitAspectHandler;
import com.taptap.ratelimiter.core.RateLimiterService;
import com.taptap.ratelimiter.web.RateLimitExceptionHandler;
import io.netty.channel.nio.NioEventLoopGroup;
import org.redisson.Redisson;
import org.redisson.api.RedissonClient;
import org.redisson.codec.JsonJacksonCodec;
import org.redisson.config.Config;
import org.springframework.boot.autoconfigure.AutoConfigureAfter;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.autoconfigure.data.redis.RedisAutoConfiguration;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

/**
 * @author kl (http://kailing.pub)
 * @since 2021/3/16
 */
@Configuration
@ConditionalOnProperty(prefix = RateLimiterProperties.PREFIX, name = "enabled", havingValue = "true")
@AutoConfigureAfter(RedisAutoConfiguration.class)
@EnableConfigurationProperties(RateLimiterProperties.class)
@Import({RateLimitAspectHandler.class, RateLimitExceptionHandler.class})
public class RateLimiterAutoConfiguration {

    private final RateLimiterProperties limiterProperties;

    public RateLimiterAutoConfiguration(RateLimiterProperties limiterProperties) {
        this.limiterProperties = limiterProperties;
    }

    @Bean(destroyMethod = "shutdown")
    @ConditionalOnMissingBean
    RedissonClient redisson() {
        Config config = new Config();
        if (limiterProperties.getRedisClusterServer() != null) {
            config.useClusterServers().setPassword(limiterProperties.getRedisPassword())
                    .addNodeAddress(limiterProperties.getRedisClusterServer().getNodeAddresses());
        } else {
            config.useSingleServer().setAddress(limiterProperties.getRedisAddress())
                    .setDatabase(limiterProperties.getRedisDatabase())
                    .setPassword(limiterProperties.getRedisPassword());
        }
        config.setCodec(new JsonJacksonCodec());
        config.setEventLoopGroup(new NioEventLoopGroup());
        return Redisson.create(config);
    }

    @Bean
    public RateLimiterService rateLimiterInfoProvider() {
        return new RateLimiterService();
    }

    @Bean
    public BizKeyProvider bizKeyProvider() {
        return new BizKeyProvider();
    }

}
```

### 1、快速开始

> 来看下作者kailing是如何提供的ratelimiter-spring-boot-starter使用文档。

#### 1.1、添加组件依赖，已上传到maven中央仓库

maven

```xml
<dependency>
    <groupId>com.github.taptap</groupId>
    <artifactId>ratelimiter-spring-boot-starter</artifactId>
    <version>1.2</version>
</dependency>
```

gradle

```groovy
implementation 'com.github.taptap:ratelimiter-spring-boot-starter:1.2'
```

#### 1.2、application.properties 配置

```properties
spring.ratelimiter.enabled = true

spring.ratelimiter.redis-address = redis://127.0.0.1:6379
spring.ratelimiter.redis-password = xxx
```

启用 ratelimiter 的配置必须加，默认不会加载。redis 相关的连接是非必须的，如果你的项目里已经使用了 `Redisson` ，则不用配置限流框架的 redis 连接

#### 1.3、在需要加限流逻辑的方法上，添加注解 @RateLimit，如：

```java
@RestController
@RequestMapping("/test")
public class TestController {

    @GetMapping("/get")
    @RateLimit(rate = 5, rateInterval = "10s")
    public String get(String name) {
        return "hello";
    }
}
```

##### 1.3.1 @RateLimit 注解说明

@RateLimit 注解可以添加到任意被 spring 管理的 bean 上，不局限于 controller ,service 、repository 也可以。在最基础限流功能使用上，以上三个步骤就已经完成了。@RateLimit 有两个最基础的参数，rateInterval 设置了时间窗口，rate 设置了时间窗口内允许通过的请求数量

##### 1.3.2 限流的粒度，限流 key

。限流的粒度是通过限流的 key 来做的，在最基础的设置下，限流的 key 默认是通过方法名称拼出来的，规则如下：

```properties
key = RateLimiter_ + 类名 + 方法名
```

除了默认的 key 策略，ratelimiter-spring-boot-starter 充分考虑了业务限流时的复杂性，提供了多种方式。结合业务特征，达到更细粒度的限流控制。

##### 1.3.3 触发限流后的行为

默认触发限流后 程序会返回一个 http 状态码为 429 的响应，响应值如下：

```json
{
  "code":429,
  "msg":"Too Many Requests"
}
```

同时，响应的 header 里会携带一个 Retry-After 的时间值，单位 s，用来告诉调用方多久后可以重试。当然这一切都是可以自定义的，进阶用法可以继续往下看

### 2、进阶用法

#### 2.1、自定义限流的 key

自定义限流 key 有三种方式，当自定义限流的 key 生效时，限流的 key 就变成了（默认的 key + 自定义的 key）。下面依次给出示例

##### 2.1.1、@RateLimitKey 的方式

```java
@RestController
@RequestMapping("/test")
public class TestController {

    @GetMapping("/get")
    @RateLimit(rate = 5, rateInterval = "10s")
    public String get(@RateLimitKey String name) {
        return "get";
    }
}
```

@RateLimitKey 注解可以放在方法的入参上，要求入参是基础数据类型，上面的例子，如果 name = kl。那么最终限流的 key 如下：

```properties
key = RateLimiter_com.taptap.ratelimiter.web.TestController.get-kl
```

##### 2.1.2、指定 keys 的方式

```java
@RestController
@RequestMapping("/test")
public class TestController {

    @GetMapping("/get")
    @RateLimit(rate = 5, rateInterval = "10s",keys = {"#name"})
    public String get(String name) {
        return "get";
    }

    @GetMapping("/hello")
    @RateLimit(rate = 5, rateInterval = "10s",keys = {"#user.name","user.id"})
    public String hello(User user) {
        return "hello";
    }
}
```

keys 这个参数比 @RateLimitKey 注解更智能，基本可以包含 @RateLimitKey 的能力，只是简单场景下，使用起来没有 @RateLimitKey 那么便捷。keys 的语法来自 spring 的 `Spel`，可以获取对象入参里的属性，支持获取多个，最后会拼接起来。使用过 spring-cache 的同学可能会更加熟悉 如果不清楚 `Spel` 的用法，可以参考 spring-cache 的注解文档

##### 2.1.3、自定义 key 获取函数

```java
@RestController
@RequestMapping("/test")
public class TestController {

    @GetMapping("/get")
    @RateLimit(rate = 5, rateInterval = "10s",customKeyFunction = "keyFunction")
    public String get(String name) {
        return "get";
    }

    public String keyFunction(String name) {
        return "keyFunction" + name;
    }
}
```

当 @RateLimitKey 和 keys 参数都没法满足时，比如入参的值是一个加密的值，需要解密后根据相关明文内容限流。可以通过在同一类里自定义获取 key 的函数，这个函数要求和被限流的方法入参一致，返回值为 String 类型。返回值不能为空，为空时，会回退到默认的 key 获取策略。

#### 2.2、自定义限流后的行为

##### 2.2.1、配置响应内容

```properties
spring.ratelimiter.enabled=true
spring.ratelimiter.response-body=Too Many Requests
spring.ratelimiter.status-code=509
```

添加如上配置后，触发限流时，http 的状态码就变成了 509 。响应的内容变成了 Too Many Requests 了

##### 2.2.2、自定义限流触发异常处理器

默认的触发限流后，限流器会抛出一个异常，限流器框架内定义了一个异常处理器来处理。自定义限流触发处理器，需要先禁用系统默认的限流触发处理器，禁用方式如下：

```properties
spring.ratelimiter.exceptionHandler.enable=false
```

然后在项目里添加自定义处理器，如下：

```java
@ControllerAdvice
public class RateLimitExceptionHandler {

    private final  RateLimiterProperties limiterProperties;

    public RateLimitExceptionHandler(RateLimiterProperties limiterProperties) {
        this.limiterProperties = limiterProperties;
    }

    @ExceptionHandler(value = RateLimitException.class)
    @ResponseBody
    public String exceptionHandler(HttpServletResponse response, RateLimitException e){
        response.setStatus(limiterProperties.getStatusCode());
        response.setHeader("Retry-After", String.valueOf(e.getRetryAfter()));
        return limiterProperties.getResponseBody();
    }
}
```

##### 2.2.3、自定义触发限流处理函数，限流降级

```java
@RequestMapping("/test")
public class TestController {

    @GetMapping("/get")
    @RateLimit(rate = 5, rateInterval = "10s",fallbackFunction = "getFallback")
    public String get(String name) {
        return "get";
    }

    public String getFallback(String name){
        return "Too Many Requests" + name;
    }

}
```

这种方式实现和使用和 2.1.3、自定义 key 获取函数类似。但是多一个要求，返回值的类型需要和原限流函数的返回值类型一致，当触发限流时，框架会调用 fallbackFunction 配置的函数执行并返回，达到限流降级的效果

#### 2.3 动态设置限流大小

##### 2.3.1、rateExpression 的使用

从 `v1.2` 版本开始，在 `@RateLimit` 注解里新增了属性 rateExpression。该属性支持 `Spel` 表达式从 Spring 的配置上下文中获取值。 当配置了 rateExpression 后，rate 属性的配置就不生效了。使用方式如下：

```java
    @GetMapping("/get2")
    @RateLimit(rate = 2, rateInterval = "10s",rateExpression = "${spring.ratelimiter.max}")
    public String get2() {
        return "get";
    }
```

集成 apollo 等配置中心后，可以做到限流大小的动态调整在线热更。

### 3、集成示例、测验

#### 3.1、集成测验

启动 src/test/java/com/taptap/ratelimiter/Application.java 后，访问 http://localhost:8080/swagger-ui.html

#### 3.2、压力测试

- 压测工具 wrk： https://github.com/wg/wrk
- 测试环境: 8 核心 cpu ，jvm 内存给的 -Xms2048m -Xmx2048m ，链接的本地的 redis

```bash
#压测数据
kldeMacBook-Pro-6:ratelimiter-spring-boot-starter kl$ wrk -t16 -c100 -d15s --latency http://localhost:8080/test/wrk
Running 15s test @ http://localhost:8080/test/wrk
  16 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     6.18ms   20.70ms 281.21ms   98.17%
    Req/Sec     1.65k   307.06     2.30k    76.44%
  Latency Distribution
     50%    3.57ms
     75%    4.11ms
     90%    5.01ms
     99%  115.48ms
  389399 requests in 15.03s, 43.15MB read
Requests/sec:  25915.91
Transfer/sec:      2.87MB
```

压测下，所有流量都过限流器，qps 可以达到 2w+。

### 4、版本更新

#### 4.1、（v1.1.1）版本更新内容

- 1、触发限流时，header 的 Retry-After 值，单位由 ms ，调整成了 s

#### 4.2、（v1.2）版本更新内容

- 1、触发限流时，响应的类型从 `text/plain` 变成了 `application/json`
- 2、优化了限流的 lua 脚本，将原来的两步 lua 脚本请求，合并成了一个，减少了和 redis 的交互
- 3、限流的时间窗口大小，支持 `Spel` 从 Spring 的配置上下文中获取，结合 `apollo` 等配置中心后，支持规则的动态下发热更新

## 示例源码

https://gitee.com/kailing/ratelimiter-spring-boot-starter

https://github.com/realpdai/tech-pdai-spring-demos