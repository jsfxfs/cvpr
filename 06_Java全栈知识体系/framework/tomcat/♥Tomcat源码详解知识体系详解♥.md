# ♥Tomcat源码详解知识体系详解♥

> 本系列主要对Tomcat源码知识体系进行深入理解。

## 知识体系

*结构图*

![](https://www.pdai.tech/images/tomcat/tomcat-x-design-2-1.jpeg)

*初始化和启动流程*

![](https://www.pdai.tech/images/tomcat/tomcat-x-start-1.png)

*相关文章*

- [Tomcat - 如何设计一个简单的web容器](Tomcat - 如何设计一个简单的web容器.md)
  - 在学习Tomcat前，很多人先入为主的对它的认知是巨复杂的；所以第一步，在学习它之前，要打破这种观念，我们通过学习如何设计一个最基本的web容器来看它需要考虑什么；进而在真正学习Tomcat时，多把重点放在它的顶层设计上，而不是某一块代码上, 思路永远比具体实现重要的多。
- [Tomcat - 理解Tomcat架构设计](Tomcat - 理解Tomcat架构设计.md)
  - 前文我们已经介绍了一个简单的Servlet容器是如何设计出来，我们就可以开始正式学习Tomcat了，在学习开始，我们有必要站在高点去看看Tomcat的架构设计。
- [Tomcat - 源码分析准备和分析入口](Tomcat - 源码分析准备和分析入口.md)
  - 上文我们介绍了Tomcat的架构设计，接下来我们便可以下载源码以及寻找源码入口了。
- [Tomcat - 启动过程：初始化和启动流程](Tomcat - 启动过程：初始化和启动流程.md)
  - 在有了Tomcat架构设计和源码入口以后，我们便可以开始真正读源码了。
- [Tomcat - 启动过程:类加载机制详解](Tomcat - 启动过程：类加载机制详解.md)
  - 上文我们讲了Tomcat在初始化时会初始化classLoader。本文将具体分析Tomcat的类加载机制，特别是区别于传统的`双亲委派模型`的加载机制。
- [Tomcat - 启动过程:Catalina的加载](Tomcat - 启动过程：Catalina的加载.md)
  - 通过前两篇文章，我们知道了[Tomcat的类加载机制](Tomcat - 启动过程：类加载机制详解.md)和[整体的组件加载流程](Tomcat - 启动过程：初始化和启动流程.md)；我们也知道通过Bootstrap初始化的catalinaClassLoader加载了Catalina，那么进而引入了一个问题就是Catalina是如何加载的呢？加载了什么呢？本文将带你进一步分析。
- [Tomcat - 组件生命周期管理:LifeCycle](Tomcat - 组件生命周期管理：LifeCycle.md)
  - 上文中，我们已经知道Catalina初始化了Server（它调用了 Server 类的 init 和 start 方法来启动 Tomcat）；你会发现Server是Tomcat的配置文件server.xml的顶层元素，那这个阶段其实我们已经进入到Tomcat内部组件的详解；这时候有一个问题，这么多组件是如何管理它的生命周期的呢？
- [Tomcat - 组件拓展管理:JMX和MBean](Tomcat - 组件拓展管理：JMX和MBean.md)
  - 我们在前文中讲Lifecycle以及组件，怎么会突然讲JMX和MBean呢？本文通过承接上文Lifecycle讲Tomcat基于JMX的实现。
- [Tomcat - 事件的监听机制：观察者模式](Tomcat - 事件的监听机制：观察者模式.md)
  - 本文承接上文中Lifecycle中实现，引出Tomcat的监听机制。
- [Tomcat - Server的设计和实现: StandardServer](Tomcat - Server的设计和实现： StandardServer.md)
  - 基于前面的几篇文章，我们终于可以总体上梳理Server的具体实现了，这里体现在StandardServer具体的功能实现上。
- [Tomcat - Service的设计和实现: StandardService](Tomcat - Service的设计和实现： StandardService.md)
  - 上文讲了Server的具体实现了，本文主要讲Service的设计和实现；我们从上文其实已经知道Server中包含多个service了。
- [Tomcat - 线程池的设计与实现：StandardThreadExecutor](Tomcat - 线程池的设计与实现：StandardThreadExecutor.md)
  - 上文中我们研究了下Service的设计和实现，StandardService中包含Executor的调用；这个比较好理解，Tomcat需要并发处理用户的请求，自然而言就想到线程池，那么Tomcat中线程池（Executor）具体是如何实现的？本文带你继续深度解析。
- [Tomcat - Request请求处理: Container设计](Tomcat - Request请求处理： Container设计.md)
  - 在理解了Server，Service和Executor后，我们可以进入Request处理环节了。我们知道客户端是可以发起多个请求的，Tomcat也是可以支持多个webapp的，有多个上下文，且一个webapp中可以有多个Servlet...等等，那么Tomcat是如何设计组件来支撑请求处理的呢？本节文将介绍Tomcat的Container设计。
- [Tomcat - Container容器之Engine：StandardEngine](Tomcat - Container容器之Engine：StandardEngine.md)
  - 上文已经知道Container的整体结构和设计，其中Engine其实就是Servlet Engine，负责处理request的顶层容器。
- [Tomcat - Container的管道机制：责任链模式](Tomcat - Container的管道机制：责任链模式.md)
  - 上文中介绍了Engine的设计，其中有Pipline相关内容没有介绍，本文将向你阐述Tomcat的管道机制以及它要解决的问题。
- [Tomcat - Request请求处理过程：Connector](Tomcat - Request请求处理过程：Connector.md)
  - 本文主要介绍request请求的处理过程。

## 参考文章

- Tomcat - 如何设计一个最简单的web容器
  - https://segmentfault.com/q/1010000024466207?utm_source=tag-newest
  - https://www.jianshu.com/p/e438d2f1e4c2
- Tomcat整体架构
  - https://www.jianshu.com/p/2b6359daf5c8
  - https://www.jianshu.com/p/8b7f81bd5e26
  - https://www.cnblogs.com/wangjiming/p/12519306.html
  - https://www.cnblogs.com/tanshaoshenghao/p/10932306.html
- Tomcat源码下载和源码入口
  - https://tomcat.apache.org/download-90.cgi
  - https://www.cnblogs.com/tanshaoshenghao/p/10932306.html
- Tomcat - Tomcat启动过程：Bootstrap和Catina详解
  - https://www.jianshu.com/p/2ec610e923ff
- Tomcat - Tomcat启动过程：Tomcat中类加载
  - https://www.jianshu.com/p/51b2c50c58eb
  - https://www.jianshu.com/p/abf6fd4531e7
- Tomcat - Tomcat启动过程：生命周期Lifecycle
  - https://www.jianshu.com/p/2a9ffbd00724
- Tomcat - Tomcat启动过程：组件管理JMX
  - https://www.jianshu.com/p/d417f308f4f5
- Tomcat - 连接器Connector详解
  - https://www.jianshu.com/p/f67f613ebc79
- Tomcat - 请求过程详解
  - https://www.jianshu.com/p/857baa251902
- Tomcat - 设计模式
  - https://developer.ibm.com/zh/articles/j-lo-tomcat2/
  - https://blog.csdn.net/Allen202/article/details/91346855

系列

- https://www.jianshu.com/p/c74d2df8bc8a
- https://www.jianshu.com/nb/18936835
- https://segmentfault.com/u/keguan/articles