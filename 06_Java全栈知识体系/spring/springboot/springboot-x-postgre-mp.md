# SpringBoot集成PostgreSQL - 基于MyBatis-Plus方式

> 前文介绍SpringBoot+MyBatis-Plus+MySQL的集成，本文主要介绍SpringBoot+MyBatis-Plus+PostgreSQL的集成。@pdai

## 知识准备

> MyBatis-Plus（简称 MP）是一个 MyBatis的增强工具，在 MyBatis 的基础上只做增强不做改变，为简化开发、提高效率而生。

- [SpringBoot集成MySQL - MyBatis-Plus方式](springboot-x-mysql-mybatis-plus.md)
  - MyBatis-Plus（简称 MP）是一个 MyBatis的增强工具，在 MyBatis 的基础上只做增强不做改变，为简化开发、提高效率而生。MyBatis-Plus在国内也有很多的用户，本文主要介绍MyBatis-Plus和SpringBoot的集成。

## 简单示例

> 这里保持我们前文同样的结构的数据库（略有更改）, 并向你展示SpringBoot + MyBatis-Plus的使用等。

### 准备DB和依赖配置

创建PostgreSQL的Database test_db_pg, 导入SQL 文件如下

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
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-boot-starter</artifactId>
    <version>3.5.1</version>
</dependency>
```

增加yml配置

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/test_db_pg
    username: postgres
    password: bfXa4Pt2lUUScy8jakXf
mybatis-plus:
  configuration:
    cache-enabled: true
    use-generated-keys: true
    default-executor-type: REUSE
    use-actual-param-name: true
```

### 定义dao

(也就是你自己的xxxMapper)

RoleDao

```java
package tech.pdai.springboot.postgre.mybatisplus.dao;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import tech.pdai.springboot.postgre.mybatisplus.entity.Role;

/**
 * @author pdai
 */
public interface IRoleDao extends BaseMapper<Role> {
}
```

UserDao

```java
package tech.pdai.springboot.postgre.mybatisplus.dao;

import java.util.List;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import tech.pdai.springboot.postgre.mybatisplus.entity.User;
import tech.pdai.springboot.postgre.mybatisplus.entity.query.UserQueryBean;

/**
 * @author pdai
 */
public interface IUserDao extends BaseMapper<User> {

    List<User> findList(UserQueryBean userQueryBean);
}
```

这里你也同时可以支持BaseMapper方式和自己定义的xml的方法（比较适用于关联查询），比如findList是自定义xml配置

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="tech.pdai.springboot.postgre.mybatisplus.dao.IUserDao">

	<resultMap type="tech.pdai.springboot.postgre.mybatisplus.entity.User" id="UserResult">
		<id     property="id"       	column="id"      		/>
		<result property="userName"     column="user_name"    	/>
		<result property="password"     column="password"    	/>
		<result property="email"        column="email"        	/>
		<result property="phoneNumber"  column="phone_number"  	/>
		<result property="description"  column="description"  	/>
		<result property="createTime"   column="create_time"  typeHandler="tech.pdai.springboot.postgre.mybatisplus.config.PgTimestampZTypeHandler"	/>
		<result property="updateTime"   column="update_time"  typeHandler="tech.pdai.springboot.postgre.mybatisplus.config.PgTimestampZTypeHandler"	/>
		<collection property="roles" ofType="tech.pdai.springboot.postgre.mybatisplus.entity.Role">
			<result property="id" column="id"  />
			<result property="name" column="name"  />
			<result property="roleKey" column="role_key"  />
			<result property="description" column="description"  />
			<result property="createTime"   column="create_time"  typeHandler="tech.pdai.springboot.postgre.mybatisplus.config.PgTimestampZTypeHandler"	/>
			<result property="updateTime"   column="update_time"  typeHandler="tech.pdai.springboot.postgre.mybatisplus.config.PgTimestampZTypeHandler"	/>
		</collection>
	</resultMap>
	
	<sql id="selectUserSql">
        select u.id, u.password, u.user_name, u.email, u.phone_number, u.description, u.create_time, u.update_time, r.name, r.role_key, r.description, r.create_time, r.update_time
		from tb_user u
		left join tb_user_role ur on u.id=ur.user_id
		inner join tb_role r on ur.role_id=r.id
    </sql>
	
	<select id="findList" parameterType="tech.pdai.springboot.postgre.mybatisplus.entity.query.UserQueryBean" resultMap="UserResult">
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
	
</mapper>
```

### 定义Service接口和实现类

UserService接口

```java
package tech.pdai.springboot.postgre.mybatisplus.service;

import java.util.List;

import com.baomidou.mybatisplus.extension.service.IService;
import tech.pdai.springboot.postgre.mybatisplus.entity.User;
import tech.pdai.springboot.postgre.mybatisplus.entity.query.UserQueryBean;

/**
 * @author pdai
 */
public interface IUserService extends IService<User> {

    List<User> findList(UserQueryBean userQueryBean);

}
```

User Service的实现类

```java
package tech.pdai.springboot.postgre.mybatisplus.service.impl;

import java.util.List;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;
import tech.pdai.springboot.postgre.mybatisplus.dao.IUserDao;
import tech.pdai.springboot.postgre.mybatisplus.entity.User;
import tech.pdai.springboot.postgre.mybatisplus.entity.query.UserQueryBean;
import tech.pdai.springboot.postgre.mybatisplus.service.IUserService;

@Service
public class UserDoServiceImpl extends ServiceImpl<IUserDao, User> implements IUserService {

    @Override
    public List<User> findList(UserQueryBean userQueryBean) {
        return baseMapper.findList(userQueryBean);
    }
}
```

Role Service 接口

```java
package tech.pdai.springboot.postgre.mybatisplus.service;

import java.util.List;

import com.baomidou.mybatisplus.extension.service.IService;
import tech.pdai.springboot.postgre.mybatisplus.entity.Role;
import tech.pdai.springboot.postgre.mybatisplus.entity.query.RoleQueryBean;

public interface IRoleService extends IService<Role> {

    List<Role> findList(RoleQueryBean roleQueryBean);

}
```

Role Service 实现类

```java
package tech.pdai.springboot.postgre.mybatisplus.service.impl;

import java.util.List;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Service;
import tech.pdai.springboot.postgre.mybatisplus.dao.IRoleDao;
import tech.pdai.springboot.postgre.mybatisplus.entity.Role;
import tech.pdai.springboot.postgre.mybatisplus.entity.query.RoleQueryBean;
import tech.pdai.springboot.postgre.mybatisplus.service.IRoleService;

@Service
public class RoleDoServiceImpl extends ServiceImpl<IRoleDao, Role> implements IRoleService {

    @Override
    public List<Role> findList(RoleQueryBean roleQueryBean) {
        return lambdaQuery().like(StringUtils.isNotEmpty(roleQueryBean.getName()), Role::getName, roleQueryBean.getName())
                .like(StringUtils.isNotEmpty(roleQueryBean.getDescription()), Role::getDescription, roleQueryBean.getDescription())
                .like(StringUtils.isNotEmpty(roleQueryBean.getRoleKey()), Role::getRoleKey, roleQueryBean.getRoleKey())
                .list();
    }
}
```

### controller

User Controller

```java
package tech.pdai.springboot.postgre.mybatisplus.controller;


import java.time.LocalDateTime;
import java.util.List;

import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import tech.pdai.springboot.postgre.mybatisplus.entity.User;
import tech.pdai.springboot.postgre.mybatisplus.entity.query.UserQueryBean;
import tech.pdai.springboot.postgre.mybatisplus.entity.response.ResponseResult;
import tech.pdai.springboot.postgre.mybatisplus.service.IUserService;


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
        if (user.getId() == null) {
            user.setCreateTime(LocalDateTime.now());
        }
        user.setUpdateTime(LocalDateTime.now());
        userService.save(user);
        return ResponseResult.success(userService.getById(user.getId()));
    }


    /**
     * @return user list
     */
    @ApiOperation("Query User One")
    @GetMapping("edit/{userId}")
    public ResponseResult<User> edit(@PathVariable("userId") Long userId) {
        return ResponseResult.success(userService.getById(userId));
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
package tech.pdai.springboot.postgre.mybatisplus.controller;


import java.util.List;

import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import tech.pdai.springboot.postgre.mybatisplus.entity.Role;
import tech.pdai.springboot.postgre.mybatisplus.entity.query.RoleQueryBean;
import tech.pdai.springboot.postgre.mybatisplus.entity.response.ResponseResult;
import tech.pdai.springboot.postgre.mybatisplus.service.IRoleService;

/**
 * @author pdai
 */
@RestController
@RequestMapping("/role")
public class RoleController {

    @Autowired
    private IRoleService roleService;

    /**
     * @return role list
     */
    @ApiOperation("Query Role List")
    @GetMapping("list")
    public ResponseResult<List<Role>> list(RoleQueryBean roleQueryBean) {
        return ResponseResult.success(roleService.findList(roleQueryBean));
    }
}
```

### 分页配置

通过配置内置的MybatisPlusInterceptor拦截器。

```java
package tech.pdai.springboot.postgre.mybatisplus.config;

import com.baomidou.mybatisplus.extension.plugins.MybatisPlusInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.PaginationInnerInterceptor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * MyBatis-plus configuration, add pagination interceptor.
 *
 * @author pdai
 */
@Configuration
public class MyBatisConfig {

    /**
     * inject pagination interceptor.
     *
     * @return pagination
     */
    @Bean
    public PaginationInnerInterceptor paginationInnerInterceptor() {
        return new PaginationInnerInterceptor();
    }

    /**
     * add pagination interceptor.
     *
     * @return MybatisPlusInterceptor
     */
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor mybatisPlusInterceptor = new MybatisPlusInterceptor();
        mybatisPlusInterceptor.addInnerInterceptor(paginationInnerInterceptor());
        return mybatisPlusInterceptor;
    }

}
```

## 进一步理解

> MyBatis-plus学习梳理

- [官方文档](https://baomidou.com/)
- [官方案例](https://github.com/baomidou/mybatis-plus-samples)
- [官方源码仓库](https://github.com/baomidou/mybatis-plus)
- [Awesome Mybatis-Plus](https://github.com/baomidou/awesome-mybatis-plus)

### 比较好的实践

> 总结下开发的过程中比较好的实践

1. Mapper层：继承`BaseMapper`

```java
public interface IRoleDao extends BaseMapper<Role> {
}
```

2. Service层：继承`ServiceImpl`并实现对应接口

```java
public class RoleDoServiceImpl extends ServiceImpl<IRoleDao, Role> implements IRoleService {

}
```

3. Lambda函数式查询

```java
@Override
public List<Role> findList(RoleQueryBean roleQueryBean) {
    return lambdaQuery().like(StringUtils.isNotEmpty(roleQueryBean.getName()), Role::getName, roleQueryBean.getName())
            .like(StringUtils.isNotEmpty(roleQueryBean.getDescription()), Role::getDescription, roleQueryBean.getDescription())
            .like(StringUtils.isNotEmpty(roleQueryBean.getRoleKey()), Role::getRoleKey, roleQueryBean.getRoleKey())
            .list();
}
```

4. 分页采用内置MybatisPlusInterceptor

```java
/**
  * inject pagination interceptor.
  *
  * @return pagination
  */
@Bean
public PaginationInnerInterceptor paginationInnerInterceptor() {
    return new PaginationInnerInterceptor();
}

/**
  * add pagination interceptor.
  *
  * @return MybatisPlusInterceptor
  */
@Bean
public MybatisPlusInterceptor mybatisPlusInterceptor() {
    MybatisPlusInterceptor mybatisPlusInterceptor = new MybatisPlusInterceptor();
    mybatisPlusInterceptor.addInnerInterceptor(paginationInnerInterceptor());
    return mybatisPlusInterceptor;
}
```

5. 对于复杂的关联查询

可以配置原生xml方式, 在其中自定义ResultMap

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="tech.pdai.springboot.postgre.mybatisplus.dao.IUserDao">

	<resultMap type="tech.pdai.springboot.postgre.mybatisplus.entity.User" id="UserResult">
		<id     property="id"       	column="id"      		/>
		<result property="userName"     column="user_name"    	/>
		<result property="password"     column="password"    	/>
		<result property="email"        column="email"        	/>
		<result property="phoneNumber"  column="phone_number"  	/>
		<result property="description"  column="description"  	/>
		<result property="createTime"   column="create_time"  typeHandler="tech.pdai.springboot.postgre.mybatisplus.config.PgTimestampZTypeHandler"	/>
		<result property="updateTime"   column="update_time"  typeHandler="tech.pdai.springboot.postgre.mybatisplus.config.PgTimestampZTypeHandler"	/>
		<collection property="roles" ofType="tech.pdai.springboot.postgre.mybatisplus.entity.Role">
			<result property="id" column="id"  />
			<result property="name" column="name"  />
			<result property="roleKey" column="role_key"  />
			<result property="description" column="description"  />
			<result property="createTime"   column="create_time"  typeHandler="tech.pdai.springboot.postgre.mybatisplus.config.PgTimestampZTypeHandler"	/>
			<result property="updateTime"   column="update_time"  typeHandler="tech.pdai.springboot.postgre.mybatisplus.config.PgTimestampZTypeHandler"	/>
		</collection>
	</resultMap>
	
	<sql id="selectUserSql">
        select u.id, u.password, u.user_name, u.email, u.phone_number, u.description, u.create_time, u.update_time, r.name, r.role_key, r.description, r.create_time, r.update_time
		from tb_user u
		left join tb_user_role ur on u.id=ur.user_id
		inner join tb_role r on ur.role_id=r.id
    </sql>
	
	<select id="findList" parameterType="tech.pdai.springboot.postgre.mybatisplus.entity.query.UserQueryBean" resultMap="UserResult">
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
	
</mapper>
```

### 除了分页插件之外还提供了哪些插件？

插件都是基于拦截器实现的，MyBatis-Plus提供了如下[插件](https://baomidou.com/pages/2976a3/#mybatisplusinterceptor)：

- 自动分页: PaginationInnerInterceptor
- 多租户: TenantLineInnerInterceptor
- 动态表名: DynamicTableNameInnerInterceptor
- 乐观锁: OptimisticLockerInnerInterceptor
- sql 性能规范: IllegalSQLInnerInterceptor
- 防止全表更新与删除: BlockAttackInnerInterceptor

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos