# 青铜 - 入门基础知识

> 经常有人问我，如果是零基础，那么如何快速入门Java开发呢？如果以一个后来者视角，确实适当的指引可以提高一些**认知的效率**。所以本节写给几乎没有啥基础，且想入门Java栈的开发的人。@pdai

## 入门与心态

致有小小野心的你

很多初学者会很迷茫，看到和想学的东西太多，定力又不够。一边感受着学习和工作（任务，通常是业务上的）本身的压力，一边期望深入学习（通常是技术点），一边还有着年轻人小小野心，但多数却又没有办法持之以恒；最后的结局是花费好长时间，在经验中摸着石头过河，所以**比起认知来说，认知效率更为重要**。这就是为什么我觉得我有必要提一下入门的心态。@pdai

这里不是鸡汤，提几个我认为重要的点：

- 行动很重要, 千里之行始于足下。
- 有人指路和没人指路差别很大。
- 阶段性目标。
- 获得正反馈。
- 圈子很重要。
- 战术上重视，战略上藐视。这绝对不是一句空话。

## 认知基础

花点时间了解下，一些项目做出来是什么样的，这样才能心中不慌；最怕说我学习了java，我能干啥呢？

## 后端基础

### Java基础

> 一定要看一本书，而且是一鼓作气。

我从来不会推荐初学者学习《Java编程思想》和《Java核心技术》，为什么？ 不是书不好，而是大多数人无法持之以恒看完的，而且我确定你读一遍无法读懂精髓，你也没有这么多时间和耐心，这会有挫败感。

但凡给刚入门的推荐一本书，我只推荐一本：

![](https://www.pdai.tech/images/project/project-a-books-1.png)

**为什么是这本呢**？

因为简单，因为你可以很快上手，因为很多都是代码块，可以很快看完，你可以有点成就感。

**怎么看呢**？

这本书也有700多页（哦天哪，都更新到700多页了），别怕，我们不是看全部，而是挑一部分看：下面是我从中截取要看的目录部分

```java
// 1部分 Java基础程序设计

1章 Java概述及开发环境搭建2
2章 简单的Java程序11
3章 Java基础程序设计16
4章 数组与方法60

// 2部分 Java面向对象程序设计

5章 面向对象（基础篇）88
6章 面向对象（高级篇）170
7章 异常的捕获及处理235
8章 包及访问控制权限252

// 3部分 Java应用程序设计

9章 多线程266 // 这章跳过不看
10章 泛型307
11章 Java常用类库336 // 第二遍再看
12章 Java IO397 // 这章跳过不看
13章 Java类集491
14章 枚举559
15章 Java反射机制577 // 第二遍再看
16章 Annotion609 // 第二遍再看
17章 Java数据库编程630 // 第二遍再看
18章 图形界面693 // 这章跳过不看
19章 Java网络编程785 // 这章跳过不看
20章 Java新IO801 // 这章跳过不看
```

**这本书看多久呢**？

> 注意了，这很重要，**最多一个星期**要看完我上面没标注的；有时间第二个星期，把第一遍和标注第二遍的再看一遍。

**有人问一开始要不要读其它书**？

> 我的观点很明确，入门阶段，这些书全不要看，书是很好，你吸收不了。你要有时间把上面那本书再看一遍。

![](https://www.pdai.tech/images/project/project-a-books-2.png)

**什么时候看其它书呢**？

> 至少你入门半年以上，你已经能通过Java来完成一些事情了，可以游刃有余的有时间来学习时；否则既要应付你手上的工作，又要深入，况且你要学的还多着呢，你不迷茫不焦虑才怪。

### SpringMVC基础

> 你可能了解和上手过SpringBoot，但是在学习SpringBoot之前，我推荐你学习SpringMVC。

如果要推荐一本《SpringMVC》相关的书，我只会推荐一本。

注意：只是一个文档，不是书

[跟开涛学 SpringMVC](/files/kaitao-springMVC.pdf)

![](https://www.pdai.tech/images/project/project-a-books-3.png)

**为什么推荐这本**？

> 因为简单，因为可以构筑你的web认知，因为你看的懂，这样循序渐进你可以很快理解。这就是我说的认知效率。

**里面技术是不是过时**？

> 表面是过时，其实被隐藏和封装起来了。这和构筑你的web认知没有关系。顺便说一句，通常一个入门者不会提出一个好的问题（包括这个问题），因为基于他现有的认知，他提出不了有价值的问题。

**这个文档看多久**？

> 推荐三天左右，你没看错，就是三天。

**里面有一些实例，我要不要自己玩转下里面的代码**？

> 想法是好，但是我不推荐你这么做。你有这时间，那就隔段时间再看一遍这个文档。为什么？因为你短期不会直接使用这个，只用了解思想和要点，还因为你还要更多时间去学其它的。

### SpringBoot基础

- **直接看Hello world的例子**

[Spring Boot - Helloworld](../spring/springboot-helloworld.md)

这部分内容的IDEA部分，也会下一节中介绍:

[青铜 - 入门开发IDE，Hello World](project-a-2-1.md)

- **如果要推荐本书**

看这本吧，为啥呢？因为这本写的真浅，入门的人很容易懂。

[Spring Boot实战](https://item.jd.com/11969881.html)

![](https://www.pdai.tech/images/project/project-a-books-11.png)

### 数据库基础

> 入门期，找个MySQL上手练练SQL就可以了。

- **MySQL的安装**

[MySQL 社区版下载和安装](https://dev.mysql.com/downloads/mysql/)

- **SQL 语句练习**
  - [SQL语言 - SQL语法基础](../db/sql-lan/sql-lan.md)
    - 本文包含了所有SQL语言的基础语法，并用例子的方式向你展示
  - [SQL语言 - SQL语句练习](../db/sql-lan/sql-lan-pratice.md)
    - 在上文学习了SQL的基本语法以后，本文将通过最经典的“教师-学生-成绩”表来帮助你练习SQL。@pdai
  - [SQL语言 - SQL题目进阶](../db/sql-lan/sql-lan-leetcode.md)
    - 接下来，通过Leetcode上的SQL题目进行进阶吧

## 前端基础

> 很多基础性的知识我只是列一下，知识点非常浅的，而且很多人其实已经有相关基础了。

### HTML基础

- **推荐学习内容**

[HTML 教程- (HTML5 标准)](https://www.runoob.com/html/html-tutorial.html)

![](https://www.pdai.tech/images/project/project-a-books-4.png)

- **学习多长时间**

很简单的内容，快速过一遍，2个小时左右。

### CSS基础

- **推荐学习内容**

[CSS 教程](https://www.runoob.com/css/css-tutorial.html)

![](https://www.pdai.tech/images/project/project-a-books-5.png)

- **学习多长时间**

很简单的内容，快速过一遍，2个小时左右。

### JS基础

- **推荐学习内容**

[JavaScript 教程](https://www.runoob.com/js/js-tutorial.html)

![](https://www.pdai.tech/images/project/project-a-books-6.png)

- **学习多长时间**

很简单的内容，快速过一遍，3个小时左右。

### Jquery基础

> 选学，老的前端项目会使用JQuery

- **推荐学习内容**

[jQuery 教程](https://www.runoob.com/jquery/jquery-tutorial.html)

![](https://www.pdai.tech/images/project/project-a-books-7.png)

- **学习多长时间**

很简单的内容，快速过一遍，2个小时左右。

### BootStrap基础

> 选学，老的前端项目会使用BootStrap布局

- **推荐学习内容**

[Bootstrap 教程](https://www.runoob.com/bootstrap/bootstrap-tutorial.html)

![](https://www.pdai.tech/images/project/project-a-books-8.png)

- **学习多长时间**

很简单的内容，快速过一遍，2个小时左右。

### VueJS基础

> 选学，国内前端栈常用框架

- **推荐学习内容**

[VueJS 官网](https://cn.vuejs.org/v2/guide/)

![](https://www.pdai.tech/images/project/project-a-books-9.png)

如果你看官网没有定力或者收获小，可以看个视频教程

[vue2.5入门](https://www.imooc.com/learn/980)

![](https://www.pdai.tech/images/project/project-a-books-10.png)

- **学习多长时间**

3个小时左右。

## 再谈学习效率

注意

关于每一项给的时间，看上去非常紧，为什么只推荐这么点时间：

- 大多数情况下，你不会是真正的0基础的；
- 在入门的时候，效率是极其重要的；一定要给自己设置Deadline，因为无数次的经验证明Deadline是最好的效率推手；
- 即便你花的时间远大于我给的设定，没关系，尽你最大能力去完成，你的认知效率已经高于其它人了。

- [后端基础](#%e5%90%8e%e7%ab%af%e5%9f%ba%e7%a1%80)
  - [Java基础](#java%e5%9f%ba%e7%a1%80) // 5天
  - [SpringMVC基础](#springmvc%e5%9f%ba%e7%a1%80) // 3天
  - [SpringBoot基础](#springboot%e5%9f%ba%e7%a1%80) // 3天
  - [数据库基础](#%e6%95%b0%e6%8d%ae%e5%ba%93%e5%9f%ba%e7%a1%80) // 1天
- [前端基础](#%e5%89%8d%e7%ab%af%e5%9f%ba%e7%a1%80)
  - [HTML基础](#html%e5%9f%ba%e7%a1%80) // 2小时
  - [CSS基础](#css%e5%9f%ba%e7%a1%80) // 2小时
  - [JS基础](#js%e5%9f%ba%e7%a1%80) // 3小时
  - [Jquery基础](#jquery%e5%9f%ba%e7%a1%80) // 选学 2小时
  - [BootStrap基础](#bootstrap%e5%9f%ba%e7%a1%80) // 选学 2小时
  - [VueJS基础](#vuejs%e5%9f%ba%e7%a1%80) // 选学 2小时