# ▶SpringBoot数据库管理 - 用Liquibase对数据库管理和迁移

> Liquibase是一个用于**用于跟踪、管理和应用数据库变化的开源工具**，通过日志文件(changelog)的形式记录数据库的变更(changeset)，然后执行日志文件中的修改，将数据库更新或回滚(rollback)到一致的状态。它的目标是提供一种数据库类型无关的解决方案，通过执行schema类型的文件来达到迁移。本文主要介绍SpringBoot与Liquibase的集成。@pdai

## 知识准备

> 需要理解什么是Liquibase，它的出现是要解决什么问题。

### 什么是Liquibase？这类工具要解决什么问题？

> Liquibase是一个用于**用于跟踪、管理和应用数据库变化的开源工具**，通过日志文件(changelog)的形式记录数据库的变更(changeset)，然后执行日志文件中的修改，将数据库更新或回滚(rollback)到一致的状态。它的目标是提供一种数据库类型无关的解决方案，通过执行schema类型的文件来达到迁移。

**其优点主要有以下**：

- 支持几乎所有主流的数据库，目前支持包括 Oracle/Sql Server/DB2/MySql/Sybase/PostgreSQL等 [各种数据库](https://docs.liquibase.com/install/tutorials/home.html)，这样在数据库的部署和升级环节可帮助应用系统支持多数据库；
- 支持版本控制，这样就能支持多开发者的协作维护；
- 日志文件支持多种格式，如XML, YAML, JSON, SQL等；
- 提供变化应用的回滚功能，可按时间、数量或标签（tag）回滚已应用的变化。通过这种方式，开发人员可轻易的还原数据库在任何时间点的状态
- 支持多种运行方式，如命令行、Spring集成、Maven插件、Gradle插件等。

**为何会出现Liquibase这类工具呢**？

在实际上线的应用中，随着版本的迭代，经常会遇到需要变更数据库表和字段，必然会遇到需要对这些变更进行记录和管理，以及回滚等等；同时只有脚本化且版本可管理，才能在让数据库实现真正的DevOps（自动化执行 + 回滚等）。在这样的场景下Liquibase等工具的出现也就成为了必然。

### Liquibase有哪些概念？是如何工作的？

> **工作流程**：将**SQL**变更记录到**changeset**，多个changeset变更组成了日志文件(**changelog**)，liquibase将changelog更新日志文件同步到指定的**RDBMS**中。

![](https://www.pdai.tech/images/spring/springboot/springboot-liquibase-1.png)

日志文件(databaseChangeLog)支持多种格式，如XML, YAML, JSON, SQL; 我们以xml为例，看下相关配置

```xml
<?xml version="1.0" encoding="UTF-8"?> 
<databaseChangeLog
	xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:ext="http://www.liquibase.org/xml/ns/dbchangelog-ext"
	xmlns:pro="http://www.liquibase.org/xml/ns/pro"
	xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
		http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.9.0.xsd
		http://www.liquibase.org/xml/ns/dbchangelog-ext http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-ext.xsd
		http://www.liquibase.org/xml/ns/pro http://www.liquibase.org/xml/ns/pro/liquibase-pro-4.9.0.xsd">
    <changeSet id="1" author="bob">  
        <comment>A sample change log</comment>  
        <createTable/> 
    </changeSet>  
    <changeSet id="2" author="bob" runAlways="true">  
        <alterTable/>  
    </changeSet>  
    <changeSet id="3" author="alice" failOnError="false" dbms="oracle">
        <alterTable/>  
    </changeSet>  
    <changeSet id="4" author="alice" failOnError="false" dbms="!oracle">
        <alterTable/>  
    </changeSet>  
</databaseChangeLog>
```

## 简单示例

> 这里主要介绍基于SpringBoot集成liquibase来管理数据库的变更。

### POM依赖

Maven 包的依赖，主要包含mysql驱动, JDBC(这里spring-boot-starter-data-jpa包含了jdbc包，当然直接引入jdbc包也行)，以及liquibase包。

```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.28</version>
</dependency>
<dependency>
    <groupId>com.github.wenhao</groupId>
    <artifactId>jpa-spec</artifactId>
    <version>3.1.0</version>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>

<dependency>
    <groupId>org.liquibase</groupId>
    <artifactId>liquibase-core</artifactId>
    <version>4.9.1</version>
</dependency>
```

### yml配置

> SpringBoot AutoConfig默认已经包含了对liquibase的配置，在spring.liquibase配置下。

基础的配置，可以直接使用如下（主要是指定change-log的位置，默认的位置是classpath:/db/changelog/db.changelog-master.yaml）：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/test_db_liquibase?useSSL=false&autoReconnect=true&characterEncoding=utf8
    driver-class-name: com.mysql.cj.jdbc.Driver
    username: root
    password: bfXa4Pt2lUUScy8jakXf
  liquibase:
    enabled: true
    # 如下配置是被spring.datasource赋值的，所以可以不配置
#    url: jdbc:mysql://localhost:3306/test_db_liquibase?useSSL=false&autoReconnect=true&characterEncoding=utf8
#    user: root
#    password: bfXa4Pt2lUUScy8jakXf
    change-log: classpath:/db/changelog/db.changelog-master.yaml
```

在开发时，更多的配置可以从如下SpringBoot AutoConfig中找到。

![](https://www.pdai.tech/images/spring/springboot/springboot-liquibase-2.png)

### 新增changelog

XML方式固然OK，不过依然推荐使用yml格式。

```yaml
databaseChangeLog:
  - changeSet:
      id: 20220412-01
      author: pdai
      changes:
        - createTable:
            tableName: person
            columns:
              - column:
                  name: id
                  type: int
                  autoIncrement: true
                  constraints:
                    primaryKey: true
                    nullable: false
              - column:
                  name: firstname
                  type: varchar(50)
              - column:
                  name: lastname
                  type: varchar(50)
                  constraints:
                    nullable: false
              - column:
                  name: state
                  type: char(2)

  - changeSet:
      id: 20220412-02
      author: pdai
      changes:
        - addColumn:
            tableName: person
            columns:
              - column:
                  name: username
                  type: varchar(8)

  - changeSet:
      id: 20220412-03
      author: pdai
      changes:
        - addLookupTable:
            existingTableName: person
            existingColumnName: state
            newTableName: state
            newColumnName: id
            newColumnDataType: char(2)
```

### 测试

启动springBootApplication, 我们可以看到如下的几个changeSet被依次执行

```bash
2022-04-12 20:41:20.591  INFO 8476 --- [           main] liquibase.lockservice                    : Successfully acquired change log lock
2022-04-12 20:41:20.737  INFO 8476 --- [           main] liquibase.changelog                      : Creating database history table with name: test_db_liquibase.DATABASECHANGELOG
2022-04-12 20:41:20.783  INFO 8476 --- [           main] liquibase.changelog                      : Reading from test_db_liquibase.DATABASECHANGELOG
Running Changeset: classpath:/db/changelog/db.changelog-master.yaml::20220412-01::pdai
2022-04-12 20:41:20.914  INFO 8476 --- [           main] liquibase.changelog                      : Table person created
2022-04-12 20:41:20.914  INFO 8476 --- [           main] liquibase.changelog                      : ChangeSet classpath:/db/changelog/db.changelog-master.yaml::20220412-01::pdai ran successfully in 53ms
Running Changeset: classpath:/db/changelog/db.changelog-master.yaml::20220412-02::pdai
2022-04-12 20:41:20.952  INFO 8476 --- [           main] liquibase.changelog                      : Columns username(varchar(8)) added to person
2022-04-12 20:41:20.952  INFO 8476 --- [           main] liquibase.changelog                      : ChangeSet classpath:/db/changelog/db.changelog-master.yaml::20220412-02::pdai ran successfully in 31ms
Running Changeset: classpath:/db/changelog/db.changelog-master.yaml::20220412-03::pdai
2022-04-12 20:41:21.351  INFO 8476 --- [           main] liquibase.changelog                      : Lookup table added for person.state
2022-04-12 20:41:21.351  INFO 8476 --- [           main] liquibase.changelog                      : ChangeSet classpath:/db/changelog/db.changelog-master.yaml::20220412-03::pdai ran successfully in 389ms
2022-04-12 20:41:21.382  INFO 8476 --- [           main] liquibase.lockservice                    : Successfully released change log lock
```

查看数据库，你会发现数据已经变更

![](https://www.pdai.tech/images/spring/springboot/springboot-liquibase-3.png)

那我们如果重新启动这个SpringBootApplication，会怎么呢？

很显然，因为databasechangelog表中已经有相关执行记录了，所以将不再执行变更

```bash
2022-04-12 20:49:01.566  INFO 9144 --- [           main] liquibase.lockservice                    : Successfully acquired change log lock
2022-04-12 20:49:01.761  INFO 9144 --- [           main] liquibase.changelog                      : Reading from test_db_liquibase.DATABASECHANGELOG
2022-04-12 20:49:01.812  INFO 9144 --- [           main] liquibase.lockservice                    : Successfully released change log lock
```

## 进一步理解

> 通过几个问题，进一步理解。

### 比较好的changelog的实践？

> 简单而言：yml格式 + [sql-file方式](https://docs.liquibase.com/change-types/sql-file.html)

执行sqlFile格式的changeSet，如下

![](https://www.pdai.tech/images/spring/springboot/springboot-liquibase-7.png)

执行的日志如下

```bash
2022-04-12 21:00:28.198  INFO 17540 --- [           main] liquibase.lockservice                    : Successfully acquired change log lock
2022-04-12 21:00:28.398  INFO 17540 --- [           main] liquibase.changelog                      : Reading from test_db_liquibase.DATABASECHANGELOG
Running Changeset: classpath:/db/changelog/db.changelog-master.yaml::20220412-04::pdai
2022-04-12 21:00:28.516  INFO 17540 --- [           main] liquibase.changelog                      : SQL in file classpath:/db/changelog/db.changelog-20220412-04.sql executed
2022-04-12 21:00:28.516  INFO 17540 --- [           main] liquibase.changelog                      : ChangeSet classpath:/db/changelog/db.changelog-master.yaml::20220412-04::pdai ran successfully in 83ms
2022-04-12 21:00:28.532  INFO 17540 --- [           main] liquibase.lockservice                    : Successfully released change log lock
```

执行后，查看变更记录

![](https://www.pdai.tech/images/spring/springboot/springboot-liquibase-4.png)

数据表user表已经创建并插入一条数据

![](https://www.pdai.tech/images/spring/springboot/springboot-liquibase-5.png)

### 除了addColumn,addTable还有哪些changeType呢？

> 除了addColumn,addTable还有哪些changeType呢?

与此同时，还支持[如下changeType](https://docs.liquibase.com/change-types/home.html)：

![](https://www.pdai.tech/images/spring/springboot/springboot-liquibase-6.png)

此外，还支持执行[command](https://docs.liquibase.com/commands/home.html)

```yaml
changeSet:  
  id:  executeCommand-example  
  author:  liquibase-docs  
  changes:  
  -  executeCommand:  
      args:  
      -  arg:  
          value:  -out  
      -  arg:  
          value:  -param2  
      executable:  mysqldump  
      os:  Windows 7  
      timeout:  10s
```

比如，回滚的操作可以通过如下command进行

![](https://www.pdai.tech/images/spring/springboot/springboot-liquibase-8.png)

再比如，我们可以通过Liquibase来生成相关差异，再制作成changeSet，最后部署。

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos

参考文章

https://docs.liquibase.com