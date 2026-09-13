# ShardingSphere详解 - 事务实现原理之柔性事务SAGA

> Apache ShardingSphere 在v5.0版本前还支持柔性事务SAGA，目前看5.x+版本中已经移除了向观众章节，本文主要介绍其实现原理; 这篇文章主要转载自[ShardingSphere官方](https://shardingsphere.apache.org/document/legacy/4.x/document/cn/features/transaction/concept/base-transaction-saga/)网站（V4.x版本）。@pdai

## Saga事务

Saga这个概念来源于三十多年前的一篇数据库论文Sagas ，一个Saga事务是一个有多个短时事务组成的长时的事务。 在分布式事务场景下，我们把一个Saga分布式事务看做是一个由多个本地事务组成的事务，每个本地事务都有一个与之对应的补偿事务。在Saga事务的执行过程中，如果某一步执行出现异常，Saga事务会被终止，同时会调用对应的补偿事务完成相关的恢复操作，这样保证Saga相关的本地事务要么都是执行成功，要么通过补偿恢复成为事务执行之前的状态。

**自动反向补偿**

Saga定义了一个事务中的每个子事务都有一个与之对应的反向补偿操作。由Saga事务管理器根据程序执行结果生成一张有向无环图，并在需要执行回滚操作时，根据该图依次按照相反的顺序调用反向补偿操作。Saga事务管理器只用于控制何时重试，何时补偿，并不负责补偿的内容，补偿的具体操作需要由开发者自行提供。

ShardingSphere采用反向SQL技术，将对数据库进行更新操作的SQL自动生成反向SQL，并交由saga-actuator执行，使用方则无需再关注如何实现补偿方法，将柔性事务管理器的应用范畴成功的定位回了事务的本源——数据库层面。

## 实现原理

> Saga柔性事务的实现类为SagaShardingTransactionMananger, ShardingSphere通过Hook的方式拦截逻辑SQL的解析和路由结果，这样，在分片物理SQL执行前，可以生成逆向SQL，在事务提交阶段再把SQL调用链交给Saga引擎处理。

![](https://www.pdai.tech/images/shardingsphere/sharding-x-trans-saga-2.png)

### Init（Saga引擎初始化）

包含Saga柔性事务的应用启动时，saga-actuator引擎会根据saga.properties的配置进行初始化的流程。

### Begin（开启Saga全局事务）

每次开启Saga全局事务时，将会生成本次全局事务的上下文（SagaTransactionContext），事务上下文记录了所有子事务的正向SQL和逆向SQL，作为生成事务调用链的元数据使用。

### 执行物理SQL

在物理SQL执行前，ShardingSphere根据SQL的类型生成逆向SQL，这里是通过Hook的方式拦截Parser的解析结果进行实现。

### Commit/rollback（提交Saga事务）

提交阶段会生成Saga执行引擎所需的调用链路图，commit操作产生ForwardRecovery（正向SQL补偿）任务，rollback操作产生BackwardRecovery任务（逆向SQL补偿）。