# SpringBoot应用部署 - 替换tomcat为Jetty容器

> 前文我们知道spring-boot-starter-web默认集成tomcat servlet容器(被使用广泛）；而Jetty也是servlet容器，它具有易用性，轻量级，可拓展性等，有些场景（Jetty更满足公有云的分布式环境的需求，而Tomcat更符合企业级环境）下会使用jetty容器。本文主要介绍SpringBoot使用Jetty容器。@pdai

## 概述

> 通过Jetty和Tomcat容器的对比，来理解什么样的场景会使用Jetty容器。

### 什么是Jetty

> 来源于百度百科

Jetty 是一个开源的servlet容器，它为基于Java的web容器，例如JSP和servlet提供运行环境。Jetty是使用Java语言编写的，它的API以一组JAR包的形式发布。开发人员可以将Jetty容器实例化成一个对象，可以迅速为一些独立运行(stand-alone)的Java应用提供网络和web连接。

- **易用性**

易用性是 Jetty 设计的基本原则，易用性主要体现在以下几个方面：

1. 通过 XML 或者 API 来对Jetty进行配置；
2. 默认配置可以满足大部分的需求；
3. 将 Jetty 嵌入到应用程序当中只需要非常少的代码；

- **可扩展性**

在使用了 Ajax 的 Web 2.0 的应用程序中，每个连接需要保持更长的时间，这样线程和内存的消耗量会急剧的增加。这就使得我们担心整个程序会因为单个组件陷入瓶颈而影响整个程序的性能。但是有了 Jetty：

1. 即使在有大量服务请求的情况下，系统的性能也能保持在一个可以接受的状态。
2. 利用 Continuation 机制来处理大量的用户请求以及时间比较长的连接。
3. 另外 Jetty 设计了非常良好的接口，因此在 Jetty 的某种实现无法满足用户的需要时，用户可以非常方便地对 Jetty 的某些实现进行修改，使得 Jetty 适用于特殊的应用程序的需求。

- **易嵌入性**

Jetty 设计之初就是作为一个优秀的组件来设计的，这也就意味着 Jetty 可以非常容易的嵌入到应用程序当中而不需要程序为了使用 Jetty 做修改。从某种程度上，你也可以把 Jetty 理解为一个嵌入式的Web服务器。

Jetty 可以作为嵌入式服务器使用，Jetty的运行速度较快，而且是轻量级的，可以在Java中可以从test case中控制其运行。从而可以使自动化测试不再依赖外部环境，顺利实现自动化测试。

### Jetty和Tomcat容器对比

> Tomcat和Jetty都是一种Servlet引擎，他们都支持标准的servlet规范和JavaEE的规范。以下对比来源于百度百科：

- **Jetty更轻量级**。这是相对Tomcat而言的。

由于Tomcat除了遵循Java Servlet规范之外，自身还扩展了大量J2EE特性以满足企业级应用的需求，所以Tomcat是较重量级的，而且配置较Jetty亦复杂许多。但对于大量普通互联网应用而言，并不需要用到Tomcat其他高级特性，所以在这种情况下，使用Tomcat是很浪费资源的。这种劣势放在分布式环境下，更是明显。换成Jetty，对新的Servlet规范的支持较好，且每个应用服务器省下那几兆内存，对于大的分布式环境则是节省大量资源。而且，Jetty的轻量级也使其在处理高并发细粒度请求的场景下显得更快速高效。

- **Jetty更灵活**

体现在其可插拔性和可扩展性，更易于开发者对Jetty本身进行二次开发，定制一个适合自身需求的Web Server。 相比之下，重量级的Tomcat原本便支持过多特性，要对其瘦身的成本远大于丰富Jetty的成本。用自己的理解，即增肥容易减肥难。

- 然而，**当支持大规模企业级应用时**

Jetty也许便需要扩展，在这场景下Tomcat便是更优的。

总结：**Jetty更满足公有云的分布式环境的需求，而Tomcat更符合企业级环境**。

## 替换tomcat为jetty容器

> 这里以一个Helloworld项目（[SpringBoot入门 - 创建第一个Hello world工程](SpringBoot入门 - SpringBoot HelloWorld.md)）为例，在此基础上移除内嵌的Tomcat并使用jetty。

### 移除内嵌的Tomcat并使用jetty

移除内嵌的Tomcat相关的依赖spring-boot-starter-tomcat，并增加jetty的依赖spring-boot-starter-jetty

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
    <artifactId>spring-boot-starter-jetty</artifactId>
</dependency>
```

### 配置jetty

jetty相关的配置可以看：

![](https://www.pdai.tech/images/spring/springboot/springboot-x-jetty-1.png)

### 简单测试

运行SpringBootApplication

结果如下

![](https://www.pdai.tech/images/spring/springboot/springboot-x-jetty-2.png)

运行的日志如下

```bash
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |___, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::                (v2.5.3)

2022-04-18  21:09:21.749  INFO 54806 --- [           main] .p.s.h.j.SpringBootHelloWorldApplication : Starting SpringBootHelloWorldApplication using Java 1.8.0_181 on MacBook-Pro.local with PID 54806 (/Users/pdai/pdai/www/tech-pdai-spring-demos/104-springboot-demo-helloworld-jetty/target/classes started by pdai in /Users/pdai/pdai/www/tech-pdai-spring-demos)
2022-04-18  21:09:21.752  INFO 54806 --- [           main] .p.s.h.j.SpringBootHelloWorldApplication : No active profile set, falling back to default profiles: default
2022-04-18  21:09:22.484  INFO 54806 --- [           main] org.eclipse.jetty.util.log               : Logging initialized @1888ms to org.eclipse.jetty.util.log.Slf4jLog
2022-04-18  21:09:22.556  INFO 54806 --- [           main] o.s.b.w.e.j.JettyServletWebServerFactory : Server initialized with port: 8080
2022-04-18  21:09:22.558  INFO 54806 --- [           main] org.eclipse.jetty.server.Server          : jetty-9.4.43.v20210629; built: 2021-06-30T11:07:22.254Z; git: 526006ecfa3af7f1a27ef3a288e2bef7ea9dd7e8; jvm 1.8.0_181-b13
2022-04-18  21:09:22.577  INFO 54806 --- [           main] o.e.j.s.h.ContextHandler.application     : Initializing Spring embedded WebApplicationContext
2022-04-18  21:09:22.577  INFO 54806 --- [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 755 ms
2022-04-18  21:09:22.632  INFO 54806 --- [           main] org.eclipse.jetty.server.session         : DefaultSessionIdManager workerName=node0
2022-04-18  21:09:22.632  INFO 54806 --- [           main] org.eclipse.jetty.server.session         : No SessionScavenger set, using defaults
2022-04-18  21:09:22.633  INFO 54806 --- [           main] org.eclipse.jetty.server.session         : node0 Scavenging every 660000ms
2022-04-18  21:09:22.638  INFO 54806 --- [           main] o.e.jetty.server.handler.ContextHandler  : Started o.s.b.w.e.j.JettyEmbeddedWebAppContext@232024b9{application,/,[file:///private/var/folders/p9/9xtytd4j6lxc0ttbpjx63s2c0000gn/T/jetty-docbase.8080.6026164686377179293/],AVAILABLE}
2022-04-18  21:09:22.638  INFO 54806 --- [           main] org.eclipse.jetty.server.Server          : Started @2043ms
2022-04-18  21:09:22.887  INFO 54806 --- [           main] o.e.j.s.h.ContextHandler.application     : Initializing Spring DispatcherServlet 'dispatcherServlet'
2022-04-18  21:09:22.887  INFO 54806 --- [           main] o.s.web.servlet.DispatcherServlet        : Initializing Servlet 'dispatcherServlet'
2022-04-18  21:09:22.888  INFO 54806 --- [           main] o.s.web.servlet.DispatcherServlet        : Completed initialization in 1 ms
2022-04-18  21:09:22.905  INFO 54806 --- [           main] o.e.jetty.server.AbstractConnector       : Started ServerConnector@78461bc4{HTTP/1.1, (http/1.1)}{0.0.0.0:8080}
2022-04-18  21:09:22.906  INFO 54806 --- [           main] o.s.b.web.embedded.jetty.JettyWebServer  : Jetty started on port(s) 8080 (http/1.1) with context path '/'
2022-04-18  21:09:22.914  INFO 54806 --- [           main] .p.s.h.j.SpringBootHelloWorldApplication : Started SpringBootHelloWorldApplication in 1.648 seconds (JVM running for 2.32)
```

## 进一步理解

> 通过几个问题进一步理解。

### Google将默认的应用引擎切换为Jetty?

> Google 应用系统引擎最初是以 Apache Tomcat 作为其 webserver/servlet 容器的，但最终将切换到 Jetty 上。为什么要做这样的改变？

**不是为了性能，而是轻量级**！

Google选择Jetty的关键原因是它的体积和灵活性。在云计算里，体积的因素是很重要，如果你运行几万个Jetty的实例（Google就是这样干的），每个server省1兆，那就会省10几个G的内存（或能够给其他应用提供更多的内存）。

Jetty 被设计成了可插拔和可扩展的特性，这样Google就可以高度的自定义它。他们在其中替换了他们自己的HTTP connector，Google认证，以及他们自己的session集群。也真是奇怪，这个特性对于云计算来说是非常出色的，但同时也让Jetty非常适合嵌入小的设备中，例如手机和机顶盒。

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos