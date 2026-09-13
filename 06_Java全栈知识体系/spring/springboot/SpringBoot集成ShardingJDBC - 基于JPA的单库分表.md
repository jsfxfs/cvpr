# SpringBoot集成ShardingJDBC - 基于JPA的单库分表

> 上文介绍SpringBoot集成基于ShardingJDBC的读写分离实践，本文在此基础上介绍SpringBoot集成基于ShardingJDBC+JPA的单库分表实践。@pdai

## 知识准备

> 主要理解Sharding-JDBC及JPA等。@pdai

- JPA相关 [SpringBoot集成MySQL - 基于JPA的封装](-SpringBoot集成MySQL - 基于JPA的封装.md)
- ShardingJDBC 相关 [SpringBoot集成ShardingJDBC - Sharding-JDBC简介和基于MyBatis的单库分表](-SpringBoot集成ShardingJDBC - Sharding-JDBC简介和基于MyBatis的单库分表.md)

## 简单示例

> 这里主要介绍SpringBoot集成基于ShardingJDBC的**单库分表**实践，主要承接之前的相关文章在JPA的基础上实现的。

### 准备DB和依赖配置

创建MySQL的schema test_db_sharding, 导入SQL 文件如下

```sql
-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: test_db_sharding
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tb_role_0`
--

DROP TABLE IF EXISTS `tb_role_0`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_role_0` (
  `id` bigint NOT NULL,
  `name` varchar(255) NOT NULL,
  `role_key` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_role_0`
--

LOCK TABLES `tb_role_0` WRITE;
/*!40000 ALTER TABLE `tb_role_0` DISABLE KEYS */;
INSERT INTO `tb_role_0` VALUES (3,'333','333','33','2021-09-08 17:09:15','2021-09-08 17:09:15');
/*!40000 ALTER TABLE `tb_role_0` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_role_1`
--

DROP TABLE IF EXISTS `tb_role_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_role_1` (
  `id` bigint NOT NULL,
  `name` varchar(255) NOT NULL,
  `role_key` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_role_1`
--

LOCK TABLES `tb_role_1` WRITE;
/*!40000 ALTER TABLE `tb_role_1` DISABLE KEYS */;
INSERT INTO `tb_role_1` VALUES (1,'admin','admin','admin','2021-09-08 17:09:15','2021-09-08 17:09:15'),(2,'11','11','11','2021-09-08 17:09:15','2021-09-08 17:09:15');
/*!40000 ALTER TABLE `tb_role_1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_user_0`
--

DROP TABLE IF EXISTS `tb_user_0`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_user_0` (
  `id` bigint NOT NULL,
  `user_name` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `email` varchar(45) DEFAULT NULL,
  `phone_number` int DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_user_0`
--

LOCK TABLES `tb_user_0` WRITE;
/*!40000 ALTER TABLE `tb_user_0` DISABLE KEYS */;
INSERT INTO `tb_user_0` VALUES (718415228786159616,'pdai','dad','pdai@pdai.tech',121212121,'pdai','2022-04-06 20:45:38','2022-04-06 20:45:38');
/*!40000 ALTER TABLE `tb_user_0` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_user_1`
--

DROP TABLE IF EXISTS `tb_user_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_user_1` (
  `id` bigint NOT NULL,
  `user_name` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `email` varchar(45) DEFAULT NULL,
  `phone_number` int DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_user_1`
--

LOCK TABLES `tb_user_1` WRITE;
/*!40000 ALTER TABLE `tb_user_1` DISABLE KEYS */;
INSERT INTO `tb_user_1` VALUES (1,'pdai','dfasdf','suzhou.daipeng@gmail.com',1212121213,'afsdfsaf','2021-09-08 17:09:15','2021-09-08 17:09:15'),(718415481409089537,'pdai2','dad2','pdai2@pdai.tech',1212121212,'pdai2','2022-04-06 20:46:38','2022-04-06 20:46:38');
/*!40000 ALTER TABLE `tb_user_1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_user_role_0`
--

DROP TABLE IF EXISTS `tb_user_role_0`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_user_role_0` (
  `id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `role_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_user_role_0`
--

LOCK TABLES `tb_user_role_0` WRITE;
/*!40000 ALTER TABLE `tb_user_role_0` DISABLE KEYS */;
INSERT INTO `tb_user_role_0` VALUES (1,1,1);
/*!40000 ALTER TABLE `tb_user_role_0` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_user_role_1`
--

DROP TABLE IF EXISTS `tb_user_role_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_user_role_1` (
  `id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `role_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_user_role_1`
--

LOCK TABLES `tb_user_role_1` WRITE;
/*!40000 ALTER TABLE `tb_user_role_1` DISABLE KEYS */;
INSERT INTO `tb_user_role_1` VALUES (11,718415481409089537,3),(13,718415228786159616,2);
/*!40000 ALTER TABLE `tb_user_role_1` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-06 23:06:23
```

引入maven依赖, 包含mysql驱动，JPA, 以及sharding-jdbc的依赖。

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
    <groupId>org.apache.shardingsphere</groupId>
    <artifactId>sharding-jdbc-spring-boot-starter</artifactId>
    <version>4.1.1</version>
</dependency>
```

增加yml配置

```yaml
spring:
  shardingsphere:
    datasource:
      names: ds
      ds:
        type: com.zaxxer.hikari.HikariDataSource
        driver-class-name: com.mysql.cj.jdbc.Driver
        jdbc-url: jdbc:mysql://localhost:3306/test_db_sharding?allowPublicKeyRetrieval=true&useSSL=false&autoReconnect=true&characterEncoding=utf8
        username: root
        password: bfXa4Pt2lUUScy8jakXf
    sharding:
      tables:
        tb_user:
          actual-data-nodes: ds.tb_user_$->{0..1}
          table-strategy:
            inline:
              sharding-column: id
              algorithm-expression: tb_user_$->{id % 2}
          key-generator:
            column: id
            type: SNOWFLAKE
            props:
              worker:
                id: 123
        tb_role:
          actual-data-nodes: ds.tb_role_$->{0..1}
          table-strategy:
            inline:
              sharding-column: id
              algorithm-expression: tb_role_$->{id % 2}
          key-generator:
            column: id
            type: SNOWFLAKE
            props:
              worker:
                id: 123
        tb_user_role:
          actual-data-nodes: ds.tb_user_role_$->{0..1}
          table-strategy:
            inline:
              sharding-column: id
              algorithm-expression: tb_user_role_$->{id % 2}
          key-generator:
            column: id
            type: SNOWFLAKE
            props:
              worker:
                id: 123
      binding-tables: tb_user,tb_role,tb_user_role
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

### Entity

user entity

```java
package tech.pdai.springboot.shardingjdbc.jpa.tables.entity;

import java.time.LocalDateTime;
import java.util.Set;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinTable;
import javax.persistence.ManyToMany;
import javax.persistence.Table;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

/**
 * @author pdai
 */
@Getter
@Setter
@ToString
@Entity
@Table(name = "tb_user")
public class User implements BaseEntity {

    /**
     * user id.
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Long id;

    /**
     * username.
     */
    private String userName;

    /**
     * user pwd.
     */
    private String password;

    /**
     * email.
     */
    private String email;

    /**
     * phoneNumber.
     */
    private long phoneNumber;

    /**
     * description.
     */
    private String description;

    /**
     * create date time.
     */
    private LocalDateTime createTime;

    /**
     * update date time.
     */
    private LocalDateTime updateTime;

    /**
     * join to role table.
     */
    @ManyToMany(cascade = {CascadeType.REFRESH}, fetch = FetchType.EAGER)
    @JoinTable(name = "tb_user_role", joinColumns = {
            @JoinColumn(name = "user_id")}, inverseJoinColumns = {@JoinColumn(name = "role_id")})
    private Set<Role> roles;

}
```

role entity

```java
package tech.pdai.springboot.shardingjdbc.jpa.tables.entity;

import java.time.LocalDateTime;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

/**
 * @author pdai
 */
@Getter
@Setter
@ToString
@Entity
@Table(name = "tb_role")
public class Role implements BaseEntity {

    /**
     * role id.
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id", nullable = false)
    private Long id;

    /**
     * role name.
     */
    private String name;

    /**
     * role key.
     */
    private String roleKey;

    /**
     * description.
     */
    private String description;

    /**
     * create date time.
     */
    private LocalDateTime createTime;

    /**
     * update date time.
     */
    private LocalDateTime updateTime;

}
```

### DAO

user dao

```java
package tech.pdai.springboot.shardingjdbc.jpa.tables.dao;

import org.springframework.stereotype.Repository;
import tech.pdai.springboot.shardingjdbc.jpa.tables.entity.User;

/**
 * @author pdai
 */
@Repository
public interface IUserDao extends IBaseDao<User, Long> {

}
```

role dao

```java
package tech.pdai.springboot.shardingjdbc.jpa.tables.dao;

import org.springframework.stereotype.Repository;
import tech.pdai.springboot.shardingjdbc.jpa.tables.entity.Role;

/**
 * @author pdai
 */
@Repository
public interface IRoleDao extends IBaseDao<Role, Long> {

}
```

### Service

user service 接口

```java
package tech.pdai.springboot.shardingjdbc.jpa.tables.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import tech.pdai.springboot.shardingjdbc.jpa.tables.entity.User;
import tech.pdai.springboot.shardingjdbc.jpa.tables.entity.query.UserQueryBean;

/**
 * @author pdai
 */
public interface IUserService extends IBaseService<User, Long> {

    /**
     * find by page.
     *
     * @param userQueryBean query
     * @param pageRequest   pageRequest
     * @return page
     */
    Page<User> findPage(UserQueryBean userQueryBean, PageRequest pageRequest);

}
```

user service 实现类

```java
package tech.pdai.springboot.shardingjdbc.jpa.tables.service.impl;


import com.github.wenhao.jpa.Specifications;
import org.apache.commons.lang3.StringUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import tech.pdai.springboot.shardingjdbc.jpa.tables.dao.IBaseDao;
import tech.pdai.springboot.shardingjdbc.jpa.tables.dao.IUserDao;
import tech.pdai.springboot.shardingjdbc.jpa.tables.entity.User;
import tech.pdai.springboot.shardingjdbc.jpa.tables.entity.query.UserQueryBean;
import tech.pdai.springboot.shardingjdbc.jpa.tables.service.IUserService;

@Service
public class UserDoServiceImpl extends BaseDoServiceImpl<User, Long> implements IUserService {

    /**
     * userDao.
     */
    private final IUserDao userDao;

    /**
     * init.
     *
     * @param userDao2 user dao
     */
    public UserDoServiceImpl(final IUserDao userDao2) {
        this.userDao = userDao2;
    }

    /**
     * @return base dao
     */
    @Override
    public IBaseDao<User, Long> getBaseDao() {
        return this.userDao;
    }

    /**
     * find by page.
     *
     * @param queryBean   query
     * @param pageRequest pageRequest
     * @return page
     */
    @Override
    public Page<User> findPage(UserQueryBean queryBean, PageRequest pageRequest) {
        Specification<User> specification = Specifications.<User>and()
                .like(StringUtils.isNotEmpty(queryBean.getName()), "user_name", queryBean.getName())
                .like(StringUtils.isNotEmpty(queryBean.getDescription()), "description",
                        queryBean.getDescription())
                .build();
        return this.getBaseDao().findAll(specification, pageRequest);
    }

}
```

role service 接口

```java
package tech.pdai.springboot.shardingjdbc.jpa.tables.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import tech.pdai.springboot.shardingjdbc.jpa.tables.entity.Role;
import tech.pdai.springboot.shardingjdbc.jpa.tables.entity.query.RoleQueryBean;

public interface IRoleService extends IBaseService<Role, Long> {

    /**
     * find page by query.
     *
     * @param roleQueryBean query
     * @param pageRequest   pageRequest
     * @return page
     */
    Page<Role> findPage(RoleQueryBean roleQueryBean, PageRequest pageRequest);

}
```

role service 实现类

```java
package tech.pdai.springboot.shardingjdbc.jpa.tables.service.impl;

import com.github.wenhao.jpa.Specifications;
import org.apache.commons.lang3.StringUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import tech.pdai.springboot.shardingjdbc.jpa.tables.dao.IBaseDao;
import tech.pdai.springboot.shardingjdbc.jpa.tables.dao.IRoleDao;
import tech.pdai.springboot.shardingjdbc.jpa.tables.entity.Role;
import tech.pdai.springboot.shardingjdbc.jpa.tables.entity.query.RoleQueryBean;
import tech.pdai.springboot.shardingjdbc.jpa.tables.service.IRoleService;

@Service
public class RoleDoServiceImpl extends BaseDoServiceImpl<Role, Long> implements IRoleService {

    /**
     * roleDao.
     */
    private final IRoleDao roleDao;

    /**
     * init.
     *
     * @param roleDao2 role dao
     */
    public RoleDoServiceImpl(final IRoleDao roleDao2) {
        this.roleDao = roleDao2;
    }

    /**
     * @return base dao
     */
    @Override
    public IBaseDao<Role, Long> getBaseDao() {
        return this.roleDao;
    }

    /**
     * find page by query.
     *
     * @param roleQueryBean query
     * @param pageRequest   pageRequest
     * @return page
     */
    @Override
    public Page<Role> findPage(RoleQueryBean roleQueryBean, PageRequest pageRequest) {
        Specification<Role> specification = Specifications.<Role>and()
                .like(StringUtils.isNotEmpty(roleQueryBean.getName()), "name",
                        roleQueryBean.getName())
                .like(StringUtils.isNotEmpty(roleQueryBean.getDescription()), "description",
                        roleQueryBean.getDescription())
                .build();
        return this.roleDao.findAll(specification, pageRequest);
    }

}
```

### Controller

user controller

```java
package tech.pdai.springboot.shardingjdbc.jpa.tables.controller;


import java.time.LocalDateTime;

import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import tech.pdai.springboot.shardingjdbc.jpa.tables.entity.User;
import tech.pdai.springboot.shardingjdbc.jpa.tables.entity.query.UserQueryBean;
import tech.pdai.springboot.shardingjdbc.jpa.tables.entity.response.ResponseResult;
import tech.pdai.springboot.shardingjdbc.jpa.tables.service.IUserService;

/**
 * @author pdai
 */
@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private IUserService userService;

    /**
     * @param user user param
     * @return user
     */
    @ApiOperation("Add/Edit User")
    @PostMapping("add")
    public ResponseResult<User> add(User user) {
        if (user.getId()==null || !userService.exists(user.getId())) {
            user.setCreateTime(LocalDateTime.now());
            user.setUpdateTime(LocalDateTime.now());
            userService.save(user);
        } else {
            user.setUpdateTime(LocalDateTime.now());
            userService.update(user);
        }
        return ResponseResult.success(userService.find(user.getId()));
    }


    /**
     * @return user list
     */
    @ApiOperation("Query User One")
    @GetMapping("edit/{userId}")
    public ResponseResult<User> edit(@PathVariable("userId") Long userId) {
        return ResponseResult.success(userService.find(userId));
    }

    /**
     * @return user list
     */
    @ApiOperation("Query User Page")
    @GetMapping("list")
    public ResponseResult<Page<User>> list(@RequestParam int pageSize, @RequestParam int pageNumber) {
        return ResponseResult.success(userService.findPage(UserQueryBean.builder().build(), PageRequest.of(pageNumber, pageSize)));
    }
}
```

### 简单测试

访问页面：

http://localhost:8080/doc.html

插入数据

![](https://www.pdai.tech/images/spring/springboot/spring-sharding-5.png)

查询数据

![](https://www.pdai.tech/images/spring/springboot/spring-sharding-6.png)

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos