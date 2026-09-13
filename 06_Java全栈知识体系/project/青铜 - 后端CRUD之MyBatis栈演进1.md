# 青铜 - 后端CRUD之MyBatis栈演进1

> 在上一节，我们安装了IDEA，也看了两个基础的例子，你可能很容易把例子跑起来，但是不懂它是怎么工作的。在初学之际这是正常的，这个阶段你了解的不够多，你也是没有太多的分辨和提问的能力的, 无需焦虑，一步步坚持高效学习就可以了，做对的事，其它交给时间。本节主要介绍最基础的增删查改的例子的第一部分，用国内最流行的框架SpringBoot+MyBatis栈，这里我不会每一个步骤都写，原因我在前面也写了，**你更缺的是方向性的指引，循序渐进的进阶例子会让你有大局观（而不是过早的沉溺于细节本身）**, 所以这里的例子也是适合有一定经验的开发人员研究和反思的。@pdai

> 为避免大量内容涌入，而给刚学习的开发者造成困扰，这里将**后端CRUD之MyBatis栈演进**分成两篇文章，本文是第第一篇， 下面是[青铜 - 后端CRUD之MyBatis栈演进2](青铜 - 后端CRUD之MyBatis栈演进2.md)。

## 学前几点（给刚入门的）

提示

对于初级的开发者，通常头脑中是一团浆糊，你需要做的是把用来焦虑的时间投入到学习中来；在学习前，从如下几个小点来进阶吧。对于有一定开发经验的开发者来说，后续几个例子仍你是很好的学习和开发的模板。@pdai

### 为什么用SpringBoot

> 框架的出现就是为了将繁杂的重复性工作抽象出去，让开发逐步用最小的代码量快速实现功能。@pdai

- **为什么学SpringBoot之前我会推荐学习SpringMVC**

我在前文也提到，我推荐先学习《[跟开涛学 SpringMVC](/files/kaitao-springMVC.pdf)》。因为SpringMVC是基础，可以构筑你的web认知，而且你看的懂，这样循序渐进你可以很快理解。这是有很好的承接的，而不是脱离了SpringBoot你啥也不知道。

![](https://www.pdai.tech/images/project/project-b-5.png)

- **为什么写代码是用SpringBoot**

> 最主要还是因为SpringBoot目前已经成为开发主流的选择。我们顺便看下网上关于springboot的核心功能和优势：

**Spring Boot 核心功能**

- 1）独立运行的 Spring 项目

Spring Boot 可以以 jar 包的形式独立运行，运行一个 Spring Boot 项目只需通过 java–jar xx.jar 来运行。

- 2）内嵌 Servlet 容器

Spring Boot 可选择内嵌 Tomcat、Jetty 或者 Undertow，这样我们无须以 war 包形式部署项目。

- 3）提供 starter 简化 Maven 配置

Spring 提供了一系列的 starter pom 来简化 Maven 的依赖加载，例如，当你使用了spring-boot-starter-web 时，会自动加入依赖包。

- 4）自动配置 Spring

Spring Boot 会根据在类路径中的 jar 包、类，为 jar 包里的类自动配置 Bean，这样会极大地减少我们要使用的配置。当然，Spring Boot 只是考虑了大多数的开发场景，并不是所有的场景，若在实际开发中我们需要自动配置 Bean，而 Spring Boot 没有提供支持，则可以自定义自动配置。

- 5）准生产的应用监控

Spring Boot 提供基于 http、ssh、telnet 对运行时的项目进行监控。

- 6）无代码生成和 xml 配置

Spring Boot 的神奇的不是借助于代码生成来实现的，而是通过条件注解来实现的，这是 Spring 4.x 提供的新特性。Spring 4.x 提倡使用 Java 配置和注解配置组合，而 Spring Boot 不需要任何 xml 配置即可实现 Spring 的所有配置。

**Spring Boot的优点**

- 快速构建项目。
- 对主流开发框架的无配置集成。
- 项目可独立运行，无须外部依赖Servlet容器。
- 提供运行时的应用监控。
- 极大地提高了开发、部署效率。
- 与云计算的天然集成。

### 什么是JDBC，ORM，MyBatis

- **什么是JDBC**

JDBC（JavaDataBase Connectivity）就是Java数据库连接，说白了就是用Java语言来操作数据库。原来我们操作数据库是在控制台使用SQL语句来操作数据库，JDBC是用Java语言向数据库发送SQL语句。

![](https://www.pdai.tech/images/project/project-b-4.png)

- **什么是ORM**

对象关系映射（Object Relational Mapping，简称ORM）， 简单的说，**ORM是通过使用描述对象和数据库之间映射的元数据，将java程序中的对象自动持久化到关系数据库中**。本质上就是将数据从一种形式转换到另外一种形式，具体如下：

![](https://www.pdai.tech/images/project/project-b-3.png)

具体映射：

- 数据库的表（table） --> 类（class）
- 记录（record，行数据）--> 对象（object）
- 字段（field）--> 对象的属性（attribute）
- **什么是MyBatis**

MyBatis是对JDBC的封装， 是常用的ORM框架之一。MyBatis是一个支持普通SQL查询，存储过程和高级映射的优秀持久层框架。MyBatis消除了几乎所有的JDBC代码和参数的手工设置以及对结果集的检索封装。MyBatis可以使用简单的XML或注解用于配置和原始映射，**将接口和Java的POJO（Plain Old Java Objects，普通的Java对象）映射成数据库中的记录**。

### 为什么初学要从CRUD开发开始

- **什么CRUD**

crud是指在做计算处理时的增加(Create)、读取(Read)、更新(Update)和删除(Delete)几个单词的首字母简写。crud主要被用在描述软件系统中数据库或者持久层的基本操作功能。

- **为什CRUD是基础**

在常见的开发中，最为基础，也是业务单元的基础。这就是好多入门级程序员一直在做的事情，所以一开始我们需要学习CRUD，并且逐渐摸出它的套路，提升自己的效率。

## SpringBoot - MySQL+MyBatis栈演进

提示

好了，进入SpringBoot+MyBatis开发正题；在开发之前有必要了解下，基于MyBatis系列这个**技术栈的发展过程**以及如何通过**循序渐进的例子**进行提升, 这对你的进阶有很大好处，因为站的高度一开始就比别人高，大脑会潜移默化的会携带对它深入思考。

### MyBatis栈技术演进

> MyBatis栈经历了什么的技术演进的？

- JDBC，自行封装JDBCUtil
  - Java5的时代，还是自行封装JDBC的Util的
- IBatis->MyBatis,基于xml配置
  - 出现了IBatis等ORM框架，且基于xml配置的开始流行
- MyBatis衍生：PageHelper分页
  - 衍生出一些基于MyBatis的插件，比如流行的分页实现PageHelper
- MyBatis衍生：相关工具
  - 为了减少重复编码，衍生出了MyBatis代码生成工具
  - IDE一些工具和插件等
- MyBatis基于注解的配置
  - 基于注解的实现逐渐替换掉基于xml配置的实现
- MyBatis-Plus
  - 国产的融合封装

### MyBatis栈技术例子

> 如何通过例子进阶呢？这里给5个相关例子

- **第一个例子** [项目代码](https://github.com/realpdai/springboot-project-learn/tree/master/B01-springboot-crud-mybatis-xml-demo)

  - MyBatis,基于xml配置的增删查改
  - PageHelper分页
  - 后端模板Thymeleaf
- **第二个例子** [项目代码](https://github.com/realpdai/springboot-project-learn/tree/master/B02-springboot-crud-mybatis-xml-multi-demo)

  - 第一个例子基础上
  - 多个关联表操作
  - Druid线程池
- **第三个例子**

  - 代码生成工具
  - MyBatis IDEA相关插件
- **第四个例子**

  - 第一个例子基础上
  - 改为MyBatis基于注解配置的增删查改
- **第五个例子**

  - 第一个例子基础上
  - 改为MyBatis-plus增删查改

## 例子1：SpringBoot+MySQL+MyBatis配置+Thymeleaf

提示

我们从MyBatis基于xml配置的实现方式开始学起， 最基本的增删查改例子，第一个例子多写几点，后续例子有一定的关联性，所以只会写差异的地方。

### 这个例子实现什么样的功能

> CURD 主体功能...

- 列表

![](https://www.pdai.tech/images/project/project-b-6.png)

- 增加

![](https://www.pdai.tech/images/project/project-b-7.png)

- 修改

![](https://www.pdai.tech/images/project/project-b-8.png)

- 搜索

![](https://www.pdai.tech/images/project/project-b-9.png)

### 如何把例子跑起来

> 代码在这里：[项目代码](https://github.com/realpdai/springboot-project-learn/tree/master/B01-springboot-crud-mybatis-xml-demo), 这个项目是我从开源项目Ruoyi中抠出来的并做了部分修改，方便大家学习使用。

- 数据库

  - 导入sql 文件

    ![](https://www.pdai.tech/images/project/project-b-10.png)
  - 修改application.yml中数据库相关配置
- 跑代码实例

![](https://www.pdai.tech/images/project/project-b-11.png)

- 代码的层次结构

![](https://www.pdai.tech/images/project/project-b-12.png)

### MyBatis相关配置和实现

> MyBatis如何配置的呢

- Pom

```xml
<!-- SpringBoot集成mybatis框架 -->
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>${mybatis.spring.boot.starter.version}</version>
</dependency>

<!-- pagehelper 分页插件 -->
<dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper-spring-boot-starter</artifactId>
    <version>${pagehelper.spring.boot.starter.version}</version>
</dependency>
```

- application.yml

```yaml
# orm
mybatis:
  mapper-locations: classpath:mybatis/mapper/*.xml
  type-aliases-package: tech.pdai.mybatis.xml.web.*.domain
  configuration:
    cache-enabled: true
    use-generated-keys: true
    default-executor-type: REUSE
    #log-impl: SLF4J
    use-actual-param-name: true
```

- mapper

代码

```java
@Mapper
public interface UserMapper {
//...
}
```

对应

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="tech.pdai.mybatis.xml.web.system.user.mapper.UserMapper">

	//...
	
</mapper>
```

### MyBatis 分页PageHelper

> PageHelper是早期MyBatis技术栈中最为常用的分页方式。（早先常见的面试题就有：如何实现数据库的分页？有哪几种方式？）

- **如何使用PageHelper呢**?

[看官网的介绍](https://github.com/pagehelper/Mybatis-PageHelper/blob/master/wikis/zh/HowToUse.md)

PageHelper有哪些使用方式呢？

```java
//第一种，RowBounds方式的调用
List<User> list = sqlSession.selectList("x.y.selectIf", null, new RowBounds(0, 10));

//第二种，Mapper接口方式的调用，推荐这种使用方式。
PageHelper.startPage(1, 10);
List<User> list = userMapper.selectIf(1);

//第三种，Mapper接口方式的调用，推荐这种使用方式。
PageHelper.offsetPage(1, 10);
List<User> list = userMapper.selectIf(1);

//第四种，参数方法调用
//存在以下 Mapper 接口方法，你不需要在 xml 处理后两个参数
public interface CountryMapper {
    List<User> selectByPageNumSize(
            @Param("user") User user,
            @Param("pageNum") int pageNum, 
            @Param("pageSize") int pageSize);
}
//配置supportMethodsArguments=true
//在代码中直接调用：
List<User> list = userMapper.selectByPageNumSize(user, 1, 10);

//第五种，参数对象
//如果 pageNum 和 pageSize 存在于 User 对象中，只要参数有值，也会被分页
//有如下 User 对象
public class User {
    //其他fields
    //下面两个参数名和 params 配置的名字一致
    private Integer pageNum;
    private Integer pageSize;
}
//存在以下 Mapper 接口方法，你不需要在 xml 处理后两个参数
public interface CountryMapper {
    List<User> selectByPageNumSize(User user);
}
//当 user 中的 pageNum!= null && pageSize!= null 时，会自动分页
List<User> list = userMapper.selectByPageNumSize(user);

//第六种，ISelect 接口方式
//jdk6,7用法，创建接口
Page<User> page = PageHelper.startPage(1, 10).doSelectPage(new ISelect() {
    @Override
    public void doSelect() {
        userMapper.selectGroupBy();
    }
});
//jdk8 lambda用法
Page<User> page = PageHelper.startPage(1, 10).doSelectPage(()-> userMapper.selectGroupBy());

//也可以直接返回PageInfo，注意doSelectPageInfo方法和doSelectPage
pageInfo = PageHelper.startPage(1, 10).doSelectPageInfo(new ISelect() {
    @Override
    public void doSelect() {
        userMapper.selectGroupBy();
    }
});
//对应的lambda用法
pageInfo = PageHelper.startPage(1, 10).doSelectPageInfo(() -> userMapper.selectGroupBy());

//count查询，返回一个查询语句的count数
long total = PageHelper.count(new ISelect() {
    @Override
    public void doSelect() {
        userMapper.selectLike(user);
    }
});
//lambda
total = PageHelper.count(()->userMapper.selectLike(user));
```

- **这个例子中是如何使用的**？

> 我们看下这个例子中是如何使用的

我们看到在UserController中：

```java
@PostMapping("/list")
@ResponseBody
public TableDataInfo list(User user) {
    startPage();
    List<User> list = userService.selectUserList(user);
    return getDataTable(list);
}
```

其中startPage方法：

```java
/**
  * 设置请求分页数据
  */
protected void startPage() {
    PageDomain pageDomain = TableSupport.buildPageRequest();
    Integer pageNum = pageDomain.getPageNum();
    Integer pageSize = pageDomain.getPageSize();
    if (StringUtils.isNotNull(pageNum) && StringUtils.isNotNull(pageSize)) {
        String orderBy = SqlUtil.escapeOrderBySql(pageDomain.getOrderBy());
        PageHelper.startPage(pageNum, pageSize, orderBy);
    }
}
```

再看下PageDomain中buildPageRequest方法的封装：

```java
public static PageDomain getPageDomain() {
    PageDomain pageDomain = new PageDomain();
    pageDomain.setPageNum(ServletUtils.getParameterToInt(Constants.PAGE_NUM));
    pageDomain.setPageSize(ServletUtils.getParameterToInt(Constants.PAGE_SIZE));
    pageDomain.setOrderByColumn(ServletUtils.getParameter(Constants.ORDER_BY_COLUMN));
    pageDomain.setIsAsc(ServletUtils.getParameter(Constants.IS_ASC));
    return pageDomain;
}
```

通过上述的代码，我们可以看出，这里使用的是中规中矩的第二种方式。在此基础上进行了一些封装：

1. 考虑到其它CURD中查询也需要分页，所以将startPage放在了父类Controller中；
2. 考虑到统一的pageNum和pageSize等，将其定为常量并封装为一个PageDomain; 同时前端也可以进行相应封装。
3. 考虑到获取request中获取参数值，所以这里再封装一个ServletUtils...

- **PageHelper是如何实现分页的**？

> 我们知道如何使用PageHelper后，我们发现使用`PageHelper.startPage(pageNum, pageSize, orderBy)`方法后的第一个select是具备分页能力的，那它是如何做到的呢？

理解它的原理，有两个点：

1. 第一，相对对于JDBC这种嵌入式的分页而言，PageHelper分页是独立的，能做到独立分页查询，那它**必然是通过某个拦截点进行了拦截，这样它才能够进行解耦分离出分页**。
2. 第二，我们通过`PageHelper.startPage(pageNum, pageSize, orderBy)`方法后的第一个select是具备分页能力的，那它**必然缓存了分页信息，同时结合线程知识，这里必然使用的是本地栈ThreadLocal**，即每个线程有一个本地缓存。

所以结合这两点，聪明的你就会想到它大概是如何实现的，关键就是两点（拦截，ThreadLocal), 我们看下源码：

简单看下拦截

```java
/**
 * Mybatis拦截器方法
 *
 * @param invocation 拦截器入参
 * @return 返回执行结果
 * @throws Throwable 抛出异常
 */
public Object intercept(Invocation invocation) throws Throwable {
    if (autoRuntimeDialect) {
        SqlUtil sqlUtil = getSqlUtil(invocation);
        return sqlUtil.processPage(invocation);
    } else {
        if (autoDialect) {
            initSqlUtil(invocation);
        }
        return sqlUtil.processPage(invocation);
    }
}
```

进而看下`sqlUtil.processPage(invocation);`方法

```java
/**
 *
 * @param invocation 拦截器入参
 * @return 返回执行结果
 * @throws Throwable 抛出异常
 */
private Object _processPage(Invocation invocation) throws Throwable {
    final Object[] args = invocation.getArgs();
    Page page = null;
    //支持方法参数时，会先尝试获取Page
    if (supportMethodsArguments) {
        // 从线程本地变量中获取Page信息，就是我们刚刚设置的
        page = getPage(args);
    }
    //分页信息
    RowBounds rowBounds = (RowBounds) args[2];
    //支持方法参数时，如果page == null就说明没有分页条件，不需要分页查询
    if ((supportMethodsArguments && page == null)
            //当不支持分页参数时，判断LocalPage和RowBounds判断是否需要分页
            || (!supportMethodsArguments && SqlUtil.getLocalPage() == null && rowBounds == RowBounds.DEFAULT)) {
        return invocation.proceed();
    } else {
        //不支持分页参数时，page==null，这里需要获取
        if (!supportMethodsArguments && page == null) {
            page = getPage(args);
        }
        // 进入查看
        return doProcessPage(invocation, page, args);
    }
}
```

所以`startPage方法`和这里的`getPage(args);`这方法里应该包含了ThreadLocal中设置和获取分页参数的，让我们看下startPage方法即可：

```java
public static <E> Page<E> startPage(int pageNum, int pageSize, boolean count, Boolean reasonable, Boolean pageSizeZero) {
    Page<E> page = new Page(pageNum, pageSize, count);
    page.setReasonable(reasonable);
    page.setPageSizeZero(pageSizeZero);
    Page<E> oldPage = getLocalPage();
    if (oldPage != null && oldPage.isOrderByOnly()) {
        page.setOrderBy(oldPage.getOrderBy());
    }

    setLocalPage(page);
    return page;
}
// ...
protected static final ThreadLocal<Page> LOCAL_PAGE = new ThreadLocal();

protected static void setLocalPage(Page page) {
    LOCAL_PAGE.set(page); // 看这里
}

// ...
```

> 所以这里提示下想进阶的开发者，源码的阅读是伴随着思路现行的（有了思路，简单看源码），而不是直接源码。

- **使用PageHelper有何注意点**？

> [看官网的说明](https://github.com/pagehelper/Mybatis-PageHelper/blob/master/wikis/zh/Important.md)

1. 只有紧跟在`PageHelper.startPage`方法后的**第一个**Mybatis的**查询（Select）**方法会被分页。
2. 请不要配置多个分页插件：请不要在系统中配置多个分页插件(使用Spring时,`mybatis-config.xml`和`Spring<bean>`配置方式，请选择其中一种，不要同时配置多个分页插件)！
3. 分页插件不支持带有`for update`语句的分页：对于带有`for update`的sql，会抛出运行时异常，对于这样的sql建议手动分页，毕竟这样的sql需要重视。
4. 分页插件不支持嵌套结果映射: 由于嵌套结果方式会导致结果集被折叠，因此分页查询的结果在折叠后总数会减少，所以无法保证分页结果数量正确。

- **如何评价下这个例子中PageHelper的封装和使用**？

> 让我们进一步思考下，PageHelper在这个例子中封装和使用是否优雅。

**就使用PageHelper本身而言**，第二种和第三种方式较为中规中矩，它是早前绝大多数的使用方式。并不是说中规中矩就是不好的，很多场景下保守能让团队的绝大多数人接受便是好的方式。当更多的人接受Java8 lambda方式后，`Page<User> page = PageHelper.startPage(1, 10).doSelectPage(()-> userMapper.selectGroupBy());`这种方式显然对于他们来说更为优雅。

**就本例对PageHelper的封装来看**，通常而言针对PageHelper封装有两个方式，一种是封装PageUtils，另一种就是放在上层Controller中， 这个例子中使用第二种。它并不是非常完美的封装方式，但确实是在有限的需求内是一个完整的封装。需要记住一点，过多的设计和封装也没有必要，重点在于封装是伴随着需求的改变而适度调整而来的。这个例子中可能出现需求变更从而影响其封装的点，比如排序可能是组合排序，比如先按照A字段的升序再按照B字段的降序排序，比如SQLUtil等带来的Util冗余等。

**就分页未来来看**，PageHelper不是长远的趋势，真正长远的趋势应该是被ORM融合，并且考虑更多的适用场景提供各种常见实现方式的封装功能（即约定大于实现中的约定），同时结合builder参数构建和lambda方式写法等语言特性写法上做到优雅。所以你可以看到JPA，MyBatis-plus等中相关的封装和实现就是这种趋势。

### Thymeleaf模板

> 我们可以看到前端是使用的Thyemeleaf，那Thymeleaf是如何使用，解析出页面的呢？

### 前端的封装

> 多个CURD时，肯定需要考虑前端的封装了，我们看下前端如何封装的。

## 例子2：SpringBoot+MySQL+MyBatis配置（多表）+Thymeleaf

提示

上述例子是一个非常简单的单表例子，接下来我们看下如何表的关联(包含一对多和一对一)等。

### 项目源码

> [项目代码](https://github.com/realpdai/springboot-project-learn/tree/master/B02-springboot-crud-mybatis-xml-multi-demo), 代码从ruoyi中抽出整理，形式上是第一个例子的拓展。

### 这个例子增加了什么功能

> 这个例子是上一个例子的延伸，我们看下功能上增加了什么

- 用户管理：关联角色,关联部门,及通过部门过滤用户

![](https://www.pdai.tech/images/project/project-b-14.png)

![](https://www.pdai.tech/images/project/project-b-15.png)

- 角色管理

![](https://www.pdai.tech/images/project/project-b-13.png)

- 部门管理（树形结构）

![](https://www.pdai.tech/images/project/project-b-16.png)

### MyBatis多表关联

> 我们来看下角色（一对多，一个用户有多个角色）和部门（一对一，一个用户属于一个部门）是如何实现的。

- User

```java
public class User extends BaseEntity {

    // ...

    /**
     * 部门对象
     */
    private Dept dept;

    private List<Role> roles;

}
```

- User和Role的关联类

```java
public class UserRole {
    /**
     * 用户ID
     */
    private Long userId;

    /**
     * 角色ID
     */
    private Long roleId;

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public Long getRoleId() {
        return roleId;
    }

    public void setRoleId(Long roleId) {
        this.roleId = roleId;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this, ToStringStyle.MULTI_LINE_STYLE)
                .append("userId", getUserId())
                .append("roleId", getRoleId())
                .toString();
    }
}
```

- UserMapper中通过association关联dept，和通过collection关联role集合。

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
"http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="tech.pdai.mybatis.xml.web.system.user.mapper.UserMapper">

	<resultMap type="tech.pdai.mybatis.xml.web.system.user.domain.User" id="UserResult">
		<id     property="userId"       column="user_id"      />
		<result property="deptId"       column="dept_id"      />
		<result property="loginName"    column="login_name"   />
		<result property="userName"     column="user_name"    />
		<result property="email"        column="email"        />
		<result property="phonenumber"  column="phonenumber"  />
		<result property="sex"          column="sex"          />
		<result property="avatar"       column="avatar"       />
		<result property="status"       column="status"       />
		<result property="delFlag"      column="del_flag"     />
		<result property="createBy"     column="create_by"    />
		<result property="createTime"   column="create_time"  />
		<result property="updateBy"     column="update_by"    />
		<result property="updateTime"   column="update_time"  />
		<result property="remark"       column="remark"       />
		<association property="dept"    column="dept_id" javaType="tech.pdai.mybatis.xml.web.system.dept.domain.Dept" resultMap="deptResult" />
		<collection  property="roles"   javaType="java.util.List"        resultMap="RoleResult" />
	</resultMap>
	
	<resultMap id="deptResult" type="tech.pdai.mybatis.xml.web.system.dept.domain.Dept">
		<id     property="deptId"   column="dept_id"     />
		<result property="parentId" column="parent_id"   />
		<result property="deptName" column="dept_name"   />
		<result property="orderNum" column="order_num"   />
		<result property="leader"   column="leader"   />
		<result property="status"   column="dept_status" />
	</resultMap>
	
	<resultMap id="RoleResult" type="tech.pdai.mybatis.xml.web.system.role.domain.Role">
		<id     property="roleId"       column="role_id"        />
		<result property="roleName"     column="role_name"      />
		<result property="roleKey"      column="role_key"       />
		<result property="roleSort"     column="role_sort"      />
		<result property="dataScope"    column="data_scope"     />
		<result property="status"       column="role_status"    />
	</resultMap>
	
	<sql id="selectUserVo">
        select  u.user_id, u.dept_id, u.login_name, u.user_name, u.email, u.avatar, u.phonenumber, u.sex, u.status, u.del_flag, u.login_ip, u.login_date, u.create_time, u.remark,
       		    d.dept_id, d.parent_id, d.dept_name, d.order_num, d.leader, d.status as dept_status,
       		    r.role_id, r.role_name, r.role_key, r.role_sort, r.data_scope, r.status as role_status
		from sys_user u
			 left join sys_dept d on u.dept_id = d.dept_id
			 left join sys_user_role ur on u.user_id = ur.user_id
			 left join sys_role r on r.role_id = ur.role_id
    </sql>
	
	<select id="selectUserList" parameterType="tech.pdai.mybatis.xml.web.system.user.domain.User" resultMap="UserResult">
		select u.user_id, u.dept_id, u.login_name, u.user_name, u.email, u.avatar, u.phonenumber, u.sex, u.status, u.del_flag, u.login_ip, u.login_date, u.create_by, u.create_time, u.remark, d.dept_name, d.leader from sys_user u
		left join sys_dept d on u.dept_id = d.dept_id
		where u.del_flag = '0'
		<if test="loginName != null and loginName != ''">
			AND u.login_name like concat('%', #{loginName}, '%')
		</if>
		<if test="status != null and status != ''">
			AND u.status = #{status}
		</if>
		<if test="phonenumber != null and phonenumber != ''">
			AND u.phonenumber like concat('%', #{phonenumber}, '%')
		</if>
		<if test="params.beginTime != null and params.beginTime != ''"><!-- 开始时间检索 -->
			AND date_format(u.create_time,'%y%m%d') &gt;= date_format(#{params.beginTime},'%y%m%d')
		</if>
		<if test="params.endTime != null and params.endTime != ''"><!-- 结束时间检索 -->
			AND date_format(u.create_time,'%y%m%d') &lt;= date_format(#{params.endTime},'%y%m%d')
		</if>
		<if test="deptId != null and deptId != 0">
			AND (u.dept_id = #{deptId} OR u.dept_id IN ( SELECT t.dept_id FROM sys_dept t WHERE FIND_IN_SET (#{deptId},ancestors) ))
		</if>
		<!-- 数据范围过滤 -->
		${params.dataScope}
	</select>
	
	<select id="selectAllocatedList" parameterType="tech.pdai.mybatis.xml.web.system.user.domain.User" resultMap="UserResult">
	    select distinct u.user_id, u.dept_id, u.login_name, u.user_name, u.email, u.avatar, u.phonenumber, u.status, u.create_time
	    from sys_user u
			 left join sys_dept d on u.dept_id = d.dept_id
			 left join sys_user_role ur on u.user_id = ur.user_id
			 left join sys_role r on r.role_id = ur.role_id
	    where u.del_flag = '0' and r.role_id = #{roleId}
	    <if test="loginName != null and loginName != ''">
			AND u.login_name like concat('%', #{loginName}, '%')
		</if>
		<if test="phonenumber != null and phonenumber != ''">
			AND u.phonenumber like concat('%', #{phonenumber}, '%')
		</if>
		<!-- 数据范围过滤 -->
		${params.dataScope}
	</select>
	
	<select id="selectUnallocatedList" parameterType="tech.pdai.mybatis.xml.web.system.user.domain.User" resultMap="UserResult">
	    select distinct u.user_id, u.dept_id, u.login_name, u.user_name, u.email, u.avatar, u.phonenumber, u.status, u.create_time
	    from sys_user u
			 left join sys_dept d on u.dept_id = d.dept_id
			 left join sys_user_role ur on u.user_id = ur.user_id
			 left join sys_role r on r.role_id = ur.role_id
	    where u.del_flag = '0' and (r.role_id != #{roleId} or r.role_id IS NULL)
	    and u.user_id not in (select u.user_id from sys_user u inner join sys_user_role ur on u.user_id = ur.user_id and ur.role_id = #{roleId})
	    <if test="loginName != null and loginName != ''">
			AND u.login_name like concat('%', #{loginName}, '%')
		</if>
		<if test="phonenumber != null and phonenumber != ''">
			AND u.phonenumber like concat('%', #{phonenumber}, '%')
		</if>
		<!-- 数据范围过滤 -->
		${params.dataScope}
	</select>
	
	<select id="selectUserByLoginName" parameterType="String" resultMap="UserResult">
	    <include refid="selectUserVo"/>
		where u.login_name = #{userName}
	</select>
	
	<select id="selectUserByPhoneNumber" parameterType="String" resultMap="UserResult">
		<include refid="selectUserVo"/>
		where u.phonenumber = #{phonenumber}
	</select>
	
	<select id="selectUserByEmail" parameterType="String" resultMap="UserResult">
	    <include refid="selectUserVo"/>
		where u.email = #{email}
	</select>
	
	<select id="checkLoginNameUnique" parameterType="String" resultType="int">
		select count(1) from sys_user where login_name=#{loginName}
	</select>
	
	<select id="checkPhoneUnique" parameterType="String" resultMap="UserResult">
		select user_id, phonenumber from sys_user where phonenumber=#{phonenumber}
	</select>
	
	<select id="checkEmailUnique" parameterType="String" resultMap="UserResult">
		select user_id, email from sys_user where email=#{email}
	</select>
	
	<select id="selectUserById" parameterType="Long" resultMap="UserResult">
		<include refid="selectUserVo"/>
		where u.user_id = #{userId}
	</select>
	
	<delete id="deleteUserById" parameterType="Long">
 		delete from sys_user where user_id = #{userId}
 	</delete>
 	
 	<delete id="deleteUserByIds" parameterType="Long">
 		update sys_user set del_flag = '2' where user_id in
 		<foreach collection="array" item="userId" open="(" separator="," close=")">
 			#{userId}
        </foreach> 
 	</delete>
 	
 	<update id="updateUser" parameterType="tech.pdai.mybatis.xml.web.system.user.domain.User">
 		update sys_user
 		<set>
 			<if test="deptId != null and deptId != 0">dept_id = #{deptId},</if>
 			<if test="loginName != null and loginName != ''">login_name = #{loginName},</if>
 			<if test="userName != null and userName != ''">user_name = #{userName},</if>
 			<if test="email != null and email != ''">email = #{email},</if>
 			<if test="phonenumber != null and phonenumber != ''">phonenumber = #{phonenumber},</if>
 			<if test="sex != null and sex != ''">sex = #{sex},</if>
 			<if test="avatar != null and avatar != ''">avatar = #{avatar},</if>
 			<if test="status != null and status != ''">status = #{status},</if>
 			<if test="updateBy != null and updateBy != ''">update_by = #{updateBy},</if>
 			<if test="remark != null">remark = #{remark},</if>
 			update_time = sysdate()
 		</set>
 		where user_id = #{userId}
	</update>
 	
 	<insert id="insertUser" parameterType="tech.pdai.mybatis.xml.web.system.user.domain.User" useGeneratedKeys="true" keyProperty="userId">
 		insert into sys_user(
 			<if test="userId != null and userId != 0">user_id,</if>
 			<if test="deptId != null and deptId != 0">dept_id,</if>
 			<if test="loginName != null and loginName != ''">login_name,</if>
 			<if test="userName != null and userName != ''">user_name,</if>
 			<if test="email != null and email != ''">email,</if>
 			<if test="avatar != null and avatar != ''">avatar,</if>
 			<if test="phonenumber != null and phonenumber != ''">phonenumber,</if>
 			<if test="sex != null and sex != ''">sex,</if>
 			<if test="status != null and status != ''">status,</if>
 			<if test="createBy != null and createBy != ''">create_by,</if>
 			<if test="remark != null and remark != ''">remark,</if>
 			create_time
 		)values(
 			<if test="userId != null and userId != ''">#{userId},</if>
 			<if test="deptId != null and deptId != ''">#{deptId},</if>
 			<if test="loginName != null and loginName != ''">#{loginName},</if>
 			<if test="userName != null and userName != ''">#{userName},</if>
 			<if test="email != null and email != ''">#{email},</if>
 			<if test="avatar != null and avatar != ''">#{avatar},</if>
 			<if test="phonenumber != null and phonenumber != ''">#{phonenumber},</if>
 			<if test="sex != null and sex != ''">#{sex},</if>
 			<if test="status != null and status != ''">#{status},</if>
 			<if test="createBy != null and createBy != ''">#{createBy},</if>
 			<if test="remark != null and remark != ''">#{remark},</if>
 			sysdate()
 		)
	</insert>
	
</mapper>
```

- User和Role之间是一对多关系，所以是独立的表，在操作用户时需要同步删除User和Role的关联表UserRole

比如

```java
/**
  * 通过用户ID删除用户
  *
  * @param userId 用户ID
  * @return 结果
  */
@Override
public int deleteUserById(Long userId) {
    // 删除用户与角色关联
    userRoleMapper.deleteUserRoleByUserId(userId);
    return userMapper.deleteUserById(userId);
}
```