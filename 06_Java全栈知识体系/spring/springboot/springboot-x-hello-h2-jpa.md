# SpringBoot入门 - 添加内存数据库H2

> 上文我们展示了通过学习经典的MVC分包结构展示了一个用户的增删查改项目，但是我们没有接入数据库；本文将在上文的基础上，增加一个H2内存数据库，并且通过Spring 提供的数据访问包JPA进行数据查询。@pdai

## 准备知识点

> 在介绍通过Spring JPA接入真实H2数据时，需要首先了解下：
>
> 1. 什么是H2数据库？
> 2. 什么是JPA？

### 什么是H2内存数据库

> H2是一个用Java开发的嵌入式数据库，它本身只是一个类库，可以直接嵌入到应用项目中。

[官方网站](http://www.h2database.com/html/main.html)

![](https://www.pdai.tech/images/spring/springboot/springboot-hello-h2-1.png)

**有哪些用途**？

- H2最大的用途在于可以同应用程序打包在一起发布，这样可以非常方便地存储少量结构化数据。
- 它的另一个用途是**用于单元测试**。启动速度快，而且可以关闭持久化功能，每一个用例执行完随即还原到初始状态。
- H2的第三个用处是作为缓存，作为NoSQL的一个补充。当某些场景下数据模型必须为关系型，可以拿它当Memcached使，作为后端MySQL/Oracle的一个缓冲层，缓存一些不经常变化但需要频繁访问的数据，比如字典表、权限表。不过这样系统架构就会比较复杂了。

**H2的产品优势**?

- 纯Java编写，不受平台的限制；
- 只有一个jar文件，适合作为嵌入式数据库使用；
- h2提供了一个十分方便的web控制台用于操作和管理数据库内容；
- 功能完整，支持标准SQL和JDBC。麻雀虽小五脏俱全；
- 支持内嵌模式、服务器模式和集群。

### 什么是JPA，和JDBC是什么关系

> 什么是JDBC, ORM, JPA? 之间的关系是什么？

- **什么是JDBC**

JDBC（JavaDataBase Connectivity）就是Java数据库连接，说白了就是用Java语言来操作数据库。原来我们操作数据库是在控制台使用SQL语句来操作数据库，JDBC是用Java语言向数据库发送SQL语句。

![](https://www.pdai.tech/images/project/project-b-4.png)

- **什么是ORM**

对象关系映射（Object Relational Mapping，简称ORM）， 简单的说，**ORM是通过使用描述对象和数据库之间映射的元数据，将java程序中的对象自动持久化到关系数据库中**。本质上就是将数据从一种形式转换到另外一种形式，具体如下：

![](https://www.pdai.tech/images/project/project-b-3.png)

具体映射：

1. 数据库的表（table） --> 类（class）
2. 记录（record，行数据）--> 对象（object）
3. 字段（field）--> 对象的属性（attribute）

- **什么是JPA**

JPA是Spring提供的一种ORM，首先让我们回顾下Spring runtime体系：

![](https://www.pdai.tech/images/db/mongo/mongo-x-usage-spring-4.png)

Spring Data是基于Spring runtime体系的，JPA 属于Spring Data, 和JDBC的关系如下：

![](https://www.pdai.tech/images/db/mongo/mongo-x-usage-spring-5.png)

## 案例

> 这里承接上文， 使用H2存放用户表，并通过JPA操作用户数据。

### 添加H2和JPA的依赖

```xml
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>runtime</scope>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
```

### 配置H2和JPA注入参数

```yaml
spring:
  datasource:
    data: classpath:db/data.sql
    driverClassName: org.h2.Driver
    password: sa
    platform: h2
    schema: classpath:db/schema.sql
    url: jdbc:h2:mem:dbtest
    username: sa
  h2:
    console:
      enabled: true
      path: /h2
      settings:
        web-allow-others: true
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
```

其中资源下还需要配置数据库的表结构schema.sql

```sql
create table if not exists tb_user (
USER_ID int not null primary key auto_increment,
USER_NAME varchar(100)
);
```

以及数据文件 data.sql, 默认插入一条‘赵一’的数据

```sql
INSERT INTO tb_user (USER_ID,USER_NAME) VALUES(1,'赵一');
```

### 实体关联表

给User添加@Entity注解，和@Table注解

```java
package tech.pdai.springboot.h2.entity;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "tb_user")
public class User {

    @Id
    private int userId;
    private String userName;

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }
}
```

### Dao继承JpaRepository

```java
package tech.pdai.springboot.h2.dao;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import tech.pdai.springboot.h2.entity.User;

@Repository
public interface UserRepository extends JpaRepository<User, Integer> {

}
```

(其它service,App启动类等代码和前文一致)

### 运行程序

![](https://www.pdai.tech/images/spring/springboot/springboot-hello-mvc-4.png)

## 一些思考

> 这里补充一些H2数据库的知识点（特别是如何用H2做单元测试）， 可以跳过。

### H2数据库通常如何使用？

- **嵌入式模式** （上文例子）

在嵌入式模式下，应用程序使用JDBC从同一JVM中打开数据库。这是最快也是最容易的连接方式。缺点是数据库可能只在任何时候在一个虚拟机（和类加载器）中打开。与所有模式一样，支持持久性和内存数据库。对并发打开数据库的数量或打开连接的数量没有限制。

![](https://www.pdai.tech/images/spring/springboot/springboot-hello-h2-2.png)

- **服务器模式**

当使用服务器模式（有时称为远程模式或客户机/服务器模式）时，应用程序使用 JDBC 或 ODBC API 远程打开数据库。服务器需要在同一台或另一台虚拟机上启动，或者在另一台计算机上启动。许多应用程序可以通过连接到这个服务器同时连接到同一个数据库。在内部，服务器进程在嵌入式模式下打开数据库。

服务器模式比嵌入式模式慢，因为所有数据都通过TCP/IP传输。与所有模式一样，支持持久性和内存数据库。对每个服务器并发打开的数据库数量或打开连接的数量没有限制。

![](https://www.pdai.tech/images/spring/springboot/springboot-hello-h2-3.png)

- **混合模式**

混合模式是嵌入式和服务器模式的结合。连接到数据库的第一个应用程序在嵌入式模式下运行，但也启动服务器，以便其他应用程序（在不同进程或虚拟机中运行）可以同时访问相同的数据。本地连接的速度与数据库在嵌入式模式中的使用速度一样快，而远程连接速度稍慢。

服务器可以从应用程序内（使用服务器API）启动或停止，或自动（自动混合模式）。当使用自动混合模式时，所有想要连接到数据库的客户端（无论是本地连接还是远程连接）都可以使用完全相同的数据库URL来实现。

![](https://www.pdai.tech/images/spring/springboot/springboot-hello-h2-4.png)

以上不同的连接方式对应不同的 JDBC URL，可以参考如下附录表格中的连接格式。

### 如何使用H2做单元测试？

为何H2会被用来做单元测试 以及 如何使用H2做单元测试？

可以参考这篇文章 [单元测试 - SpringBoot2+Mockito实战](../../develop/ut/dev-ut-springboot2.md)

### H2数据库的兼容性？

H2会被用作单元测试的模拟库，所以必然也需要了解H2数据库的兼容性。

h2官网对此有[详细的描述](http://www.h2database.com/html/features.html#compatibility)

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos

## 参考文章

https://www.jianshu.com/p/0288242ee2cb

https://www.cnblogs.com/cnjavahome/p/8995650.html