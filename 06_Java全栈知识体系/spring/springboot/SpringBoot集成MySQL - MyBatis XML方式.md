# SpringBoot集成MySQL - MyBatis XML方式

> 上文介绍了用JPA方式的集成MySQL数据库，JPA方式在中国以外地区开发而言基本是标配，在国内MyBatis及其延伸框架较为主流。本文主要介绍**MyBatis技栈的演化**以及**SpringBoot集成基础的MyBatis XML实现方式**的实例。@pdai

## 准备知识

> 需要了解MyBatis及MyBatis技术栈的演进，这对新的开发者可以很好的构筑其知识体系。@pdai

### 什么是MyBatis？

> MyBatis是一款优秀的基于java的持久层框架，它内部封装了jdbc，使开发者只需要关注sql语句本身，而不需要花费精力去处理加载驱动、创建连接、创建statement等繁杂的过程。

MyBatis 是一款优秀的持久层框架，它支持定制化 SQL、存储过程以及高级映射。

- mybatis是一个优秀的基于java的持久层框架，它内部封装了jdbc，使开发者只需要关注sql语句本身，而不需要花费精力去处理加载驱动、创建连接、创建statement等繁杂的过程。
- mybatis通过xml或注解的方式将要执行的各种statement配置起来，并通过java对象和statement中sql的动态参数进行映射生成最终执行的sql语句，最后由mybatis框架执行sql并将结果映射为java对象并返回。

**MyBatis的主要设计目**的就是让我们对执行SQL语句时对输入输出的数据管理更加方便，所以方便地写出SQL和方便地获取SQL的执行结果才是MyBatis的核心竞争力。

**Mybatis的功能架构分为三层**：

- **API接口层**：提供给外部使用的接口API，开发人员通过这些本地API来操纵数据库。接口层一接收到调用请求就会调用数据处理层来完成具体的数据处理。
- **数据处理层**：负责具体的SQL查找、SQL解析、SQL执行和执行结果映射处理等。它主要的目的是根据调用的请求完成一次数据库操作。
- **基础支撑层**：负责最基础的功能支撑，包括连接管理、事务管理、配置加载和缓存处理，这些都是共用的东西，将他们抽取出来作为最基础的组件。为上层的数据处理层提供最基础的支撑。

更多介绍可以参考：[MyBatis3 官方网站](https://mybatis.org/mybatis-3/)

### 为什么说MyBatis是半自动ORM？

> 为什么说MyBatis是半自动ORM？

- **什么是ORM**？

JDBC，ORM知识点可以参考[SpringBoot入门 - 添加内存数据库H2](SpringBoot入门 - 添加内存数据库H2.md)

- **什么是全自动ORM**？

ORM框架可以根据对象关系模型直接获取，查询关联对象或者关联集合对象，简单而言使用全自动的ORM框架查询时可以不再写SQL。典型的框架如Hibernate； 因为Spring-data-jpa很多代码也是Hibernate团队贡献的，所以spring-data-jpa也是全自动ORM框架。

- **MyBatis是半自动ORM**？

Mybatis 在查询关联对象或关联集合对象时，需要手动编写 sql 来完成，所以，称之为半自动ORM 映射工具。

（PS: 正是由于MyBatis是半自动框架，基于MyBatis技术栈的框架开始考虑兼容MyBatis开发框架的基础上提供自动化的能力，比如MyBatis-plus等框架）

### MyBatis栈技术演进

> 了解MyBatis技术栈的演进，对你构建基于MyBatis的知识体系极为重要。@pdai

#### JDBC，自行封装JDBCUtil

Java5的时代，通常的开发中会自行封装JDBC的Util，比如创建 Connection，以及确保关闭 Connection等。

#### IBatis

MyBatis的前身，它封装了绝大多数的 JDBC 样板代码，使得开发者只需关注 SQL 本身，而不需要花费精力去处理例如注册驱动，创建 Connection，以及确保关闭 Connection 这样繁杂的代码。

#### MyBatis

伴随着JDK5+ 泛型和注解特性开始流行，IBatis在3.0变更为MyBatis，对泛型和注解等特性开始全面支持，同时支持了很多新的特性，比如：

1. mybatis实现了接口绑定，通过Dao接口 和xml映射文件的绑定，自动生成接口的具体实现
2. mybatis支持 ognl表达式，比如 `<if>, <else>`使用ognl进行解析
3. mybatis插件机制等，（PageHelper分页插件应用而生，解决了数据库层的分页封装问题）

所以这个时期，**MyBatis XML 配置方式 + PageHelper** 成为重要的开发方式。

#### MyBatis衍生：代码生成工具等

MyBatis提供了开发上的便捷，但是依然需要写大量的xml配置，并且很多都是CRUD级别的（这便有了很多重复性的工作），所以为了减少重复编码，衍生出了MyBatis代码生成工具, 比如CodeGenerator等。

其它开发IDE也开始出现封装一些工具和插件来生成代码生成工具等。

由于后端视图解析引擎多样性（比如freemarker, volicty, thymeleaf等），以及前后端分离前端独立等，为了进一步减少重复代码的编写（包括视图层），自动生成的代码工具也开始演化为自动生成前端视图代码。

#### Spring+MyBatis基于注解的配置集成

与此同时，Spring 2.5 开始完全支持基于注解的配置并且也支持JSR250 注解。在Spring后续的版本发展倾向于通过注解和Java配置结合使用。基于Spring+MyBatis开发技术栈开始有xml配置方式往注解和java配置方式反向发展。

Spring Boot的出现便是要解决配置过多的问题，它实际上通过约定大于配置的方式大大简化了用户的配置，对于三方组件使用xx-starter统一的对Bean进行默认初始化，用户只需要很少的配置就可以进行开发了。所以出现了mybatis-spring-boot-starter的封装等。

这个阶段，主要的开发技术栈是 **Spring + mybatis-spring-boot-starter 自动化配置 + PageHelper**，并且很多数据库实体mapper还是通过xml方式配置的（伴随着使用一些自动化生成工具）。

#### MyBatis-Plus

为了更高的效率，出现了MyBatis-Plus这类工具，对MyBatis进行增强。

1. **考虑到MyBatis是半自动化ORM**，MyBatis-Plus 启动即会自动注入基本 CURD，性能基本无损耗，直接面向对象操作; 并且内置通用 Mapper、通用 Service，仅仅通过少量配置即可实现单表大部分 CRUD 操作，更有强大的条件构造器，满足各类使用需求；总体上让其支持全自动化的使用方式（本质上借鉴了Hibernate思路）。
2. **考虑到Java8 Lambda（函数式编程）开始流行**，MyBatis-Plus支持 Lambda 表达式，方便的编写各类查询条件，无需再担心字段写错
3. **考虑到MyBatis还需要独立引入PageHelper分页插件**，MyBatis-Plus支持了内置分页插件，同PageHelper一样基于 MyBatis 物理分页，开发者无需关心具体操作，配置好插件之后，写分页等同于普通 List 查询
4. **考虑到自动化代码生成方式**，MyBatis-Plus也支持了内置代码生成器，采用代码或者 Maven 插件可快速生成 Mapper 、 Model 、 Service 、 Controller 层代码，支持模板引擎，更有超多自定义配置等您来使用
5. **考虑到SQL性能优化等问题**，MyBatis-Plus内置性能分析插件, 可输出 SQL 语句以及其执行时间，建议开发测试时启用该功能，能快速揪出慢查询
6. 其它还有解决一些常见开发问题，比如**支持主键自动生成**，支持4 种主键策略（内含分布式唯一 ID 生成器 - Sequence），可自由配置，完美解决主键问题；以及**内置全局拦截插件**，提供全表 delete 、 update 操作智能分析阻断，也可自定义拦截规则，预防误操作

顶层思维能力

用这种思路去理解，你便能很快了解MyBatis技术栈的演化（能够快速维护老一些的技术框架），以及理解新的中小项目中MyBatis-Plus被大量使用的原因（新项目的技术选型参考）；所以java全栈知识体系的目标是帮助你构建知识体系，甚至是辅助你培养顶层思维能力。@pdai

## 简单示例

> 尽管MyBatis-Plus大行其道，MyBatis XML 配置方式 + PageHelper依然是基础使用方式。本例依然向你展示MyBatis XML 配置方式，考虑到和spring-data-jpa方式对比，这里沿用上一篇文章的数据库。后续的案例中将具体介绍MyBatis分页，以及MyBatis-Plus的使用等。

### 准备DB和依赖配置

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

```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.47</version>
</dependency>
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>2.1.0</version>
</dependency>
<!--pagehelper分页 -->
<dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper-spring-boot-starter</artifactId>
    <version>1.2.10</version>
</dependency>
```

增加yml配置

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/test_db?useSSL=false&autoReconnect=true&characterEncoding=utf8
    driver-class-name: com.mysql.jdbc.Driver
    username: root
    password: bfXa4Pt2lUUScy8jakXf

mybatis:
  mapper-locations: classpath:mybatis/mapper/*.xml
  type-aliases-package: tech.pdai.springboot.mysql57.xml.entity
  configuration:
    cache-enabled: true
    use-generated-keys: true
    default-executor-type: REUSE
    use-actual-param-name: true
```

`classpath:mybatis/mapper/*.xml`是mapper的位置。

### Mapper文件

mapper文件定义在配置的路径中（`classpath:mybatis/mapper/*.xml`）

UserMapper.xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="tech.pdai.springboot.mysql57.mybatis.xml.dao.IUserDao">

	<resultMap type="tech.pdai.springboot.mysql57.mybatis.xml.entity.User" id="UserResult">
		<id     property="id"       	column="id"      		/>
		<result property="userName"     column="user_name"    	/>
		<result property="password"     column="password"    	/>
		<result property="email"        column="email"        	/>
		<result property="phoneNumber"  column="phone_number"  	/>
		<result property="description"  column="description"  	/>
		<result property="createTime"   column="create_time"  	/>
		<result property="updateTime"   column="update_time"  	/>
		<collection property="roles" ofType="tech.pdai.springboot.mysql57.mybatis.xml.entity.Role">
			<result property="id" column="id"  />
			<result property="name" column="name"  />
			<result property="roleKey" column="role_key"  />
			<result property="description" column="description"  />
			<result property="createTime"   column="create_time"  	/>
			<result property="updateTime"   column="update_time"  	/>
		</collection>
	</resultMap>
	
	<sql id="selectUserSql">
        select u.id, u.password, u.user_name, u.email, u.phone_number, u.description, u.create_time, u.update_time, r.name, r.role_key, r.description, r.create_time, r.update_time
		from tb_user u
		left join tb_user_role ur on u.id=ur.user_id
		inner join tb_role r on ur.role_id=r.id
    </sql>
	
	<select id="findList" parameterType="tech.pdai.springboot.mysql57.mybatis.xml.entity.query.UserQueryBean" resultMap="UserResult">
		<include refid="selectUserSql"/>
		where u.id != 0
		<if test="userName != null and userName != ''">
			AND u.user_name like concat('%', #{user_name}, '%')
		</if>
		<if test="description != null and description != ''">
			AND u.description like concat('%', #{description}, '%')
		</if>
		<if test="phoneNumber != null and phoneNumber != ''">
			AND u.phone_number like concat('%', #{phoneNumber}, '%')
		</if>
		<if test="email != null and email != ''">
			AND u.email like concat('%', #{email}, '%')
		</if>
	</select>
	
	<select id="findById" parameterType="Long" resultMap="UserResult">
		<include refid="selectUserSql"/>
		where u.id = #{id}
	</select>
	
	<delete id="deleteById" parameterType="Long">
 		delete from tb_user where id = #{id}
 	</delete>
 	
 	<delete id="deleteByIds" parameterType="Long">
		delete from tb_user where id in
 		<foreach collection="array" item="id" open="(" separator="," close=")">
 			#{id}
        </foreach> 
 	</delete>
 	
 	<update id="update" parameterType="tech.pdai.springboot.mysql57.mybatis.xml.entity.User">
 		update tb_user
 		<set>
 			<if test="userName != null and userName != ''">user_name = #{userName},</if>
 			<if test="email != null and email != ''">email = #{email},</if>
 			<if test="phoneNumber != null and phoneNumber != ''">phone_number = #{phoneNumber},</if>
			<if test="description != null and description != ''">description = #{description},</if>
 			update_time = sysdate()
 		</set>
 		where id = #{id}
	</update>

	<update id="updatePassword" parameterType="tech.pdai.springboot.mysql57.mybatis.xml.entity.User">
		update tb_user
		<set>
			password = #{password}, update_time = sysdate()
		</set>
		where id = #{id}
	</update>
 	
 	<insert id="save" parameterType="tech.pdai.springboot.mysql57.mybatis.xml.entity.User" useGeneratedKeys="true" keyProperty="id">
 		insert into tb_user(
 			<if test="userName != null and userName != ''">user_name,</if>
			<if test="password != null and password != ''">password,</if>
 			<if test="email != null and email != ''">email,</if>
			<if test="phoneNumber != null and phoneNumber != ''">phone_number,</if>
 			<if test="description != null and description != ''">description,</if>
 			create_time,
			update_time
 		)values(
 			<if test="userName != null and userName != ''">#{userName},</if>
			<if test="password != null and password != ''">#{password},</if>
 			<if test="email != null and email != ''">#{email},</if>
 			<if test="phoneNumber != null and phoneNumber != ''">#{phone_number},</if>
 			<if test="description != null and description != ''">#{description},</if>
 			sysdate(),
			sysdate()
 		)
	</insert>
	
</mapper>
```

RoleMapper.xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="tech.pdai.springboot.mysql57.mybatis.xml.dao.IRoleDao">

	<resultMap type="tech.pdai.springboot.mysql57.mybatis.xml.entity.Role" id="RoleResult">
		<id     property="id"       	column="id"      		/>
		<result property="name" 		column="name"  />
		<result property="roleKey" 		column="role_key"  />
		<result property="description" 	column="description"  />
		<result property="createTime"   column="create_time"  	/>
		<result property="updateTime"   column="update_time"  	/>
	</resultMap>
	
	<sql id="selectRoleSql">
        select  r.id, r.name, r.role_key, r.description, r.create_time, r.update_time
			from tb_role r
    </sql>
	
	<select id="findList" parameterType="tech.pdai.springboot.mysql57.mybatis.xml.entity.query.RoleQueryBean" resultMap="RoleResult">
		<include refid="selectRoleSql"/>
		where r.id != 0
		<if test="name != null and name != ''">
			AND r.name like concat('%', #{name}, '%')
		</if>
		<if test="roleKey != null and roleKey != ''">
			AND r.role_key = #{roleKey}
		</if>
		<if test="description != null and description != ''">
			AND r.description like concat('%', #{description}, '%')
		</if>
	</select>
	
</mapper>
```

### 定义dao

与Mapper文件中方法对应

UserDao

```java
package tech.pdai.springboot.mysql57.mybatis.xml.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.User;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.query.UserQueryBean;

/**
 * @author pdai
 */
@Mapper
public interface IUserDao {

    List<User> findList(UserQueryBean userQueryBean);

    User findById(Long id);

    int deleteById(Long id);

    int deleteByIds(Long[] ids);

    int update(User user);

    int save(User user);

    int updatePassword(User user);
}
```

RoleDao

```java
package tech.pdai.springboot.mysql57.mybatis.xml.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.Role;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.query.RoleQueryBean;

/**
 * @author pdai
 */
@Mapper
public interface IRoleDao {
    List<Role> findList(RoleQueryBean roleQueryBean);
}
```

### 定义Service接口和实现类

UserService接口

```java
package tech.pdai.springboot.mysql57.mybatis.xml.service;

import java.util.List;

import tech.pdai.springboot.mysql57.mybatis.xml.entity.User;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.query.UserQueryBean;


/**
 * @author pdai
 */
public interface IUserService {

    List<User> findList(UserQueryBean userQueryBean);

    User findById(Long id);

    int deleteById(Long id);

    int deleteByIds(Long[] ids);

    int update(User user);

    int save(User user);

    int updatePassword(User user);

}
```

User Service的实现类

```java
package tech.pdai.springboot.mysql57.mybatis.xml.service.impl;

import java.util.List;

import org.springframework.stereotype.Service;
import tech.pdai.springboot.mysql57.mybatis.xml.dao.IUserDao;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.User;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.query.UserQueryBean;
import tech.pdai.springboot.mysql57.mybatis.xml.service.IUserService;

@Service
public class UserDoServiceImpl implements IUserService {

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

    @Override
    public List<User> findList(UserQueryBean userQueryBean) {
        return userDao.findList(userQueryBean);
    }

    @Override
    public User findById(Long id) {
        return userDao.findById(id);
    }

    @Override
    public int deleteById(Long id) {
        return userDao.deleteById(id);
    }

    @Override
    public int deleteByIds(Long[] ids) {
        return userDao.deleteByIds(ids);
    }

    @Override
    public int update(User user) {
        return userDao.update(user);
    }

    @Override
    public int save(User user) {
        return userDao.save(user);
    }

    @Override
    public int updatePassword(User user) {
        return userDao.updatePassword(user);
    }
}
```

Role Service 接口

```java
package tech.pdai.springboot.mysql57.mybatis.xml.service;

import java.util.List;

import tech.pdai.springboot.mysql57.mybatis.xml.entity.Role;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.query.RoleQueryBean;

public interface IRoleService {

    List<Role> findList(RoleQueryBean roleQueryBean);

}
```

Role Service 实现类

```java
package tech.pdai.springboot.mysql57.mybatis.xml.service.impl;

import java.util.List;

import org.springframework.stereotype.Service;
import tech.pdai.springboot.mysql57.mybatis.xml.dao.IRoleDao;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.Role;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.query.RoleQueryBean;
import tech.pdai.springboot.mysql57.mybatis.xml.service.IRoleService;

@Service
public class RoleDoServiceImpl implements IRoleService {

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

    @Override
    public List<Role> findList(RoleQueryBean roleQueryBean) {
        return roleDao.findList(roleQueryBean);
    }
}
```

### controller

User Controller

```java
package tech.pdai.springboot.mysql57.mybatis.xml.controller;


import java.time.LocalDateTime;
import java.util.List;

import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.User;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.query.UserQueryBean;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.response.ResponseResult;
import tech.pdai.springboot.mysql57.mybatis.xml.service.IUserService;

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
        if (user.getId()==null) {
            user.setCreateTime(LocalDateTime.now());
            user.setUpdateTime(LocalDateTime.now());
            userService.save(user);
        } else {
            user.setUpdateTime(LocalDateTime.now());
            userService.update(user);
        }
        return ResponseResult.success(userService.findById(user.getId()));
    }


    /**
     * @return user list
     */
    @ApiOperation("Query User One")
    @GetMapping("edit/{userId}")
    public ResponseResult<User> edit(@PathVariable("userId") Long userId) {
        return ResponseResult.success(userService.findById(userId));
    }

    /**
     * @return user list
     */
    @ApiOperation("Query User List")
    @GetMapping("list")
    public ResponseResult<List<User>> list(UserQueryBean userQueryBean) {
        return ResponseResult.success(userService.findList(userQueryBean));
    }
}
```

Role Controller

```java
package tech.pdai.springboot.mysql57.mybatis.xml.controller;


import java.util.List;

import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.Role;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.query.RoleQueryBean;
import tech.pdai.springboot.mysql57.mybatis.xml.entity.response.ResponseResult;
import tech.pdai.springboot.mysql57.mybatis.xml.service.IRoleService;

/**
 * @author pdai
 */
@RestController
@RequestMapping("/role")
public class RoleController {

    @Autowired
    private IRoleService roleService;

    /**
     * @return user list
     */
    @ApiOperation("Query Role List")
    @GetMapping("list")
    public ResponseResult<List<Role>> list(RoleQueryBean roleQueryBean) {
        return ResponseResult.success(roleService.findList(roleQueryBean));
    }
}
```

## 示例源码

（上述代码中一些实体类和配置的完整代码，请参考如下代码仓库）

https://github.com/realpdai/tech-pdai-spring-demos