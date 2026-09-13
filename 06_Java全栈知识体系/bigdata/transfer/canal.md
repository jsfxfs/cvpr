# 数据同步 - Canal的介绍和使用

> canal是由Alibaba开源的一个基于binlog的增量日志组件，其核心原理是canal伪装成Mysql的slave，发送dump协议获取binlog，解析并存储起来给客户端消费。

## Canal介绍

> `Canal [kə'næl]`，译意为水道/管道/沟渠，主要用途是基于 MySQL 数据库增量日志解析，提供增量数据订阅和消费

### Canal出现的背景

早期阿里巴巴因为杭州和美国双机房部署，存在跨机房同步的业务需求，实现方式主要是基于业务 trigger 获取增量变更。从 2010 年开始，业务逐步尝试数据库日志解析获取增量变更进行同步，由此衍生出了大量的数据库增量订阅和消费业务。

基于日志增量订阅和消费的业务包括

- 数据库镜像
- 数据库实时备份
- 索引构建和实时维护(拆分异构索引、倒排索引等)
- 业务 cache 刷新
- 带业务逻辑的增量数据处理

### Canal是什么

Canal基于 MySQL 数据库增量日志解析，提供增量数据订阅和消费. 当前的 canal 支持源端 MySQL 版本包括 5.1.x , 5.5.x , 5.6.x , 5.7.x , 8.0.x。

![](https://www.pdai.tech/images/bigdata/canal/canal-1.png)

## Canal原理

> 需要先理解MySQL的主从复制的原理

![](https://www.pdai.tech/images/mysql/master-slave.png)

- MySQL master 将数据变更写入二进制日志( binary log, 其中记录叫做二进制日志事件binary log events，可以通过 show binlog events 进行查看)
- MySQL slave 将 master 的 binary log events 拷贝到它的中继日志(relay log)
- MySQL slave 重放 relay log 中事件，将数据变更反映它自己的数据

**Canal的原理如下**

- canal 模拟 MySQL slave 的交互协议，伪装自己为 MySQL slave ，向 MySQL master 发送dump 协议
- MySQL master 收到 dump 请求，开始推送 binary log 给 slave (即 canal )
- canal 解析 binary log 对象(原始为 byte 流)

## Canal架构

![](https://www.pdai.tech/images/bigdata/canal/canal-2.png)

说明：

- server代表一个canal运行实例，对应于一个jvm
- instance对应于一个数据队列 （1个server对应1..n个instance)

instance模块：

- **eventParser** ： 数据源接入，模拟slave协议和master进行交互，协议解析
- **eventSink** ： Parser和Store链接器，进行数据过滤，加工，分发的工作
- **eventStore** ： 数据存储
- **metaManager** ： 增量订阅&消费信息管理器

### EventParser设计

![](https://www.pdai.tech/images/bigdata/canal/canal-3.png)

整个parser过程大致可分为几步：

- Connection获取上一次解析成功的位置 (如果第一次启动，则获取初始指定的位置或者是当前数据库的binlog位点)
- Connection建立链接，发送BINLOG_DUMP指令

```bash
// 0. write command number
// 1. write 4 bytes bin-log position to start at
// 2. write 2 bytes bin-log flags
// 3. write 4 bytes server id of the slave
// 4. write bin-log file name
```

- Mysql开始推送Binaly Log
- 接收到的Binaly Log的通过Binlog parser进行协议解析，补充一些特定信息

```bash
// 补充字段名字，字段类型，主键信息，unsigned类型处理
```

- 传递给EventSink模块进行数据存储，是一个阻塞操作，直到存储成功
- 存储成功后，定时记录Binaly Log位置

### EventSink设计

![](https://www.pdai.tech/images/bigdata/canal/canal-4.png)

说明：

- 数据过滤：支持通配符的过滤模式，表名，字段内容等
- 数据路由/分发：解决1:n (1个parser对应多个store的模式)
- 数据归并：解决n:1 (多个parser对应1个store)
- 数据加工：在进入store之前进行额外的处理，比如join

**数据1:n业务**

为了合理的利用数据库资源， 一般常见的业务都是按照schema进行隔离，然后在mysql上层或者dao这一层面上，进行一个数据源路由，屏蔽数据库物理位置对开发的影响，阿里系主要是通过cobar/tddl来解决数据源路由问题。

所以，一般一个数据库实例上，会部署多个schema，每个schema会有由1个或者多个业务方关注

**数据n:1业务**

同样，当一个业务的数据规模达到一定的量级后，必然会涉及到水平拆分和垂直拆分的问题，针对这些拆分的数据需要处理时，就需要链接多个store进行处理，消费的位点就会变成多份，而且数据消费的进度无法得到尽可能有序的保证。

所以，在一定业务场景下，需要将拆分后的增量数据进行归并处理，比如按照时间戳/全局id进行排序归并.

### EventStore设计

目前canal实现了memory内存、本地file存储以及持久化到zookeeper以保障数据集群共享。memory内存的RingBuffer设计如下图：

![](https://www.pdai.tech/images/bigdata/canal/canal-6.png)

定义了3个cursor：

- Put : Sink模块进行数据存储的最后一次写入位置
- Get : 数据订阅获取的最后一次提取位置
- Ack : 数据消费成功的最后一次消费位置

借鉴Disruptor的RingBuffer的实现，将RingBuffer拉直来看：

![](https://www.pdai.tech/images/bigdata/canal/canal-7.png)

### Instance设计

![](https://www.pdai.tech/images/bigdata/canal/canal-8.png)

instance代表了一个实际运行的数据队列，包括了EventPaser,EventSink,EventStore等组件。

抽象了CanalInstanceGenerator，主要是考虑配置的管理方式：

- **manager方式**： 和你自己的内部web console/manager系统进行对接。(目前主要是公司内部使用)
- **spring方式**：基于spring xml + properties进行定义，构建spring配置.

### Server设计

![](https://www.pdai.tech/images/bigdata/canal/canal-9.png)

server代表了一个canal的运行实例，为了方便组件化使用，特意抽象了Embeded(嵌入式) / Netty(网络访问)的两种实现

- **Embeded** : 对latency和可用性都有比较高的要求，自己又能hold住分布式的相关技术(比如failover)
- **Netty** : 基于netty封装了一层网络协议，由canal server保证其可用性，采用的pull模型，当然latency会稍微打点折扣，不过这个也视情况而定。(阿里系的notify和metaq，典型的push/pull模型，目前也逐步的在向pull模型靠拢，push在数据量大的时候会有一些问题)

### 增量订阅/消费设计

![](https://www.pdai.tech/images/bigdata/canal/canal-10.jpg)

具体的协议格式，可参见：[CanalProtocol.proto](https://github.com/alibaba/canal/blob/master/protocol/src/main/java/com/alibaba/otter/canal/protocol/CanalProtocol.proto)

**get/ack/rollback协议介绍**：

- Message getWithoutAck(int batchSize)，允许指定batchSize，一次可以获取多条，每次返回的对象为Message，包含的内容为：
  - batch id 唯一标识
  - entries 具体的数据对象，对应的数据对象格式：EntryProtocol.proto
- void rollback(long batchId)，顾命思议，回滚上次的get请求，重新获取数据。基于get获取的batchId进行提交，避免误操作
- void ack(long batchId)，顾命思议，确认已经消费成功，通知server删除数据。基于get获取的batchId进行提交，避免误操作

canal的get/ack/rollback协议和常规的jms协议有所不同，允许get/ack异步处理，比如可以连续调用get多次，后续异步按顺序提交ack/rollback，项目中称之为流式api.

**流式api设计的好处**：

- get/ack异步化，减少因ack带来的网络延迟和操作成本 (99%的状态都是处于正常状态，异常的rollback属于个别情况，没必要为个别的case牺牲整个性能)
- get获取数据后，业务消费存在瓶颈或者需要多进程/多线程消费时，可以不停的轮询get数据，不停的往后发送任务，提高并行化. (作者在实际业务中的一个case：业务数据消费需要跨中美网络，所以一次操作基本在200ms以上，为了减少延迟，所以需要实施并行化)

**流式api设计**：

1. 每次get操作都会在meta中产生一个mark，mark标记会递增，保证运行过程中mark的唯一性
2. 每次的get操作，都会在上一次的mark操作记录的cursor继续往后取，如果mark不存在，则在last ack cursor继续往后取
3. 进行ack时，需要按照mark的顺序进行数序ack，不能跳跃ack. ack会删除当前的mark标记，并将对应的mark位置更新为last ack cusor
4. 一旦出现异常情况，客户端可发起rollback情况，重新置位：删除所有的mark, 清理get请求位置，下次请求会从last ack cursor继续往后取

### 数据对象格式：EntryProtocol.proto

```bash
Entry
	Header
		logfileName [binlog文件名]
		logfileOffset [binlog position]
		executeTime [binlog里记录变更发生的时间戳]
		schemaName [数据库实例]
		tableName [表名]
		eventType [insert/update/delete类型]
	entryType 	[事务头BEGIN/事务尾END/数据ROWDATA]
	storeValue 	[byte数据,可展开，对应的类型为RowChange]
RowChange
isDdl		[是否是ddl变更操作，比如create table/drop table]
sql		[具体的ddl sql]
rowDatas	[具体insert/update/delete的变更数据，可为多条，1个binlog event事件可对应多条变更，比如批处理]
beforeColumns [Column类型的数组]
afterColumns [Column类型的数组]


Column
index		[column序号]
sqlType		[jdbc type]
name		[column name]
isKey		[是否为主键]
updated		[是否发生过变更]
isNull		[值是否为null]
value		[具体的内容，注意为文本]
```

说明：

- 可以提供数据库变更前和变更后的字段内容，针对binlog中没有的name,isKey等信息进行补全
- 可以提供ddl的变更语句

### HA机制设计

canal的ha分为两部分，canal server和canal client分别有对应的ha实现

- **canal server**: 为了减少对mysql dump的请求，不同server上的instance要求同一时间只能有一个处于running，其他的处于standby状态.
- **canal client**: 为了保证有序性，一份instance同一时间只能由一个canal client进行get/ack/rollback操作，否则客户端接收无法保证有序。

整个HA机制的控制主要是依赖了zookeeper的几个特性，watcher和EPHEMERAL节点(和session生命周期绑定)，可以看下我之前zookeeper的相关文章。

Canal Server:

![](https://www.pdai.tech/images/bigdata/canal/canal-12.png)

大致步骤：

- canal server要启动某个canal instance时都先向zookeeper进行一次尝试启动判断 (实现：创建EPHEMERAL节点，谁创建成功就允许谁启动)
- 创建zookeeper节点成功后，对应的canal server就启动对应的canal instance，没有创建成功的canal instance就会处于standby状态
- 一旦zookeeper发现canal server A创建的节点消失后，立即通知其他的canal server再次进行步骤1的操作，重新选出一个canal server启动instance.
- canal client每次进行connect时，会首先向zookeeper询问当前是谁启动了canal instance，然后和其建立链接，一旦链接不可用，会重新尝试connect.

Canal Client的方式和canal server方式类似，也是利用zookeeper的抢占EPHEMERAL节点的方式进行控制.

## Canal使用

- [Quick Start](https://github.com/alibaba/canal/wiki/QuickStart)
- [Client Example](https://github.com/alibaba/canal/wiki/ClientExample)
- [Canal Admin QuickStart](https://github.com/alibaba/canal/wiki/Canal-Admin-QuickStart)

## 参考文章

https://github.com/alibaba/canal

https://blog.csdn.net/qq_43338943/article/details/118737010