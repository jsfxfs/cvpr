# ▶SpringBoot集成MySQL - 基于JPA的封装

> 在实际开发中，最为常见的是基于数据库的CRUD封装等，比如SpringBoot集成MySQL数据库，常用的方式有JPA和MyBatis； 本文主要介绍基于JPA方式的基础封装思路。@pdai

## 知识准备

> 需要对MySQL，JPA以及接口封装有了解。

### MySQL相关

- [数据库基础和SQL知识体系详解](../../db/sql/♥数据库基础和SQL知识体系详解♥.md)
- [MySQL知识体系详解](../../db/sql-mysql/♥MySQL知识体系详解♥.md)

### JPA相关

- [SpringBoot入门 - 添加内存数据库H2](SpringBoot入门 - 添加内存数据库H2.md)

### 接口相关

- [SpringBoot接口 - 如何统一接口封装](-SpringBoot接口 - 如何统一接口封装.md)
  - 在以SpringBoot开发Restful接口时，统一返回方便前端进行开发和封装，以及出现时给出响应编码和信息。
- [SpringBoot接口 - 如何对参数进行校验](SpringBoot接口 - 如何对参数进行校验.md)
  - 在以SpringBoot开发Restful接口时, 对于接口的查询参数后台也是要进行校验的，同时还需要给出校验的返回信息放到上文我们统一封装的结构中。那么如何优雅的进行参数的统一校验呢？
- [SpringBoot接口 - 如何参数校验国际化](SpringBoot接口 - 如何参数校验国际化.md)
  - 上文我们学习了如何对SpringBoot接口进行参数校验，但是如果需要有国际化的信息，应该如何优雅处理呢？
- [SpringBoot接口 - 如何统一异常处理](SpringBoot接口 - 如何统一异常处理.md)
  - SpringBoot接口如何对异常进行统一封装，并统一返回呢？以上文的参数校验为例，如何优雅的将参数校验的错误信息统一处理并封装返回呢？
- [SpringBoot接口 - 如何提供多个版本接口](SpringBoot接口 - 如何提供多个版本接口.md)
  - 在以SpringBoot开发Restful接口时，由于模块，系统等业务的变化，需要对同一接口提供不同版本的参数实现（老的接口还有模块或者系统在用，不能直接改，所以需要不同版本）。如何更加优雅的实现多版本接口呢？
- [SpringBoot接口 - 如何生成接口文档](SpringBoot接口 - 如何生成接口文档之Swagger技术栈.md)
  - SpringBoot开发Restful接口，有什么API规范吗？如何快速生成API文档呢？
- [SpringBoot接口 - 如何访问外部接口](SpringBoot接口 - 如何访问外部接口.md)
  - 在SpringBoot接口开发中，存在着本模块的代码需要访问外面模块接口或外部url链接的需求, 比如调用外部的地图API或者天气API。那么有哪些方式可以调用外部接口呢？
- [SpringBoot接口 - 如何对接口进行加密](SpringBoot接口 - 如何对接口进行签名.md)
  - 在以SpringBoot开发后台API接口时，会存在哪些接口不安全的因素呢？通常如何去解决的呢？本文主要介绍API**接口有不安全的因素**以及**常见的保证接口安全的方式**，重点**实践如何对接口进行签名**。
- [SpringBoot接口 - 如何保证接口幂等](SpringBoot接口 - 如何保证接口幂等.md)
  - 在以SpringBoot开发Restful接口时，如何防止接口的重复提交呢？ 本文主要介绍接口幂等相关的知识点，并实践常见基于Token实现接口幂等。
- [SpringBoot接口 - 如何实现接口限流之单实例](SpringBoot接口 - 如何实现接口限流之单实例.md)
  - 在以SpringBoot开发Restful接口时，当流量超过服务极限能力时，系统可能会出现卡死、崩溃的情况，所以就有了降级和限流。在接口层如何做限流呢？ 本文主要回顾限流的知识点，并实践单实例限流的一种思路。
- [SpringBoot接口 - 如何实现接口限流之分布式](SpringBoot接口 - 如何实现接口限流之分布式.md)
  - 上文中介绍了单实例下如何在业务接口层做限流，本文主要介绍分布式场景下限流的方案，以及什么样的分布式场景下需要在业务层加限流而不是接入层; 并且结合kailing开源的[ratelimiter-spring-boot-starter](https://gitee.com/kailing/ratelimiter-spring-boot-starter)为例， 学习**思路+代码封装+starter封装**。

## 实现案例

> 本例主要简单示例下基于JPA DAO/Service层封装， 并且注意下如下例子MySQL是5.7版本，8.x版本相关例子也在[示例源码](https://github.com/realpdai/tech-pdai-spring-demos)中。

### 准备DB

创建MySQL的schema test_db, 导入SQL 文件如下

```sql
-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: localhost    Database: test_db
-- ------------------------------------------------------
-- Server version	5.7.17-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tb_role`
--

DROP TABLE IF EXISTS `tb_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `role_key` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_role`
--

LOCK TABLES `tb_role` WRITE;
/*!40000 ALTER TABLE `tb_role` DISABLE KEYS */;
INSERT INTO `tb_role` VALUES (1,'admin','admin','admin','2021-09-08 17:09:15','2021-09-08 17:09:15');
/*!40000 ALTER TABLE `tb_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_user`
--

DROP TABLE IF EXISTS `tb_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `email` varchar(45) DEFAULT NULL,
  `phone_number` int(11) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_user`
--

LOCK TABLES `tb_user` WRITE;
/*!40000 ALTER TABLE `tb_user` DISABLE KEYS */;
INSERT INTO `tb_user` VALUES (1,'pdai','dfasdf','suzhou.daipeng@gmail.com',1212121213,'afsdfsaf','2021-09-08 17:09:15','2021-09-08 17:09:15');
/*!40000 ALTER TABLE `tb_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_user_role`
--

DROP TABLE IF EXISTS `tb_user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_user_role` (
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_user_role`
--

LOCK TABLES `tb_user_role` WRITE;
/*!40000 ALTER TABLE `tb_user_role` DISABLE KEYS */;
INSERT INTO `tb_user_role` VALUES (1,1);
/*!40000 ALTER TABLE `tb_user_role` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-09-08 17:12:11
```

引入maven依赖

```java
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.47</version>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<!-- jpa-spec --->
<dependency>
    <groupId>com.github.wenhao</groupId>
    <artifactId>jpa-spec</artifactId>
    <version>3.1.0</version>
</dependency>
```

增加yml配置

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/test_db?useSSL=false&autoReconnect=true&characterEncoding=utf8
    driver-class-name: com.mysql.jdbc.Driver
    username: root
    password: xxxxxxxxx
    initial-size: 20
    max-idle: 60
    max-wait: 10000
    min-idle: 10
    max-active: 200
  jpa:
    generate-ddl: false
    show-sql: false
    properties:
      hibernate:
        dialect: org.hibernate.dialect.MySQLDialect
        format_sql: true
        use-new-id-generator-mappings: false
```

### 定义实体

> USER/ROLE

BaseEntity

```java
package tech.pdai.springboot.mysql57.jpa.entity;

import java.io.Serializable;

/**
 * @author pdai
 */
public interface BaseEntity extends Serializable {
}
```

User

```java
package tech.pdai.springboot.mysql57.jpa.entity;

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

Role

```java
package tech.pdai.springboot.mysql57.jpa.entity;

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

### DAO层

BaseDao

```java
package tech.pdai.springboot.mysql57.jpa.dao;

import java.io.Serializable;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.repository.NoRepositoryBean;
import tech.pdai.springboot.mysql57.jpa.entity.BaseEntity;

/**
 * @author pdai
 */
@NoRepositoryBean
public interface IBaseDao<T extends BaseEntity, I extends Serializable>
        extends JpaRepository<T, I>, JpaSpecificationExecutor<T> {
}
```

UserDao

```java
package tech.pdai.springboot.mysql57.jpa.dao;

import org.springframework.stereotype.Repository;
import tech.pdai.springboot.mysql57.jpa.entity.User;

/**
 * @author pdai
 */
@Repository
public interface IUserDao extends IBaseDao<User, Long> {

}
```

RoleDao

```java
package tech.pdai.springboot.mysql57.jpa.dao;

import org.springframework.stereotype.Repository;
import tech.pdai.springboot.mysql57.jpa.entity.Role;

/**
 * @author pdai
 */
@Repository
public interface IRoleDao extends IBaseDao<Role, Long> {

}
```

### Service层

#### BaseService

封装BaseService

```java
package tech.pdai.springboot.mysql57.jpa.service;

import java.io.Serializable;
import java.util.List;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.domain.Specification;

/**
 * @author pdai
 */
public interface IBaseService<T, I extends Serializable> {

    /**
     * @param id id
     * @return T
     */
    T find(I id);

    /**
     * @return List
     */
    List<T> findAll();

    /**
     * @param ids ids
     * @return List
     */
    List<T> findList(I[] ids);

    /**
     * @param ids ids
     * @return List
     */
    List<T> findList(Iterable<I> ids);

    /**
     * @param pageable pageable
     * @return Page
     */
    Page<T> findAll(Pageable pageable);

    /**
     * @param spec     spec
     * @param pageable pageable
     * @return Page
     */
    Page<T> findAll(Specification<T> spec, Pageable pageable);

    /**
     * @param spec spec
     * @return T
     */
    T findOne(Specification<T> spec);

    /**
     * count.
     *
     * @return long
     */
    long count();

    /**
     * count.
     *
     * @param spec spec
     * @return long
     */
    long count(Specification<T> spec);

    /**
     * exists.
     *
     * @param id id
     * @return boolean
     */
    boolean exists(I id);

    /**
     * save.
     *
     * @param entity entity
     */
    void save(T entity);

    /**
     * save.
     *
     * @param entities entities
     */
    void save(List<T> entities);

    /**
     * update.
     *
     * @param entity entity
     * @return T
     */
    T update(T entity);

    /**
     * delete.
     *
     * @param id id
     */
    void delete(I id);

    /**
     * delete by ids.
     *
     * @param ids ids
     */
    void deleteByIds(List<I> ids);

    /**
     * delete.
     *
     * @param entities entities
     */
    void delete(T[] entities);

    /**
     * delete.
     *
     * @param entities entities
     */
    void delete(Iterable<T> entities);

    /**
     * delete.
     *
     * @param entity entity
     */
    void delete(T entity);

    /**
     * delete all.
     */
    void deleteAll();

    /**
     * find list.
     *
     * @param spec spec
     * @return list
     */
    List<T> findList(Specification<T> spec);

    /**
     * find list.
     *
     * @param spec spec
     * @param sort sort
     * @return List
     */
    List<T> findList(Specification<T> spec, Sort sort);


    /**
     * flush.
     */
    void flush();

}
```

BaseService实现类

```java
package tech.pdai.springboot.mysql57.jpa.service.impl;

import java.io.Serializable;
import java.util.Arrays;
import java.util.List;

import javax.transaction.Transactional;

import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.domain.Specification;
import tech.pdai.springboot.mysql57.jpa.dao.IBaseDao;
import tech.pdai.springboot.mysql57.jpa.entity.BaseEntity;
import tech.pdai.springboot.mysql57.jpa.service.IBaseService;

/**
 * @author pdai
 */
@Slf4j
@Transactional
public abstract class BaseDoServiceImpl<T extends BaseEntity, I extends Serializable> implements IBaseService<T, I> {

    /**
     * @return IBaseDao
     */
    public abstract IBaseDao<T, I> getBaseDao();

    /**
     * findById.
     *
     * @param id id
     * @return T
     */
    @Override
    public T find(I id) {
        return getBaseDao().findById(id).orElse(null);
    }

    /**
     * @return List
     */
    @Override
    public List<T> findAll() {
        return getBaseDao().findAll();
    }

    /**
     * @param ids ids
     * @return List
     */
    @Override
    public List<T> findList(I[] ids) {
        List<I> idList = Arrays.asList(ids);
        return getBaseDao().findAllById(idList);
    }

    /**
     * find list.
     *
     * @param spec spec
     * @return list
     */
    @Override
    public List<T> findList(Specification<T> spec) {
        return getBaseDao().findAll(spec);
    }

    /**
     * find list.
     *
     * @param spec spec
     * @param sort sort
     * @return List
     */
    @Override
    public List<T> findList(Specification<T> spec, Sort sort) {
        return getBaseDao().findAll(spec, sort);
    }

    /**
     * find one.
     *
     * @param spec spec
     * @return T
     */
    @Override
    public T findOne(Specification<T> spec) {
        return getBaseDao().findOne(spec).orElse(null);
    }

    /**
     * @param pageable pageable
     * @return Page
     */
    @Override
    public Page<T> findAll(Pageable pageable) {
        return getBaseDao().findAll(pageable);
    }

    /**
     * count.
     *
     * @return long
     */
    @Override
    public long count() {
        return getBaseDao().count();
    }

    /**
     * count.
     *
     * @param spec spec
     * @return long
     */
    @Override
    public long count(Specification<T> spec) {
        return getBaseDao().count(spec);
    }

    /**
     * exists.
     *
     * @param id id
     * @return boolean
     */
    @Override
    public boolean exists(I id) {
        return getBaseDao().findById(id).isPresent();
    }

    /**
     * save.
     *
     * @param entity entity
     */
    @Override
    public void save(T entity) {
        getBaseDao().save(entity);
    }

    /**
     * save.
     *
     * @param entities entities
     */
    @Override
    public void save(List<T> entities) {
        getBaseDao().saveAll(entities);
    }

    /**
     * update.
     *
     * @param entity entity
     * @return T
     */
    @Override
    public T update(T entity) {
        return getBaseDao().saveAndFlush(entity);
    }

    /**
     * delete.
     *
     * @param id id
     */
    @Override
    public void delete(I id) {
        getBaseDao().deleteById(id);
    }

    /**
     * delete by ids.
     *
     * @param ids ids
     */
    @Override
    public void deleteByIds(List<I> ids) {
        getBaseDao().deleteAllById(ids);
    }

    /**
     * delete all.
     */
    @Override
    public void deleteAll() {
        getBaseDao().deleteAllInBatch();
    }

    /**
     * delete.
     *
     * @param entities entities
     */
    @Override
    public void delete(T[] entities) {
        List<T> tList = Arrays.asList(entities);
        getBaseDao().deleteAll(tList);
    }

    /**
     * delete.
     *
     * @param entities entities
     */
    @Override
    public void delete(Iterable<T> entities) {
        getBaseDao().deleteAll(entities);
    }

    /**
     * delete.
     *
     * @param entity entity
     */
    @Override
    public void delete(T entity) {
        getBaseDao().delete(entity);
    }

    /**
     * @param ids ids
     * @return List
     */
    @Override
    public List<T> findList(Iterable<I> ids) {
        return getBaseDao().findAllById(ids);
    }

    /**
     * @param spec     spec
     * @param pageable pageable
     * @return Page
     */
    @Override
    public Page<T> findAll(Specification<T> spec, Pageable pageable) {
        return getBaseDao().findAll(spec, pageable);
    }

    /**
     * flush.
     */
    @Override
    public void flush() {
        getBaseDao().flush();
    }

}
```

#### UserService

UserService接口定义

```java
package tech.pdai.springboot.mysql57.jpa.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import tech.pdai.springboot.mysql57.jpa.entity.query.UserQueryBean;
import tech.pdai.springboot.mysql57.jpa.entity.User;

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

UserService实现类

```java
package tech.pdai.springboot.mysql57.jpa.service.impl;


import com.github.wenhao.jpa.Specifications;
import org.apache.commons.lang3.StringUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import tech.pdai.springboot.mysql57.jpa.dao.IBaseDao;
import tech.pdai.springboot.mysql57.jpa.dao.IUserDao;
import tech.pdai.springboot.mysql57.jpa.entity.User;
import tech.pdai.springboot.mysql57.jpa.entity.query.UserQueryBean;
import tech.pdai.springboot.mysql57.jpa.service.IUserService;

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

#### RoleService

RoleService接口定义

```java
package tech.pdai.springboot.mysql57.jpa.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import tech.pdai.springboot.mysql57.jpa.entity.Role;
import tech.pdai.springboot.mysql57.jpa.entity.query.RoleQueryBean;

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

RoleService实现类

```java
package tech.pdai.springboot.mysql57.jpa.service.impl;

import com.github.wenhao.jpa.Specifications;
import org.apache.commons.lang3.StringUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import tech.pdai.springboot.mysql57.jpa.dao.IBaseDao;
import tech.pdai.springboot.mysql57.jpa.dao.IRoleDao;
import tech.pdai.springboot.mysql57.jpa.entity.Role;
import tech.pdai.springboot.mysql57.jpa.entity.query.RoleQueryBean;
import tech.pdai.springboot.mysql57.jpa.service.IRoleService;

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

### Controller层

UserController

```java
package tech.pdai.springboot.mysql57.jpa.controller;


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
import tech.pdai.springboot.mysql57.jpa.entity.User;
import tech.pdai.springboot.mysql57.jpa.entity.query.UserQueryBean;
import tech.pdai.springboot.mysql57.jpa.entity.response.ResponseResult;
import tech.pdai.springboot.mysql57.jpa.service.IUserService;

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

### 运行测试

查询一个

![](https://www.pdai.tech/images/spring/springboot/springboot-mysql57-jpa-1.png)

查询分页列表

![](https://www.pdai.tech/images/spring/springboot/springboot-mysql57-jpa-2.png)

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos