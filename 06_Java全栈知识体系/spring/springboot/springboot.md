# ♥SpringBoot 知识体系详解♥

提示

Spring，Spring Boot系列的章节在整理中... 包含实际业务开发中的方方面面... @pdai

**PS：本来没想写那么多的，没想到梳理了一下知识体系，一发不可收拾**； 来时好好的，回不去了... 计划5月份完成大部分。 2022.04.15 @pdai

## 相关文章

> 站在知识体系的视角，基于SpringBoot开发。@pdai

### SpringBoot入门(helloworld,banner,logback,分层设计)

> 首先，在开始SpringBoot开发时，我们了解一些技术栈背景并通过Hello World级别应用程序开始延伸出SpringBoot入门应用的开发。

- [SpringBoot入门 - SpringBoot 简介](springboot-x-overview.md)
  - 为什么有了SpringFramework还会诞生SpringBoot？简单而言，因为虽然Spring的组件代码是轻量级的，但它的配置却是重量级的；所以SpringBoot的设计策略是通过开箱即用和约定大于配置 来解决配置重的问题的。
- [SpringBoot入门 - 创建第一个Hello world工程](springboot-x-hello-world.md)
  - 我们了解了SpringBoot和SpringFramework的关系之后，我们可以开始创建一个Hello World级别的项目了。
- [SpringBoot入门 - 对Hello world进行MVC分层](springboot-x-hello-world-mvc.md)
  - 上文中我们创建一个简单的Hello Wold级别的web应用程序，但是存在一个问题，我们将所有代码都放在一个类中的, 这显然是不合理的，那么一个经典的CRUD项目如何分包呢？本文结合常见的MVC分层思路带你学习常见的包结构划分。
- [SpringBoot入门 - 添加内存数据库H2](springboot-x-hello-h2-jpa.md)
  - 上文我们展示了通过学习经典的MVC分包结构展示了一个用户的增删查改项目，但是我们没有接入数据库；本文将在上文的基础上，增加一个H2内存数据库，并且通过Spring 提供的数据访问包JPA进行数据查询。
- [SpringBoot入门 - 定制自己的Banner](springboot-x-hello-banner.md)
  - 我们在启动Spring Boot程序时，有SpringBoot的Banner信息，那么如何自定义成自己项目的信息呢？
- [SpringBoot入门 - 添加Logback日志](springboot-x-hello-logback.md)
  - SpringBoot开发中如何选用日志框架呢？ 出于性能等原因，Logback 目前是springboot应用日志的标配； 当然有时候在生产环境中也会考虑和三方中间件采用统一处理方式。
- [SpringBoot入门 - 配置热部署devtools工具](springboot-x-hello-devtool.md)
  - 在SpringBoot开发调试中，如果我每行代码的修改都需要重启启动再调试，可能比较费时间；SpringBoot团队针对此问题提供了spring-boot-devtools（简称devtools）插件，它试图提升开发调试的效率。
- [SpringBoot入门 - 开发中还有哪些常用注解](springboot-x-hello-anno.md)
  - SpringBoot中常用的注解

### SpringBoot接口设计和实现(封装,校验,异常,加密,幂等)

> 接着， 站在接口设计和实现的角度，从实战开发中梳理出，关于接口开发的技术要点。

- [SpringBoot接口 - 如何统一接口封装](springboot-x-interface-response.md)
  - 在以SpringBoot开发Restful接口时，统一返回方便前端进行开发和封装，以及出现时给出响应编码和信息。
- [SpringBoot接口 - 如何对参数进行校验](springboot-x-interface-param.md)
  - 在以SpringBoot开发Restful接口时, 对于接口的查询参数后台也是要进行校验的，同时还需要给出校验的返回信息放到上文我们统一封装的结构中。那么如何优雅的进行参数的统一校验呢？
- [SpringBoot接口 - 如何参数校验国际化](springboot-x-interface-param-i18n.md)
  - 上文我们学习了如何对SpringBoot接口进行参数校验，但是如果需要有国际化的信息，应该如何优雅处理呢？
- [SpringBoot接口 - 如何统一异常处理](springboot-x-interface-exception.md)
  - SpringBoot接口如何对异常进行统一封装，并统一返回呢？以上文的参数校验为例，如何优雅的将参数校验的错误信息统一处理并封装返回呢？
- [SpringBoot接口 - 如何提供多个版本接口](springboot-x-interface-version.md)
  - 在以SpringBoot开发Restful接口时，由于模块，系统等业务的变化，需要对同一接口提供不同版本的参数实现（老的接口还有模块或者系统在用，不能直接改，所以需要不同版本）。如何更加优雅的实现多版本接口呢？
- [SpringBoot接口 - 如何生成接口文档之Swagger技术栈](springboot-x-interface-doc.md)
  - SpringBoot开发Restful接口，有什么API规范吗？如何快速生成API文档呢？Swagger 是一个用于生成、描述和调用 RESTful 接口的 Web 服务。通俗的来讲，Swagger 就是将项目中所有（想要暴露的）接口展现在页面上，并且可以进行接口调用和测试的服务。本文主要介绍OpenAPI规范，以及Swagger技术栈基于OpenAPI规范的集成方案。
- [SpringBoot接口 - 如何生成接口文档之集成Smart-Doc](springboot-x-interface-doc-smart.md)
  - 上文我们看到可以通过Swagger系列可以快速生成API文档， 但是这种API文档生成是需要在接口上添加注解等，这表明这是一种侵入式方式； 那么有没有非侵入式方式呢, 比如通过注释生成文档？ 本文主要介绍非侵入式的方式及集成Smart-doc案例。我们构建知识体系时使用Smart-doc这类工具并不是目标，而是**要了解非侵入方式能做到什么程度和技术思路**, 最后**平衡**下来多数情况下多数人还是会选择Swagger+openapi技术栈的。
- [SpringBoot接口 - 如何访问外部接口](springboot-x-interface-3rd.md)
  - 在SpringBoot接口开发中，存在着本模块的代码需要访问外面模块接口或外部url链接的需求, 比如调用外部的地图API或者天气API。那么有哪些方式可以调用外部接口呢？
- [SpringBoot接口 - 如何对接口进行加密](springboot-x-interface-jiami.md)
  - 在以SpringBoot开发后台API接口时，会存在哪些接口不安全的因素呢？通常如何去解决的呢？本文主要介绍API**接口有不安全的因素**以及**常见的保证接口安全的方式**，重点**实践如何对接口进行签名**。
- [SpringBoot接口 - 如何保证接口幂等](springboot-x-interface-mideng.md)
  - 在以SpringBoot开发Restful接口时，如何防止接口的重复提交呢？ 本文主要介绍接口幂等相关的知识点，并实践常见基于Token实现接口幂等。
- [SpringBoot接口 - 如何实现接口限流之单实例](springboot-x-interface-xianliu.md)
  - 在以SpringBoot开发Restful接口时，当流量超过服务极限能力时，系统可能会出现卡死、崩溃的情况，所以就有了降级和限流。在接口层如何做限流呢？ 本文主要回顾限流的知识点，并实践单实例限流的一种思路。
- [SpringBoot接口 - 如何实现接口限流之分布式](springboot-x-interface-xianliu-dist.md)
  - 上文中介绍了单实例下如何在业务接口层做限流，本文主要介绍分布式场景下限流的方案，以及什么样的分布式场景下需要在业务层加限流而不是接入层; 并且结合kailing开源的[ratelimiter-spring-boot-starter](https://gitee.com/kailing/ratelimiter-spring-boot-starter)为例， 学习**思路+代码封装+starter封装**。

### SpringBoot集成MySQL(JPA,MyBatis,MyBatis-Plus)

> 接下来，我们学习SpringBoot如何集成数据库，比如MySQL数据库，常用的方式有JPA和MyBatis。

- [SpringBoot集成MySQL - 基于JPA的封装](springboot-x-mysql-jpa.md)
  - 在实际开发中，最为常见的是基于数据库的CRUD封装等，比如SpringBoot集成MySQL数据库，常用的方式有JPA和MyBatis； 本文主要介绍基于JPA方式的基础封装思路。
- [SpringBoot集成MySQL - MyBatis XML方式](springboot-x-mysql-mybatis-xml.md)
  - 上文介绍了用JPA方式的集成MySQL数据库，JPA方式在中国以外地区开发而言基本是标配，在国内MyBatis及其延伸框架较为主流。本文主要介绍**MyBatis技栈的演化**以及**SpringBoot集成基础的MyBatis XML实现方式**的实例。
- [SpringBoot集成MySQL - MyBatis 注解方式](springboot-x-mysql-mybatis-anno.md)
  - 上文主要介绍了Spring集成MyBatis访问MySQL，采用的是XML配置方式；我们知道除了XML配置方式，MyBatis还支持注解方式。本文主要介绍SpringBoot+MyBatis注解方式。
- [SpringBoot集成MySQL - MyBatis PageHelper分页](springboot-x-mysql-mybatis-page.md)
  - 前文中，我们展示了Spring Boot与MyBatis的集成，但是没有展示分页实现。本文专门介绍分页相关知识体系和基于MyBatis的物理分页PageHelper。
- [SpringBoot集成MySQL - MyBatis 多个数据源](springboot-x-mysql-mybatis-multi-ds.md)
  - 前文介绍的SpringBoot集成单个MySQL数据库的情形，那么什么场景会使用多个数据源以及什么场景会需要多个数据源的动态切换呢？本文主要介绍上述场景及SpringBoot+MyBatis实现多个数据源的方案和示例。
- [SpringBoot集成MySQL - MyBatis-Plus方式](springboot-x-mysql-mybatis-plus.md)
  - MyBatis-Plus（简称 MP）是一个 MyBatis的增强工具，在 MyBatis 的基础上只做增强不做改变，为简化开发、提高效率而生。MyBatis-Plus在国内也有很多的用户，本文主要介绍MyBatis-Plus和SpringBoot的集成。
- [SpringBoot集成MySQL - MyBatis-Plus代码自动生成](springboot-x-mysql-mybatis-plus-gen.md)
  - 本文主要介绍 MyBatis-Plus代码自动生成，以及产生此类代码生成工具的背景和此类工具的基本实现原理。
- [SpringBoot集成MySQL - MyBatis-Plus基于字段隔离的多租户](springboot-x-mysql-mybatis-plus-multi-tenant.md)
  - 本文主要介绍 MyBatis-Plus的基于字段隔离的多租户实现，以及MyBatis-Plus的基于字段的隔离方式实践和原理。

### SpringBoot集成ShardingJDBC(分表分库,读写分离,多租户)

> 随着数据量和业务的增长，我们还需要进行分库分表，这里主要围绕ShardingSphere中间件来实现分库分表，读写分离和多租户等。

- [SpringBoot集成ShardingJDBC - Sharding-JDBC简介和基于MyBatis的单库分表](springboot-x-mysql-shardingjdbc.md)
  - 本文主要介绍分表分库，以及SpringBoot集成基于ShardingJDBC的单库分表实践。
- [SpringBoot集成ShardingJDBC - 基于JPA的单库分表](springboot-x-mysql-shardingjdbc-jpa.md)
  - 上文介绍SpringBoot集成基于ShardingJDBC的读写分离实践，本文在此基础上介绍SpringBoot集成基于ShardingJDBC+JPA的单库分表实践。
- [SpringBoot集成ShardingJDBC - 基于JPA的读写分离](springboot-x-mysql-shardingjdbc-jpa-masterslave.md)
  - 本文主要介绍分表分库，以及SpringBoot集成基于ShardingJDBC的读写分离实践。
- [SpringBoot集成ShardingJDBC - 基于JPA的DB隔离多租户方案](springboot-x-mysql-shardingjdbc-jpa-tenant-db.md)
  - 本文主要介绍ShardingJDBC的分片算法和分片策略，并在此基础上通过SpringBoot集成ShardingJDBC的几种策略（标准分片策略，行表达式分片策略和hint分片策略）向你展示DB隔离的多租户方案。

### SpringBoot集成连接池(HikariCP,Druid)

> 为了提高对数据库操作的性能，引出了数据库连接池，它负责分配、管理和释放数据库连接。历史舞台上出现了C3P0，DBCP，BoneCP等均已经被淘汰，目前最为常用（也是SpringBoot2标配的）是HikariCP，与此同时国内阿里Druid（定位为基于数据库连接池的监控）也有一些市场份额。

- [SpringBoot集成连接池 - 数据库连接池和默认连接池HikariCP](springboot-x-mysql-HikariCP.md)
  - 本文主要介绍数据库连接池，以及SpringBoot集成默认的HikariCP的实践。
- [SpringBoot集成连接池 - 集成数据库Druid连接池](springboot-x-mysql-druid.md)
  - 上文介绍默认数据库连接池HikariCP，本文主要介绍SpringBoot集成阿里的Druid连接池的实践; 客观的来说，阿里Druid只能说是中文开源中功能全且广泛的连接池为基础的监控组件，但是（仅从连接池的角度）在生态，维护性，开源规范性，综合性能等方面和HikariCP比还是有很大差距。

### SpringBoot集成数据迁移(Liquibase,Flyway)

> 在实际上线的应用中，随着版本的迭代，经常会遇到需要变更数据库表和字段，必然会遇到需要对这些变更进行记录和管理，以及回滚等等；同时只有脚本化且版本可管理，才能在让数据库实现真正的DevOps（自动化执行 + 回滚等）。在这样的场景下出现了Liquibase, Flyway等数据库迁移管理工具。

- [SpringBoot数据库管理 - 用Liquibase对数据库管理和迁移](springboot-x-mysql-liquibase.md)
  - Liquibase是一个用于**用于跟踪、管理和应用数据库变化的开源工具**，通过日志文件(changelog)的形式记录数据库的变更(changeset)，然后执行日志文件中的修改，将数据库更新或回滚(rollback)到一致的状态。它的目标是提供一种数据库类型无关的解决方案，通过执行schema类型的文件来达到迁移。本文主要介绍SpringBoot与Liquibase的集成。
- [SpringBoot数据库管理 - 用flyway对数据库管理和迁移](springboot-x-mysql-flyway.md)
  - 上文介绍了Liquibase，以及和SpringBoot的集成。除了Liquibase之外，还有一个组件Flyway也是经常被使用到的类似的数据库版本管理中间件。本文主要介绍Flyway, 以及SpringBoot集成Flyway。

### SpringBoot集成PostgreSQL(JPA,MyBatis-Plus,Json)

> 在企业级应用场景下开源数据库PostgreSQL对标的是Oracle，它的市场份额稳步攀升，并且它在自定义函数，NoSQL等方面也支持，所以PostgreSQL也是需要重点掌握的。

- [SpringBoot集成PostgreSQL - 基于JPA封装基础数据操作](springboot-x-postgre-jpa.md)
  - PostgreSQL在关系型数据库的稳定性和性能方面强于MySQL，所以它在实际项目中使用和占比越来越高。对开发而言最为常见的是基于数据库的CRUD封装等，本文主要介绍SpringBoot集成PostgreSQL数据库，以及基于JPA方式的基础封装思路。
- [SpringBoot集成PostgreSQL - 基于MyBatis-Plus方式](springboot-x-postgre-mp.md)
  - 前文介绍SpringBoot+MyBatis-Plus+MySQL的集成，本文主要介绍SpringBoot+MyBatis-Plus+PostgreSQL的集成。
- [SpringBoot集成PostgreSQL - NoSQL特性JSONB及自定义函数的封装](springboot-x-postgre-jpa-jsonb.md)

### SpringBoot集成Redis(Jedis,Luttue,Redission)

> 学习完SpringBoot和SQL数据库集成后，我们开始学习NoSQL数据库的开发和集成；最重要的是分布式的缓存库Redis，它是最为常用的key-value库。主要包括早前的Jedis集成，目前常见的Luttue和Redission的封装集成；还包括基于此的Redis分布式锁的实现等。

- [SpringBoot集成Redis - 基于RedisTemplate+Jedis的数据操作](springboot-x-redis-jedis.md)
  - Redis是最常用的KV数据库，Spring 通过模板方式（RedisTemplate）提供了对Redis的数据查询和操作功能。本文主要介绍基于RedisTemplate + Jedis方式对Redis进行查询和操作的案例。
- [SpringBoot集成Redis - 基于RedisTemplate+Lettuce数据操作](springboot-x-redis-lettuce.md)
  - 在SpringBoot 2.x版本中Redis默认客户端是Lettuce，本文主要介绍SpringBoot 和默认的Lettuce的整合案例。
- [SpringBoot集成Redis - 基于RedisTemplate+Lettuce数据类封装](springboot-x-redis-lettuce-wrap.md)
  - 前两篇文章介绍了SpringBoot基于RedisTemplate的数据操作，那么如何对这些操作进行封装呢？本文主要介绍基于RedisTemplate的封装。
- [SpringBoot集成Redis - Redis分布式锁的实现](springboot-x-redis-lettuce-dist-lock.md)
  - Redis实际使用场景最为常用的还有通过Redis实现分布式锁。本文主要介绍Redis实现分布式锁。

### SpringBoot集成其它NoSQL数据库(MongoDB,ElasticSearch,Noe4J)

- [SpringBoot集成MongoDB - 基于MongoTemplate的数据操作](springboot-x-mongodb-template.md)
- [SpringBoot集成ElasticSearch - 基于ElasticSearchTemplate的数据操作](springboot-x-elastic-template.md)
- SpringBoot集成Noe4J - 集成图数据Noe4J

### SpringBoot集成Websocket(socket,netty)

> 进一步，我们看下SpringBoot集成Socket

- [SpringBoot集成Socket - 基础的Websocket实现](springboot-x-socket-websocket.md)
- [SpringBoot集成Socket - 用Netty实现socket](springboot-x-socket-netty.md)

### SpringBoot集成定时任务(springtask,quartz,elastic-job,xxl-job)

> 开发中常用的还有定时任务，我们看下SpringBoot集成定时任务, 包括Timer，ScheduleExecutorService， HashedWheelTimer， Spring tasks， quartz，elastic-job， xxl-job等。

- [SpringBoot集成定时任务 - Timer实现方式](springboot-x-task-timer.md)
  - 定时任务在实际开发中有着广泛的用途，本文主要帮助你构建定时任务的知识体系，同时展示Timer 的schedule和scheduleAtFixedRate例子；后续的文章中我们将逐一介绍其它常见的与SpringBoot的集成。
- [SpringBoot集成定时任务 - ScheduleExecutorService实现方式](springboot-x-task-executor-timer.md)
  - 上文介绍的Timer在实际开发中很少被使用， 因为Timer底层是使用一个单线程来实现多个Timer任务处理的，所有任务都是由同一个线程来调度，所有任务都是串行执行。而ScheduledExecutorService是基于线程池的，可以开启多个线程进行执行多个任务，每个任务开启一个线程； 这样任务的延迟和未处理异常就不会影响其它任务的执行了。
- [SpringBoot集成定时任务 - Netty HashedWheelTimer方式](springboot-x-task-hashwheeltimer-timer.md)
  - Timer和ScheduledExecutorService是JDK内置的定时任务方案，而业内还有一个经典的定时任务的设计叫时间轮(Timing Wheel), Netty内部基于时间轮实现了一个HashedWheelTimer来优化百万量级I/O超时的检测，它是一个高性能，低消耗的数据结构，它适合用非准实时，延迟的短平快任务，例如心跳检测。本文主要介绍时间轮(Timing Wheel)及其使用。
- [SpringBoot集成定时任务 - Spring tasks实现方式](springboot-x-task-spring-task-timer.md)
  - 前文我们介绍了Timer和ScheduledExecutorService是JDK内置的定时任务方案以及Netty内部基于时间轮实现的HashedWheelTimer；而主流的SpringBoot集成方案有两种，一种是Spring Sechedule, 另一种是Spring集成Quartz； 本文主要介绍Spring Schedule实现方式。
- [SpringBoot集成定时任务 - 基础quartz实现方式](springboot-x-task-quartz-timer.md)
  - 除了SpringTask，最为常用的Quartz，并且Spring也集成了Quartz的框架。本文主要介绍Quartz和基础的Quartz的集成案例。
- [SpringBoot集成定时任务 - 分布式quartz cluster方式](springboot-x-task-quartz-cluster-timer.md)
  - 通常我们使用quartz只是实现job单实例运行，本例将展示quartz实现基于数据库的分布式任务管理，和控制job生命周期。
- [SpringBoot集成定时任务 - 分布式elastic-job方式](springboot-x-task-elastic-job-timer.md)
  - 前文展示quartz实现基于数据库的分布式任务管理和job生命周期的控制，那在分布式场景下如何解决弹性调度、资源管控、以及作业治理等呢？针对这些功能前当当团队开发了ElasticJob，2020 年 5 月 28 日ElasticJob成为 Apache ShardingSphere 的子项目；本文介绍ElasticJob以及SpringBoot的集成。
- [SpringBoot集成定时任务 - 分布式xxl-job方式](springboot-x-task-xxl-job-timer.md)
  - 除了前文介绍的ElasticJob，xxl-job在很多中小公司有着应用（虽然其代码和设计等质量并不太高，License不够开放，有着个人主义色彩，但是其具体开箱使用的便捷性和功能相对完善性，这是中小团队采用的主要原因）；XXL-JOB是一个分布式任务调度平台，其核心设计目标是开发迅速、学习简单、轻量级、易扩展。本文介绍XXL-JOB以及SpringBoot的集成。@pdai

### SpringBoot集成视图解析(Thymeleaf,FreeMarker,Velocity,JSP,VueJS)

> SpringBoot集成视图解析，包括SpringBoot推荐的Thymeleaf，其它常用的FreeMarker, Velocity, Mustache，甚至JSP；还包括在后端视图的基础上采用主流的前端视图（比如VueJs)的兼容方案等。

- [SpringBoot集成视图 - 集成Thymeleaf视图解析](springboot-x-view-thymeleaf.md)
- SpringBoot集成视图 - 集成FreeMarker视图解析
- SpringBoot集成视图 - 集成Velocity视图解析
- SpringBoot集成视图 - 集成Mustache视图解析
- SpringBoot集成视图 - 集成JSP视图解析
- SpringBoot集成视图 - 集成后端视图+VueJS解析

### SpringBoot集成缓存(Caffeine,EhCache,CouchBase)

- SpringBoot + Spring Cache + ConcurrentMap
- SpringBoot + Spring Cache + EHCache
- SpringBoot + Spring Cache + Redis
- SpringBoot + Spring Cache + Caffeine
- SpringBoot + Spring Cache + CouchBase

### SpringBoot集成认证授权(SpringSecurity,Shiro,Oauth2,SA-Token,Keycloak)

- SpringBoot + Shiro
- SpringBoot + Spring Security
  - 常规实现
  - Oauth2
- SpringBoot + SA-Token
- SpringBoot + Keycloak
- SpringBoot + 登录验证码
  - AJ_Captcha

### SpringBoot集成文档操作(上传,PDF,Excel,Word)

> 开发中常见的文档操作，包括文件的上传和下载，上传又包含大文件的处理；针对不同的文档类型又有些常见的工具，比如POI及衍生框架用来导出Excel, iText框架用来导出PDF等。

- [SpringBoot集成文件 - 基础的文件上传和下载](springboot-x-file-upload-download.md)
  - 项目中常见的功能是需要将数据文件（比如Excel,csv)上传到服务器端进行处理，亦或是将服务器端的数据以某种文件形式（比如excel,pdf,csv,word)下载到客户端。本文主要介绍基于SpringBoot的对常规文件的上传和下载，以及常见的问题等。
- [SpringBoot集成文件 - 大文件的上传(异步，分片，断点续传和秒传)](springboot-x-file-upload-bigfile.md)
  - 上文中介绍的是常规文件的上传和下载，而超大文件的上传技术手段和普通文件上传是有差异的，主要通过基于分片的断点续传和秒传和异步上传等技术手段解决。本文主要介绍SpringBoot集成大文件上传的案例。
- [SpringBoot集成文件 - 集成POI之Excel导入导出](springboot-x-file-excel-poi.md)
  - Apache POI 是用Java编写的免费开源的跨平台的 Java API，Apache POI提供API给Java程序对Microsoft Office格式档案读和写的功能。本文主要介绍通过SpringBoot集成POI工具实现Excel的导入和导出功能。
- [SpringBoot集成文件 - 集成EasyExcel之Excel导入导出](springboot-x-file-excel-easyexcel.md)
  - EasyExcel是一个基于Java的、快速、简洁、解决大文件内存溢出的Excel处理工具。它能让你在不用考虑性能、内存的等因素的情况下，快速完成Excel的读、写等功能。它是基于POI来封装实现的，主要解决其易用性，封装性和性能问题。本文主要介绍通过SpringBoot集成EasyExcel实现Excel的导入，导出和填充模板等功能。
- [SpringBoot集成文件 - 集成EasyPOI之Excel导入导出](springboot-x-file-excel-easypoi.md)
  - 除了POI和EasyExcel，国内还有一个EasyPOI框架较为常见，适用于没有使用过POI并希望快速操作Excel的入门项目，在中大型项目中并不推荐使用(为了保证知识体系的完整性，把EasyPOI也加了进来)。本文主要介绍SpringBoot集成EasyPOI实现Excel的导入，导出和填充模板等功能。
- [SpringBoot集成文件 - 集成POI之Word导出](springboot-x-file-word-poi.md)
  - 前文我们介绍了通过Apache POI导出excel，而Apache POI包含是操作Office Open XML（OOXML）标准和微软的OLE 2复合文档格式（OLE2）的Java API。所以也是可以通过POI来导出word的。本文主要介绍通过SpringBoot集成POI工具实现Word的导出功能。
- [SpringBoot集成文件 - 集成POI-tl之基于模板的Word导出](springboot-x-file-word-poi-tl.md)
  - 前文我们介绍了通过Apache POI通过来导出word的例子；那如果是word模板方式，有没有开源库通过模板方式导出word呢？poi-tl是一个基于Apache POI的Word模板引擎，也是一个免费开源的Java类库，你可以非常方便的加入到你的项目中，并且拥有着让人喜悦的特性。本文主要介绍通过SpringBoot集成poi-tl实现模板方式的Word导出功能。
- [SpringBoot集成文件 - 集成itextpdf之导出PDF](springboot-x-file-pdf-itext.md)
  - 除了处理word, excel等文件外，最为常见的就是PDF的导出了。在java技术栈中，PDF创建和操作最为常用的itext了，但是使用itext一定要了解其版本历史和License问题，在早前版本使用的是MPL和LGPL双许可协议，在5.x以上版本中使用的是AGPLv3(这个协议意味着，只有个人用途和开源的项目才能使用itext这个库，否则是需要收费的)。本文主要介绍通过SpringBoot集成itextpdf实现PDF导出功能。
- SpringBoot + 集成PDFBox之PDF操作
- SpringBoot + 集成OpenOffice之文档在线预览
  - https://blog.csdn.net/shipfei_csdn/article/details/105141487
- SpringBoot + 集成LibreOffice之文档在线预览
- SpringBoot + 集成kkfileview之文档在线预览
  - https://kkfileview.keking.cn

### SpringBoot集成消息队列(ActiveMQ,RabbitMQ,ZeroMQ,Kafka)

- SpringBoot + ActiveMQ
- SpringBoot + RabbitMQ
- SpringBoot + ZeroMQ
- SpringBoot + Kafka

### SpringBoot集成通知(Email,短信,钉钉,微信)

- SpringBoot + 邮件
- SpringBoot + 钉钉
- SpringBoot + 微信
- SpringBoot + 短信

### SpringBoot集成文件系统(minIO,aliyun,tencentCloud,FastDFS)

- SpringBoot + MinIO
- SpringBoot + aliyun
- SpringBoot + TecentCloud
- SpringBoot + FastDFS

### SpringBoot集成工作流引擎(activi,jBPM,flowable)

- SpringBoot + activi
- SpringBoot + jBPM
- SpringBoot + flowable

### SpringBoot集成其它功能(支付,OPC-UA,JavaFX2)

> 除了上述的常见的业务上的集成功能外，还有哪些功能或者应用呢？

- [SpringBoot集成JavaFX2 - JavaFX 2.0应用](springboot-x-others-javafx2.md)
  - 很多人对Java开发native程序第一反应还停留在暗灰色单一风格的Java GUI界面，开发方式还停留在AWT或者Swing。本文主要基于SpringBoot和JavaFX开发一个Demo给你展示Java Native应用可以做到什么样的程度。当然JavaFX 2.0没有流行起来也是有原因的，而且目前native的选择很多，前端是个框架都会搞个native...
- SpringBoot + 支付
- SpringBoot + OPC-UA
- ...

### SpringBoot应用部署(jar,war,linux,docker,docker-compose)

> 那么如何将SpringBoot应用打包并部署呢？打包主要有jar，war两种方式；部署包含在linux或者windows上制作成服务，以及制作成docker进行部署；此外也可以结合CI/CD 环境进行部署。

- [SpringBoot应用部署 - 打包成jar部署](springboot-x-deploy-jar.md)
  - 我们知道spring-boot-starter-web默认已经集成了web容器（tomcat)，在部署前只需要将项目打包成jar即可。那么怎么将springboot web项目打包成jar呢？本文主要介绍常见的几种方式。
- [SpringBoot应用部署 - 使用第三方JAR包](springboot-x-deploy-jar-3rd.md)
  - 在项目中我们经常需要使用第三方的Jar，比如某些SDK，这些SDK没有直接发布到公开的maven仓库中，这种情况下如何使用这些三方JAR呢？本文提供最常用的两种方式。
- [SpringBoot应用部署 - 打包成war部署](springboot-x-deploy-war.md)
  - 前文我们知道SpringBoot web项目默认打包成jar部署是非常方便的，那什么样的场景下还会打包成war呢？本文主要介绍SpringBoot应用打包成war包的示例。
- [SpringBoot应用部署 - 替换tomcat为Jetty容器](springboot-x-container-jetty.md)
  - 前文我们知道spring-boot-starter-web默认集成tomcat servlet容器(被使用广泛）；而Jetty也是servlet容器，它具有易用性，轻量级，可拓展性等，有些场景（Jetty更满足公有云的分布式环境的需求，而Tomcat更符合企业级环境）下会使用jetty容器。本文主要介绍SpringBoot使用Jetty容器。
- [SpringBoot应用部署 - 替换tomcat为Undertow容器](springboot-x-container-undertow.md)
  - 前文我们了解到Jetty更满足公有云的分布式环境的需求，而Tomcat更符合企业级环境；那么从性能的角度来看，更为优秀的servlet容器是Undertow。本文将介绍Undertow，以及SpringBoot集成Undertow的示例。
- [SpringBoot应用部署 - 在linux环境将jar制作成service](springboot-x-jar-service-linux.md)
  - 前文我们将SpringBoot应用打包成jar，那么如何将jar封装成service呢？本文主要介绍将SpringBoot应用部署成linux的service。
- [SpringBoot应用部署 - 在windows环境将jar制作成service](springboot-x-jar-service-windows.md)
  - 前文我们将SpringBoot应用打包成jar并在Linux上封装成service，那么在Windows环境下如何封装呢？本文主要介绍将SpringBoot应用部署成Windows的service。
- [SpringBoot应用部署 - docker镜像打包,运行和管理](springboot-x-deploy-docker.md)
  - 随着软虚拟化docker的流行，基于docker的devops技术栈也开始流行。本文主要介绍通过docker-maven-plugin将springboot应用打包成docker镜像，通过Docker桌面化管理工具或者Idea Docker插件进行管理。
- [SpringBoot应用部署 - 使用Docker Compose对容器编排管理](springboot-x-deploy-docker-compose.md)
  - 如果docker容器是相互依赖的（比如SpringBoot容器依赖另外一个MySQL的数据库容器），那就需要对容器进行编排。本文主要介绍基于Docker Compose的简单容器化编排SpringBoot应用。

### SpringBoot集成监控(actuator,springboot-admin,ELK,Grafana,APM)

> SpringBoot集成监控，包括SpringBoot自带的actuator，基于actuator的可视化工具springboot admin。监控的日志体系技术栈ELK，监控状态和指标收集prometheus+Grafana，基于Agent的APM性能监控等。

- [SpringBoot集成监控 - 集成actuator监控工具](springboot-x-monitor-actuator.md)
  - 当SpringBoot的应用部署到生产环境中后，如何监控和管理呢？比如审计日志，监控状态，指标收集等。为了解决这个问题，SpringBoot提供了Actuator。本文主要介绍Spring Boot Actuator及实现案例。
- [SpringBoot集成监控 - 集成springboot admin监控工具](springboot-x-monitor-boot-admin.md)
  - 上文中展示了SpringBoot提供了Actuator对应用进行监控和管理， 而Spring Boot Admin能够将 Actuator 中的信息进行界面化的展示，也可以监控所有 Spring Boot 应用的健康状况，提供实时警报功能。 本文主要介绍springboot admin以及SpringBoot和springboot admin的集成。
- SpringBoot集成监控 - 日志收集(ELK)
- SpringBoot集成监控 - 状态监控(Prometheus+Grafana)
- SpringBoot集成监控 - 性能监控(APM Agent)

### SpringBoot进阶(starter,自动装配原理,各类机制等)

> SpringBoot进阶

- [SpringBoot进阶 - 实现自动装配原理](springboot-y-auo-config.md)
- [SpringBoot进阶 - 自定义starter](springboot-y-starter.md)
  - 如何将自己的模块封装成starter， 并给其它springBoot项目使用呢？ 本文主要介绍在Springboot封装一个自定义的Starter的一个Demo，从创建一个模块->封装starter->使用
- [SpringBoot进阶 - 嵌入web容器Tomcat原理](springboot-y-wrap-tomcat.md)
- [SpringBoot进阶 - 健康检查Actuator原理](springboot-y-th-actuator.md)