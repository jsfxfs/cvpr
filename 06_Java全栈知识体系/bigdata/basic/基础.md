# 基础

https://mattturck.com/data2020/

https://mattturck.wpenginepowered.com/wp-content/uploads/2020/09/2020-Data-and-AI-Landscape-Matt-Turck-at-FirstMark-v1.pdf

https://mattturck.wpenginepowered.com/wp-content/uploads/2021/12/2021-MAD-Landscape-v3.pdf

## 架构选型

https://docherish.com/post/ji-zhu-jia-gou-xuan-xing/

1 数据采集 采集框架名称 主要功能 Sqoop 大数据平台和关系型数据库的导入导出 datax 大数据平台和关系型数据库的导入导出 flume 擅长日志数据的采集和解析 logstash 擅长日志数据的采集和解析 maxwell 常用作实时解析mysql的binlog数据 canal 常用作实时解析mysql的binlog数据 waterDrop 数据导入导出工具2 消息中间件 开源MQ 概述 1.RabbitMQ LShift 用Erlang实现，支持多协议，broker架构，重量级 2.ZeroMQ AMQP最初设计者iMatix公司实现，轻量消息内核，无broker设计。C++实现 3.Jafka/Kafka LinkedIn用Scala语言实现，支持hadoop数据并行加载 4.ActiveMQ Apach的一种JMS具体实现，支持代理和p2p部署。支持多协议。Java实现 5.Redis Key-value NoSQL数据库，有MQ的功能 6.MemcacheQ 国人利用memcache缓冲队列协议开发的消息队列,C/C++实现3 实时流式处理 框架名称 框架介绍 Storm Twitter公司开源提供，早期的流式计算框架，基本已经退出大数据的舞台 SparkStreaming 当下最火热的流式处理技术之一 Flink 流式计算 当下最火热的流式处理技术之一 Blink流式计算 阿里二次开发的Flink框架4 数据持久化 框架名称 主要用途 HDFS 分布式文件存储系统 Hbase Key，value对的nosql数据库 Kudu Cloudera公司开源提供的类似于Hbase的数据存储5 离线计算框架 框架名称 基本介绍 MapReduce 最早期的分布式文件计算系统 hive 基于MR的数据仓库工具 impala 号称当前大数据领域最快的sql on hadoop框架，内存消耗特别大 SparkSQL 基于spark，一站式解决批流处理问题 FlinkSQL 基于flink，一站式解决批流处理问题 druid 针对时间序列数据提供低延迟的数据写入以及快速交互式查询的分布式OLAP数据库 kylin 基于Hbase实现的预计算 presto 分布式SQL查询引擎，用于查询分布在一个或多个不同数据源中的大数据集 clickHouse 俄罗斯开源提供的一个OLAP分析框架