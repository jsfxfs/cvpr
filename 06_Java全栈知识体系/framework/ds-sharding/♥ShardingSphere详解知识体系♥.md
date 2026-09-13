# ♥ShardingSphere详解知识体系♥

> ShardingSphere知识体系详解。@pdai

## 相关文章

> ShardingSphere应用和ShardingSphere架构实现两个部分。

### ShardingSphere应用篇

> 主要是通过SpringBoot对ShardingSphere进行集成

- [SpringBoot集成ShardingJDBC - Sharding-JDBC简介和基于MyBatis的单库分表](../../spring/springboot/-SpringBoot集成ShardingJDBC - Sharding-JDBC简介和基于MyBatis的单库分表.md)
  - 本文主要介绍分表分库，以及SpringBoot集成基于ShardingJDBC的单库分表实践。
- [SpringBoot集成ShardingJDBC - 基于JPA的单库分表](../../spring/springboot/SpringBoot集成ShardingJDBC - 基于JPA的单库分表.md)
  - 上文介绍SpringBoot集成基于ShardingJDBC的读写分离实践，本文在此基础上介绍SpringBoot集成基于ShardingJDBC+JPA的单库分表实践。
- [SpringBoot集成ShardingJDBC - 基于JPA的读写分离](../../spring/springboot/SpringBoot集成ShardingJDBC - 基于JPA的读写分离.md)
  - 本文主要介绍分表分库，以及SpringBoot集成基于ShardingJDBC的读写分离实践。
- [SpringBoot集成ShardingJDBC - 基于JPA的DB隔离多租户方案](../../spring/springboot/SpringBoot集成ShardingJDBC - 基于JPA的DB隔离多租户方案.md)
  - 本文主要介绍ShardingJDBC的分片算法和分片策略，并在此基础上通过SpringBoot集成ShardingJDBC的几种策略（标准分片策略，行表达式分片策略和hint分片策略）向你展示DB隔离的多租户方案。

### ShardingSphere架构实现篇

> 主要是对ShardingSphere主要的架构和原理进行分析（多数内容来源于[ShardingSphere官方网站](https://shardingsphere.apache.org/document/5.1.0/cn/overview/)）

- [ShardingSphere详解 - 整体架构设计](ShardingSphere详解 - 整体架构设计.md)
  - Apache ShardingSphere 5.x 版本开始致力于可插拔架构，项目的功能组件能够灵活的以可插拔的方式进行扩展。 目前，数据分片、读写分离、数据库高可用、数据加密、影子库压测等功能，以及对 MySQL、PostgreSQL、SQLServer、Oracle 等 SQL 与协议的支持，均通过插件的方式织入项目; 在 Apache ShardingSphere 中，很多功能实现类的加载方式是通过 SPI（Service Provider Interface） 注入的方式完成的。 SPI 是一种为了被第三方实现或扩展的 API，它可以用于实现框架扩展或组件替换。
- [ShardingSphere详解 - 数据分片的原理](ShardingSphere详解 - 数据分片的原理.md)
  - 本文主要介绍ShardingSphere最重要的数据分片功能的原理，ShardingSphere的3个产品的数据分片主要流程是完全一致的，**Standard 内核流程由 SQL 解析 => SQL 路由 => SQL 改写 => SQL 执行 => 结果归并 组成**，主要用于处理标准分片场景下的 SQL 执行。 **Federation 执行引擎流程由 SQL 解析 => 逻辑优化 => 物理优化 => 优化执行 => Standard 内核流程 组成**。 这篇文章主要转载自[ShardingSphere官方](https://shardingsphere.apache.org/document/legacy/4.x/document/cn/features/sharding/)网站（v4.x版本 + V5.1.0版本），对于进阶数据库中间件或者设计自带Sharding的数据库(真正的分布式SQL数据库）极具参考价值。
- [ShardingSphere详解 - 数据脱敏(加密)详解](ShardingSpherex详解 - 数据脱敏(加密)详解.md)
  - 根据业界对加密的需求及业务改造痛点，提供了一套完整、安全、透明化、低改造成本的数据加密整合解决方案，是 Apache ShardingSphere 数据加密模块的主要设计目标; 这篇文章主要转载自[ShardingSphere官方](https://shardingsphere.apache.org/document/5.1.0/cn/features/encrypt/)网站（V5.1.0版本），对开发者进阶设计通过数据库中间件进行数据脱敏、加密有着很大的借鉴意义。
- [ShardingSphere详解 - 事务实现原理之两阶段事务XA](ShardingSphere详解 - 事务实现原理之两阶段事务XA.md)
  - 本文主要介绍ShardingSphere分布式事务XA的实现原理; 这篇文章主要转载自[ShardingSphere官方](https://shardingsphere.apache.org/document/5.1.0/cn/reference/transaction/base-transaction-seata/)网站（V5.1.0版本）。
- [ShardingSphere详解 - 事务实现原理之柔性事务SAGA](ShardingSphere详解 - 事务实现原理之柔性事务SAGA.md)
  - Apache ShardingSphere 在v5.0版本前还支持柔性事务SAGA，目前看5.x+版本中已经移除了向观众章节，本文主要介绍其实现原理; 这篇文章主要转载自[ShardingSphere官方](https://shardingsphere.apache.org/document/legacy/4.x/document/cn/features/transaction/concept/base-transaction-saga/)网站（V4.x版本）。
- [ShardingSphere详解 - 事务实现原理之柔性事务SEATA](ShardingSphere详解 - 事务实现原理之柔性事务SEATA.md)
  - Apache ShardingSphere 集成了 SEATA 作为柔性事务的使用方案，本文主要介绍其实现原理; 这篇文章主要转载自[ShardingSphere官方](https://shardingsphere.apache.org/document/5.1.0/cn/reference/transaction/base-transaction-seata/)网站（V5.1.0版本）。
- [ShardingSphere详解 - 弹性伸缩原理](ShardingSphere详解 - 弹性伸缩原理.md)
  - 支持自定义分片算法，减少数据伸缩及迁移时的业务影响，提供一站式的通用弹性伸缩解决方案，是 Apache ShardingSphere 弹性伸缩的主要设计目标; 这篇文章主要转载自[ShardingSphere官方](https://shardingsphere.apache.org/document/5.1.0/cn/features/scaling/)网站（V5.1.0版本）。
- [ShardingSphere详解 - 通过影子库进行压测](ShardingSphere详解 - 通过影子库进行压测.md)
  - Apache ShardingSphere 关注于全链路压测场景下，数据库层面的解决方案。 将压测数据自动路由至用户指定的数据库，是 Apache ShardingSphere 影子库模块的主要设计目标; 这篇文章主要转载自[ShardingSphere官方](https://shardingsphere.apache.org/document/5.1.0/cn/reference/shadow)网站（V5.1.0版本）。