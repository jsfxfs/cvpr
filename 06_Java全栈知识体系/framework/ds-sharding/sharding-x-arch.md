# ShardingSphere详解 - 整体架构设计

> Apache ShardingSphere 5.x 版本开始致力于可插拔架构，项目的功能组件能够灵活的以可插拔的方式进行扩展。 目前，数据分片、读写分离、数据库高可用、数据加密、影子库压测等功能，以及对 MySQL、PostgreSQL、SQLServer、Oracle 等 SQL 与协议的支持，均通过插件的方式织入项目; 在 Apache ShardingSphere 中，很多功能实现类的加载方式是通过 SPI（Service Provider Interface） 注入的方式完成的。 SPI 是一种为了被第三方实现或扩展的 API，它可以用于实现框架扩展或组件替换。@pdai

## ShardingSphere产品定位

> Apache ShardingSphere 产品定位为 Database Plus，旨在构建多模数据库上层的标准和生态。 它关注如何充分合理地利用数据库的计算和存储能力，而并非实现一个全新的数据库。ShardingSphere 站在数据库的上层视角，关注他们之间的协作多于数据库自身。

- **连接、增量和可插拔是 Apache ShardingSphere 的核心概念**。
- **连接**：通过对数据库协议、SQL 方言以及数据库存储的灵活适配，快速的连接应用与多模式的异构数据库；
- **增量**：获取数据库的访问流量，并提供流量重定向（数据分片、读写分离、影子库）、流量变形（数据加密、数据脱敏）、流量鉴权（安全、审计、权限）、流量治理（熔断、限流）以及流量分析（服务质量分析、可观察性）等透明化增量功能；
- **可插拔**：项目采用微内核 + 三层可插拔模型，使内核、功能组件以及生态对接完全能够灵活的方式进行插拔式扩展，开发者能够像使用积木一样定制属于自己的独特系统。

![](https://www.pdai.tech/images/shardingsphere/sharding-x-arch-1.png)

- **线路规划**

![](https://www.pdai.tech/images/shardingsphere/sharding-x-arch-6.png)

## ShardingSphere组成简介

> Apache ShardingSphere 由 JDBC、Proxy 和 Sidecar（规划中）这 3 款既能够独立部署，又支持混合部署配合使用的产品组成。 它们均提供标准化的基于数据库作为存储节点的增量功能，可适用于如 Java 同构、异构语言、云原生等各种多样化的应用场景。

关系型数据库当今依然占有巨大市场份额，是企业核心系统的基石，未来也难于撼动，我们更加注重在原有基础上提供增量，而非颠覆。

| ShardingSphere-JDBC | ShardingSphere-Proxy | ShardingSphere-Sidecar |
| --- | --- | --- |
| 数据库 | 任意 | MySQL/PostgreSQL |
| 连接消耗数 | 高 | 低 |
| 异构语言 | 仅 Java | 任意 |
| 性能 损耗低 | 损耗略高 | 损耗低 |
| 无中心化 | 是 | 否 |
| 静态入口 | 无 | 有 |

### ShardingSphere-JDBC

> **定位为轻量级 Java 框架，在 Java 的 JDBC 层提供的额外服务**。 它使用客户端直连数据库，以 jar 包形式提供服务，无需额外部署和依赖，可理解为增强版的 JDBC 驱动，完全兼容 JDBC 和各种 ORM 框架。

- 适用于任何基于 JDBC 的 ORM 框架，如：JPA, Hibernate, Mybatis, Spring JDBC Template 或直接使用 JDBC；
- 支持任何第三方的数据库连接池，如：DBCP, C3P0, BoneCP, HikariCP 等；
- 支持任意实现 JDBC 规范的数据库，目前支持 MySQL，PostgreSQL，Oracle，SQLServer 以及任何可使用 JDBC 访问的数据库。

![](https://www.pdai.tech/images/shardingsphere/sharding-x-arch-2.png)

### ShardingSphere-Proxy

> **定位为透明化的数据库代理端，提供封装了数据库二进制协议的服务端版本，用于完成对异构语言的支持**。 目前提供 MySQL 和 PostgreSQL（兼容 openGauss 等基于 PostgreSQL 的数据库）版本，它可以使用任何兼容 MySQL/PostgreSQL 协议的访问客户端（如：MySQL Command Client, MySQL Workbench, Navicat 等）操作数据，对 DBA 更加友好。

- 向应用程序完全透明，可直接当做 MySQL/PostgreSQL 使用；
- 适用于任何兼容 MySQL/PostgreSQL 协议的的客户端。

![](https://www.pdai.tech/images/shardingsphere/sharding-x-arch-3.png)

### ShardingSphere-Sidecar（TODO）

> **定位为 Kubernetes 的云原生数据库代理，以 Sidecar 的形式代理所有对数据库的访问**。 通过无中心、零侵入的方案提供与数据库交互的啮合层，即 Database Mesh，又可称数据库网格。

Database Mesh 的关注重点在于如何将分布式的数据访问应用与数据库有机串联起来，它更加关注的是交互，是将杂乱无章的应用与数据库之间的交互进行有效地梳理。 使用 Database Mesh，访问数据库的应用和数据库终将形成一个巨大的网格体系，应用和数据库只需在网格体系中对号入座即可，它们都是被啮合层所治理的对象。

![](https://www.pdai.tech/images/shardingsphere/sharding-x-arch-4.png)

### 混合架构

> Apache ShardingSphere 是多接入端共同组成的生态圈。 通过混合使用 ShardingSphere-JDBC 和 ShardingSphere-Proxy，并采用同一注册中心统一配置分片策略，能够灵活的搭建适用于各种场景的应用系统，使得架构师更加自由地调整适合于当前业务的最佳系统架构。

- ShardingSphere-JDBC 采用无中心化架构，与应用程序共享资源，适用于 Java 开发的高性能的轻量级 OLTP 应用；
- ShardingSphere-Proxy 提供静态入口以及异构语言的支持，独立于应用程序部署，适用于 OLAP 应用以及对分片数据库进行管理和运维的场景。

![](https://www.pdai.tech/images/shardingsphere/sharding-x-arch-5.png)

## ShardingSphere可插拔架构

> 让开发者能够像使用积木一样定制属于自己的独特系统，是 Apache ShardingSphere 可插拔架构的设计目标。

在 Apache ShardingSphere 中，很多功能实现类的加载方式是通过 SPI（Service Provider Interface） 注入的方式完成的。 SPI 是一种为了被第三方实现或扩展的 API，它可以用于实现框架扩展或组件替换。

SPI相关的文章请参考：[Java常用机制 - SPI机制](../../java/advanced/java-advanced-spi.md)

**挑战**

可插拔架构对程序架构设计的要求非常高，需要将各个模块相互独立，互不感知，并且通过一个可插拔内核，以叠加的方式将各种功能组合使用。 设计一套将功能开发完全隔离的架构体系，既可以最大限度的将开源社区的活力激发出来，也能够保障项目的质量。

Apache ShardingSphere 5.x 版本开始致力于可插拔架构，项目的功能组件能够灵活的以可插拔的方式进行扩展。 目前，数据分片、读写分离、数据库高可用、数据加密、影子库压测等功能，以及对 MySQL、PostgreSQL、SQLServer、Oracle 等 SQL 与协议的支持，均通过插件的方式织入项目。 Apache ShardingSphere 目前已提供数十个 SPI 作为系统的扩展点，而且仍在不断增加中。

![](https://www.pdai.tech/images/shardingsphere/sharding-x-arch-7.png)

### 实现

> Apache ShardingSphere 的可插拔架构划分为 3 层，它们是：L1 内核层、L2 功能层、L3 生态层。

#### L1 内核层

是数据库基本能力的抽象，其所有组件均必须存在，但具体实现方式可通过可插拔的方式更换。 主要包括查询优化器、分布式事务引擎、分布式执行引擎、权限引擎和调度引擎等。

#### L2 功能层

用于提供增量能力，其所有组件均是可选的，可以包含零至多个组件。组件之间完全隔离，互无感知，多组件可通过叠加的方式相互配合使用。 主要包括数据分片、读写分离、数据库高可用、数据加密、影子库等。用户自定义功能可完全面向 Apache ShardingSphere 定义的顶层接口进行定制化扩展，而无需改动内核代码。

#### L3 生态层

用于对接和融入现有数据库生态，包括数据库协议、SQL 解析器和存储适配器，分别对应于 Apache ShardingSphere 以数据库协议提供服务的方式、SQL 方言操作数据的方式以及对接存储节点的数据库类型。