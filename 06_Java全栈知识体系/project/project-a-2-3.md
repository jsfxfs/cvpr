# 青铜 - 后端CRUD之MyBatis栈演进2

> 本文是 **青铜 - 后端CRUD之MyBatis栈演进**的第二篇，上一篇是 [青铜 - 后端CRUD之MyBatis栈演进1](project-a-2-2.md)。@pdai

## 例子3：SpringBoot+MySQL+MyBatis代码生成+Thymeleaf

提示

伴随着很多相似的CRUD功能的出现，意味着开发内容是重复的，于是乎便出现了**代码生成**和**向上抽象封装**来减少重复。这里我们主要谈谈代码生成方式。

- 使用模板（vm, freemarker等）生成
- 使用IDE插件

  - 比如EasyCode

## 例子4：SpringBoot+MySQL+MyBatis注解+Thymeleaf

## 例子5：SpringBoot+MySQL+MyBatis-plus+Thymeleaf

## MyBatis技术栈重要的总结

提示

通过几个问题，我们来更加深入了解上面的例子和MyBatis技术栈。

### 第一个问题：上面的几个例子是最优雅的实现吗？

> 不是，如果放在前几年（五年前）可能是相对主流，现在绝不是。

简单说几点：

- 第一，从代码风格来看，源作者应该是吸收了早先SSM传统CRM后台框架的经验演进过来的，这个后面我会有两篇文章来帮你构建十年前项目是如何开发的认知；因为不是从头写的（考虑到代价, 沿用了原有的一些配置和Util等），所以必然不会是最新最优雅的方式，后续几点具体说明。
- 第二，过多的自定义的Util，而现有的项目项目中，Util一定不要自己造轮子，原则是优先使用[Guava](../develop/package/dev-package-x-google-guava.md)，[commons](../develop/package/dev-package-x-apache-common.md)等开源工具类；还有一些新的[hutool](../develop/package/dev-package-x-hu-tool.md)等工具库是可以满足绝大部分需求的，如果没有再添加。于此同时，如果项目规模稍微大一点和要求，还可以使用外观模式进行小量的封装，比如你同时使用了Guava，Common库中StringUtils，那么可以增加一个MyStringUtils，将常用方法融入这个类，对项目中所有类来说只使用MyStringUtils。此外这里的例子还有一些标注为@Component等模块作为util，造成了代码的耦合度增加。
- 第三，没有完全注解化，还有一部分是xml；使用**约定大于配置**一定是最优雅的必要条件，因为大部分starters是支持的，比如这里的mybatis-springboot-starter中已经提供了mybatis的配置，无需再使用xml方式的配置了。
- 第四，Mapper和Service层抽象的缺失：

比如Mapper里

```xml
  <delete id="deleteUserById" parameterType="Long">
 		delete from sys_user where user_id = #{userId}
 	</delete>
 	
 	<delete id="deleteUserByIds" parameterType="Long">
 		update sys_user set del_flag = '2' where user_id in
 		<foreach collection="array" item="userId" open="(" separator="," close=")">
 			#{userId}
        </foreach> 
 	</delete>
```

```xml
	<delete id="deleteRoleById" parameterType="Long">
 		delete from sys_role where role_id = #{roleId}
 	</delete>
 	
 	<delete id="deleteRoleByIds" parameterType="Long">
 	    update sys_role set del_flag = '2' where role_id in
 		<foreach collection="array" item="roleId" open="(" separator="," close=")">
 			#{roleId}
        </foreach> 
 	</delete>
```

这种类似的代码不就是重复么？不是可以抽象么？所以这里可以看下MyBatis-Plus中BaseMapper和JPA中CRUDRespositry的实现。

所以从这个角度来看，比较好的实现应该是(这里写个大概的思路）：

```java
@Mapper
public class XXXMapper<E，ID> extends xxxBaseMappper<E extends BaseEntity， ID extends XXID>{
  // 这里应该是空实现，基本的CRUD全部风封装至上层
}
```

同样的Service层也可以封装。

```java
@Service
public class XXXService<M，E，ID> extends xxxBaseServie<M Extends XXXMapper，E extends BaseEntity， ID extends XXID>{
  // 这里应该是空实现，基本的CRUD Service全部风封装至上层；可以Override，和添加新的
}
```

- 第五，更为优雅的Lamada语法使用，比如MyBatis-Plus WrapperQuery的lambda查询方式。

比如：

```java
/**
  * 名字为王姓并且(年龄小于40或者邮箱不为空)
  * sql：name like '王%' and (age < 40 or email is not null)
  */
@Test
public void selectLambda2() {
    LambdaQueryWrapper<User> lambdaQuery = Wrappers.<User>lambdaQuery();
    lambdaQuery.likeLeft(User::getName, "王")
            .lt(User::getAge, 40)
            .isNotNull(User::getEmail);
    List<Object> userList = userMapper.selectObjs(lambdaQuery);
    userList.forEach(System.out::println);
}

@Test
public void selectLambda3() {
    List<User> userList = new LambdaQueryChainWrapper<User>(userMapper)
            .like(User::getName, "雨")
            .ge(User::getAge, 20)
            .list();
    userList.forEach(System.out::println);
}
```

可以看下MyBatis-Plus[官方测试用例 WrapperTest.java](https://gitee.com/baomidou/mybatis-plus/blob/3fde155990917731b50e2aaa848cef20b403f263/mybatis-plus-core/src/test/java/com/baomidou/mybatisplus/core/test/WrapperTest.java)

- 第六，删除Fastjson等漏洞较多的使用库，改用Jackson；

关于JSON库可以参考 [常用类库 - JSON类库详解](../develop/package/dev-package-x-json.md)：

- 第七，注意下前端库的使用:
  - BootStrap推荐升级至V4；
  - jQuery低版本漏洞较多，推荐升级至3.4.1；
  - Select2插件不推荐使用，因为有xss漏洞，至今还没有修复；
  - ...

PS:商业系统上线前都会做[渗透测试](../develop/security/dev-security-y-pentest-workflow.md)，有这些漏洞是无法上线的。

### 第二个问题：既然不是最优雅的实现，为什么你还是给了上面的例子？

很好的问题，我从三个方面说明下：

- 第一：在学习例子时候，和真正在项目中使用是有一定的差异的: 项目中需要的是权衡编码的时间和代价，所以必定不会是最新最优雅的技术，且有可能你还是会需要维护一些老的代码，甚至于一些十几年前的代码。（PS：技术决策就是权衡，老板的利益永远是对的）
- 第二，并不是一上来给你最佳的实践，你就会更好的理解，因为最优雅意味着你写更少的代码，最少的代码意味着更多的封装（通常不是你实现的），在这种情况下，你觉得你会更好的理解？所以我拿了最流行（Star最多的）的Ruoyi项目抽象出例子，然后跳出代码本身，用上帝视角来思考并指出最优雅的形式(这里看第三个问题)。
- 第三：为了保持与后面代码的承接，我是从互联网上最为流行的Ruoyi项目抽象出来的 ，后面的文章会基于这个项目进行多方面的拓展，所以我希望上下文是能够循序渐进的向你阐述技术演进的，而不是一步步就写个最佳实践。

### 第三个问题： 什么样的实现是优雅的？

> 至少可以在如下几个方面使其更为优雅：

- **基于约定大于配置**

  - `MyBatis-plus`注解方式（不再使用xml）
  - Lamada方式实现，比如`WrapQuery`
- **实现一定的逻辑抽象**

  - 比如Dao（Mapper），Service层的抽象
  - 对于基础的CURD接口和功能应该被封装，而实现类基础应该是空实现；
- **减少自己写Util的量**

  - 推荐`Guava`，`Apache commons`，或者`hutool`等
  - 稍复杂项目可以考虑外观模式，比如你同时使用了Guava，Common库中StringUtils，那么可以增加一个MyStringUtils，将常用方法融入这个类，对项目中所有类来说只使用MyStringUtils。
- **如果使用模板，有几个要注意**

  - 尽量不使用IDEA提供的代码生成工具，表面上减少了工作量。其实有两个问题：
    - 第一，自定义能力差，代码逻辑稍微复杂一点，基本你需要改动，此时代码生成工具就是鸡肋，比如加入一些自定义的`日志注解`，`swagger注解`，`导出注解`，`权限注解`等；
    - 第二：你需要理解一点，凡是需要生成代码意味着重复的代码形式和工作，而封装和抽象是用来解决这个工作的最好方式，而不是生成代码；
  - 所以如果使用模板生成代码，那么使用自己写的模板生成是最好的；这里也有三点需要注意的：
    - 第一：上文提及的约定大于配置，这是趋势；
    - 第二：绝大部分重复通过抽象完成，其余部分（比如`类的申明`等，例如`Entity`，基于`Service`抽象继承后的`Service`类等等）通过模板实现；
    - 第三，将其它工具和配置一并加入模板中（比如自定义的`日志注解`，`swagger注解`，`导出注解`，`权限注解`以及`前端页面`等）。

### 第四个问题：如何理解你说的：凡是需要生成代码意味着重复的代码形式和工作？

> 我认为理解这一点是非常重要的，凡是需要生成代码意味着重复的代码形式和工作，肯定是可以使用抽象或者封装框架去实现的。试想下，如果我们可以做到通用的代码生成，它必然是可以通过更好的封装形式提供给你服务的。这么来说是比较抽象的，举个例子：

我们现有的认知都是通过`Entity->Mapper/Dao->Service->(Business)->Controller`这种代码结构的，所以如果需要我们想要实现CRUD的**通用**功能，基于上述理解我们不通过代码生成（因为重复），是可以完全抛弃掉这套代码结构的（那就是不用生成了），也就是完全封装至上层框架中；我们只需要配置数据源，封装的框架可以直接提供`CRUD Restful`功能。

有这样的框架？请百度搜索 - `DataWay`。也可以看下这两篇文章：

[在 Spring Boot 中使用 Dataway 配置数据查询接口](https://my.oschina.net/ta8210/blog/3234639)

[Dataway 配置数据接口时和前端进行参数对接](https://my.oschina.net/ta8210/blog/3236659)

但是`DataWay`能做到通用么? **并不能**，因为你会有自己的业务逻辑, 这表示它只会使用在很小的领域。所以多数情况下不要指望通过通用的代码生成工具去实现代码的生成来减少代码量，如果可以那么可定有类似`DataWay`的封装方式。这就是我在上个问题中我说的如果使用模板生成代码一定是结合一定的框架根据项目实际情况自定义编写的原因。