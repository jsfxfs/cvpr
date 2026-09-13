# 网站更新计划

> 网站更新计划 @pdai

## 技术团队

- 美团技术团队
- 滴滴技术
- 网易云音乐技术团队
- 网易传媒技术团队
- 达达集团技术
- 京东技术
- 哈啰技术
- 顺丰技术
- 阿里开发者
- 阿里妈妈技术
- 360技术工程
- 携程技术
- 蘑菇街技术
- 腾讯技术工程
- 哔哩哔哩技术

## Java基础

- 锁
  - 不可不说的Java“锁”事 https://tech.meituan.com/2018/11/15/java-lock.html
- 线程池
  - CompletableFuture原理与实践-外卖商家端API的异步化 https://tech.meituan.com/2022/05/12/principles-and-practices-of-completablefuture.html
  - Java线程池实现原理及其在美团业务中的实践 https://tech.meituan.com/2020/04/02/java-pooling-pratice-in-meituan.html
- JVM
  - 字节码增强技术探索 https://tech.meituan.com/2019/09/05/java-bytecode-enhancement.html
  - [-] Java动态追踪技术探究 https://tech.meituan.com/2019/02/28/java-dynamic-trace.html
- GC
  - 从实际案例聊聊Java应用的GC优化 https://tech.meituan.com/2017/12/29/jvm-optimize.html

### Java特性

- 更新：JDK部分脑图插入具体文章
- 新增：JDK 12特性和脑图
- 新增：JDK 16特性和脑图
  - https://www.jianshu.com/p/0504d48d1a50
  - https://blog.csdn.net/weixin_48967543/article/details/115263346
  - https://blog.csdn.net/qf2019/article/details/114962794
- 新增：JDK 17特性和脑图
  - https://www.oracle.com/news/announcement/oracle-releases-java-17-2021-09-14/
  - https://developer.huawei.com/consumer/cn/forum/topic/0201671904835110263
- 新增：JDK 18特性和脑图
- 新增：JDK8升级到JDK11的特性理解
- 新增：JDK11升级到JDK17的特性理解
- 补充：JDK整体知识体系补充完善
- 资料参考
  - https://openjdk.java.net/jeps/0

### Java并发

- 新增：并发的本质：协作，分工和互斥
- 新增：并发的模式梳理

### JVM调试等

- 新增：ZGC 垃圾回收详解
  - https://zhuanlan.zhihu.com/p/337204437
  - https://segmentfault.com/a/1190000023568163
  - https://www.jianshu.com/p/664e4da05b2c
- 新增：堆外内存分析
  - https://tech.meituan.com/2019/01/03/spring-boot-native-memory-leak.html
- 新增：高CPU高内存分析
  - https://www.cnblogs.com/AloneSword/p/3821569.html
- 新增：使用MAT进行内存分析
  - https://blog.csdn.net/canot/article/details/78079085
  - https://www.yourkit.com/docs/java/help/gc_roots.jsp
  - https://www.yourkit.com/docs/java/help/sizes.jsp
- 新增：高IO分析
  - https://www.cnblogs.com/xiaoyaojinzhazhadehangcheng/p/7911747.html
- 完善 - GC基础
  - https://www.cnblogs.com/yescode/p/13934840.html
- 补充 - 垃圾回收18问整理
  - https://www.cnblogs.com/yescode/p/13961190.html
- 补充 - JVM参数配置补充
  - https://www.jianshu.com/p/664e4da05b2c

## 数据结构和算法

- 补充完善
  - 新增：计数排序算法, 桶排序和计数排序区分
  - 更新：调整排序算法整个文章顺序
- 因果推断
  - [哈啰：董彦燊：因果推断在哈啰出行的实践探索](https://mp.weixin.qq.com/s/ZvdrOmy9-smky682bTspTA)
- 司乘匹配
  - https://mp.weixin.qq.com/s/gD7vOGVlsG5JcpfjaagifQ
- 算法测试
  - https://mp.weixin.qq.com/s/i6l89p3fVRNJ848dcohrgQ
- 算法平台
  - [算法在哈啰顺风车中的实践应用](https://mp.weixin.qq.com/s/HPKzTZ0nQ8WUM4Yhb0VFaQ)
  - [算法平台在线服务体系的演进与实践](https://mp.weixin.qq.com/s?__biz=MjM5NjQ5MTI5OA==&mid=2651762169&idx=1&sn=4f28a8fac47ab2b28265dca489cff695&chksm=bd1274b48a65fda25011247807430d7451b9a3461956a4b8eade2db183a873d4b4fbe535ce99&cur_album_id=1573133921079361536&scene=189#wechat_redirect)
- 治理算法
  - [滴滴治理算法探索与实践](https://mp.weixin.qq.com/s/Kn0NToHvCPvIBvSIIN18cQ)

## 中间件

### Tomcat

- 新增：Tomcat知识体系列表

### MyBatis

- [从零开始实现一个MyBatis加解密插件](https://mp.weixin.qq.com/s/WUEAdFDwZsZ4EKO8ix0ijg)
- [MyBatis版本升级引发的线上告警回顾及原理分析](https://tech.meituan.com/2020/06/18/inf-bom-mybatis.html)

### MyBatis-Plus

- [Mybatis-Plus的应用场景及注入SQL原理分析](https://mp.weixin.qq.com/s/Fm8YsIlUfsar7zscrOYEdg)

### Quartz

- Quartz应用与集群原理分析 https://tech.meituan.com/2014/08/31/mt-crm-quartz.html

### 规则引擎Drools

- [规则引擎Drools在贷后催收业务中的应用](https://mp.weixin.qq.com/s/32O2KwQxlQodac0IpYClLQ)
- [美团酒旅实时数据规则引擎应用实践](https://mp.weixin.qq.com/s/UYN4cxH4gT0WsFTrBKRKGA)
- [从0到1：构建强大且易用的规则引擎](https://mp.weixin.qq.com/s/E-9GR0Mun1pudC0V1nXCsg)

### 规则引擎Esper

### 表达式引擎Aviator

### 工作流引擎

### 数据库连接池

### kafka

- [vivo: Kafka 原理和实践](https://mp.weixin.qq.com/s/bV8AhqAjQp4a_iXRfobkCQ)
- [vivo: Kafka 万亿级消息实践之资源组流量掉零故障排查分析](https://mp.weixin.qq.com/s/uNq0RSOsTBWxpMYNpsm9gg)
- [vivo: Kafka 原理以及分区分配策略剖析](https://mp.weixin.qq.com/s/upMG8xUAXbN6R4EgqrHhTw)
- [vivo: Kafka 负载均衡在 vivo 的落地实践](https://mp.weixin.qq.com/s/Zio9V_XXUTNZ3-TDHCt6LQ)
- [Kafka在美团数据平台的实践](https://tech.meituan.com/2022/08/04/the-practice-of-kafka-in-the-meituan-data-platform.html)
- [基于SSD的Kafka应用层缓存架构设计与实现](https://tech.meituan.com/2021/01/14/kafka-ssd.html)

### RabbitMQ

## 数据库

从Hadoop生态的Hive, Spark, Presto, Kylin, Druid到非Hadoop生态的ClickHouse, Elasticsearch，不一而足...

### SQL

- SQL解析在美团的应用 https://tech.meituan.com/2018/05/20/sql-parser-used-in-mtdp.html
- 美团点评SQL优化工具SQLAdvisor开源 https://tech.meituan.com/2017/03/09/sqladvisor-pr.html

### MySQL

- MySQL索引原理及慢查询优化 https://tech.meituan.com/2014/06/30/mysql-index.html
- 美团MySQL数据库巡检系统的设计与应用 https://tech.meituan.com/2020/06/04/mysql-detection-system.html
- [-] Innodb中的事务隔离级别和锁的关系 https://tech.meituan.com/2014/08/20/innodb-lock.html
- 基于代价的慢查询优化建议 https://tech.meituan.com/2022/04/21/slow-query-optimized-advice-driven-by-cost-model.html

### Redis

- Redis知识体系详解
- Redis基础 - Redis安装
- Redis进阶 - Redis内存消耗和回收机制
- Redis进阶 - 分布式：分片技术
- Redis进阶 - 更多Redis相关

  - Redis 6.0 多线程发布之后面试题如何回答？
    - https://zhuanlan.zhihu.com/p/344007443
- [美团针对Redis Rehash机制的探索和实践](https://tech.meituan.com/2018/07/27/redis-rehash-practice-optimization.html)
- [Redis 高负载下的中断优化](https://tech.meituan.com/2018/03/16/redis-high-concurrency-optimization.html)
- [redis之bigkey（看这一篇就够）](https://www.cnblogs.com/szq95716/p/14271108.html)
- [vivo: Redis高效压缩位图在推荐系统中的应用](https://mp.weixin.qq.com/s/zLLvyb4pPUXa436vGPrnsA)

### ElasticSearch

- [哈啰：记录一次ElasticSearch的查询性能优化](https://mp.weixin.qq.com/s?__biz=MzI3OTE3ODk4MQ==&mid=2247486047&idx=1&sn=b3ab21da891df124c03e628eb3851b4c&chksm=eb4af1d5dc3d78c3be8995c0e16674f47598f907185dac03919f0c4d0a26ea4a71a0543390bf&scene=132#wechat_redirect)
- [记一次Elasticsearch问题排查](https://mp.weixin.qq.com/s/smV6EVo3WD6H1RoX09PyQA)
- [从一个生产的问题分析ElasticSearch负载均衡算法](https://mp.weixin.qq.com/s?__biz=MzI3OTE3ODk4MQ==&mid=2247486599&idx=1&sn=873b34d82dc7d20bde6aa61170987af8&chksm=eb4af70ddc3d7e1ba1b082eee6858931e3f9f2580c4ce169e65c517157f00d7335091cc8396c&scene=178&cur_album_id=2474410650073776130#rd)
- [分布式搜索引擎Elasticsearch的架构分析](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247488533&idx=4&sn=0b6689af6b8ce8ef5a15e38f0a7ffc03&chksm=ebd86487dcafed9142b8085624746e368eeea0da21dee920a17f3c03aab17eea00d2c5b9afcc&scene=178&cur_album_id=1500549131247910916#rd)
- [Elasticsearch 在地理信息空间索引的探索和演进](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247493879&idx=1&sn=9b7ba7da6f6c3f9c9a66043b529e2f1e&chksm=ebdb9865dcac11734585ca8b5c07fcd7d7afacc8f40f046c4239763717f6b80530f05745653b&scene=178&cur_album_id=1500549131247910916#rd)

### OpenTSDB

- [OpenTSDB 数据存储详解](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247487289&idx=1&sn=72dd26e52e7547e4eda770e90fff82de&chksm=ebd87fabdcaff6bd19454cc261a10cdf0a84c6c51ac636507efd5fec66feb51195fe39f90146&scene=178&cur_album_id=1500549131247910916#rd)

### Druid

- [理“ Druid 元数据”之乱](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247493768&idx=1&sn=e8f6619d8b4a26ccc328629b6097587d&chksm=ebdb981adcac110c7993446ec899c4df5f85f850227d8c413f968401b564a66d88e794cf2c4f&scene=178&cur_album_id=1500549131247910916#rd)

### Nebula Graph

- [vivo 大规模特征存储实践](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247486646&idx=1&sn=fd16e939839ba8ec0f5d5e3f31d8db48&chksm=ebd87c24dcaff532ec5fbb8650bc9d04fda1e778473296a6361142b6e0682c6e690bbe02f25e&scene=178&cur_album_id=1500549131247910916#rd)

### HDFS

- [vivo 万台规模 HDFS 集群升级 HDFS 3.x 实践](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247493631&idx=1&sn=050f57bfdc1e5ea5759567b7444f2d8f&chksm=ebdb976ddcac1e7b21e0139eac67ea43a92421a93515e86af7a68eec75a34c63088da360ab49&scene=178&cur_album_id=1500549131247910916#rd)

### Presto

- [探究Presto SQL引擎(1)-巧用Antlr](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247491631&idx=2&sn=d70dd5119f456986a9a7939914cc0f98&chksm=ebdb90bddcac19ab0523b46f6b82361eda6858063d42b4ada781bd449a08c9fba6b92c78d23e&scene=178&cur_album_id=1500549131247910916#rd)

### Spark

- [Spark Executor内存管理](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247486613&idx=1&sn=36ef309ae2f25431573895ae24480e2d&chksm=ebd87c07dcaff511031fed148181909be5b75bc33b535c72511e4a994e02b5563df11a2eda1f&scene=178&cur_album_id=1500549131247910916#rd)
- [Spark SQL 字段血缘在 vivo 互联网的实践](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247493545&idx=1&sn=83d59507c2bd8feb2c61f3136c693199&chksm=ebdb973bdcac1e2d42a772e796e57ab3f6b3522b41a3de3783774d92ff1686e4181028b36a85&scene=178&cur_album_id=1500549131247910916#rd)
- [Spark 数据倾斜及其解决方案](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247486291&idx=1&sn=36003888a4b5859ed324479434309cdb&chksm=ebd87bc1dcaff2d7d4f664bd5d5eca011e1d2a6b0623daf3089469b1b0691b399414c221c647&scene=178&cur_album_id=1500549131247910916#rd)
- [SparkSql连接查询中的谓词下推处理(一)](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247484202&idx=2&sn=daee88ceb5482c68c596c98807e477fa&chksm=ebd873b8dcaffaae37f1fcdbb6f1053683b23ad35199fa6b9186e0e65a38b3735437e205debd&scene=178&cur_album_id=1500549131247910916#rd)
- [SparkSQL连接查询中的谓词下推处理(二)](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247484240&idx=1&sn=a423b43767499d82853be8653f393fa4&chksm=ebd873c2dcaffad450cb9d7ebf56559f043be38f35dc0f314b28be45bdbfac88d6bb5f7cc90d&scene=178&cur_album_id=1500549131247910916#rd)

### clickhouse

- [基于ClickHouse的用户行为分析系统](https://mp.weixin.qq.com/s/lrgSGhsAUGR7aD16KQYT5A)

### Doris

## Spring

### Spring系列文章

- Spring MVC注解故障追踪记 https://tech.meituan.com/2016/09/30/mt-trip-springmvc-service-annotation-problem-research.html

### Springboot系列文章

- [SpringBoot集成MongoDB - 基于MongoTemplate的数据操作](spring/springboot/springboot-x-mongodb-template.md)
- [SpringBoot集成ElasticSearch - 基于ElasticSearchTemplate的数据操作](spring/springboot/springboot-x-elastic-template.md)
- [SpringBoot集成Socket - 基础的Websocket实现](spring/springboot/springboot-x-socket-websocket.md)
- [SpringBoot集成Socket - 用Netty实现socket](spring/springboot/springboot-x-socket-netty.md)
- [SpringBoot定时任务 - Netty HashedWheelTimer方式](spring/springboot/springboot-x-task-hashwheeltimer-timer.md)
- [SpringBoot定时任务 - 分布式elastic-job方式](spring/springboot/springboot-x-task-elastic-job-timer.md)
- [SpringBoot定时任务 - 分布式xxl-job方式](spring/springboot/springboot-x-task-xxl-job-timer.md)
- [SpringBoot后端视图 - 基于Thymeleaf视图解析](spring/springboot/springboot-x-view-thymeleaf.md)
- [SpringBoot进阶 - 实现自动装配原理](spring/springboot/springboot-y-auo-config.md)
- [SpringBoot进阶 - 嵌入web容器Tomcat原理](spring/springboot/springboot-y-wrap-tomcat.md)
- [SpringBoot进阶 - 健康检查Actuator原理](spring/springboot/springboot-y-th-actuator.md)

> 待加入体系

- [Springboot集成sentinel实现接口限流入门](https://blog.csdn.net/tianyaleixiaowu/article/details/89916891)
- SpringBoot集成文件系统
  - SpringBoot + MinIO
  - SpringBoot + aliyun
  - SpringBoot + TecentCloud
  - SpringBoot + FastDFS
- SpringBoot集成认证授权
  - SpringBoot + Shiro
  - SpringBoot + Spring Security
    - 常规实现
    - Oauth2
  - SpringBoot + SA-Token
  - SpringBoot + Keycloak
  - SpringBoot + 登录验证码
    - AJ_Captcha
- SpringBoot集成接口（拓展）
  - SmartDoc
  - magic-api
    - https://juejin.cn/post/6968632716434604068
  - 接口设计和交互工具
    - APIFox
    - PostMan
    - Apizza
- SpringBoot集成数据库连接池
  - HikariCP
  - Druid
- SpringBoot集成缓存
  - Spring Cache
  - EHCache
- SpringBoot集成后端视图
  - Thymeleaf
  - FreeMarker
  - Velocity
  - Mustache
  - JSP
- SpringBoot集成消息队列
  - ActiveMQ
  - RabbitMQ
  - ZeroMQ
  - Kafka
- SpringBoot集成日志
  - SpringBoot+ELK
    - https://juejin.cn/post/6844904196672585741
- SpringBoot集成文档
  - 文件上传
    - 文件上传进度条
  - Excel导入导出 - POI
  - Excel导入导出 - EasyExcel
  - PDF导出 - Itext
  - Word导出
- SpringBoot集成通知
  - 邮件
  - 钉钉
  - 微信
  - 短信
- SpringBoot应用安全
  - SpringBoot 配置文件密码
    - https://www.cnblogs.com/kexianting/p/11689289.html
    - https://www.cnblogs.com/ruhuanxingyun/p/12152579.html
  - Druid 密码配置
- SpringBoot集成其它
  - 支付
  - OPC-UA milo
- SpringBoot Intergration
  - https://spring.io/projects/spring-integration
- Spring 系列
  - Spring 事务源码
  - Spring JDBC源码
  - Spring Security源码
    - https://www.javadevjournal.com/spring-security/spring-security-authentication-providers/
- Spring Framework基础
  - Spring 基于注解的配置
    - 从Spring v2-4 中发展而言，Spring 构筑了它的生态体系，以及围绕Java5注解和反射在框架级别的衍生； 在这个阶段，它的趋势是：组件化+反射+注解方式配置编程。
  - Spring 5 中特性
    - 从Spring v5 中的特性来看未来一段时间开发框架的发展趋势： 函数式+异步+响应式编程。

https://mp.weixin.qq.com/s?__biz=MzU5MDgzOTYzMw==&mid=2247484640&idx=1&sn=41b813b09eb228343f7ac6c22dcc0f94&chksm=fe396edec94ee7c8485e6619ad18ed40c3645ccb7a1457aa81bfe8ac3e2cccc617b68b9f4fc5&scene=178&cur_album_id=1344425436323037184#rd

### Spring Native

### Spring Cloud

## 架构

### 完善架构章节

- 补充 - 架构之高可用：容灾备份,故障转移
- 补充 - 分布式系统 - 知识体系
- 完善 - 分布式系统 - 理论基础及一致性算法
- 补充 - 分布式系统 - 分布式锁及实现方案
- 完善 - 分布式系统 - 分布式事务及实现方案
- 补充 - 分布式系统 - 分布式任务及实现方案
- 补充 - 分布式系统 - 分布式服务链路追踪
- 补充 - 分布式系统 - 分布式文件系统
- 补充 - 分布式系统 - 分布式存储系统

### 架构设计之商业业务平台

- 【秒杀抽奖】系统
  - [【秒杀抽奖】秒杀系统设计](arch/arch-example-seckill.md)
  - [从限流削峰到性能优化，谈1号店的抽奖系统架构实践](https://mp.weixin.qq.com/s?__biz=MzI4MTY5NTk4Ng==&mid=2247489518&idx=1&sn=79e0296ed22538eabc0b94a6465a3af0&source=41#wechat_redirect)
- 【电商交易】系统
  - [【电商交易】京东-亿级商品详情页设计](arch/arch-example-goods-detail.md)
  - [【电商交易】闲鱼-亿级商品结构化背后的思考和演进](arch/arch-example-xianyu-goods.md)
  - [【电商交易】闲鱼-多状态多操作的交易链路架构演进](arch/arch-example-xianyu-jiaoyi.md)
  - [【电商交易】蘑菇街-电商交易平台服务架构及改造优化历程](https://mp.weixin.qq.com/s/wQH7Zz6o88pj-v1E2rGJEw?)
- 【仓储物流】系统
  - [【仓储物流】菜鸟-揭秘菜鸟全球智能仓配技术实践](https://mp.weixin.qq.com/s/igH0UwkvP9WiVTkFX-IrLA)
  - [【仓储物流】美团-配送系统架构演进实践](arch/arch-example-meituan-peisong.md)
  - [【仓储物流】美团-即时物流的分布式系统架构设计](arch/arch-example-meituan-jishiwuliu.md)
- 【拉新投放】系统
  - [【拉新投放】闲鱼-拉新投放系统如何设计](arch/arch-example-xianyu-laxintoufang.md)
- 【综合/其它】
  - [【综合/其它】闲鱼-复杂搜索系统的可靠性优化之路](arch/arch-example-xianyu-search.md)
  - [【综合/其它】美团-外卖客户端高可用建设体系](arch/arch-example-meituan-waimai.md)

### 架构设计之数据仓库平台

- 数据仓库
  - [美团: 数据库高可用架构的演进与设想](arch/arch-example-meituan-db-hp.md)
  - [美团: 数据同步到仓库的架构实践](arch/arch-example-meituan-db-binlog.md)
  - [美团: 美团外卖实时数仓建设实践](https://tech.meituan.com/2021/08/26/data-warehouse-in-meituan-waimai.html)
  - [携程: 携程机票数据仓库建设之路](https://mp.weixin.qq.com/s/CfxNcMJIl6irunrTNTs25g)
- 数据治理
  - [美团: 业务数据治理体系化思考与实践](https://tech.meituan.com/2022/05/12/business-data-governance.html)
  - [美团: 数据库异常智能分析与诊断](https://tech.meituan.com/2022/05/05/meituan-database-autonomy-service.html)
  - [美团: 数据治理一体化实践之体系化建模](https://tech.meituan.com/2022/02/24/systematic-modeling-of-data-development-and-governance-integration-practice.html)
  - [携程: 平台化常态化数据治理之路](https://mp.weixin.qq.com/s/B9T_hNBfm8nl85BYvmhftA)
  - [实时数据产品实践——美团大交通战场沙盘](https://tech.meituan.com/2018/05/24/traffic-realtime-data-product-practice.html)
- 数据质量
  - [哈啰: 数据质量监控&接口语义监控实践分享](https://mp.weixin.qq.com/s/Bq9pLgrj7YHnezODTTrOHQ)

### 架构设计之日志系统平台

- [vivo大数据日志采集Agent设计实践](http://blog.itpub.net/69912579/viewspace-2924905/)
- [美团高性能终端实时日志系统建设实践](https://tech.meituan.com/2022/11/03/logan-real-time-log.html)
- [可视化全链路日志追踪](https://tech.meituan.com/2022/07/21/visualized-log-tracing.html)
- [日志导致线程Block的这些坑，你不得不防](https://tech.meituan.com/2022/07/29/tips-for-avoiding-log-blocking-threads.html)
- [京东APP秒级百G日志传输存储架构设计与实战](https://mp.weixin.qq.com/s/IEK4WeFmiz9TzZWIJ40Whg)
- [-] [你真的会打Log吗？](https://mp.weixin.qq.com/s/XJMAEixyJ8DQJDmjIKoUKA)
- [-] [京东流式计算日志系统应用实践](https://mp.weixin.qq.com/s/ex_1j4DYjpJD57-UrglY6w)
- [如何优雅地记录操作日志？](https://mp.weixin.qq.com/s/JC51S_bI02npm4CE5NEEow)
- [日均TB级数据，携程支付统一日志框架](https://mp.weixin.qq.com/s/GWRGcIwuKGiZC1ZOb2Z2JQ)
- [企业微信万亿级日志检索系统](https://mp.weixin.qq.com/s/opxvlddsSQctb3nwcxaW_g)

### 架构设计之大屏设计

- [从0到1设计通用数据大屏搭建平台](http://blog.itpub.net/69912579/viewspace-2918077/)
- [数据可视化大屏产品在滴滴的技术探索](https://mp.weixin.qq.com/s/eWifSqOvhHCqVul1tKDSlw)

### 架构设计之安全平台

- [攻击面分析及应对实践](https://blog.csdn.net/vivo_tech/article/details/127087086)

### 架构设计之监控平台

- [vivo: 服务端监控架构设计与实践](https://mp.weixin.qq.com/s/P4GWV1u7jrn6eog1zEH56w)

### 架构设计之推荐系统

- [vivo: 推荐系统-协同过滤在Spark中的实现](https://mp.weixin.qq.com/s/PQol3h0KmqmElYRJ1Pu2Mw)
- [vivo: 应用商店推荐系统探索与实践](https://mp.weixin.qq.com/s/PfOg3jrQOEi_DJNR6ehquQ)
- [哈啰: 搜索推荐一体化建设](https://mp.weixin.qq.com/s/fSSykywinHOIeDVUIk2UfA)
- [哈啰: 推荐引擎搭建实战](https://mp.weixin.qq.com/s/MGP2UkZZg0nrDJNLEZGtmw)
- [美团: 综合业务推荐系统的质量模型及实践](https://mp.weixin.qq.com/s/SCFzFIshY9a2wdsPnfffVA)

### 架构设计之网关设计

- [美团: 百亿规模API网关服务Shepherd的设计与实现](https://tech.meituan.com/2021/05/20/shepherd-api-gateway.html)
- [携程: 高吞吐消息网关的探索与思考](https://mp.weixin.qq.com/s/EIa4a3VPX9Onj1bt24hWjA)
- [vivo: 微服务 API 网关架构实践](https://mp.weixin.qq.com/s/5U1rgpcW21LDYzv8K9EX7g)

### 其它系统设计

- 用户行为分析模型
  - [用户行为分析模型实践（一）—— 路径分析模型](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247490504&idx=1&sn=9827b136fa5cfc81467cb1b795f7bc41&chksm=ebd86b5adcafe24c450237a7ef2ac09c0efb5c8212cb6755e1703d46329dc321f17d32d9617d&scene=21#wechat_redirect)
  - [用户行为分析模型实践（二）—— 漏斗分析模型](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247493594&idx=2&sn=73a7695bfd664a617adc35c88ccd9637&chksm=ebdb9748dcac1e5e1ea9ecc9aa47cbcd7d78735a5b489b2a4f8878fc79fc1d28b038036693df&scene=178&cur_album_id=1500549131247910916#rd)

### 架构设计之云平台

- 可编程网络
  - [可编程网络系列(一)：可编程网络在阿里云的规模化应用和实践](https://mp.weixin.qq.com/s/PuB8IA51p5MU59V1njTeaw)
  - [可编程网络系列(二)：软硬结合看阿里云自研新一代SNA场景化应用](https://mp.weixin.qq.com/s/NKQO5Vy1yrcjQ-7KQJMHqA)
  - [可编程网络系列(三)：可编程网络 “阿里云自研编译器”全解析](https://mp.weixin.qq.com/s/QPuoFP3flHsSKN8oNciIdQ)
  - [云栖进行时｜分享：可编程网络的现在与未来](https://mp.weixin.qq.com/s/jSjNjsBTnE9BVItKPpNqIg)
- DNS管控平台
  - [阿里云DNS管控平台：新一代DNS解析管理及分发系统](https://mp.weixin.qq.com/s/rNcvWCOQqnOuGl5NJqfrtg)
  - [阿里云DNS统一运维服务的演进和实践](https://mp.weixin.qq.com/s/UjsO7WLT2Z_yZFkv4vH7-w)
- AIOPS
  - [看不见的“网” 一文读懂阿里云基础设施网络](https://mp.weixin.qq.com/s/tFS_xgBDOVRgNbCbFBrtgg)

### 架构设计之基础综合平台

- 研发平台化
  - 美团弹性伸缩系统的技术演进与落地实践 https://tech.meituan.com/2021/04/01/hulk-kubernetes-docker-octo.html
- 中台建设
  - [哈啰：行程平台中台化建设](https://mp.weixin.qq.com/s/vvvDi-KVbNzX8XlXcrzskg)
- 异地多活
  - [解密阿里巴巴高可用架构技术——“异地多活”](https://mp.weixin.qq.com/s/Osggn2PFSySsrqCyW2Dtmw?)
  - [哈啰：异地双活在哈啰四轮出行的落地](https://mp.weixin.qq.com/s?__biz=MzI3OTE3ODk4MQ==&mid=2247486061&idx=1&sn=af816da94ff7b4c44d418436e37da87d&chksm=eb4af1e7dc3d78f16dda9015039d6fba76ce58aaab527f48712b046b91ffe2ae81d01e20d52b&scene=21#wechat_redirect)
  - [哈啰：异地双活在哈啰四轮出行的落地- redis](https://mp.weixin.qq.com/s?__biz=MzI3OTE3ODk4MQ==&mid=2247486077&idx=1&sn=0e3160a7bbd8c9e9bb37fa11e744876a&chksm=eb4af1f7dc3d78e10d08a505fd2d695c9deaed04c8e4a98d69103da5e6e3dbc89fe90adc1534&scene=132#wechat_redirect)

### 低代码平台

- [网易云音乐低代码体系建设思考与实践](https://mp.weixin.qq.com/s/9yo-Au3wwsWErBJfFjhxUg)

## DevOPS部分

- CICD

  - CD
    - Jenkins的Pipeline脚本在美团餐饮SaaS中的实践 https://tech.meituan.com/2018/08/02/erp-cd-jenkins-pipeline.html
    - 美团外卖持续交付的前世今生 https://tech.meituan.com/2020/02/13/meituan-waimai-continuous-delivery.html
  - 版本分支管理
    - 客户端单周发版下的多分支自动化管理与实践https://tech.meituan.com/2019/01/10/traffic-git-branch-management.html
- 稳定性建设

  - https://mp.weixin.qq.com/s/iUW_w3j6SZzarMSR0s8b2w
  - https://mp.weixin.qq.com/s/VwSuYx7SXnIOxDQ2Lm84hg
  - https://mp.weixin.qq.com/s/tQMZ-X0p7N997TCoqGHdgg
  - https://mp.weixin.qq.com/s/h4_yWNonjrpho2TODjlRgw
- 测试

  - 压力测试
    - [从0到1构建美团压测工具](https://tech.meituan.com/2016/01/08/loading-test.html)
    - [如何做一次完美的 ABTest？](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247487163&idx=2&sn=aea33b5bcb36f9ff481edbc8ff84a9c1&chksm=ebd87e29dcaff73f5f65e413ff26141b9d5d970055af421341a999ca175a761024a5f14184f8&scene=178&cur_album_id=1500549131247910916#rd)
    - [全链路压测在网易传媒的落地与实践](https://mp.weixin.qq.com/s/5uY50nJoBsFYetO7jhQ16w)
  - 自动化测试
    - [携程安全自动化测试之路](https://mp.weixin.qq.com/s/OtqJ-14vEPEcLmf4Ctk7vQ)
- 云原生

  - 容器化
    - [美团: Docker系列之二：基于容器的自动构建](https://tech.meituan.com//page/24.html)
    - [美团: 美团外卖前端容器化演进实践](https://tech.meituan.com/2019/11/28/meituan-front-end-containerization-evolution.html)
    - [美团: 美团点评Docker容器管理平台](https://tech.meituan.com/2017/01/23/mt-docker-practice.html)
    - [vivo: 容器集群监控系统架构与实践](https://mp.weixin.qq.com/s/SBZO48fWcEojlDlBROdogQ)
  - k8s
    - https://tech.meituan.com/2019/08/22/kubernetes-cluster-management-practice.html
    - 云原生
      - [美团: 云原生之容器安全实践](https://tech.meituan.com/2020/03/12/cloud-native-security.html)
      - [美团: 集群调度系统的云原生实践](https://tech.meituan.com/2022/02/17/kubernetes-cloudnative-practices.html)
- 版本灰度

  - [从0到1建设智能灰度数据体系：以vivo游戏中心为例](https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247493933&idx=1&sn=17111739f770ba0439c282ac34da22e4&chksm=ebdb99bfdcac10a9670102d080b57f7144136991297a9865915b06433262182452ead2283957&scene=178&cur_album_id=1500549131247910916#rd)
- AIOps

  - [AIOps在美团的探索与实践——故障发现篇](https://mp.weixin.qq.com/s/AjE7uP7ApVPyL_HdQDkk5g)

## 前端部分

- [从0到1：美团端侧CDN容灾解决方案](https://tech.meituan.com/2022/01/13/phoenix-cdn.html)

## 软技能

- 如何阅读源码

  - https://zhuanlan.zhihu.com/p/72581899
- 画图工具

  - https://blog.csdn.net/weixin_34220834/article/details/91937295
  - https://asciiflow.cn/
- API 设计工具

  - https://openapi.tools/#gui-editors
  - 在线文档工具
    - https://robertlove.github.io/jekyll-openapi/#get-pets
    - https://github.com/robertlove/jekyll-openapi
    - https://mermade.github.io/shins/index.html
- Markdown画图

  - mermaidjs
    - vuepress 插件 https://github.com/eFrane/vuepress-plugin-mermaidjs
    - https://mermaid-js.github.io/mermaid/#/newDiagram
  - kityeditor
    - https://github.com/xjjdog/okmind
    - http://mind.xjjdog.cn/mind/ok-java_tools
    - https://naotu.baidu.com/home
    - https://gitee.com/BinLing2017/vue-kityminder-editor
    - https://gitee.com/orh/vue-kityminder
- 主页列表

  - https://www.codercto.com/courses/newest.html
- 导航

  - https://github.com/vercel/next.js/discussions/categories/help
  - https://chuangzaoshi.com/

### 团队管理

- [哈啰：团队过程管理演进之路](https://mp.weixin.qq.com/s/Q9gczCwf8A_W1DBaEBs30A)

## 网站自身

- 更新：对于403页面跳转到主页面获取去掉相关条件
- 新增：赞赏收入和公益捐赠
- 彩蛋

  - 点击后随机打开一个游戏，但是会有20%的概率打开一个广告
  - 游戏
  - 广告
  - 赞助
  - 随机打开一篇文章
  - AI算法自动推荐