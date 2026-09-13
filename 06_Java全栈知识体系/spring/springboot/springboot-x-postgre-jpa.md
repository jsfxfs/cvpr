# ▶SpringBoot集成PostgreSQL - 基于JPA封装基础数据操作

> PostgreSQL在关系型数据库的稳定性和性能方面强于MySQL，所以它在实际项目中使用和占比越来越高。对开发而言最为常见的是基于数据库的CRUD封装等，本文主要介绍SpringBoot集成PostgreSQL数据库，以及基于JPA方式的基础封装思路。@pdai

## 知识准备

> 需要对PostgreSQL，JPA以及接口封装有了解。

### PostgreSQL简介

> 来源于百度百科。

PostgreSQL是一个功能非常强大的、源代码开放的客户/服务器关系型数据库管理系统（RDBMS）。PostgreSQL最初设想于1986年，当时被叫做Berkley Postgres Project。该项目一直到1994年都处于演进和修改中，直到开发人员Andrew Yu和Jolly Chen在Postgres中添加了一个SQL（Structured Query Language，结构化查询语言）翻译程序，该版本叫做Postgres95，在开放源代码社区发放。

1996年，再次对Postgres95做了较大的改动，并将其作为PostgresSQL6.0版发布。该版本的Postgres提高了后端的速度，包括增强型SQL92标准以及重要的后端特性（包括子选择、默认值、约束和触发器）。

PostgreSQL是一个非常健壮的软件包，有很多在大型商业RDBMS中所具有的特性，包括事务、子选择、触发器、视图、外键引用完整性和复杂锁定功能。另一方面，PostgreSQL也缺少商业数据库中某些可用的特性，如用户定义的类型、继承性和规则。从用户的角度来讲，PostgreSQL惟一不具备的主要特性就是外部连接，在今后的版本中会将其加入。 PostgreSQL提供了两种可选模式。一种模式保证如果操作系统或硬件崩溃，则数据将保存到磁盘中，这种模式通常比大多数商业数据库要慢，这是因为它使用了刷新（或同步）方法；另一种模式与第一种不同，它不提供数据保证，但它通常比商业数据库运行得快。遗憾的是，还没有一种折中的模式：既提供一定程度的数据安全性，又有较快的执行速度。今后的版本将会提供这种模式。

### PostgreSQL的特点

> 来源于百度百科。

PostgreSQL 的 **主要优点**如下：

- 维护者是PostgreSQL Global Development Group，首次发布于1989年6月。
- 操作系统支持WINDOWS、Linux、UNIX、MAC OS X、BSD。
- 从基本功能上来看，支持ACID、关联完整性、数据库事务、Unicode多国语言。
- 表和视图方面，PostgreSQL支持临时表，而物化视图，可以使用PL/pgSQL、PL/Perl、PL/Python或其他过程语言的存储过程和触发器模拟。
- 索引方面，全面支持R-/R+tree索引、哈希索引、反向索引、部分索引、Expression 索引、GiST、GIN（用来加速全文检索），从8.3版本开始支持位图索引。
- 其他对象上，支持数据域，支持存储过程、触发器、函数、外部调用、游标7）数据表分区方面，支持4种分区，即范围、哈希、混合、列表。
- 从事务的支持度上看，对事务的支持与MySQL相比，经历了更为彻底的测试。
- My ISAM表处理方式方面，MySQL对于无事务的MyISAM表，采用表锁定，1个长时间运行的查询很可能会阻碍对表的更新，而PostgreSQL不存在这样的问题。
- 从存储过程上看，PostgreSQL支持存储过程。因为存储过程的存在也避免了在网络上大量原始的SQL语句的传输，这样的优势是显而易见的。
- 用户定义函数的扩展方面，PostgreSQL可以更方便地使用UDF（用户定义函数）进行扩展。

PostgreSQL 的 **应用劣势**如下：

- 最新版本和历史版本不分离存储，导致清理老旧版本时需要做更多的扫描，代价比较大但一般的数据库都有高峰期，如果合理安排VACUUM，这也不是很大的问题，而且在PostgreSQL9.0中VACUUM进一步被加强了。
- 在PostgreSQL中，由于索引完全没有版本信息，不能实现Coverage index scan，即查询只扫描索引，不能直接从索引中返回所需的属性，还需要访问表，而Oracle与Innodb则可以。

### JPA相关

- [SpringBoot入门 - 添加内存数据库H2](springboot-x-hello-h2-jpa.md)

### 接口相关

> 站在接口设计和实现的角度，从实战开发中梳理出，关于接口开发的技术要点。

- [SpringBoot接口 - 如何统一接口封装](springboot-x-interface-response.md)
  - 在以SpringBoot开发Restful接口时，统一返回方便前端进行开发和封装，以及出现时给出响应编码和信息。
- [SpringBoot接口 - 如何对参数进行校验](springboot-x-interface-param.md)
  - 在以SpringBoot开发Restful接口时, 对于接口的查询参数后台也是要进行校验的，同时还需要给出校验的返回信息放到上文我们统一封装的结构中。那么如何优雅的进行参数的统一校验呢？
- [SpringBoot接口 - 如何参数校验国际化](springboot-x-interface-param-i18n.md)
  - 上文我们学习了如何对SpringBoot接口进行参数校验，但是如果需要有国际化的信息，应该如何优雅处理呢？
- [SpringBoot接口 - 如何统一异常处理](springboot-x-interface-exception.md)
  - SpringBoot接口如何对异常进行统一封装，并统一返回呢？以上文的参数校验为例，如何优雅的将参数校验的错误信息统一处理并封装返回呢？
- [SpringBoot接口 - 如何提供多个版本接口](springboot-x-interface-version.md)
  - 在以SpringBoot开发Restful接口时，由于模块，系统等业务的变化，需要对同一接口提供不同版本的参数实现（老的接口还有模块或者系统在用，不能直接改，所以需要不同版本）。如何更加优雅的实现多版本接口呢？
- [SpringBoot接口 - 如何生成接口文档](springboot-x-interface-doc.md)
  - SpringBoot开发Restful接口，有什么API规范吗？如何快速生成API文档呢？
- [SpringBoot接口 - 如何访问外部接口](springboot-x-interface-3rd.md)
  - 在SpringBoot接口开发中，存在着本模块的代码需要访问外面模块接口或外部url链接的需求, 比如调用外部的地图API或者天气API。那么有哪些方式可以调用外部接口呢？
- [SpringBoot接口 - 如何对接口进行加密](springboot-x-interface-jiami.md)
  - 在以SpringBoot开发后台API接口时，会存在哪些接口不安全的因素呢？通常如何去解决的呢？本文主要介绍API**接口有不安全的因素**以及**常见的保证接口安全的方式**，重点**实践如何对接口进行签名**。
- [SpringBoot接口 - 如何保证接口幂等](springboot-x-interface-mideng.md)
  - 在以SpringBoot开发Restful接口时，如何防止接口的重复提交呢？ 本文主要介绍接口幂等相关的知识点，并实践常见基于Token实现接口幂等。
- [SpringBoot接口 - 如何实现接口限流之单实例](springboot-x-interface-xianliu.md)
  - 在以SpringBoot开发Restful接口时，当流量超过服务极限能力时，系统可能会出现卡死、崩溃的情况，所以就有了降级和限流。在接口层如何做限流呢？ 本文主要回顾限流的知识点，并实践单实例限流的一种思路。
- [SpringBoot接口 - 如何实现接口限流之分布式](springboot-x-interface-xianliu-dist.md)
  - 上文中介绍了单实例下如何在业务接口层做限流，本文主要介绍分布式场景下限流的方案，以及什么样的分布式场景下需要在业务层加限流而不是接入层; 并且结合kailing开源的[ratelimiter-spring-boot-starter](https://gitee.com/kailing/ratelimiter-spring-boot-starter)为例， 学习**思路+代码封装+starter封装**。

## 实现案例

> 本例主要简单示例下基于JPA DAO/Service层封装， 并且注意下如下例子MySQL是5.7版本，8.x版本相关例子也在[示例源码](https://github.com/realpdai/tech-pdai-spring-demos)中。

### 准备DB

创建PostgreSQL DB: test_db_pg

![](https://www.pdai.tech/images/spring/springboot/springboot-pg-jpa-1.png)

导入SQL 文件如下

```sql
CREATE TABLE public.tb_user
(
    id bigint NOT NULL,
    user_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    password character varying(255) COLLATE pg_catalog."default" NOT NULL,
    email character varying(255) COLLATE pg_catalog."default",
    phone_number bigint,
    description character varying(255) COLLATE pg_catalog."default",
    create_time timestamp(6) with time zone,
    update_time timestamp(6) with time zone,
    CONSTRAINT tb_user_pkey PRIMARY KEY (id)
)

CREATE TABLE public.tb_role
(
    id bigint NOT NULL,
    name character varying(255) COLLATE pg_catalog."default",
    role_key character varying(255) COLLATE pg_catalog."default",
    description character varying(255) COLLATE pg_catalog."default",
    create_time timestamp(6) with time zone,
    update_time timestamp(6) with time zone,
    CONSTRAINT tb_role_pkey PRIMARY KEY (id)
)

CREATE TABLE public.tb_user_role
(
    user_id bigint NOT NULL,
    role_id bigint NOT NULL
)
```

引入maven依赖

```xml
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <version>42.2.18</version>
</dependency>
<dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-java8</artifactId>
    <version>5.0.12.Final</version>
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
```

增加yml配置

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/test_db_pg
    username: postgres
    password: bfXa4Pt2lUUScy8jakXf
    initial-size: 100
    max-idle: 60
    max-wait: 10000
    min-idle: 20
    max-active: 500
  jpa:
    database: postgresql
    generate-ddl: false
    show-sql: false
    open-in-view: false
    database-platform: org.hibernate.dialect.PostgreSQL94Dialect
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQL94Dialect
        format_sql: true
```

### 定义实体

> USER/ROLE

BaseEntity

```java
package tech.pdai.springboot.postgre.jpa.entity;

import java.io.Serializable;

/**
 * @author pdai
 */
public interface BaseEntity extends Serializable {
}
```

Role

```java
package tech.pdai.springboot.postgre.jpa.entity;

import java.time.LocalDateTime;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.GenericGenerator;
import tech.pdai.springboot.postgre.jpa.constants.PGConstants;

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
    @Column(name = "id", nullable = false)
    @GeneratedValue(generator = PGConstants.ID_GENERATOR)
    @GenericGenerator(name = PGConstants.ID_GENERATOR, strategy = PGConstants.ID_GENERATOR_CONFIG)
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

User

```java
package tech.pdai.springboot.postgre.jpa.entity;

import java.time.LocalDateTime;
import java.util.Set;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinTable;
import javax.persistence.ManyToMany;
import javax.persistence.Table;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.GenericGenerator;
import tech.pdai.springboot.postgre.jpa.constants.PGConstants;

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
    @Column(name = "id", nullable = false)
    @GeneratedValue(generator = PGConstants.ID_GENERATOR)
    @GenericGenerator(name = PGConstants.ID_GENERATOR, strategy = PGConstants.ID_GENERATOR_CONFIG)
    private Long id;

    /**
     * username.
     */
    private String userName;

    /**
     * user pwd.
     */
    @JsonIgnore
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

### DAO层

BaseDao

```java
package tech.pdai.springboot.postgre.jpa.dao;

import java.io.Serializable;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.repository.NoRepositoryBean;
import tech.pdai.springboot.postgre.jpa.entity.BaseEntity;

/**
 * @author pdai
 */
@NoRepositoryBean
public interface IBaseDao<T extends BaseEntity, I extends Serializable>
        extends JpaRepository<T, I>, JpaSpecificationExecutor<T> {
}
```

RoleDao

```java
package tech.pdai.springboot.postgre.jpa.dao;

import org.springframework.stereotype.Repository;
import tech.pdai.springboot.postgre.jpa.entity.Role;

/**
 * @author pdai
 */
@Repository
public interface IRoleDao extends IBaseDao<Role, Long> {

}
```

UserDao

```java
package tech.pdai.springboot.postgre.jpa.dao;

import org.springframework.stereotype.Repository;
import tech.pdai.springboot.postgre.jpa.entity.User;

/**
 * @author pdai
 */
@Repository
public interface IUserDao extends IBaseDao<User, Long> {

}
```

### Service层

#### BaseService

封装BaseService

```java
package tech.pdai.springboot.postgre.jpa.service;

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
package tech.pdai.springboot.postgre.jpa.service.impl;

import java.io.Serializable;
import java.util.Arrays;
import java.util.List;

import javax.transaction.Transactional;

import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.domain.Specification;
import tech.pdai.springboot.postgre.jpa.dao.IBaseDao;
import tech.pdai.springboot.postgre.jpa.entity.BaseEntity;
import tech.pdai.springboot.postgre.jpa.service.IBaseService;

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
package tech.pdai.springboot.postgre.jpa.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import tech.pdai.springboot.postgre.jpa.entity.User;
import tech.pdai.springboot.postgre.jpa.entity.query.UserQueryBean;

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
package tech.pdai.springboot.postgre.jpa.service.impl;


import com.github.wenhao.jpa.Specifications;
import org.apache.commons.lang3.StringUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import tech.pdai.springboot.postgre.jpa.dao.IBaseDao;
import tech.pdai.springboot.postgre.jpa.dao.IUserDao;
import tech.pdai.springboot.postgre.jpa.entity.User;
import tech.pdai.springboot.postgre.jpa.entity.query.UserQueryBean;
import tech.pdai.springboot.postgre.jpa.service.IUserService;

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
package tech.pdai.springboot.postgre.jpa.service;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import tech.pdai.springboot.postgre.jpa.entity.Role;
import tech.pdai.springboot.postgre.jpa.entity.query.RoleQueryBean;

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
package tech.pdai.springboot.postgre.jpa.service.impl;

import com.github.wenhao.jpa.Specifications;
import org.apache.commons.lang3.StringUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import tech.pdai.springboot.postgre.jpa.dao.IBaseDao;
import tech.pdai.springboot.postgre.jpa.dao.IRoleDao;
import tech.pdai.springboot.postgre.jpa.entity.Role;
import tech.pdai.springboot.postgre.jpa.entity.query.RoleQueryBean;
import tech.pdai.springboot.postgre.jpa.service.IRoleService;

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
package tech.pdai.springboot.postgre.jpa.controller;


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
import tech.pdai.springboot.postgre.jpa.entity.User;
import tech.pdai.springboot.postgre.jpa.entity.query.UserQueryBean;
import tech.pdai.springboot.postgre.jpa.entity.response.ResponseResult;
import tech.pdai.springboot.postgre.jpa.service.IUserService;

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

插入数据

![](https://www.pdai.tech/images/spring/springboot/springboot-pg-jpa-2.png)

查询分页列表

![](https://www.pdai.tech/images/spring/springboot/springboot-pg-jpa-3.png)

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos