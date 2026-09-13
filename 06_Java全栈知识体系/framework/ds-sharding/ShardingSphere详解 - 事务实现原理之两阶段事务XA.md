# ShardingSphere详解 - 事务实现原理之两阶段事务XA

> 本文主要介绍ShardingSphere分布式事务XA的实现原理; 这篇文章主要转载自[ShardingSphere官方](https://shardingsphere.apache.org/document/5.1.0/cn/reference/transaction/base-transaction-seata/)网站（V5.1.0版本）。@pdai

## 两阶段事务XA介绍

两阶段事务提交采用的是 X/OPEN 组织所定义的 DTP 模型所抽象的 AP（应用程序）, TM（事务管理器）和 RM（资源管理器） 概念来保证分布式事务的强一致性。 其中 TM 与 RM 间采用 XA 的协议进行双向通信。 与传统的本地事务相比，XA 事务增加了准备阶段，数据库除了被动接受提交指令外，还可以反向通知调用方事务是否可以被提交。 TM 可以收集所有分支事务的准备结果，并于最后进行原子提交，以保证事务的强一致性。

![](https://www.pdai.tech/images/shardingsphere/sharding-x-trans-xa-2.png)

Java 通过定义 JTA 接口实现了 XA 模型，JTA 接口中的 ResourceManager 需要数据库厂商提供 XA 驱动实现， TransactionManager 则需要事务管理器的厂商实现，传统的事务管理器需要同应用服务器绑定，因此使用的成本很高。 而嵌入式的事务管器可以通过 jar 形式提供服务，同 Apache ShardingSphere 集成后，可保证分片后跨库事务强一致性。

通常，只有使用了事务管理器厂商所提供的 XA 事务连接池，才能支持 XA 的事务。 Apache ShardingSphere 在整合 XA 事务时，采用分离 XA 事务管理和连接池管理的方式，做到对应用程序的零侵入。

## 实现原理

> XAShardingSphereTransactionManager 为 Apache ShardingSphere 的分布式事务的 XA 实现类。 它主要负责对多数据源进行管理和适配，并且将相应事务的开启、提交和回滚操作委托给具体的 XA 事务管理器。

![](https://www.pdai.tech/images/shardingsphere/sharding-x-trans-xa-1.png)

### 开启全局事务

收到接入端的 set autoCommit=0 时，XAShardingSphereTransactionManager 将调用具体的 XA 事务管理器开启 XA 全局事务，以 XID 的形式进行标记。

### 执行真实分片SQL

XAShardingSphereTransactionManager 将数据库连接所对应的 XAResource 注册到当前 XA 事务中之后，事务管理器会在此阶段发送 XAResource.start 命令至数据库。 数据库在收到 XAResource.end 命令之前的所有 SQL 操作，会被标记为 XA 事务。

例如:

```bash
XAResource1.start             ## Enlist阶段执行
statement.execute("sql1");    ## 模拟执行一个分片SQL1
statement.execute("sql2");    ## 模拟执行一个分片SQL2
XAResource1.end               ## 提交阶段执行
```

示例中的 sql1 和 sql2 将会被标记为 XA 事务。

### 提交或回滚事务

XAShardingSphereTransactionManager 在接收到接入端的提交命令后，会委托实际的 XA 事务管理进行提交动作， 事务管理器将收集到的当前线程中所有注册的 XAResource，并发送 XAResource.end 指令，用以标记此 XA 事务边界。 接着会依次发送 prepare 指令，收集所有参与 XAResource 投票。 若所有 XAResource 的反馈结果均为正确，则调用 commit 指令进行最终提交； 若有任意 XAResource 的反馈结果不正确，则调用 rollback 指令进行回滚。 在事务管理器发出提交指令后，任何 XAResource 产生的异常都会通过恢复日志进行重试，以保证提交阶段的操作原子性，和数据强一致性。

例如:

```bash
XAResource1.prepare           ## ack: yes
XAResource2.prepare           ## ack: yes
XAResource1.commit
XAResource2.commit

XAResource1.prepare           ## ack: yes
XAResource2.prepare           ## ack: no
XAResource1.rollback
XAResource2.rollback
```