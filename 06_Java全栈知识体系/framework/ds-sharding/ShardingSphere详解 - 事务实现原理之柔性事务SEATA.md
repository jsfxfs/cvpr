# ShardingSphere详解 - 事务实现原理之柔性事务SEATA

> Apache ShardingSphere 集成了 SEATA 作为柔性事务的使用方案，本文主要介绍其实现原理; 这篇文章主要转载自[ShardingSphere官方](https://shardingsphere.apache.org/document/5.1.0/cn/reference/transaction/base-transaction-seata/)网站（V5.1.0版本）。@pdai

## Seata柔性事务

> Apache ShardingSphere 集成了 SEATA 作为柔性事务的使用方案。

**柔性事务**

柔性事务在 2008 年发表的一篇论文中被最早提到， 它提倡采用最终一致性放宽对强一致性的要求，以达到事务处理并发度的提升。

TCC 和 Saga 是两种常见实现方案。 他们主张开发者自行实现对数据库的反向操作，来达到数据在回滚时仍能够保证最终一致性。 SEATA 实现了 SQL 反向操作的自动生成，可以使柔性事务不再必须由开发者介入才能使用。

**Seata**

Seata是阿里集团和蚂蚁金服联合打造的分布式事务框架，截止到0.5.x版本包含了AT事务和TCC事务。其中AT事务的目标是在微服务架构下，提供增量的事务ACID语意，让用户像使用本地事务一样，使用分布式事务，核心理念同ShardingSphere一脉相承。

**Seata AT事务模型**

Seata AT事务模型包含TM(事务管理器)，RM(资源管理器)，TC(事务协调器)。其中TC是一个独立的服务需要单独部署，TM和RM以jar包的方式同业务应用部署在一起，它们同TC建立长连接，在整个事务生命周期内，保持RPC通信。 其中全局事务的发起方作为TM，全局事务的参与者作为RM ; TM负责全局事务的begin和commit/rollback，RM负责分支事务的执行结果上报，并且通过TC的协调进行commit/rollback。

![](https://www.pdai.tech/images/shardingsphere/sharding-x-trans-seata-1.png)

## 实现原理

> 整合 Seata AT 事务时，需要将 TM，RM 和 TC 的模型融入 Apache ShardingSphere 的分布式事务生态中。 在数据库资源上，Seata 通过对接 DataSource 接口，让 JDBC 操作可以同 TC 进行远程通信。 同样，Apache ShardingSphere 也是面向 DataSource 接口，对用户配置的数据源进行聚合。 因此，将 DataSource 封装为 基于Seata 的 DataSource 后，就可以将 Seata AT 事务融入到 Apache ShardingSphere的分片生态中。

![](https://www.pdai.tech/images/shardingsphere/sharding-x-trans-seata-2.png)

### 引擎初始化

包含 Seata 柔性事务的应用启动时，用户配置的数据源会根据 seata.conf 的配置，适配为 Seata 事务所需的 DataSourceProxy，并且注册至 RM 中。

### 开启全局事务

TM 控制全局事务的边界，TM 通过向 TC 发送 Begin 指令，获取全局事务 ID，所有分支事务通过此全局事务 ID，参与到全局事务中；全局事务 ID 的上下文存放在当前线程变量中。

### 执行真实分片SQL

处于 Seata 全局事务中的分片 SQL 通过 RM 生成 undo 快照，并且发送 participate 指令至 TC，加入到全局事务中。 由于 Apache ShardingSphere 的分片物理 SQL 采取多线程方式执行，因此整合 Seata AT 事务时，需要在主线程和子线程间进行全局事务 ID 的上下文传递。

### 提交或回滚事务

提交 Seata 事务时，TM 会向 TC 发送全局事务的提交或回滚指令，TC 根据全局事务 ID 协调所有分支事务进行提交或回滚。