# SpringBoot接口 - 如何实现接口限流之单实例

> 在以SpringBoot开发Restful接口时，当流量超过服务极限能力时，系统可能会出现卡死、崩溃的情况，所以就有了降级和限流。在接口层如何做限流呢？ 本文主要回顾限流的知识点，并实践单实例限流的一种思路。 @pdai

## 准备知识点

> 主要的知识点，请参考[架构之高并发：限流](../../arch/架构之高并发：限流.md), 这里小结下。

### 为什么要限流

每个系统都有服务的上线，所以当流量超过服务极限能力时，系统可能会出现卡死、崩溃的情况，所以就有了降级和限流。限流其实就是：当高并发或者瞬时高并发时，为了保证系统的稳定性、可用性，系统以牺牲部分请求为代价或者延迟处理请求为代价，保证系统整体服务可用。

### 限流有哪些常见思路？

- **从算法上看**

令牌桶(Token Bucket)、漏桶(leaky bucket)和计数器算法是最常用的三种限流的算法。

- **单实例**

应用级限流方式只是单应用内的请求限流，不能进行全局限流。

1. 限流总资源数
2. 限流总并发/连接/请求数
3. 限流某个接口的总并发/请求数
4. 限流某个接口的时间窗请求数
5. 平滑限流某个接口的请求数
6. Guava RateLimiter

- **分布式**

我们需要**分布式限流**和**接入层限流**来进行全局限流。

1. redis+lua实现中的lua脚本
2. 使用Nginx+Lua实现的Lua脚本
3. 使用 OpenResty 开源的限流方案
4. 限流框架，比如Sentinel实现降级限流熔断

## 实现思路

> 主要思路：AOP拦截自定义的RateLimit注解，在AOP中通过Guava RateLimiter; Guava RateLimiter提供了令牌桶算法实现：平滑突发限流(SmoothBursty)和平滑预热限流(SmoothWarmingUp)实现。

### 定义RateLimit注解

```java
package tech.pdai.ratelimit.guava.config.ratelimit;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * @author pdai
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface RateLimit {

    int limit() default 10;

}
```

### 定义AOP

```java
package tech.pdai.ratelimit.guava.config.ratelimit;

import java.lang.reflect.Method;
import java.util.concurrent.ConcurrentHashMap;

import com.google.common.util.concurrent.RateLimiter;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.core.annotation.AnnotationUtils;
import org.springframework.stereotype.Component;

/**
 * @author pdai
 */
@Slf4j
@Aspect
@Component
public class RateLimitAspect {

    private final ConcurrentHashMap<String, RateLimiter> EXISTED_RATE_LIMITERS = new ConcurrentHashMap<>();

    @Pointcut("@annotation(tech.pdai.ratelimit.guava.config.ratelimit.RateLimit)")
    public void rateLimit() {
    }

    @Around("rateLimit()")
    public Object around(ProceedingJoinPoint point) throws Throwable {
        MethodSignature signature = (MethodSignature) point.getSignature();
        Method method = signature.getMethod();
        RateLimit annotation = AnnotationUtils.findAnnotation(method, RateLimit.class);

        // get rate limiter
        RateLimiter rateLimiter = EXISTED_RATE_LIMITERS.computeIfAbsent(method.getName(), k -> RateLimiter.create(annotation.limit()));

        // process
        if (rateLimiter!=null && rateLimiter.tryAcquire()) {
            return point.proceed();
        } else {
            throw new RuntimeException("too many requests, please try again later...");
        }
    }
}
```

### 自定义相关异常

```java
package tech.pdai.ratelimit.guava.config.exception;

import lombok.extern.slf4j.Slf4j;

/**
 * business exception, besides normal exception.
 *
 * @author pdai
 */
@Slf4j
public class BusinessException extends RuntimeException {

    /**
     * Constructs a new exception with {@code null} as its detail message. The cause is not initialized, and may
     * subsequently be initialized by a call to {@link #initCause}.
     */
    public BusinessException() {
        super();
    }

    /**
     * Constructs a new exception with the specified detail message. The cause is not initialized, and may subsequently
     * be initialized by a call to {@link #initCause}.
     *
     * @param message the detail message. The detail message is saved for later retrieval by the {@link #getMessage()}
     *                method.
     */
    public BusinessException(final String message) {
        super(message);
    }

    /**
     * Constructs a new exception with the specified detail message and cause.
     * <p>
     * Note that the detail message associated with {@code cause} is <i>not</i> automatically incorporated in this
     * exception's detail message.
     *
     * @param message the detail message (which is saved for later retrieval by the {@link #getMessage()} method).
     * @param cause   the cause (which is saved for later retrieval by the {@link #getCause()} method). (A <tt>null</tt>
     *                value is permitted, and indicates that the cause is nonexistent or unknown.)
     * @since 1.4
     */
    public BusinessException(final String message, final Throwable cause) {
        super(message, cause);
    }

    /**
     * Constructs a new exception with the specified cause and a detail message of
     * <tt>(cause==null ? null : cause.toString())</tt> (which typically contains the class and detail message of
     * <tt>cause</tt>). This constructor is useful for exceptions that are little more than wrappers for other
     * throwables (for example, {@link java.security.PrivilegedActionException}).
     *
     * @param cause the cause (which is saved for later retrieval by the {@link #getCause()} method). (A <tt>null</tt>
     *              value is permitted, and indicates that the cause is nonexistent or unknown.)
     * @since 1.4
     */
    public BusinessException(final Throwable cause) {
        super(cause);
    }

    /**
     * Constructs a new exception with the specified detail message, cause, suppression enabled or disabled, and
     * writable stack trace enabled or disabled.
     *
     * @param message            the detail message.
     * @param cause              the cause. (A {@code null} value is permitted, and indicates that the cause is nonexistent or
     *                           unknown.)
     * @param enableSuppression  whether or not suppression is enabled or disabled
     * @param writableStackTrace whether or not the stack trace should be writable
     * @since 1.7
     */
    protected BusinessException(final String message, final Throwable cause, boolean enableSuppression,
                                boolean writableStackTrace) {
        super(message, cause, enableSuppression, writableStackTrace);
    }

}
```

异常的处理

```java
package tech.pdai.ratelimit.guava.config.exception;


import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import tech.pdai.ratelimit.guava.config.response.ResponseResult;
import tech.pdai.ratelimit.guava.config.response.ResponseStatus;

/**
 * @author pdai
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * handle business exception.
     *
     * @param businessException business exception
     * @return ResponseResult
     */
    @ResponseBody
    @ExceptionHandler(BusinessException.class)
    public ResponseResult<BusinessException> processBusinessException(BusinessException businessException) {
        log.error(businessException.getLocalizedMessage());
        return ResponseResult.fail(null, businessException.getLocalizedMessage()==null
                ? ResponseStatus.HTTP_STATUS_500.getDescription()
                :businessException.getLocalizedMessage());
    }

    /**
     * handle other exception.
     *
     * @param exception exception
     * @return ResponseResult
     */
    @ResponseBody
    @ExceptionHandler(Exception.class)
    public ResponseResult<Exception> processException(Exception exception) {
        log.error(exception.getLocalizedMessage(), exception);
        return ResponseResult.fail(null, ResponseStatus.HTTP_STATUS_500.getDescription());
    }
}
```

### 统一结果返回封装

```java
package tech.pdai.ratelimit.guava.config.response;

import java.io.Serializable;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder
public class ResponseResult<T> {

    /**
     * response timestamp.
     */
    private long timestamp;

    /**
     * response code, 200 -> OK.
     */
    private String status;

    /**
     * response message.
     */
    private String message;

    /**
     * response data.
     */
    private T data;

    /**
     * response success result wrapper.
     *
     * @param <T> type of data class
     * @return response result
     */
    public static <T> ResponseResult<T> success() {
        return success(null);
    }

    /**
     * response success result wrapper.
     *
     * @param data response data
     * @param <T>  type of data class
     * @return response result
     */
    public static <T> ResponseResult<T> success(T data) {
        return ResponseResult.<T>builder().data(data)
                .message(ResponseStatus.SUCCESS.getDescription())
                .status(ResponseStatus.SUCCESS.getResponseCode())
                .timestamp(System.currentTimeMillis())
                .build();
    }

    /**
     * response error result wrapper.
     *
     * @param message error message
     * @param <T>     type of data class
     * @return response result
     */
    public static <T extends Serializable> ResponseResult<T> fail(String message) {
        return fail(null, message);
    }

    /**
     * response error result wrapper.
     *
     * @param data    response data
     * @param message error message
     * @param <T>     type of data class
     * @return response result
     */
    public static <T> ResponseResult<T> fail(T data, String message) {
        return ResponseResult.<T>builder().data(data)
                .message(message)
                .status(ResponseStatus.FAIL.getResponseCode())
                .timestamp(System.currentTimeMillis())
                .build();
    }


}
```

### controller接口

```java
package tech.pdai.ratelimit.guava.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import tech.pdai.ratelimit.guava.config.ratelimit.RateLimit;
import tech.pdai.ratelimit.guava.config.response.ResponseResult;

/**
 * @author pdai
 */
@Slf4j
@RestController
public class RateLimitTestController {

    @RateLimit
    @GetMapping("/limit")
    public ResponseResult<String> limit() {
        log.info("limit");
        return ResponseResult.success();
    }

    @RateLimit(limit = 5)
    @GetMapping("/limit1")
    public ResponseResult<String> limit1() {
        log.info("limit1");
        return ResponseResult.success();
    }

    @GetMapping("/nolimit")
    public ResponseResult<String> noRateLimiter() {
        log.info("no limit");
        return ResponseResult.success();
    }

}
```

### 接口测试

```java
@SneakyThrows
public static void test(int clientSize) {
    CountDownLatch downLatch = new CountDownLatch(clientSize);
    ExecutorService fixedThreadPool = Executors.newFixedThreadPool(clientSize);
    IntStream.range(0, clientSize).forEach(i ->
            fixedThreadPool.submit(() -> {
                RestTemplate restTemplate = new RestTemplate();
                restTemplate.getForObject("http://localhost:8080/limit1", ResponseResult.class);
                downLatch.countDown();
            })
    );
    downLatch.await();
    fixedThreadPool.shutdown();
}
```

测试结果

```java
2021-10-01 15:22:47.171  INFO 30092 --- [nio-8080-exec-4] t.p.r.g.c.RateLimitTestController        : limit1
2021-10-01 15:22:47.171  INFO 30092 --- [nio-8080-exec-8] t.p.r.g.c.RateLimitTestController        : limit1
2021-10-01 15:22:47.171  INFO 30092 --- [nio-8080-exec-5] t.p.r.g.c.RateLimitTestController        : limit1
2021-10-01 15:22:47.187  INFO 30092 --- [nio-8080-exec-9] t.p.r.g.c.RateLimitTestController        : limit1
2021-10-01 15:22:47.187  INFO 30092 --- [nio-8080-exec-2] t.p.r.g.c.RateLimitTestController        : limit1
2021-10-01 15:22:47.187  INFO 30092 --- [io-8080-exec-10] t.p.r.g.c.RateLimitTestController        : limit1
2021-10-01 15:22:47.202 ERROR 30092 --- [nio-8080-exec-7] t.p.r.g.c.e.GlobalExceptionHandler       : too many requests, please try again later...
2021-10-01 15:22:47.202 ERROR 30092 --- [nio-8080-exec-6] t.p.r.g.c.e.GlobalExceptionHandler       : too many requests, please try again later...
2021-10-01 15:22:47.221 ERROR 30092 --- [nio-8080-exec-1] t.p.r.g.c.e.GlobalExceptionHandler       : too many requests, please try again later...
2021-10-01 15:22:47.222 ERROR 30092 --- [nio-8080-exec-5] t.p.r.g.c.e.GlobalExceptionHandler       : too many requests, please try again later...
2021-10-01 15:22:47.225 ERROR 30092 --- [nio-8080-exec-6] t.p.r.g.c.e.GlobalExceptionHandler       : too many requests, please try again later...
2021-10-01 15:22:47.225 ERROR 30092 --- [nio-8080-exec-8] t.p.r.g.c.e.GlobalExceptionHandler       : too many requests, please try again later...
2021-10-01 15:22:47.225 ERROR 30092 --- [nio-8080-exec-3] t.p.r.g.c.e.GlobalExceptionHandler       : too many requests, please try again later...
2021-10-01 15:22:47.225 ERROR 30092 --- [io-8080-exec-12] t.p.r.g.c.e.GlobalExceptionHandler       : too many requests, please try again later...
2021-10-01 15:22:47.225 ERROR 30092 --- [io-8080-exec-14] t.p.r.g.c.e.GlobalExceptionHandler       : too many requests, please try again later...
2021-10-01 15:22:47.225 ERROR 30092 --- [io-8080-exec-13] t.p.r.g.c.e.GlobalExceptionHandler       : too many requests, please try again later...
2021-10-01 15:22:47.225 ERROR 30092 --- [io-8080-exec-15] t.p.r.g.c.e.GlobalExceptionHandler       : too many requests, please try again later...
2021-10-01 15:22:47.240 ERROR 30092 --- [io-8080-exec-11] t.p.r.g.c.e.GlobalExceptionHandler       : too many requests, please try again later...
2021-10-01 15:22:47.240 ERROR 30092 --- [nio-8080-exec-4] t.p.r.g.c.e.GlobalExceptionHandler       : too many requests, please try again later...
2021-10-01 15:22:47.256 ERROR 30092 --- [nio-8080-exec-2] t.p.r.g.c.e.GlobalExceptionHandler       : too many requests, please try again later...
```

### 上述实现方案的槽点

注意

必须要说明一下，**上述实现方式只是单实例下一种思路而已**，如果细细的看，上面的代码存在一些槽点。

1. 首先, `EXISTED_RATE_LIMITERS.computeIfAbsent(method.getName(), k -> RateLimiter.create(annotation.limit()))` 这行代码中 `method.getName()`表明是对方法名进行限流的，其实并不合适，应该需要至少加上类名；
2. 其次, 如果首次运行时访问的请求是一次性涌入的，即EXISTED_RATE_LIMITERS还是空的时候并发请求@RateLimit接口，那么RateLimiter.create(annotation.limit())是会重复创建并加入到EXISTED_RATE_LIMITERS的，这是明显的bug；
3. 再者, 上述实现方式按照方法名去限定请求量，对于很多情况下至少需要支持按照IP和方法名，或者其它自定义的方式进行限流。
4. 其它一些场景支持的参数抽象和封装等

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos