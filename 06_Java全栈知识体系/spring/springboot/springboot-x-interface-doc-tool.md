# SpringBoot接口 - 如何生成接口文档之常用接口管理工具

> 上文我们看到可以通过Swagger系列可以快速生成API文档， 但是这种API文档生成是需要在接口上添加注解等，这表明这是一种侵入式方式； 那么有没有非侵入式方式呢？ 本文主要介绍非侵入式的方式及集成Smart-doc案例。我们构建体系时使用Smart-doc这类工具并不是目标，而是要了解非侵入方式能做到什么程度和技术思路, 最后**平衡**下来多数情况下多数人还是会选择Swagger+openapi技术栈的。 @pdai

## 准备知识点

> 需要了解Swagger侵入性和依赖性， 以及Smart-Doc这类工具如何解决这些问题。@pdai

https://github.com/YMFE/yapi

https://hellosean1025.github.io/yapi/devops/index.html

https://gitee.com/durcframework/torna

> TBD