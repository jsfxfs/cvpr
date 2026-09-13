# 青铜 - 入门开发IDE，Hello World

> 正式开始开发前，从两个点出发，一个是开发工具，另外一个HelloWorld级别的应用开始。由于东西比较简单，我这里主要给些链接和例子， 大家都是聪明人，多一点行动力就行了，简单的东西百度下；主要是给你一个**一步步学习的思路和知识点**。另外还提供了两个helloworld级别的例子，你自己下载下来运行下感受下，这主要是**给你一个先入为主的认知**。@pdai

## IDEA下载和安装

> 工欲善其事必先利其器，首推IDEA，其次是Eclipse/STS。

- IDEA 下载和安装

  - [IDEA官网](https://www.jetbrains.com)
  - ... // 非社区版想破解的话网上找找破解方法就可以了
- IDEA 插件的安装

  - Spring Assist // 新版里面是这个名字
  - ... // 自己搜索就可以了

![](https://www.pdai.tech/images/project/project-b-1.png)

- [IDEA 常用配置和快捷键](https://segmentfault.com/a/1190000020289200)

  - Maven 仓库源
  - UTF-8
  - 代码块注释配置
  - 自动import配置
- 其它一些配置

  - 设置代码不自动折叠 File->Setting->Editor->General->Code Folding 将One-line methods去除即可

## SpringBoot - Hello World

> 如何写一个Hello World

看这篇文章的例子 [Spring Boot - Helloworld](../spring/Spring Boot - Helloworld.md)，关注如下几个问题：

- 如何通过Spring Assist工具初始化SpringBoot应用

![](https://www.pdai.tech/images/spring/springboot-helloworld-2.png)

- 思考如何通过maven初始化，如何自定义？

## SpringBoot - Swagger API

> 给你一个基于内存库H2的增删改例子

看这篇文章的例子[Spring Boot - Swagger UI](../spring/Spring Boot - Swagger UI.md)，关注如下几个问题（有个印象）：

- **代码分层结构**

![](https://www.pdai.tech/images/project/project-b-2.png)

- **接口文档化**

![](https://www.pdai.tech/images/spring/springboot-swagger-1.png)

- **JPA 是什么**？

  - 百度下
  - 看下[这篇文章](https://blog.csdn.net/u010837612/article/details/47610823)
- **H2 用来干啥**？

  - H2是一个短小精干的嵌入式数据库引擎，主要的特性包括：
    - 免费、开源、快速
    - 嵌入式的数据库服务器，支持集群
    - 提供JDBC、ODBC访问接口，提供基于浏览器的控制台管理程序
    - Java编写，可使用GCJ和IKVM.NET编译
    - 短小精干的软件，1M左右。
  - [官网](http://www.h2database.com/html/main.html)