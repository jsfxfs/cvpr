# 数据同步 - Sqoop的介绍和使用

> Sqoop(SQL-to-Hadoop)是一款开源的工具，主要用于在Hadoop(Hive)与传统的数据库(mysql、postgresql…)间进行数据的传递，可以将一个关系型数据库（例如 ： MySQL ,Oracle ,Postgres等）中的数据导入到Hadoop的HDFS中，也可以将HDFS的数据导出到关系型数据库中。

## Sqoop介绍

> 传统的应用程序管理系统，即应用程序与使用RDBMS的关系数据库的交互，是产生大数据的来源之一。由RDBMS生成的这种大数据存储在关系数据库结构中的关系数据库服务器中。

### Sqoop出现的背景

> 当大数据存储和Hadoop生态系统的MapReduce，Hive，HBase，Cassandra，Pig等分析器出现时，他们需要一种工具来与关系数据库服务器进行交互，以导入和导出驻留在其中的大数据。在这里，Sqoop在Hadoop生态系统中占据一席之地，以便在关系数据库服务器和Hadoop的HDFS之间提供可行的交互。

Sqoop - “SQL到Hadoop和Hadoop到SQL”

Sqoop是一个用于在Hadoop和关系数据库服务器之间传输数据的工具。它用于从关系数据库（如MySQL，Oracle）导入数据到Hadoop HDFS，并从Hadoop文件系统导出到关系数据库。它由Apache软件基金会提供。

### Sqoop的功能

> Sqoop是一个用于Hadoop和结构化数据存储（如关系型数据库）之间进行高效传输大批量数据的工具。它包括以下两个方面：

- 可以使用Sqoop将数据从关系型数据库管理系统(如MySQL)导入到Hadoop系统(如HDFS、Hive、HBase)中
- ​将数据从Hadoop系统中抽取并导出到关系型数据库(如MySQL)

![](https://www.pdai.tech/images/bigdata/sqoop/sqoop-1.png)

## Sqoop的版本及架构

> Sqoop有两个大的版本：Sqoop1和Sqoop2; 最新1.4.x 的为 Sqoop1，1.99.X 为 Sqoop2。

关于 Sqoop1 与 Sqoop2 的区别：

- Sqoop1 只是一个客户端工具，Sqoop2 加入了 Server 来集中化管理连接器
- Sqoop1 通过命令行来工作，工作方式单一，Sqoop2 则有更多的方式来工作，比如 REST api接口、Web 页
- Sqoop2 加入权限安全机制

### Sqoop1的架构

sqoop1的架构，仅仅使用一个sqoop客户端

![](https://www.pdai.tech/images/bigdata/sqoop/sqoop-2.png)

### Sqoop2的架构

sqoop2的架构，引入了sqoop server集中化管理connector，以及rest api，web，UI，并引入权限安全机制。

![](https://www.pdai.tech/images/bigdata/sqoop/sqoop-3.png)

## Sqoop的使用

TODO

[Sqoop 5 Minutes Demo](https://sqoop.apache.org/docs/1.99.7/user/Sqoop5MinutesDemo.html)

## Sqoop已停止更新

EOL

Apache Sqoop moved into the Attic in 2021-06. Apache Sqoop mission was the creation and maintenance of software related to Bulk Data Transfer for Apache Hadoop and Structured Datastores.

The website, downloads and issue tracker all remain open, though the issue tracker is read-only. See the website at http://sqoop.apache.org for more information on Sqoop.

As with any project in the Attic - if you should choose to fork Sqoop outside of Apache, please let us know so we can link to your project.

## 参考文章

- https://sqoop.apache.org/docs/1.99.7/admin.html