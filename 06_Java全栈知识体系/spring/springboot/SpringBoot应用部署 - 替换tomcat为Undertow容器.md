# SpringBoot应用部署 - 替换tomcat为Undertow容器

> 前文我们了解到Jetty更满足公有云的分布式环境的需求，而Tomcat更符合企业级环境；那么从性能的角度来看，更为优秀的servlet容器是Undertow。本文将介绍Undertow，以及SpringBoot集成Undertow的示例。@pdai

## 概述

> 需要了解什么是Undertow，以及Undertow的性能优势。

### 什么是Undertow?

> 内容来源于[Undertow官网](https://undertow.io/)

Undertow 是一个采用 Java 开发的灵活的高性能 Web 服务器，提供包括阻塞和基于 NIO 的非堵塞机制。Undertow 是RedHat公司的开源产品(原先是JBoss的产品，然后Redhat收购了JBoss)，是 Wildfly 默认的 Web 服务器。

Undertow 提供一个基础的架构用来构建 Web 服务器，这是一个完全为嵌入式设计的项目，提供易用的构建器 API，完全兼容 Java EE Servlet 4 和低级非堵塞的处理器。

Undertow设计为完全可嵌入的，并具有易于使用的流畅的Builder API。 Undertow的生命周期完全由嵌入应用程序控制。

**Undertow的特性有哪些**？

- **HTTP/2 Support** Undertow 支持 HTTP/2 开箱即用，不需要重写引导类路径。
- **支持 HTTP 升级** 支持 HTTP 升级，允许多个协议通过 HTTP 端口上进行复用。
- **支持 Web Socket** Undertow 提供对 Web 套接字的全面支持，包括对 JSR-356 的支持。
- **支持 Servlet 4.0** Undertow 提供了对 Servlet 4.0 的支持，包括对嵌入式 Servlet 的支持，还可以混合部署 Servlet 和原生 Undertow 非阻塞处理程序。
- **可嵌入式** Undertow 可以嵌入到应用程序中，也可以通过几行代码独立运行。
- **高灵活性** 一个 Undertow 服务器是通过链式处理器来配置的，可以根据需要添加功能，因此可以避免添加没有必要的功能。

### Undertow性能比jetty和tomcat强多少？

> 关于Undertow的性能和jetty,tomcat对于，可以看如下两篇文章：

1. [Tomcat vs. Jetty vs. Undertow: Comparison of Spring Boot Embedded Servlet Containers](https://examples.javacodegeeks.com/enterprise-java/spring/tomcat-vs-jetty-vs-undertow-comparison-of-spring-boot-embedded-servlet-containers/)
2. [Tomcat vs Jetty vs Undertow性能对比](https://cloud.tencent.com/developer/article/1699803)

大概的结论是：综合吞吐量，响应时间以及资源消耗，Undertow胜出

1. 吞吐量及响应时间
   1. 吞吐量：Undertow > Jetty > Tomcat
   2. 响应时间：Jetty < Tomcat < Undertow
2. CPU使用率：Undertow < Jetty < Tomcat
3. 内存使用率：Undertow < Jetty < Tomcat
4. 线程数：Undertow < Jetty < Tomcat

## 替换tomcat为Undertow容器

> 这里以一个Helloworld项目（[SpringBoot入门 - 创建第一个Hello world工程](SpringBoot入门 - SpringBoot HelloWorld.md)）为例，在此基础上移除内嵌的Tomcat并使用Undertow。

### 移除内嵌的Tomcat并使用Undertow

移除内嵌的Tomcat相关的依赖spring-boot-starter-tomcat，并增加undertow的依赖spring-boot-starter-undertow

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
            <artifactId>spring-boot-starter-tomcat</artifactId>
            <groupId>org.springframework.boot</groupId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-undertow</artifactId>
</dependency>
```

### 配置Undertow

Undertow相关的配置可以看：

![](https://www.pdai.tech/images/spring/springboot/springboot-x-undertow-1.png)

### 简单测试

运行SpringBootApplication

结果如下

![](https://www.pdai.tech/images/spring/springboot/springboot-x-undertow-2.png)

运行的日志如下

```bash
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |___, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::                (v2.5.3)

2022-04-18  22:47:28.900  INFO 60368 --- [           main] .p.s.h.u.SpringBootHelloWorldApplication : Starting SpringBootHelloWorldApplication using Java 1.8.0_181 on MacBook-Pro.local with PID 60368 (/Users/pdai/pdai/www/tech-pdai-spring-demos/105-springboot-demo-helloworld-undertow/target/classes started by pdai in /Users/pdai/pdai/www/tech-pdai-spring-demos)
2022-04-18  22:47:28.902  INFO 60368 --- [           main] .p.s.h.u.SpringBootHelloWorldApplication : No active profile set, falling back to default profiles: default
2022-04-18  22:47:29.691  WARN 60368 --- [           main] io.undertow.websockets.jsr               : UT026010: Buffer pool was not set on WebSocketDeploymentInfo, the default pool will be used
2022-04-18  22:47:29.710  INFO 60368 --- [           main] io.undertow.servlet                      : Initializing Spring embedded WebApplicationContext
2022-04-18  22:47:29.710  INFO 60368 --- [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 769 ms
2022-04-18  22:47:30.020  INFO 60368 --- [           main] io.undertow                              : starting server: Undertow - 2.2.9.Final
2022-04-18  22:47:30.025  INFO 60368 --- [           main] org.xnio                                 : XNIO version 3.8.4.Final
2022-04-18  22:47:30.029  INFO 60368 --- [           main] org.xnio.nio                             : XNIO NIO Implementation Version 3.8.4.Final
2022-04-18  22:47:30.060  INFO 60368 --- [           main] org.jboss.threads                        : JBoss Threads version 3.1.0.Final
2022-04-18  22:47:30.121  INFO 60368 --- [           main] o.s.b.w.e.undertow.UndertowWebServer     : Undertow started on port(s) 8080 (http)
2022-04-18  22:47:30.132  INFO 60368 --- [           main] .p.s.h.u.SpringBootHelloWorldApplication : Started SpringBootHelloWorldApplication in 1.586 seconds (JVM running for 2.215)
```

## 进一步理解

> 通过几个问题进一步理解。

### 在异步NIO环境下的性能？

> 结论来源于：https://blog.51cto.com/u_3664660/3212743

HTTP异步的目的在帮助dispatcherservlet分担压力，提升吞吐量。但如果运行在NIO模式的服务容器上，就会产生负面影响，因为NIO本身就做了类似的事情，此时再加HTTP异步，则相当于又加了N多不必要的线程，导致性能主要消耗在线程的开销上，所以**建议使用tomcat作为内嵌容器并且没有开启tomcat的NIO模式时，可以配合HTTP异步来提升程序性能**。尤其是当业务繁重时，提升效果尤其明显。

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos