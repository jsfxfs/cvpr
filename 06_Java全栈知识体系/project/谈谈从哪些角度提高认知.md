# 谈谈从哪些角度提高认知

> 上面如果你写了一段时间的代码，你会发现其实写代码是很容易的事。虽然一些技术点知识被集中放在这里，但是在白银和黄金阶段你可以已经需要开始逐步理解相关的知识点了。

- 钻石阶段 - Overview

  - 这个阶段需要思考什么
- 从代码优化 - 重构和优化

  - 重构机制之如何去掉多余的if else
- 从技术深度 - 知识点上深入

  - Java
    - 解耦机制之Java的SPI机制
  - Spring
    - 拦截机制之Filter和Inteceptor
    - 拦截机制之AOP切面拦截
    - IOC 依赖注入，控制反转
    - Spring Bean， IOC，容器
  - SpringBoot
    - SpringBoot自动配置机制
    - SpringBoot启动过程
    - SpringBootStarter依赖
    - 深入了解SpringBoot的启动过程 https://www.jianshu.com/p/cb5cb5937686
    - SpringBoot学习笔记 https://blog.hanqunfeng.com/2016/12/09/spring-boot-study/
- 从技术广度 - 业务演进带来广度

  - FastDFS集成 - 分布式文件存储
  - 接口 - 幂等设计
  - 搜索 - ElasticSearch
  - 流式处理 - Flink

> 技术归根到底还是为了解决问题，所以需要落地（即将技术点组织）项目化和平台化

- 从团队协作 - 平台化

  - 考虑项目的团队协作
    - 需求跟进 JIRA
    - 接口Mock - Moco
    - 文档管理wiki
  - 考虑代码管理
    - Git分支管理等
- 从流程自动化 - 自动化部署

  - 脚本化是自动化的前提
  - Docker容器化
  - 持续集成CI - Jenkins
  - 集成静态代码检查 - SonarCube
  - 持续交付CD，版本管理
- 从项目质量 - 项目质量保障

  - 程序员
    - 单元测试UT, 代码覆盖率
    - 代码评审code Review
  - 测试员
    - 功能 - 黑盒测试
    - 性能 - 压力测试
- 从项目上线 - 项目上线前做什么

  - 代码审计，三方库License等
  - 渗透测试
  - 全链路压测
- 从项目运维 - 监控运维及自动化