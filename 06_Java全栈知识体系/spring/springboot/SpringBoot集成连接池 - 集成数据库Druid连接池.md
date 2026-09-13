# SpringBoot集成连接池 - 集成数据库Druid连接池

> 上文介绍默认数据库连接池HikariCP，本文主要介绍SpringBoot集成阿里的Druid连接池的实践; 客观的来说，阿里Druid只能说是中文开源中功能全且广泛的连接池为基础的监控组件，但是（仅从连接池的角度）在生态，维护性，开源规范性，综合性能等方面和HikariCP比还是有很大差距。 @pdai

## 知识准备

> 了解Druid连接池。

### Druid连接池的定位？

> Druid连接池是阿里巴巴开源的数据库连接池项目。Druid连接池**为监控而生**，内置强大的监控功能，监控特性不影响性能。功能强大，能防SQL注入，内置Loging能诊断Hack应用行为。

- Github项目地址 https://github.com/alibaba/druid
- 文档 https://github.com/alibaba/druid/wiki/%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98
- 下载 http://repo1.maven.org/maven2/com/alibaba/druid/
- 监控DEMO http://120.26.192.168/druid/index.html

（更多功能请看后续文章）

## 简单示例

> 本示例主要展示SpringBoot2 和 Druid CP的集成，并在[SpringBoot集成MySQL - 基于JPA的封装](-SpringBoot集成MySQL - 基于JPA的封装.md)基础增加Druid而成。

### POM配置

增加依赖

```xml
<!-- https://mvnrepository.com/artifact/com.alibaba/druid-spring-boot-starter -->
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>druid-spring-boot-starter</artifactId>
    <version>1.2.9</version>
</dependency>
```

### yml配置

详细的yml配置如下：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/test_db?useSSL=false&autoReconnect=true&characterEncoding=utf8
    driver-class-name: com.mysql.cj.jdbc.Driver
    username: root
    password: bfXa4Pt2lUUScy8jakXf
    # Druid datasource
    type: com.alibaba.druid.pool.DruidDataSource
    druid:
      # 初始化大小
      initial-size: 5
      # 最小连接数
      min-idle: 10
      # 最大连接数
      max-active: 20
      # 获取连接时的最大等待时间
      max-wait: 60000
      # 一个连接在池中最小生存的时间，单位是毫秒
      min-evictable-idle-time-millis: 300000
      # 多久才进行一次检测需要关闭的空闲连接，单位是毫秒
      time-between-eviction-runs-millis: 60000
      # 配置扩展插件：stat-监控统计，log4j-日志，wall-防火墙（防止SQL注入），去掉后，监控界面的sql无法统计
      filters: stat,wall
      # 检测连接是否有效的 SQL语句，为空时以下三个配置均无效
      validation-query: SELECT 1
      # 申请连接时执行validationQuery检测连接是否有效，默认true，开启后会降低性能
      test-on-borrow: true
      # 归还连接时执行validationQuery检测连接是否有效，默认false，开启后会降低性能
      test-on-return: true
      # 申请连接时如果空闲时间大于timeBetweenEvictionRunsMillis，执行validationQuery检测连接是否有效，默认false，建议开启，不影响性能
      test-while-idle: true
      # 是否开启 StatViewServlet
      stat-view-servlet:
        enabled: true
        # 访问监控页面 白名单，默认127.0.0.1
        allow: 127.0.0.1
        login-username: admin
        login-password: admin
      # FilterStat
      filter:
        stat:
          # 是否开启 FilterStat，默认true
          enabled: true
          # 是否开启 慢SQL 记录，默认false
          log-slow-sql: true
          # 慢 SQL 的标准，默认 3000，单位：毫秒
          slow-sql-millis: 5000
          # 合并多个连接池的监控数据，默认false
          merge-sql: false
  jpa:
    open-in-view: false
    generate-ddl: false
    show-sql: false
    properties:
      hibernate:
        dialect: org.hibernate.dialect.MySQLDialect
        format_sql: true
        use-new-id-generator-mappings: false
```

更多的配置，请参考[官方配置](https://github.com/alibaba/druid/wiki/DruidDataSource%E9%85%8D%E7%BD%AE%E5%B1%9E%E6%80%A7%E5%88%97%E8%A1%A8)

### 测试

访问http://localhost:8080/druid/datasource.html

admin/admin登录

![](https://www.pdai.tech/images/spring/springboot/springboot-druid-11.png)

访问接口，进行SQL查询

![](https://www.pdai.tech/images/spring/springboot/springboot-druid-12.png)

SQL和慢查询监控

![](https://www.pdai.tech/images/spring/springboot/springboot-druid-13.png)

## 进一步理解

> 进一步理解下阿里的Druid。

### 更多功能等

> Druid连接池最初就是为监控系统采集jdbc运行信息而生的，它内置了StatFilter 功能，能采集非常完备的连接池执行信息Druid连接池内置了能和Spring/Servlet关联监控的实现，使得监控Web应用特别方便Druid连接池内置了一个监控页面，提供了非常完备的监控信息，可以快速诊断系统的瓶颈。更多请参考：Druid 的GitHub仓库[wiki](https://github.com/alibaba/druid/wiki/%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98)

#### 监控信息采集的StatFilter

Druid连接池的监控信息主要是通过StatFilter 采集的，采集的信息非常全面，包括SQL执行、并发、慢查、执行时间区间分布等。具体配置可以看这个 https://github.com/alibaba/druid/wiki/%E9%85%8D%E7%BD%AE_StatFilter

- **监控不影响性能**

Druid增加StatFilter之后，能采集大量统计信息，同时对性能基本没有影响。StatFilter对CPU和内存的消耗都极小，对系统的影响可以忽略不计。监控不影响性能是Druid连接池的重要特性。

- **SQL参数化合并监控**

实际业务中，如果SQL不是走PreparedStatement，SQL没有参数化，这时SQL需要参数化合并监控才能真实反映业务情况。如下SQL：

```sql
select * from t where id = 1
select * from t where id = 2
select * from t where id = 3
```

参数化后：

```sql
select * from t where id = ?
```

参数化合并监控是基于SQL Parser语法解析实现的，是Druid连接池独一无二的功能。

- **执行次数、返回行数、更新行数和并发监控**

StatFilter能采集到每个SQL的执行次数、返回行数总和、更新行数总和、执行中次数和和最大并发。并发监控的统计是在SQL执行开始对计数器加一，结束后对计数器减一实现的。可以采集到每个SQL的当前并发和采集期间的最大并发。

- **慢查监控**

缺省执行耗时超过3秒的被认为是慢查，统计项中有包括每个SQL的最后发生的慢查的耗时和发生时的参数。

- **Exception监控**

如果SQL执行时抛出了Exception，SQL统计项上会Exception有最后的发生时间、堆栈和Message，根据这些信息可以很容易定位错误原因。

#### 诊断支持

Druid连接池内置了LogFilter，将Connection/Statement/ResultSet相关操作的日志输出，可以用于诊断系统问题，也可以用于Hack一个不熟悉的系统。

LogFilter可以输出连接申请/释放，事务提交回滚，Statement的Create/Prepare/Execute/Close，ResultSet的Open/Next/Close，通过LogFilter可以详细诊断一个系统的Jdbc行为。

LogFilter有Log4j、Log4j2、Slf4j、CommsLog等实现，具体配置看这里 https://github.com/alibaba/druid/wiki/%E9%85%8D%E7%BD%AE_LogFilter

#### 防SQL注入

SQL注入攻击是黑客对数据库进行攻击的常用手段，Druid连接池内置了WallFilter 提供防SQL注入功能，在不影响性能的同时防御SQL注入攻击。

- **基于语意的防SQL注入**

Druid连接池内置了一个功能完备的SQL Parser，能够完整解析mysql、sql server、oracle、postgresql的语法，通过语意分析能够精确识别SQL注入攻击。

- **极低的漏报率和误报率**

基于SQL语意分析，大量应用和反馈，使得Druid的防SQL注入拥有极低的漏报率和误报率。

- **防注入对性能影响极小**

内置参数化后的Cache、高性能手写的Parser，使得打开防SQL注入对应用的性能基本不受影响。

### 如何评价阿里的Druid连接池

> **客观的来说**，阿里Druid只能说是中文开源中功能全且广泛的连接池为基础的监控组件，但是（仅从连接池的角度）在生态，维护性，开源规范性，综合性能等方面和HikariCP比还是有很大差距。（**以下是pdai本人观点，对国产开源并没偏见**！）。

首先，仅从[功能](https://github.com/alibaba/druid/wiki/Druid%E8%BF%9E%E6%8E%A5%E6%B1%A0%E4%BB%8B%E7%BB%8D)上看，Druid并不是一个存粹的连接池，它还承载了监控，诊断，安全的功能。从产品的角度看，all in one 也是有代价的，如果我只期望使用连接池的功能，其它的功能对于使用者来说就是鸡肋；而我们没有看到其长期架构设计（比如插拔式架构，分包设计等）， 大概率是当时Druid这种开源的驱动方式并不是一个完善规范的开源软件开发方式（比如KPI driven和个人主义色彩)

（如果你仅仅从功能上比较，你就已经输了，因为这种比较根本不在一个维度上；看到druid主要作者wenshao和hikari作者的[讨论](https://github.com/brettwooldridge/HikariCP/issues/232)，读者自行辨别~）

![](https://www.pdai.tech/images/spring/springboot/springboot-druid-1.png)

文档的规范性，发包规范性，bug修复，生态构建等方面国产开源在那时（当下及未来一段时间）还有很长的路要走。

来看看相关Isusse，2k多个issues哈，没有专职维护（图中Spring的高危漏洞无人修正）

![](https://www.pdai.tech/images/spring/springboot/springboot-druid-2.png)

源代码中当前版本是1.2.8，实际版本

![](https://www.pdai.tech/images/spring/springboot/springboot-druid-3.png)

实际mvn repo中已经是1.2.9

![](https://www.pdai.tech/images/spring/springboot/springboot-druid-4.png)

再看wiki，有些链接居然是空的...

![](https://www.pdai.tech/images/spring/springboot/springboot-druid-6.png)

最新的Springboot-starter中SpringBoot还是1.5.12-RELEASE版本，先不说没有支持SpringBoot 2.x版本；高危漏洞无人持续维护，对于开发者而言就是坑(不禁让我又想起了FastJson，说多了都是泪)！

![](https://www.pdai.tech/images/spring/springboot/springboot-druid-5.png)

此外，广告都加到UI上了（KPI压力？）

![](https://www.pdai.tech/images/spring/springboot/springboot-druid-8.png)

只能说，国产开源在还有很长的路要走！

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos