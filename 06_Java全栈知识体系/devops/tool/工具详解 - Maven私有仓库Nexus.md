# 工具详解 - Maven私有仓库Nexus

> Maven私有仓库Nexus介绍和使用, 工具的使用查查资料就可以，给几个链接减少下查找的时间。@pdai

## Nexus是什么

1、有些公司都不提供外网给项目组人员，因此就不能使用maven访问远程的仓库地址，所以很有必要在局域网里找一台有外网权限的机器，搭建nexus私服，然后开发人员连到这台私服上，这样的话就可以通过这台搭建了nexus私服的电脑访问maven的远程仓库。而且自己maven私服更容易维护，由于在内网，公司的开发人员从maven私服迁出jar到本地仓库更快。

2、当需要上传第三方或者自己的jar到maven仓库时，就需要私服了。

## Nexus安装

https://blog.csdn.net/yjclsx/article/details/83992321

## Nexus功能介绍

https://blog.csdn.net/yjclsx/article/details/83994535

## Nexus配置和使用

https://blog.csdn.net/yjclsx/article/details/83996224

## Nexus上传第三方jar包

上传含Maven依赖的jar包和源码包到Nexus并下载引入到其他项目中

- https://www.jianshu.com/p/b8ec688c388e
- https://blog.csdn.net/yjclsx/article/details/84027055