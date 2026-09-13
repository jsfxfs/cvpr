# 黄金 - 完整电商项目之后台(mall4j)

> Mall4j

## 学习项目

### 看代码的原则

- 始终持反思的态度：别人写的不一定就是完全对的，或者有其场景性；多问自己，为什么是这样，我能不能不这样？有没有更好的选择？
- 代码的结构是迎合业务的需求而变化着的，这点是至关重要的。代码结构往往是开发成本和业务的折中， 不是说代码这样很精致我们就这样做的，不是说这样炫酷我们就这样实现的。
- 注重总体的理解，而不是细节。

### 学习着手点

- 先看pom引入
- 对于不知道在哪里使用的类，或者想看之间的关联，先注释掉，看报错

### 准备知识

- Guava
- SpringBoot
- Java 8

## 开始学习之理解业务

### 一般电商有哪些业务

### 这个项目包含哪些业务

## 开始学习之后端学习

### 1. 后端 - 环境准备和配置

### 2. 后端 - 理解包结构

- 包的划分是按照模块划分还是按照逻辑层次？
- 包的统一版本管理
- 证书问题
- Readme

### 3. 后端 - Common包

- 什么内容应该放在common包？Bean和Security应该放common包吗？
- 统一的工具类
- 统一的序列化
- 统一的响应封装
- 统一的异常处理
- 统一的日志拦截
- 统一的常量定义
- 统一的配置（包括第三方组件配置）

  - 缓存配置 - Redis（接口幂等）
  - ORM层 - MyBatis配置
  - 文件上传 - 七牛云配置
  - 短信通知 - 阿里大鱼

### 4. 后端 - Bean包

- 理解DO，DTO，VO
- 理解Param
- 理解Mapper是否要和DO放一起？
- 理解层次和业务模块分包原则？
- lombok不一致
- 序列化的意义

### 5. 后端 - Security包

- AAA与HTTP Status Code
- 理解RBAC
- 理解SpringSecurity和Shiro
- SpringSecurity - Filter，Provider， Parser之间的关系

  - https://www.cnblogs.com/jeeweb/p/11818948.html
  - https://www.cnblogs.com/demingblog/p/10874753.html
- 普通用户和系统用户分离
- 登录登出
- 验证码
- 错误信息提示
- 权限控制
- AppConnect放这里是否合适

  - 如果不放在这里会出现鸡生蛋蛋生鸡的问题
- 里面Mpxxx开头的是否可以删除？

  - MpAuthenticationProvider
  - MpAuthenticationToken

### 6. 后端 - Service包

- 理解ORM
- 理解MyBatis，JPA等
- 理解MyBatisPlus
- MyBatisPlus相关配置和使用
- 为什么其它包里还有DAO相关的？
- 缓存的使用
- Service，Mapper, DO之间的关联
- 是否需要使用代码生成

### 7. 后端 - Mp包

- 微信小程序
- 微信公众号
- 微信支付

### 8. 后端 - API包

- 分布式ID - Snowflake
- Swagger2 接口文档

  - https://doc.xiaominfo.com/guide/i18n.html
- 资源管理 ResourceServer
- 授权管理 AuthorizationServerConfigurer
- Lisener 默认操作

  - 确认订单信息时的默认操作
  - 默认的购物车链进行组装时的操作
  - 确认订单信息时的默认操作
- 删除和编辑等数据操作并没有权限的控制，是否有需要做？

```java
/**
    * 删除订单配送地址
    */
@DeleteMapping("/deleteAddr/{addrId}")
@ApiOperation(value = "删除订单用户地址", notes = "根据地址id，删除用户地址")
@ApiImplicitParam(name = "addrId", value = "地址ID", required = true, dataType = "Long")
public ResponseEntity<String> deleteDvy(@PathVariable("addrId") Long addrId) {
    String userId = SecurityUtils.getUser().getUserId();
    UserAddr userAddr = userAddrService.getUserAddrByUserId(addrId, userId);
    if (userAddr == null) {
        return ResponseEntity.badRequest().body("该地址已被删除");
    }
    if (userAddr.getCommonAddr() == 1) {
        return ResponseEntity.badRequest().body("默认地址无法删除");
    }
    userAddrService.removeById(addrId);
    userAddrService.removeUserAddrByUserId(addrId, userId);
    return ResponseEntity.ok("删除地址成功");
}
```

### 9. 后端 - Quartz包

- Quartz基本使用
- Quartz任务持久化
- Quartz任务和任务日志
- 异步监听定时任务事件，解决job线程无故丢失的问题

### 10. 后端 - Sys包

- 系统日志切面
- 系统配置信息管理
- 系统日志查询
- 系统菜单管理
- RBAC - 系统用户和角色管理

### 11. 后端 - admin包

- Swagger Bootstrap UI 设置
  - 不同环境下控制
  - 开发环境接口授权 - [官网demo](https://gitee.com/xiaoym/swagger-bootstrap-ui-demo/blob/master/swagger-bootstrap-ui-demo/src/main/java/com/swagger/bootstrap/ui/demo/config/SwaggerConfiguration.java), [官网链接](https://doc.xiaominfo.com/guide/authorize.html)

### 12. 后端 - Docker